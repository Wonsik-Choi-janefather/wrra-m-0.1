# Finite WRRA Models — five reinforcements, v1.0

Wonsik Choi and Jeongin Choi, 2026-10-21.
WRRA means **Wonsik Reality-Renderer Architecture**.

Standalone Korean and English papers: https://doi.org/10.5281/zenodo.23522417

This release rechecks finite scaling, SOURCE/carrier dynamics, RAR-preserving gravity, zeta readout/dynamics, and freedom/falsifiability accounting. All seven main-program/verifier pairs passed; all 19 cross-module checks passed. The 1,459 sampled internal invariants are not independent experimental evidence. This is a preprint, not a claim of completed GR/SM derivation or external peer review.

## Reproduce

Use Python 3.12, install `requirements.txt`, then run:

```sh
OPENBLAS_NUM_THREADS=2 python recheck.py
python cross_audit.py
python make_figures.py
```

The first command reruns seven modules with concurrency limited to two. The JSON reports record the actual tested environment. `modules/` contains frozen inputs, executable code, outputs and individual verification logs. `PROVENANCE.json` identifies the earlier module sources. Historical module publication statements describe their earlier context; this consolidated release supplies the current paper. The zeta CRT preparation and original sector-specific SOURCE are distinct test preparations; no complete universe simulation is claimed.

Read PAPER_EN.md or PAPER_KO.md for equations, calibration choices, falsifiers and OPEN connections. Existing RAR is retained, and adopted QUMOND is credited. Known observations are legitimate calibration; neither numerical novelty nor unique predictions are prerequisites for evaluating the declared transformations. No new SPARC fit or whole-model likelihood comparison was executed.

GitBook was not modified for this release.

License: CC BY 4.0; retained third-party inputs and methods remain attributed to their original sources.
