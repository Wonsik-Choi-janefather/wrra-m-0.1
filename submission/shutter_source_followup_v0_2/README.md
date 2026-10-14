# Finite SOURCE follow-up v0.2

Supply averaging, photon pulses, and CMB higher-order correlations.
Wonsik Choi and Jeongin Choi, Independent Researchers. 15 October 2026.

Reserved DOI (public publication pending): https://doi.org/10.5281/zenodo.23380920

Zenodo DOI 10.5281/zenodo.23380920 is reserved. A metadata draft was saved, but file-upload completion and public publication remain unverified after a browser connection failure. Do not treat the reserved DOI as a published record until verified. The preceding input record DOI 10.5281/zenodo.23361676 remains published.
Inherited clock-to-CMB record: https://doi.org/10.5281/zenodo.23361676

## Review outcome

176/176 internal numerical controls pass. Original principal v0.1 values are
preserved. This version corrects the Gaussian CMB comparator interpretation,
GDD units, entropy claims, threshold edge cases and rerun verification.
Common-axis Gaussian-moment initial harmonics retain a connected sky fourth
moment; they must not be confused with an isotropic Gaussian angular field.
No new observational fit, new CAMB solver run, or full NG likelihood is claimed.

## Reproduce from the complete Zenodo ZIP

```bash
python -m pip install -r requirements.txt
python verify.py --archive
OPENBLAS_NUM_THREADS=1 python reproduce.py
python figures.py
python verify.py
```

The ZIP contains frozen inputs/, source, outputs, an unchanged optical_model_v1_0
appendix, Korean/English reports and PDFs, numerical references and SHA256SUMS.
`--archive` checks all bytes as distributed. Default verification checks frozen
source/input hashes plus stable numerical observables after rerunning, excluding
elapsed wall time. The optical appendix retains its historical v1.0 manifest.

The GitHub folder provides readable source, reports and selected results; large
binary input/output arrays are distributed in the complete Zenodo ZIP. Extract
the ZIP to reproduce. Do not attempt to reproduce from a partial repository copy.
Historical v0.1 reports in review/ are superseded by the v0.2 reports.

## Results and limits

- Independent-shutter supply thresholds: D 1.203737902 us, R 4.016874415 us;
  static bits do not average down. Correlation and resource laws are explicit.
- Fixed linear optical phase: zero intrinsic energy-dependent dispersion;
  40.38596522 as ensemble arrival RMS at 1 m. This is phase-screen statistics.
- Actual cached seven-mode CAMB transfer: conditional SOURCE T excess kurtosis
  32.2551732492 at ell 2..256; common-axis Gaussian-moment comparator 40.7442439509.
  Joint-preparation dependence prevents a unique quantization interpretation.

Read REPORT_EN.txt / REPORT_KO.txt for validation inputs, WRRA transformation,
outputs, refutation conditions and qualified conclusions, in that order.
Existing calibration constants are accepted as inputs, not reclassified as new
independent predictions. All controls are internal numerical checks.
