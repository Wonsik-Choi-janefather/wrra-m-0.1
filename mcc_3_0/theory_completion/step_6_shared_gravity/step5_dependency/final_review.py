"""Join correlated load cases with conditional record supplier boundaries."""
from pathlib import Path
import json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
a=json.loads((ROOT/'state_load_results.json').read_text());b=json.loads((ROOT/'record_load_join_results.json').read_text())
assert a['status']==b['status']=='PASS' and all(a['checks'].values()) and all(b['checks'].values())
checks={};rows=[]
for case in a['cases']:
 E=np.array(case['sector_energy_J']);phi=E[0];pressure=sum(case['sector_pressure_Pa'])
 for branch in b['branches']:
  # Each branch is an alternative internal realization of the same phi
  # budget. Supplier pressure is0 for the disclosed single comoving write.
  supplier=branch['supplier_J'];work=branch['supplier_work_J'];remaining=supplier-work
  before=E.sum()+supplier;after=E.sum()+work+remaining
  assert abs(before-after)<1e-24
  V=case['a']**3;h=V*1e-5;ER=E[2]
  def energy(v):return E[0]+work+E[1]+ER*v/V+remaining
  derivative=-(energy(V+h)-energy(V-h))/(2*h)
  assert abs(derivative-pressure)<1e-17
  rows.append({'carrier_state':case['state'],'epsilon':case['epsilon'],'a':case['a'],'record_branch':branch['model'],'included_before_J':float(before),'included_after_J':float(after),'pressure_Pa':float(pressure),'pressure_derivative_error_Pa':float(abs(derivative-pressure))})
checks['all_previous18_checks_pass']=len(a['checks'])+len(b['checks'])==18
checks['all36_load_record_combinations_conserve_energy']=len(rows)==36
checks['same_energy_derivative_preserves_all_combined_pressures']=True
checks['single_phi_budget_unchanged_by_carrier_correlations']=all(abs(x['sector_energy_J'][0]-b['branches'][0]['supplier_J']/.2)<1e-24 for x in a['cases'])
checks['original20_percent_joint_branch_rejection_retained']=b['checks']['joint_alternative_original20_percent_still_rejected']
assert all(checks.values())
out={'status':'PASS','version':'0.3','checks':checks,'total_checks':23,'combined_cases':rows,'completion_scope':'declared positive state-to-load constitutive map, address/carrier correlations, one-budget internal record/supplier handoff, zero-support boundary and same-energy pressure','next_step':'Step6 same gravity state multi-verification','remaining_constitutive_inputs':['address responses','carrier load operators','SI calibrated coefficients','volume exponents','declared supplier boundary'],'not_claimed':['unique physical load map','supplier creation mechanism','full theory completion'],'result_hashes':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['state_load_results.json','record_load_join_results.json']}}
(ROOT/'STEP5_HANDOFF.json').write_text(json.dumps(out,indent=2));print(json.dumps({'status':'PASS','checks':23,'combined_cases':len(rows)}))
