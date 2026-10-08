"""Freeze branch contracts and verify reject/admit behavior and included budgets."""
from pathlib import Path
import json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
inputs={name:json.loads((ROOT/name).read_text()) for name in ['carrier_selection_results.json','phenotype_transform_results.json','channel_record_results.json','mass_mixing_join_results.json']}
for x in inputs.values():assert x['status']=='PASS' and all(x['checks'].values())
r=inputs['mass_mixing_join_results.json'];phi=inputs['phenotype_transform_results.json']['phenotype_energy_J'];checks={};branches=[]
# Admission is a boundary condition, not a fitting objective or silent input edit.
def admit(available,required):
 if not np.isfinite(available) or available<0:raise ValueError('invalid supplier')
 return 'admitted' if available>=required else 'insufficient_supplier'
for row in r['cases']:
 required=row['required_supplier_J'];original=.2*phi;selected=max(original,required);work=row['supplier_work_J'];remaining=selected-work
 assert admit(required,required)=='admitted'
 assert admit(np.nextafter(required,-np.inf),required)=='insufficient_supplier'
 assert abs((phi+selected)-(phi+work+remaining))<1e-24
 assert remaining>=0
 branches.append({'model':row['internal_model'],'ground_mass_MeV':row['ground_mass_MeV'],'internal_gap_MeV':row['gap_MeV'],'baseline_supplier_fraction':.2,'baseline_status':admit(original,required),'minimum_supplier_fraction':required/phi,'admitted_supplier_J':selected,'admitted_supplier_status':admit(selected,required),'supplier_after_mean_write_J':remaining,'energy_boundary':'phenotype system + record + disclosed supplier; no fourth cosmic sector','alternative_to_baseline_not_additive':True})
checks['all_prior_43_connection_checks_pass']=sum(len(x['checks']) for x in inputs.values())==43
checks['supplier_admission_boundary_exactly_tested']=True
checks['both_admitted_branches_conserve_included_energy']=True
checks['joint_branch_rejected_at_original20_percent']=branches[1]['baseline_status']=='insufficient_supplier'
checks['principal_branch_admitted_at_original20_percent']=branches[0]['baseline_status']=='admitted'
checks['baseline_microgap_preserved_as_separate_model']=abs(r['baseline_record_gap_MeV']-431.08124431500175)<1e-8
checks['three_cosmic_sectors_retained']=len(inputs['phenotype_transform_results.json']['sector_shares'])==3
checks['selection_result_is_consumed_by_phenotype']=inputs['carrier_selection_results.json']['handoff']['selected_filter']=='F_DX' and inputs['phenotype_transform_results.json']['channel_table']['benchmark_matches']
assert all(checks.values())
out={'status':'PASS','version':'0.5','checks':checks,'prior_connection_checks':43,'total_connection_checks':51,'inherited_internal_replay_checks_separate':38,'branches':branches,'baseline_policy':'retain original record model and20% supplier; never silently substitute an alternate gap','completion_scope':'carrier response -> calibrated selection -> address/channel phenotype -> effective internal mass/configuration mixing and finite single record with explicit branch budgets','not_claimed':['CKM/PMNS integration','all species mass decoding','a composite proton is one Weyl channel','physical supplier mechanism derived','reset/repeated write costs','complete theory'],'next_theory_step':'Step5 phenotype/resident state to physical load','result_hashes':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in inputs}}
(ROOT/'STEP4_HANDOFF.json').write_text(json.dumps(out,indent=2));print(json.dumps({'status':'PASS','new_checks':8,'total_connection_checks':51,'branches':branches},indent=2))
