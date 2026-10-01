#!/usr/bin/env python3
"""WRRA M zeta-zero admission and two-stage residue calculation v0.1.

The zero values are mathematical inputs. The drive, sigmoid gate, sector
assignment and recovery time are explicit model choices. Fractions are
normalized arithmetic weights; their physical readout remains in v1.0.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.optimize import brentq
from scipy.special import bernoulli, expit

ROOT = Path(__file__).resolve().parent
N = 1_000_000
K = 8
J = 4
XI = .1


def prime_mask(limit):
    a = np.ones(limit + 1, dtype=bool)
    a[:2] = False
    for p in range(2, math.isqrt(limit) + 1):
        if a[p]:
            a[p*p::p] = False
    return a


def prime_power_mask(limit, primes):
    a = np.zeros(limit + 1, dtype=bool)
    for p in np.flatnonzero(primes[:math.isqrt(limit)+1]):
        power = int(p)**2
        while power <= limit:
            a[power] = True
            power *= int(p)
    return a


def zeta_euler_maclaurin(s, cutoff=64, terms=12):
    """Independent double-precision check with Euler--Maclaurin tail.

    See DLMF 25.11(iii); zeta(s) = sum_{n<cutoff} n^-s plus the tail
    starting at cutoff. This finite expansion is used for numerical
    cross-checking, not for a rigorous interval certificate.
    """
    z = np.exp(-s * np.log(np.arange(1, cutoff, dtype=float))).sum()
    z += cutoff**(1-s)/(s-1) + .5*cutoff**(-s)
    bs = bernoulli(2*terms)
    rising = complex(s)
    for r in range(1, terms+1):
        if r > 1:
            rising *= (s+2*r-3)*(s+2*r-2)
        z += bs[2*r]/math.factorial(2*r)*rising*cutoff**(-s-2*r+1)
    return z


def zeros_and_validation(count=8):
    with mp.workdps(40):
        low = [mp.zetazero(i) for i in range(1, count+1)]
        low_text = [mp.nstr(z.imag, 38) for z in low]
    rows = []
    with mp.workdps(60):
        high = [mp.zetazero(i) for i in range(1, count+1)]
        for i, (text, z) in enumerate(zip(low_text, high), 1):
            gamma = float(z.imag)
            em64 = zeta_euler_maclaurin(.5+1j*gamma, 64)
            em96 = zeta_euler_maclaurin(.5+1j*gamma, 96)
            rows.append({
                'index': i, 'gamma_decimal_38_digits': text,
                'gamma_used_double': gamma,
                'abs_zeta_at_60_digit_zero': str(abs(mp.zeta(z))),
                'abs_40_60_digit_gamma_difference': str(abs(mp.mpf(text)-z.imag)),
                'abs_Euler_Maclaurin_zeta_double': float(abs(em64)),
                'abs_Euler_Maclaurin_cutoff_difference': float(abs(em64-em96)),
            })
    return np.array([r['gamma_used_double'] for r in rows]), rows


def drive(logn, gamma, frames, xi):
    # gamma log(n) uses the phase of n^(-s); the cosine superposition and
    # equal coefficients are the present WRRA trial rule.
    return np.array([np.cos(gamma[:, None]*(logn[None, :]+xi*k)).sum(axis=0)
                     / math.sqrt(len(gamma)) for k in range(frames)])


def cumulative(deltas, threshold):
    # Product survival is evaluated stably; this is NOT sum of attempts.
    return -np.expm1(-np.logaddexp(0, deltas-threshold).sum(axis=0))


def fit_threshold(deltas, weights, target=.05):
    return float(brentq(lambda h: float(weights@cumulative(deltas, h))-target,
                       -20, 20, xtol=1e-12))


def fractions(deltas, threshold, weights, dark, prime):
    t = cumulative(deltas, threshold)
    matter = float(weights@t)
    return {'phenotype': matter, 'nonphenotypic_Actual': dark,
            'Actual': dark+matter, 'return': prime+float(weights@(1-t)),
            'weighted_effective_beta': matter/float(weights.sum())}


def main(output=ROOT/'results.json'):
    primes_full = prime_mask(N)
    n = np.arange(2, N+1, dtype=np.int64)
    primes = primes_full[2:]
    even = (~primes) & (n%2 == 0)
    odd = (~primes) & (n%2 == 1)
    logn = np.log(n)

    def weights(alpha):
        w = np.exp(-alpha*logn)
        return w/w.sum()

    alpha = float(brentq(lambda a: float(weights(a)[even].sum())-.268,
                        1.8, 2, xtol=1e-12))
    w = weights(alpha)
    dark = float(w[even].sum())
    prime = float(w[primes].sum())
    odd_n, odd_w, odd_log = n[odd], w[odd], logn[odd]
    gamma, zero_rows = zeros_and_validation()
    deltas = drive(odd_log, gamma[:J], K, XI)
    h = fit_threshold(deltas, odd_w)
    t = cumulative(deltas, h)
    terminal = fractions(deltas, h, odd_w, dark, prime)

    # Exact expected-weight transport. No Monte Carlo sampling is performed.
    remaining = odd_w.copy()
    rows = []
    matter = 0.
    for k in range(K):
        admission = expit(deltas[k]-h)
        born = remaining*admission
        remaining *= 1-admission
        matter += float(born.sum())
        reservoir = prime+float(remaining.sum())
        rows.append({'frame': k, 'new_phenotype': float(born.sum()),
                     'phenotype': matter, 'nonphenotypic_Actual': dark,
                     'SOURCE_reservoir': reservoir, 'returned': 0.,
                     'ledger_sum': matter+dark+reservoir,
                     'phase': 'initial_admission'})
    address_completeness = float(np.max(np.abs(t+remaining/odd_w-1)))
    naive_sum = float(odd_w@expit(deltas-h).sum(axis=0))
    for frame in (K, K+1, K+8, K+64, K+1024):
        rows.append({'frame': frame, 'new_phenotype': 0.,
                     'phenotype': matter, 'nonphenotypic_Actual': dark,
                     'SOURCE_reservoir': 0., 'returned': prime+float(remaining.sum()),
                     'ledger_sum': matter+dark+prime+float(remaining.sum()),
                     'phase': 'normalized_return_gate'})

    samples = []
    powers = prime_power_mask(N, primes_full)[2:][odd]
    for addr in (9,15,21,25,27,33,35,49,77,91,119,121,133,143,161):
        pos = int(np.searchsorted(odd_n, addr))
        assert odd_n[pos] == addr
        samples.append({'address': addr, 'prime_power': bool(powers[pos]),
                        'initial_admission_by_frame': expit(deltas[:,pos]-h).tolist(),
                        'cumulative_admission': float(t[pos]),
                        'weight_fraction': float(odd_w[pos]),
                        'residual_weight_fraction': float(odd_w[pos]*t[pos])})

    families = []
    available = np.ones(len(odd_n), dtype=bool)
    for p in np.flatnonzero(primes_full[3:math.isqrt(N)+1])+3:
        family = available & (odd_n%p == 0)
        if family.any():
            families.append({'smallest_prime_factor': int(p),
                             'raw_weight_fraction': float(odd_w[family].sum()),
                             'residual_weight_fraction': float((odd_w[family]*t[family]).sum()),
                             'effective_admission': float(odd_w[family]@t[family]/odd_w[family].sum())})
            available[family] = False

    variants = []
    for name, j, frames, xi in [('recovery_after_4_frames',4,4,.1),
                               ('recovery_after_16_frames',4,16,.1),
                               ('phase_step_005',4,8,.05),
                               ('phase_step_020',4,8,.2),
                               ('one_zero',1,8,.1),('two_zeros',2,8,.1),
                               ('eight_zeros',8,8,.1),('static_phase',4,8,0)]:
        d = drive(odd_log, gamma[:j], frames, xi)
        variants.append({'case':name,'J':j,'K':frames,'xi':xi,
                         'threshold':h,'threshold_refitted':False,
                         **fractions(d,h,odd_w,dark,prime)})
    d0 = np.zeros_like(deltas)
    variants.append({'case':'zero_drive','J':0,'K':K,'xi':None,
                     'threshold':h,'threshold_refitted':False,
                     **fractions(d0,h,odd_w,dark,prime)})
    for dh in (-.1,.1):
        variants.append({'case':f'threshold_shift_{dh:+.1f}','J':J,'K':K,'xi':XI,
                         'threshold':h+dh,'threshold_refitted':False,
                         **fractions(deltas,h+dh,odd_w,dark,prime)})

    # Equal aggregate fractions leave measurable address-level freedom.
    identifiability = []
    for name, frequencies, xi in [('static_zeta_phase',gamma[:J],0.),
                                 ('equally_spaced_control',np.array([14.,21.,28.,35.]),XI)]:
        d = drive(odd_log,frequencies,K,xi)
        hh = fit_threshold(d,odd_w)
        tt = cumulative(d,hh)
        identifiability.append({'case':name,'frequencies':frequencies.tolist(),
                                'xi':xi,'threshold_refitted_to_5_percent':hh,
                                **fractions(d,hh,odd_w,dark,prime),
                                'weighted_address_admission_absolute_difference':
                                    float(odd_w@np.abs(tt-t)/odd_w.sum()),
                                'address_9_cumulative_admission':float(tt[np.searchsorted(odd_n,9)])})

    n_sensitivity=[]
    # Retain alpha and h, renormalize each finite universe; no refitting.
    for limit in (10_000,100_000,N):
        sel = n<=limit
        denominator = np.exp(-alpha*logn[sel]).sum()
        scale = float(np.exp(-alpha*logn).sum()/denominator)
        odd_sel = odd_n<=limit
        m = float((odd_w[odd_sel]*t[odd_sel]).sum()*scale)
        dd = float(w[even & sel].sum()*scale)
        n_sensitivity.append({'N':limit,'phenotype':m,'nonphenotypic_Actual':dd,
                              'Actual':m+dd,'return':1-m-dd})

    # Stress case: each return event leaks fraction epsilon of remaining
    # resident probability. epsilon is NOT a fitted cosmological constant.
    leak_rows=[]
    for eps in (0.,1e-8,1e-6,1e-4):
        for events in (1,1000,1_000_000):
            survival = float(np.exp(events*np.log1p(-eps)))
            leak_rows.append({'return_event_count':events,'epsilon_probability':eps,
                              'residue_survival_fraction':survival,
                              'Actual':terminal['Actual']*survival,
                              'return':1-terminal['Actual']*survival})
    leakage_bound = float(-np.expm1(np.log1p(-.01)/1_000_000))
    checks={
        'zero_dps_comparison_below_1e_36':all(float(r['abs_40_60_digit_gamma_difference'])<1e-36 for r in zero_rows),
        'high_precision_zeta_residual_below_1e_55':all(float(r['abs_zeta_at_60_digit_zero'])<1e-55 for r in zero_rows),
        'independent_Euler_Maclaurin_residual_below_1e_11':all(r['abs_Euler_Maclaurin_zeta_double']<1e-11 for r in zero_rows),
        'matter_target_within_1e_10':abs(terminal['phenotype']-.05)<1e-10,
        'dark_target_within_1e_10':abs(dark-.268)<1e-10,
        'sequential_and_product_results_agree':abs(matter-terminal['phenotype'])<1e-12,
        'each_address_admission_survival_complete':address_completeness<1e-12,
        'each_frame_weight_ledger_complete':all(abs(r['ledger_sum']-1)<1e-12 for r in rows),
        'first_stage_effects_are_probabilities':bool(np.all((t>=0)&(t<=1))),
        'odd_prime_families_exhaust_support':bool(not available.any()),
        'prime_family_residue_partition':abs(sum(r['residual_weight_fraction'] for r in families)-matter)<1e-12,
        'early_recovery_reduces_residue':variants[0]['phenotype']<matter,
        'late_recovery_increases_residue':variants[1]['phenotype']>matter,
        'zero_leakage_recovers_blocked_residue':all(abs(r['Actual']-terminal['Actual'])<1e-12 for r in leak_rows if r['epsilon_probability']==0),
    }
    checks['all_passed']=all(checks.values())
    result={
        'title':'WRRA M zeta-zero frame admission and normalized residue v0.1',
        'author':'Wonsik Choi','date':'2026-10-01',
        'inputs':{'N':N,'J':J,'K':K,'xi':XI,'phase_offsets':'all zero',
                  'drive_coefficients':'equal 1/sqrt(J)',
                  'verified_mathematical_inputs':'low positive zeta zeros computed with mpmath and independently checked with Euler--Maclaurin',
                  'targets_used_for_calibration':{'nonphenotypic_Actual':.268,'phenotype':.05}},
        'calibration':{'alpha':alpha,'sigmoid_threshold_h':h,
                       'constant_beta_supplied_as_input':False,
                       'fitting_rule':'alpha to even-composite 26.8%, h to odd-composite admitted 5%; K,J,xi fixed before h fit'},
        'rules':{
            'weights':'n^-alpha / sum_{m=2..N} m^-alpha',
            'drive':'delta_n(k)=sum_{j=1..J} cos(gamma_j*(log(n)+xi*k))/sqrt(J)',
            'odd_admission':'a_n(k)=sigmoid(delta_n(k)-h), only 0<=k<K',
            'birth':'b_n(k)=s_n(k)*a_n(k); s_n(k+1)=s_n(k)*(1-a_n(k))',
            'cumulative':'T_n(K)=1-product_{k=0..K-1}(1-a_n(k))',
            'even_composites':'all admitted at frame 0, assigned nonphenotypic Actual as in v1.0',
            'primes':'stay in SOURCE until release at normalized recovery',
            'second_filter':'prime no-fold proxy passes; admitted composites lie in blocked kernel; no new admission after frame K',
            'post_recovery':'resident identity evolution preserves folds and the two readout sectors; reservoir returned at K',
            'WRRA_prime_like_composite':'incomplete-readout composite, not Fermat pseudoprime',
            'method':'deterministic expectation-weight transport, not individual stochastic histories',
            'time':'dimensionless frame index; xi not seconds; no inferred Planck clock'},
        'zeta_zero_validation':zero_rows,'terminal':terminal,'frames':rows,
        'address_samples':samples,'smallest_prime_family_residue':families,
        'prime_power_residue_fraction':float((odd_w[powers]*t[powers]).sum()),
        'non_prime_power_residue_fraction':float((odd_w[~powers]*t[~powers]).sum()),
        'naive_attempt_sum_without_reservoir_depletion':naive_sum,
        'per_address_completeness_max_error':address_completeness,
        'frozen_threshold_sensitivity':variants,
        'same_aggregate_different_address_controls':identifiability,
        'fixed_parameter_cutoff_sensitivity':n_sensitivity,
        'return_leakage_stress':leak_rows,
        'retention_condition':{'formula':'(1-epsilon)^L >= 1-delta',
                               'delta':.01,'L':1_000_000,
                               'epsilon_max':leakage_bound,
                               'physical_time_assigned':False},
        'verification':checks,
        'falsification_conditions':[
            'negative admission/return weights or failure of a common per-frame ledger',
            'independent zero recomputation or normalization convergence fails tolerance',
            'a proposed normal return/internal evolution maps preserved folds outside the blocked subspace at a rate inconsistent with the chosen retention horizon',
            'a future shared physical readout maps these address weights to incompatible energy fractions or particle responses under frozen calibrated parameters'],
        'scope':'phase-resolved extension of the calibrated arithmetic partition; physical energy, gravity and particle readout are the continuing WRRA tasks',
        'sources':[
            'https://dlmf.nist.gov/25.10',
            'https://dlmf.nist.gov/25.11.iii',
            'https://mpmath.readthedocs.io/en/latest/functions/zeta.html'],
        'runtime':{'numpy':np.__version__,'mpmath':mp.__version__},
    }
    assert checks['all_passed'], checks
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'calibration':result['calibration'],'terminal':terminal,
                      'verification':checks,'variants':variants,
                      'address_9':samples[0],
                      'leakage_bound':leakage_bound},ensure_ascii=False,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,default=ROOT/'results.json')
    main(p.parse_args().output)
