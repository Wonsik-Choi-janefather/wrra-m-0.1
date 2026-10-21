---
title: "WRRA: A finite discrete-to-continuum bridge"
subtitle: "Finite-scale bridge v0.1 · Derivation and computation"
author: "Won sik Choi · Jeongin Choi | MCC / WRRA research record"
date: "2026-10-21"
---

# 1. Registered definitions and result

WRRA means **Wonsik Reality–Renderer Architecture**. This calculation retains the spatial and transport definitions in registered MCC 3.0 v0.27-r1. It addresses task 1: conserved quantities, resolution errors and scaling conditions between finite discrete representations and macroscopic continuum equations.

Assessment follows **fixed inputs → WRRA transformation → outputs → falsification conditions**. We reconstruct the existing SOURCE energy output and coarse-grain it, then apply a declared weak-field receiver to measure representation error. This includes a direct application to the actual WRRA energy output, alongside a separate numerical witness.

**Results:** maximum relative sector-energy averaging error $3.933\times10^{-16}$; maximum relative discrepancy between averaging before and after spectral transport $5.343\times10^{-16}$; approximately second-order potential convergence for the actual source receiver and a separate three-dimensional witness. All 179 internal checks passed. An independent modal calculation cross-checked the three-dimensional error values. The check count is not a count of preregistered independent experiments or observational tests.

# 2. Inputs, types and units

| Object | Registered definition / use here |
|---|---|
| SOURCE | 1,015,000 address labels; address 1 inactive |
| Internal slots | 128; distinct from physical cells |
| Original profiles | 1,024 samples; both weighting branches |
| Spatial renderer | Conditional $500\times29\times70$ periodic graph |
| Inherited transport | FFT implementation of $H=\hbar c|k|$; spatially nonlocal |
| Microscopic scales | $\Delta t=1.4813019664\times10^{-21}$ s; $d=c\Delta t$ |
| Macroscopic anchor | $k_1=0.05\ \mathrm{Mpc}^{-1}$; retained as calibrated input |
| Receiver witness | Unit periodic length; dimensionless $4\pi G\rho_0=1$ |

Addresses, internal slots and profile samples are not identified with one physical grid. The one-dimensional profile calculation tests the existing periodic representation; it does not prove that SOURCE addresses form one-dimensional physical space. The $N^3$ receiver family changes numerical resolution, not SOURCE cardinality.

Original `positive_profile_and_payload.npz` SHA-256:

`1aa16e3b048b3d54457924584d79793fc6cd28cee5f1880cf337e3ff35e1f602`

We retain frozen $B_{srj}$, $\eta_s$, $\epsilon=10^{-8}$ and $g_*=2\cos(\pi/8)$. No new observational fit parameter is optimized. Witness period, time, resolution and tolerances are numerical settings, not replacements for the original physical anchors.

# 3. Transformation and conservation

The inherited positive kernel with $p=2,3,5$ is replayed:

$$
D_p(r,x)=\frac1p\sum_{a=0}^{p-1}e^{2\pi i a((r\bmod p)/p-x)},\qquad
K_r(x)=\frac{\prod_{p=2,3,5}|1-D_p(r,x)|^2}{\langle\prod_{p=2,3,5}|1-D_p(r,x)|^2\rangle}.
$$

$$
C_{sr}=\sum_jB_{srj},\qquad S_s(x)=\sum_rC_{sr}K_r(x).
$$

Information $I=\sum_sS_s$ is not substituted directly for mass density. We retain the existing energy-supply map:

$$
\delta u_s(x)=\epsilon\eta_sg_*\sum_{r:\,r\bmod3\ne0}C_{sr}[K_r(x)-1],\qquad\delta u_P=0,
$$
$$
u_s(x)=\eta_s\langle S_s\rangle+\delta u_s(x),\qquad p(x)=-u_R(x).
$$

The resulting density-contrast RMS is $7.46947\times10^{-9}$ for the weighted branch and $7.51209\times10^{-9}$ for the unweighted branch, distinct from the information-contrast RMS of approximately 0.4133.

Define block averaging by

$$
(\mathcal A_bf)_J=\frac1b\sum_{a=0}^{b-1}f_{bJ+a},\qquad h_c=bh.
$$

Then $h_c\sum_J\mathcal A_bu_s=h\sum_ju_s$; positivity and $\mathcal A_bp=-\mathcal A_bu_R$ are preserved. The finite-volume continuity identity also survives by telescoping boundary fluxes. The flux $J(x)$ used to test that identity is a declared test function; it is not a new microscopic SOURCE equation of motion.

The original kernel has nonconstant support $|m|\le7$. Its exact point-sample box transfer is

$$
H_b(m)=\frac1b\sum_{a=0}^{b-1}e^{2\pi i ma/1024}.
$$

At least 16 coarse samples retain this band without aliasing. Eight samples do not and are explicitly flagged unsafe. Box averaging is not an ideal anti-alias filter. We executed inherited spectral evolution $U(t)=e^{-ic|k|t}$ and compared average-then-evolve with evolve-then-average, at $t=0.137L/c$. For a common period and retained band they commute to floating-point precision. Information $I$ is supplied as a complex test amplitude for the operator audit, not redefined as mass or a normalized physical quantum state.

# 4. Finite-resolution bounds

The following local operator is an **adopted receiver for measuring scale error**. It does not replace the registered nonlocal spectral dynamics:

$$
(L_h\phi)_{\boldsymbol j}=\sum_{a=1}^3\frac{\phi_{\boldsymbol j+e_a}-2\phi_{\boldsymbol j}+\phi_{\boldsymbol j-e_a}}{h^2},
\qquad \lambda_h(\boldsymbol k)=\frac4{h^2}\sum_a\sin^2(k_ah/2).
$$

Periodic summation by parts gives $-\langle\phi,L_h\phi\rangle=\sum_a\langle|(\phi_{j+e_a}-\phi_j)/h|^2\rangle$. A discrete gradient-energy functional with a linear $+\delta\rho\phi$ term has stationarity condition $L_h\phi=\delta\rho$. This is a variational representation of the adopted receiver, not a first-principles SOURCE action.

With $k^2=|\boldsymbol k|^2$ and $\kappa=h|\boldsymbol k|$, resolved modes obey

$$
0\le1-\frac{\lambda_h}{k^2}\le\frac{\kappa^2}{12}=A.
$$

For $A<1$, nonzero-mode Poisson potential error obeys

$$
0\le\frac{k^2}{\lambda_h}-1\le\frac{A}{1-A}.
$$

For the semidiscrete wave receiver $\omega_h=c\sqrt{\lambda_h}$, phase-speed error is $1-\sqrt{\lambda_h/k^2}$. The resulting direction-independent sufficient conditions are:

| Target | Sufficient cells per wavelength |
|---|---:|
| Phase-speed relative error at most 1% | 12.858 |
| Poisson modal potential relative error at most 1% | 18.229 |

These are sufficient bounds for the declared isotropic difference operator, not universal WRRA transition lengths or cosmic sizes. Force errors additionally depend on the gradient operator, so the potential bound is not a force bound.

# 5. Executed results and cross-check

The actual contrast $\sum_s\delta u_s/\sum_su_{0s}$ is passed to a one-dimensional Poisson receiver. We compare the averaged fine continuum Fourier solution against the difference solution of the averaged input. Weighted-branch results:

| Samples per period | Relative potential $L^2$ error |
|---:|---:|
| 16 | 2.03376% |
| 32 | 0.500343% |
| 64 | 0.124628% |
| 128 | 0.0311291% |
| 1024 | 0.000486249% |

The separate three-dimensional source is fixed as $\delta\rho=0.05\sin(2\pi x)+0.025\cos[2\pi(x+2y)]+0.01\sin[2\pi(x+y+z)]$. Physical density in the witness is the positive background $1+\delta\rho$; the periodic Poisson problem uses its mean-subtracted contrast.

| Samples per axis | Potential error | Centered-force error |
|---:|---:|---:|
| 16 | 1.36316% | 1.71447% |
| 32 | 0.338379% | 0.427492% |
| 64 | 0.0844456% | 0.106802% |
| 128 | 0.0211021% | 0.0266962% |

The final resolution pair gives orders 2.00064 and 2.00024, respectively. After solving with FFTs, local stencils and face-flux divergence separately check the residual and discrete Gauss law. Independent `verify.py` calculates the above three-dimensional errors from modal solutions and Parseval's identity, without solving another grid problem. The maximum absolute discrepancy is below $2.178\times10^{-16}$. This is an internal independent calculation, not external peer review or new observational confirmation.

Negative controls were also executed. Raw decimation confuses a high mode with a low mode. Nonlinear subcell covariance $\overline{\rho v}-\bar\rho\bar v$ reaches approximately 0.03536 for a declared test velocity, showing why a mean-only nonlinear closure loses stress. Changing length units does not erase contrast. Transplanting a one-cell one-dimensional CFL into a local three-dimensional leapfrog yields a highest-mode growth factor approximately 9.899 per step.

# 6. Falsification and remaining connection

The corresponding bridge claim must be revised if source hashes or replay disagree; sector-energy or pressure ownership is lost; retained-band averaging/transport commutation fails; a stated modal bound is violated; second-order convergence fails for the specified smooth witness; or an aliased mode is accepted as physically resolved.

This calculation establishes **conservative averaging of actual finite SOURCE output and its connection to a macroscopic receiver with controlled finite-resolution errors**. Registered spectral transport remains spatially nonlocal. It does not complete GR/SM renormalization, establish a strict microscopic light cone, derive the cosmic calibration length from the microscopic length, close physical nonlinear stresses, or derive an information-to-gravity law from first principles. A suitable next calculation is a conservative nonlinear closure tracking the subcell covariance omitted by averaging.

# 7. Sources and reproduction

Registered book: MCC 3.0 v0.27-r1, DOI **10.5281/zenodo.23516661**; inspected publication-status commit `002b37a681d6693db9eb72ad9945ec1e5752b5af`. Spatial bridge: DOI **10.5281/zenodo.23329214**. The retained energy map is in repository stage `time_to_cmb_research_record_v1_0/stages/source_shutter_bridge_v02`.

Repository: <https://github.com/Wonsik-Choi-janefather/wrra-m-0.1>.

This package is separate from those registered editions. No new DOI has been assigned and the book has not been overwritten. Input hashes, all CSVs, results JSON, bilingual reports and code are supplied. Python 3 and NumPy are required. From the package directory run `python3 compute.py`, then `python3 verify.py`.
