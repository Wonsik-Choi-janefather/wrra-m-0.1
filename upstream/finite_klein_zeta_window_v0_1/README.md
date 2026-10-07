# WRRA_M Finite Klein–Zeta Generation Window v0.1

This package tests a finite upstream address-window candidate for WRRA_M.

## Core result

Using the adopted WRRA_M arithmetic ledger, the existing harmonic ledger, and a finite zeta-focus count,

[
L=500,qquad H=29,qquad C=N_zeta(2pi H)=70,
]

the declared product rule gives

[
N_U=LHC=1,015,000.
]

Status: **PASS-C** — accepted as a finite-generation-window candidate and conditional WRRA_M prediction under the stated construction, not as an experimentally established fundamental constant.

## Verification sequence

**Verification input → WRRA-specific transformation → output → falsification condition**

The code:

- reproduces the legacy `N=1,000,000` WRRA_M address ledger first;
- inserts `N_U=1,015,000` with old arithmetic parameters frozen;
- refits only the same two arithmetic freedoms already used by WRRA_M (`alpha` and threshold `h`);
- keeps the downstream SI response coefficients frozen;
- checks downstream `q0`, reference rotation and conditional lensing;
- checks finite-carrier positivity and proper-time energy conservation.

## Main numerical outputs

- Candidate finite window: `N_U = 1,015,000`
- 70th zeta zero: `182.20707848436646`
- Boundary: `2*pi*29 = 182.212373908208`
- Recalibrated `alpha = 1.8996877935161325`
- Recalibrated `h = 1.4476744689338703`
- Derived `beta_eff = 0.8654567230719301`
- Arithmetic ledger: `5% / 26.8% / 68.2%`
- Frozen-SI downstream:
  - `q0 = -0.5285585894376319`
  - `v_ref = 207.5102418659153 km/s`
  - `lensing = 0.5355822400088303 arcsec`
- Maximum proper-time relative energy drift: `9.992007221626409e-16`

## Files

- `code/compute.py` — self-contained executable verification
- `results/results.json` — full numerical ledger and checks
- `paper/PAPER_KO.md` — Korean paper
- `paper/PAPER_EN.md` — English paper

## Run

```bash
python code/compute.py
```

Dependencies: Python 3, NumPy, SciPy, mpmath.

## Main unresolved condition

The numerical and ledger tests pass, but the product

[
N_U=L	imes H	imes C
]

is still an explicit WRRA construction assumption. The next step is to derive, or falsify, the independence of these three coordinates from a higher WRRA state law.

## Provenance

This package extends the existing repository lines `upstream/zeta_frame_v0_1`, `upstream/two_stage_filter_v1_0`, and downstream calculations `wrra_m_0_9` through `wrra_m_0_12`.

Authors: Wonsik Choi, Jeongin Choi  
Date: 2026-10-07
