"""Independent finite-channel and direct factorization audit."""
import json,math
from pathlib import Path
import numpy as np
from compute import b8,prepare,residue_fraction,validate
ROOT=Path(__file__).resolve().parent
checks={};rng=np.random.default_rng(20261003)
# Explicit Kraus maps from six input labels to two orthogonal internal modes.
for strength in [0,.2,1]:
    mask=np.array([0,1,1,0,1,0]);ks=[]
    for j,s in enumerate(mask):
        for output,prob in enumerate([1-strength*s,strength*s]):
            k=np.zeros((2,6));k[output,j]=math.sqrt(prob);ks.append(k)
    complete=sum(k.T@k for k in ks)
    checks[f'kraus_complete_{strength}']=np.allclose(complete,np.eye(6))
    choi=sum(np.outer(k.reshape(-1,order='F'),k.reshape(-1,order='F')) for k in ks)
    checks[f'choi_positive_{strength}']=np.linalg.eigvalsh(choi).min()>-1e-12
    for i in range(20):
        x=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6));rho=x@x.conj().T;rho/=np.trace(rho)
        out=sum(k@rho@k.T for k in ks)
        expected=strength*float(np.sum(np.real(np.diag(rho))[mask==1]))
        checks[f'channel_formula_{strength}_{i}']=np.allclose(out,np.diag([1-expected,expected]))
        checks[f'channel_positive_trace_{strength}_{i}']=np.linalg.eigvalsh(out).min()>-1e-12 and abs(np.trace(out)-1)<1e-12
# Scalar integer trial factorization does not call the parent's sieve or valuations.
h=json.loads((ROOT.parent/'shutter_v0_8/handoff.json').read_text())
def trial_prime(n):return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
def v3(n):
    count=0
    while n%3==0:count+=1;n//=3
    return count
for epsilon in [-.15,0,.15]:
    numerator=[];denominator=[]
    for n in range(2,10001):
        if n%2 and not trial_prime(n):
            w=n**(-h['alpha'])*math.exp(epsilon*v3(n));denominator.append(w)
            if v3(n)%2:numerator.append(w)
    direct=math.fsum(numerator)/math.fsum(denominator)
    n,vec,p=b8.branches(10000,h['alpha'],h['beta'],{3:{'epsilon':epsilon}})
    checks[f'direct_scalar_selector_{epsilon}']=abs(direct-residue_fraction(n,vec['phi'],3))<2e-12
r=json.loads((ROOT/'results.json').read_text());rows=r['rows'];base=next(x for x in rows if x['case']=='baseline' and x['strength']==.2)
phase=next(x for x in rows if x['case']=='p3_phase' and x['strength']==.2)
checks['declared_dephasing_phase_invariant']=abs(base['excited_population']-phase['excited_population'])<1e-12
low=next(x for x in rows if x['case']=='p3_low' and x['strength']==.2);high=next(x for x in rows if x['case']=='p3_high' and x['strength']==.2)
checks['SOURCE_intensity_changes_internal_population']=abs(high['excited_population']-low['excited_population'])>.001
checks['source_D_R_preserved_by_preparation']=all(abs(x['phi_fraction']+x['D_fraction']+x['return_fraction']-1)<2e-11 for x in rows)
for strength in [-1,2,float('nan')]:
    try:prepare(np.array([1.,0]),np.array([0.,1]),.4,strength)
    except ValueError:checks[f'invalid_strength_{strength}']=True
    else:checks[f'invalid_strength_{strength}']=False
if not all(checks.values()):raise AssertionError([k for k,v in checks.items() if not v])
(ROOT/'audit.json').write_text(json.dumps({'seed':20261003,'checks':{k:bool(v) for k,v in checks.items()},'checks_passed':int(sum(checks.values()))},indent=2)+'\n')
print('Independent audit:',len(checks),'checks passed')
