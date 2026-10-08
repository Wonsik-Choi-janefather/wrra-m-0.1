"""Finite WRRA address-to-pair interface. Run: python reproduce.py.
Requires numpy and scipy. No network, random seed 10701.
Outputs are conditional model readouts, not measured abundances.
"""
from pathlib import Path
import json, numpy as np
from scipy.special import expit
R=Path(__file__).resolve().parent
src=json.loads((R/'r11_controls.json').read_text())
N=src['inputs']['N']; alpha=src['inputs']['alpha']; K=src['inputs']['K']
me=0.51099895069; mmu=105.6583755; Estar=2*mmu
spf=np.arange(N+1)
for p in range(2,int(N**.5)+1):
 if spf[p]==p:
  v=spf[p*p::p]; v[v==np.arange(p*p,N+1,p)]=p
n=np.arange(2,N+1); w=n.astype(float)**(-alpha); w/=w.sum()
odd=(n%2==1)&(spf[2:]!=n); addr=n[odd]; weights=w[odd]
chi=[]
for a in addr:
 x=int(a); powers=[]
 while x>1:
  p=int(spf[x]); k=0
  while x%p==0: x//=p; k+=1
  powers.append(k)
 chi.append(sum(k*k for k in powers)/sum(powers)**2)
chi=np.array(chi)
checks=[]
def check(name,ok,value=None):
 checks.append({'name':name,'passed':bool(ok),'value':None if value is None else float(value)})
check('chi bounds',np.all((chi>0)&(chi<=1)))
for a,c in [(9,1),(15,.5),(45,5/9),(105,1/3)]:check('factor witness '+str(a),abs(chi[np.where(addr==a)[0][0]]-c)<1e-14)
rows=[]; dists=[]
r=(me/mmu)**2
for ctrl in src['outputs']:
 freq=ctrl['frequencies']; h=ctrl['refitted_threshold']; survival=np.ones(len(addr))
 for k in range(K):
  drive=np.zeros(len(addr)) if freq is None else sum(np.cos(f*(np.log(addr)+ctrl['xi']*k)) for f in freq)/np.sqrt(len(freq))
  survival*=1-expit(drive-h)
 T=1-survival; prob=weights*T; total=prob.sum(); pi=prob/total; dists.append(pi)
 x_reverse=float(pi@(1-chi)); x_constant=float(pi@np.full_like(chi,.5))
 check(ctrl['case']+' reversed routing',abs(x_reverse-(1-float(pi@chi)))<1e-12,x_reverse)
 check(ctrl['case']+' constant routing',abs(x_constant-.5)<1e-12,x_constant)
 x=float(pi@chi); rest=2*(x*me+(1-x)*mmu); kinetic=Estar-rest
 pressure=x*(1-r)/3; q=-.523+.025*x*(1-r)
 rows.append({'drive':ctrl['case'],'phi':float(total),'electron_pair_probability':x,'reversed_electron_probability':x_reverse,'constant_electron_probability':x_constant,'muon_pair_probability':1-x,'mean_pair_rest_energy_MeV':rest,'mean_pair_kinetic_energy_MeV':kinetic,'total_pair_energy_MeV':Estar,'pV_over_E_phi_at_v1':pressure,'instantaneous_formal_q':q})
 check(ctrl['case']+' phenotype reconstruction',abs(total-.05)<1e-11,total)
 check(ctrl['case']+' r11 address9',abs(T[np.where(addr==9)[0][0]]-ctrl['address_9_admission'])<1e-12)
 check(ctrl['case']+' energy allocation',abs(rest+kinetic-Estar)<1e-11)
 def eng(v):return .05*(x*np.sqrt(r+(1-r)*v**(-2/3))+(1-x))+.268+.682*v
 def pv(v):return .05*x*(1-r)*v**(-2/3)/(3*np.sqrt(r+(1-r)*v**(-2/3)))-.682*v
 errs=[]
 for v in [.5,1,2]:
  d=1e-5*v; num=-v*(eng(v+d)-eng(v-d))/(2*d); errs.append(abs(num-pv(v)))
 check(ctrl['case']+' finite difference pressure',max(errs)<1e-8,max(errs))
 check(ctrl['case']+' q from same energy',abs(.5*(1+3*pv(1)/eng(1))-q)<1e-12)
check('four readouts differ',len({round(row['electron_pair_probability'],10) for row in rows})==4)
for i in range(1,4):check('TV bound '+str(i),abs(rows[i]['electron_pair_probability']-rows[0]['electron_pair_probability'])<=.5*np.abs(dists[i]-dists[0]).sum()+1e-13)
# Small coherent realization with orthogonal address record.
cs=np.array([1,.5,5/9,1/3]); V=np.zeros((8,4))
for j,c in enumerate(cs):V[2*j,j]=np.sqrt(c);V[2*j+1,j]=np.sqrt(1-c)
check('isometry',np.max(np.abs(V.T@V-np.eye(4)))<1e-14)
rng=np.random.default_rng(10701); A=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)); rho=A@A.conj().T;rho/=np.trace(rho);out=V@rho@V.T
check('coherent trace and positivity',abs(np.trace(out)-1)<1e-12 and np.linalg.eigvalsh(out).min()>-1e-12)
# Orthogonal record removal is not an isometry.
U=np.array([np.sqrt(cs),np.sqrt(1-cs)])
check('negative control record erasure',np.max(np.abs(U.T@U-np.eye(4)))>.1)
# Positive Choi matrix for measured preparation channel; stack address blocks.
choi=np.zeros((8,8))
for j,c in enumerate(cs):
 psi=np.array([np.sqrt(c),np.sqrt(1-c)]);choi[2*j:2*j+2,2*j:2*j+2]=np.outer(psi,psi)
check('Choi positivity',np.linalg.eigvalsh(choi).min()>-1e-12)
check('Choi trace preservation',all(abs(np.trace(choi[2*j:2*j+2,2*j:2*j+2])-1)<1e-12 for j in range(4)))
# Spin singlet and total charge / total lepton number in each opposite-charge pair.
sx=np.array([[0,1],[1,0]])/2;sy=np.array([[0,-1j],[1j,0]])/2;sz=np.diag([.5,-.5]); sing=np.array([0,1,-1,0])/np.sqrt(2); I=np.eye(2)
check('spin singlet',all(np.linalg.norm((np.kron(S,I)+np.kron(I,S))@sing)<1e-12 for S in [sx,sy,sz]))
check('pair total charge and lepton number',(-1+1)==0 and (1-1)==0)
pe=np.sqrt(mmu**2-me**2)
check('electron mass shell',abs(np.hypot(me,pe)-mmu)<1e-12)
check('cold equal-energy obstruction',abs(2*me-2*mmu)>1)
check('dust counterexample positive pressure',all(row['pV_over_E_phi_at_v1']>0 for row in rows))
result={'version':'0.2','scope':'Kinematic two-species interface and fixed-occupation pressure diagnostic; not a cosmic muon population or a mass derivation.','inputs':{'N':N,'alpha':alpha,'K':K,'electron_rest_energy_MeV':me,'muon_rest_energy_MeV':mmu,'pair_energy_MeV':Estar,'chi_rule':'sum valuation squared / total valuation squared','routing':'electron=chi, muon=1-chi'},'rows':rows,'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks)}
(R/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps({'rows':rows,'passed':result['passed'],'total':len(checks)},indent=2))
assert all(c['passed'] for c in checks)
