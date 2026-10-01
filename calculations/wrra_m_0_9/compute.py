"""WRRA-M 0.9: executable upstream contract and common arithmetic ledger.

Expected address-weight transport is not a physical measurement instrument.
Returned addresses are represented by a downstream background-response label;
their physical energy and pressure require the explicit 0.10 map.
"""
from __future__ import annotations
from pathlib import Path
import csv
import hashlib
import json
import math
import numpy as np
from scipy.special import expit
from scipy.optimize import brentq
import importlib.util

ROOT = Path(__file__).resolve().parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


m08 = module('wrra08_common_ledger', ROOT.parent/'wrra_m_0_8/compute.py')
SECTORS = ('phenotype', 'resident_nonphenotype', 'return')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def normalized(values, length, label):
    a = np.asarray(values, dtype=float)
    if a.shape != (length,) or not np.isfinite(a).all() or (a < 0).any() or abs(a.sum()-1) > 1e-12:
        raise ValueError('invalid normalized '+label)
    return a


def integer(value, minimum, label):
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError('invalid '+label)


def validate(cfg):
    if cfg['model_version'] != 'WRRA-M 0.9' or cfg['interface_version'] != 'wrra.upstream-ledger/1':
        raise ValueError('unsupported version')
    m08.validate(cfg['baseline_0_8'])
    u = cfg['upstream']; s = u['spectrum']; k = u['update']; c = cfg['channel_coupling']
    integer(u['address_cutoff_N'], 4, 'address cutoff')
    integer(s['J_zero'], 1, 'zero cutoff')
    integer(k['admission_frames_K'], 1, 'frame boundary')
    if u['state']['kind'] != 'normalized_power_law': raise ValueError('unsupported address state')
    if s['kind'] != 'adopted_zeta_zero_heights': raise ValueError('unsupported spectrum')
    if k['frame_unit'] != 'dimensionless_order' or k['post_recovery'] != 'identity_on_resident_folds':
        raise ValueError('unsupported clock or recovery boundary')
    for key in ('gamma', 'coefficients', 'phase_offsets'):
        a = np.asarray(s[key], dtype=float)
        if a.shape != (s['J_zero'],) or not np.isfinite(a).all(): raise ValueError('invalid spectrum '+key)
    if min(s['gamma']) <= 0 or any(b <= a for a, b in zip(s['gamma'], s['gamma'][1:])):
        raise ValueError('zero heights must be positive and increasing')
    for v in (u['state']['alpha'], k['phase_step_xi'], k['sigmoid_threshold_h']):
        if not math.isfinite(v): raise ValueError('nonfinite address rule')
    if u['state']['alpha'] <= 1 or k['phase_step_xi'] < 0: raise ValueError('invalid exponent or phase step')
    beta = u['scalar_comparison']['odd_composite_admission_beta']
    if not math.isfinite(beta) or not 0 <= beta <= 1: raise ValueError('invalid scalar beta')
    normalized(list(u['targets'].values()), 3, 'targets')
    if set(u['targets']) != set(SECTORS): raise ValueError('invalid target sectors')
    if c['rule'] != 'normalized_conditional_origin_kernel_then_selected_permutation':
        raise ValueError('unsupported channel coupling')
    normalized(c['default_origin_weights'], 16, 'channel kernel')
    normalized(c['family_weights'], cfg['baseline_0_8']['family_replication']['family_count'], 'family kernel')
    for p, weights in c['odd_smallest_prime_overrides'].items():
        if not p.isdigit() or int(p) < 3 or int(p) % 2 == 0 or int(p)**2 > u['address_cutoff_N']:
            raise ValueError('invalid odd-family key')
        if any(int(p) % d == 0 for d in range(2, math.isqrt(int(p))+1)):
            raise ValueError('family key is not prime')
        normalized(weights, 16, 'family-specific channel kernel')
    for n in u['sample_addresses']:
        integer(n, 2, 'sample address')
        if n > u['address_cutoff_N']: raise ValueError('sample outside address cutoff')
    b = cfg['physical_bridge']
    expected = dict(zip(SECTORS, ('expressed', 'clustering_nonphenotype', 'background_response')))
    if b['status'] != 'pending_0.10' or b['energy_map'] is not None or b['pressure_map'] is not None:
        raise ValueError('physical energy or pressure map is outside 0.9')
    if b['branch_correspondence'] != expected: raise ValueError('unsupported structural correspondence')
    if cfg['physical_records'] or cfg['measurement_events']: raise ValueError('measurement is outside 0.9')
    for path, sha in cfg['provenance']['source_files_sha256'].items():
        file = (ROOT/path).resolve()
        if not file.is_relative_to(ROOT/'references') or hashlib.sha256(file.read_bytes()).hexdigest() != sha:
            raise ValueError('upstream source snapshot changed')


def address_base(cfg, explicit_state=None):
    u = cfg['upstream']; N = u['address_cutoff_N']
    spf = np.zeros(N+1, dtype=np.int32)
    for p in range(2, N+1):
        if spf[p] == 0:
            spf[p] = p
            if p*p <= N:
                block = spf[p*p::p]
                block[block == 0] = p
    n = np.arange(2, N+1, dtype=np.int64)
    prime = spf[2:] == n
    even = ~prime & (n % 2 == 0); odd = ~prime & (n % 2 == 1)
    w = np.exp(-u['state']['alpha']*np.log(n)); w /= w.sum()
    if explicit_state is not None: w = normalized(explicit_state, N-1, 'explicit address state')
    return {'n':n, 'spf':spf[2:], 'prime':prime, 'even':even, 'odd':odd, 'w':w}


def phase_drive(cfg, n):
    s = cfg['upstream']['spectrum']; k = cfg['upstream']['update']
    gamma = np.asarray(s['gamma'])[:, None]
    offset = np.asarray(s['phase_offsets'])[:, None]
    coeff = np.asarray(s['coefficients'])[:, None]
    return np.array([(coeff*np.cos(gamma*(np.log(n)[None, :]+k['phase_step_xi']*i)+offset)).sum(axis=0)
                     for i in range(k['admission_frames_K'])])


def effects(cfg, base, profile='frames'):
    odd = base['odd']; n = base['n']
    admission = np.zeros(len(n))
    if profile == 'frames':
        drive = phase_drive(cfg, n[odd]); h = cfg['upstream']['update']['sigmoid_threshold_h']
        admission[odd] = -np.expm1(-np.logaddexp(0, drive-h).sum(axis=0))
    elif profile == 'scalar':
        admission[odd] = cfg['upstream']['scalar_comparison']['odd_composite_admission_beta']
    else: raise ValueError('unsupported profile')
    dark = base['even'].astype(float)
    return np.array([admission, dark, 1-admission-dark])


def shares(effect, weights):
    return dict(zip(SECTORS, map(float, effect@weights)))


def frame_transport(cfg, base):
    odd = base['odd']; w = base['w']; rows = []; matter = 0.0
    dark = float(w[base['even']].sum()); prime = float(w[base['prime']].sum())
    remaining = w[odd].copy(); drive = phase_drive(cfg, base['n'][odd])
    def row(index, new, source, returned, phase):
        return {'frame':index, 'new_phenotype':new, 'phenotype':matter, 'resident_nonphenotype':dark,
                'source_pending':source, 'return':returned, 'ledger_sum':matter+dark+source+returned, 'phase':phase}
    rows.append(row(-1, 0.0, prime+float(remaining.sum()), 0.0, 'before_admission'))
    for index, delta in enumerate(drive):
        birth = remaining*expit(delta-cfg['upstream']['update']['sigmoid_threshold_h'])
        remaining -= birth; matter += float(birth.sum())
        rows.append(row(index, float(birth.sum()), prime+float(remaining.sum()), 0.0, 'admission'))
    returned = prime+float(remaining.sum()); K = len(drive)
    for index in (K, K+1, K+2):
        rows.append(row(index, 0.0, 0.0, returned, 'recovery_boundary' if index == K else 'resident_identity_update'))
    return rows


def channel_join(cfg, base, effect, reference):
    selected = reference['selection']['selected_filter']
    if selected is None: raise ValueError('no selected downstream filter')
    slots, P = m08.placement(selected)
    c = cfg['channel_coupling']; phi = base['w']*effect[0]
    default = np.asarray(c['default_origin_weights']); origin = np.zeros(16)
    remaining = np.ones(len(phi), dtype=bool)
    for p, kernel in c['odd_smallest_prime_overrides'].items():
        mask = base['spf'] == int(p)
        family_mass = float(phi[mask].sum())
        origin += family_mass*np.asarray(kernel)
        remaining &= ~mask
    origin += float(phi[remaining].sum())*default
    mapped = P@origin
    inventory = m08.replicate_families(reference, cfg['baseline_0_8'])['particle_inventory']
    rows = []
    for item in inventory:
        row = dict(item); index = row['target_index']
        row['arithmetic_phenotype_weight'] = float(c['family_weights'][row['generation']-1]*mapped[index])
        rows.append(row)
    return rows


def scope_rows(terminal):
    resident = terminal['phenotype']+terminal['resident_nonphenotype']
    return [{'scope':'complete_current_Actual', 'denominator':1.0, 'phenotype':terminal['phenotype'],
             'resident_nonphenotype':terminal['resident_nonphenotype'], 'return_background_response':terminal['return'],
             'sum':sum(terminal.values())},
            {'scope':'upstream_resident_Actual_conditional', 'denominator':resident,
             'phenotype':terminal['phenotype']/resident,
             'resident_nonphenotype':terminal['resident_nonphenotype']/resident,
             'return_background_response':0.0, 'sum':1.0}]


def csv_write(path, rows):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def calibrate(cfg, base):
    """Explicit arithmetic refit only; never called silently by run()."""
    u = cfg['upstream']; logn = np.log(base['n'])
    def trial(a):
        v = np.exp(-a*logn); return v/v.sum()
    alpha = float(brentq(lambda a: float(trial(a)[base['even']].sum())-u['targets']['resident_nonphenotype'],
                        1.01, 4.0, xtol=1e-12))
    w = trial(alpha); oddw = w[base['odd']]; drive = phase_drive(cfg, base['n'][base['odd']])
    h = float(brentq(lambda v: float(oddw@(-np.expm1(-np.logaddexp(0, drive-v).sum(axis=0))))-u['targets']['phenotype'],
                    -30, 30, xtol=1e-12))
    return {'alpha':alpha, 'threshold_h':h, 'derived_effective_beta':u['targets']['phenotype']/float(oddw.sum()),
            'input_degrees_of_freedom':'alpha and h fitted to two independent arithmetic targets; return closes the ledger; beta_eff is derived'}


def run(cfg, out):
    validate(cfg); hashed = digest(cfg); base = address_base(cfg)
    effect = effects(cfg, base); terminal = shares(effect, base['w']); scalar = shares(effects(cfg, base, 'scalar'), base['w'])
    baseline = m08.run(cfg['baseline_0_8'], out/'baseline_0_8')
    reference = next(v for v in baseline['cases'] if v['case_name'] == 'uniform_a1.0')
    joined = channel_join(cfg, base, effect, reference); frames = frame_transport(cfg, base)
    samples = [{'address':n, 'smallest_prime_factor':int(base['spf'][n-2]),
                'normalized_address_weight':float(base['w'][n-2]),
                **{s+'_effect':float(effect[i,n-2]) for i,s in enumerate(SECTORS)}} for n in cfg['upstream']['sample_addresses']]
    comparisons = []
    for a in (2.0, 1.9):
        w = np.exp(-a*np.log(base['n'])); w /= w.sum()
        comparisons.append({'alpha':a, 'full_odd_composite_share':float(w[base['odd']].sum()),
                            'even_composite_share':float(w[base['even']].sum()), 'prime_share':float(w[base['prime']].sum())})
    old = cfg['baseline_0_8']['ledger_0_7']['calibration_and_local_source']
    physical = {'phenotype':old['fraction_phenotype'], 'clustering':old['fraction_twist_clustering'],
                'background':1-old['fraction_phenotype']-old['fraction_twist_clustering']}
    result = {'version':'WRRA-M 0.9', 'date':'2026-10-01', 'input_hash_sha256':hashed,
              'input_ledger':cfg, 'terminal_common_arithmetic_ledger':terminal,
              'scalar_comparison_ledger':scalar, 'upstream_resident_Actual':terminal['phenotype']+terminal['resident_nonphenotype'],
              'complete_current_Actual':sum(terminal.values()), 'scope_rows':scope_rows(terminal),
              'frame_transport':frames, 'address_samples':samples, 'separate_exponent_comparisons':comparisons,
              'derived_effective_beta':terminal['phenotype']/float(base['w'][base['odd']].sum()),
              'channel_phenotype_weight_sum':sum(v['arithmetic_phenotype_weight'] for v in joined),
              'channel_inventory':joined, 'selected_filter':reference['selection']['selected_filter'],
              'inherited_physical_reference_0_8':physical, 'physical_bridge':cfg['physical_bridge'],
              'cutoffs':{'address_N':len(base['n'])+1, 'zero_J':cfg['upstream']['spectrum']['J_zero'],
                         'carrier_lattice_N':reference['lattice_N'], 'physical_capacity_bits':None},
              'physical_records':[], 'measurement_events':[],
              'claim_scope':'same-denominator arithmetic transport and conditional channel routing; SI energy/pressure bridge pending 0.10; physical measurement pending 0.13',
              'falsification_conditions':['negative or incomplete address effects or frame ledger',
                  'failure to reproduce declared upstream calibration with frozen inputs',
                  'conditional routing changes sector totals or charges or double counts family/channel multiplicity',
                  'scope mismatch, unreported calibration change, or treating arithmetic transport as SI pressure or physical measurement']}
    if digest(cfg) != hashed: raise RuntimeError('input mutated')
    out.mkdir(parents=True, exist_ok=True)
    (out/'results.json').write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+'\n')
    for name, rows in (('frame_ledger',frames), ('scope_table',result['scope_rows']),
                       ('channel_ledger',joined), ('address_samples',samples), ('exponent_comparisons',comparisons)):
        csv_write(out/(name+'.csv'), rows)
    return result


if __name__ == '__main__':
    result = run(json.loads((ROOT/'parameters.json').read_text()), ROOT/'results')
    print(json.dumps({k:result[k] for k in ('version','terminal_common_arithmetic_ledger','upstream_resident_Actual','complete_current_Actual','selected_filter')}, indent=2))
