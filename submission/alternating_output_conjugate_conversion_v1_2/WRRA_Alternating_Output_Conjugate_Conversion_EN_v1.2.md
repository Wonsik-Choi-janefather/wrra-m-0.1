---
title: "Alternating Output, Equal Conjugate Splitting and One-Clock Rendering in WRRA"
author: "Wonsik Choi · Jeongin Choi"
date: "2026-10-19 | Additions-only paper v1.2"
lang: en
---

## 135. Alternating Single-Sector Output, Remainder Placement and Conjugate Conversion

*Added 19 October 2026 · Structural model and initial-condition hypothesis · No newly calculated microscopic production or annihilation rates*

### Verified inputs

Corresponding particles and antiparticles have equal masses and spin magnitudes, with conjugate internal quantum numbers. Opposite electric charge alone does not identify the pair: an electron and a positron correspond, whereas an electron and a proton do not. A representative confirmed channel is $e^-+e^+\to\gamma+\gamma$; allowed channels depend on initial states and conservation laws. The incoming particles need not have been created together [S1–S2].

This hypothesis distinguishes which sector a declared source newly outputs in a particular execution from how already existing conjugate phenotypes interact. Requiring pair production in the source-output specification and allowing subsequent physical pair production/annihilation are distinct contracts.

### WRRA transformation

#### 135.1 One newly output sector per declared execution and region

Let $k$ be an execution index in a declared region, with a source setting $\kappa_k\in\{+1,-1\}$. The signs select matter and antimatter respectively. Let $J_k\ge0$ be the attempted new source output and $Q_k\in\{0,1\}$ the resource, interaction and conservation permission gate. This revision maps $k$ to the existing conditional shutter clock of Chapter 112 as a construction assumption; the physical output unit for $J$ still needs a microscopic bridge.

$$J_{M,k}^{\rm new}=Q_k\frac{1+\kappa_k}{2}J_k,\qquad J_{\bar M,k}^{\rm new}=Q_k\frac{1-\kappa_k}{2}J_k.$$

The specified gate gives

$$J_{M,k}^{\rm new}J_{\bar M,k}^{\rm new}=0,\qquad J_{M,k}^{\rm new}+J_{\bar M,k}^{\rm new}=Q_kJ_k.$$

This specifies single-sector production at a given execution. Exclusivity follows by definition of the gate, not from a completed microscopic derivation. It does not set the product of already accumulated occupations $N_MN_{\bar M}$ to zero. The switching law is specified below; permissions and resource costs remain explicit state data.

The scope is the declared source's initial/basic output. It is not a universal prohibition of experimentally confirmed pair production in subsequent interactions. Replacing every production pathway by this gate would require an extension reproducing those actual reactions.

#### 135.2 Initial setting of our universe

Wonsik Choi's proposal is recorded as an initial-condition hypothesis:

> The phenotype renderer can select the matter or antimatter sector. The initial source execution of our universe was prepared in the matter-output condition.

Thus $\kappa_0=+1$ is applied to that initial source. This explicitly chosen preparation corresponds to observed matter predominance; it is not a calculated necessity for the sign. The conjugate setting remains a permitted candidate, without granting our realization a privileged selector. No actual second universe or antimatter identification of a dark sector is inferred.

Matter output does not mean producing only negative electric charge. Ordinary matter contains negative electrons and positive protons. The setting refers to conjugate matter/antimatter configurations, not spatial reflection or the earlier exterior-algebra parity selection alone.

Initial-condition ownership is explicit. One may implement $\kappa_0$ as a function of the existing SOURCE preparation $\eta$; if independently selected, it counts as an additional input. That interface is not completed here. Chapter 8's prohibition on arbitrary asymmetry from both CP-symmetric LAW and CP-symmetric preparation is retained. The new $\kappa_0=+1$ preparation declares an asymmetric state and is a different hypothesis.

Actual one-sector particle production requires source energy, charge and every declared conserved or violated quantum number to be tracked. A closed initial state with zero baryon number and exact baryon conservation cannot acquire net baryon number without an owner. Transfer, permitted violation or the opening interface must be supplied by a microscopic model. Output permission and actual production are distinct responsibilities.

#### 135.3 Alternating click modes and rare late output

The revised proposal specifies the switching law:

$$\kappa_{k+1}=-\kappa_k,\qquad \kappa_0=+1,\qquad \kappa_k=(-1)^k.$$

The setting alternates every click; actual generation occurs only when $Q_k$ permits it. This is not mandatory production of one particle per click. Define $J_k$ as a count of comparable output packages. Assume the large initial output $Q_0J_0=A>0$ completes within the matter-mode click. If the initial burst spans several clicks, its weighted sum $\sum_k\kappa_kQ_kJ_k$ must be recomputed. Equal output in two consecutive modes cancels their initial imbalance. An initial sign alone therefore does not ensure matter dominance.

Late output is small and infrequently permitted. Add the condition that the two modes have equal mean permitted output. For example, let $J_k=1$ for $k=1,\ldots,2n$, with independent $Q_k\sim\mathrm{Bernoulli}(p)$ and $0<p<1$. The late count difference $D=N_M^{\rm late}-N_{\bar M}^{\rm late}$ then satisfies

$$\mathbb E[D]=0,\qquad \operatorname{Var}(D)=2np(1-p).$$

Each late sector has expected count $np$. A long-run 1:1 ratio requires mode-unbiased statistics and sufficiently many events; exact equality in a finite realization is not guaranteed. This independent Bernoulli example demonstrates statistical compatibility, not a derived microscopic production probability. Mode-dependent permissions can produce a nonzero mean difference.

The total sector difference is

$$\Delta N=A+\sum_{k=1}^{2n}(-1)^kQ_kJ_k.$$

A large initial matter output and mean-symmetric late output coexist under these conditions. Baryon asymmetry requires separate weighting by each package's baryon number. The expression does not derive the observed five-percent matter fraction or baryon-to-photon ratio.

#### 135.4 Withdrawal of the pair-production prohibition and even-state splitting

The pair-production prohibition is withdrawn. For a corresponding particle-antiparticle species, equal rest masses are the verified input. WRRA assigns the same mass-implementation code $n$ to both conjugate outputs. This is a declared mapping assumption, not a theorem equating mass with every information measure.

$$\mathcal C_{\rm out}(2n,\xi)\rightleftarrows(n,a,\chi)+(n,a,\bar\chi).$$

Only equal-size splitting is permitted; asymmetric splitting is forbidden in this channel:

$$\mathcal D_{\rm eq}(r)=\{(n,n):n\text{ is an admitted odd composite},\ r=2n\}.$$

Examples admitted arithmetically are $18\to9+9$, $30\to15+15$ and $54\to27+27$. The channels $24\to9+15$ and $54\to9+45$ are forbidden. Since $24/2=12$ is not an odd composite, code 24 has no channel here. Admission, species, conjugate charges and energy conditions remain required. Equal mass-implementation codes do not imply equal kinetic energies in every observation frame.

The parent and environment must supply energy and momentum. A single photon cannot create two free massive particles alone in vacuum; a second photon, nuclear recoil or an external field must be included as appropriate. An even output code is not automatically a SOURCE resident or a photon. The actual conjugate outputs are now stipulated to occur on successive existing clock ticks, as specified below.

#### 135.5 Separate source, conversion and occupation ledgers

Let $P_{M,k}$ and $P_{\bar M,k}$ count actual pair-derived outputs on each tick. Replace the former simultaneous $+P_k$ terms by

$$N_{M,k+1}=N_{M,k}+J_{M,k}^{\rm new}+P_{M,k}-H_k,$$
$$N_{\bar M,k+1}=N_{\bar M,k}+J_{\bar M,k}^{\rm new}+P_{\bar M,k}-H_k.$$

A permitted pair reserves its second output for the next tick. Pending occupations $L_{M,k},L_{\bar M,k}$ record the unrendered partner. The parent/source/environment must own its energy and conserved charges until output; neither gaps in conservation nor double counting are allowed. Over each completed pair, $\sum_k P_{M,k}=\sum_k P_{\bar M,k}$. Completed symmetric pairs do not create a net matter excess, although the rendered occupations alone can differ during the intermediate tick. Annihilation cannot exceed actual available occupations.

Electric charge is distinct from sector identity. A lone emitted electron requires the opposite charge in the source/environment, with an open ledger until transfer is specified. A neutral matter package is possible, but its baryon and lepton ownership remains required. Average cancellation between modes cannot replace local charge conservation.

#### 135.6 Upper/lower placement of the odd remainder

For an odd composite $n=2q+1$, introduce $b\in\{+1,-1\}$ to specify whether the remainder one is attached to the upper or lower position. The ordered occupations are

$$T(n,b)=\left(\frac{n+b}{2},\frac{n-b}{2}\right),\qquad U+D=n,\quad U-D=b.$$

The upper position has one extra unit for $b=+1$; the lower has one extra for $b=-1$. Arithmetic parity is unchanged, but the ordered placement differs. The renderer selects the permitted phenotype's remainder placement $b$. An interface to the source mode can declare a species reference $b_a^{(0)}$ and assign $b_{a,k}=\kappa_k b_a^{(0)}$. This correspondence is a structural assumption.

![Figure 1. Two placements of the odd address 9. The extra unit gives (5,4) above or (4,5) below. Cells are arithmetic occupation units, not measured particle shapes.](figures/remainder_placement.png)

The combined placement residual is

$$\delta_{\rm pair}=(U_1+U_2)-(D_1+D_2)=b_1+b_2.$$

Opposite placements give zero; like placements leave $+2$ or $-2$. When $b_2=-b_1$, each position holds $n$. For example, the upper placement of 9, $(5,4)$, and lower placement of 9, $(4,5)$, combine as $(9,9)$. Two upper placements instead give $(10,8)$, leaving residual two.

| First | Second | Ordered totals for 9 and 9 | Residual | This balanced-closure channel |
|---|---|---|---|---|
| Upper | Lower | $(9,9)$ | $0$ | Candidate allowed |
| Lower | Upper | $(9,9)$ | $0$ | Candidate allowed |
| Upper | Upper | $(10,8)$ | $+2$ | Closed under this rule |
| Lower | Lower | $(8,10)$ | $-2$ | Closed under this rule |

![Figure 2. The same two odd addresses yield balanced or residual occupations depending on remainder placement. All four address sums equal the even number 18, so evenness alone cannot select annihilation.](figures/conjugate_closure.png)

The candidate closure gate is $K_{\rm close}=\mathbf1[n_1=n_2]\mathbf1[b_1+b_2=0]$. The proposed difficulty of interlocking like placements is formalized as non-admission to this particular balanced-closure channel. It does not prohibit all interactions or binding between like placements. Actual interlocking feasibility and transition rates are not calculated from the occupation difference alone.

Exchanging the positions gives $\tau T(n,b)=T(n,-b)$ with $\tau^2=1$. This is a candidate geometric representation of conjugacy, not a substitute for the full species and charge/baryon/lepton conjugacy conditions. Upper/lower initially label internal or local positions, not electron spin up/down or an absolute cosmic direction. A physical spatial shape additionally needs coordinate-transformation rules, length/energy functions and an interaction.

For inverse splitting, the candidate parent has $U=D=r/2$ and distributes its occupations to admitted identical odd composites $n=n_1=n_2=r/2$ with opposite placements $b,-b$. The code $r$ alone does not specify addresses, directions or quantum correlations; $\xi$ and permission conditions remain necessary. Equal physical masses are imposed through the input-to-code mapping; electric-charge magnitudes, photon channels and annihilation cross sections have not been derived from this occupation model.

#### 135.7 Conjugate structures open each other's release pathway

The proposed annihilation interpretation is:

> Two conjugate particle phenotypes can open an interaction pathway that releases their stable implementation structures, transferring their particle-form energy into other carrier phenotypes.

The knot/key language denotes structural compatibility and release. Whether there is an actual geometric or topological twist is unresolved. Such a claim requires defined degrees of freedom, invariants, an energy functional and an interaction operator. Equal mass alone does not establish equal bit count or every information measure. Implementation load and distinguishable states/correlations require separate ledgers.

Use already admitted odd-composite mass-implementation codes $n,n$, a corresponding species $a$ and conjugate internal structures $\chi,\bar\chi$. A candidate code is

$$(n,a,\chi)+(n,a,\bar\chi)\xrightarrow{\text{allowed interaction}}\bigl(r=2n,\text{carrier output state}\bigr).$$

Every sum of two odd integers is even. Conjugacy therefore gates the interpretation as annihilation, rather than the arithmetic fact of evenness. Two same-sector particles also have an even address sum and must not annihilate solely for that reason.

The aggregate code $r$ has a different type from an existing even-composite SOURCE resident. Evenness alone identifies neither a photon nor dark matter. Exceeding the existing address cutoff does not automatically create SOURCE capacity; finite output encoding and its cost need specification.

#### 135.8 Energy and information transfer

Lost incoming particle occupations must transfer their energy, momentum and conserved internal quantum numbers to the outgoing state. Antimatter energy is not cancelled as negative energy. Zero rest mass of individual outgoing photons does not require zero invariant mass of the whole outgoing system.

$$E_{\rm out}=E_{\rm in},\qquad\mathbf p_{\rm out}=\mathbf p_{\rm in}.$$

Track states, phases and correlations rather than declaring information deleted. The equal-split sum code recovers $n$ but does not preserve momenta, spins, phases or correlations. Asymmetric alternative decompositions are forbidden here. An implementation requiring overall reversibility must retain the distinction in other output degrees of freedom or included environmental correlations. This does not require storing the universe's entire past as an additional archive.

#### 135.9 Existing renderer clock and alternating conjugate placements

The conditional shutter already calculated in Chapter 112 is adopted as one renderer tick, without fitting a new time constant:

$$\Delta t_{\rm clk}=1.4813019664158633\times10^{-21}\ {\rm s},\qquad f_{\rm clk}\simeq6.750818015\times10^{20}\ {\rm Hz}.$$

Matter and antimatter denote conjugate implementations of the particle itself: opposite twist directions or upper/lower placements of remainder one are candidate representations of that distinction. Molecular chirality, amino-acid L/D forms and sugar handedness are excluded. These are two conjugate alternatives, not four independent states or a four-tick cycle.

$$\kappa_{k+1}=-\kappa_k,\quad b_{a,k}=\kappa_k b_a^{(0)},\quad t_{k+1}-t_k=\Delta t_{\rm clk}.$$

Choosing which placement labels matter is a reference-sign convention. The same sector returns after $2\Delta t_{\rm clk}$, corresponding to $3.375409007\times10^{20}$ Hz. Clock activity does not require particle output on every tick: permission is still required. Once a pair is permitted, the second output is reserved for the next tick and its intermediate conservation ledger must close. Adopting this existing conditional clock is a construction assumption, not a measurement of a unique universal minimum time.

#### 135.10 One-tick sequential output and initial separation

The two equal-code conjugate phenotypes of a pair are stipulated to appear one tick apart. The earlier phenotype can move before its partner appears. Their separation immediately after the second output is

$$d(t_{k+1})=\left|\mathbf x_1(t_k)+\int_{t_k}^{t_{k+1}}\mathbf v_1(t)dt-\mathbf x_2(t_{k+1})\right|.$$

For a fixed common source location and constant first-particle velocity, $d=|v_1|\Delta t_{\rm clk}$. The light-speed reference scale in that source frame is

$$c\Delta t_{\rm clk}=4.440831575520451\times10^{-13}\ {\rm m}=0.4440831575520451\ {\rm pm}.$$

This is a reference length, not a universal actual displacement of a massive particle. Sequential output permits initial spatial separation; subsequent trajectories and interactions require their own dynamics. If timing correlations disagree with observations, or if the parent/environment cannot close intermediate conserved quantities, this sequential rule fails. Production rates, microscopic correlations and cross sections have not yet been calculated.

### Outputs and scope

The new outputs are an alternating-mode/rare-output statistical ledger, conjugate splitting of even aggregate states with a common annihilation ledger, a single-sector gate for initial/basic source production, the matter-prepared initial condition of our universe, the conjugate-release interpretation and the type distinction between arithmetic codes and physical ledgers, now supplemented by equal-only splitting and the existing-clock sequential output contract. No new microscopic production rate, annihilation cross section/lifetime, cosmic thermal history or five-percent composition calculation was executed. Chapter 135 connects Chapters 8 and 18 to a subsequent output-architecture hypothesis without recalibrating existing address, energy, GR or CMB results.

### Falsification conditions

An implementation fails if it annihilates same-sector particles merely because their address sum is even, identifies electron/proton as conjugates merely because charges are opposite, loses or duplicates energy/conserved quantities, or discards information it declares conserved. A microscopic interface must be revised if it fails to reproduce known production/annihilation channels or lacks an owner for its initial preparation and resource costs.

### Conclusion and genealogy

The hypothesis distinguishes a large initial matter-mode output, rare later output under alternating modes, and conjugate splitting of even aggregate states with reverse annihilation. The pair-production prohibition is withdrawn. Our universe's $\kappa_0=+1$ is a declared initial condition; arithmetic evenness is a candidate transition code. Actual knot structure and microscopic interactions remain to be derived.

This chapter is added to the formal v0.24 baseline. The earlier v0.25 calibrated generation/survival draft is discarded; this material replaces it in the new v0.25 without incorporating that calculation. The separated matter/antimatter-domain and SOURCE-size exploration also remains separate. Inclusion here records a structural hypothesis, not completed physical validation.

[S1] MIT, Markus Klute, [Charge Conjugation, Lecture 2.4](https://ocw.mit.edu/courses/8-701-introduction-to-nuclear-and-particle-physics-fall-2020/1f2bba94386a64cd8f5b640358c6a8d4_MIT8_701f20_lec2.4.pdf).

[S2] MIT, [Principles of Radiation Interactions: Electron–Positron Annihilation](https://ocw.mit.edu/courses/22-55j-principles-of-radiation-interactions-fall-2004/ca1553f56c6670570f63f804edbeffa9_energ_depos_elec.pdf).

[S3] SLAC E144 Collaboration, [Experiment E144: pair production](https://www.slac.stanford.edu/exp/e144/e144.html); K. T. McDonald, [Positron Production by Laser Light](https://www.slac.stanford.edu/pubs/slacreports/reports08/ssi97-029.pdf), 1997.
