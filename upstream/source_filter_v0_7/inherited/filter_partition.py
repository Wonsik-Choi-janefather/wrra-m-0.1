#!/usr/bin/env python3
"""Candidate Actual/phenotype partition for the WRRA upstream hypothesis.

The assignment of the smallest-prime-factor-2 family to unexpressed Actual
is a declared trial rule, not a derived physical identification.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from compute import prime_mask


ROOT = Path(__file__).resolve().parent
N = 1_000_000
TARGET_DARK = .268
TARGET_MATTER = .05


def sectors(N, alpha, beta):
    numbers = np.arange(2, N + 1, dtype=np.int64)
    prime = prime_mask(N)[2:]
    composite = ~prime
    even = composite & (numbers % 2 == 0)
    odd = composite & (numbers % 2 != 0)
    weight = numbers.astype(float) ** (-alpha)
    weight /= weight.sum()

    # Conditional branch assignment: lowest-prime 2 family -> unexpressed Actual.
    dark_effect = even.astype(float)
    matter_effect = beta * odd.astype(float)
    # Prime SOURCE addresses return; a rejected initial odd relation is reflected.
    source_effect = prime.astype(float) + (1 - beta) * odd.astype(float)
    row = {
        'N': N, 'alpha': alpha, 'initial_odd_relation_admission': beta,
        'unexpressed_Actual_fraction': float(weight @ dark_effect),
        'phenotype_fraction': float(weight @ matter_effect),
        'source_return_fraction': float(weight @ source_effect),
        'odd_composite_available_fraction': float(weight[odd].sum()),
        'even_composite_available_fraction': float(weight[even].sum()),
        'ledger_sum': float(weight @ (dark_effect + matter_effect + source_effect)),
        'Actual_total_fraction': float(weight @ (dark_effect + matter_effect)),
        'effect_completeness_max_error': float(np.max(np.abs(dark_effect + matter_effect + source_effect - 1))),
        'all_effects_between_zero_and_one': bool(0 <= beta <= 1),
    }
    # Normal zero-dimensional return gate: no fold permits return. Arithmetic
    # primality serves as a proxy for no fold. Composite fold retention is a rule.
    actual_support = composite
    normal_zero_return = prime
    row['Actual_has_no_allowed_return_under_declared_fold_rule'] = bool(not np.any(actual_support & normal_zero_return))
    small = np.arange(2, N // 2 + 1, dtype=float)
    row['even_family_from_prime2_factor_identity'] = float(2 ** (-alpha) * (small ** (-alpha)).sum() / (numbers.astype(float) ** (-alpha)).sum())
    return row


def smallest_prime_families(N, alpha):
    numbers = np.arange(2, N + 1, dtype=np.int64)
    prime = prime_mask(N)
    remaining = ~prime[2:]
    weight = numbers.astype(float) ** (-alpha)
    weight /= weight.sum()
    rows = []
    for p0 in np.flatnonzero(prime[:math.isqrt(N) + 1]):
        p = int(p0)
        family = remaining & (numbers % p == 0)
        rows.append({'smallest_prime_factor': p,
                     'address_count': int(family.sum()),
                     'weight_fraction': float(weight[family].sum())})
        remaining[family] = False
    assert not remaining.any()
    return rows


def main():
    prime = prime_mask(N)[2:]
    numbers = np.arange(2, N + 1, dtype=np.int64)
    logn = np.log(numbers)
    even = (~prime) & (numbers % 2 == 0)
    odd = (~prime) & (numbers % 2 != 0)

    def weights(alpha):
        w = np.exp(-alpha * logn)
        return w / w.sum()

    def fraction(mask, alpha):
        return float(weights(alpha)[mask].sum())

    alpha = float(brentq(lambda a: fraction(even, a) - TARGET_DARK, 1.8, 2.0, xtol=1e-12))
    beta = float(TARGET_MATTER / fraction(odd, alpha))
    baseline = sectors(N, alpha, beta)

    scan = []
    for a in np.linspace(.5, 3., 26):
        scan.append({'alpha': float(a), 'prime2_family_weight': fraction(even, float(a)),
                     'odd_composite_weight': fraction(odd, float(a))})
    nearest = min(scan, key=lambda r: abs(r['prime2_family_weight'] - TARGET_DARK))
    families = smallest_prime_families(N, alpha)
    pre = sectors(N, 2., 1.)
    checks = {
        'all_effects_between_zero_and_one': baseline['all_effects_between_zero_and_one'],
        'per_address_three_way_completeness': baseline['effect_completeness_max_error'] < 1e-12,
        'weighted_three_way_ledger': abs(baseline['ledger_sum'] - 1) < 1e-12,
        'matter_target_reproduced': abs(baseline['phenotype_fraction'] - TARGET_MATTER) < 1e-10,
        'dark_target_reproduced': abs(baseline['unexpressed_Actual_fraction'] - TARGET_DARK) < 1e-10,
        'normal_zero_return_blocks_Actual_by_declared_rule': baseline['Actual_has_no_allowed_return_under_declared_fold_rule'],
        'prime2_family_factorization_identity': abs(baseline['unexpressed_Actual_fraction'] - baseline['even_family_from_prime2_factor_identity']) < 1e-12,
        'smallest_prime_families_partition_all_composites': abs(sum(r['weight_fraction'] for r in families) - baseline['odd_composite_available_fraction'] - baseline['even_composite_available_fraction']) < 1e-12,
    }
    checks['all_passed'] = all(checks.values())
    result = {
        'title': 'WRRA upstream 26.8% unexpressed Actual candidate',
        'date': '2026-10-01', 'author': 'Wonsik Choi',
        'same_denominator_targets': {'phenotype': .05, 'unexpressed_Actual': .268, 'total_Actual': .318, 'source_return': .682},
        'weight_rule': 'w_n=n^(-alpha)/sum_{m=2..N} m^(-alpha)',
        'candidate_partition_rule': {
            'prime2_family': 'all even composites, n=2m with m>=2, assigned to unexpressed Actual',
            'other_composite_families': 'odd composites; admitted fraction beta assigned to phenotype',
            'source_return': 'prime addresses plus rejected initial odd-composite attempts',
            'rule_status': 'declared arithmetic proxy; physical dark/matter response not yet derived',
            'normal_filter_recovery': 'all admitted composite folds are in the blocked subspace of the declared 0D return gate',
        },
        'prime2_identity': 'f_2(N,alpha)=2^(-alpha) Z_floor(N/2)(alpha)/Z_N(alpha), Z_N=sum_{n=2..N} n^(-alpha)',
        'coarse_exponent_scan': scan,
        'closest_coarse_scan_case': nearest,
        'calibration': {'alpha_fitted_to_26_8_percent': alpha,
                        'beta_fitted_to_5_percent': beta,
                        'particle_constants_used_to_fit_alpha_or_beta': False},
        'joint_output': baseline,
        'old_alpha2_full_composite_limit': pre,
        'fixed_parameter_N_sensitivity': [sectors(k, alpha, beta) for k in (10000, 100000, N)],
        'fixed_parameter_alpha_sensitivity': [sectors(N, alpha + da, beta) for da in (-.01, 0., .01)],
        'smallest_prime_family_contributions': families,
        'verification': checks,
        'scope': {
            'computed': 'common weighted three-way partition and post-recovery residue under a declared no-fold return gate',
            'not_yet_computed': ['physical fold metric', 'particle masses/charges from prime combinations', 'zeta-zero phase filter', 'gravity/energy readout for these candidate states'],
            'cosmological_energy_identification': 'needs the same physical energy map; arithmetic weight share alone does not establish this identification',
            'frozen_core_and_downstream': 'unchanged',
        },
    }
    assert checks['all_passed'], checks
    (ROOT / 'results_26_8.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'scan_case': nearest, 'calibration': result['calibration'], 'joint_output': baseline, 'verification': checks}, indent=2))


if __name__ == '__main__':
    main()
