## 138. A Live Galactic Distribution Function and the Gaia Comparison

### 138.1 Verified inputs and the executed WRRA connection

The WRRA–AGAMA bridge v0.3 advances the galactic branch from a prescribed spatial profile to an actual live stellar distribution-function and Poisson iteration. Inputs are the original baryonic masses/radial scales and constitutive response, $a_T=1.191812669\times10^{-10}\ {\rm m\,s^{-2}}$, explicit finite-height profiles, two trial QuasiIsothermal stellar DFs and public Gaia samples. Gas and bulge remain static; the two stellar DFs are live. Adopted stellar heights are 0.3/0.9 kpc, gas sech-squared scales 0.085/0.045 kpc and trial radial-dispersion amplitudes 35/55 km/s at 8.2 kpc. These are disclosed physical choices, not new microscopic derivations.

The executed chain is baryonic state → prescribed WRRA residual acceleration → spherical effective density/potential → live stellar $f(\mathbf J)$ → updated baryonic state. Iterate the stellar potential, density and residual response. The response law and DF parameters are fixed; the field itself changes. Spherical residual closure and global boundary regularization are additional assumptions. This galactic branch is not the full CAMB state junction of Chapter 136 and does not recalibrate the book's cosmological sector shares.

The interface patch exposes AGAMA's existing native integration controls without changing physical formulae. Density integration uses relative tolerance $10^{-4}$ and up to $10^6$ evaluations; the stellar grid starts at $z=0.08$ kpc. Both resolutions start from archived v0.2 densities and perform five further iterations, meeting the 0.2% local criterion twice consecutively. These are warm-start convergence tests, not five iterations from an arbitrary initial state or a global convergence theorem.

### 138.2 Numerical closure and distinct density observables

| At $R=8.2$ kpc | Base grid | Refined grid |
|---|---:|---:|
| Additional iterations; recorded checks | 5; 16/16 | 5; 16/16 |
| Circular speed (km/s) | 215.56532 | 215.62089 |
| $K_z(1.1\ {\rm kpc})/(2\pi G)$ ($M_\odot/{\rm pc}^2$) | 71.82974 | 71.83659 |
| True column within $|z|\le1.1$ kpc ($M_\odot/{\rm pc}^2$) | 79.31428 | 79.31056 |
| Total midplane Poisson density ($M_\odot/{\rm pc}^3$) | 0.0790443 | 0.0790715 |

The force-equivalent surface density $K_z/(2\pi G)$ is not the integrated mass column. Cylindrical Poisson's equation retains a radial term; silently equating the two would misread the model. Displayed digits support reproduction rather than observational precision.

Across 20 probes, the maximum force change is 0.0515%; circular speeds differ by at most 0.0268% over 5–25 kpc. Total midplane density changes by 0.0344%, resolving the earlier tested grid sensitivity. Four test orbits over ten nominal periods pass energy and axial-angular-momentum checks. The maximum sampled direct-moment Jeans residual is 2.19%; approximate actions are not exact invariants. The initial finite-height circular speed 222.16 km/s changes to about 215.62 km/s because the live DF changes the initial spatial density. The old linearized rotation reference has about 5.18 km/s RMS difference over 8.25–25 kpc; that comparison is not an individual-data likelihood.

These archived numerical outputs were cross-checked against their released JSON/CSV records during book integration. This update did not rebuild AGAMA or rerun its full DF integration; the executed v0.3 source run and the book's record-level checks are separate provenance levels.

### 138.3 Actual Gaia sample and what the comparison finds

The explicit DR3 selection uses a 0.25 kpc cylinder, $G=7$–17, BP–RP=1.0–1.4, uncorrected absolute $G=5$–6, parallax S/N above 10 and RUWE below 1.4. The retrieved sample contains 90,113 stars, 72,603 with radial velocities and 48,794 after an RV-uncertainty cut below 3 km/s. The count comparison uses 79,716 stars in 17 paired-height bins over $|z|=0.15$–1.0 kpc. Two global tracer weights are fitted, with no per-bin adjustment or gravity-parameter refit.

The geometry-only fixed-DF count template does **not** reproduce the selected count profile: Poisson deviance is 1747.2021. Mass density is not automatically a star count. Extinction, luminosity/color populations, RUWE selection and Gaia/RVS completeness are not fully forward-modeled; population mapping and selection remain unverified. The discrepancy cannot yet be uniquely assigned to gravity. Reporting that discrepancy is part of the model test, not a reason to erase the actual numerical implementation.

The reflected equilibrium model predicts zero North–South asymmetry and zero vertical streaming. Separate Bennett–Bovy Gaia DR2 tables show count asymmetries reaching 9.92%. Diagonal residual sums are 1692.2282 for 31 asymmetry bins and 436.9542 for 50 velocity bins after one global velocity offset. No full covariance is supplied and no formal joint significance follows. These DR2 and direct DR3 selections are different and are not combined into one likelihood. The same symmetry limitation applies to a conventional reflected equilibrium control; this identifies a missing perturbation sector rather than a unique discrimination between gravity theories.

### 138.4 Falsification conditions and research sequence

Non-positive source density, failed force/density convergence, unacceptable grid sensitivity, invariant violation or disagreement in a population- and selection-matched observational test would challenge the relevant model claim. Current numerical closure passes the declared tests; full joint star-count/velocity validation remains open. The present selected-count template already fails its narrower sample comparison and must be improved or rejected at that scope.

First specify the tracer populations and selection function and calibrate a tracer DF against density and velocity-dispersion data. Then test a fixed calibrated model on held-out observables with the appropriate errors/covariance. If vertical waves are a target, add an explicit non-equilibrium perturbation with declared source, evolution and observational projection, and compare it under the same selection. Calibration to verified observations is legitimate construction; an unrelated independent prediction is not required to recognize a reproducible connection.

The achievements are a live WRRA-response/DF/Poisson implementation, controlled two-resolution numerical closure and an actual observational comparison exposing its present boundary. They do not establish a fully validated Galaxy model. This extends the book's galactic implementation while preserving earlier radial/RAR results at their original scope.

Sources: [wrra-galactic-disk/releases/agama-v0.3](https://github.com/Wonsik-Choi-janefather/wrra-galactic-disk/tree/3b49da87c27379e9637a53aa38e325f43808685d/releases/agama-v0.3), including `validation/summary.json`, `observations/summary.json`, the ADQL query and reproduction instructions. AGAMA source commit `f302756b8af2b763db58e278e30478517dc8eea3` plus its disclosed precision patch; original radial model commit `2528be62a70c1579308389621e75988f1f777c82`, [DOI 10.5281/zenodo.23003875](https://doi.org/10.5281/zenodo.23003875). Data credit: ESA Gaia DR3; Bennett & Bovy, arXiv:1809.03507 and `morganb-phys/VWaves-GaiaDR2` commit `203c2e111c24b99351871e562d4efe193fed586b`. Finite-height choices follow the disclosed McMillan (2017) model family; the complete McMillan model is not copied.
