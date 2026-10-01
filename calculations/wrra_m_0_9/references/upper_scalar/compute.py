#!/usr/bin/env python3
"""Finite WRRA upstream residue pilot, 2026-10-01.

This is an arithmetic filter experiment. A surviving address is a candidate
for residue, not proof of irreversible physical trapping or a particle.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq


def prime_mask(limit):
    mask = np.ones(limit + 1, dtype=bool)
    mask[:2] = False
    for p in range(2, math.isqrt(limit) + 1):
        if mask[p]:
            mask[p * p::p] = False
    return mask


def prime_power_mask(limit, prime):
    mask = np.zeros(limit + 1, dtype=bool)
    for p in np.flatnonzero(prime[:math.isqrt(limit) + 1]):
        q = int(p) ** 2
        while q <= limit:
            mask[q] = True
            q *= int(p)
    return mask


def weighted_row(N, p, alive, powers, alpha):
    n = np.arange(2, N + 1, dtype=float)
    weight = n ** (-alpha)
    selected = alive[2:N + 1]
    echoes = selected & powers[2:N + 1]
    denom = float(weight.sum())
    value = float(weight[selected].sum() / denom)
    echo = float(weight[echoes].sum() / denom)
    return {
        'N': N, 'last_prime': p, 'alpha': alpha,
        'normalization': 'all integer addresses 2..N, weights n**(-alpha)',
        'residual_count': int(selected.sum()),
        'residual_weight_fraction': value,
        'prime_power_weight_fraction': echo,
        'distinct_source_composite_weight_fraction': value - echo,
    }


def run(limit):
    if limit < 10000:
        raise ValueError('Use max-N >= 10000 for this pilot.')
    prime = prime_mask(limit)
    powers = prime_power_mask(limit, prime)
    bases = np.flatnonzero(prime[:math.isqrt(limit) + 1])
    Ns = sorted(set([161, 210, 1000, 2310, 10000, limit]))
    alphas = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
    alive = ~prime
    alive[:2] = False
    all_rows = []
    exact_windows = []
    fixed_gate_sensitivity = []
    indices = np.arange(limit + 1, dtype=np.int64)
    previous_counts = {N: int(alive[:N + 1].sum()) for N in Ns}
    monotone = True
    for p_ in bases:
        p = int(p_)
        alive[p::p] = False
        for N in Ns:
            if p > math.isqrt(N):
                continue
            count = int(alive[:N + 1].sum())
            monotone &= count <= previous_counts[N]
            previous_counts[N] = count
            for alpha in alphas:
                all_rows.append(weighted_row(N, p, alive, powers, alpha))
        if p <= 97:
            counts = np.cumsum(alive, dtype=np.int64)
            hits = np.flatnonzero((indices >= 100) & (20 * counts == indices - 1))
            if len(hits):
                exact_windows.append({
                    'last_prime': p, 'N': int(hits[0]),
                    'residual_count': int(counts[hits[0]]),
                    'fraction': 0.05,
                    'number_of_exact_windows_in_scan': int(len(hits)),
                    'selection': 'post-selected by a declared 5% target scan',
                })
        if p == 5:
            example = np.flatnonzero(alive[:162]).tolist()
            for N in (121, 141, 161, 181, 201, 321, 1000):
                fixed_gate_sensitivity.append(weighted_row(N, p, alive, powers, 0.0))

    assert not alive.any()
    nearest = []
    for N in Ns:
        for alpha in alphas:
            rows = [r for r in all_rows if r['N'] == N and r['alpha'] == alpha]
            nearest.append(min(rows, key=lambda r: abs(r['residual_weight_fraction'] - .05)))

    odd_composites = ~prime
    odd_composites[:2] = False
    odd_composites[2::2] = False
    n = np.arange(2, limit + 1, dtype=float)
    logn = np.log(n)
    odd_mask = odd_composites[2:]

    def residue(alpha):
        w = np.exp(-alpha * logn)
        return float(w[odd_mask].sum() / w.sum())

    calibrated = []
    for target in (.05, .0493):
        alpha = float(brentq(lambda x: residue(x) - target, 1.5, 2.5, xtol=1e-12))
        calibrated.append({
            'N': limit, 'last_prime': 2, 'target_fraction': target,
            'calibrated_alpha': alpha, 'output_fraction': residue(alpha),
            'status': 'target-calibrated weight exponent; not derived from particle constants',
        })

    convergence = [weighted_row(N, 2, odd_composites, powers, 2.0)
                   for N in (161, 1000, 10000, 100000, limit) if N <= limit]
    checks = verify(prime, example, monotone, limit)
    checks['full_filter_cascade_removes_all_composites'] = not bool(alive.any())
    checks['calibration_max_error'] = max(abs(c['output_fraction'] - c['target_fraction']) for c in calibrated)
    checks['all_passed'] = all(v for k, v in checks.items() if isinstance(v, bool)) and checks['calibration_max_error'] < 1e-10

    result = {
        'title': 'WRRA upstream composite-residue finite pilot',
        'date': '2026-10-01', 'author': 'Wonsik Choi',
        'source_code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'inputs': {
            'max_N': limit, 'alpha_values': alphas,
            'address_1': 'excluded as the identity/vacuum placeholder in this pilot',
            'source_vs_relation': 'prime addresses are counted as SOURCE, composites as RELATION',
            'filter_order': 'ascending primes',
            'filter_rule': 'H_p(n)=1 if p does not divide n, else 0',
            'residue_rule': 'composite n and product(H_p(n))=1',
            'weight_rule': 'n**(-alpha)=product(p**(-alpha*valuation_p(n)))',
            'pseudoprime_usage': 'WRRA relation-residue candidate, not Fermat pseudoprime',
        },
        'stage_rows': all_rows,
        'nearest_5_percent_for_each_configuration': nearest,
        'exact_uniform_5_percent_windows': exact_windows,
        'N161_P5_residue_addresses': example,
        'fixed_P5_range_sensitivity': fixed_gate_sensitivity,
        'alpha2_P2_range_sensitivity': convergence,
        'target_calibration': calibrated,
        'verification': checks,
        'physical_connection_status': {
            'particle_constants': 'not yet used to determine N, stopping prime, or alpha',
            'zeta_zeros': 'not yet used; this pilot uses only denominator weights',
            'physical_irreversibility': 'not established; additional prime filters remove current residue',
            'phenotype': 'residue candidate only; stability and particle readout remain to be specified',
            'cosmological_energy_share': 'not identified with address-weight share without an energy map',
            'dark_matter_Actual_branch': 'deferred by user instruction to focus on the 5% branch',
        },
        'primary_math_reference': 'https://dlmf.nist.gov/27.4',
        'wrra_filter_reference': 'https://github.com/Wonsik-Choi-janefather/wrra-modular-optical-comb-prime-sieve',
        'interpretation': 'Conditional arithmetic results and calibrated candidate filters; no unique universe or physical-prime origin claim.',
    }
    return result


def verify(prime, example, monotone, limit):
    trial_prime = lambda n: all(n % d for d in range(2, math.isqrt(n) + 1))
    exact_prime = all(bool(prime[n]) == trial_prime(n) for n in range(2, 232))
    expected = [n for n in range(2, 162)
                if not trial_prime(n) and all(n % p for p in (2, 3, 5))]
    dft_error = 0.0
    for p in (2, 3, 5, 7, 11):
        for n in range(2, 232):
            h = 1 - np.exp(2j * np.pi * np.arange(p) * n / p).mean()
            dft_error = max(dft_error, abs(h - int(n % p != 0)))
    weight_error = 0.0
    for n in (49, 77, 91, 119, 121, 133, 143, 161):
        remaining = n
        factors = []
        d = 2
        while d * d <= remaining:
            while remaining % d == 0:
                factors.append(d); remaining //= d
            d += 1
        if remaining > 1:
            factors.append(remaining)
        for alpha in (.5, 1., 1.5, 2., 3.):
            weight_error = max(weight_error, abs(n ** (-alpha) - math.prod(p ** (-alpha) for p in factors)))
    return {
        'prime_classification_matches_independent_trial_division': exact_prime,
        'N161_residue_matches_independent_trial_division': example == expected,
        'N161_P5_count_is_8_and_fraction_is_5_percent': len(example) == 8 and len(example)/160 == .05,
        'cumulative_residue_is_monotone_under_added_filters': bool(monotone),
        'DFT_filter_matches_modular_selector': bool(dft_error < 1e-10),
        'DFT_filter_max_error': float(dft_error),
        'factor_product_weights_match_integer_weights': bool(weight_error < 1e-12),
        'factor_product_max_error': float(weight_error),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-N', type=int, default=1_000_000)
    parser.add_argument('--out', default=str(Path(__file__).with_name('results.json')))
    args = parser.parse_args()
    result = run(args.max_N)
    Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({
        'alpha2_P2': result['alpha2_P2_range_sensitivity'][-1],
        'calibrated_exponents': result['target_calibration'],
        'verification': result['verification'],
    }, indent=2))

