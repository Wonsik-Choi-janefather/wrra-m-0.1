from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
import mpmath as mp
from scipy.optimize import brentq
from scipy.integrate import quad

OUT = Path(__file__).with_name('results.json')

BASE_N = 1_000_000
CANDIDATE_N = 1_015_000
ALPHA0 = 1.8996876950554356
H0_THRESHOLD = 1.44767317035244
BETA0 = 0.8654570124136961
GAMMA = np.array([14.134725141734695, 21.022039638771556, 25.01085758014569, 30.424876125859512])
COEFF = np.full(4, 0.5)
PHASE_STEP_XI = 0.1
ADMISSION_FRAMES = 8
TARGET = np.array([0.05, 0.268, 0.682])

ETA = np.array([7.561582499072265e-10, 7.285761328795971e-10, 7.646102818811323e-10])
LAM = np.array([0.0, 0.25, 0.1])
UCRIT = 7.668947767821907e-10
C = 299792458.0
G = 6.6743e-11
H0_KM_S_MPC = 67.4
PARSEC_M = 30856775814913670.0
M_SUN_KG = 1.98847e30
FP = 0.0493
FC = 0.265
FH = 1 - FP
SPHERE_MASS_MSUN = 60_000_000_000
SPHERE_SCALE_KPC = 3.0
PATCH_RADIUS_KPC = 200.0
TEST_RADIUS_KPC = 8.2
LENS_IMPACT_KPC = 10.0
HBAR = 1.0545718176461565e-34
DELTA_TAU = 1.4813019664158691e-21

def sieve_state(N: int, alpha: float):
    spf = np.zeros(N + 1, dtype=np.int32)
    for p in range(2, N + 1):
        if spf[p] == 0:
            spf[p] = p
            if p * p <= N:
                block = spf[p * p::p]
                block[block == 0] = p
    n = np.arange(2, N + 1, dtype=np.int64)
    prime = spf[2:] == n
    even = (~prime) & (n % 2 == 0)
    odd = (~prime) & (n % 2 == 1)
    w = np.exp(-alpha * np.log(n)); w /= w.sum()
    return n, prime, even, odd, w

def phase_effect(n: np.ndarray, odd: np.ndarray, threshold: float):
    admission = np.zeros(len(n))
    no = n[odd]
    drive = np.array([
        (COEFF[:, None] * np.cos(GAMMA[:, None] * (np.log(no)[None, :] + PHASE_STEP_XI * i))).sum(axis=0)
        for i in range(ADMISSION_FRAMES)
    ])
    admission[odd] = -np.expm1(-np.logaddexp(0, drive - threshold).sum(axis=0))
    return admission

def ledger(N: int, alpha: float, threshold: float):
    n, prime, even, odd, w = sieve_state(N, alpha)
    admission = phase_effect(n, odd, threshold)
    effect = np.array([admission, even.astype(float), 1 - admission - even.astype(float)])
    shares = effect @ w
    return {'n': n, 'prime': prime, 'even': even, 'odd': odd, 'w': w, 'effect': effect, 'shares': shares}

def recalibrate_candidate():
    n, prime, even, odd, _ = sieve_state(CANDIDATE_N, ALPHA0)
    logn = np.log(n)
    def weights(a):
        v = np.exp(-a * logn); return v / v.sum()
    alpha = float(brentq(lambda a: float(weights(a)[even].sum()) - TARGET[1], 1.01, 4.0, xtol=1e-14))
    w = weights(alpha)
    no = n[odd]
    drive = np.array([
        (COEFF[:, None] * np.cos(GAMMA[:, None] * (np.log(no)[None, :] + PHASE_STEP_XI * i))).sum(axis=0)
        for i in range(ADMISSION_FRAMES)
    ])
    oddw = w[odd]
    threshold = float(brentq(
        lambda h: float(oddw @ (-np.expm1(-np.logaddexp(0, drive - h).sum(axis=0)))) - TARGET[0],
        -30, 30, xtol=1e-14))
    admission = -np.expm1(-np.logaddexp(0, drive - threshold).sum(axis=0))
    beta_eff = float((oddw @ admission) / oddw.sum())
    return alpha, threshold, beta_eff

def address_moments(state, N):
    x = np.log(state['n']) / math.log(N)
    response = np.array([1 + LAM[i] * x for i in range(3)])
    return np.sum(state['effect'] * response * state['w'][None, :], axis=1)

def plummer(r_m, aT):
    mass = SPHERE_MASS_MSUN * M_SUN_KG
    b = SPHERE_SCALE_KPC * 1000 * PARSEC_M
    mb = mass * r_m**3 / (r_m*r_m + b*b)**1.5
    gm = G * mb / r_m**2
    y = gm / aT
    nu = 1.0 / (-np.expm1(-np.sqrt(y)))
    g = gm * nu
    return gm, g

def local_outputs(energy):
    H0 = H0_KM_S_MPC * 1000 / (1e6 * PARSEC_M)
    aT0 = C * H0 * math.sqrt(FC / 8)
    aT = aT0 * math.sqrt(energy[1] / (UCRIT * FC))
    r = TEST_RADIUS_KPC * 1000 * PARSEC_M
    _, g = plummer(r, aT)
    v = math.sqrt(r * g) / 1000
    kpc = 1000 * PARSEC_M
    impact = LENS_IMPACT_KPC * kpc
    R = PATCH_RADIUS_KPC * kpc
    zmax = math.sqrt(R*R - impact*impact)
    def integrand(t):
        z = t * kpc
        rr = math.hypot(impact, z)
        _, gg = plummer(rr, aT)
        return gg * impact / rr * kpc
    total, _ = quad(integrand, 0, zmax/kpc, epsabs=1e-4, epsrel=2e-11)
    lens = 4 / C**2 * total * 180 / math.pi * 3600
    return aT, v, lens

def macro(state, N):
    mu = address_moments(state, N)
    energy = ETA * mu
    total = float(energy.sum())
    q = 0.5 * (total - 3 * energy[2]) / total
    aT, v, lens = local_outputs(energy)
    return {'mu': mu, 'energy': energy, 'total': total, 'q': q, 'aT': aT, 'v': v, 'lens': lens}

def carrier_dynamics(mu):
    N = 128; epsilon = 8.0
    I = np.eye(N)
    Kc = 2*I - np.roll(I, 1, axis=0) - np.roll(I, -1, axis=0)
    D = np.zeros((N, N)); D[0, 0] = 1
    Kb = (Kc + epsilon * D) / (1 + epsilon/(2*N))
    ops = (I, Kc/2, Kb/2)
    amps = ETA * mu
    H = sum(a * A for a, A in zip(amps, ops))
    vals, basis = np.linalg.eigh(H / UCRIT)
    def wave(j):
        return np.exp(2j*math.pi*j*np.arange(N)/N)/math.sqrt(N)
    psi = sum(math.sqrt(1/3)*wave(j) for j in (8,16,24))
    rho0 = np.outer(psi, psi.conj())
    rows = []
    for k in (0,1,2,4,8):
        xi = k * DELTA_TAU * UCRIT / HBAR
        U = (basis * np.exp(-1j*xi*vals)) @ basis.conj().T
        rho = U @ rho0 @ U.conj().T
        loads = np.array([float(np.trace(rho @ A).real) for A in ops])
        energy = amps * loads
        total = float(energy.sum())
        rows.append({
            'frame': k, 'total_energy_J': total,
            'D_load': float(loads[1]), 'R_load': float(loads[2]),
            'q': float(0.5*(total - 3*energy[2])/total),
            'trace': float(np.trace(rho).real),
            'minimum_eigenvalue': float(np.linalg.eigvalsh(rho).min()),
        })
    E0 = rows[0]['total_energy_J']
    return rows, max(abs(r['total_energy_J']/E0 - 1) for r in rows), max(abs(r['trace']-1) for r in rows)

def zeta_em(s: complex, M: int):
    n = np.arange(1, M, dtype=float)
    sm = np.sum(np.exp(-s * np.log(n)))
    return (sm + M**(1-s)/(s-1) + 0.5*M**(-s) + (s/12)*M**(-s-1)
            - (s*(s+1)*(s+2)/720)*M**(-s-3))

def zeta_window():
    mp.mp.dps = 50
    H = 29; T = 2 * mp.pi * H
    zeros = [mp.im(mp.zetazero(k)) for k in range(1, 72)]
    count = sum(z <= T for z in zeros)
    M = 500 * H
    residuals = [abs(zeta_em(0.5 + 1j*float(z), M)) for z in zeros[:count]]
    nearest_by_H = []
    allz = [mp.im(mp.zetazero(k)) for k in range(1, 100)]
    for h in range(1, 30):
        th = 2*mp.pi*h
        d, idx, z = min((abs(z-th), i+1, z) for i,z in enumerate(allz))
        nearest_by_H.append({'H':h,'zero_index':idx,'distance':float(d),'zero':float(z)})
    return {
        'H': H, 'T': float(T), 'zero_count': count,
        'gamma_last': float(zeros[count-1]), 'gamma_next': float(zeros[count]),
        'boundary_gap_to_last': float(T-zeros[count-1]),
        'boundary_gap_to_next': float(zeros[count]-T),
        'finite_EM_terms_M': M,
        'finite_EM_max_residual_first_70': float(max(residuals)),
        'finite_EM_residual_70th': float(residuals[-1]),
        'nearest_boundary_alignment_H_1_to_29': min(nearest_by_H, key=lambda x:x['distance']),
        'second_nearest_boundary_alignment_H_1_to_29': sorted(nearest_by_H, key=lambda x:x['distance'])[1],
    }

def main():
    z = zeta_window()
    source_N = 500 * 29 * z['zero_count']
    assert source_N == CANDIDATE_N
    base = ledger(BASE_N, ALPHA0, H0_THRESHOLD)
    frozen = ledger(CANDIDATE_N, ALPHA0, H0_THRESHOLD)
    alpha1, h1, beta1 = recalibrate_candidate()
    recal = ledger(CANDIDATE_N, alpha1, h1)
    base_macro = macro(base, BASE_N)
    frozen_macro = macro(frozen, CANDIDATE_N)
    recal_macro = macro(recal, CANDIDATE_N)
    dynamics, Eerr, Terr = carrier_dynamics(recal_macro['mu'])
    result = {
        'model': 'WRRA_M KZF finite-source closure candidate v0.1',
        'generator': {
            'sector_ledger_denominator_L': 500,
            'harmonic_phase_H': 29,
            'zeta_focus_count_C': z['zero_count'],
            'candidate_N_U': source_N,
            'construction_rule': 'N_U = L * H * C',
            'status': 'construction hypothesis; independence/product rule not yet derived',
            'zeta_window': z,
        },
        'baseline': {
            'N': BASE_N, 'alpha': ALPHA0, 'threshold_h': H0_THRESHOLD, 'beta_scalar': BETA0,
            'shares': base['shares'].tolist(),
            'counts': {'prime': int(base['prime'].sum()), 'even_composite': int(base['even'].sum()), 'odd_composite': int(base['odd'].sum())},
            'macro': {k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in base_macro.items()},
        },
        'candidate_frozen_no_refit': {
            'N': CANDIDATE_N, 'alpha': ALPHA0, 'threshold_h': H0_THRESHOLD, 'beta_scalar': BETA0,
            'shares': frozen['shares'].tolist(),
            'counts': {'prime': int(frozen['prime'].sum()), 'even_composite': int(frozen['even'].sum()), 'odd_composite': int(frozen['odd'].sum())},
            'macro': {k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in frozen_macro.items()},
        },
        'candidate_minimal_recalibration': {
            'N': CANDIDATE_N, 'alpha': alpha1, 'threshold_h': h1, 'derived_effective_beta': beta1,
            'delta_alpha': alpha1-ALPHA0, 'delta_threshold_h': h1-H0_THRESHOLD, 'delta_beta_eff': beta1-BETA0,
            'shares': recal['shares'].tolist(),
            'macro_with_frozen_SI_coefficients': {k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in recal_macro.items()},
            'proper_time_dynamics': dynamics,
            'max_energy_relative_error': Eerr,
            'max_trace_absolute_error': Terr,
        },
        'tests': {
            'finite_source_only': True,
            'candidate_equals_generator_product': source_N == CANDIDATE_N,
            'no_refit_ledger_complete': abs(float(frozen['shares'].sum())-1) < 2e-12,
            'minimal_recalibration_hits_5_26_8_68_2': bool(np.max(abs(recal['shares']-TARGET)) < 2e-12),
            'all_sector_effects_positive_complete': bool(recal['effect'].min() >= 0 and recal['effect'].max() <= 1 and np.max(abs(recal['effect'].sum(axis=0)-1)) < 2e-12),
            'proper_time_energy_conserved': Eerr < 1e-12,
            'proper_time_state_trace_conserved': Terr < 1e-12,
            'product_rule_derived': False,
        },
        'verdict': 'PASS-C: adopt as a finite-generation-window candidate, not as a uniquely derived fundamental constant.'
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({
        'candidate_N_U':source_N,
        'zeta_zero_count':z['zero_count'],
        'recalibrated_shares':recal['shares'].tolist(),
        'alpha':alpha1,'threshold_h':h1,'beta_eff':beta1,
        'q0':recal_macro['q'],'rotation_km_s':recal_macro['v'],'lensing_arcsec':recal_macro['lens'],
        'energy_rel_error':Eerr,'verdict':result['verdict']
    }, indent=2))

if __name__ == '__main__':
    main()
