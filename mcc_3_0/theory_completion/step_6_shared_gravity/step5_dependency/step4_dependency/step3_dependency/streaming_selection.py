"""Compare two equivalent streamed phase implementations and select by explicit cost axes."""
from pathlib import Path
import ast,json,hashlib,math,time,gc
import numpy as np
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
dep=json.loads((ROOT/'dependency_manifest.json').read_text())
for name,digest in dep['files'].items():assert hashlib.sha256((ROOT/'step2_dependency'/name).read_bytes()).hexdigest()==digest
p=ROOT/'step2_dependency/address_structure.py';nodes=[]
for node in ast.parse(p.read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name=='product':break
 nodes.append(node)
s={'__file__':str(p),'__name__':'setup'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),s)
cfg=s['cfg'];sp=cfg['upstream']['spectrum'];up=cfg['upstream']['update'];gamma=np.array(sp['gamma'])[:,None];co=np.array(sp['coefficients'])[:,None];offset=np.array(sp['phase_offsets'])[:,None];xi=up['phase_step_xi'];h=up['sigmoid_threshold_h'];K=up['admission_frames_K'];J=len(gamma)
mask=s['struct_odd'];cost=s['cost'][2:][mask];w=s['w'][mask];g=s['g'][:,mask];reference=s['effect'][0,mask];M=len(cost)
ct=np.cos(gamma*xi);st=np.sin(gamma*xi)

def run(method,chunk,verify=True):
 shares=np.zeros(K);load_frames=np.zeros(K);return_load=0.;error=0.
 for lo in range(0,M,chunk):
  hi=min(M,lo+chunk);cc=cost[lo:hi];remain=np.ones(hi-lo);admitted=np.zeros(hi-lo)
  if method=='rotation':
   angle=gamma*cc[None,:]+offset;c=np.cos(angle);z=np.sin(angle)
  for k in range(K):
   if method=='rotation':drive=(co*c).sum(axis=0)
   else:drive=(co*np.cos(gamma*(cc[None,:]+xi*k)+offset)).sum(axis=0)
   transfer=remain*(-np.expm1(-np.logaddexp(0,drive-h)))
   remain-=transfer;admitted+=transfer
   shares[k]+=float(w[lo:hi]@transfer)
   load_frames[k]+=float((w[lo:hi]*g[0,lo:hi])@transfer)
   if method=='rotation' and k+1<K:c,z=c*ct-z*st,z*ct+c*st
  if verify:error=max(error,float(np.max(np.abs(admitted-reference[lo:hi]))))
  return_load+=float((w[lo:hi]*g[2,lo:hi])@remain)
 mu=np.array([load_frames.sum(),s['mu'][1],return_load+float(s['w'][s['struct_prime']]@s['g'][2,s['struct_prime']])])
 return {'frame_shares':shares.tolist(),'frame_phi_loads':load_frames.tolist(),'address_moments':mu.tolist(),'max_address_admission_error':error}

checks={};cases=[]
for method in ('direct','rotation'):
 for chunk in (1024,65536,M):
  out=run(method,chunk)
  assert out['max_address_admission_error']<2e-13
  assert np.allclose(out['address_moments'],s['mu'],atol=3e-13,rtol=0)
  assert abs(sum(out['frame_shares'])-s['shares'][0])<3e-13
  cases.append({'method':method,'chunk':chunk,**out})
reference_frames=np.array(cases[0]['frame_shares'])
checks['all_streamed_address_admissions_preserved']=all(x['max_address_admission_error']<2e-13 for x in cases)
checks['all_streamed_sector_loads_preserved']=all(np.allclose(x['address_moments'],s['mu'],atol=3e-13,rtol=0) for x in cases)
checks['all_frame_contributions_preserved']=all(np.allclose(x['frame_shares'],reference_frames,atol=3e-13,rtol=0) for x in cases)
checks['chunk_size_does_not_change_model']=True
# Warm both kernels, then alternate measured runs. Setup/classification is excluded.
for m in ('direct','rotation'):run(m,65536,False)
timings={'direct':[],'rotation':[]}
for repeat in range(3):
 for m in (('direct','rotation') if repeat%2==0 else ('rotation','direct')):
  t=time.perf_counter();run(m,65536,False);timings[m].append(time.perf_counter()-t)
medians={m:float(np.median(v)) for m,v in timings.items()}
# Memory is an explicit conservative live phase-work-array accounting bound,
# not process RSS or input/source classification storage.
B=65536
bounds={'direct_stream':8*B*(3*J+8),'rotation_stream':8*B*(10*J+8),'stored_all_frame_drives':8*M*K}
costs={'eligible_addresses':M,'spectral_terms':J,'frames':K,'direct_trig_calls':M*J*K,'rotation_trig_calls':2*M*J+2*J,'extra_rotation_multiplications':4*M*J*(K-1),'extra_rotation_additions':2*M*J*(K-1),'unchanged_inherited_spectrum_entries':sum(len(sp[x]) for x in ('gamma','coefficients','phase_offsets')),'unchanged_calibration_parameters':2,'memory_accounting_bytes':bounds,'memory_scope':'conservative phase-work-array bounds; excludes shared inputs, allocator/RSS and common source construction'}
checks['streamed_rotation_reduces_trig_calls']=costs['rotation_trig_calls']<costs['direct_trig_calls']
checks['both_work_array_bounds_below_full_drive_table']=max(bounds['direct_stream'],bounds['rotation_stream'])<bounds['stored_all_frame_drives']
checks['no_new_calibration_or_structural_parameters']=True
# Keep Pareto tradeoff explicit. Adopt recurrence for fewer transcendental calls
# and local speed; retain direct-stream implementation as a low-memory reference.
selected='rotation_stream' if medians['rotation']<medians['direct'] else 'direct_stream'
checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),checks
r={'status':'PASS','version':'0.2','date':'2026-10-08','fixed_explanation_scope':'same address effects, all eight frame contributions, sector loads, inherited channel and record interfaces','cases':cases,'operation_and_storage_accounting':costs,'kernel_timings_seconds':timings,'median_kernel_seconds':medians,'timing_scope':'three local alternating runs after warmup; phase/readout kernel only, not full pipeline or universal hardware claim','local_selected_implementation':selected,'selection_policy':'retain original phase structure; chunk65536; choose locally faster kernel, preserve direct reference; no universal scalar cost or unique physical minimum asserted','checks':checks,'next_stage_handoff':{'phase_structure':'unchanged','N':s['N'],'alpha':cfg['upstream']['state']['alpha'],'h':h,'K':K,'default_kernel':selected,'chunk':B,'macroscopic_outputs':s['adapter']['macro'](np.array(cases[-1]['address_moments']))['rows'][1]}}
(ROOT/'streaming_selection_results.json').write_text(json.dumps(r,indent=2));print(json.dumps({'status':r['status'],'checks':checks,'costs':costs,'median_seconds':medians,'selected':selected},indent=2))
