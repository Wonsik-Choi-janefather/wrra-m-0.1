"""Stage3: calibrated finite alternatives and a cheaper exact phase recurrence."""
from pathlib import Path
import ast,json,math,time,hashlib
import numpy as np
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
dependency=json.loads((ROOT/'dependency_manifest.json').read_text())
for name,digest in dependency['files'].items():
 assert hashlib.sha256((ROOT/'step2_dependency'/name).read_bytes()).hexdigest()==digest
p=ROOT/'step2_dependency/address_structure.py';nodes=[]
for node in ast.parse(p.read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name=='product':break
 nodes.append(node)
s={'__file__':str(p),'__name__':'setup'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),s)
cfg=s['cfg'];w=s['w'];g=s['g'];mask=s['struct_odd'];even=s['struct_even'];n=s['base']['n'];cost=s['cost'][2:]
sp=cfg['upstream']['spectrum'];up=cfg['upstream']['update'];gamma=np.array(sp['gamma'])[:,None];coef=np.array(sp['coefficients'])[:,None];offset=np.array(sp['phase_offsets'])[:,None];xi=up['phase_step_xi'];h0=up['sigmoid_threshold_h'];K=up['admission_frames_K']
target=float(s['shares'][0]);t0=time.perf_counter()
drives=np.array([(coef*np.cos(gamma*(cost[mask][None,:]+xi*k)+offset)).sum(axis=0) for k in range(K)])
direct_time=time.perf_counter()-t0
# Exact trigonometric recurrence: cache initial cos/sin and fixed frame rotations.
t0=time.perf_counter();angle=gamma*cost[mask][None,:]+offset;c=np.cos(angle);z=np.sin(angle)
ct=np.cos(gamma*xi);st=np.sin(gamma*xi);rec=[]
for k in range(K):
 rec.append((coef*c).sum(axis=0))
 c,z=c*ct-z*st,z*ct+c*st
rec=np.array(rec);rec_time=time.perf_counter()-t0
err=float(np.max(np.abs(rec-drives)));assert err<1e-12
reference_admit=s['effect'][0,mask]
rec_admit=-np.expm1((-np.logaddexp(0,rec-h0)).sum(axis=0))
assert np.allclose(rec_admit,reference_admit,atol=2e-13,rtol=0)
checks={'recurrence_preserves_all_frame_drives':err<1e-12,'recurrence_preserves_every_address_admission':bool(np.allclose(rec_admit,reference_admit,atol=2e-13,rtol=0))}
# Same verified share targets for each alternative; calibration is legitimate.
# alpha fixed by the shared D readout; threshold/beta sets the remaining P/R split.
models=[]
selector=np.zeros(len(n),np.int16);power=3
while power<=s['N']:selector+=n%power==0;power*=3
sel=selector[mask]%2==1

def record(name,admit,threshold,frames,kind):
 effect=np.array([np.zeros(len(w)),even.astype(float),1-even.astype(float)])
 effect[0,mask]=admit;effect[2,mask]-=admit
 shares=effect@w;mu=(effect*g*w).sum(axis=1)
 assert np.allclose(shares,s['shares'],atol=2e-12,rtol=0)
 macro=s['adapter']['macro'](mu)['rows'][1]
 conditional=w[mask]*admit/shares[0]
 models.append({'model':name,'kind':kind,'frames':frames,'calibrated_threshold_or_beta':threshold,'shares':shares.tolist(),'address_moments':mu.tolist(),'phenotype_weighted_abs_admission_difference':float(w[mask]@np.abs(admit-reference_admit)),'selector_odd_v3_fraction':float(conditional@sel),'present_q':macro['q'],'present_rotation_km_s':macro['rotation_km_s'],'present_lensing_arcsec':macro['lensing_arcsec'],'trig_evaluations_per_eligible_address':int(len(gamma)*frames),'aggregate_calibration_degrees':2,'retained_eight_frame_structure':frames==K and kind=='phase','calibration_policy':'shared alpha unchanged; threshold or beta calibrated to same P target; SI and load coefficients unchanged'})
for frames in (1,2,4,8):
 d=drives[:frames]
 def admitted(h):return -np.expm1((-np.logaddexp(0,d-h)).sum(axis=0))
 h=brentq(lambda v:float(w[mask]@admitted(v))-target,-50,50,xtol=1e-13)
 record('phase_K'+str(frames),admitted(h),h,frames,'phase')
beta=target/float(w[mask].sum());record('constant_admission',np.full(mask.sum(),beta),beta,0,'scalar')
record('phase_K8_recurrence',rec_admit,h0,K,'phase')
models[-1]['trig_evaluations_per_eligible_address']=int(2*len(gamma))
models[-1]['fixed_rotation_trig_evaluations']=int(2*len(gamma))
# Route all recurrence frame transfers and their address-dependent load through
# the ledger; preserving only global shares is not enough.
remaining=np.ones(mask.sum());total_load=np.zeros(3)
for row in rec:
 born=remaining*(-np.expm1(-np.logaddexp(0,row-h0)));remaining-=born
 total_load[0]+=float((w[mask]*g[0,mask])@born)
total_load[1]=float(w[even]@g[1,even])
total_load[2]=float((w[mask]*g[2,mask])@remaining)+float(w[s['struct_prime']]@g[2,s['struct_prime']])
checks['recurrence_frame_ledger_preserves_sector_loads']=bool(np.allclose(total_load,s['mu'],atol=2e-13,rtol=0))
checks['each_alternative_calibrated_to_same_verified_shares']=all(np.max(np.abs(np.array(r['shares'])-s['shares']))<2e-12 for r in models)
checks['scalar_has_same_shares_but_different_address_response']=models[4]['phenotype_weighted_abs_admission_difference']>1e-4
checks['baseline_threshold_reproduced']=abs(models[3]['calibrated_threshold_or_beta']-h0)<1e-10
checks['recurrence_has_same_no_new_calibration']=models[5]['calibrated_threshold_or_beta']==h0 and models[5]['aggregate_calibration_degrees']==2
checks['recurrence_reduces_trig_evaluation_count']=models[5]['trig_evaluations_per_eligible_address']<models[3]['trig_evaluations_per_eligible_address']
checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),checks
r={'status':'PASS','date':'2026-10-08','stage':'theory improvement Step3, minimum-computation structure comparison','target_shares':s['shares'].tolist(),'models':models,'recurrence':{'maximum_drive_error':err,'direct_seconds_single_run':direct_time,'recurrence_seconds_single_run':rec_time,'timing_scope':'one local run; not a universal speed or operation-cost ordering','relation':'cos(theta+k delta), sin(theta+k delta) updated by a fixed rotation','eligible_addresses':int(mask.sum()),'direct_trig_count':int(mask.sum()*len(gamma)*K),'recurrence_initial_trig_count':int(mask.sum()*2*len(gamma))},'checks':checks,'input_structure_accounting':{'phase_inherited_spectrum_entries':sum(len(sp[x]) for x in ('gamma','coefficients','phase_offsets')),'phase_step_entries':1,'calibrated_continuous_parameters':2,'frame_count_discrete_choice':1,'note':'stored specification entries, not independent statistically identified degrees of freedom; scalar drops spectrum and frame dynamics'},'dependency_provenance':dependency['github_commit'],'comparison_limits':['finite tested model family, no global unique-minimum proof','common share calibration does not guarantee identical address or frame explanations','inherited spectrum and load laws kept fixed','fewer trig evaluations add arithmetic; total cost depends on implementation and hardware']}
(ROOT/'structure_comparison_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
