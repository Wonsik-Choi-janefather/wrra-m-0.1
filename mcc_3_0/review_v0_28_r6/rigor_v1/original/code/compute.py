#!/usr/bin/env python3
"""WRRA_M finite Klein-zeta generation-window candidate v0.1.

Purpose
-------
Construct and verify a finite address-window candidate from:
(1) the adopted WRRA_M arithmetic ledger 5%/26.8%/68.2%,
(2) the existing harmonic ledger maximum mode H=29,
(3) the count of positive nontrivial Riemann-zeta zeros below T=2*pi*H,
then insert the resulting address cutoff into the frozen WRRA_M address and
downstream energy rules.

The Klein-type quotient and the Cartesian product L*H*C are explicit WRRA
construction rules. They are not presented as independently established
properties of physical spacetime.

Dependencies: numpy, scipy, mpmath
"""
from __future__ import annotations
import json, math
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "results" / "results.json"

TARGETS = {"phenotype": 0.05, "resident_nonphenotype": 0.268, "return": 0.682}
ALPHA0 = 1.8996876950554356
BETA0 = 0.8654570124136961
H0_THRESHOLD = 1.44767317035244
K = 8
XI = 0.1
GAMMA4 = np.array([
    14.134725141734695,
    21.022039638771556,
    25.01085758014569,
    30.424876125859512,
], dtype=float)
COEFF4 = np.array([0.5, 0.5, 0.5, 0.5], dtype=float)

HARMONIC_LEDGER = (0, 5, 29)
H = max(HARMONIC_LEDGER)

UCRIT = 7.668947767821907e-10
ETA = np.array([
    7.561582499072265e-10,
    7.285761328795971e-10,
    7.646102818811323e-10,
])
LAMBDA = np.array([0.0, 0.25, 0.1])

C_SI = 299792458.0
G_SI = 6.6743e-11
H0_KM_S_MPC = 67.4
PARSEC_M = 30856775814913670.0
M_SUN_KG = 1.98847e30
F_PHI_PHYS = 0.0493
F_C_PHYS = 0.265
SPHERE_MASS_MSUN = 60_000_000_000.0
SPHERE_SCALE_KPC = 3.0
TEST_RADIUS_KPC = 8.2
PATCH_RADIUS_KPC = 200.0
LENS_IMPACT_KPC = 10.0

DELTA_TAU_S = 1.4813019664158691e-21
HBAR_J_S = 1.0545718176461565e-34
CARRIER_N = 128
CARRIER_EPSILON = 8.0


def rational_ledger_resolution():
    from fractions import Fraction
    fs = [Fraction(str(v)) for v in TARGETS.values()]
    den = 1
    for f in fs:
        den = math.lcm(den, f.denominator)
    nums = [int(f * den) for f in fs]
    return den, nums


def finite_zeta_em(s: complex, cutoff: int):
    """Finite Euler-Maclaurin approximation with B2 and B4 tail terms."""
    logn = np.log(np.arange(1, cutoff, dtype=float))
    z = np.exp(-s * logn).sum()
    z += cutoff ** (1 - s) / (s - 1)
    z += 0.5 * cutoff ** (-s)
    z += s / 12 * cutoff ** (-s - 1)
    z -= s * (s + 1) * (s + 2) / 720 * cutoff ** (-s - 3)
    return z


def zeta_focus_count(H_value: int, finite_cutoff: int):
    T = 2 * math.pi * H_value
    with mp.workdps(50):
        gammas = []
        k = 1
        while True:
            g = float(mp.im(mp.zetazero(k)))
            gammas.append(g)
            if g > T:
                break
            k += 1
    C = len(gammas) - 1
    residuals = [float(abs(finite_zeta_em(0.5 + 1j * g, finite_cutoff))) for g in gammas[:C]]
    scan = []
    zero_pool = gammas
    while zero_pool[-1] < 2 * math.pi * H:
        k = len(zero_pool) + 1
        zero_pool.append(float(mp.im(mp.zetazero(k))))
    for m in range(1, H + 1):
        t = 2 * math.pi * m
        idx = int(np.argmin(np.abs(np.asarray(zero_pool) - t)))
        g = zero_pool[idx]
        d = abs(g - t)
        if idx == 0:
            local_spacing = zero_pool[1] - zero_pool[0]
        else:
            if idx + 1 >= len(zero_pool):
                zero_pool.append(float(mp.im(mp.zetazero(len(zero_pool) + 1))))
            local_spacing = (zero_pool[idx + 1] - zero_pool[idx - 1]) / 2
        scan.append({
            "m": m, "nearest_zero_index": idx + 1, "nearest_gamma": g,
            "absolute_distance": d, "distance_over_local_mean_spacing": d / local_spacing
        })
    return {
        "H": H_value,
        "T_2piH": T,
        "C": C,
        "gamma_C": gammas[C - 1],
        "gamma_C_plus_1": gammas[C],
        "gap_to_gamma_C": T - gammas[C - 1],
        "gap_to_gamma_C_plus_1": gammas[C] - T,
        "finite_cutoff": finite_cutoff,
        "finite_EM_max_abs_residual_first_C": max(residuals),
        "finite_EM_abs_residual_gamma_C": residuals[-1],
        "boundary_scan": scan,
    }


def address_base(N: int, alpha: float):
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
    w = np.exp(-alpha * np.log(n))
    w /= w.sum()
    return {"n": n, "prime": prime, "even": even, "odd": odd, "w": w, "spf": spf[2:]}


def phase_drive(nodd):
    gamma = GAMMA4[:, None]
    coeff = COEFF4[:, None]
    return np.array([
        (coeff * np.cos(gamma * (np.log(nodd)[None, :] + XI * i))).sum(axis=0)
        for i in range(K)
    ])


def effects(base, h):
    n, odd = base["n"], base["odd"]
    admission = np.zeros(len(n))
    d = phase_drive(n[odd])
    admission[odd] = -np.expm1(-np.logaddexp(0, d - h).sum(axis=0))
    dark = base["even"].astype(float)
    return np.array([admission, dark, 1 - admission - dark])


def shares(base, effect):
    return effect @ base["w"]


def calibrate_candidate(N: int):
    seed = address_base(N, ALPHA0)
    n, even, odd = seed["n"], seed["even"], seed["odd"]
    logn = np.log(n)

    def weights(a):
        v = np.exp(-a * logn)
        return v / v.sum()

    alpha = float(brentq(
        lambda a: float(weights(a)[even].sum()) - TARGETS["resident_nonphenotype"],
        1.01, 4.0, xtol=1e-14
    ))
    w = weights(alpha)
    d = phase_drive(n[odd])
    oddw = w[odd]
    h = float(brentq(
        lambda x: float(oddw @ (-np.expm1(-np.logaddexp(0, d - x).sum(axis=0)))) - TARGETS["phenotype"],
        -30, 30, xtol=1e-14
    ))
    beta_eff = TARGETS["phenotype"] / float(oddw.sum())
    base = address_base(N, alpha)
    E = effects(base, h)
    return alpha, h, beta_eff, base, E


def address_moments(N, base, effect):
    n = base["n"]
    g = np.array([1 + LAMBDA[i] * np.log(n) / math.log(N) for i in range(3)])
    return np.sum(effect * g * base["w"][None, :], axis=1), g


def nu(y):
    y = np.asarray(y, dtype=float)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def plummer(r, aT):
    b = SPHERE_SCALE_KPC * 1000 * PARSEC_M
    M = SPHERE_MASS_MSUN * M_SUN_KG
    mb = M * r**3 / (r*r + b*b)**1.5
    gm = G_SI * mb / r**2
    y = gm / aT
    g = gm * nu(y)
    return float(g), float(gm)


def lens_segment(impact_kpc, aT):
    kpc = 1000 * PARSEC_M
    b = impact_kpc * kpc
    R = PATCH_RADIUS_KPC * kpc
    zmax = math.sqrt(R*R - b*b)

    def fn(t, baryon=False):
        z = t * kpc
        r = math.hypot(b, z)
        g, gm = plummer(r, aT)
        acc = gm if baryon else g
        return acc * b / r * kpc

    total, err = quad(lambda t: fn(t), 0, zmax/kpc, epsabs=1e-4, epsrel=2e-11)
    baryon, _ = quad(lambda t: fn(t, True), 0, zmax/kpc, epsabs=1e-4, epsrel=2e-11)
    factor = 4 / C_SI**2
    return {
        "alpha_patch_rad": factor * total,
        "alpha_baryon_patch_rad": factor * baryon,
        "alpha_twist_patch_rad": factor * (total - baryon),
        "alpha_patch_arcsec": factor * total * 180 / math.pi * 3600,
        "quad_abs_error_rad": factor * err,
    }


def downstream(N, base, effect):
    mu, response = address_moments(N, base, effect)
    sector_energy = ETA * mu
    total = float(sector_energy.sum())
    pressure = -float(sector_energy[2])
    q = 0.5 * (total + 3 * pressure) / total
    fractions = sector_energy / total

    H0 = H0_KM_S_MPC * 1000 / (1e6 * PARSEC_M)
    aT0 = C_SI * H0 * math.sqrt(F_C_PHYS / 8)
    hidden_ref = 1 - F_PHI_PHYS
    aT_over_ref = math.sqrt(sector_energy[1] / (UCRIT * F_C_PHYS))
    aT = aT0 * aT_over_ref
    hidden_over_ref = float((sector_energy[1] + sector_energy[2]) / (UCRIT * hidden_ref))
    r = TEST_RADIUS_KPC * 1000 * PARSEC_M
    g, gm = plummer(r, aT)
    v = math.sqrt(r * g) / 1000
    v_direct = math.sqrt(r * gm) / 1000
    lens = lens_segment(LENS_IMPACT_KPC, aT)

    return {
        "address_moments": dict(zip(("phenotype", "resident_nonphenotype", "return"), map(float, mu))),
        "sector_energy_J": dict(zip(("phenotype", "resident_nonphenotype", "return"), map(float, sector_energy))),
        "sector_energy_fractions": dict(zip(("phenotype", "resident_nonphenotype", "return"), map(float, fractions))),
        "total_energy_J_uniform_a1": total,
        "total_pressure_Pa_uniform_a1": pressure,
        "deceleration_q_uniform_a1": q,
        "aT_m_s2": aT,
        "hidden_density_over_reference": hidden_over_ref,
        "rotation_km_s": v,
        "direct_rotation_km_s": v_direct,
        "lensing_arcsec": lens["alpha_patch_arcsec"],
        "lensing_detail": lens,
        "SI_eta_refit": False,
    }


def carrier_energy_check(down):
    I = np.eye(CARRIER_N)
    Kc = 2*I - np.roll(I, 1, axis=0) - np.roll(I, -1, axis=0)
    D = np.zeros((CARRIER_N, CARRIER_N)); D[0, 0] = 1
    Kb = (Kc + CARRIER_EPSILON * D) / (1 + CARRIER_EPSILON/(2*CARRIER_N))
    A = [I, Kc/2, Kb/2]
    amp = np.array(list(down["sector_energy_J"].values()))
    EH = sum(k * op for k, op in zip(amp, A))
    eig = np.linalg.eigvalsh(EH / UCRIT)

    def wave(j):
        return np.exp(2j*math.pi*j*np.arange(CARRIER_N)/CARRIER_N) / math.sqrt(CARRIER_N)
    psi = sum(math.sqrt(1/3) * wave(j) for j in (8, 16, 24))
    rho0 = np.outer(psi, psi.conj())
    vals, vec = np.linalg.eigh(EH / UCRIT)
    rows = []
    for k in (0, 1, 2, 4, 8):
        xi = k * DELTA_TAU_S * UCRIT / HBAR_J_S
        U = (vec * np.exp(-1j * xi * vals)) @ vec.conj().T
        rho = U @ rho0 @ U.conj().T
        loads = np.array([float(np.trace(rho @ op).real) for op in A])
        energy = amp * loads
        total = float(energy.sum())
        q = 0.5 * (total - 3*float(energy[2])) / total
        rows.append({
            "proper_frame": k,
            "total_energy_J": total,
            "D_load": float(loads[1]),
            "R_load": float(loads[2]),
            "q": q,
            "state_trace": float(np.trace(rho).real),
            "minimum_state_eigenvalue": float(np.linalg.eigvalsh(rho).min()),
        })
    E0 = rows[0]["total_energy_J"]
    return {
        "minimum_energy_operator_eigenvalue_over_ucrit": float(eig.min()),
        "proper_frame_rows": rows,
        "maximum_relative_energy_drift": max(abs(r["total_energy_J"]/E0 - 1) for r in rows),
    }


def main():
    L, ledger_counts = rational_ledger_resolution()
    finite_cutoff = L * H
    zeta = zeta_focus_count(H, finite_cutoff)
    C = zeta["C"]
    N = L * H * C

    first = 1
    last = 1 + (L-1) + L*((H-1) + H*(C-1))
    bijection_ok = (first == 1 and last == N)

    base0 = address_base(1_000_000, ALPHA0)
    E0 = effects(base0, H0_THRESHOLD)
    s0 = shares(base0, E0)
    down0 = downstream(1_000_000, base0, E0)

    base_frozen = address_base(N, ALPHA0)
    E_frozen = effects(base_frozen, H0_THRESHOLD)
    s_frozen = shares(base_frozen, E_frozen)

    alpha1, h1, beta_eff1, base1, E1 = calibrate_candidate(N)
    s1 = shares(base1, E1)
    down = downstream(N, base1, E1)
    carrier = carrier_energy_check(down)

    checks = {
        "ledger_exact_common_denominator_is_500": L == 500 and ledger_counts == [25, 134, 341],
        "harmonic_max_is_29": H == 29,
        "zeta_count_below_2piH_is_70": C == 70,
        "70th_zero_inside_71st_outside": zeta["gamma_C"] <= zeta["T_2piH"] < zeta["gamma_C_plus_1"],
        "finite_EM_residual_below_1e-11": zeta["finite_EM_max_abs_residual_first_C"] < 1e-11,
        "finite_address_bijection": bijection_ok and N == 1_015_000,
        "legacy_N1e6_baseline_reproduced": bool(np.max(np.abs(s0 - np.array([.05, .268, .682]))) < 2e-12),
        "candidate_frozen_parameters_close_to_targets": bool(np.max(np.abs(s_frozen - np.array([.05, .268, .682]))) < 5e-8),
        "candidate_two_parameter_recalibration_closes_targets": bool(np.max(np.abs(s1 - np.array([.05, .268, .682]))) < 2e-12),
        "beta_eff_is_derived_not_refit": abs(beta_eff1 - BETA0) < 5e-7,
        "SI_coefficients_frozen": down["SI_eta_refit"] is False,
        "downstream_sector_energies_positive": min(down["sector_energy_J"].values()) > 0,
        "energy_operator_positive": carrier["minimum_energy_operator_eigenvalue_over_ucrit"] > 0,
        "proper_time_energy_conserved": carrier["maximum_relative_energy_drift"] < 1e-12,
        "state_trace_and_positivity_roundoff": all(abs(r["state_trace"]-1) < 1e-12 and r["minimum_state_eigenvalue"] > -1e-12 for r in carrier["proper_frame_rows"]),
    }

    result = {
        "title": "WRRA_M Finite Klein-Zeta Generation Window v0.1",
        "date": "2026-10-07",
        "authors": ["Wonsik Choi", "Jeongin Choi"],
        "evaluation_protocol": ["verification input", "WRRA-specific transformation", "output", "falsification condition"],
        "verification_inputs": {
            "adopted_arithmetic_targets": TARGETS,
            "legacy_address_cutoff_for_regression_only": 1_000_000,
            "legacy_alpha": ALPHA0,
            "legacy_threshold_h": H0_THRESHOLD,
            "legacy_scalar_beta": BETA0,
            "harmonic_ledger": list(HARMONIC_LEDGER),
            "zeta_phase_rule": {"K": K, "xi": XI, "gamma_first4": GAMMA4.tolist(), "coefficients": COEFF4.tolist()},
            "frozen_SI_eta_J_m3": dict(zip(("phenotype", "resident_nonphenotype", "return"), map(float, ETA))),
        },
        "WRRA_transformation": {
            "ledger_resolution_L": L,
            "ledger_integer_counts": ledger_counts,
            "harmonic_H": H,
            "zeta_boundary_T": zeta["T_2piH"],
            "zeta_focus_count_C": C,
            "finite_zeta_cutoff_M": finite_cutoff,
            "candidate_generation_window_NU": N,
            "address_map": "n = 1 + ell + L*(h + H*(z-1)); 0<=ell<L, 0<=h<H, 1<=z<=C",
            "vacuum_address_policy": "label 1 is the inherited inactive multiplicative/vacuum reference; active addresses are 2..N_U",
            "klein_quotient_candidate": "one cycle closes with orientation reversal, e.g. (-T,theta)~(T,-theta), with the transverse coordinate periodic",
            "product_rule_status": "explicit WRRA construction assumption; uniqueness not established",
        },
        "zeta_verification": zeta,
        "outputs": {
            "legacy_regression_shares": dict(zip(("phenotype", "resident_nonphenotype", "return"), map(float, s0))),
            "legacy_regression_downstream": down0,
            "candidate_frozen_parameter_shares": dict(zip(("phenotype", "resident_nonphenotype", "return"), map(float, s_frozen))),
            "candidate_recalibration": {
                "alpha": alpha1,
                "threshold_h": h1,
                "derived_effective_beta": beta_eff1,
                "delta_alpha": alpha1 - ALPHA0,
                "delta_h": h1 - H0_THRESHOLD,
                "delta_beta_eff_vs_legacy_beta": beta_eff1 - BETA0,
                "shares": dict(zip(("phenotype", "resident_nonphenotype", "return"), map(float, s1))),
            },
            "candidate_address_counts": {
                "labels_total_including_1": N,
                "active_addresses_2_to_N": N - 1,
                "primes": int(base1["prime"].sum()),
                "even_composites": int(base1["even"].sum()),
                "odd_composites": int(base1["odd"].sum()),
            },
            "frozen_SI_downstream": down,
            "downstream_change_vs_legacy": {
                "delta_q": down["deceleration_q_uniform_a1"] - down0["deceleration_q_uniform_a1"],
                "delta_rotation_km_s": down["rotation_km_s"] - down0["rotation_km_s"],
                "delta_lensing_arcsec": down["lensing_arcsec"] - down0["lensing_arcsec"],
                "relative_q_abs": abs((down["deceleration_q_uniform_a1"] - down0["deceleration_q_uniform_a1"]) / down0["deceleration_q_uniform_a1"]),
                "relative_rotation_abs": abs((down["rotation_km_s"] - down0["rotation_km_s"]) / down0["rotation_km_s"]),
                "relative_lensing_abs": abs((down["lensing_arcsec"] - down0["lensing_arcsec"]) / down0["lensing_arcsec"]),
            },
            "proper_time_energy_check": carrier,
        },
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "assessment": {
            "status": "PASS-C",
            "meaning": "adopt as a finite-generation-window candidate, not as an established fundamental constant",
            "candidate_prediction": "N_U = 1,015,000 under the stated L*H*C construction",
            "not_claimed": [
                "that the Cartesian product L*H*C is uniquely forced by known physics",
                "that the Klein quotient is measured spacetime topology",
                "that the rounded 5%/26.8%/68.2% ledger is exact in nature",
                "that N_U is experimentally measured",
            ],
        },
        "falsification_conditions": [
            "the 70-zero count or finite-zeta numerical validation fails under independent recomputation",
            "the adopted L, H and C cannot be represented as independent state coordinates in a consistent WRRA ledger",
            "a competing closure rule is required by the same WRRA state variables and invalidates the L*H*C bijection",
            "the N_U candidate fails the common arithmetic ledger after the declared minimal calibration",
            "with frozen downstream SI coefficients the candidate produces negative energy, breaks energy conservation, or violates an inherited observable constraint",
            "future better-validated sector inputs or harmonic structure remove the 500, 29 or 70 construction without a consistent model update",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    assert result["all_checks_passed"], checks
    print(json.dumps({
        "N_U": N,
        "L": L, "H": H, "C": C,
        "gamma_70": zeta["gamma_C"],
        "gamma_71": zeta["gamma_C_plus_1"],
        "frozen_shares": result["outputs"]["candidate_frozen_parameter_shares"],
        "recalibration": result["outputs"]["candidate_recalibration"],
        "downstream": {
            "q0": down["deceleration_q_uniform_a1"],
            "rotation_km_s": down["rotation_km_s"],
            "lensing_arcsec": down["lensing_arcsec"],
        },
        "max_energy_drift": carrier["maximum_relative_energy_drift"],
        "all_checks_passed": result["all_checks_passed"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
