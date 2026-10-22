---
title: "WRRA: A finite admission gate matching the fixed RAR"
subtitle: "Information-gravity mechanism v0.2 · Full-range reconstruction and verification"
author: "Won sik Choi · Jeongin Choi | MCC / WRRA research record"
date: "2026-10-21"
---

# 1. Verified inputs and objective

**WRRA means Wonsik Reality–Renderer Architecture.** The goal is to retain the existing RAR while constructing a finite execution/cost bridge between information load and gravitational response. Assessment follows verified inputs → WRRA transformation → outputs → falsification conditions.

The regular equilibrium candidate in v0.1 saturates at finite low-field gain and does not reproduce the fixed RAR. It is retained as a failed route, not integrated into the old gravity branch. This v0.2 uses a different construction: a gate and cost **reverse reconstructed** to match the frozen RAR, not an independent microscopic discovery of the empirical function.

Retain original shared-state D energy density, $G$, $c$, $H_0$, coefficient $1/8$, Plummer baryons and lens patch. Original code/results and v0.1 results are frozen with hashes. Empirical RAR provenance is credited. WRRA's achievement is its structure, transformation and explanation connecting this response to the same information/energy account.

$$
a_T=cH_0\sqrt{\rho_D/(8u_{\rm crit})},\qquad
 a_{T,\rm ref}=1.1917875313971119\times10^{-10}\ \mathrm{m\,s^{-2}}.
$$

# 2. WRRA transformation: least exposure and a two-state gate

Set $y=g_b/a_T$ and $x=g/a_T$. New local response variable $\sigma\ge0$ is a **dimensionless load exposure/response amplitude, not physical elapsed time**. It is distinct from SOURCE addresses, timeless allocation slots and particle species.

## 2.1 Minimum exposure covering a quadratic capacity

Explicitly adopt

$$
\min_{\sigma\ge0}\sigma\quad\text{subject to}\quad\sigma^2\ge y.
$$

Its minimizer is $\sigma_*(y)=\sqrt y$. Quadratic capacity can connect to the existing quadratic twist-stress interpretation, but this exact local capacity law is a **new constitutive assumption**, not uniquely proved by KZF or finite SOURCE cardinality. It supplies one concrete minimal-computation criterion: minimize exposure while meeting prescribed demand.

## 2.2 Finite admission

Use states unresolved U and admitted A, with $\mu(0)=0$ and column-probability generator

$$
Q=\begin{pmatrix}-1&0\\1&0\end{pmatrix},\qquad
\frac{d}{d\sigma}\begin{pmatrix}p_U\\p_A\end{pmatrix}
=Q\begin{pmatrix}p_U\\p_A\end{pmatrix}.
$$

Unit admission rate also minimizes the declared local activity cost

$$
\mathcal R(j;\mu)=j\log\frac{j}{1-\mu}-j+(1-\mu),\qquad j\ge0.
$$

For $0\le\mu<1$, the minimum is $j=1-\mu$, yielding $d\mu/d\sigma=1-\mu$. This relative activity cost is a model definition, not a proof of universal machine complexity or dissipation. Its solution is

$$
p_U=e^{-\sigma},\qquad \mu=p_A=1-e^{-\sigma}.
$$

Only two states are used. The exponential does not require infinitely many SOURCE addresses or physical events. Exposure is not time, so this is not asserted to be cosmic time evolution or autonomous thermalization.

## 2.3 Flux ownership

For the inherited spherical/local receiver, adopt $y=\mu x$. Combining the two preceding results gives

$$
\boxed{g=\frac{g_b}{1-\exp[-\sqrt{g_b/a_T}]}}.
$$

This is exactly the frozen RAR. Finite admission and least exposure construct its response, conditional on the stated capacity, rate and flux contracts. The entire function is fixed, not adjusted at one observed point. No new observational fit is performed.

Unlike the regular equilibrium candidate, this constrained minimization has an admissibility boundary at $y=0$, $\sigma=0$. Deep response has $\mu\sim x$ and $F(x)\sim x^3/3$, with vanishing stiffness at the origin. This does not relabel negative stiffness as stable: it changes the positive-linear-stiffness response class. A finite construction need not share the earlier candidate's low-field limitation.

# 3. Cost and the spatial field equation

Define load cost from the gate response $x(y)$:

$$
\Psi(y)=\int_0^y x(t)\,dt
=\int_0^{\sqrt y}\frac{2s^3}{1-e^{-s}}\,ds.
$$

At $y>0$, $\Psi'(y)=x(y)$ and $\Psi''(y)>0$. Thus the finite scalar minimization

$$
\min_{y\ge0}[\Psi(y)-xy]
$$

selects a unique $y_*(x)$. Its convex dual $F(x)=xy_*(x)-\Psi(y_*(x))$ has $F'(x)=y_*(x)$ and equals the static RAR cost reconstructed in v0.1.

$$
\mathcal E[\Phi]=\int d^3r\left[\frac{a_T^2}{4\pi G}F\!\left(\frac{|\nabla\Phi|}{a_T}\right)+\rho_b\Phi\right],
$$
$$
\nabla\!\cdot[\mu(|\nabla\Phi|/a_T)\nabla\Phi]=4\pi G\rho_b.
$$

Physical acceleration is $-\nabla\Phi$. Direct algebraic RAR equivalence holds in spherical symmetry or the specified aligned local receiver. General nonspherical galaxies require a separate three-dimensional PDE solution; none is newly validated here.

Effective residual mass $M_{\rm eff}-M_b$ is the same response in ordinary source language, not another dark mass to add after modifying the field response. The same D account fixes $a_T$ without separate observable-specific recalibration.

# 4. Finite record realization and resource boundaries

For one specified exposure, an admission bit and a blank record bit provide a four-dimensional, single-use unitary realization:

$$
|U,0\rangle\mapsto e^{-\sigma/2}|U,0\rangle+
\sqrt{1-e^{-\sigma}}|A,1\rangle.
$$

Rotate the orthogonal partner consistently and leave the other two basis states unchanged. The full map is unitary and retains gate/record ownership without copying or deleting information. Reduced record entropy $-p_U\log p_U-\mu\log\mu$ is calculated, not silently reset.

This is a **single-use finite realization for given exposure**, not a closed finite Hamiltonian producing irreversible semigroup evolution forever in physical time. Repeated execution needs owned blank records, environment, control work and reset costs. Degenerate logical energies do not establish zero total physical control cost.

Admission is a mean-response constitutive coefficient; no $g_b/0$ is assigned to an individual unresolved outcome. Mean-to-individual preparation/correlation remains open. Existing P6 preparation-dependent susceptibilities are not automatically identified with this gate.

# 5. Outputs and verification

\Needspace{15\baselineskip}

| Test | Result |
|---|---:|
| Comparison domain | $10^{-12}\le g_b/a_T\le10^4$, 801 points |
| Maximum relative fixed-RAR discrepancy | $2.22\times10^{-16}$ |
| Maximum relative inverse-map discrepancy | $4.45\times10^{-16}$ |
| Single-use unitarity error | At most $2.23\times10^{-16}$ |
| Relative convex-dual identity error | At most $8.85\times10^{-15}$ |
| Maximum relative load-cost derivative error | At most $1.01\times10^{-8}$ |
| Maximum rotation difference, 12 old states | $5.69\times10^{-14}$ km/s |
| Maximum conditional lens difference, 12 states | $1.93\times10^{-14}$ arcsec |

The reference outputs **207.5102418659 km/s** and **0.5355822400 arcsec** are recovered. Deep acceleration gives $g\sim\sqrt{a_Tg_b}$; high acceleration gives $g\sim g_b$. The regular-equilibrium candidate's finite-gain failure is removed. At the origin use the continuous extension $g(0)=0$.

All **843/843 internal checks** pass. Counts include sampled identities and cost competitors, not independent physical experiments. A separate verifier integrates the two-state ODE without inserting its exponential answer; resulting RAR differs relatively by at most $4.02\times10^{-14}$. Separate constrained minimization, adaptive cost quadrature and lens integration also pass.

Negative controls change the capacity power to 1 or 3, or double the hazard rate; each fails the original function. Quadratic capacity and fixed exposure normalization therefore matter. Changing the rate freely also changes the $a_T$ normalization and must not be hidden as another adjustment.

Function agreement and preservation of original observational diagnostics are achievements, not new observations. SPARC is not refitted and its old RMS is not recomputed as an independent result. The static field is elliptic away from the origin, but a naive unit time kinetic term gives radial stiffness above one in part of the range. Full causal metric completion is not automatic, and the old v0.1 scalar propagation speed is not transferred to this branch.

# 6. Falsification and the remaining physical idea

Revise the construction if the fixed function or twelve shared states fail replay; probabilities, record ownership or unitarity fail; cost derivatives/minimality fail; effective residuals are counted twice; or observations disagree with the fixed connection. Changing preparation, units or coefficients separately for each observable changes the model.

**Resolved here:** numerical/function mismatch between the v0.1 candidate and the fixed RAR. A finite-state, constrained-cost construction with the same WRRA energy normalization reproduces the original macroscopic branch.

**Remaining physical connection:** why local WRRA capacity is exactly $\sigma^2$ and why exposure has the unit-hazard admission law. Presently $\sigma$ is the minimum response amplitude covering local demand. Mapping it to actual twist amplitude, unresolved-residue accumulation or another retained quantity needs additional structure. Quadratic stress is a promising interpretation, not a completed integer-SOURCE derivation of this local law.

The conclusion is a **conditional finite execution/cost structure matching the frozen RAR**, not the completed cause of all gravity or a unique microscopic realization.

# 7. Sources and reproduction

Baseline MCC 3.0 v0.27-r1: DOI **10.5281/zenodo.23516661**. Shared states and RAR code: `mcc_3_0/theory_completion/step_6_shared_gravity`, `mcc_3_0/stage_5_macro_universe_replay`. v0.1 results are included as failed-route comparisons. Repository: <https://github.com/Wonsik-Choi-janefather/wrra-m-0.1>.

No new public release or DOI is assigned to this package. Run `python3 compute.py` with Python 3 and NumPy; run `python3 verify.py` with SciPy also installed. Frozen inputs/hashes, full-domain CSVs, twelve-state replay, negative controls, result JSON and bilingual reports are included.
