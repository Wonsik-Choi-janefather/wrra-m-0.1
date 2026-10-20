---
title: "WRRA Full-State Junction: Development Audit v0.7-dev-r1"
author: "Won sik Choi · Jeongin Choi"
date: "2026-10-20"
---

## 1. Verified inputs

The frozen inputs are the 64 evolved v0.4 modes with 13 neutrino moments,
the v0.5 finite-packet clock with 256 reservoir partitions, and the v0.6
massive-electron thermal completion. The original 128-cell seed is used
without amplitude refitting. The inherited WRRA dark-weight-only target is
$\omega_c=0.12037806177378$. This target and known physical constants
are explicitly declared calibration inputs.

## 2. WRRA transformations

The complete available scalar state of each v0.4 mode is transformed into
the post-exchange CDM-comoving synchronous frame. Density, velocity, metric
derivatives and the neutrino monopole/dipole are transformed together.
The r1 adapter also stores the small metric derivative combination directly
to prevent cancellation loss. Separately, the seed-dependent event-time motion of v0.5 is included in the
v0.6 thermal equations through a common-time saltation tangent. These two
validated calculations still describe different source models. They are
not represented as a single completed finite-k integration.

## 3. Computed outputs

| Quantity | Result |
|:---|---:|
| Maximum transformed Hamiltonian constraint residual | $3.29\times10^{-16}$ |
| Maximum momentum constraint residual | $4.31\times10^{-16}$ |
| Maximum absolute entropy gauge-invariance error | $<1.12\times10^{-16}$ |
| Finite-packet thermal $k=0$ entropy response | 0.194818034056 |
| Earlier smooth-source response | 0.723567385056 |
| Original-seed entropy RMS under the new local tangent | $4.80263\times10^{-9}$ |
| Thermally normalized packet $\omega_c$ at old $\beta$ | 0.103663511129 |
| Relative discrepancy against inherited late target | -13.885047% |
| Recalibrated conversion fraction $\beta$ | $8.85389093544\times10^{-7}$ |
| Change in conversion fraction | +16.123841% |

The old packet normalization produces about 13.9% less present dark matter
than the inherited downstream input. This is a junction normalization
discrepancy, not an observational exclusion of the WRRA structure.
Recalibration yields $\omega_c=0.120378062005$.
This is legitimate background calibration, not an independent density
prediction. The 64 finite-k modes have not yet been rerun on that new background.

## 4. Falsification and checks

Both Einstein constraints, inverse transformation, entropy invariance and
retention of high neutrino moments are tested mode by mode. Simply deleting
the CDM velocity violates the momentum constraint by about 1.47%.
Omitting event-time motion incorrectly gives zero response for this model.

Independent central differences of nonlinear histories agree with the
saltation entropy tangent to at most $2.68\times10^{-7}$ relatively.
Simultaneously refined EOS grid, quadrature and time tolerance change the
response by $1.39\times10^{-12}$ relatively. Energy-plus-pressure-work
residuals remain below $3.11\times10^{-11}$ and $2.53\times10^{-12}$
for the base and refined runs. All 472 acceptance checks pass.

The derivative is valid only on the fixed-count open branch
$-0.00281226035<\xi<0.00845879466$. All original 128 cells lie inside it.
These checks establish the stated numerical transformations, not an
observational validation of a completed cosmology.

## 5. Conclusion and remaining junction

**Step 4 remains partially implemented.** Executed advances are the conserving
64-mode frame transformation, local thermal/event-time tangent and background
recalibration. No new CMB spectrum or lensing likelihood is calculated here.

A genuine next integration must specify the finite-k energy/momentum transfer
across each event hypersurface; complete baryon/electron and massive-neutrino
distribution states; rerun modes on the recalibrated thermal background; and
declare the three-dimensional/angular covariance of the finite seed.
The first two requirements cannot be supplied by rearranging arrays.
An angular completion can be a declared conditional model, but none is
introduced here. Exporting these partial states as complete CAMB initial
conditions raises an explicit error listing the unmet physical requirements.

\newpage

## Equations and conventions

For $y=(N,\ln T_\gamma,M,W)$ and $N=\ln a_{\rm rel}$,
$C$ is constant between events. The background equations are

$$\rho=\rho_{\rm EM}(T)+\rho_{\nu,i}e^{-4N}+Ce^{-4N}+Me^{-3N},$$
$$\dot N=H,\qquad
\dot{\ln T}=-\frac{3H(\rho_{\rm EM}+p_{\rm EM})}{T\partial_T\rho_{\rm EM}},
\qquad \dot M=0.$$

Dots in the implemented ODE use the inherited dimensionless time. The finite
electron mass, thermal Fermi integrals, effective $N_{\rm eff}=3.044$ input,
and instantaneous relativistic neutrino decoupling branch are inherited from
v0.6. This is not a collision-integral calculation or a BBN yield prediction.

At event $j$, with $q=\beta\rho_i/256$ and $\epsilon=0.01$,

$$C^+=C^--q,\quad M^+=M^-+(1-\epsilon)qe^{-N},\quad
\rho_{\rm EM}(T^+)=\rho_{\rm EM}(T^-)+\epsilon qe^{-4N}.$$

The rate modulation is the original seed $\xi$, with no amplitude refit.
In the fixed-count neighborhood $t_j(\xi)=t_j(0)/(1+\xi)$.
For the common-time tangent $z=\partial y/\partial\xi$, the reset is

$$z^+=DR\,z^-+(DR\,f^--f^+)t'_j,\qquad t'_j=-t_j/(1+\xi).$$

Between events $\dot z=(\partial f/\partial y)z$. The last term above is
essential. Merely differentiating the state reset loses the entire response
in this autonomous fixed-packet model. On the final common proper-time slice,

$$S_{m,{\rm EM}}=\frac{z_M}{M}-3z_N-
\frac{\partial_{\ln T}\rho_{\rm EM}}{\rho_{\rm EM}+p_{\rm EM}}z_{\ln T}.$$

This expression is a $k=0$ tangent of local cells. It supplies no new
finite-gradient radiation or momentum source.

For the *separate frozen v0.4 smooth-source states*, a residual synchronous
transformation into the post-exchange CDM frame is

$$\alpha=\theta_m/k^2,\quad \theta_i^{c}=\theta_i-k^2\alpha,\quad
\delta_i^c=\delta_i+3(1+w_i){\cal H}\alpha,\quad
\eta^c=\eta+{\cal H}\alpha.$$

Here $\alpha'=-{\cal H}\alpha$ after exchange. The implementation also
transforms $h'$ and $\eta'$, with
$\eta^{c\prime}=\eta'+({\cal H}'-{\cal H}^2)\alpha$ and
$h^{c\prime}=h'+2k^2\alpha-6({\cal H}'-{\cal H}^2)\alpha$.
The neutrino monopole and dipole change; all retained moments $\ell\ge2$
remain intact. CAMB conventions are $\mathrm{etak}=k\eta$,
$q_\gamma=4\theta_\gamma/(3k)$, and $q_\nu=F_{\nu1}$.
The adapter exports a partial native variable dictionary, not a complete
CAMB evolution array. No metric $h$ is invented from an unspecified spatial
gauge integration constant.

## Release revalidation and numerical correction

Ten supplementary release checks pass in addition to the 472 base checks.
The independent clock coordinate $u=(1+\xi)t$ keeps events fixed and integrates
$w'=Jw-f$, $w^+=DRw^-$; the final derivative is $z=w+t_{\rm end}f$.
It recovers the entropy response within relative $8.39\times10^{-9}$.
A five-point numerical flow Jacobian agrees within $1.78\times10^{-10}$.

Reconstructing $h'+6\eta'$ from its separately rounded transformed terms
causes up to 16.66% error in the small Bardeen potential at the lowest mode.
The r1 adapter therefore retains the combination directly as
$h'+6\eta'=2k^2(g/2+\alpha)$, using the inherited scaled shear $g$.
The Bardeen potential computed from this stable combination is gauge-invariant
within relative $4.35\times10^{-12}$ over all 64 modes. The lossy reconstruction
is kept as a negative control. Separate derivative components are diagnostics;
they must not be used to recover this small difference. A future actual CAMB
transport must also verify stable constraint evaluation; this release does not
claim to have performed that transport.

The original entropy response, target calibration and 472 base checks are
unchanged. An independent SI-unit reconstruction yields
$\omega_c=0.103663511046343$, consistent with the thermal-density calculation.

## Sources and reproducibility

- WRRA v0.4: DOI [10.5281/zenodo.23490141](https://doi.org/10.5281/zenodo.23490141).
- WRRA v0.5: DOI [10.5281/zenodo.23491041](https://doi.org/10.5281/zenodo.23491041).
- WRRA v0.6: DOI [10.5281/zenodo.23491673](https://doi.org/10.5281/zenodo.23491673).
- Ma and Bertschinger (1995), [astro-ph/9506072](https://arxiv.org/abs/astro-ph/9506072): scalar gauge and Einstein-Boltzmann conventions.
- CAMB 2.0.4 pristine local source, `fortran/equations.f90`: native variable conventions; scalar initial-state assignment and constraint equations. This artifact does not modify or run CAMB.
- CODATA constants through SciPy 1.17.0; the same finite-mass electromagnetic EOS code as the frozen v0.6 input.

Run `python run_all.py` with the pinned requirements. The bundle includes
all inputs used here, scripts, machine-readable outputs, checks and hashes.
The original v0.4/v0.5/v0.6 publications remain unchanged.
Release DOI: [10.5281/zenodo.23492328](https://doi.org/10.5281/zenodo.23492328).
No new CMB or lensing result is claimed.
