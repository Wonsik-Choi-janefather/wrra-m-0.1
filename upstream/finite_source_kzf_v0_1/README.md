# WRRA_M finite SOURCE closure — KZF v0.1

> Compatibility/checkpoint package. Canonical reviewed package: `../finite_klein_zeta_window_v0_1/`.

This folder tests a finite-generation-window candidate for WRRA_M.

Core result:

`N_U = 500 × 29 × 70 = 1,015,000`

Status: **PASS-C** — admissible finite SOURCE candidate, not yet a uniquely derived fundamental constant.

Files:
- `WRRA_M_KZF_Finite_Source_Closure_v0_1_EN.md` — English paper
- `WRRA_M_KZF_Finite_Source_Closure_v0_1_KO.md` — Korean paper
- `verify_kzf.py` — standalone reproducibility script
- `results.json` — machine-readable verification output

Run:

```bash
python verify_kzf.py
```

Dependencies: NumPy, SciPy, mpmath.
