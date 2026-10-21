"""Wonsik Reality-Renderer Architecture: branch-blind combiner and driven phase law.
Finite positive time-dependent Hamiltonian; apparatus clock remains external.
"""
from pathlib import Path
import numpy as np,json,math,csv,hashlib
P=Path(__file__).resolve().parent;C=70;N=1015000;SH=(213,65,77)
HBAR=1.054571817e-34;TAU=1.481301966415863e-21;EV=1.602176634e-19
UNIT=HBAR/TAU/EV/1e3;checks={}
def ck(n,v):
 checks[n]=bool(v)
 if not v:raise AssertionError(n)
def csvwrite(name,rows):
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
def main():
 for fn,meta in json.loads((P/'input_manifest.json').read_text()).items():ck('hash_'+fn,hashlib.sha256((P/'inputs'/fn).read_bytes()).hexdigest()==meta['sha256'])
 old=json.loads((P/'inputs/previous_results.json').read_text());gam=np.loadtxt(P/'inputs/zero_heights.csv',skiprows=1)
 # Same universal distinct-prime folding selection, all addresses evaluated.
 prime=np.ones(N+1,bool);prime[:2]=False
 for p in range(2,math.isqrt(N)+1):
  if prime[p]:prime[p*p::p]=False
 omega=np.zeros(N+1,np.int8)
 for p in np.flatnonzero(prime):omega[p::p]+=1
 ids=np.flatnonzero(omega>=2);idx=tuple(ids%m for m in SH);ln=np.log(ids)
 axes=[]
 for a,m in enumerate(SH):
  s=[1]*3;s[a]=m;axes.append((2*np.pi*np.fft.fftfreq(m)).reshape(s))
 rad=np.sqrt(sum(a*a for a in axes));band=rad<=.8*np.pi
 def ft(v):
  x=np.zeros(SH,complex);x[idx]=v;return np.fft.fftn(x,norm='ortho')
 def E(f):return float(np.sum(rad*abs(f)**2))
 # Complete-graph contrast Laplacian C I - 11^T: unique zero eigenspace.
 L=C*np.eye(C)-np.ones((C,C));vals=np.linalg.eigvalsh(L);u=np.ones(C)/np.sqrt(C)
 ck('unique_branchblind_ray',np.sum(abs(vals)<1e-10)==1)
 ck('contrast_gap',np.max(abs(vals[1:]-C))<2e-12)
 ck('uniform_contrast_zero',abs(u@L@u)<1e-12)
 rng=np.random.default_rng(20261021)
 for j in range(30):
  b=rng.normal(size=C)+1j*rng.normal(size=C);b/=np.linalg.norm(b)
  ck('contrast_identity_'+str(j),abs((b.conj()@L@b).real-(C-abs(b.sum())**2))<1e-11)
 rows=[];paths=[];noise=[];summ={}
 for prep,alpha in [('uniform',0.),('inherited_alpha',1.8996877935161325)]:
  print(prep,flush=True);s=ids.astype(float)**(-alpha/2);s/=np.linalg.norm(s)
  w=s*s;ein=E(ft(s));Bmean=float(gam.mean()*np.dot(w,ln));bmax=float(gam[-1]*np.log(N))
  filt=np.zeros(len(ids),complex);emix=0.;pmixband=0.;emixband=0.;axis_mix=np.zeros(SH[0])
  for j,g in enumerate(gam):
   phase=np.exp(-1j*g*ln);filt+=phase/C;f=ft(s*phase)
   emix+=E(f)/C;pmixband+=float(np.sum(abs(f[band])**2))/C
   emixband+=float(np.sum(rad[band]*abs(f[band])**2))/C
   psi=np.fft.ifftn(f*band*np.exp(-1j*rad),norm='ortho')
   axis_mix+=np.sum(abs(psi)**2,axis=(1,2))/C
  out=ft(s*filt);pcoh=float(np.sum(abs(out)**2));ecoh=E(out)
  pband=float(np.sum(abs(out[band])**2));eband=float(np.sum(rad[band]*abs(out[band])**2))
  cohpsi=np.fft.ifftn(out*band*np.exp(-1j*rad),norm='ortho');axcoh=np.sum(abs(cohpsi)**2,axis=(1,2))
  prev=next(x for x in old['rows'] if x['preparation']==prep and x['case']=='zeta')
  ck(prep+'_endpoint_probability',abs(pcoh-prev['pass_probability'])<2e-14)
  ck(prep+'_endpoint_work',abs((emix-ein)*UNIT-prev['phase_work_mean_keV'])<2e-10)
  ck(prep+'_mixture_band_marginal',abs(float(axis_mix.sum())-pmixband)<2e-14)
  # Exact solution of H_total(t)=H0+U0(t) B U0(t)^dagger:
  # U_total(t)=U0(t) exp[-i B t/hbar]. Here t/TAU is s_time.
  # Mean V is constant Bmean; turning it on/off returns the same Bmean.
  for st in [0.,.25,.5,.75,1.]:
   k=sum(np.exp(-1j*g*ln*st) for g in gam)/C
   f=ft(s*k)*np.exp(-1j*rad*st);p=float(np.sum(abs(f)**2))
   paths.append({'preparation':prep,'time_over_tau':st,'selected_port_probability':p,'selected_weighted_energy_keV':E(f)*UNIT})
  g=np.load(P/'inputs'/(prep+'_combiner.npz'));b=g['coefficients'];contrast=float((b.conj()@L@b).real/C)
  ck(prep+'_optimized_nonblind',contrast>1e-4)
  row={'preparation':prep,'original_pass_probability':pcoh,'optimized_contrast_normalized':contrast,
   'mean_control_potential_keV':Bmean*UNIT,'control_operator_norm_keV':bmax*UNIT,
   'switch_on_mean_keV':Bmean*UNIT,'switch_off_mean_keV':-Bmean*UNIT,
   'during_drive_mean_work_keV':(emix-ein)*UNIT,'endpoint_all_ports_energy_keV':emix*UNIT}
  rows.append(row)
  for sig in [0.,.05,.1,.25,.5,1.,2.,4.]:
   eta=math.exp(-sig*sig);prob=eta*pcoh+(1-eta)/C
   energy=eta*ecoh+(1-eta)*emix/C
   pb=eta*pband+(1-eta)*pmixband/C;eb=eta*eband+(1-eta)*emixband/C
   axis=eta*axcoh+(1-eta)*axis_mix/C
   ck(prep+'_noise_probability_'+str(sig),abs(float(axis.sum())-pb)<2e-14)
   ck(prep+'_noise_energy_positive_'+str(sig),0<=energy<=emix+1e-12)
   noise.append({'preparation':prep,'phase_std_rad':sig,'coherence_eta':eta,'pass_probability':prob,
    'band_probability':pb,'selected_weighted_energy_keV':energy*UNIT,
    'band_conditional_energy_keV':eb/pb*UNIT,'band_axis0_TV_from_noiseless':float(.5*np.sum(abs(axis/pb-axcoh/pband)))})
  summ[prep]={'equal_pass':pcoh,'fully_dephased_pass':1/C,'band_pass':pband,
   'fully_dephased_band_pass':pmixband/C,'mean_control_potential_MeV':Bmean*UNIT/1e3,
   'optimized_contrast_normalized':contrast,'signed_switch_sum_keV':0.}
 csvwrite('drive_energy.csv',rows);csvwrite('driven_path.csv',paths);csvwrite('phase_noise.csv',noise)
 r={'architecture':'Wonsik Reality-Renderer Architecture','version':'zeta symmetry and drive v0.2','summaries':summ,
  'constants':{'C':C,'N':N,'selected_addresses':len(ids),'tau_s':TAU,'energy_unit_keV':UNIT},
  'checks':checks,'all_checks_pass':all(checks.values()),
  'scope':'Branch-blind rank-one readout contract selects equal combination. Positive prescribed Hamiltonian executes old phase plus physical propagation in one interval. External clock/control and reset remain open. Not unique zeta selection or particle spectrum derivation.'}
 (P/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps({'check_count':len(checks),'summaries':summ},indent=2),flush=True)
if __name__=='__main__':main()
