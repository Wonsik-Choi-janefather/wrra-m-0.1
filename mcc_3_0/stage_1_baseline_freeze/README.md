# Minimal Computing Cosmology 3.0 — Stage 1 Baseline Freeze

**Status:** PASS — baseline and provenance frozen for MCC 3.0 integration  
**Date:** 2026-10-07  
**Authors:** Wonsik Choi, Jeongin Choi  
**Baseline lock ID:** `MCC3-S1-21daec11-43b998ca-f667bbdf`

## Purpose

Stage 1 freezes the three inherited research lines that MCC 3.0 will integrate without rewriting their historical results:

1. **Minimal Computing Cosmology 2.3.2** — foundational MCC corpus.
2. **WRRA_M Integrated Model 1.0 r1** — executable upstream/downstream/bridge baseline.
3. **WRRA_M Finite Klein–Zeta Generation Window v0.1** — finite SOURCE generator candidate.

No numerical result is reclassified silently. Every inherited item is assigned one of five roles:

- verification input,
- calibration input,
- WRRA-specific rule,
- derived output,
- open assumption.

## Frozen source pins

| Source | Repository / path | Frozen commit | Role in MCC 3.0 |
|---|---|---|---|
| MCC 2.3.2 | `Wonsik-Choi-janefather/minimal-computing-cosmology-2.3.2` | `21daec110c0cbecb228c445d587eac8302e7f767` | Foundational theory corpus |
| WRRA_M 1.0 r1 | `integrated/v1_0_r1/` | `43b998ca0ac63c6ae21eb0e0bc543e98172a42e4` | Frozen executable physical baseline |
| KZF v0.1 | `upstream/finite_klein_zeta_window_v0_1/` | `f667bbdfc7d6b6202fda8003289d11ff69d491b1` | Candidate finite SOURCE generator |

These pins are provenance anchors. Later MCC 3.0 work may copy or call equations and code from them, but must not overwrite the meaning of the frozen releases.

## Stage-1 role classification

### Verification inputs

These are supplied or adopted physical/arithmetic reference values used to test or fix the model:

- SI defining value `c = 299792458 m/s`.
- `G = 6.6743e-11 SI`.
- `H0 = 67.4 km/s/Mpc` in the frozen WRRA_M physical baseline.
- inherited late-universe physical energy calibration `0.0493 / 0.265 / 0.6857`.
- adopted arithmetic ledger targets `0.05 / 0.268 / 0.682`.
- electron rest-energy anchor `510998.95069 eV`.
- other measured particle constants remain inherited at their source-stage provenance and are not promoted to new MCC 3.0 predictions.

### Calibration inputs

These values fix declared model freedoms and are not independent predictions:

- legacy address exponent `alpha_0 = 1.8996876950554356`.
- legacy admission threshold `h_0 = 1.44767317035244`.
- scalar comparison `beta_0 = 0.8654570124136961`.
- frozen SI address-response coefficients `eta_phi, eta_D, eta_R`.
- response-profile slopes and other already disclosed constitutive choices of WRRA_M 1.0.

For the KZF candidate window, the same two arithmetic freedoms are minimally recalibrated to

- `alpha_1 = 1.8996877935161325`,
- `h_1 = 1.4476744689338703`,

while `beta_eff = 0.8654567230719301` is read out as a derived value, not independently refitted.

### WRRA-specific rules

The following are part of the model transformation rather than external measurements:

- finite address weighting and prime/composite classification;
- filter / residue / component / phenotype transport;
- address-state to information-load and SI energy map;
- one-ledger pressure, gravity, rotation, lensing and expansion propagation;
- finite proper-time state update and conservation checks;
- KZF address map
  `n = 1 + ell + L[h + H(z-1)]`;
- candidate finite closure
  `N_U = L * H * C`.

### Derived outputs

Outputs generated after the above inputs/rules are fixed include:

- legacy WRRA_M regression values such as `q0 = -0.52855`, reference rotation and conditional lensing;
- harmonic ledger quantities retained from the existing model;
- KZF quantities
  `L = 500`, `H = 29`, `C = 70`;
- conditional finite SOURCE prediction
  `N_U = 1,015,000`;
- KZF frozen-SI downstream outputs
  `q0 = -0.5285585894376319`,
  `v_ref = 207.5102418659153 km/s`,
  lensing `0.5355822400088303 arcsec`;
- proper-time conservation diagnostics.

Known-value reproduction remains a reality-consistency/explanatory result. A previously unmeasured quantity produced after model fixing is classified as a conditional WRRA/MCC model prediction.

### Open assumptions

The following are **not frozen as derived laws** in Stage 1:

1. `T = 2*pi*H` is the physically required zeta phase boundary.
2. `L`, `H`, and `C` are independent Cartesian state coordinates.
3. `N_U = L*H*C` is the unique finite closure rather than one admissible closure.
4. The Klein-type orientation reversal is the required upstream topology rather than a useful finite boundaryless implementation.
5. The zeta-focus structure is a physical upstream mechanism rather than a successful mathematical organizing rule.
6. Any still-open microscopic component-to-particle or fully covariant completion from the frozen MCC/WRRA corpus remains open unless explicitly executed in MCC 3.0.

## Stage-1 falsification / rejection conditions

Stage 1 fails if:

- one of the frozen source pins cannot reproduce its declared release;
- an inherited calibration is mislabeled as a derived prediction;
- an open KZF assumption is silently promoted to a physical law;
- a later MCC 3.0 stage changes a frozen baseline value without a new provenance record;
- the same symbol or quantity is assigned incompatible roles across the Master Ledger.

## Stage-1 output

The baseline is now locked. Stage 2 may therefore replace the old practical address cutoff only inside the **new MCC 3.0 integration branch**, while preserving the legacy `N=1,000,000` execution as a regression reference.

**Stage 1 verdict: PASS.**
