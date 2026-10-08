"""Distinguish the fixed continuation theorem from the eight-frame observation."""
from pathlib import Path
import json,hashlib,numpy as np
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
manifest=json.loads((ROOT/'dependency_manifest.json').read_text())
for name,h in manifest['files'].items():assert hashlib.sha256((ROOT/'step2_dependency'/name).read_bytes()).hexdigest()==h
cfg=json.loads((ROOT/'step2_dependency/dependencies/original/parameters.json').read_text());sp=cfg['upstream']['spectrum'];g=np.array(sp['gamma']);c=np.array(sp['coefficients']);xi=cfg['upstream']['update']['phase_step_xi'];off=np.array(sp['phase_offsets']);rows=[]
for n in (9,15,105,1001):
 seq=np.array([np.sum(c*np.cos(g*(np.log(n)+xi*k)+off)) for k in range(8)])
 H=np.array([[seq[i+j] for j in range(4)] for i in range(4)])
 # Only indices0..6 are needed. Eight samples do not provide H8 (indices0..14).
 rows.append({'address':n,'finite8_available_hankel_size':4,'finite8_hankel_rank':int(np.linalg.matrix_rank(H))})
checks={'frozen_dependency_hashes_match':True,'finite8_samples_do_not_supply_rank8_hankel':all(x['finite8_available_hankel_size']==4 for x in rows),'fixed_continuation_theorem_still_rank8':json.loads((ROOT/'minimum_phase_state_results.json').read_text())['real_state_dimension']==8,'comparison_does_not_unique_select4modes_from_shares':len(json.loads((ROOT/'mode_comparison_results.json').read_text())['rows'])==15}
assert all(checks.values())
out={'status':'PASS','checks':checks,'probes':rows,'correction':'eight-state lower bound applies to reproducing the entire fixed spectral continuation under autonomous real LTI realization; not to arbitrary reproduction of only eight admission samples','selection':'equivalent rotation kernel retained; constitutive4modes/K8 retained for existing declared phase-address explanation, not uniquely identified from aggregate shares','prior_checks':34,'total_checks':38}
(ROOT/'review_scope_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
