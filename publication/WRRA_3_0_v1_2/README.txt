WRRA 3.0 publication revision v1.2 reproducibility archive.
Python 3.12, numpy 2.3.5, scipy 1.17.0; matplotlib for figure.
Run python reproduce_all.py, python benchmark.py, python rar_comparison.py without -O.
Frozen stage snapshots include nested dependencies. Reproduction is isolated, not a refit.
benchmark.py: Propositions 1, 3 and 4 implementation controls, same-marginals and actual-interface counterexamples; repeated changing-query grouped baseline.
rar_comparison.py: all 2693 official RAR rows, frozen WRRA scale, no fit.
REPRO_MANIFEST_SHA256.json covers all sources and fixed inputs; timing-dependent results are archived reported runs.
PASS labels describe internal mathematical/implementation checks, not publication approval or SOURCE identification.
