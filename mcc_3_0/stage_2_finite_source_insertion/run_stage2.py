#!/usr/bin/env python3
"""MCC 3.0 Stage 2 — finite SOURCE insertion.

This script keeps the historical WRRA_M 0.9 configuration untouched,
generates N_U from the KZF module, and creates a separate MCC 3.0
candidate branch using the same address-filter implementation.

Run from repository root:
    python mcc_3_0/stage_2_finite_source_insertion/run_stage2.py
"""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

m09 = load_module("mcc3_wrra09", REPO / "calculations" / "wrra_m_0_9" / "compute.py")
kzf = load_module("mcc3_kzf", REPO / "upstream" / "finite_klein_zeta_window_v0_1" / "code" / "compute.py")

stage1 = json.loads((REPO / "mcc_3_0" / "stage_1_baseline_freeze" / "baseline_manifest.json").read_text())
legacy_cfg = json.loads((REPO / "calculations" / "wrra_m_0_9" / "parameters.json").read_text())
published_kzf = json.loads((REPO / "upstream" / "finite_klein_zeta_window_v0_1" / "results" / "results.json").read_text())

LOCK = "MCC3-S1-21daec11-43b998ca-f667bbdf"
TARGET = np.array([0.05, 0.268, 0.682], dtype=float)
SECTORS = ("phenotype", "resident_nonphenotype", "return")

def summarize(cfg):
    base = m09.address_base(cfg)
    effect = m09.effects(cfg, base)
    shares = m09.shares(effect, base["w"])
    return {
        "N": int(cfg["upstream"]["address_cutoff_N"]),
        "alpha": float(cfg["upstream"]["state"]["alpha"]),
        "threshold_h": float(cfg["upstream"]["update"]["sigmoid_threshold_h"]),
        "beta_scalar": float(cfg["upstream"]["scalar_comparison"]["odd_composite_admission_beta"]),
        "shares": dict(zip(SECTORS, map(float, shares))),
        "counts": {
            "active_addresses": int(len(base["n"])),
            "prime": int(base["prime"].sum()),
            "even_composite": int(base["even"].sum()),
            "odd_composite": int(base["odd"].sum()),
        },
        "minimum_effect": float(effect.min()),
        "maximum_effect": float(effect.max()),
        "maximum_completeness_error": float(np.max(np.abs(effect.sum(axis=0)-1))),
    }

def main():
    assert stage1["baseline_lock_id"] == LOCK
    assert stage1["stage_2_contract"]["legacy_N"] == 1_000_000
    assert legacy_cfg["upstream"]["address_cutoff_N"] == 1_000_000

    L, counts = kzf.rational_ledger_resolution()
    H = max(kzf.HARMONIC_LEDGER)
    zeta = kzf.zeta_focus_count(H, L*H)
    C = int(zeta["C"])
    N_U = int(L*H*C)

    assert [L, H, C, N_U] == [500, 29, 70, 1_015_000]
    assert N_U == published_kzf["WRRA_transformation"]["candidate_generation_window_NU"]

    legacy = summarize(legacy_cfg)

    frozen_cfg = copy.deepcopy(legacy_cfg)
    frozen_cfg["upstream"]["address_cutoff_N"] = N_U
    frozen = summarize(frozen_cfg)

    seed = m09.address_base(frozen_cfg)
    fitted = m09.calibrate(frozen_cfg, seed)

    candidate_cfg = copy.deepcopy(frozen_cfg)
    candidate_cfg["upstream"]["state"]["alpha"] = fitted["alpha"]
    candidate_cfg["upstream"]["update"]["sigmoid_threshold_h"] = fitted["threshold_h"]
    candidate_cfg["upstream"]["scalar_comparison"]["odd_composite_admission_beta"] = fitted["derived_effective_beta"]
    candidate = summarize(candidate_cfg)

    legacy_vec = np.array(list(legacy["shares"].values()))
    frozen_vec = np.array(list(frozen["shares"].values()))
    candidate_vec = np.array(list(candidate["shares"].values()))

    checks = {
        "stage1_lock_preserved": stage1["baseline_lock_id"] == LOCK,
        "legacy_cutoff_preserved": legacy["N"] == 1_000_000,
        "finite_source_generated_not_manual": N_U == L*H*C == 1_015_000,
        "published_kzf_agrees": N_U == published_kzf["WRRA_transformation"]["candidate_generation_window_NU"],
        "legacy_regression_hits_targets": bool(np.max(np.abs(legacy_vec-TARGET)) < 2e-12),
        "candidate_no_refit_stays_close": bool(np.max(np.abs(frozen_vec-TARGET)) < 5e-8),
        "candidate_no_refit_complete": frozen["maximum_completeness_error"] == 0.0 and frozen["minimum_effect"] >= 0.0,
        "same_two_parameter_calibration_closes_targets": bool(np.max(np.abs(candidate_vec-TARGET)) < 2e-12),
        "beta_is_derived_readout": abs(candidate["beta_scalar"]-fitted["derived_effective_beta"]) < 1e-15,
        "no_third_arithmetic_fit": fitted["input_degrees_of_freedom"].startswith("alpha and h fitted to two independent arithmetic targets"),
        "candidate_active_domain_matches_NU": candidate["counts"]["active_addresses"] == N_U-1,
        "legacy_and_candidate_are_separate_configs": legacy_cfg["upstream"]["address_cutoff_N"] == 1_000_000 and candidate_cfg["upstream"]["address_cutoff_N"] == N_U,
        "stage2_does_not_execute_measurement": candidate_cfg["measurement_events"] == [] and candidate_cfg["physical_records"] == [],
        "physical_bridge_still_pending_at_stage2": candidate_cfg["physical_bridge"]["energy_map"] is None and candidate_cfg["physical_bridge"]["pressure_map"] is None,
    }

    patch = {
        "source": "MCC 3.0 Stage 2 generated finite SOURCE insertion",
        "base": "calculations/wrra_m_0_9/parameters.json",
        "legacy_config_mutated": False,
        "candidate_patch": {
            "upstream.address_cutoff_N": N_U,
            "upstream.state.alpha": fitted["alpha"],
            "upstream.update.sigmoid_threshold_h": fitted["threshold_h"],
            "upstream.scalar_comparison.odd_composite_admission_beta": fitted["derived_effective_beta"],
        },
        "roles": {
            "address_cutoff_N": "derived from KZF finite SOURCE generator",
            "alpha": "declared arithmetic calibration",
            "sigmoid_threshold_h": "declared arithmetic calibration",
            "odd_composite_admission_beta": "derived effective readout; not independently fitted",
        }
    }

    result = {
        "project": "Minimal Computing Cosmology 3.0",
        "stage": "2_finite_source_insertion",
        "date": "2026-10-07",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "stage1_lock": LOCK,
        "generator": {
            "L": L,
            "ledger_integer_counts": counts,
            "H": H,
            "C": C,
            "N_U": N_U,
            "product_rule_status": "OPEN construction assumption inherited from Stage 1",
        },
        "legacy_regression": legacy,
        "candidate_frozen_no_refit": frozen,
        "candidate_calibrated": candidate,
        "calibration": {
            "alpha": fitted["alpha"],
            "threshold_h": fitted["threshold_h"],
            "derived_effective_beta": fitted["derived_effective_beta"],
            "delta_alpha_vs_legacy": fitted["alpha"]-legacy["alpha"],
            "delta_h_vs_legacy": fitted["threshold_h"]-legacy["threshold_h"],
            "delta_beta_vs_legacy": fitted["derived_effective_beta"]-legacy["beta_scalar"],
            "input_degrees_of_freedom": fitted["input_degrees_of_freedom"],
        },
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "stage3_handoff": {
            "N_U": N_U,
            "alpha": fitted["alpha"],
            "threshold_h": fitted["threshold_h"],
            "derived_effective_beta": fitted["derived_effective_beta"],
            "legacy_regression_N": 1_000_000,
            "instruction": "Replay component/particle and Prime Parts layers on this candidate address state without changing the historical legacy branch."
        },
        "falsification_conditions": [
            "KZF generation no longer yields N_U=1,015,000 under the frozen Stage-1 construction",
            "candidate address effects become negative or incomplete",
            "the adopted arithmetic targets cannot be closed with the same two disclosed calibration freedoms",
            "a hidden third fit is required",
            "the legacy one-million-address branch must be altered for the candidate branch to work",
            "the OPEN L*H*C construction is silently promoted to a unique law without derivation"
        ]
    }

    (RESULTS / "results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+"
")
    (RESULTS / "candidate_patch.json").write_text(json.dumps(patch, indent=2, ensure_ascii=False, allow_nan=False)+"
")
    assert result["all_checks_passed"], checks
    print(json.dumps({
        "status": result["status"],
        "N_U": N_U,
        "legacy": legacy["shares"],
        "candidate_frozen": frozen["shares"],
        "candidate_calibrated": candidate["shares"],
        "stage3_handoff": result["stage3_handoff"]
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
