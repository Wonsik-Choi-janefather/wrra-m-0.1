"""WRRA-M 0.7: positive weighted Actual ledger, using the frozen 0.6-r2 bridge.

This release defines a measure and an accounting interface. It does not execute
particle filter selection or a measurement/quantization event. Shares below are
energy-weighted allocations, never probabilities for measurement outcomes.
"""
from __future__ import annotations
import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'wrra_m_0_6'
spec = importlib.util.spec_from_file_location('wrra06_ledger_bridge', BASE / 'compute.py')
m06 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m06)
SECTORS = ('phenotype', 'hidden_clustering', 'hidden_background')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
        separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def validate(cfg):
    if cfg['model_version'] != 'WRRA-M 0.7':
        raise ValueError('unsupported model version')
    p, b = cfg['carrier_and_background'], cfg['calibration_and_local_source']
    m06.validate(p, b)
    if b['c_m_s'] != 299792458.0:
        raise ValueError('c is the fixed SI defining value')
    if not math.isfinite(cfg['reference_volume_m3']) or cfg['reference_volume_m3'] <= 0:
        raise ValueError('reference volume must be finite and positive')
    if cfg['measure'] != 'energy_weighted_information_load':
        raise ValueError('unsupported measure')
    # None of these empty fields stands for a physical measurement result.
    if cfg.get('measurement_events', []) or cfg.get('physical_records', []):
        raise ValueError('measurement events belong to the later quantization release')


def validate_state(rho, N):
    rho = np.asarray(rho, dtype=complex)
    if rho.shape != (N, N) or not np.isfinite(rho).all():
        raise ValueError('invalid density-matrix shape or finite entries')
    if np.linalg.norm(rho - rho.conj().T) > 1e-10:
        raise ValueError('state is not Hermitian')
    if abs(np.trace(rho) - 1) > 1e-10:
        raise ValueError('state trace is not one')
    if np.linalg.eigvalsh(rho).min() < -1e-10:
        raise ValueError('state is not positive semidefinite')
    return rho


def operators(a, carrier, cfg):
    if not math.isfinite(a) or a <= 0:
        raise ValueError('scale factor must be finite and positive')
    p, b = cfg['carrier_and_background'], cfg['calibration_and_local_source']
    fp, fc = b['fraction_phenotype'], b['fraction_twist_clustering']
    fb = 1 - fp - fc
    return (fp * np.eye(carrier.N),
            fc / 2 * a ** p['clustering_energy_exponent'] * carrier.Kc,
            fb / 2 * a ** p['background_energy_exponent'] * carrier.Kb)


def ledger(a, rho, carrier, cfg, *, validate_rho=True):
    """Compute additive positive weights, SI energy, pressure and the 0.6 bridge."""
    if validate_rho:
        rho = validate_state(rho, carrier.N)
    A = operators(a, carrier, cfg)
    raw = [float(np.trace(rho @ op).real) for op in A]
    if min(raw) < -1e-10:
        raise ValueError('negative sector weight')
    # Only remove numerical zeros, without hiding negative physical weights.
    weights = [0.0 if abs(x) < 1e-13 else x for x in raw]
    total = sum(weights)
    shares = [x / total for x in weights] if total > 0 else [None] * 3
    p, b = cfg['carrier_and_background'], cfg['calibration_and_local_source']
    c = m06.calibration(b)
    u0, V0 = c['ucrit_J_m3'], cfg['reference_volume_m3']
    volume = V0 * a ** 3
    energies = [u0 * V0 * w for w in weights]
    densities = [e / volume for e in energies]
    exponents = (0.0, p['clustering_energy_exponent'], p['background_energy_exponent'])
    pressures = [-n * u / 3 for n, u in zip(exponents, densities)]
    jc = float(np.trace(rho @ carrier.Kc).real)
    jb = float(np.trace(rho @ carrier.Kb).real)
    jc = 0.0 if abs(jc) < 1e-13 else jc
    jb = 0.0 if abs(jb) < 1e-13 else jb
    inherited = m06.snapshot(a, jc, jb, p, c)
    local = m06.local_readout(inherited, p, b, c)
    eig = np.linalg.eigvalsh(rho)
    positive = eig[eig > 1e-13]
    entropy = float(-np.sum(positive * np.log2(positive)))
    E = sum(energies)
    pressure = sum(pressures)
    expected_u = u0 * inherited['density_total_over_ucrit']
    expected_pressure = u0 * inherited['pressure_over_ucrit']
    return {
        'scale_factor': a, 'lattice_N': carrier.N,
        'carrier_epsilon': carrier.epsilon,
        'state_trace': float(np.trace(rho).real),
        'state_entropy_bits': max(0.0, entropy),
        'state_rank_at_tolerance': int(len(positive)), 'Jc': jc, 'Jb': jb,
        'measure': cfg['measure'],
        'reference_volume_m3': V0, 'physical_volume_m3': volume,
        'sector_weights': dict(zip(SECTORS, weights)),
        'total_actual_weight': total,
        'actual_normalized_share': 1.0 if total > 0 else None,
        'sector_shares': dict(zip(SECTORS, shares)),
        'hidden_share': shares[1] + shares[2] if total > 0 else None,
        'sector_energy_J': dict(zip(SECTORS, energies)), 'total_energy_J': E,
        'sector_density_J_m3': dict(zip(SECTORS, densities)),
        'total_density_J_m3': E / volume,
        'sector_pressure_Pa': dict(zip(SECTORS, pressures)),
        'total_pressure_Pa': pressure,
        'quantization_status': 'not_executed_in_0.7',
        'measurement_outcome_probabilities': None,
        'physical_records': [], 'measurement_energy_transfers': [],
        'record_energy_policy': 'future record energy is a sector suballocation, not an extra fourth sector',
        'residue_policy': 'unexpressed state content retained; not equated with a bit count or a fourth energy component',
        'bridge_0_6': {'snapshot': inherited, 'local_readout': local,
            'density_absolute_error_J_m3': abs(E / volume - expected_u),
            'pressure_absolute_error_Pa': abs(pressure - expected_pressure)},
        'invariants': {
            'weight_partition_absolute_error': abs(float(np.trace(rho @ sum(A)).real) - total),
            'share_partition_absolute_error': abs(sum(shares) - 1) if total > 0 else None,
            'energy_partition_absolute_error_J': abs(sum(energies) - E),
            'state_rank': int(len(positive))}
    }


def state_from_recipe(carrier, recipe):
    if recipe['kind'] == 'uniform':
        return np.eye(carrier.N) / carrier.N
    if recipe['kind'] == 'mode':
        v = carrier.wave(recipe['mode'])
    elif recipe['kind'] == 'packet':
        v = carrier.packet(recipe['modes'], recipe['weights'])
    else:
        raise ValueError('unknown state recipe')
    return np.outer(v, v.conj())


def provenance(cfg):
    records = []
    for group in ('carrier_and_background', 'calibration_and_local_source'):
        for key, value in cfg[group].items():
            kind = 'constitutive_choice' if group == 'carrier_and_background' else 'inherited_calibration_or_source'
            if key in ('c_m_s',):
                kind = 'SI_defining_constant'
            if key in ('G_SI', 'M_sun_kg', 'parsec_m', 'electron_mass_energy_eV'):
                kind = 'inherited_constant_or_unit_conversion'
            if key in ('fraction_phenotype', 'fraction_twist_clustering', 'H0_km_s_Mpc'):
                kind = 'editable_late_universe_calibration'
            records.append({'path': group + '.' + key, 'value': value, 'classification': kind,
                'source': 'WRRA-M 0.6-r2 input ledger, DOI 10.5281/zenodo.23076547'})
    records += [{'path': 'reference_volume_m3', 'value': cfg['reference_volume_m3'],
                 'classification': 'bookkeeping_unit_volume', 'source': '0.7 convention; not cosmic size'},
                {'path': 'measure', 'value': cfg['measure'], 'classification': 'WRRA_measure_choice',
                 'source': '0.7 additive positive sector-load definition'}]
    return records


def run(cfg, out):
    validate(cfg)
    original_hash = digest(cfg)
    p = cfg['carrier_and_background']
    N = p['lattice_N']
    plain = m06.Carrier(N, 0.0)
    coupled = m06.Carrier(N, p['noncommuting_test_strength'])
    recipes = [('uniform', {'kind': 'uniform'}),
               ('low_mode', {'kind': 'mode', 'mode': N // 16}),
               ('high_mode', {'kind': 'mode', 'mode': N // 2}),
               ('zero_mode', {'kind': 'mode', 'mode': 0}),
               ('coherent_packet', {'kind': 'packet',
                   'modes': p['noncommuting_test_initial_modes'],
                   'weights': p['noncommuting_test_initial_weights']})]
    cases = []
    for name, recipe in recipes:
        for a in ([0.5, 1.0, 2.0] if name == 'uniform' else [1.0]):
            row = ledger(a, state_from_recipe(plain, recipe), plain, cfg)
            row.update(case_name=name + '_a' + str(a), state_recipe=recipe)
            cases.append(row)
    for name, recipe in (recipes[0], recipes[-1]):
        row = ledger(1.0, state_from_recipe(coupled, recipe), coupled, cfg)
        row.update(case_name=name + '_noncommuting_a1.0', state_recipe=recipe)
        cases.append(row)
    result = {'version': 'WRRA-M 0.7', 'date': '2026-10-01', 'author': 'Wonsik Choi',
        'input_hash_sha256': original_hash,
        'input_ledger': cfg, 'input_provenance': provenance(cfg), 'cases': cases,
        'scope': 'positive weighted Actual partition and exact 0.6-r2 bridge; no quantization event',
        'claims': [
            {'id': 'C07-1', 'kind': 'definition', 'claim': 'Actual 100 percent is normalized total modeled weighted load'},
            {'id': 'C07-2', 'kind': 'constitutive_mapping', 'claim': 'energy-weighted information load maps to the same comoving energy as 0.6-r2'},
            {'id': 'C07-3', 'kind': 'calibrated_reproduction', 'claim': 'reference phenotype share is 0.0493 at a=1 and rho=I/N'},
            {'id': 'C07-4', 'kind': 'internal_calculation', 'claim': 'state and scale changes recalculate shares and preserve sector accounting'},
            {'id': 'C07-5', 'kind': 'scope_boundary', 'claim': 'measurement probabilities, outcomes and records remain unexecuted'},
        ], 'handoff': {'0.8': 'channel/filter labels attached to the same input ledger',
             '0.9': 'physical measurement event and record-generation law',
             '0.10': 'repeated events and uncertainty propagation',
             '0.11': 'measurement energy exchange and coupled load update',
             '0.12': 'whole-model reproducibility and claim freeze'},
        'falsification_conditions': ['negative sector weight from admissible positive state',
            'partition or normalization failure', '0.6 energy/pressure/local bridge mismatch',
            'fractions or constants secretly changed outside the hashed input ledger',
            'claiming measurement or filter selection without executing the corresponding law']}
    if digest(cfg) != original_hash:
        raise RuntimeError('input ledger was modified during calculation')
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    with (out / 'case_table.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['case', 'a', 'Jc', 'Jb', 'phenotype_share', 'hidden_share', 'total_weight', 'H_over_H0', 'q'])
        for x in cases:
            writer.writerow([x['case_name'], x['scale_factor'], x['Jc'], x['Jb'],
                x['sector_shares']['phenotype'], x['hidden_share'], x['total_actual_weight'],
                x['bridge_0_6']['snapshot']['H_over_H0'], x['bridge_0_6']['snapshot']['deceleration_q']])
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--parameters', default=str(ROOT / 'parameters.json'))
    ap.add_argument('--out', default=str(ROOT / 'results'))
    args = ap.parse_args()
    r = run(json.loads(Path(args.parameters).read_text()), Path(args.out))
    present = next(x for x in r['cases'] if x['case_name'] == 'uniform_a1.0')
    print(json.dumps({'version': r['version'], 'cases': len(r['cases']),
        'phenotype_share': present['sector_shares']['phenotype'],
        'hidden_share': present['hidden_share'], 'q': present['bridge_0_6']['snapshot']['deceleration_q'],
        'input_hash_sha256': r['input_hash_sha256']}, indent=2))
