"""Release recheck supplement; original 444 checks are not recounted here."""
import json, math, hashlib
from pathlib import Path
import numpy as np
from emission import Model, schedule, simulate, BETA, GAMMA

P=Path(__file__).resolve().parent
checks={}
def require(name,ok):
    checks[name]=bool(ok)
    if not ok:raise AssertionError(name)

base=simulate(Model());events=base['events'];times=np.array([e['time'] for e in events])
reference=np.array([math.fsum(1/(256-m) for m in range(j))/(GAMMA) for j in range(1,129)])
require('compensated_sum_clock',np.max(abs(reference-times))<2e-14)
edge=float(times[63])
require('endpoint_equality_included',len(schedule(Model(pulse=edge))[0])==64)
require('immediately_before_endpoint_excluded',len(schedule(Model(pulse=float(np.nextafter(edge,0))))[0])==63)
require('immediately_after_endpoint_included',len(schedule(Model(pulse=float(np.nextafter(edge,1))))[0])==64)
actual_balance=max(abs(e['reservoir_after']-e['reservoir_before']+
    e['a']*e['matter_gain']+e['record_heat_comoving'])/e['q_comoving'] for e in events)
require('reconstruct_energy_from_actual_ledger',actual_balance<1e-12)
total_m=math.fsum(e['matter_gain'] for e in events)
total_j=math.fsum(e['record_heat_comoving'] for e in events)
require('reconstruct_final_matter_from_events',abs(total_m/base['M']-1)<2e-15)
require('reconstruct_final_heat_from_events',abs(total_j/base['J']-1)<2e-15)
require('one_record_per_event',all(e['records_left']==256-e['event'] for e in events))
manifest=json.loads((P/'SHA256SUMS.json').read_text())
for name in ['audit.json','cells.json','events.csv']:
    require('rerun_exact_'+name,hashlib.sha256((P/'results'/name).read_bytes()).hexdigest()==manifest['results/'+name])
za=np.load(P/'results/actual_seed_event_times.npz')
references=json.loads((P/'REVALIDATION_REFERENCE.json').read_text())
require('rerun_all_arrays_exact',all(hashlib.sha256(za[k].tobytes()).hexdigest()==references[k] for k in za.files))
result=dict(date='2026-10-20',original_checks_passed=444,supplementary_checks_passed=sum(checks.values()),
    checks=checks,compensated_clock_max_error=float(np.max(abs(reference-times))),
    actual_ledger_jump_max_normalized=actual_balance,
    assessment='Original scientific outputs exactly reproduced. No scientific manuscript changes required. Supplementary endpoint and actual-ledger checks pass.',
    note='Original 444 include repeated per-cell consistency checks; supplementary checks are reported separately, not independent physical confirmations.')
(P/'REVALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
