# v0.28-r5 review evidence

Run from this directory:

    python sparc_fit_v02/test_controls.py
    python review_checks.py

The first replays saved fitted parameters and intentionally corrupts an isolated copy. The second matches saved input rows to the preserved source catalogs and checks finite matrix examples. Full optimization is reproducible with `python sparc_fit_v02/fit.py`; it was not rerun for the r5 review.

`address_scaling` and `laboratory_design` preserve the previously executed r2/r3 work, not newly performed laboratory observations. Legacy READMEs/manifests are provenance snapshots; `SHA256SUMS_r5.json` is this package's current manifest. The review does not establish universal NFW superiority or whole-MCC execution.
