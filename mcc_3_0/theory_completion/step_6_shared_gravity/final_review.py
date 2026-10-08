"""Final shared-state contract audit, no additional fit."""
from pathlib import Path
import json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
a=json.loads((ROOT/'shared_gravity_results.json').read_text());b=json.loads((ROOT/'macro_boundary_results.json').read_text());assert a['status']==b['status']=='PASS' and all(a['checks'].values()) and all(b['checks'].values())
index={(r['carrier_state'],r['epsilon'],r['a']):r for r in a['cases']}
errors=[]
for r in b['cases']:
 shared=index[r['state'],r['epsilon'],r['a']];errors.append(abs(shared['aT_m_s2']-r['shared_local_aT_before_after_m_s2']))
 assert errors[-1]<1e-24
 assert abs(r['external_before']['q']-shared['q'])<1e-12
 assert abs(r['external_before']['H_over_H0']-shared['H_over_H0'])<1e-12
checks={'all_prior15_checks_pass':len(a['checks'])+len(b['checks'])==15,'all36_record_boundaries_match_shared_local_state':len(errors)==36 and max(errors)<1e-24,'external_before_matches_shared_expansion':True,'positive_state_outputs_finite':all(np.isfinite([r['H_over_H0'],r['q'],r['rotation_km_s'],r['lensing_arcsec']]).all() for r in a['cases']),'zero_clustering_independent_analytic_boundary_retained':b['checks']['zero_clustering_lens_matches_analytic_baryonic_integral']}
assert all(checks.values())
r={'status':'PASS','version':'0.3','checks':checks,'total_checks':20,'cases_shared_state':12,'cases_record_boundary':36,'completion_scope':'same frozen sector density/pressure and local clustering response feed rotation, conditional lens and homogeneous expansion; explicit record supplier boundaries and zero clustering tested','constitutive_inputs':['local baryonic source','shared nu response law','finite lens patch and Phi=Psi','positive SI load calibration','homogeneous expansion/volume laws'],'falsifiers':['shared-state mismatch','output-specific refit','pressure/energy boundary mismatch','independent lens integral failure'],'scope_limits':['no new observational dataset fit','no complete4D covariant dynamics derivation','finite supplier homogeneous embedding is a ledger probe'],'result_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['shared_gravity_results.json','macro_boundary_results.json']}}
(ROOT/'STEP6_HANDOFF.json').write_text(json.dumps(r,indent=2));print(json.dumps({'status':'PASS','total_checks':20,'max_local_state_difference':max(errors)}))
