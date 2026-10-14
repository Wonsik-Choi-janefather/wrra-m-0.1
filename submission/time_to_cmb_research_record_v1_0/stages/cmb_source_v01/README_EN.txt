Conditional SOURCE CMB verification 0.1 — 14 October 2026
Research context: Wonsik Choi and Jeongin Choi

The frozen seven SOURCE/supply harmonics have been propagated through a modified CAMB 2.0.4 photon/neutrino calculation. This is an explicit conserved dark/vacuum response, rather than a relabeling of existing adiabatic spectra. No new cosmological optimization was performed.

At accuracy 2.5, using the released native Plik-lite high-ell TTTEEE covariance and bin weights, with A_planck fixed to 1:
weighted: quadratic form 591.5703358 for 613 bins;
unweighted: 1217.7512273 for 613 bins.
The conditional weighted completion is consistent with these data; the unweighted completion exhibits substantially larger disagreement. These scores are a native Gaussian implementation, not an official clik executable run, and exclude low-ell and lensing likelihoods.

The extra SOURCE TT contribution peaks at approximately 1.54e-5 and 1.47e-5 microK^2. Its effect on the quadratic form is negligible and much smaller than baseline numerical precision changes. Baseline agreement does not identify this very small new contribution.

New, explicitly conditional choices:
- Extend the former late-epoch SOURCE test into the radiation era using regular CDM-isocurvature entropy amplitude delta_u_D0/u_D0 and a constant delta_R. This is not an inverse continuation preserving the former a=.02 initial data.
- Uniform global phase and orientation define the angular ensemble. Retain D/R cross covariance at each harmonic. SOURCE and the existing standard adiabatic perturbations are independent.
- Retain k_n=.05*n Mpc^-1 and epsilon=1e-8. No new spatial-scale fit.
- Calculate the SOURCE contribution linearly without SOURCE lensing, then add it to the standard lensed baseline as a first-order diagnostic.

Geodesic synchronous-gauge equations:
delta_R'=0;
delta_D'=-k(z+v_D);
v_D'=-H_conformal*v_D-k*(rho_R/rho_D)*delta_R.
Vacuum pressure perturbation is -rho_R*delta_R; total added momentum is rho_D*v_D. Dust velocity is included in both the metric momentum and the dust continuity equation. The late radiation approximation is disabled for SOURCE runs, and late ISW sources are retained.

Checks include archived-baseline reproduction at identical lmax, zero-source restoration, two resolutions, a tenfold earlier start, nonnegative auto spectra and TE covariance, an independent integrating-factor momentum test, and an omitted-force negative control. The actual combined perturbations remain inside the declared linear regime. See results/results.json and evolution_audit.json for values; numerical checks are distinct from observational evidence.

The CMB physical ages are also expressed in the existing shutter unit. This conversion adopts the declared FRW background; it does not derive the SI second from SOURCE addresses alone.

Run: install requirements.txt, then python reproduce.py.
An experimental Linux x86_64 CAMB binary is included in runtime/camb. For other systems, use python build.py with gfortran and make. The pristine archive, patch and license are included. The CMB stage reads frozen upstream Fourier vectors; upstream address aggregation is documented rather than rerun here.

Main outputs: baseline and SOURCE TT/TE/EE CSVs, seven-k T/E transfer functions, native Plik-lite scores, conservation audit, physical-time/shutter conversions, and SOURCE_CMB_comparison.png. README_KO.txt explains assumptions, refutation conditions and remaining integration work in detail.

Sources: CAMB 2.0.4 (included license); Planck 2018 V, doi:10.1051/0004-6361/201936386; Planck PR3 public bins; native Plik-lite data from CobayaSampler/planck_native_data release v1; likelihood conventions by E. Calabrese and A. Lewis in Cobaya PlanckPlikLite. Frozen upstream research context: doi:10.5281/zenodo.23329214. This new calculation has not been deposited at that DOI by this task.
