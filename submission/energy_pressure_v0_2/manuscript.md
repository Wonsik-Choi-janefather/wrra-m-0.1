---
title: Energy and Pressure Compatibility in Finite WRRA Models
subtitle: Cold Allocations and Compensating Sectors
author:
- Wonsik Choi
- Jeongin Choi
date: Version 0.2 · 9 October 2026
---

Corresponding author: Wonsik Choi, Independent Researcher, Seoul, Republic of Korea  
Email: janefather@gmail.com · ORCID: 0009-0001-4263-9772

## Abstract

A finite particle readout can reproduce an assigned energy while failing to reproduce its pressure. We investigate when this obstruction can be removed within the Worldline–Residue–Resource–Action framework. For frozen relativistic populations, exact dust pressure requires every occupied momentum to vanish. Cold allocation therefore changes either the reference energy, the expected particle count, or the energy carried outside the particle sector. For hot allocations, we characterize differentiable compensators that preserve a constant total energy on a volume interval and construct a finite reservoir with correlated records. Its matching subspace has constant bare energy and zero pressure, and supports the earlier common-carrier conversion at every allowed volume. This completion has explicit resource requirements: a positive reference reserve, a finite compression range, and records distinguishing inequivalent energy functions. We prove that a hot kinetic sector cannot be exactly compensated by an independently convex additive reservoir. A constant-density negative-pressure term can match one reference point but cannot supply interval compensation. Executed composition with the preceding muon-decay calculation further shows that an unchanged compensator fails as daughter populations develop, whereas updated momentum-cohort records close the energy and pressure ledger. The result is a conditional effective completion with quantified capacity and stability boundaries, not a derivation of a new fundamental matter species. It identifies precisely which assumptions must change to reconcile microscopic kinetic readout with an aggregate dust allocation.

**Keywords:** finite energy ledger; kinetic pressure; compensating sector; effective Hamiltonian; coarse graining; WRRA

# 1 Introduction

A finite coarse description can preserve energy at a reference preparation while losing the response to volume changes. The general question is which additional state distinctions and energy resources allow one fixed constitutive law to preserve both quantities over a declared domain. An unrestricted complementary energy function answers the algebraic question immediately; a useful completion must also specify which transitions preserve it, how much reserve it consumes, and where it ceases to be admissible.

The four preceding studies isolate different parts of one problem. A finite two-stage filter supplies a retained address distribution and an aggregate energy allocation [1]. A particle interface maps that distribution to electron and muon pairs and shows that equal reference energies need not have equal volume derivatives [2]. A dynamical extension tracks decay daughters and their momentum cohorts [3]. An effective carrier implements the routing with a common interaction and relates pressure to the response of switching work [4]. The remaining question is whether the positive kinetic pressure can be reconciled with the earlier aggregate dust allocation through a specified additional sector.

This question matters because assigning a pressure independently of an energy function can conceal an inconsistency. It is equally insufficient to cancel a pressure at one reference volume and then retain that cancellation during compression, expansion, or decay. A compensating sector must carry energy, respond to the same volume coordinate, and retain enough state information to follow the matter it compensates.

We study a finite effective model, rather than an independently established form of matter. The construction uses measured lepton rest energies, the archived arithmetic preparation, and explicit dispersion and reservoir assumptions. Reproduction of the inherited energy and acceleration readouts is a consistency result of that construction. The structural contribution is the connection between a refinement criterion, a finite correlated carrier, reserve bounds, and a mechanical stability obstruction. We assess it through declared inputs, the WRRA transformation, calculated outputs, and failure conditions; a new numerical value is not a prerequisite for this analysis.

An explicit work-storage system is a familiar element of quantum thermodynamics [6]. Decompositions of cosmological energy into interacting sectors also require a prescription for their exchange and perturbations [7]. We do not claim either general idea as new. Our narrower problem is to complete the particular finite WRRA readout of [2–4] while accounting for the volume derivative of the same Hamiltonian. The reservoir spectrum below is engineered to satisfy this requirement. Its value is that the resulting conditions and costs can be stated and tested, including circumstances in which the completion is impossible within a restricted physical class.

Energy-conserving operations and explicit work storage also appear in the resource-theoretic treatment of finite thermodynamics [8]. Our commuting carrier uses this familiar conservation structure; it does not derive new thermal state-conversion laws or work-extraction bounds. Its additional question is simultaneous compatibility with a volume derivative on a fixed matching subspace. Work statistics under a driven Hamiltonian require a temporal measurement prescription [9]; the instantaneous pressure operator used here is not a substitute for those statistics. We compute mean switching work only for the specified pulse.

The progression within WRRA is equally specific. The aggregate allocation in [1] supplies the target and budget, which are retained rather than re-inferred. The sector-refinement obstruction of [2] becomes an energy-function equivalence criterion and a minimum unresolved-response error in Section 4. The carrier in [4], resonant at its reference volume, becomes an interval-resonant carrier after addition of two correlated reservoir levels in Section 5. The cohorts already evolved in [3] acquire energy and stress companions in Section 8, with a new joint record–volume capacity condition. The mathematical complement itself is elementary. The contribution is this executed connection, together with its record, reserve, domain, and curvature restrictions.

The main result has two sides. A correlated finite reservoir can produce an exact interval completion on a specified matching subspace. However, the compensator then has negative frozen bulk response when considered independently of the kinetic matter. Moreover, a fixed initial reservoir state cannot track the pressure created by decay. These restrictions prevent an algebraic completion from being mistaken for a stable autonomous cosmological medium.

# 2 Inputs and the assessment ledger

The verified numerical anchors are the inherited electron and muon rest energies, $m_e=0.51099895069$ MeV and $m_\mu=105.6583755$ MeV, with $c=1$ [5]. The archived finite preparation uses $N=10^6$ addresses. Its thresholds and control choices are copied unchanged. For an admitted composite address $n=\prod_p p^{\nu_p(n)}$, the routing statistic and ensemble readout are

$$
\chi(n)=\frac{\sum_p\nu_p(n)^2}{[\sum_p\nu_p(n)]^2},\qquad
X=\sum_n\pi(n)\chi(n). \tag{1}
$$

The baseline calculation gives $X=0.7390664036122881$. Four archived preparations are re-executed. The prime statistics and weights are not re-fitted to obtain compensation. The physical species assignment, source energy, opposite pair momenta, and isotropic volume law remain declared modeling inputs.

**Verified inputs.** Rest energies, archived preparation and routing, and the supplied finite decay kernel of [3] fix the calculation. The fractions $A=0.05$, $D=0.268$, and $L=0.682$ specify the inherited reference cell allocation; this paper does not infer them anew.

**WRRA transformation.** Finite address preparation is passed through the common carrier, assigned a relativistic energy function, and extended with correlated compensation records. Both pressure and reservoir exchange are obtained from that energy function. The decay calculation is executed on the retained populations.

**Outputs.** We obtain a cold-allocation criterion, an interval-completion theorem, a minimum record distinction, reserve and compression bounds, an independent-convexity obstruction, and an implemented decay-composition example.

**Failure conditions.** A candidate fails if it violates normalization, positivity on the declared domain, the derivative definition of pressure, the reserve budget, matching-subspace invariance, or the stated dynamical record rule. Mechanical convexity is tested separately; it is not inferred from energy positivity.

# 3 The pressure observable and the cold alternative

## 3.1 A fixed-state derivative

Let $v=V/V_0>0$ and let $H(v)$ be a differentiable finite Hamiltonian in a fixed basis. We write $\Pi=PV$ for the pressure-volume observable, which has units of energy:

$$
\Pi(v)=-v\partial_v H(v),\qquad
\frac{d\operatorname{Tr}[\rho(v)H(v)]}{d\log v}
=-\langle\Pi\rangle+\operatorname{Tr}[H\,\partial_{\log v}\rho]. \tag{2}
$$

The first definition holds the state, occupations, momentum labels, and preparation records fixed. The second expression compares a family of states. Confusing them can produce an apparent pressure cancellation that is actually a change in preparation. All interval statements below use fixed state labels and weights unless an evolution is explicitly specified.

For a finite population with nonnegative weights $w_i$, rest energies $m_i$, and reference momenta $k_i$, the kinetic energy and its pressure-volume moment are

$$
B(v)=\sum_i w_i\sqrt{m_i^2+k_i^2v^{-2/3}},\qquad
\Pi_B(v)=\sum_i\frac{w_i k_i^2v^{-2/3}}{3\sqrt{m_i^2+k_i^2v^{-2/3}}}. \tag{3}
$$

Zero-energy absent modes are omitted, avoiding an undefined zero divided by zero. Weights can represent expected numbers; they need not sum to one in Eq. (3).

**Proposition 1 (cold support).** Under Eq. (3), $\Pi_B(v)=0$ at any finite positive volume if and only if $k_i=0$ for every occupied mode $w_i>0$.

*Proof.* Each summand is nonnegative. An occupied term is positive exactly when its momentum is nonzero. A finite sum can vanish only when every occupied term vanishes. The converse follows directly. □

The assertion concerns the specified isotropic redshift law and frozen populations. Interactions, anisotropic stresses, or an additional volume-dependent term change its premises. Lowering a nonzero temperature or momentum makes the pressure small; it does not make it identically zero.

## 3.2 Energy normalization is not particle counting

In [2], one electron or muon pair is produced per admitted address and each pair has reference energy $E_*=2m_\mu$. If both species are instead cold while retaining their probabilities and one pair per address, their mean energy becomes

$$
\frac{B_{\mathrm{cold}}}{E_*}=X\frac{m_e}{m_\mu}+1-X
=0.2645079666631295. \tag{4}
$$

It is no longer the inherited unit energy. Three consistent alternatives can be distinguished. One can adopt this lower energy, retaining probabilities and pair count. One can multiply the expected number of pairs by $1/0.2645079666631295=3.7806044657761637$, preserving an ensemble energy but changing particle count. Or one can retain one cold pair per address and allocate the missing energy to another sector.

The third choice has a simple conditional completion: assign $E_*-2m_e$ to the reservoir on the electron branch and zero on the muon branch. Both assignments are volume independent, so their pressure vanishes. The mean reservoir energy is $0.7354920333368705E_*$. This is a rest-energy allocation, not a small correction. The second choice involves expected counts, not a literal fractional number of particles in each event, and it does not preserve the common energy of every individual branch. These distinctions rule out repairing the hot allocation by renormalizing probabilities alone.

# 4 Interval completion and the information retained

Let $I$ be a connected positive-volume interval. A fixed microstate label $i$ has energy $B_i(v)$, differentiable on $I$. A label can include a carrier branch, a finite momentum node, and a birth record. Define dust compatibility to mean a volume-independent total energy for each label in the admitted class. This is a constitutive statement about the combined sector, not a declaration that every constituent is pressureless.

**Theorem 2 (finite interval completion).** Fix a common total energy $\mathcal K$. An additive differentiable compensator achieves $B_i(v)+C_i(v)=\mathcal K$ throughout $I$ if and only if

$$
C_i(v)=\mathcal K-B_i(v),\qquad
\Pi_{C,i}(v)=-\Pi_{B,i}(v). \tag{5}
$$

If only zero total pressure is required, the constant $\mathcal K$ may depend on $i$. For a nonnegative compensator on all admitted labels and volumes, the common constant must obey

$$
\mathcal K\geq\sup_{i,v\in I}B_i(v). \tag{6}
$$

*Proof.* The energy identity implies Eq. (5). Conversely Eq. (5) supplies the identity and its derivative. Vanishing total pressure implies $\partial_v(B_i+C_i)=0$ because $v\ne0$; connectedness makes the sum a constant. Nonnegativity is precisely Eq. (6). For finitely many continuous energies on a compact interval the bound is finite and attained. □

The theorem intentionally exposes the engineered part of the construction. A free function can always complete a bounded finite energy ledger. The physical issue is whether the necessary function can be represented by a reservoir with stated resources and permissible responses. Sections 5–7 make those restrictions explicit.

**Proposition 3 (record distinction).** Suppose the compensator sees only a record $r(i)$ and uses one function $C_{r(i)}(v)$. With common $\mathcal K$, two microstates may share a record only if their functions $B_i(v)$ agree throughout $I$. For pressure-only compensation, they may share a record only if their derivatives agree, equivalently if $B_i-B_j$ is constant on $I$.

*Proof.* Subtract the two completion equations, or their derivatives. Conversely, assign one compensator to each equivalence class of identical energy functions, or identical derivatives for pressure alone. □

Thus the minimum number of distinguishable classical records in this deterministic assignment is the number of equivalence classes. This is not a bound on every possible quantum encoding, approximate device, or state-dependent average. It is an exact criterion for the finite diagonal assignment used here. It extends the sectorwise refinement criterion in Proposition 5 of [2]: coarse sector totals cannot determine a response that varies within a sector.

A scalar $C(v)$ can compensate one chosen mixture without resolving every branch. It then generally fails after changing that mixture. Universal compensation with the same uncorrelated reservoir state would require $\Pi_B$ to be proportional to the identity on the allowed matter space, since its expectation would have to be identical for all matter states. The hot electron and cold muon branches violate that condition. The distinction between a fixed-mixture fit and a correlated completion is operational, not terminological.

**Corollary 3.1 (unresolved response error).** At a fixed volume, let the pressure-volume values within one unresolved record class range from $p_{\min}$ to $p_{\max}$. The smallest possible worst-state residual after adding one common compensator response is $(p_{\max}-p_{\min})/2$. It is attained by choosing the negative midpoint. Indeed, the two endpoint residuals differ by $p_{\max}-p_{\min}$, so one has magnitude at least half that difference; the midpoint attains the bound for every intermediate value. For an unresolved electron–muon class in Eq. (7), the bound is $E_*s(v)/2$. At $v=1$ it is $0.1666627683159496E_*$. This is an exact fixed-volume approximation bound; attaining it at separate volumes does not by itself specify one differentiable reservoir energy or its reserve.

# 5 A finite correlated carrier construction

## 5.1 Complementary reservoir levels

Use dimensionless energies in units of $E_*$. The preceding source, electron-pair, and muon-pair branches have

$$
h_s(v)=h_\mu(v)=1,\quad h_e(v)=e(v)=\sqrt{r+(1-r)v^{-2/3}},
\qquad r=(m_e/m_\mu)^2. \tag{7}
$$

Let $K=\mathcal K/E_*$. A two-level reservoir has $c_0=K-1$ and $c_1(v)=K-e(v)$. With matter basis $(s,e,\mu)$ and reservoir basis $(0,1)$, set

$$
H_B/E_*=\operatorname{diag}(1,e,1),\quad
H_C/E_*=\operatorname{diag}(K-1,K-e),\quad
H_T=H_B\otimes I+I\otimes H_C. \tag{8}
$$

The matching subspace $\mathcal M$ is spanned by $|s,0\rangle$, $|e,1\rangle$, and $|\mu,0\rangle$. It is fixed as $v$ changes. On this subspace, $H_T=KE_* I$ and $-v\partial_vH_T=0$. These are operator identities, so they hold for mixtures and coherences supported on $\mathcal M$. They do not hold for arbitrary states of the full tensor product. For example, $|e,0\rangle$ retains the electron pressure.

The two reservoir levels are degenerate at $v=1$, but their slopes differ. Degenerate energy does not erase the record distinction required for pressure. Two levels suffice here because the source and cold muon have identical energy functions. The electron function is different. Extra zero-energy preparation registers are still needed for the prime-label comparison of [4].

## 5.2 Common interaction over the allowed interval

Let $Q$ be the equality projector for the two prime-label registers of [4]. Conditional independent preparation gives $\langle Q\rangle=\chi(n)$. The following extension of its interaction uses one volume-independent coupling $g$:

$$
H_I=g\{Q\otimes(|e,1\rangle\langle s,0|+\mathrm{h.c.})
+(I-Q)\otimes(|\mu,0\rangle\langle s,0|+\mathrm{h.c.})\}. \tag{9}
$$

**Proposition 4 (interval resonance).** For the fixed-basis Hamiltonians (8)–(9), the matching subspace is invariant, $[H_T,H_I]=0$, and the total pressure operator vanishes on that subspace. Starting in the source, a pulse with $\theta=gt/\hbar$ gives probabilities $\cos^2\theta$, $\chi\sin^2\theta$, and $(1-\chi)\sin^2\theta$ at every volume for which the reservoir is admitted.

*Proof.* Every nonzero coupling joins matching basis vectors with the same energy $KE_*$. The commutator therefore vanishes. Each block is a two-state rotation after removal of a common phase. The derivative of the interaction is zero and the derivative of the bare sum vanishes on the fixed matching subspace. □

This removes the particular bare-energy detuning of the unextended carrier [4] by changing the physical allocation: the electron conversion also changes the reservoir record. It does not show that the unextended Hamiltonian was resonant away from $v=1$. For the ideal rectangular pulse, the source initially has zero interaction expectation; because that expectation is conserved during the pulse, mean switching work is zero in this extended protocol. Preparation, control resources, and record resetting are not thereby costless. Their Hamiltonians have not been supplied.

The code checks the full six-dimensional matter–reservoir matrices for both controlled branches at five volumes, including partial pulses at $\theta=0,\pi/6,\pi/4,\pi/2,\pi$. It compares source and target probabilities and checks leakage outside the two coupled states. The inherited prime-register calculation is also re-executed. This is an effective Hermitian realization with specified correlated records. A local relativistic field interaction, a material reservoir, and an autonomous preparation device are not derived.

# 6 Reserve capacity and the aggregate cell

For the initial source, electron, and muon records, define the static domain $I_{\mathrm{static}}=[0.5,8]$. The bounds in this section apply to that record set. Daughter birth records introduced in Section 8 require their own joint record–volume domain.

The hot-branch pressure is $s(v)E_*$, where

$$
s(v)=\frac{(1-r)v^{-2/3}}{3e(v)},\qquad
b(v)=Xe(v)+1-X. \tag{10}
$$

A mean compensator has energy $[K-b(v)]E_*$ and pressure $-Xs(v)E_*$. The stronger branchwise positivity bound is $K\geq e(v_{\min})$ when the interval includes compression below one; also $K\geq1$ for source and muon branches. It is stronger than checking positivity only for the averaged state. For $K\geq1$, the electron branch has the exact compression boundary

$$
v_{\mathrm{pos}}=\left(\frac{1-r}{K^2-r}\right)^{3/2}. \tag{11}
$$

No finite $K$ covers arbitrary compression towards zero volume for a populated hot branch. This is a domain limit, not a requirement to realize an infinite universe or an infinite state space.

A second diagnostic is $C_i\geq|\Pi_{C,i}|$. If one were to interpret a sector as an isotropic stress-energy contribution with density $C_i/V$, this would be the algebraic dominant-energy inequality; for its negative pressure it also enforces the null-energy inequality. Such an inequality alone neither constructs a covariant stress tensor nor proves causality or stability. Here it is imposed only as an additional finite-ledger constraint. For the hot branch it requires $K\geq e(v)+s(v)$. Both $e$ and $s$ decrease with $v$, so the lower endpoint controls the interval bound.

To keep the inherited cell budget explicit, put a reserve $\beta$ into the compensator by transferring it from the original constant $D$ allocation. In units of the original reference cell energy $E_0$, define

$$
\mathcal E_B=A b(v),\quad
\mathcal E_C=\beta+A[1-b(v)],\quad
\mathcal E_D=D-\beta,\quad \mathcal E_R=L v. \tag{12}
$$

This gives $K=1+\beta/A$ per initially allocated pair energy, and

$$
\mathcal E_{\mathrm{cell}}=A+D+Lv,
\qquad \Pi_{\mathrm{cell}}/E_0=-Lv. \tag{13}
$$

The reserve is not added on top of an unchanged reference total. The internal interpretation of part of $D$ changes: $D-\beta$ remains the simple constant-energy component and $\beta$ is the initial compensator reserve. We do not identify the compensator with observationally established dark matter. Equation (13) preserves the chosen background ledger while refining its internal allocation.

For $I=[0.5,8]$, the minimum reserve for branch positivity is $\beta_{\mathrm{pos}}=0.01299577987048669$. The stronger diagnostic requires $\beta_{\mathrm{diag}}=0.03399406374700843$. We choose $\beta=0.035$, so $K=1.7$ and $D-\beta=0.233$. This is a declared design choice above the computed threshold, not a measured or fitted new constant. The choice gives $v_{\mathrm{pos}}=0.2035369539870002$ and $v_{\mathrm{diag}}=0.4824573142185409$.

Table 1. Dimensionless hot-branch energies and pressure-volume moments. Reservoir values are for $K=1.7$.

| Volume $v$ | Electron energy | Electron $PV$ | Reservoir energy |
|---|---:|---:|---:|
| 0.5 | 1.25991560 | 0.41996568 | 0.44008440 |
| 1.0 | 1.00000000 | 0.33332554 | 0.70000000 |
| 2.0 | 0.79370598 | 0.26455884 | 0.90629402 |

The numbers at $v=2$ are rounded values; the machine-readable output carries full precision. The pressure of the corresponding reservoir level is the negative of column three.

![Fig. 1. Exact interval completion for the archived baseline mixture. Left: matter energy, compensator energy, and their constant sum. Right: equal and opposite pressure-volume responses. The reserve is explicitly allocated and is not a free zero of energy.](figures/Fig1.png){width=6.2in}

Using the same homogeneous acceleration diagnostic as [1–2], $q=\tfrac12[1+3\Pi/E]$ at $v=1$, Eq. (13) reproduces $q=-0.523$. The uncompensated hot allocation gives $-0.5045237720806997$. Recovering the former is an exact consequence of the completed ledger; it is not an additional observational fit or a calculation of cosmological perturbations. A comparison with actual cosmological data would require a specified geometric and dynamical realization of these sectors.

# 7 Mechanical stability and a restricted impossibility result

Positive reservoir energy is not enough for independent material stability. Consider the standard frozen response to a volume variation, keeping all other internal labels fixed. Since $v=V/V_0$, a nonnegative bulk modulus requires nonnegative second derivative of energy with respect to $v$. For one relativistic energy $f(v)=\sqrt{m^2+k^2v^{-2/3}}$, with $y=k^2v^{-2/3}$,

$$
f''(v)=\frac{y(5m^2+4y)}{9v^2(m^2+y)^{3/2}}>0
\quad\text{when }k\ne0. \tag{14}
$$

**Proposition 5 (independent-convexity obstruction).** Let a frozen matter sector obey Eq. (3) and contain an occupied nonzero momentum. If an additive compensator has $C''(v)\geq0$ on an interval, the combined energy cannot be constant on that interval. Exact compensation instead requires $C''=-B''<0$.

*Proof.* Equation (14) makes $B''>0$. An independently convex compensator implies $(B+C)''>0$, contradicting a constant total. Differentiating Eq. (5) twice gives the second claim. □

The restriction is substantive: the complement reservoir cannot simultaneously be interpreted as an unconstrained, independently convex material under this same coordinate and frozen-state derivative. It does not invalidate the finite Hamiltonian of Section 5. There, matter and reservoir share the imposed volume coordinate and matching records. Their combined energy is flat along that coordinate. Flatness is neutral response, not strictly restoring stability, and it says nothing about relative deformations of constituents, shear, gradients, or inhomogeneous modes. A claim of a stable macroscopic medium would need those additional degrees of freedom and their dynamics.

The trade-off is visible without a complicated model. Add $\kappa(v-1)^2/2$ to the dimensionless compensator. Then

$$
(B+C)/E_*=K+\frac{\kappa}{2}(v-1)^2,
\qquad \Pi_{B+C}/E_*=-\kappa v(v-1). \tag{15}
$$

Choosing $\kappa$ larger than the maximum kinetic curvature makes the mean compensator convex on a compact interval. The code checks $\kappa=3$ on $[0.5,8]$ for the baseline mixture. The combined sector remains pressureless at the reference point but ceases to be dust throughout the interval. This is a controlled stable-curvature alternative, not an exact solution to the original interval requirement. The energy correction is an elastic model assumption, not a covariant sound-speed calculation.

A constant-density negative-pressure term has a different failure. Such a sector has $C=av$ and $\Pi_C=-av$. One can tune $a=Xs(1)$ to cancel the reference pressure. Interval cancellation would require $Xs(v)=av$, but the left side decreases and the right side increases for positive $a$. Thus the reference match cannot extend to an open interval. This explains why assigning a vacuum-like pressure is not by itself the compensating construction required here.

# 8 Decay and the records required for continuation

## 8.1 A frozen initial compensator fails

At fixed reference volume, the inherited muon-decay kernel conserves energy but creates daughter pressure [3]. Write $u=t/\tau_\mu$ and let $d=0.3333073631272256$ be the daughter packet pressure-volume moment divided by its parent rest energy. The matter pressure per initial pair is

$$
\Pi_B(u)/E_*=Xs(1)+(1-X)(1-e^{-u})d. \tag{16}
$$

A compensator whose state and pressure remain fixed at their initial values leaves residual $(1-X)(1-e^{-u})d$. At five lifetimes this equals $0.08638508237540457$. No change in the total matter energy is needed for this failure: parent and daughter states can have equal energy and different energy derivatives.

Table 2. Executed fixed-volume decay composition. All pressure-volume values are divided by $E_*$.

| Time in lifetimes | Matter $PV$ | Fixed compensator residual |
|---|---:|---:|
| 0 | 0.24634971 | 0.00000000 |
| 1 | 0.30132592 | 0.05497621 |
| 3 | 0.32899076 | 0.08264105 |
| 5 | 0.33273479 | 0.08638508 |

## 8.2 Matching daughter and birth records

A daughter packet needs a new reservoir energy function. For a muon at rest decaying at volume $v_b$, let $p_j$ be one finite electron-momentum quadrature node and let $a=(v_b/v)^{1/3}$. After angular summation the packet energy is

$$
B_j(v;v_b)=\sqrt{m_e^2+p_j^2a^2}
+[m_\mu-\sqrt{m_e^2+p_j^2}]a. \tag{17}
$$

The second term includes both massless neutrinos. Define its companion as $C_j=K m_\mu-B_j$. At birth $B_j=m_\mu$ for every node, so the reservoir changes from a parent level to a daughter level with the same energy $(K-1)m_\mu$. The slope, and therefore its pressure, changes. An energy-degenerate record transition can therefore compensate the stress created by decay without requiring an energy jump at that fixed-volume event.

**Proposition 6 (daughter domain and reserve).** For a finite set of records $(j,v_b)$, let $I_{j,v_b}$ be the admitted volume interval for that record and let $\mathcal D$ collect the admitted triples $(j,v_b,v)$. Positivity requires
$$
K\geq\sup_{\mathcal D} B_j(v;v_b)/m_\mu.
$$
The stronger algebraic diagnostic requires $K\geq\sup_{\mathcal D}(B_j+\Pi_j)/m_\mu$. These suprema replace the initial-record bounds of Section 6. On a noncontracting trajectory after birth, $v\geq v_b$, each packet obeys
$$
0\leq B_j\leq m_\mu,\qquad 0\leq\Pi_j\leq B_j/3.
$$
Consequently $K\geq4/3$ suffices for both conditions for every daughter record on that trajectory.

*Proof.* Write $q=p_j(v_b/v)^{1/3}$ and $N_j=m_\mu-\sqrt{m_e^2+p_j^2}\geq0$. Then $\Pi_j=[q^2/\sqrt{m_e^2+q^2}+N_j(v_b/v)^{1/3}]/3\leq B_j/3$. For $v\geq v_b$, both terms in Eq. (17) are no larger than at birth, where their sum is $m_\mu$. The two reserve bounds follow from $C_j=Km_\mu-B_j$ and $\Pi_{C,j}=-\Pi_j$. □

For the executed trajectory we use $I_{j,v_b}=[v_b,v_{\mathrm{end}}]$ with $v_{\mathrm{end}}=\exp(1.5)$. The selected $K=1.7$ exceeds $4/3$; the surviving original electron and muon records also obey their static bounds. The bounds hold on an open neighborhood of each trajectory point by continuity and strict reserve margin, so the local frozen-record derivative is well defined. They do not authorize arbitrary compression of late-born records. At $v_b=\exp(1.5)$ and $v=0.5$, the 64 momentum nodes give $B_j/m_\mu=2.072056$–$2.077221$, so the same reservoir becomes negative. This is an explicit excluded-domain control, not a failure of the calculated noncontracting path.

This prescription adds a new assumption: decay must update the compensation record along with the particle packet. The supplied weak-decay distribution and lifetime remain external physical inputs. No microscopic interaction has been derived that makes a material reservoir perform this update. The implemented process is a finite classical transition rule on packet records, combined with the earlier carrier preparation; it is not a closed unitary derivation of irreversible decay.

The 64 by 64 quadrature of [3] is retained. For these additive observables the angular variable can be summed out, leaving 64 electron-momentum nodes per birth cohort. A five-lifetime run with step $0.01\tau_\mu$ has at most 500 birth cohorts. This is a finite record set. Equivalent energy functions may share labels, as Proposition 3 permits. Retaining only total energy or only present pressure is generally insufficient for future transport of massive packets; [3] supplies a constructive cohort witness for that loss of information.

For increasing volume, old matter packets lose energy by redshift. Their compensators gain the same amount. With a physical volume coordinate this is equal and opposite mechanical work, not heat silently discarded from the ledger:

$$
\dot B=-\Pi_B\dot{\log v},\qquad
\dot C=+\Pi_B\dot{\log v},\qquad \dot B+\dot C=0, \tag{18}
$$

between supplied energy-conserving transitions. If a preparation scan changes occupation weights, the extra state term in Eq. (2) must still be retained. On the matching space with common constant total energy that term sums to zero for a normalized mixture. Individual sectors need not have a zero state term.

## 8.3 Executed expansion example

We repeat the inherited prescribed expansion $a(t)=\exp(0.1t/\tau_\mu)$, with $v=a^3$, right-endpoint decay, and step $0.01\tau_\mu$. This is a prescribed path for testing the ledger, not a self-consistent expansion solution. A separately written implementation of the same right-endpoint cohort formula agrees with the unchanged inherited calculation. Both use the same birth rule and finite kernel; this is an implementation cross-check, not an independent validation of the decay physics. Differentiating the compensator energy at fixed cohort records gives its pressure; it is not assigned solely by subtracting printed pressure values.

At five lifetimes, $v=4.481689070338065$, the matter has $B/E_*=0.6240247228381602$ and $\Pi_B/E_*=0.2074025858177988$. For $K=1.7$, the compensator has $C/E_*=1.0759752771618398$. Its finite-difference pressure is $-0.2074025858611605E_*$. Their constant energy sum and vanishing pressure agree within the declared numerical tolerance. The small pressure residual is differentiation error. The inherited script separately supplies time-step convergence; exact cancellation does not improve the discretization accuracy of its matter trajectory.

![Fig. 2. Limits of compensation. Left: positivity and the stronger algebraic energy-condition diagnostic fail at distinct compression boundaries. Right: fixed initial compensation fails during decay; updating matching records preserves the specified pressure cancellation.](figures/Fig2.png){width=6.2in}

# 9 Reproducibility and controlled failures

Online Resource 1 contains the new script, frozen inherited scripts, input controls, machine-readable results, hashes, and vector figures. Running `python reproduce.py` executes the carrier calculation of [4], which in turn executes the decay and interface calculations. The current new suite reports 244 of 244 checks passing; inherited reports contain 123 carrier, 56 decay, and 47 interface checks. These counts overlap through nested execution and must not be added as independent confirmations.

The tests compare analytic derivatives with centered finite differences, analytic convexity with second differences, partial and full matrix pulses with their analytic probabilities, and cohort outputs with the inherited implementation. The positivity threshold is checked by substitution in its boundary equation; independent root finding is used for the stronger diagnostic threshold. Daughter tests check all finite momentum nodes on post-birth expansion samples, the analytic pathwise bounds, and the excluded compression example. The uncorrelated-reservoir control is an algebraic response witness, not a simulated density-matrix evolution. Other controls exceed the capacity domain, substitute a one-point vacuum-like term, or freeze the compensator during decay. Passing these controls means the code detects the specified failures. It does not establish an experimentally observed compensation mechanism.

First derivatives use relative volume step $2\times10^{-5}$ and tolerance $10^{-9}$ for normalized pressure comparisons. Curvature uses step $10^{-4}v$ with tolerance $2\times10^{-7}$. Most algebraic and matrix comparisons use $10^{-11}$. Full-precision values, individual errors, software versions, and reference-input hashes are recorded in the archive. Universal interval claims rest on the proofs, rather than on checking a finite grid.

## 9.1 A fixed constitutive test

Before acquiring test data, fix $K$, the admitted record–volume domain, the spectra $H_B(v)$ and $H_C(v)$, the coupling $g$, the record-update rule, and the preparation protocol. Calibrate energy and force responses separately; do not infer the measured reservoir force by subtracting the measured matter force. At held volume $v$, prepare several allowed mixtures with electron probability $x$. The proposed matching realization predicts the independently measured residual
$$
R(v,x)=\langle\Pi_B\rangle_{\mathrm{meas}}+\langle\Pi_C\rangle_{\mathrm{meas}}=0.
$$
A nonzero residual beyond a predeclared combined measurement uncertainty and systematic-error budget rejects that realization. The code tolerance $10^{-9}E_*$ is a numerical comparison tolerance, not an experimental sensitivity claim.

A controlled record mismatch supplies a nonzero comparison. Immediately after a completed pulse, suppose a fraction $\eta$ of electron outcomes is paired with record 0 rather than record 1, while muon records remain correct. At fixed $v$, the predicted residual is $R/E_*=\eta x s(v)$. For example, $x=X$, $\eta=0.1$, and $v=1$ give $R/E_*=0.0246349705590674$. This is a specified erroneous-preparation comparison, not a claim that the ideal Hamiltonian generates leakage. Alternatively, holding the original compensator during decay predicts the nonzero residual in Eq. (16). These comparisons test both the sign and population dependence of the response.

For a spectral error $C_i=KE_*-B_i+\epsilon_i(v)$, frozen-record residuals are $R_i=-v\epsilon_i'(v)$; a constant energy offset is invisible to the pressure test and must be checked by the energy measurement. Once the law is fixed, it may fail these tests. Redefining $C$ after each observation to force $C=K-B$ would instead make the energy identity uninformative about nature. We therefore claim a conditional test of a specified realization, not empirical falsifiability of every unconstrained complementary function. No laboratory implementation is reported.

# 10 Scope and conclusion

The energy-pressure obstruction is resolved in a specified effective class: a correlated additive reservoir with a sufficiently large reference reserve and a declared joint record–volume domain. The initial record bounds and the post-birth noncontracting domain are distinct; arbitrary compression of late-born records is excluded. The same completion extends the carrier resonance beyond the single reference volume and composes with the executed decay ledger when the reservoir records follow the daughter cohorts. Both are changes to the model's allocation and state space, rather than a reinterpretation of the original hot matter as dust.

The result is also restrictive. An independently convex additive compensator cannot perform exact interval cancellation for a hot kinetic sector. A fixed reservoir cannot track changing daughter pressure, and a constant-density term cannot replace the required volume response. Positivity, algebraic energy inequalities, and mechanical stability are different tests. Exact background closure alone settles none of the unmodeled inhomogeneous dynamics.

For WRRA, the advance is an explicit connection from finite address statistics through common-carrier conversion to a compensated energy-and-stress ledger, together with quantified conditions under which that connection exists. Known reference values remain legitimate inputs, and recovering the inherited aggregate readout is a consistency achievement. The next physical question is the origin and dynamics of the compensating degrees of freedom. The full fifteen-channel carrier, local field interactions, causal perturbations, and autonomous controller resources remain outside the present finite construction.

# Statements and Declarations

**Data and code availability.** All newly generated results and their offline reproduction code accompany this manuscript as Online Resource 1. Public preceding records are cited in [1–4]. No new experimental dataset is reported. This fifth manuscript has not been assigned a DOI or submitted to a journal by this preparation workflow.

**AI assistance.** ChatGPT assisted with mathematical development, coding, numerical checks, drafting, and document preparation. Version 0.1 received a separately executed Astra medium AI review; this revision addresses its technical and presentation comments. The review and response are supplied as preparation records, not journal peer review or evidence of acceptance. Human authors are responsible for the final text and its submission.

**Funding and competing interests.** Author declarations must be confirmed before journal submission. No funding or conflict-of-interest declaration is inferred from earlier papers.

**Author contributions and approval.** The author list follows the four companion papers. Contributions, affiliations for both authors, and approval of this new manuscript must be finalized by the authors for journal submission.

# References

[1] Choi, W., Choi, J.: Conditional Reproduction of Ordinary Matter Fractions: Admissible Targets and Energy Readout in a WRRA Two Stage Filter Model. Preprint r11 (2026). https://doi.org/10.5281/zenodo.23237629

[2] Choi, W., Choi, J.: From Number Structure to Particle Selection: A Possible Readout and Its Energy–Pressure Constraints in a Finite WRRA Toy Model. Version 0.2 (2026). https://doi.org/10.5281/zenodo.23241511

[3] Choi, W., Choi, J.: Dynamic Decays and Nonequilibrium State Transitions in a Finite WRRA Model. Version 0.2 (2026). https://doi.org/10.5281/zenodo.23246308

[4] Choi, W., Choi, J.: Effective Carrier Routing, Control Work, and Stress in a Finite WRRA Model. Version 0.2 (2026). https://doi.org/10.5281/zenodo.23250062

[5] National Institute of Standards and Technology: CODATA recommended values of the fundamental physical constants, 2022 adjustment. https://physics.nist.gov/cuu/Constants/Table/allascii.txt. Values inherited unchanged from [2–4].

[6] Skrzypczyk, P., Short, A.J., Popescu, S.: Work extraction and thermodynamics for individual quantum systems. Nature Communications 5, 4185 (2014). https://doi.org/10.1038/ncomms5185

[7] Wands, D., De-Santiago, J., Wang, Y.: Inhomogeneous vacuum energy. Classical and Quantum Gravity 29, 145017 (2012). https://doi.org/10.1088/0264-9381/29/14/145017

[8] Horodecki, M., Oppenheim, J.: Fundamental limitations for quantum and nanoscale thermodynamics. Nature Communications 4, 2059 (2013). https://doi.org/10.1038/ncomms3059

[9] Talkner, P., Lutz, E., Hänggi, P.: Fluctuation theorems: Work is not an observable. Physical Review E 75, 050102(R) (2007). https://doi.org/10.1103/PhysRevE.75.050102
