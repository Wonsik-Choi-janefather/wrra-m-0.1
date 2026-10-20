"""Scientific acceptance tests and a deliberately closed full-state export gate."""
from pathlib import Path
import json,math
import numpy as np
from event_tangent import EOS,run,BETA,Model,schedule
P=Path(__file__).resolve().parent
checks={}
def check(name,ok):
    checks[name]=bool(ok)
    if not ok:raise AssertionError(name)

class IncompleteStateError(ValueError):pass
def injection_payload(states,finite_k_packets=False,species_completed=False,thermal_rerun=False,angular_completed=False):
    missing=[]
    if not finite_k_packets:missing.append('finite-k packet energy and momentum source on specified event hypersurfaces')
    if not species_completed:missing.append('baryon/electron and massive-neutrino distribution states')
    if not thermal_rerun:missing.append('all finite-k modes rerun on recalibrated thermal background')
    if not angular_completed:missing.append('declared three-dimensional/angular covariance of the finite seed')
    if missing:raise IncompleteStateError('; '.join(missing))
    raise NotImplementedError('No validated CAMB full-state transport implementation in this development artifact')

def main():
    r=json.loads((P/'results/event_tangent.json').read_text());b=r['base'];c=r['calibration']
    refined=json.loads((P/'results/event_tangent_refined.json').read_text())
    rows=json.loads((P/'results/cdm_comoving_64_states.json').read_text())
    for row in rows:
        a=row['audit'];n=row['mode'];s=row['adapted']
        check(f'mode_{n:02}_Hamiltonian',a['Hamiltonian_normalized']<2e-12)
        check(f'mode_{n:02}_momentum',a['momentum_normalized']<2e-12)
        check(f'mode_{n:02}_entropy_gauge_invariance',a['entropy_invariance_absolute']<5e-15)
        check(f'mode_{n:02}_inverse_transform',a['inverse_normalized']<2e-14)
        check(f'mode_{n:02}_high_neutrino_moments',a['unchanged_high_neutrino_moments'])
        check(f'mode_{n:02}_CDM_comoving',abs(s['theta_m'])<1e-24)
        check(f'mode_{n:02}_velocity_deletion_rejected',a['deletion_negative_control']>.01)
    check('all_original_64_modes_retained',len(rows)==64)
    check('finite_event_count',b['count']==128)
    check('common_slice_saltation_nonzero',abs(b['S_m_em_response'])>.1)
    check('missing_event_time_detected',abs(r['missing_event_time_negative_control']['S_m_em_response'])<1e-30)
    for x in r['finite_difference']:
        check(f'FD_{x["epsilon"]}_fixed_count',x['count_plus']==x['count_minus']==128)
        check(f'FD_{x["epsilon"]}_independent_entropy',x['relative_error']<1e-6)
    check('thermal_energy_pressure_work',b['max_energy_work_residual']<1e-9)
    check('refined_energy_pressure_work',refined['max_energy_work_residual']<1e-10)
    check('EOS_and_time_refinement_entropy',abs(refined['S_m_em_response']/b['S_m_em_response']-1)<1e-8)
    check('EOS_and_time_refinement_density',abs(refined['omch2_from_packets']/b['omch2_from_packets']-1)<1e-8)
    v6=json.loads((P/'inputs/v06_thermal.json').read_text())
    check('independent_solver_v06_scale',abs(b['a_initial']/v6['a_initial_derived']-1)<1e-8)
    check('unrecalibrated_density_mismatch_detected',abs(c['old_relative_mismatch'])>.1)
    check('recalibration_recovers_target_density',abs(c['recalibrated_result']['omch2_from_packets']/c['target_omch2']-1)<1e-7)
    check('recalibrated_background_energy',c['recalibrated_result']['max_energy_work_residual']<1e-9)
    check('smooth_response_not_reused',abs(b['S_m_em_response']/r['smooth_v04_entropy_response']-1)>.5)
    seed=np.load(P/'results/local_seed_tangent.npz')
    raw=np.load(P/'inputs/quantized_seed.npz')['entropy'];raw-=raw.mean()
    check('actual_seed_not_amplitude_refitted',np.array_equal(seed['rate_modulation'],raw))
    # Exact open interval in rate modulation with exactly 128 pre-closure events.
    N=256;rate=math.log(2);times=np.cumsum(1/(rate*np.arange(N,0,-1,dtype=float)))
    low=times[127]-1;high=times[128]-1
    check('all_seed_cells_inside_differentiable_event_branch',raw.min()>low and raw.max()<high)
    check('per_cell_event_counts',all(len(schedule(Model(xi=float(x)))[0])==128 for x in raw))
    # Time derivative independently agrees with the exact schedule, not the tangent integrator.
    e=1e-5;tm=schedule(Model(xi=-e))[0];tp=schedule(Model(xi=e))[0]
    check('event_clock_derivative',np.max(abs((tp-tm)/(2*e)/(-times[:128])-1))<2e-10)
    try:injection_payload(rows);closed=False
    except IncompleteStateError as ex:closed=True;reason=str(ex)
    check('incomplete_physical_state_blocks_CAMB_claim',closed)
    scope=dict(status='DEVELOPMENT PARTIAL; step 4 is not complete',full_state_injected=False,
        new_CMB_spectrum=False,new_lensing_likelihood=False,
        executed=['64-mode conserving CDM-comoving coordinate transform',
                  'finite-packet massive-electron thermal local-cell tangent with event-time saltation',
                  'physical dark-matter density normalization and recalibration',
                  'actual 128-cell k=0 tangent application without amplitude refit'],
        blocking_reason=reason,event_count_interval=dict(lower_xi=low,upper_xi=high),
        calibration_is_not_observational_fit=True,
        original_v04_v05_v06_results_unchanged=True)
    (P/'results/full_state_gate.json').write_text(json.dumps(scope,indent=2)+'\n')
    result=dict(checks_passed=sum(checks.values()),checks=checks,
        verification_order=['verified inherited seed, thermal EOS, clock and fixed calibration target',
                            'full scalar gauge transform and common-slice event tangent',
                            'conserving adapted states, thermal density and entropy response',
                            'constraint, refinement, finite-difference and omission counterexamples'],
        scope=scope)
    (P/'results/audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print('checks passed:',result['checks_passed']);print(json.dumps(scope,indent=2))
if __name__=='__main__':main()
