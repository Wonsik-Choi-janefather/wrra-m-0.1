---
title: 'WRRA Freedom Ledger and Joint Falsification Conditions'
subtitle: 'Research item 5 | Calibration, state space and model choices | v0.1'
author: 'Won sik Choi · Jeongin Choi'
date: '21 October 2026 | Scoped calculation and verification'
lang: en
---

**WRRA = Wonsik Reality-Renderer Architecture.** Audit the book's reference calibration chain, recent shared-gravity/zeta modules and inherited CMB settings. This is not an exhaustive free-parameter census of all 138 chapters. Calibration to observations is legitimate. Numerical novelty or exclusive predictions are not requirements. Record explanatory reproduction and conditional predictions computed through WRRA transformations after inputs are fixed.

## 1. Verified inputs

Inspect and freeze the v0.27-r1 calibration table, shared-gravity outputs, finite RAR gate contract, zeta physical readout v0.1 and symmetry/drive v0.2 outputs. Inspect actual CMB settings in the original `run_camb.py`. There are zero new observational fits. Sensitivity grids, injected discrepancies and parameter-recovery examples are generated diagnostics. No new SPARC-residual replay is claimed.

The registry contains 30 entries with values, roles, dependencies and potential continuous coordinates if released. Inputs and derived coefficients on the same dependency chain are not counted twice.

| Entry | Independence and present role |
|---|---|
| Address shares 0.05/0.268/0.682 | Three normalized values, two independent components |
| Address calibration $\alpha,h$ | Two coordinates calibrated to those targets; not two additional target freedoms |
| SI energy shares 0.0493/0.265/0.6857 | Separate ledger from address shares; two components |
| $H_0=67.4$ km/s/Mpc | One inherited Planck reference anchor |
| $u_{\rm crit}$ and three $\eta_s$ | Derived by $u_{\rm crit}=3H_0^2c^2/(8\pi G)$ and $\eta_s=u_{\rm crit}F_s/\mu_s^{\rm ref}$ |
| $N_U=500\times29\times70$ | Finite construction output; constituent choices/provenance retained |
| $\xi$, sector-load slopes, $1/8$ | Fixed constitutive rules; fixed does not imply derived |
| Shutter and edge | Inherited calibration $\tau$; derived $d=c\tau$ |
| $A_s,n_s,\tau_{\rm reio}$ | Supplied to CMB code as $2.1\times10^{-9}$, 0.9649, 0.0544 |
| Neutrinos and CMB temperature | Supplied $m_\nu=0.06$ eV, $N_{\rm eff}=3.044$, $T=2.7255$ K |

The reference address/energy normalization chain has $2+2+1=5$ independent anchor components. This is an **input-coordinate dimension for that chain**, not the whole theory's fitted-parameter count or five statistically independent measurements. It excludes the shutter calibration, other constitutive/discrete choices, CMB spectral inputs, source descriptions and observational nuisance parameters.

\Needspace{10\baselineskip}
Planck's base ΛCDM has six cosmological parameters [3], but comparing that six with this five would not establish fewer WRRA parameters. Match data, observables, initial conditions, nuisance parameters and likelihood scope first. No matched likelihood, AIC or BIC comparison is performed here. Permit both theories to use known-value calibration under the same accounting rules.

## 2. WRRA transformation: distinguish states from fitting freedoms

An unrestricted normalized 70-branch pure combining ray has $2C-2=138$ real dimensions after removing global phase. The existing branch-blind single-port contract leaves no new adjustable combining coordinates. The 70 zero heights are fixed mathematical inputs, rather than 70 currently fitted observational parameters.

A general pure state in 128 dimensions has 254 real coordinates; a general density matrix has interior dimension 16,383. These are possible state-space dimensions. They are not all fitting parameters unless independently adjusted against observations. Conversely, changing states, sector coefficients or branch weights for each galaxy/output adds estimation freedom and must be recorded. Apply this same distinction to other quantum/cosmological models.

## 3. WRRA transformation and output A: four symbols, one gravity response

Release the earlier gate's unit-hazard normalization as $\lambda_h$. The current local response is

$$g=\frac{g_b}{1-e^{-\sqrt{g_b/a_{\rm eff}}}},\qquad
 a_{\rm eff}=\frac{cH_0\sqrt{\kappa f_D}}{\lambda_h^2},
\quad\kappa=1/8,\ f_D=u_D/u_{\rm crit}.$$

Consequently,

$$d\log a_{\rm eff}=d\log H_0+\tfrac12d\log\kappa
+\tfrac12d\log f_D-2d\log\lambda_h.$$

On a 201-point acceleration diagnostic grid, the four-coordinate response Jacobian has **rank one**, with three exact null directions also checked. Local rotation alone cannot determine all four coordinates separately. No new $a_{\rm eff}$ fit is applied to the frozen reference.

If SI density $u_D$ is the independent input, $H_0$ cancels:

$$a_{\rm eff}^2=\frac{8\pi G\kappa u_D}{3\lambda_h^4}.$$

Counting $H_0$ as another independent local-response adjustment at fixed $u_D$ would be redundant. For the same frozen Plummer source, lens patch and weak-field receiver $\Phi=\Psi$, one acceleration determines both rotation and conditional lensing.

| Joint reference output | Value |
|---|---:|
| $a_{\rm eff}$ | $1.191787531397112\times10^{-10}\,\mathrm{m\,s^{-2}}$ |
| Rotation at 8.2 kpc | 207.510241866 km/s |
| Conditional lens angle | 0.535582240009 arcsec |

A **generated diagnostic** keeps rotation fixed and raises lensing alone by 2%. Rotation requires $\log(a_{\rm eff}/a_0)=0$, whereas lensing requires 0.0521822. Both cannot be reproduced with one acceleration under those same inputs. Adding a separate lens correction or gravitational slip is a declared model extension, not an unchanged one-parameter explanation. No actual observed 2% mismatch is asserted.

\Needspace{17\baselineskip}
## 4. WRRA transformation and output B: a remaining zeta constraint

For fixed preparation let $P$ denote total selected probability, $B$ selected in-band probability, and $E$ probability-weighted selected-port energy. Declare a common, energy-independent detection efficiency $\epsilon$. Total probability and energy include the selected high-frequency complementary channel; this requires a corresponding readout, rather than assuming one band-only detector measures all three quantities. Even allowing coherence $\eta$ as a second nuisance coordinate,

$$\boldsymbol y=\epsilon[\boldsymbol b+\eta(\boldsymbol c-\boldsymbol b)],
\qquad\boldsymbol y=(P,B,E/(\hbar/\tau)).$$

Here $\boldsymbol c$ and $\boldsymbol b$ are frozen coherent and completely dephased outputs. The three readouts remain in a plane. Define $q=B/P$ and $\bar E=E/P$ to eliminate efficiency. Coefficients below follow algebraically from the existing outputs, without linear-regression fitting.

| Fixed preparation | Joint WRRA readout, energy in keV |
|---|---|
| Uniform | $\bar E=1519.626252-675.466754\,q$ |
| Inherited alpha | $\bar E=1507.317730-621.543517\,q$ |

These are conditional WRRA predictions for the stated preparation, calibration, band, noise and detector. Exclusivity to WRRA is unnecessary. Once the first two readouts determine common efficiency and coherence, the third energy readout has no separate fitting coordinate. Across 101 coherence values the maximum relation error is $1.64\times10^{-11}$ keV, a numerical error rather than achievable experimental precision.

A synthetic $\eta=0.6$, $\epsilon=0.8$ example recovers both coordinates and reproduces the third output. A 1% energy-only perturbation violates the constraint. This is an implementation diagnostic, not observational fitting.

**Identifiability does not imply easy measurement.** The stated dimensionless readout matrix has condition number about 73.9 for uniform preparation and 2167.5 for inherited alpha. With ideal independent count statistics, jointly estimating efficiency/coherence from two count readouts at that synthetic point gives local Fisher lower-bound trial counts of roughly $1.28\times10^6$ and $1.07\times10^8$ for coherence standard error 0.1. This excludes apparatus systematics and additional energy information. It is a design estimate, not a performance guarantee or measured significance.

\Needspace{18\baselineskip}
![](joint_constraints.png){width=100%}

*Left: rotation–conditional-lensing curve from one shared acceleration, plus an intentionally inconsistent synthetic point. Right: zeta joint readout relations surviving common efficiency and coherence nuisance freedom. Neither panel shows observational data.*

\Needspace{20\baselineskip}
## 5. Falsification and revision rules

1. If the same source/receiver requires different accelerations for rotation and lensing, revise the current shared-gravity model. Changes to source, distance, uncertainty or slip belong in a declared calibration branch.
2. After fixing preparation, energy scale and band, and checking the common-efficiency and noise assumptions, failure of the plane/line relation revises the current zeta instrument. Energy-dependent efficiency or different noise defines another model.
3. Counting derived coefficients twice, or changing states/coefficients by output while reporting one fixed model, fails the ledger. Legitimate observation-driven revisions remain allowed: record changed inputs, fit dimension, objective and all resulting shared outputs.

## 6. Assessment

Thirty main checks and 88 separate checks pass. Separate checks use analytic sensitivity, independent adaptive lens integration, determinant constraints and conditional count information. These are numerical checks, not counts of independent observations.

**This stage replaces a claim of few parameters with an explicit dependency ledger and joint constraints that remain after allowed adjustments.** It fixes calibration redundancy, three local-gravity null directions and a zeta relation that common efficiency/coherence cannot absorb. Assess consistency by applying the same calibrated WRRA rule to several outputs. Assess originality through that structure and transformation. No whole-model parameter advantage over ΛCDM or new observational success is claimed by this calculation.

Reproduce with `registry.py`, `compute.py`, `verify.py`, `plot.py`. The 30-entry ledger, input hashes, fixed-model/revision rules, sensitivity matrix, CSV/JSON and bilingual reports are included. This is not yet a new GitHub, GitBook or Zenodo release.

Sources: [1] MCC 3.0 v0.27-r1, https://doi.org/10.5281/zenodo.23516661 and frozen subsequent computations. [2] McGaugh, Lelli, Schombert (2016), inherited empirical RAR function, https://arxiv.org/abs/1609.05917 . [3] Planck Collaboration, base six-parameter model and reference $H_0$, https://arxiv.org/abs/1807.06209 .
