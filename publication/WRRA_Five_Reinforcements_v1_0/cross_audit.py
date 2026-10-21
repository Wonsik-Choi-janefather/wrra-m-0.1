"""Cross-module ownership audit, independent of the individual sample counters."""
from pathlib import Path
import json,numpy as np,hashlib
P=Path(__file__).resolve().parent;M=P/'modules';checks={}
def load(n):return json.loads((M/n/'results.json').read_text())
def ck(k,b):
 checks[k]=bool(b)
 if not b:raise AssertionError(k)
a=load('finite_scale_bridge_v0_1');b=load('source_carrier_action_v0_1');g=load('information_gravity_mechanism_v0_2');t=load('local_twist_load_bridge_v0_3');z=load('zeta_physical_readout_v0_1');d=load('zeta_symmetry_drive_v0_2');f=load('freedom_falsifiability_v0_1')
ck('payload_byte_identity_tasks_1_2',(M/'finite_scale_bridge_v0_1/payloads.json').read_bytes()==(M/'source_carrier_action_v0_1/inputs/payloads.json').read_bytes())
ck('task2_modes_not_SOURCE_cardinality',b['registers']['source_mode']==128 and z['constants']['N']==1015000)
ck('same_15_channel_contract',b['geometry']['carrier_channels']==15)
ck('timeless_slots_preserved',b['registers']['timeless_allocation_slots_unchanged'])
ck('same_conditional_energy_unit_tasks_2_4',abs(b['minimum_generator']['conditional_hbar_over_tau_J']/(z['constants']['hbar_J_s']/z['constants']['shutter_s'])-1)<1e-15)
ck('different_geometries_not_equated',int(np.prod(z['constants']['shape']))==1066065 and 500*29*70==1015000 and 1066065!=1015000)
ck('same_aT_tasks_3_5',abs(g['origin_reference']['aT_m_s2']/f['gravity']['reference_a_eff_m_s2']-1)<1e-14)
ck('same_twist_aT',t['normalization']['aT_m_s2']==g['origin_reference']['aT_m_s2'])
ck('same_reference_rotation',abs(t['reference_local']['rotation_km_s']-f['gravity']['reference_rotation_km_s'])<1e-10)
ck('same_conditional_lens',abs(g['origin_reference']['lensing_arcsec']-f['gravity']['reference_lens_arcsec'])<1e-10)
ck('bare_storage_not_effective_Poisson_density',t['reference_local']['effective_to_bare_density_ratio']>1e5)
ck('same_shutter_task4_driven',z['constants']['shutter_s']==d['constants']['tau_s'])
for prep in ['uniform','inherited_alpha']:
 row=next(r for r in z['rows'] if r['preparation']==prep and r['case']=='zeta')
 ck(prep+'_same_port_tasks4_5',abs(row['pass_probability']-f['zeta_constraints'][prep]['coherent_vector_P_B_Edimensionless'][0])<1e-14)
 ck(prep+'_same_driven_port',abs(row['pass_probability']-d['summaries'][prep]['equal_pass'])<1e-14)
ck('no_new_observational_fit',f['counts']['new_observational_fits_in_this_package']==0)
ck('whole_model_dimension_not_claimed','not a full-universe' in f['scope'])
ck('all_seven_execution_verifier_pairs',json.loads((P/'RECHECK_RESULTS.json').read_text())['all_pass'])
# Rebuilt outputs may differ in float formatting; original module manifests
# remain historical evidence. The release manifest will freeze final bytes.
result={'checks':checks,'all_pass':all(checks.values()),'boundaries':[
'Only tasks 1/2 share the exact frozen payload; the zeta CRT branch uses two separate inherited test preparations.',
'The QUMOND-type receiver is adopted/credited; bare twist energy is not silently added as GR dust.',
'The driven phase controller is external and generally nonlocal; no autonomous reset/device closure.',
'The five topics are coordinated finite modules, not one rerun of complete SM/GR/CMB cosmos.']}
(P/'CROSS_MODULE_AUDIT.json').write_text(json.dumps(result,indent=2));print(json.dumps({'cross_checks':len(checks),'all_pass':all(checks.values())}))
