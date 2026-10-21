---
title: "WRRA: Local twist amplitude and gravitational load"
subtitle: "Local twist-load bridge v0.3 · Units, traction and a 3D receiver"
author: "Won sik Choi · Jeongin Choi | MCC / WRRA research record"
date: "2026-10-21"
---

# 1. Verified inputs and advance

**WRRA means Wonsik Reality–Renderer Architecture.** This work connects the RAR-matching exposure $\sigma$ of v0.2 to a local twist amplitude. Assessment follows verified inputs → WRRA transformation → outputs → falsification conditions.

MCC 3.0 v0.27-r1 Chapters 21–23 provide countertwist, quadratic storage, mass phenotype and the static response. Original shared D energy and v0.2 gate results are frozen. SOURCE addresses, timeless allocation slots and numerical spatial cells remain distinct.

Three advances are executed: SI interpretation of $\sigma$ using the existing energy law; an explicit traction/source-load version of the capacity contract; and a three-dimensional test using the same gate cost in an adopted QUMOND receiver. This is not a new observational fit or complete relativistic theory.

# 2. WRRA transformation I: dimensions and normalization

The inherited storage and same-state acceleration calibration are

$$
u_T=\frac{\zeta c^4\kappa^2}{16\pi G},\qquad
 a_T=cH_0\sqrt{\frac{u_D}{8u_{\rm crit}}},\qquad
 u_{\rm crit}=\frac{3H_0^2c^2}{8\pi G}.
$$

Here $u_D$ denotes the original D energy density. Combining these equations gives

$$
u_D=\frac{3a_T^2}{\pi G}.
$$

Keep stiffness $\zeta$ and absolute twist rate $\kappa$ unseparated; use their **stiffness-weighted twist** combination:

$$
\omega=\sqrt\zeta\,\kappa,\qquad
\omega_D=\frac{4\sqrt3\,a_T}{c^2},\qquad
L_0=\omega_D^{-1},\qquad
\boxed{\sigma=L_0\omega,\quad\sigma^2=u_T/u_D.}
$$

The last relation is a normalization identity consistent with the inherited quadratic storage, not by itself a new dynamical prediction. Reference values:

| Quantity | Value |
|---|---:|
| $u_D$ | $2.0321854301\times10^{-10}$ J/m³ |
| $a_T$ | $1.1917875314\times10^{-10}$ m/s² |
| $\omega_D$ | $9.1870916799\times10^{-27}$ $\mathrm{m}^{-1}$ |
| $L_0$ | $1.0884837496\times10^{26}$ m |

$L_0$ normalizes amplitude; it is not universe size, actual contact range or instantaneous communication length. Rescaling stiffness and inversely rescaling $\kappa$ preserves $\omega$ and outputs. The original stiffness/twist degeneracy is not closed by an arbitrary numerical choice.

# 3. WRRA transformation II: least storage and source traction

For a local weighted twist covector along normal $n$, varying the quadratic energy at fixed covector gives the **candidate stress witness**

$$
S_{ij}=\frac{c^4}{16\pi G}(2\omega_i\omega_j-|\omega|^2\delta_{ij}),\qquad S_{nn}=u_T.
$$

This is checked by independent metric differentiation. It is a unit/traction witness for the simple quadratic model, not a complete universal stress tensor.

Define reference column load

$$
\Sigma_\star=\frac{u_D}{a_T}=\frac{3a_T}{\pi G}
=1.7051574853\ \mathrm{kg/m^2},
$$

and adopt the **new source-traction contract**

$$
\min u_T\quad\text{subject to}\quad S_{nn}\ge\Sigma_\star g_N.
$$

$g_N$ is the auxiliary Newtonian source-field magnitude. $\Sigma_\star$ normalizes a response port, not a measured stellar/gas surface density or another particle component. Ordinary matter is not assumed to feel this auxiliary field instead of the total field.

At the minimum, $u_T=\Sigma_\star g_N$, hence

$$
\sigma^2=\frac{u_T}{u_D}=\frac{g_N}{a_T}.
$$

The v0.2 capacity law now has a same-energy/traction representation: least twist storage covering source demand. Autonomous emergence of such a port and coupling from SOURCE is not proved. Replacing source magnitude $g_N$ with total $g$ would define a different law. Unit admission $\mu=1-e^{-\sigma}$ remains an explicit construction assumption.

Countertwist retains $\kappa^2=\kappa_+^2+\kappa_-^2$. Changing directional bias at fixed squared sum preserves storage and normal traction, as tested. Thus small net directional bias can coexist with stored response.

# 4. A 3D receiver using the same cost

The v0.2 load cost was $\Psi(y)=\int_0^y t/[1-e^{-\sqrt t}]\,dt$. With auxiliary potential $\Phi_N$, put $Y=|\nabla\Phi_N|^2/a_T^2$. Then

$$
\mathcal Q(Y)=2\Psi(\sqrt Y),\qquad
\mathcal Q'(Y)=\nu(\sqrt Y),\qquad
\nu(y)=\frac1{1-e^{-\sqrt y}}.
$$

Use this cost in Milgrom's **existing QUMOND mathematics** as an explicitly adopted nonrelativistic receiver [2]:

$$
\mathscr S_{\rm stat}=-\int d^3x\left[\frac{2\nabla\Phi\!\cdot\!\nabla\Phi_N-a_T^2\mathcal Q(Y)}{8\pi G}+\rho_b\Phi\right].
$$

The two variations yield

$$
\nabla^2\Phi_N=4\pi G\rho_b,\qquad
\nabla^2\Phi=\nabla\!\cdot[\nu(|\nabla\Phi_N|/a_T)\nabla\Phi_N].
$$

This is a stationary saddle functional, not a positive global energy minimum. It recovers the old RAR in spherical symmetry and differs from AQUAL for general nonspherical systems. Receiver selection is not a unique WRRA microscopic derivation.

In general, $\nu\nabla\Phi_N$ need not be curl-free. We calculate its irrotational component while preserving divergence, rather than call the algebraic vector a potential gradient. Finite Fourier orthogonal projection is also a least-squares correction. The receiver is actually executed internally, but this candidate connection is not called complete GR integration.

## 4.1 Executed boundary conditions

Resolutions $32^3$, $64^3$, $128^3$ use a smooth nonspherical periodic density contrast. Adding the declared positive reference background keeps total density positive; the Poisson problem uses the mean-subtracted contrast. The 16 kpc side is a test-box choice, not SOURCE cardinality or universe size. An auxiliary harmonic field is prescribed; the output retains the mean algebraic response as its boundary convention. This is not an isolated-galaxy/SPARC fit.

Nyquist planes of the real even grid are excluded from the admitted band. Maximum relative loss is approximately $1.38\times10^{-12}$ and falls to roundoff with refinement. Projection checks concern this band.

# 5. Outputs, independent checks and ownership

The reference spherical calculation retains **207.5102418659 km/s**. The nonspherical algebraic response has curl. Its potential-field correction is **4.318148%** in relative vector $L^2$ norm, a geometric result of this declared test, not a measured galaxy residual.

\Needspace{11\baselineskip}

| Check | Result |
|---|---:|
| Spectral output curl RMS | At most $5.59\times10^{-15}$ |
| Relative divergence discrepancy | At most $3.01\times10^{-14}$ |
| Independent finite-volume convergence orders | 1.99931, 1.99983 |
| Two mixed-action directional derivative errors | At most $3.34\times10^{-11}$ |
| Quadratic-storage metric derivative error | At most $2.04\times10^{-11}$ |
| Main / independent internal checks | 61/61, 5/5 pass |

Counts are not independent physical observations. An independent staggered finite-volume Poisson calculation converges to the spectral result at second order.

\Needspace{18\baselineskip}

![](three_dimensional_receiver.png){width=100%}

*Prescribed source field, curl from direct scaling, and required potential correction. This is a periodic diagnostic, not observed data or an isolated galaxy.*

A weighted connection $\boldsymbol\omega=\omega_D\sqrt{|\nabla\Phi_N|/a_T}\,n$, oriented with the source gradient, passes a loop/Stokes test. The weighted circulation in the 16 kpc box is approximately $-1.3110\times10^{-9}$. This candidate need not be the exact differential of one global scalar phase. It is not measured cosmic topology or non-Abelian holonomy. Identifying $\sigma$ with a literal single-shutter rotation fails: the conditional microscopic edge's weighted angle is approximately $3.79\times10^{-39}$ rad, a different quantity.

\Needspace{10\baselineskip}

## 5.1 Stored energy versus mass phenotype

At the 8.2 kpc reference point, $\sigma=0.92973206$ and $u_T=1.75662\times10^{-10}$ J/m³. But

$$
u_T/c^2=1.95451\times10^{-27}\ \mathrm{kg/m^3},\qquad
\rho_{\rm eff}=5.12098\times10^{-22}\ \mathrm{kg/m^3},
$$

which differ by approximately $2.62009\times10^5$. The former converts stored field energy to mass; the latter expresses the modified response as a standard-Poisson residual. Adding only the former as minimally coupled GR matter would fail to recover the response. Here the receiver variation produces the latter; the two are not added twice.

The simple fixed-covector stress averages isotropically to $-u_TI/3$, unlike the existing D dust pressure. Thus this local norm alone does not derive the cosmic pressure law. Existing D and local storage are not simultaneously added as separate cosmic components; dynamics, transfer and metric completion must determine their relationship.

# 6. Falsification and conclusion

Revise the connection if source/units/normalization/normal traction fail; source and total fields are interchanged; storage and effective mass are equated or double-counted; or 3D divergence, curl and convergence fail. Observational comparison must fix sources, boundaries, gate and coefficients first.

**Conclusion:** $\sigma$ is made explicit as stiffness-weighted local twist normalized by the existing D account. Minimum traction coverage and a 3D receiver using the same cost are executed. Remaining structures are the physical source-loaded port, unit-rate admission dynamics and complete metric matching to the D pressure law. The advance exceeds a rename without claiming those remaining links are solved.

\Needspace{15\baselineskip}

# 7. Sources and reproduction

[1] MCC 3.0 v0.27-r1, Chapters 21–23. DOI **10.5281/zenodo.23516661**. Original excerpt, shared state and v0.2 results are frozen with hashes.

[2] M. Milgrom, *Quasi-linear formulation of MOND*, MNRAS 403, 886 (2010), <https://arxiv.org/abs/0911.5464>, DOI **10.1111/j.1365-2966.2009.16184.x**. Credited as adopted receiver mathematics.

With Python 3 and NumPy run `python3 compute.py`, then `python3 verify.py`. Rebuild the plot with Matplotlib using `python3 plot.py`. No new public release/DOI is assigned. Repository: <https://github.com/Wonsik-Choi-janefather/wrra-m-0.1>.
