CMB follow-up audit — units, seven harmonics and ledger counterfactuals
14 October 2026

Validation inputs: frozen SOURCE/supply amplitudes, both background ledgers, patched CAMB 2.0.4 and native Plik-lite TTTEEE data. Transformation: physical energy density -> dimensionless D/R vector -> conserved mode evolution and angular transfer, followed by a fixed-ledger swap diagnosis.

Direct SI conversion of background density, vacuum stress, dark momentum and force ratio agrees with the executed coefficients to a relative error below 5.56e-16. Native solver tests with vacuum basis amplitudes .01 and 2, and a directly evolved mixed D/R vector, agree with normalized or superposed transfer functions. The largest amplitude-test discrepancy is 0.0788% in E for the .01 case.

All 28 real harmonic trajectories remain finite. Individual density, velocity, growth and momentum residuals are exported. Logarithmic growth is marked OPEN near a density zero crossing; this diagnostic singularity is not labeled a state runaway. A second-gauge execution/comparison is not claimed.

Background high-ell quadratic forms at fixed calibration:
unweighted original: 1217.75122;
replace only its dark ledger with the weighted value: 585.91392;
replace only its vacuum ledger with the weighted value: 1121.90312;
weighted original: 591.57034.
H0 is recomputed from the closed background energy total, not independently optimized. These hybrids are diagnosis-only configurations, not newly derived WRRA branches. The dark background ledger is the stronger contributor to the discrepancy in this setup.

Refutation conditions: unit mismatch, failure of solver amplitude convergence/superposition, conservation failure, departure from the linear regime, or failure of the ledger-swap diagnosis at higher precision.

The early-universe extension was already included in the first CMB calculation. Its upstream preparation derivation and SOURCE-specific lensing remain open. No new scale optimization or arbitrary SOURCE amplification is performed here.

Install requirements.txt, then run python reproduce.py. The executed Linux CAMB binary and required prior arrays are included. Other platforms can build the included patch with python build.py, gfortran and make. See README_KO.txt for equations, covariance conventions and source attribution.
