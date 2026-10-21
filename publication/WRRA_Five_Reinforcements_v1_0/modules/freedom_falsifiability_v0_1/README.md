# WRRA freedom ledger and joint falsification v0.1

Wonsik Reality-Renderer Architecture. Research item 5.

## Reproduce

```sh
python3 registry.py
OPENBLAS_NUM_THREADS=2 python3 compute.py
OPENBLAS_NUM_THREADS=2 python3 verify.py
python3 plot.py
```

Python 3, NumPy, SciPy and Matplotlib. Main 30/30 checks; separate 88/88 checks. No new observational data fit or SPARC replay. All sensitivity grids, discrepancy injections and parameter recovery examples are generated diagnostics, not measurements.

## Scope

A 30-entry registry covers selected book calibration, recent gravity/zeta modules and explicitly read inherited CMB settings. It is not an exhaustive census of all 138 chapters. Five reference-chain anchor components are not five global WRRA free parameters, nor proof of fewer parameters than base LCDM. Frozen structural choices and calibration inputs remain disclosed. State-space dimension and active fitted dimension are distinguished symmetrically for every theory.

RAR response has only one effective combination of log H0, log kappa, log fD and log gate hazard. Three exact null directions are checked. At fixed SI D-density, H0 cancels. Rotation and finite-patch conditional lensing must use the same effective acceleration with fixed source/receiver. An injected 2% lens-only shift exposes mismatch.

The finite zeta instrument, even with common unknown efficiency and one coherence parameter, leaves a plane constraint among selected probability, in-band probability and probability-weighted energy. Equivalent conditional energy/band-fraction lines are derived algebraically. Synthetic recovery and 1% energy-only perturbation test the constraint. Ideal count Fisher information quantifies weak identification; exact arithmetic recovery is not presented as experimental precision.

Full selected-port energy includes the higher-frequency complementary channel, which requires an appropriate calibrated readout; the single band detector is not assumed to supply all observables. No new physical detector implementation is claimed.

## Files

- `input_manifest.json`, `inputs/`: frozen provenance, original CMB code, previous model results.
- `parameter_registry.csv/json`: roles, values, dependencies and potential dimensions if released.
- `MODEL_LOCK.json`: shared-output and legitimate revision rules.
- `RAR_identifiability.npz`, CSV curves, `results.json`, `independent_verification.json`: computed constraints.
- KO/EN reports and figure. PDFs are included in the deliverable archive.

No exclusive/independent prediction requirement is imposed. Known-value reproduction is explanatory success. Calculated unmeasured relations after fixing inputs belong to conditional WRRA predictions even if another theory yields them too. The RAR response is inherited/credited; WRRA ownership concerns its executed load-to-shared-output chain.

This research result is not yet registered as a new GitHub/GitBook/Zenodo edition. Original book: https://doi.org/10.5281/zenodo.23516661 .
