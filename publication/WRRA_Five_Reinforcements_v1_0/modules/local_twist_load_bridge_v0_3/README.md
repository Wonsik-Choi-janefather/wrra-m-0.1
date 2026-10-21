# WRRA local twist/load bridge v0.3

**Wonsik Reality-Renderer Architecture**. This develops the approved interpretation of the v0.2 RAR exposure as local twist amplitude.

## Reproduce

Python 3, NumPy; Matplotlib only for the optional figure:

```sh
python3 compute.py
python3 verify.py
python3 plot.py
```

Validated with NumPy 2.3.5. Main: 61/61 checks. Independent: 5/5 checks. Counts include numerical invariants, not independent physical observations.

## Existing inputs, then new contracts

The book's native quadratic twist storage and shared D-load/aT normalization imply uD=3*aT^2/(pi*G). Define weighted twist omega=sqrt(zeta)*kappa and L0=c^2/(4*sqrt(3)*aT), giving sigma=L0*omega and sigma^2=u_twist/uD.

This is a dimensional normalization identity, not a new motion law. New source-traction coverage S_nn>=Sigma_star*gN, with Sigma_star=uD/aT, makes minimum storage reproduce the v0.2 quadratic capacity. The response port is a constitutive candidate, not ordinary matter coupling to an unobserved force.

Original countertwist energy, stiffness/twist degeneracy and RAR rotation are retained. L0 is a normalization length, not universe size or communication range. sigma is not a literal per-shutter angle.

## 3D receiver

The SAME v0.2 load cost supplies Q(Y)=2*Psi(sqrt(Y)) in an explicitly ADOPTED and CREDITED QUMOND-type two-potential receiver (Milgrom 2010, https://arxiv.org/abs/0911.5464). This is not new QUMOND mathematics or unique microscopic WRRA derivation.

A periodic positive background plus nonspherical contrast and fixed harmonic field is tested on 32^3,64^3,128^3 grids. The scalar-gradient vectors are projected; physical acceleration has the opposite sign. Preserve the mean algebraic output as a boundary convention. Nyquist planes are excluded and their loss is recorded. A 4.318148% vector correction is required; independent finite-volume solutions converge at second order.

## Scope

No new isolated-galaxy/SPARC fit, full GR/causal dynamics, universal port microphysics, dust pressure derivation or full SOURCE-to-metric completion is claimed. Bare field storage/c^2 and effective Poisson mass are numerically distinct and never counted twice. The elementary covector stress does not automatically have the old D dust pressure. The new local storage is not independently added to the old cosmic energy budget.

Original book DOI: https://doi.org/10.5281/zenodo.23516661 . Inputs are hashed in input_manifest.json. Complete CSV/JSON, central-plane arrays, independent finite-volume/mixed-action/metric checks and bilingual reports are supplied. This package has not yet been published as a new GitHub/GitBook/Zenodo release.
