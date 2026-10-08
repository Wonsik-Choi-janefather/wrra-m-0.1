Executive paper A revised v1.0
Authors: Wonsik Choi and Jeongin Choi

Read Paper_A_EN_v1.0 or Paper_A_KO_v1.0 for the revised argument.
Astra_Review_EN.txt records the separate AI-assisted review; it is not journal acceptance.

Reproduction:
  python -m pip install -r requirements.txt
  python run_all.py
Do not use python -O. Tested Python 3.12.14, numpy 2.3.5, mpmath 1.3.0.
The vendored mpmath 1.3.0 is provided with its distribution license and metadata.
NumPy must be available. No network is used by the audit scripts themselves.

SOURCE_SHA256.json protects the executed source/config files.
RELEASE_SHA256.json records final deliverable/source/evidence hashes.
The runner compares newly calculated outputs to registered numeric expectations.
Numerical contour winding is explicitly not interval-certified.
The full source_A.md is the historical executive-paper A preserved for comparison.

Experiments:
1 audit_A.py: exact serialization, standard zeta count, finite-function contour,
  boundary crossing, imported-zero residuals, high-precision spot checks, cutoff tail.
2 frozen_source_replay.py: original alpha/h and no-refit cutoff comparison.
3 address_structure.py: recalibrated MCC reference, factor structure, transported
  readouts across all six tuple orders and three random permutations, active controls,
  and conditional macro replay. Its dependency_manifest pins original functions.
These are separate calibrated configurations; no new fit is performed.
