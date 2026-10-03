"""Exact block representation of a dephased address/internal/carrier CQ state.
Run from an extracted package root or set WRRA_REPO to the frozen checkout.
No dense million-address tensor matrix is allocated; contractions are exact.
"""
from pathlib import Path
import os,sys,importlib.util,json,hashlib
import numpy as np
R=Path(__file__).resolve().parent
repo=Path(os.environ.get('WRRA_REPO',str(R/'wrra-m')))
if not repo.exists(): repo=R.parents[1]/'wrra-m'
path=repo/'upstream/residue_current_v0_9/compute.py'
spec=importlib.util.spec_from_file_location('bridge_parent',path)
up=importlib.util.module_from_spec(spec);spec.loader.exec_module(up)
cfg=json.loads((path.parent/'inputs.json').read_text())
inp=json.loads((up.P6/'inputs.json').read_text())
m,p,e,V,g,c=up.v6.construct(inp)
exc=V[:,cfg['excited_mode_index']]
H=p['delta_MeV']*(m['h0']-p['x']*m['bounded'])
gap=float(exc@H@exc-g@H@g)
carrier=np.eye(128)/128
checks=[];rows=[]
def ck(name,ok): checks.append({'name':name,'passed':bool(ok)})
ck('orthonormal internal support',abs(g@exc)<1e-10 and abs(g@g-1)<1e-10 and abs(exc@exc-1)<1e-10)
ck('internal basis dimension',len(g)==95)
ck('carrier positivity/trace',np.linalg.eigvalsh(carrier).min()>0 and abs(np.trace(carrier)-1)<1e-12)
h=json.loads((up.P8/'handoff.json').read_text())
ops={(q,s):up.v6.currents.full_charge(c,q,s) for q in cfg['Q2_GeV2'] for s in ['proton','neutron']}
for case in cfg['source_controls']:
 n,vec,probs=up.b8.branches(h['N'],h['alpha'],h['beta'],case['controls'])
 w=np.abs(vec['phi'])**2;f=float(w.sum());w=w/f
 selector=(up.b8.parent.valuations(n,3)%2==1)
 t=float(w@selector);a=cfg['reference_preparation_strength'];pop=a*t
 # Each address block has eigenvalues 1-a*selector and a*selector;
 # carrier factor I/128 adds a positive normalized common transport state.
 rho=(1-pop)*np.outer(g,g)+pop*np.outer(exc,exc)
 tag=case['name'];ck(tag+' instrument trace',abs(sum(probs.values())-1)<2e-11)
 ck(tag+' conditional address trace',abs(w.sum()-1)<2e-11)
 ck(tag+' all block positivity',0<=a<=1 and np.all(w>=0))
 ck(tag+' internal marginal positivity/trace',np.linalg.eigvalsh(rho).min()>-2e-11 and abs(np.trace(rho)-1)<2e-11)
 ck(tag+' weighted phi trace',abs(f*np.trace(rho)-probs['phi'])<2e-11)
 energy=pop*gap;ck(tag+' same H energy',abs(np.trace(rho@H)-g@H@g-energy)<2e-8)
 # A diagonal address-sensitive load probe, using the downstream response shape.
 # This is NOT an additional cosmic energy density or a measured particle load.
 response=1+.25*np.log(n)/np.log(h['N'])
 joint=float(w@(response*a*selector))*gap
 product=float(w@response)*energy
 predicted=a*gap*(float(w@(response*selector))-float(w@response)*t)
 ck(tag+' covariance identity',abs(joint-product-predicted)<2e-10)
 ck(tag+' correlation detected',abs(joint-product)>1e-5)
 ck(tag+' joint trace equals address marginal',abs(float(w@((1-a*selector)+a*selector))-1)<2e-11)
 ck(tag+' product limit constant response',abs(float(w@(a*selector))*gap-energy)<2e-9)
 currents=[]
 for (q,s),op in ops.items():
  jg=float(g@op@g);je=float(exc@op@exc)
  direct=float(w@((1-a*selector)*jg+(a*selector)*je))
  marginal=float(np.trace(rho@op))
  ck(tag+f' {s} Q2={q} marginal-current',abs(direct-marginal)<2e-10)
  cj=float(w@(response*((1-a*selector)*jg+a*selector*je)))
  cp=float(w@response)*marginal
  cv=a*(je-jg)*(float(w@(response*selector))-float(w@response)*t)
  ck(tag+f' {s} Q2={q} correlated-current identity',abs(cj-cp-cv)<2e-10)
  currents.append({'Q2_GeV2':q,'species':s,'GE':marginal,'address_weighted_joint':cj,'address_weighted_product':cp,'difference':cj-cp})
 ref=json.loads((path.parent/'results.json').read_text())
 match=next(x for x in ref['rows'] if x['case']==tag and x['strength']==a)
 ck(tag+' upstream reference excitation',abs(energy-match['conditional_excitation_MeV'])<2e-8)
 rows.append({'case':tag,'four_branch_probabilities':probs,'selector_fraction':t,'excited_population':pop,'conditional_excitation_MeV':energy,'probe_joint_MeV':joint,'probe_product_MeV':product,'probe_difference_MeV':joint-product,'currents':currents})
np.savez_compressed(R/'internal_and_carrier_basis.npz',ground=g,excited=exc,H_MeV=H,carrier=carrier)
out={'version':'bridge-0.2','state':'conditional phi CQ blocks, normalized; D and return retain original branch ledgers without nucleon preparation','representation':'exact diagonal-address blocks, two-mode internal support in frozen 95-dimensional basis, 128-dimensional stationary carrier','address_dephasing':'inherited upstream measure-and-prepare scope; no coherent address preservation claim','rows':rows,'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'physical_scope':'no new energy supply, particle number, SI time, durable record or coupled gravity dynamics','source_sha256':{str(p.relative_to(R/'wrra-m')):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'wrra-m').rglob('*')) if p.is_file() and p.suffix in ['.py','.json'] and '__pycache__' not in str(p)}}
(R/'results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'passed':out['passed'],'failed':out['failed'],'rows':[{k:v for k,v in r.items() if k in ['case','conditional_excitation_MeV','probe_difference_MeV']} for r in rows]}))
if out['failed']: raise SystemExit(1)
