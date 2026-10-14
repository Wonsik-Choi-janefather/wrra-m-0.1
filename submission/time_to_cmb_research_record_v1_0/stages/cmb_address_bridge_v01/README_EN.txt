Address-generated dark-weight candidate and CMB bridge 0.1
14 October 2026

Validation inputs: the actual frozen 1,015,000-address ledger (address 1 handled separately), sector effects, eta, residue kernels, 128-slot routing, finite source/supply rule, existing conditional primordial extension and public CMB data.

Transformation: address -> sector-specific logarithmic weight -> rerouted residue payload -> counted finite source/supplier -> mean physical energy and Fourier stress -> executed modified CAMB -> TT/TE/EE and covariance evaluation.

The inherited family is c_s(n)=e_s(n)w_n[1+lambda_s ln(n)/ln(N_U)]. Existing cases use lambda=(0,0,0) and (0,.25,.1). The new lambda=(0,.25,0) candidate is selected after the observational ledger-swap diagnosis. It is an observationally informed calibration within the existing family, not a uniquely forced or blind prediction.

Exact dark mean reconstruction:
mu_D(0)=.268;
sum e_D*w*ln(n)/ln(N_U)=.04370244390697558;
Delta mu_D=.25 times this moment=.010925610976743895;
mu_D(.25)=.27892561097674395.
The energy increment is 7.960139394787346e-12 J/m^3, or 4.07672%. Addresses below 100 supply 88.8042% of the increment. The controlled mod3 complement supplies 68.4135%, and the other addresses 31.5865%.

Slot capacity depends on the complete input ledger, so the candidate is rerouted from addresses. Its dark slot payload differs from the original weighted payload, while its dark residue marginals agree. Both source and supplier are counted. A8+gap/2=1 closes the inherited uniform mean. The new energy/pressure balance error is below 2.07e-25 J/m^3.

The directly generated background is:
H0=67.2568374662005 km/s/Mpc;
omega_b h^2=.022395806792949086;
omega_c h^2=.12037806177378184.
H0 follows from the energy total and fixed thermal budget; no new optimizer or downstream density swap is used.

Native high-ell Plik-lite TTTEEE quadratic forms, 613 bins, fixed A_planck=1:
unweighted address baseline: 1217.7512246828783;
weighted address baseline: 591.5703352409629;
new address candidate baseline: 585.913918450675;
candidate plus linear SOURCE: 585.9139188511556.
The new baseline reproduces the earlier exchange diagnostic to 3.47e-9 in the quadratic form. Its SOURCE TT contribution peaks at 1.53409e-5 microK^2 and remains observationally negligible here.

All 41 construction and numerical checks pass, including address/route equality, source/supply energy and pressure, original-branch reproduction, zero-source restoration, two resolutions, independent momentum integration and linear-regime bounds.

Refutation conditions: failed address/routing identity, energy/pressure conservation, baseline reproduction, zero-source restoration, numerical convergence, linear-regime bounds or disagreement under agreed completed observational modeling.

Conclusion: the diagnostic dark-ledger change is realized as an explicitly generated upstream candidate and propagated internally to CMB observables. This is a conditional reality-consistency and explanatory result. Weight calibration's interpretation/applicability, upstream derivation of primordial preparation, SOURCE-specific lensing and full Planck likelihood remain open. The early-universe extension itself is already included.

Install requirements.txt and run python reproduce.py. Actual address arrays and the experimental Linux CAMB runtime are included. Other systems can use python build.py with gfortran/make. See README_KO.txt and the JSON/CSV/NPZ outputs for details. Sources: CAMB 2.0.4 (included license), Planck 2018 V, native Plik-lite data and conventions from Cobaya/Calabrese/Lewis. Frozen upstream context: doi:10.5281/zenodo.23329214; this new package has not been uploaded to that DOI by this task.
