# From Clock Synchronization to SOURCE Lensing and CMB

Wonsik Choi and Jeongin Choi · Independent Researchers · 14 October 2026 · v1.0

A bilingual executable MCC/WRRA research record from neutrino/hydrogen time and phase calibration through finite shared-carrier transport, SOURCE supplier/stress construction, actual Boltzmann propagation, address-level calibration, and expanded CMB/lensing evaluation.

- [English report](MCC_Clock_to_CMB_Research_Record_v1_0_EN.pdf) · [Korean report](MCC_Clock_to_CMB_Research_Record_v1_0_KO.pdf)
- [English research record](RESEARCH_RECORD_EN.md) · [Korean research record](RESEARCH_RECORD_KO.md)
- [Numerical index](research_record.json) · [Exact stage manifest](release_manifest.json)

## Validation inputs

Known physical constants, experimental summaries and public Planck data; inherited finite address/slot/supplier ledgers. Calibration is recorded separately from later frozen-rule checks. c is an input, not a prediction.

## WRRA transformation

Event coding → resource/energy ledgers → shared-carrier clock and metric → supplier stress and actual physical evolution → observational evaluation. Adopted physical modules are credited and counted as integrated only when executed.

## Outputs

The latest high-l Plik-lite quadratic form is **585.7475077953264**. SOURCE deflection RMS is **0.009556588544185153 arcsec**. The latest numerical controls pass **15/15**; upstream reconstruction passes **28/28**. Earlier failures and observationally informed changes remain visible, including the hydrogen precision holdout and unweighted CMB discrepancy.

## Refutation conditions and assessment

Require correct event/unit meanings, address and probability conservation, positive covariances, consistent stress/transfer coupling, numerical convergence and declared observational comparisons. The current result is a conditional mean-stress model, with primordial generation, single-outcome gravity, a unique universal clock/metric, exact non-Gaussian SOURCE remapping, BAO and nucleosynthesis comparisons still open.

## Reproduce

The repository contains the reports, source code and text result ledgers. Large binary inputs and transfer arrays are archived in the complete Zenodo package. Download and extract that package from https://doi.org/10.5281/zenodo.23361676, then:

```bash
python prepare_workspace.py --verify-only
python prepare_workspace.py
pip install -r requirements.txt
python stages/neutrino_sync_v01/reproduce.py
python stages/cmb_preparation_lensing_v01/reproduce.py --verify-only
```

Each stage preserves its original reproduce.py, README, frozen inputs, controls, CSV/JSON/NPZ results and applicable software licenses. Heavy CAMB runs must be serial. Linux runtime and the pristine CAMB source/patch/build route are included in the complete package. Large repeated assets use a SHA256 object store and are restored locally without network access.

Original finite-frame context: [DOI 10.5281/zenodo.23329214](https://doi.org/10.5281/zenodo.23329214). No private correspondence is included and no external endorsement is claimed.

Archived release DOI: https://doi.org/10.5281/zenodo.23361676
