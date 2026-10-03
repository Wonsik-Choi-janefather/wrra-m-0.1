"""Adversarial contracts, pre-review numerical regression, and clean replay."""
from pathlib import Path
import importlib.util,copy,json,sys,subprocess,os,tempfile,shutil,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent;UP=ROOT.parent
checks={}
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
v10=load('review10',UP/'generator_v0_10/compute.py');v9=v10.v9;b8=v9.b8;s8=load('review8',UP/'shutter_v0_8/compute.py')
def reject(name,fn):
 try:fn()
 except ValueError:checks[name]=True
 else:checks[name]=False
# Strict Hermiticity, no silently accepted bools, and zero-probability endpoints.
rho=np.eye(3)/3;bad=rho.copy();bad[0,1]=1e-7
reject('08_nonhermitian_rejected',lambda:s8.shutter(bad,.5))
reject('08_boolean_eta_rejected',lambda:s8.shutter(rho,True))
reject('08_boolean_draw_rejected',lambda:s8.select_record(rho,True))
for probs in [[1,0,0],[0,1,0],[0,0,1],[.5,.5,0]]:
 for draw in [0.,.5,float(np.nextafter(1.,0.))]:
  j,state=s8.select_record(np.diag(probs),draw);checks[f'08_zero_branch_{probs}_{draw}']=probs[j]>0 and np.trace(state)==1
keys=['phi','D','initial_reflection','normal_return'];a={k:np.array([1. if i==0 else 0.,0.]) for i,k in enumerate(keys)}
for kind in ['nan','empty','shape','missing','norm']:
 bad=copy.deepcopy(a)
 if kind=='nan':bad['phi'][0]=np.nan
 if kind=='empty':bad={k:np.array([]) for k in keys}
 if kind=='shape':bad['D']=np.zeros(3)
 if kind=='missing':del bad['D']
 if kind=='norm':bad['phi']*=2
 reject('08_branch_'+kind,lambda bad=bad:b8.record(bad,0.))
rev=dict(reversed(list(a.items())))
checks['08_branch_order_is_named']=b8.record(rev,.9)[0]=='phi'
g=np.array([1.,0.]);e=np.array([0.,1.])
for kind in ['nan','shape','norm','orthogonality','boolean']:
 gg=g.copy();ee=e.copy();strength=.2
 if kind=='nan':gg[0]=np.nan
 if kind=='shape':ee=np.zeros(3)
 if kind=='norm':gg*=2
 if kind=='orthogonality':ee=gg
 if kind=='boolean':strength=True
 reject('09_preparation_'+kind,lambda gg=gg,ee=ee,strength=strength:v9.prepare(gg,ee,.4,strength))
for kind,n,v,p in [('order',[9,3],[1,1],3),('duplicates',[3,3],[1,1],3),('float',[3.,9.],[1,1],3),('nan',[3,9],[np.nan,1],3),('shape',[3,9],[1],3),('prime',[3,9],[1,1],4),('zero',[3,9],[0,0],3)]:
 reject('09_selector_'+kind,lambda n=n,v=v,p=p:v9.residue_fraction(np.array(n),np.array(v),p))
cfg=json.loads((UP/'residue_current_v0_9/inputs.json').read_text())
for kind in ['empty','duplicate','baseline','reference']:
 bad=copy.deepcopy(cfg)
 if kind=='empty':bad['source_controls']=[]
 if kind=='duplicate':bad['source_controls'].append(bad['source_controls'][0])
 if kind=='baseline':bad['source_controls'][0]['controls']={'2':{'epsilon':.1}}
 if kind=='reference':bad['reference_preparation_strength']=.3
 reject('09_config_'+kind,lambda bad=bad:v9.validate(bad))
# Frozen real adapter must reject complex input rather than miscompute missing conjugation.
c={'g':g}
reject('09_complex_current_rejected',lambda:v9.state_current_context(c,g.astype(complex)*1j))
inp=json.loads((UP/'generator_v0_10/inputs.json').read_text())
for kind in ['baseline','duplicate_protocol','empty_protocol','reference','leakage','release','Q2']:
 bad=copy.deepcopy(inp)
 if kind=='baseline':bad['source_cases']=[x for x in bad['source_cases'] if x['name']!='baseline']
 if kind=='duplicate_protocol':bad['protocols'].append(bad['protocols'][0])
 if kind=='empty_protocol':bad['protocols']=[]
 if kind=='reference':bad['protocols'][0]['release_fractions']=[1,1]
 if kind=='leakage':bad['protocols'][1]['leakage']=np.nan
 if kind=='release':bad['protocols'][1]['release_fraction']=True
 if kind=='Q2':bad['record_readout_Q2_GeV2']=True
 reject('10_config_'+kind,lambda bad=bad:v10.validate(bad))
# Compare physical outputs; provenance bytes intentionally change after implementation review.
old09=json.loads((ROOT/'baseline/residue_current_v0_9/results.json').read_text());new09=json.loads((UP/'residue_current_v0_9/results.json').read_text())
checks['09_all_numerical_rows_unchanged']=old09['rows']==new09['rows']
old10=json.loads((ROOT/'baseline/generator_v0_10/results.json').read_text());new10=json.loads((UP/'generator_v0_10/results.json').read_text())
for old,new in zip(old10['rows'],new10['rows']):
 old=copy.deepcopy(old);new=copy.deepcopy(new)
 for r in old['finite_records']:
  if r['internal_readout']:
   r['internal_readout']['Q2_GeV2']=.1;r['internal_readout']['currents']=r['internal_readout'].pop('current_at_Q2_0_1')
 checks['10_numerical_'+new['case']]=old==new
for stage,path in [('07','source_filter_v0_7/code/results.json'),('08','shutter_v0_8/results.json')]:
 checks[stage+'_results_byte_unchanged']=(ROOT/'baseline'/path).read_bytes()==(UP/path).read_bytes()
env=dict(os.environ,OPENBLAS_NUM_THREADS='2',OMP_NUM_THREADS='2')
with tempfile.TemporaryDirectory() as temp:
 dest=Path(temp)/'upstream'
 for stage in ['source_filter_v0_7','shutter_v0_8','residue_current_v0_9','generator_v0_10','review_0_4_0_6_r1']:
  shutil.copytree(UP/stage,dest/stage,ignore=shutil.ignore_patterns('__pycache__','paper','*.docx','*.pdf','*.png'))
 # Clean 0.7 regeneration verifies two passes in its own runner.
 for path in ['code/results.json','code/handoff.json','verification/independent_audit.json']:(dest/'source_filter_v0_7'/path).unlink()
 subprocess.run([sys.executable,str(dest/'source_filter_v0_7/reproduce_all.py')],env=env,check=True,stdout=subprocess.DEVNULL)
 checks['07_clean_regeneration']=all((dest/'source_filter_v0_7'/p).read_bytes()==(UP/'source_filter_v0_7'/p).read_bytes() for p in ['code/results.json','code/handoff.json','verification/independent_audit.json'])
 # Reorder both stages and scan grids; reference labels and Q2 identities must survive.
 f=dest/'residue_current_v0_9/inputs.json';reordered=copy.deepcopy(cfg)
 for key in ['source_controls','Q2_GeV2','preparation_strength_scan']:reordered[key].reverse()
 f.write_text(json.dumps(reordered));subprocess.run([sys.executable,str(dest/'residue_current_v0_9/compute.py')],env=env,check=True,stdout=subprocess.DEVNULL)
 f=dest/'generator_v0_10/inputs.json';ri=copy.deepcopy(inp);ri['source_cases'].reverse();ri['protocols'].reverse();ri['record_readout_Q2_GeV2']=.01;f.write_text(json.dumps(ri))
 subprocess.run([sys.executable,str(dest/'generator_v0_10/compute.py')],env=env,check=True,stdout=subprocess.DEVNULL)
 reorder=json.loads((dest/'generator_v0_10/results.json').read_text());hand=json.loads((dest/'generator_v0_10/handoff.json').read_text())
 checks['10_reordered_baseline_handoff']=hand['baseline_information_fractions']==json.loads((UP/'generator_v0_10/handoff.json').read_text())['baseline_information_fractions']
 for row in reorder['rows']:
  reference=next(x for x in new10['rows'] if x['case']==row['case'])
  checks['10_reordered_curves_'+row['case']]=sorted(row['curves'],key=lambda x:x['Q2_GeV2'])==sorted(reference['curves'],key=lambda x:x['Q2_GeV2'])
  for rec in row['finite_records']:
   if rec['internal_readout']:
    curve=next(x for x in row['curves'] if x['Q2_GeV2']==.01)
    checks['10_explicit_record_Q2_'+row['case']]=rec['internal_readout']['Q2_GeV2']==.01 and all(abs(rec['internal_readout']['currents'][k][field]-curve[k][field])<2e-10 for k in ['proton','neutron','weak'] for field in curve[k])
if not all(checks.values()):raise AssertionError([k for k,v in checks.items() if not v])
stage_counts={'0.7':113,'0.8':431,'0.9':318,'0.10':465}
out={'all_passed':True,'review_checks':len(checks),'stage_checks':stage_counts,'total_counted_checks':sum(stage_counts.values())+len(checks),'checks':{k:bool(v) for k,v in checks.items()},'interpretation':'counted implementation and mathematical audits, including regression; not independent experimental confirmations','upstream_endpoint':'0.10'}
(ROOT/'review_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
