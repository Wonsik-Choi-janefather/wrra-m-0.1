"""Nested record/supplier loads and zero-support execution boundaries."""
from pathlib import Path
import json,math
import numpy as np
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
step4=ROOT/'step4_dependency';handoff=json.loads((step4/'STEP4_HANDOFF.json').read_text());micro=json.loads((step4/'mass_mixing_join_results.json').read_text());ref=json.loads((step4/'step3_dependency/step2_dependency/connection_results.json').read_text())['measurement_join'];load=json.loads((ROOT/'state_load_results.json').read_text());assert load['status']=='PASS'
# These operators are normalized energy loads inside the already allocated
# phenotype sector, not an independent cosmic species/sector.
E=np.array(ref['sector_energy_before_J']);phi=E[0];checks={};rows=[]
models=[{'model':'baseline_record','supplier_work_J':ref['supplier_work_J'],'supplier_J':ref['supplier_before_J'],'required_supplier_J':max(ref['conditional_branch_supply_J'])}]
for row in micro['cases']:
 models.append({'model':row['internal_model'],'supplier_work_J':row['supplier_work_J'],'supplier_J':row['admitted_supplier_J'],'required_supplier_J':row['required_supplier_J']})
for row in models:
 work=row['supplier_work_J'];supplier=row['supplier_J'];remaining=supplier-work
 before=np.r_[E,supplier];after=np.r_[E[0]+work,E[1:],remaining]
 assert remaining>=0 and supplier>=row['required_supplier_J']
 assert abs(before.sum()-after.sum())<1e-24
 # Loads of the nested phenotype+supplier identity agree. Channel labels and
 # alternative internal views are not added on top of this total.
 pre_load=before/phi;post_load=after/phi
 assert abs(pre_load.sum()-post_load.sum())<1e-13
 for a in (.5,1.,2.):
  # Single-write pressureless comoving allocation; same R-volume law.
  V=a**3;total_before=E[0]+E[1]+E[2]*V+supplier;total_after=E[0]+work+E[1]+E[2]*V+remaining
  assert abs(total_before-total_after)<1e-24
  pressure=-E[2];eps=V*1e-5
  energy=lambda v:E[0]+work+E[1]+E[2]*v+remaining
  pnum=-(energy(V+eps)-energy(V-eps))/(2*eps)
  assert abs(pnum-pressure)<1e-17
 rows.append({**row,'supplier_after_J':remaining,'included_energy_before_J':float(before.sum()),'included_energy_after_J':float(after.sum()),'included_dimensionless_energy_load':float(pre_load.sum()),'record_nested_in_phi':True})
checks['all_three_internal_record_branches_admitted_with_disclosed_suppliers']=True
checks['record_and_supplier_energy_load_conserved']=True
checks['same_volume_law_pressure_preserved_after_write']=True
checks['no_added_channel_or_alternative_energy_budget']=len(rows)==3 and len(E)==3
# Zero sector support: impossible to calibrate positive target from zero load.
def coefficient(target,reference_load):
 if not np.isfinite([target,reference_load]).all() or min(target,reference_load)<0:raise ValueError('invalid calibration')
 if reference_load==0:
  if target>0:raise ValueError('positive energy target has zero support')
  return 0.
 return target/reference_load
rejected=False
try:coefficient(1.,0.)
except ValueError:rejected=True
checks['positive_target_zero_support_rejected']=rejected
checks['zero_target_zero_support_returns_zero']=coefficient(0.,0.)==0
# Positive-load state approaching the zero-mode is retained, not thresholded.
N=128;I=np.eye(N);K=2*I-np.roll(I,1,axis=0)-np.roll(I,-1,axis=0);zero=np.ones(N)/math.sqrt(N);high=np.exp(2j*math.pi*(N//2)*np.arange(N)/N)/math.sqrt(N)
loads=[]
for t in (0.,1e-12,.1,1.):
 rho=(1-t)*np.outer(zero,zero)+t*np.outer(high,high.conj());val=np.trace(rho@K/2).real
 assert abs(val-2*t)<1e-13
 loads.append({'high_mode_weight':t,'clustering_load':float(val)})
checks['zero_mode_load_is_zero_with_nonzero_phenotype']=abs(loads[0]['clustering_load'])<1e-13
checks['small_positive_load_not_erased']=loads[1]['clustering_load']>1e-12
checks['convex_state_transition_linear_load']=all(abs(x['clustering_load']-2*x['high_mode_weight'])<1e-13 for x in loads)
checks['joint_alternative_original20_percent_still_rejected']=handoff['branches'][1]['baseline_status']=='insufficient_supplier'
assert all(checks.values())
out={'status':'PASS','version':'0.2','checks':checks,'branches':rows,'zero_mode_transition':loads,'scope':'single effective write nested in existing phenotype and disclosed pressureless supplier; correlated address/carrier load map retained separately','remaining':'common-input final review','not_claimed':['supplier naturally generated','unitary reset cost zero','all cosmic states have the chosen correlation','one bit universal fixed SI energy']}
(ROOT/'record_load_join_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'status':'PASS','checks':len(checks),'branches':len(rows)}))
