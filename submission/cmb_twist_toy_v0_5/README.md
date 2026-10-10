# A Calibrated Twist-Stress Toy-Model Hypothesis for CMB Temperature and Polarization in WRRA

Wonsik Choi · Version 0.5 · 10 October 2026 · ORCID 0009-0001-4263-9772

## Files

- [Final English manuscript](WRRA_Twist_CMB_Calibrated_Toy_EN_v0_5.pdf)
- [Reproducibility supplement: code, raw binned data, numerical outputs, logs and reviews](Reproducibility_CMB_Toy_v0_5.zip)
- [Korean guide](README_Calibrated_Toy_KO.md)
- [Complete Astra Medium v0.4 review](Astra_Medium_Toy_v0_4_Review_EN.txt)

## Input → transformation → output → rejection conditions

Planck PR3 binned TT, TE and EE spectra supply calibration data; fixed baryon fraction and perturbation rules are declared model assumptions. The WRRA twist-stress interpretation is mapped to a neutrino-separated density ledger and executed through adopted CAMB transfer equations. The combined diagonal residual diagnostic improves from 1.106151 to 1.034789; TE slightly worsens. Reproduction failures or disagreement with a fixed effective profile reject the corresponding implementation or realization. Identical CDM perturbation rules do not distinguish the two interpretations through CMB spectra alone.

This is an exploratory calibrated toy-model/model-development preprint. The finite SOURCE-to-spatial-perturbation transformation is not implemented here. The diagnostic is not the official Planck likelihood.

## Reproduce

Extract the supplement, install requirements.txt, then run `python calibrate_twist.py` followed by `python check_twist_robustness.py`. Exact environment and termination diagnostics are included. Stable calibration endpoints are not claimed as verified stationary or global optima.

## Review status

Astra Medium recommended publication of v0.4 after minor revisions within the exploratory calibrated toy-model/computational model-development scope. All three requested minor edits are implemented in v0.5. No separate fresh v0.5 review or journal acceptance is claimed. Full reviews and the reviewed/final PDF provenance are preserved in the supplement.

Zenodo registration is in progress; no DOI is asserted before publication is verified.
