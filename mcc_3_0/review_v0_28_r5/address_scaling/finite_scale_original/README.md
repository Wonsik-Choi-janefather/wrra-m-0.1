# WRRA finite-scale bridge v0.1

**Wonsik Reality–Renderer Architecture**. This package addresses finite discrete-to-continuum scaling while retaining the existing SOURCE ownership and spectral transport contracts.

## Reproduce

Requires Python 3 and NumPy. Validated with NumPy 2.3.5.

```sh
python3 compute.py
python3 verify.py
```

`compute.py` reads only `payloads.json`, `reference_profiles.npz`, and `inputs_manifest.json`. It reconstructs both frozen branches, executes conservative coarse-graining and spectral evolution, applies an adopted weak-field receiver to the actual energy output, and performs a separate 3D convergence witness and negative controls. No network calls or fitted observational parameters.

Expected results: 179 internal checks pass. Independent modal/Parseval verification matches 3D grid-error values within 2.178e-16 absolute difference. Exact floating-point values can differ slightly across platforms.

Reports: `REPORT_KO.md`, `REPORT_EN.md`. Tables: `source_coarse_graining.csv`, `actual_source_receiver.csv`, `spectral_coarse_transport.csv`, `refinement.csv`. Details: `results.json`, `independent_verification.json`.

## Scientific status

The original source is replayed; Poisson and local difference-wave equations are declared receivers, not newly derived microscopic WRRA laws. No full GR/SM renormalization, universal transition scale or physical nonlinear closure is claimed. Source address labels, internal slots, profile samples and spatial renderer cells remain distinct. The original positive-frequency spectral operator remains spatially nonlocal.

Existing registered book: https://doi.org/10.5281/zenodo.23516661
Existing spatial bridge: https://doi.org/10.5281/zenodo.23329214
Repository: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1

This new calculation package is not represented as an already published Zenodo/GitBook edition. Original inputs and their provenance hashes are retained in `inputs_manifest.json`.
