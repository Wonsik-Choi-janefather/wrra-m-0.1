"""Separate checks: explicit finite DFT port dilation and SciPy FFT full readout.
No calls into compute.py; test assertions are internal numerical checks.
"""
from pathlib import Path
import numpy as np,json,math,hashlib
from scipy.fft import fftn
import mpmath as mp
P=Path(__file__).resolve().parent;r=json.loads((P/'results.json').read_text());checks={};metrics={}
def ck(n,b):
 checks[n]=bool(b)
 if not b:raise AssertionError(n)
C=70;gamma=np.loadtxt(P/'inputs/zero_heights.csv',skiprows=1)
mp.mp.dps=35
res=max(float(abs(mp.zeta(mp.mpc('.5',str(g))))) for g in gamma)
ck('rounded_zero_residual',res<1e-10);metrics['rounded_zero_max_zeta_residual']=res
# Explicit 70-port unitary on a separate 53-site ring, nontrivial preparation.
L=53;n=np.arange(1,L+1);s=n.astype(float)**(-.6);s/=np.linalg.norm(s)
phase=np.exp(-1j*gamma[:,None]*np.log(n));branches=phase*s/np.sqrt(C)
ports=np.fft.fft(branches,axis=0,norm='ortho')
k=abs(2*np.pi*np.fft.fftfreq(L));e=lambda a:float(np.sum(k*abs(np.fft.fft(a,axis=-1,norm='ortho'))**2))
ck('explicit_port_norm',abs(np.sum(abs(ports)**2)-1)<1e-14)
ck('selected_port_formula',np.max(abs(ports[0]-phase.mean(axis=0)*s))<1e-14)
ck('full_ports_energy_equals_branch_mixture',abs(e(ports)-e(branches))<1e-14)
ck('inverse_ports_recovers_state',np.max(abs(np.fft.ifft(ports,axis=0,norm='ortho')-branches))<1e-14)
ck('conditional_postselection_not_energy_gain',abs(e(ports[0])+e(ports[1:])-e(branches))<1e-14)
# Permuting zero labels keeps uniform port and energy mixture unchanged.
ck('permutation',np.max(abs(phase[::-1].mean(0)-phase.mean(0)))<1e-14)
# Common height offset is address-dependent, not a common global phase.
shift=np.exp(-.5j*np.log(n));ck('height_shift_identity',np.max(abs(np.exp(-1j*(gamma[:,None]+.5)*np.log(n)).mean(0)-phase.mean(0)*shift))<1e-13)
ck('global_phase_invariance',abs(e(ports[0]*np.exp(.37j))-e(ports[0]))<1e-14)
# Full-N sieve independent of original omega accumulation: smallest prime factor.
N=1015000;spf=np.zeros(N+1,np.int32)
for p in range(2,N+1):
 if spf[p]==0:spf[p::p]=np.where(spf[p::p]==0,p,spf[p::p])
ids=np.arange(2,N+1);q=ids.copy();first=spf[ids];q//=first
while True:
 mask=(q>1)&(q%first==0)
 if not mask.any():break
 q[mask]//=first[mask]
ids=ids[q>1];ck('independent_selected_count',len(ids)==935155)
shape=(213,65,77);idx=tuple(ids%m for m in shape)
axes=[]
for j,m in enumerate(shape):
 sh=[1]*3;sh[j]=m;axes.append((np.fft.fftfreq(m)*2*np.pi).reshape(sh))
rad=np.sqrt(sum(x*x for x in axes));band=rad<=.8*np.pi;unit=r['constants']['energy_unit_keV']
filt=sum(np.exp(-1j*g*np.log(ids)) for g in gamma)/C
for prep,alpha in [('uniform',0),('inherited_alpha',1.8996877935161325)]:
 seed=ids.astype(float)**(-alpha/2);seed/=np.sqrt(seed@seed)
 a=np.zeros(shape,complex);a[idx]=seed*filt;f=fftn(a,norm='ortho',workers=2);p=abs(f)**2
 row=next(v for v in r['rows'] if v['case']=='zeta' and v['preparation']==prep)
 ck(prep+'_scipy_pass',abs(float(p.sum())-row['pass_probability'])<2e-14)
 ck(prep+'_scipy_band',abs(float(p[band].sum())-row['band_detect_probability'])<2e-14)
 ck(prep+'_scipy_energy',abs(float(np.sum(p*rad))*unit-row['pass_energy_weighted_keV'])<2e-11)
 g=np.load(P/(prep+'_combiner.npz'));G=g['gram'];b=g['coefficients']
 ev=g['eigenvalues'][-1];residual=np.linalg.norm(G@b-ev*b)
 ck(prep+'_eigen_residual',residual<1e-12)
 # Variational bound for 100 random normalized combining vectors, same Gram.
 rng=np.random.default_rng(20261021);B=rng.normal(size=(C,100))+1j*rng.normal(size=(C,100));B/=np.linalg.norm(B,axis=0)
 ck(prep+'_variational_bound',np.max(np.sum(B.conj()*(G@B),axis=0).real)<=ev+1e-12)
 metrics[prep+'_eigen_residual']=float(residual)
metrics['explicit_port_energy_error']=abs(e(ports)-e(branches))
(P/'independent_verification.json').write_text(json.dumps({'checks':checks,'metrics':metrics,'all_checks_pass':all(checks.values())},indent=2));print(json.dumps({'checks':len(checks),'metrics':metrics},indent=2))
