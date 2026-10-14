Minimum-Computation Cosmology: Finite Mean Preparation, SOURCE Lensing, and Expanded CMB Evaluation v0.1
Wonsik Choi and Jeongin Choi / 2026-10-14

INPUTS
Actual 1,015,000-address archive; inherited residue/128-slot/supplier ledgers;
fixed eta, lambda=(0,0.25,0), epsilon=1e-8, k_n=0.05 n Mpc^-1 for n=1..7.
The prior observationally informed calibration is retained, with no amplitude optimizer
or post-readout density swap. c is a declared fixed input. Calibration by known data
is permitted; an independent prediction is not a mandatory criterion of the architecture.
Public Planck high-l Plik-lite (613 bins), low-T/low-E (l=2..29), and nine
CMB-marginalized lensing bins are executed, not merely referenced.

ARCHITECTURAL TRANSFORMATION
Reconstruct e_s(n)w_n[1+lambda_s ln(n)/ln(N_U)] -> residue/slot/supply payload.
Add a counted 128-state phase-control register rho=I/128, distinct from the pure |8>
SOURCE register. Conditional supplier states have p_r,j=1/2+epsilon(K_r,j-1).
The initial control entropy is ln(128); energy-degenerate memory is declared.
No free repeated reset or dynamical preparation process is claimed.
Construct the finite mean-energy profile and compare its covariance with
sum_n(v_cos v_cos^T+v_sin v_sin^T)/2. Retain the adopted macro-scale anchor
and isotropic orientation average. Feed the resulting S_D and delta_R into the
adopted regular radiation/CDM-isocurvature extension; inspect actual CAMB
initial-condition callbacks. The retarded dark velocity ledger uses the near-radiation
background series; the solver callback uses its regular leading term.
Run patched CAMB for all seven SOURCE wavenumbers and every l=2..6000,
including the third (phi) transfer. Disable continuum Limber substitution for SOURCE.
Check phi normalization against direct primordial quadrature at low L.
Execute CAMB covariance remapping as
L(C_std,Cphi_std+Cphi_SOURCE)+L(C_SOURCE,Cphi_std+Cphi_SOURCE).
The adopted standard primary field and SOURCE primary field are independent.
This is a covariance-kernel extension. SOURCE higher connected moments and primary/lens
correlations are not fully remapped; it is not exact finite-ensemble non-Gaussian lensing.
Execute native Cobaya TT/EE and CMBlikes with released CMBmarged data,
and native Gaussian Plik-lite with the full released bin covariance and weights.
Official clik and an unmarginalized full foreground analysis are not executed.

OUTPUTS
Finite-phase/Fourier covariance relative discrepancy: 1.94218577e-09.
Initial density callback maximum relative discrepancy: 3.31358074313e-08
(native named density outputs are float32); velocity: 2.22044604925e-16.
SOURCE deflection RMS: 0.00955658854419 arcsec.
Standard deflection RMS: 146.804724052 arcsec.
SOURCE/standard deflection variance: 4.23765614476e-09.
High-l quadratic form: 585.747507795326.
Low-T -2logL: 23.425650359080.
Low-E -2logL: 396.117345699899.
CMBmarged lensing -2logL: 9.066339239596.
SOURCE change in the summed offset-dependent -2logL: -8.07531250757e-07.
The sum near 1014.36 is not a universal chi-square with a simple degree count;
blocks have different likelihood normalization constants. The SOURCE change is tiny.
The earlier high-l result 585.9139 versus 585.7475 is primarily a change of the
baseline lensing calculation, not evidence for a SOURCE-driven fit improvement.

REFUTATION AND NUMERICAL CONTROLS
Revise the connection if preparation positivity, covariance positivity, initial
callback agreement, phi units/normalization, or resolution/remapping checks fail.
New checks: 15/15 passed. Upstream reconstruction: 28/28 passed.
Accuracy 1.5 -> 2.5 changes the peak-normalized phi spectrum by
0.25953% and the CMB spectrum by 0.01491%.
Lmax 5000/6000 and Python/native Fortran baseline remapping controls have
covariance-whitened bin RMS differences approximately 0.000305 and 0.000288.
An int32 overflow in the squared lensing normalization was caught by the positivity
check, corrected using float64, and all affected outputs recomputed before packaging.
These are numerical/structural checks of the declared conditional model.

CONCLUSION AND OPEN CONNECTION
The finite mean preparation, adopted physical initial dressing, executed SOURCE
covariance lensing, and expanded native observational evaluation are connected.
The mean/single-outcome bridge remains open. In an explicitly independent-address
supplier-bit preparation, intrinsic relative RMS is D=0.34514 and R=0.49415,
versus mean phase modulation RMS 1.21074e-8 and 9.48940e-9.
Current gravity reads ensemble-mean stress; this intrinsic variance is not silently
identified with a cosmological stochastic field. Correlated preparations can alter it.
Pure independent-frame averaging would require roughly 8.13e14/2.71e15 samples;
fresh resources, independence, record/reset costs, and actual averaging dynamics
have not been implemented. The next task is a counted correlated preparation or
finite averaging model linking individual execution to mean stress. Dynamical
generation of the primordial preparation and exact SOURCE non-Gaussian remapping
also remain open.

REPRODUCTION
pip install -r requirements.txt
python reproduce.py                 # serial upstream, CAMB, likelihood, controls
python reproduce.py --skip-camb     # re-use saved transfers
python reproduce.py --verify-only   # numerical controls and plots
Bundled patched Linux runtime; pristine CAMB source tarball, patch, build script,
licenses, actual public datasets, JSON/CSV/NPZ outputs, figures and SHA256 checksums.
If the binary is incompatible, install gfortran/make and run python build.py.
