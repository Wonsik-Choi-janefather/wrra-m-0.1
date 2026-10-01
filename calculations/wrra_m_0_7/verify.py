"""Independent physical-accounting checks for the 0.7 release."""
import copy
from fractions import Fraction
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
import compute as m

ROOT = Path(__file__).resolve().parent


def main():
    cfg = json.loads((ROOT / 'parameters.json').read_text())
    result = m.run(cfg, ROOT / 'results')
    checks = []
    def check(name, condition, **metrics):
        if not condition:
            raise AssertionError(name + ': ' + str(metrics))
        checks.append({'name': name, 'passed': True, **metrics})
    cases = result['cases']
    present = next(x for x in cases if x['case_name'] == 'uniform_a1.0')
    p, b = cfg['carrier_and_background'], cfg['calibration_and_local_source']
    N = p['lattice_N']
    carrier = m.m06.Carrier(N, p['noncommuting_test_strength'])
    rho = m.state_from_recipe(carrier, {'kind': 'packet',
        'modes': p['noncommuting_test_initial_modes'], 'weights': p['noncommuting_test_initial_weights']})
    # Rational arithmetic is independent of density-matrix trace arithmetic.
    fp = Fraction(str(b['fraction_phenotype']))
    fc = Fraction(str(b['fraction_twist_clustering']))
    fb = 1 - fp - fc
    exact_error = 0.0
    for a in (Fraction(1, 2), Fraction(1), Fraction(2)):
        row = next(x for x in cases if x['case_name'] == 'uniform_a' + str(float(a)))
        denominator = fp + fc + fb * a ** 3
        expected = (fp / denominator, fc / denominator, fb * a ** 3 / denominator)
        exact_error = max(exact_error, *(abs(float(e) - row['sector_shares'][s]) for e, s in zip(expected, m.SECTORS)))
    check('exact_reference_fraction_at_three_scales', exact_error < 1e-13, maximum_absolute_error=exact_error)
    partition_error = max(x['invariants']['weight_partition_absolute_error'] for x in cases)
    share_error = max(x['invariants']['share_partition_absolute_error'] for x in cases)
    check('positive_additive_weight_and_normalized_partition',
          all(min(x['sector_weights'].values()) >= 0 for x in cases) and partition_error < 1e-12 and share_error < 1e-12,
          weight_max_error=partition_error, share_max_error=share_error)
    density_error = max(x['bridge_0_6']['density_absolute_error_J_m3'] for x in cases)
    pressure_error = max(x['bridge_0_6']['pressure_absolute_error_Pa'] for x in cases)
    check('same_energy_and_pressure_as_0_6_r2', density_error < 1e-20 and pressure_error < 1e-20,
          density_max_absolute_error_J_m3=density_error, pressure_max_absolute_error_Pa=pressure_error)
    old = json.loads((m.BASE / 'results/summary.json').read_text())
    old_state = next(x for x in old['present_information_state_outputs'] if x['state'] == 'uniform')
    local = present['bridge_0_6']['local_readout']
    velocity_error = abs(local['v_total_km_s'] - old_state['v_total_km_s'])
    lens_error = abs(local['finite_patch_lensing']['alpha_patch_rad'] - old_state['finite_patch_lensing']['alpha_patch_rad'])
    check('inherited_reference_rotation_and_lensing', velocity_error < 1e-12 and lens_error < 1e-18,
          velocity_absolute_error_km_s=velocity_error, lens_absolute_error_rad=lens_error)
    # Pressure must be the finite-volume derivative of the same energy.
    fd_error = 0.0
    for a in (0.5, 1.0, 2.0):
        V = cfg['reference_volume_m3'] * a ** 3
        delta = V * 1e-5
        minus = m.ledger(((V-delta)/cfg['reference_volume_m3'])**(1/3), rho, carrier, cfg)
        plus = m.ledger(((V+delta)/cfg['reference_volume_m3'])**(1/3), rho, carrier, cfg)
        middle = m.ledger(a, rho, carrier, cfg)
        derivative = -(plus['total_energy_J']-minus['total_energy_J'])/(2*delta)
        fd_error = max(fd_error, abs(derivative-middle['total_pressure_Pa'])/max(abs(middle['total_pressure_Pa']),1e-30))
    check('pressure_from_independent_volume_difference', fd_error < 1e-7, maximum_relative_error=fd_error)
    # A simultaneous state/operator basis transformation cannot change the load.
    phase = np.exp(1j * np.arange(N) * 0.217)
    U = np.diag(phase) @ np.roll(np.eye(N), 7, axis=0)
    transformed = m.m06.Carrier(N, p['noncommuting_test_strength'])
    transformed.Kc = U @ carrier.Kc @ U.conj().T
    transformed.Kb = U @ carrier.Kb @ U.conj().T
    original = m.ledger(1.0, rho, carrier, cfg)
    alternate = m.ledger(1.0, U @ rho @ U.conj().T, transformed, cfg)
    basis_error = max(abs(original['sector_weights'][s]-alternate['sector_weights'][s]) for s in m.SECTORS)
    check('joint_basis_covariance', basis_error < 1e-12, maximum_weight_error=basis_error)
    # Unitary propagation at a fixed scale preserves total energy and eigenvalues.
    a = 0.8
    A = m.operators(a, carrier, cfg)
    unitary = expm(-0.4j * sum(A))
    evolved = unitary @ rho @ unitary.conj().T
    before, after = m.ledger(a, rho, carrier, cfg), m.ledger(a, evolved, carrier, cfg)
    energy_relative_error = abs(after['total_energy_J']/before['total_energy_J']-1)
    spectral_error = float(np.max(np.abs(np.linalg.eigvalsh(rho)-np.linalg.eigvalsh(evolved))))
    sector_change = max(abs(after['sector_weights'][s]-before['sector_weights'][s]) for s in m.SECTORS)
    check('fixed_scale_unitary_energy_and_state_spectrum', energy_relative_error < 1e-12 and spectral_error < 1e-12,
          energy_relative_error=energy_relative_error, state_spectrum_max_error=spectral_error,
          sector_weights_change=sector_change)
    # Test normalized random mixed states and nonpreferred exponents.
    rng = np.random.default_rng(707)
    random_count = 0
    random_partition_error = 0.0
    for testN in (32, 64):
        cc = copy.deepcopy(cfg)
        cc['carrier_and_background']['lattice_N'] = testN
        for epsilon in (0.0, 8.0):
            C = m.m06.Carrier(testN, epsilon)
            X = rng.normal(size=(testN, 4)) + 1j*rng.normal(size=(testN, 4))
            mixed = X @ X.conj().T
            mixed /= np.trace(mixed).real
            for nb in (1.0, 3.0):
                cc['carrier_and_background']['background_energy_exponent'] = nb
                for aa in (0.5, 1.0, 2.0):
                    row = m.ledger(aa, mixed, C, cc)
                    random_partition_error = max(random_partition_error, row['invariants']['weight_partition_absolute_error'])
                    if min(row['sector_weights'].values()) < 0:
                        raise AssertionError('negative random-state weight')
                    random_count += 1
    check('admissible_mixed_states_and_exponent_changes', random_partition_error < 1e-12,
          evaluated_cases=random_count, maximum_partition_error=random_partition_error)
    # Recalibration is explicit and changes the computed reference.
    recalibrated = copy.deepcopy(cfg)
    recalibrated['calibration_and_local_source']['fraction_phenotype'] = 0.08
    rr = m.ledger(1.0, np.eye(N)/N, carrier, recalibrated)
    check('declared_recalibration_propagates', abs(rr['sector_shares']['phenotype']-.08) < 1e-13
          and m.digest(recalibrated) != result['input_hash_sha256'],
          recalibrated_phenotype_share=rr['sector_shares']['phenotype'])
    cc = copy.deepcopy(cfg)
    cc['reference_volume_m3'] = 13.0
    unit = m.ledger(1.0, np.eye(N)/N, carrier, cfg)
    larger = m.ledger(1.0, np.eye(N)/N, carrier, cc)
    check('bookkeeping_volume_does_not_change_density_or_share',
          math.isclose(larger['total_energy_J']/unit['total_energy_J'],13,rel_tol=1e-14)
          and math.isclose(larger['total_density_J_m3'],unit['total_density_J_m3'],rel_tol=1e-14)
          and math.isclose(larger['sector_shares']['phenotype'],unit['sector_shares']['phenotype'],rel_tol=1e-14))
    low = next(x for x in cases if x['case_name'] == 'low_mode_a1.0')
    high = next(x for x in cases if x['case_name'] == 'high_mode_a1.0')
    check('information_weight_is_distinct_from_entropy_or_state_count',
          low['state_entropy_bits'] < 1e-10 and high['state_entropy_bits'] < 1e-10
          and abs(low['sector_shares']['phenotype']-high['sector_shares']['phenotype']) > 0.1,
          low_mode_phenotype_share=low['sector_shares']['phenotype'],
          high_mode_phenotype_share=high['sector_shares']['phenotype'])
    # Zero weighted load can coexist with a trace-one carrier state.
    zero = copy.deepcopy(cfg)
    zero['calibration_and_local_source']['fraction_phenotype'] = 0.0
    plain = m.m06.Carrier(N, 0.0)
    z = m.ledger(1.0, m.state_from_recipe(plain, {'kind':'mode','mode':0}), plain, zero)
    check('zero_total_weight_is_undefined_fraction_not_false_probability',
          z['total_actual_weight'] == 0 and z['actual_normalized_share'] is None
          and all(v is None for v in z['sector_shares'].values())
          and z['bridge_0_6']['snapshot']['H_over_H0'] == 0,
          state_trace=z['state_trace'])
    boundary = copy.deepcopy(cfg)
    boundary['calibration_and_local_source']['fraction_phenotype'] = 1-b['fraction_twist_clustering']
    row = m.ledger(1.0, rho, carrier, boundary)
    check('zero_background_sector', row['sector_weights']['hidden_background'] == 0 and row['total_pressure_Pa'] == 0)
    rejected = []
    invalids = []
    for name, group, key, value in (
        ('negative_fraction','calibration_and_local_source','fraction_phenotype',-0.1),
        ('overallocated_fractions','calibration_and_local_source','fraction_phenotype',0.9),
        ('changed_SI_c','calibration_and_local_source','c_m_s',3e8),
        ('nan_H0','calibration_and_local_source','H0_km_s_Mpc',float('nan')),
        ('invalid_grid','carrier_and_background','lattice_N',5),
        ('negative_epsilon','carrier_and_background','noncommuting_test_strength',-1),
    ):
        invalid = copy.deepcopy(cfg)
        invalid[group][key] = value
        invalids.append((name, invalid))
    fake = copy.deepcopy(cfg); fake['physical_records'] = [{'outcome':0}]
    invalids.append(('unexecuted_physical_record',fake))
    for name, invalid in invalids:
        try: m.validate(invalid)
        except ValueError: rejected.append(name)
        else: raise AssertionError('accepted invalid input '+name)
    negative = np.zeros((N,N)); negative[0,0] = 1.1; negative[1,1] = -.1
    for name, invalid in [('negative_state',negative), ('wrong_trace',np.eye(N))]:
        try: m.validate_state(invalid,N)
        except ValueError: rejected.append(name)
        else: raise AssertionError('accepted invalid state '+name)
    check('invalid_inputs_and_states_rejected', len(rejected) == 9, rejected_cases=rejected)
    check('no_fictitious_measurement_or_double_counted_record',
          all(x['measurement_outcome_probabilities'] is None and x['physical_records'] == []
              and set(x['sector_energy_J']) == set(m.SECTORS) for x in cases))
    check('input_ledger_preserved', m.digest(cfg) == result['input_hash_sha256'])
    tiny = copy.deepcopy(cfg)
    tiny['calibration_and_local_source']['fraction_phenotype'] = 1e-15
    zero_state = m.state_from_recipe(plain, {'kind':'mode','mode':0})
    row = m.ledger(1.0, zero_state, plain, tiny)
    check('tiny_positive_load_is_retained_with_matching_gravity',
          row['sector_weights']['phenotype'] == 1e-15
          and row['actual_normalized_share'] == 1
          and row['sector_shares']['phenotype'] == 1
          and math.isclose(row['total_density_J_m3'],
              m.m06.calibration(tiny['calibration_and_local_source'])['ucrit_J_m3'] * 1e-15, rel_tol=1e-14),
          phenotype_weight=row['sector_weights']['phenotype'],
          H_over_H0=row['bridge_0_6']['snapshot']['H_over_H0'])
    near_trace = np.eye(N) / N * (1+9e-11)
    normalized = m.validate_state(near_trace, N)
    normalized_row = m.ledger(1.0, near_trace, plain, cfg)
    check('accepted_trace_roundoff_is_normalized_before_accounting',
          abs(np.trace(normalized)-1) < 1e-14
          and abs(normalized_row['total_actual_weight']-1) < 1e-14,
          incoming_trace=float(np.trace(near_trace)),
          effective_trace=float(np.trace(normalized).real))
    negative = np.zeros((N,N)); negative[0,0]=1+9e-11; negative[1,1]=-9e-11
    try: m.validate_state(negative,N)
    except ValueError: rejected_small_negative=True
    else: rejected_small_negative=False
    check('negative_state_above_roundoff_is_rejected', rejected_small_negative)
    report = {'version':'WRRA-M 0.7', 'passed':True, 'check_count':len(checks),
              'input_hash_sha256':result['input_hash_sha256'], 'checks':checks}
    (ROOT/'results/verification.json').write_text(json.dumps(report,indent=2,allow_nan=False))
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
