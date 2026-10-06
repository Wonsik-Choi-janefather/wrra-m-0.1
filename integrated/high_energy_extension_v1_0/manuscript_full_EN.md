---
title: "WRRA M High-Energy-to-Phenotype Extension 1.0"
subtitle: "Detailed Integrated Research Manuscript for Stages 0.1-0.12: Thermal Probes, Record Stability, Component Activation, Harmonic States, and Downstream Reconnection"
author:
  - "Wonsik Choi"
  - "Jeongin Choi"
date: "6 October 2026"
lang: en
---

# Abstract

This study re-examines, through the finite research sequence 0.1-0.12, the upstream problems of high-energy states, filter stability, record formation, the micro-macro boundary, component activation, assembly grammar, harmonic states, and phenotype formation, while preserving the address, energy, pressure, information-load, gravity, and expansion ledgers frozen in WRRA Core 1.0, Minimal Computation Cosmology (MCC) 2.3.2, and the existing WRRA M 1.0. The central rule of the study is to prohibit post-hoc retuning to match established downstream outputs and to evaluate every stage in the order **verified inputs -> WRRA-specific transformation -> outputs -> falsification conditions**.

Stage 0.1 freezes the address ledger $5\%/26.8\%/68.2\%$, the inherited SI energy composition $4.93\%/26.5\%/68.57\%$, the deceleration diagnostic $q_0=-0.52855$, the reference rotation speed $207.5109051266\,\mathrm{km\,s^{-1}}$, and the conditional lensing deflection $0.5355865106^{\prime\prime}$ as the baseline. Stage 0.2 defines a thermal probe using a finite Hamiltonian $H$, temperature $T$, and energy reference $E_0$, thereby making explicit that temperature alone does not determine a WRRA state. Stage 0.3 directly tests the hypothesis that high-temperature thermal population mixing alone destroys the existing filter gap. The hypothesis is rejected because a positive gap remains even in the high-temperature uniform state. This negative result indicates that filter stability is controlled not merely by population mixing but by response contrast and the readout structure.

Stage 0.4 parameterizes filter contrast by an order coordinate $m_F$, establishing a structural connection between cooling and filter stabilization. Stage 0.5 separates the channel-selection filter from the SOURCE address admission/return filter and reconstructs the phenotype, resident-nonphenotype, and return branching under the address weighting $w_n\propto n^{-\alpha}$. This step also shows that the resident Actual fraction $31.8\%$ is not an automatic fixed point of unlimited recycling, which implies the need for a finite generation window. Stage 0.6 defines the shutter/frame as a finite record event while separating event discreteness from discreteness of physical time. The hypothesis that the WRRA frame is identical to Planck time is therefore not adopted.

Stage 0.7 defines the micro-macro boundary not by one universal constant but by the intersection of the state-distinguishability boundary $B_D$ and the repeated-record-stability boundary $B_R(\delta)$. Calculations show a continuous record-stability crossover as the number of fine shutters $K$ increases and the transition probability decreases. Stage 0.8 defines a component by the four conditions origin, activation, identity retention, and ledger closure. Using the existing Prime Parts result that removing the origin tag breaks isometry, the study introduces the origin-preserving component as a formal intermediate layer of WRRA M. The Address 105 case shows that the number of active component occurrences is not identical to the number of fundamental primitive types.

Stage 0.9 divides stabilized component assemblies into two representations, stable codewords and harmonic states. The existing WRRA neutrino candidate $(0,5,29)q_\nu$ has an integer-cycle ledger under a common rest-phase recurrence and is therefore retained as a concrete example of harmonic representation. Stage 0.10 fixes the nonduplication condition $\sum_{g,j}E_{\phi,g,j}=E_\phi$, under which components, channels, generations, and harmonic modes do not create new cosmic energy but decompose the existing phenotype energy in normalized form. By changing the upstream generation rule while keeping the SI coefficients frozen, the study also confirms that the downstream value of $q$ responds, thereby establishing a sensitivity path through which upstream change propagates into downstream cosmological output.

The reverse minimality audit of stage 0.11 summarizes the minimum interface required by the present executable structure as $G_{\min}=\{A_{N_P},O,B_L,B_R,R,\Phi,L\}$. The primitive-alphabet size $N_P$ is not fixed here; $N_P=4$ is retained only as a candidate under additional grammar assumptions. Stage 0.12 integrates stages 0.1-0.11 into a single typed Master Ledger, closing the structural chain from high-energy Actual through the thermal probe, filter, SOURCE branching, shutter/record, micro-macro boundary, component activation, stable codeword/harmonic state, phenotype, SI energy, pressure/load, and finally twist/gravity/expansion.

The final verdict of this study is therefore **WRRA M 0.1-0.12 Structural Integration 1.0 - CLOSED**. Research after 0.12 is not framed as repair of a failed 0.1-0.12 integration. It is instead defined as the next independent set of questions: a physical law that autonomously generates filter/admission/generation controls from temperature, a law that constructs the physical particle Hamiltonian from primitive grammar, a law that derives flavor mixing upstream from the $0:5:29$ harmonic ledger, and a law that evolves homogeneous background and nonuniform local states in one covariant SI geometry.

**Keywords:** WRRA, Minimal Computation Cosmology, high-energy state, thermal probe, SOURCE, record stability, micro-macro boundary, component activation, primitive alphabet, codeword, harmonic state, neutrino, information load, gravity, cosmic expansion

# 1. Research Background and Objective

## 1.1 The connection problem remaining after 2.3.2

MCC 2.3.2 and the existing WRRA M integration provide a downstream executable path connecting the common carrier, address conditioning, internal state, phenotype energy, pressure, information load, gravity, and expansion. What had not yet been organized sufficiently into one ledger was how high-energy Actual descends into the stable phenotypes of the present universe, and where the component identity, activation, and assembly-order effects observed in Prime Parts belong within the upstream-downstream structure.

The direct questions of this study can be grouped into four sets.

1. How should a high-energy or high-temperature condition be entered into a WRRA state?
2. How can the boundary between microscopic state and macroscopic record be defined without identifying it with a minimum time or one universal constant?
3. When is a pre-phenotype part judged to be an independent component, and how is its origin preserved after a state transition?
4. How can stable component assembly and harmonic states be connected to the existing phenotype-energy and downstream-gravity ledgers without energy duplication?

These questions are not independent. If temperature does not directly generate a particle, intermediate states are needed between temperature and phenotype: filter, admission/return, record, component stabilization, and assembly. The strategy of this study is therefore to solve the problems separately and then reconnect them in stage 0.12 as a single typed ledger.

## 1.2 Completion criterion

This study is not defined so that it can be completed only by producing a new independent prediction. Its completion criterion consists of four items:

**verified inputs -> WRRA-specific transformation -> outputs -> falsification conditions**

Even when established constants and observations are used, values reproduced through WRRA-specific state transformations after those inputs have been frozen are treated as consistency and explanatory achievements. Conversely, if an as-yet-unmeasured quantity is produced after the model has been fixed, it is distinguished as a conditional WRRA prediction.

## 1.3 Rule against mixing types

The most important ledger rule in this study is that numbers with different meanings must not be treated as the same physical quantity. At least the following five types are kept distinct.

| Ledger type | Meaning | Representative example |
|---|---|---|
| ADDRESS | admitted, resident, and returned address shares | $0.05/0.268/0.682$ |
| ENERGY | physical distribution of SI energy | $0.0493/0.265/0.6857$ |
| RECORD | state readout and repeated stability | $B_D$, $B_R(\delta)$ |
| COMPONENT | part identity that preserves origin | $O$, active/reserve |
| PHASE | relative-phase ledger for multiple modes | $\Phi$, $0:5:29$ |

Without this distinction, address shares may be mistaken for energy shares, the number of components may be mistaken for an amount of energy, or a phase-cycle count may be mistaken for a particle count.

# 2. Method: Frozen Baseline and Typed Ledger

## 2.1 Freeze contract

The new high-energy extension is attached upstream of the existing WRRA M model. Downstream coefficients therefore may not be readjusted in order to match the established outputs. The frozen baseline is shown in Table 1.

| Quantity | Frozen value | Type |
|---|---:|---|
| phenotype address fraction | 0.050000000 | ADDRESS |
| resident nonphenotype fraction | 0.268000000 | ADDRESS |
| return fraction | 0.682000000 | ADDRESS |
| phenotype energy fraction | 0.0493 | ENERGY |
| resident nonphenotype energy fraction | 0.2650 | ENERGY |
| return energy fraction | 0.6857 | ENERGY |
| deceleration diagnostic $q_0$ | -0.52855 | DOWNSTREAM |
| reference rotation | 207.5109051266 km/s | DOWNSTREAM |
| conditional lensing | 0.5355865106 arcsec | DOWNSTREAM |

The address fractions sum to one, and the energy fractions form a separately normalized SI ledger. The two ledgers are not automatically identified merely because some values are numerically similar.

## 2.2 Overall research flow

The entire 0.1-0.12 connection is

$$
\text{high-energy Actual}
\rightarrow \rho_T
\rightarrow \text{filter/readout}
\rightarrow \text{SOURCE branching}
\rightarrow \text{shutter/record}
\rightarrow B_{\mu M}
\rightarrow \text{component activation}
\rightarrow \text{codeword/harmonic}
\rightarrow \text{phenotype}
\rightarrow E(V)
\rightarrow P
\rightarrow \text{load}
\rightarrow \text{twist/gravity/expansion}.
$$

Each arrow is treated not as a loose conceptual association but as an interface specifying what type of input is received and what type of output is passed to the next stage.

# 3. Stage 0.1 - Freezing the Baseline

## 3.1 Verified inputs

The address branching, internal Hamiltonian, SI energy ledger, pressure, information load, local gravity, and homogeneous-expansion calculations used in WRRA Core 1.0, MCC 2.3.2, and the existing WRRA M 1.0 are fixed.

## 3.2 WRRA-specific transformation

The new upstream variables do not alter the cause of the established downstream outputs. They are added only as an input layer determining **which state is supplied to the downstream model**. Therefore, after introducing the new upstream layer, the downstream coefficients may not be retuned merely to preserve the existing $q_0$.

## 3.3 Outputs and interpretation

The frozen values are reference points that the new research is not allowed to move. A change that rearranges only internal labels or phases, without changing total energy or population, must preserve the baseline downstream values. By contrast, an upstream change that genuinely changes the population must produce a downstream response. This distinction is tested directly in the stage-0.10 sensitivity analysis.

## 3.4 Falsification conditions

The 0.1 contract fails if any of the following occurs.

- Existing SI coefficients are recalibrated in order to connect the new upstream layer.
- ADDRESS fractions are automatically substituted for ENERGY fractions.
- An increase in the number of components or harmonics is treated as an increase in cosmic energy.

**Verdict: PASS.**

# 4. Stage 0.2 - From Temperature to a WRRA State

## 4.1 Problem statement

Entering temperature $T$ as one number does not uniquely determine the internal state. At the same temperature, the state distribution depends on the Hamiltonian and on the choice of energy reference. Temperature is therefore treated in WRRA as one condition used to construct a state, not as the state itself.

## 4.2 Definition of the thermal probe

For a finite Hamiltonian $H$ and reference energy $E_0$, define

$$
\rho_T=
\frac{
\exp[-(H-E_0I)/(k_BT)]
}{
\operatorname{Tr}\exp[-(H-E_0I)/(k_BT)]
}
$$

as the thermal probe. The required input is therefore the triple

$$
(T,H,E\text{-prescription}).
$$

The Planck temperature may be used as a comparison scale, but a state not defined by the present finite representation is not silently extrapolated merely because the Planck scale is invoked. Regions outside the defined representation remain NULL.

## 4.3 Numerical check using the inherited internal gap

The inherited internal gap is

$$
\Delta E=431.081244315\ \mathrm{MeV}.
$$

The existing conditional excited population is

$$
p_{\mathrm{exc}}=0.0799766545,
$$

with excitation contribution

$$
E_{\mathrm{exc}}=34.4764357391\ \mathrm{MeV}.
$$

If this population is interpreted backward only as a two-state Gibbs population, the equivalent temperature is approximately

$$
T_{\mathrm{Gibbs}}\simeq 2.048\times10^{12}\ \mathrm{K},
$$

while the temperature scale of the gap itself is

$$
\frac{\Delta E}{k_B}\simeq5.00249\times10^{12}\ \mathrm{K}.
$$

These values are vastly below the Planck temperature. There is therefore no basis for identifying the internal thermal mixing of the current particle model with the Planck boundary.

## 4.4 Outputs and falsification conditions

The conclusion that temperature alone does not determine the state becomes an important constraint on all later stages. The thermal-probe definition would fail if different Hamiltonians were forced to yield the same state at the same $T$. Likewise, the inherited address-conditioned population must not be automatically reinterpreted as a thermal population.

**Verdict: finite thermal probe PASS.**

# 5. Stage 0.3 - The Planck Boundary and Filter Stability

## 5.1 Test hypothesis

The initial candidate hypothesis was

$$
T\uparrow
\Rightarrow \text{thermal mixing}\uparrow
\Rightarrow \text{filter gap}\downarrow
\Rightarrow 0.
$$

If this were correct, the phenotype filter would lose its discriminating power at high temperature and be reselected as the system cooled. This stage tests that intuition directly under the frozen filter rule.

## 5.2 Compatibility and the gap

Define the compatibility between carrier states $u_i$ and $u_j$ as

$$
c(i,j)=-\|u_i-u_j\|_C^2.
$$

For $F_{DX}$ to be selected uniquely in the inherited four-filter structure, both left and right competitive gaps must be positive.

Representative baseline responses are

$$
0.672634137,
\qquad
0.825428002,
$$

and the baseline calculation gives

$$
\Delta_L=\Delta_R=0.04669193039>0.
$$

Selection of $F_{DX}$ is retained in the nine inherited perturbation cases. For a finite perturbation $\rho$, one may use the stability condition that selection is preserved whenever the minimum gap remains sufficiently large, schematically

$$
\min\Delta > 4\rho.
$$

## 5.3 High-temperature limiting test

When only the thermal population is mixed toward a uniform high-$T$ limit, the frozen response rule does not send the gap to zero. A positive gap remains even for a uniform population.

Therefore

$$
\boxed{
\text{thermal population mixing alone}
\not\Rightarrow
\text{filter destruction}
}
$$

under the present implementation.

## 5.4 Meaning of the negative result

This is not a failed stage. It narrows the physical location of the missing mechanism. If high-to-low temperature evolution is to control filter stability, temperature must act on **response contrast, the metric, the readout structure, or an activation law**, rather than merely on carrier populations. That conclusion becomes the starting point of stage 0.4.

**Verdict: NEGATIVE RESULT PRESERVED.**

# 6. Stage 0.4 - Cooling and Filter Stabilization

## 6.1 Contrast order parameter

Take 1.0 as the center of the two filter responses and set the frozen contrast to

$$
\kappa_0=0.25.
$$

The two representative response positions are then

$$
1-\kappa_0=0.75,
\qquad
1+\kappa_0=1.25.
$$

Define the diagnostic coordinate

$$
m_F=\frac{\kappa}{\kappa_0}.
$$

At $m_F=0$, contrast vanishes and the competing filters are tied. At $m_F=1$, the frozen filter structure is recovered.

## 6.2 Gap at small contrast

In the small-$\kappa$ region, the calculated gap is approximately

$$
\Delta\approx1.56498\kappa^2.
$$

Substituting $\kappa=0.25m_F$ gives

$$
\Delta\approx0.0978113m_F^2.
$$

If the environmental perturbation scale is $\rho_{\mathrm{env}}$, the approximate order required to preserve filter selection may be written as

$$
m_{F,\mathrm{crit}}\approx6.395\sqrt{\rho_{\mathrm{env}}}.
$$

## 6.3 What is connected and what remains to be generated

This stage establishes the final three links in

$$
T\rightarrow m_F(T)\rightarrow\kappa(T)\rightarrow\Delta(T)\rightarrow F.
$$

That is, once $m_F$ is supplied, the route from contrast to filter gap and filter selection is calculable. The first arrow, $T\rightarrow m_F(T)$, still requires an independent physical generation law.

Accordingly, an arbitrary interpolation such as

$$
m_F=1-T/T_P
$$

is not inserted merely to force $T_F=T_P$. Doing so would amount to entering the desired boundary by hand rather than deriving a new physical law.

**Verdict: structural PASS. The absolute Kelvin law $T\rightarrow m_F$ is a follow-up research problem.**

# 7. Stage 0.5 - Residue, Return, and SOURCE Address Branching

## 7.1 Separating two kinds of filters

Stages 0.3-0.4 concern carrier/channel selection. SOURCE admission/return, which generates the present-universe address composition, is a separate operation. The two operations are therefore kept distinct:

- Filter A: carrier/channel selection
- Filter B: SOURCE address admission/return

This distinction becomes important when the component layer is inserted. Selecting a channel does not automatically imply that a source address has been admitted into phenotype.

## 7.2 Address weighting and branching rule

Let addresses run over $n=2,\ldots,N$ with weights

$$
w_n\propto n^{-\alpha}.
$$

The baseline calculation uses

$$
N=10^6,
\qquad
\alpha_0=1.8996876950554356,
\qquad
\beta_0=0.8654570124136961.
$$

Classifying the weighted sum gives the odd-composite weight

$$
O=0.05777294456,
$$

the even-composite weight

$$
E=0.268,
$$

and the prime weight

$$
P=0.6742270554.
$$

If a fraction $\beta$ of the odd-composite weight is admitted to phenotype, then

$$
\phi=\beta O=0.05,
$$

while the rejected odd-composite weight is

$$
O-\phi=0.00777294456.
$$

Return is therefore not a third independently fitted quantity. It follows from completeness:

$$
R=P+(O-\phi)=0.682.
$$

The resident Actual share is

$$
\phi+D=0.05+0.268=0.318.
$$

## 7.3 The 31.8% share is not an automatic recycling fixed point

A separate test asks whether $31.8\%$ becomes an automatic equilibrium when the SOURCE repeatedly releases the remaining stock. Under a representative repeated-release control, a release fraction of 0.2 applied over 32 cycles moves the cumulative branching to about $87.79\%$. If release is allowed indefinitely in the mathematical iteration, the cumulative release approaches 100%.

Thus the present $31.8\%$ Actual fraction is not an automatic fixed point of unlimited recycling. Maintaining a specific cosmic branching ratio therefore requires

$$
\boxed{\text{a finite generation window}}
$$

or another explicit balance closure.

## 7.4 Verdict

Address branching and completeness close at this stage. How $\alpha$, $\beta$, the admission shutter, and the generation window are set by an actual cosmic thermal history is a separate generation-law problem.

**Verdict: SOURCE address branching PASS.**

# 8. Stage 0.6 - Shutter, Event Discreteness, and Physical Time

## 8.1 Meaning of a frame

A WRRA frame is a finite execution unit ordered as

$$
\text{preparation}
\rightarrow
\text{transformation}
\rightarrow
\text{shutter}
\rightarrow
\text{record}.
$$

Here, "minimum" means a **readout event not further subdivided within the execution contract**, not a universal minimum physical time shared by the whole universe.

Four objects are kept distinct:

1. SOURCE frame index $k$,
2. readout shutter,
3. worldline proper time $\tau$,
4. Planck time $t_P$.

## 8.2 Inherited SI clock bridge and numerical scale

For the inherited electron mode,

$$
23\mu_E=22217.345682174\ \mathrm{eV}
$$

corresponds to the characteristic time

$$
t_\mu=2.962603932832\times10^{-20}\ \mathrm{s}.
$$

Applying the conditional resolution $\epsilon=0.05$ gives

$$
\Delta\tau_*
=1.481301966416\times10^{-21}\ \mathrm{s}.
$$

Relative to Planck time,

$$
\frac{\Delta\tau_*}{t_P}\approx2.75\times10^{22}.
$$

Under the separate SOURCE condition $\xi=0.1$, the time interval used is

$$
\Delta\tau_{\mathrm{source}}
=2.962603932832\times10^{-21}\ \mathrm{s}.
$$

## 8.3 The same frame unitary with different physical times

If only the dimensionless frame transformation is fixed, one may increase the generator rate and shorten the frame duration, or decrease the rate and lengthen the duration, while preserving the same unitary transformation. The frame index therefore does not determine a unique SI time interval.

Hence

$$
\boxed{
\text{event discreteness}
\neq
\text{physical-time discreteness}
}
$$

in the current implementation.

The baseline choice $K=8$ is an execution input, not a derivation that the universe possesses a universal shutter count of eight.

## 8.4 Verdict

**Finite shutter/readout event: PASS.**

Identifying a WRRA frame with Planck time is not required and is not supported by the present calculations. This separation motivates stage 0.7, where the micro-macro boundary is reformulated as a record-structure problem rather than as a universal time constant.

# 9. Stage 0.7 - Boundary Between Microscopic Uncertainty and Macroscopic Record

## 9.1 Two boundaries instead of one threshold

If the microscopic-macroscopic distinction is defined by one absolute number, it cannot naturally reflect the fact that the boundary depends on which observable is read, at what resolution, and with what tolerance. This study therefore uses two boundaries.

**Distinguishability boundary**

$$
B_D:
\quad
\text{Can different states be distinguished by different record projectors?}
$$

**Record-stability boundary**

$$
B_R(\delta):
\quad
\text{Is instability under repeated readout below the tolerance }\delta\text{?}
$$

The micro-macro interface is then defined as

$$
\boxed{
B_{\mu M}=B_D\cap B_R(\delta)
}
$$

rather than by one universal constant.

## 9.2 Address 9/15 and coarse/fine readout

The inherited 9/15 state pair is distinguishable under fine readout, while a coarse bin can place both addresses in the same record class. The same physical state information may therefore remain as internal coherence or be separated into distinct records depending on the readout partition.

The readout scaling $q$ is kept distinct from the projector itself. Numerical scaling of the displayed readout must not be confused with the partition structure that defines which states are distinguishable.

## 9.3 Repeated-shutter calculation

Let $K$ be the number of fine shutter events over a fixed total evolution interval. The transition probability is

$$
a_K=
\frac{1-\cos^K(2gs/K)}{2}.
$$

For the baseline $g=1$ and $s=1.2$, the values are:

| $K$ | $a_K$ |
|---:|---:|
| 1 | 86.869686% |
| 2 | 43.434843% |
| 4 | 26.799767% |
| 8 | 15.308671% |
| 16 | 8.264840% |
| 32 | 4.307302% |
| 64 | 2.200630% |
| 128 | 1.112503% |
| 256 | 0.559356% |
| 512 | 0.280461% |
| 1024 | 0.140428% |

For large $K$,

$$
a_K\sim\frac{1.44}{K}.
$$

The transition probability therefore decreases continuously as repeated fine readout increases.

## 9.4 Record-stability boundary as a function of tolerance

If record instability is required to stay below a tolerance $\delta$, the approximate minimum $K$ shifts as follows.

| tolerance $\delta$ | approximate minimum $K$ |
|---:|---:|
| 0.1 | 13 |
| 0.05 | 28 |
| 0.01 | 143 |
| 0.001 | 1,439 |
| 0.0001 | 14,399 |

The micro-macro boundary is therefore not best represented as one universal number. It is a **family of boundaries determined by the distinction being demanded and the stability tolerance being imposed**.

## 9.5 Separating decoherence from a unique record

Even when off-diagonal coherence disappears under a three-branch coarse shutter, the calculated purity remains

$$
\mathcal P=0.539448,
$$

and the diagonal population remains

$$
(0.05,0.268,0.682).
$$

The disappearance of coherence therefore does not automatically imply that one unique record has been selected.

$$
\boxed{
\text{decoherence}
\neq
\text{single selected record}
}
$$

This distinction leads directly to the stage-0.8 requirement that a component must preserve origin and ledger identity rather than merely correspond to a decohered branch.

**Verdict: micro/macro record interface PASS.**

# 10. Stage 0.8 - Component Activation Boundary and Primitive Alphabet

## 10.1 Why a component layer is needed before particle phenotype

If the upstream model moves directly into a final particle phenotype, there is no layer in which to represent the assembly order, origin identity, inactive reserve, and repeated-composition differences found in the Prime Parts studies. A component layer is therefore inserted before particle phenotype.

A component is defined here by four jointly required properties:

$$
\boxed{
\text{Component}
=
\text{origin}
+
\text{activation}
+
\text{identity retention}
+
\text{ledger closure}
}
$$

## 10.2 Component boundary

The structural component boundary can be written as

$$
B_C=B_D\cap B_{\mathrm{origin}}\cap B_{\mathrm{ledger}}.
$$

When the component must persist into a stable phenotype, repeated-record stability is also required:

$$
B_C^{\mathrm{persistent}}
=B_C\cap B_R(\delta).
$$

## 10.3 Origin-preserving transition

The inherited Prime Parts execution retains orthogonal origin tags through state transitions. For example,

$$
j:n\rightarrow j:D
$$

changes the current state label while preserving the origin $j$. In the control in which the origin tag is removed, the isometry test fails. Origin is therefore not merely a descriptive name. It is a degree of freedom required to preserve the history carried by the component.

## 10.4 Inactive reserve

A component that is not currently expressed in the phenotype is not treated as having disappeared.

$$
\boxed{
\text{inactive reserve}
=
\text{origin preserved, phenotype inactive}
}
$$

This separates the currently expressed phenotype from the larger pre-phenotype component inventory.

## 10.5 What Address 105 shows

Address 105 demonstrates that the same source address can produce different numbers of active component occurrences depending on assembly order.

| assembly order | active component occurrences |
|---|---:|
| small-first | 11 |
| big-first | 4 |

One therefore cannot conclude directly that there are four fundamental component types merely because one assembly path produces four active occurrences. The quantity four in this case is an **active occurrence count** associated with one assembly path.

Thus

$$
\boxed{
N_{\mathrm{active}}
\neq
N_{\mathrm{primitive}}
}
$$

in general.

## 10.6 Primitive hierarchy

The minimum hierarchy is written as

$$
A_{N_P}=\{b_1,\ldots,b_{N_P}\},
$$

for the primitive alphabet,

$$
C_j=G(\text{sequence, order, phase, repetition}),
$$

for the origin/code layer, and

$$
P=\mathcal R(C_1,C_2,\ldots)
$$

for the final particle phenotype.

Within this hierarchy, prime labels may be used as address rules at the component/origin layer, but primality itself is not automatically asserted to be the fundamental primitive alphabet.

## 10.7 Exact status of the four-primitive candidate

Under the additional assumption of a code with two independent positions,

$$
4^2=16
$$

is an interesting candidate relation. However, the same 16-state capacity can also be generated by another grammar such as $2^4$, while a three-symbol alphabet with code length three has capacity $3^3>16$. The present data therefore do not uniquely fix $N_P=4$.

Likewise, the inherited common-carrier inventory contains 15 base channels and permits a conditional 16th neutral extension. That statement is not equivalent to the claim that the universe fundamentally contains 16 primitive component types.

**Verdict: Component Activation Boundary PASS. The size of the primitive alphabet remains a follow-up output target.**

# 11. Stage 0.9 - Cooling, Stable Codewords, and Harmonic States

## 11.1 Cooling suppresses reverse transitions rather than creating components from nothing

After stage 0.8 defines the existence conditions for a component, stage 0.9 interprets the role of cooling not as "creating components from nothing" but as **suppressing reverse transitions and stabilizing allowed assemblies**.

If the reverse barrier of state $j$ is $\Delta E_j$, one may use the diagnostic relation

$$
P_{\mathrm{reverse},j}
\sim
\exp\left[-\frac{\Delta E_j}{k_BT}\right].
$$

For a tolerated reverse probability $\delta$, define the state-dependent stability scale

$$
T_j(\delta)
=
\frac{\Delta E_j}{k_B\ln(1/\delta)}.
$$

This is not a prediction of the actual cosmic temperature history. It is a diagnostic showing how much thermal suppression is required for a given barrier and tolerance.

## 11.2 Examples of state-dependent barriers

Inherited reference barriers already span substantially different scales, for example the deuteron scale $2.22588559\,\mathrm{MeV}$ and the $\alpha\rightarrow d+d$ breakup scale $23.92275894\,\mathrm{MeV}$. This supports the use of state-dependent stability boundaries rather than the assumption that every component locks simultaneously at one universal $T_C$.

## 11.3 Distinguishing stable codewords from harmonic states

A **stable codeword** is defined as an assembly satisfying three conditions:

1. its origin is distinguishable,
2. reverse transitions are sufficiently suppressed,
3. its assembly identity is maintained under repeated record formation.

A **harmonic state**, by contrast, contains multiple eigenmodes while preserving relative-phase information. Such a state is more naturally represented by a multi-mode phase ledger than by one fixed component codeword.

## 11.4 Phase ledger of the neutrino $0:5:29$ structure

The existing WRRA neutrino candidate is retained:

$$
(n_1,n_2,n_3)=(0,5,29).
$$

The basic mass quantum is

$$
q_\nu=1.725929280\ \mathrm{meV}.
$$

Therefore

$$
m_1=0,
$$

$$
m_2=5q_\nu=8.6296464\ \mathrm{meV},
$$

and

$$
m_3=29q_\nu=50.0519491\ \mathrm{meV}.
$$

Their sum is

$$
\sum m_\nu=58.6815955\ \mathrm{meV}
\approx58.6816\ \mathrm{meV}.
$$

The common rest-phase recurrence is

$$
T_\Phi\approx2.39619\times10^{-12}\ \mathrm{s},
$$

and over this interval the three modes accumulate respectively

$$
0,
\quad5,
\quad29
$$

integer phase cycles. Thus $0:5:29$ is not merely a list of three numbers; it is an integer phase ledger defined on a common recurrence interval.

## 11.5 What is claimed and what is not yet claimed

This result provides an internal basis for representing the neutrino state harmonically. It does not identify the rest-phase recurrence directly with an observable flavor-oscillation period. Nor does it claim that the microscopic origin of the PMNS mixing matrix has already been generated from primitive grammar.

A diagnostic ratio such as

$$
\Lambda=\frac{\Gamma_R}{\Delta f_{ij}}
$$

may be useful for characterizing the boundary between codeword locking and harmonic coherence, but it is not fixed here as a universal law.

**Verdict: stable-codeword/harmonic interface PASS.**

# 12. Stage 0.10 - Reconnecting Phenotype Energy to Downstream Gravity

## 12.1 The central conservation rule

After adding the component and harmonic layers, the first required test is energy nonduplication. Finer internal structure must not increase the total cosmic energy merely because more internal labels exist.

The conserved normalization rule is therefore

$$
\boxed{
\sum_{g,j}E_{\phi,g,j}=E_\phi
}
$$

where $g$ may label generation and $j$ a component/channel slot. The inherited 48-slot routing uses normalized weights, and its sum returns to the existing $E_\phi$.

## 12.2 Reserve and harmonic phase are not new cosmic sectors

Inactive reserve is component inventory not currently expressed in phenotype. It is not a fourth cosmic fraction added to ordinary matter, resident nonphenotype, and return. Likewise, a harmonic phase register increases internal state information but does not automatically increase population or total energy.

Therefore

$$
\text{more components/channels/generations/phases}
\not\Rightarrow
\text{more cosmic energy}.
$$

## 12.3 Separating internal rearrangement from real population change

If only labels or phases are rearranged within the same $E_\phi$, the baseline $q_0$, rotation, and lensing outputs should remain unchanged. If the SOURCE generation rule actually changes the phenotype population, however, the downstream pressure and load should change and $q$ should respond.

To test this, the generation control is varied while the SI coefficients are kept frozen.

| upstream control | phenotype fraction | downstream $q$ |
|---:|---:|---:|
| $K=4$ | 3.704794619% | -0.547908522 |
| $K=8$ | 5.000000000% | -0.528550000 |
| $K=16$ | 5.682473858% | -0.518343025 |

These values are not obtained by refitting the coefficients to a target output. The upstream population moves, passes through the same frozen downstream mapping, and produces a corresponding change in $q$.

The sensitivity chain is therefore

$$
\boxed{
\text{upstream population change}
\rightarrow
\text{same }E(V)
\rightarrow
P
\rightarrow
\text{load}
\rightarrow
q
}
$$

and exists explicitly within the model.

## 12.4 Relation to inherited local and global outputs

At the baseline state $K=8$, the frozen outputs remain

$$
q_0=-0.52855,
$$

$$
v_{\mathrm{rot}}=207.5109051266\ \mathrm{km\,s^{-1}},
$$

and

$$
\theta_{\mathrm{lens}}=0.5355865106^{\prime\prime}.
$$

Internal relabeling or phase rearrangement alone should not move these values. A genuine change in population or in the energy ledger, by contrast, should propagate through the same downstream rule.

**Verdict: upstream-downstream structural reconnection PASS.**

# 13. Stage 0.11 - Reverse Minimality Audit

## 13.1 Reversing the question

Stages 0.1-0.10 proceed from high-energy conditions toward phenotype and downstream physics. Stage 0.11 reverses the direction and asks which ingredients cannot be removed while preserving the current calculations.

The minimum interface required by the present executable structure is summarized as

$$
\boxed{
G_{\min}=\{A_{N_P},O,B_L,B_R,R,\Phi,L\}
}
$$

with the following roles.

| Symbol | Meaning | Failure when removed |
|---|---|---|
| $A_{N_P}$ | primitive alphabet | minimum symbol space for assembly disappears |
| $O$ | origin identity | component history/isometry breaks |
| $B_L,B_R$ | independent filter distinctions | independent filter discrimination disappears |
| $R$ | assembly/termination rule | the assembly result for a given address is not determined |
| $\Phi$ | phase register | harmonic multi-mode representation disappears |
| $L$ | conservation/normalization ledger | energy and population may be duplicated |

## 13.2 Origin is required

Without origin, different histories cannot be distinguished by the current state label alone, and the inherited isometry control fails. Preserving component identity therefore requires $O$.

## 13.3 Assembly order and termination rule are required

Address 105 produces different active component profiles under different assembly orders. An alphabet alone is therefore insufficient to determine the result. At minimum, order and a termination rule are also required.

## 13.4 Harmonic interpretation requires a phase register

To preserve relative-phase structure in a multi-mode state such as the neutrino $0:5:29$ configuration, $\Phi$ cannot be removed. The need for a phase register, however, does not by itself determine the primitive count.

## 13.5 What is not a required assumption

Removing the assumption $N_P=4$ does not destroy the current component boundary, codeword/harmonic interface, energy normalization, or downstream sensitivity. Four primitive types are therefore not yet a necessary premise.

Likewise, removing the identification of the WRRA frame with Planck time leaves the executed results intact. Planck-time identification is not part of the minimum structure.

The three neutrino modes may imply a spectral capacity of at least three, but spectral-mode capacity is not identical to the number of primitive component types. The two counts remain distinct.

**Verdict: reverse/minimality constraints PASS.**

# 14. Stage 0.12 - Closing the Master Ledger

## 14.1 One typed chain

The results obtained in stages 0.1-0.11 are finally placed into the following chain:

$$
\boxed{
\begin{aligned}
\text{high-energy Actual}
&\rightarrow \text{finite thermal probe}\\
&\rightarrow \text{filter/readout}\\
&\rightarrow \text{SOURCE admission/return}\\
&\rightarrow \text{shutter + conditional record}\\
&\rightarrow B_D\cap B_R(\delta)\\
&\rightarrow \text{origin-preserving component}\\
&\rightarrow \text{stable codeword or harmonic state}\\
&\rightarrow \text{phenotype}\\
&\rightarrow \text{normalized SI energy}\\
&\rightarrow \text{pressure/information load}\\
&\rightarrow \text{twist/gravity/expansion}.
\end{aligned}
}
$$

## 14.2 Closed interfaces

The interfaces judged closed at stage 0.12 are listed below.
| No. | Interface | What is closed |
|---:|---|---|
| 1 | finite thermal probe | finite thermal state defined by $T,H,E_0$ |
| 2 | SOURCE branching | phenotype/resident/return completeness |
| 3 | shutter/readout | finite conditional record event |
| 4 | micro/macro | record boundary $B_D\cap B_R(\delta)$ |
| 5 | component | origin-preserving activation/reserve accounting |
| 6 | codeword/harmonic | distinction between stable assembly and multi-mode phase |
| 7 | phenotype -> SI energy | normalized allocation without energy duplication |
| 8 | energy -> pressure | pressure calculated from the same $E(V)$ |
| 9 | upstream -> $q$ | downstream propagation of a genuine population perturbation |
| 10 | local gravity | retained conditional rotation/lensing outputs |
| 11 | homogeneous expansion | macroscopic output of the frozen energy-pressure ledger |

## 14.3 What stage 0.12 closes is the research scope

Closure at stage 0.12 does not mean that every microscopic origin in the universe has already been derived. The question closed by this study is narrower and explicit:

> Can high-energy states be connected through records, components, and phenotypes to the existing WRRA M energy-gravity ledger as one executable structure without mixing types, duplicating energy, or retuning the frozen downstream model?

The answer produced by stages 0.1-0.12 is **yes**.

The final verdict is therefore

$$
\boxed{
\textbf{WRRA M 0.1-0.12 Structural Integration 1.0 - CLOSED}
}
$$

# 15. Structures Newly Secured by the Integrated Study

## 15.1 A component layer now exists between upstream generation and downstream physics

The earlier simplified flow could be read as

$$
\text{carrier/filter}
\rightarrow
\text{phenotype}
\rightarrow
\text{downstream physics}.
$$

After the present study, the structure becomes

$$
\boxed{
\text{carrier/filter}
\rightarrow
\text{record}
\rightarrow
\text{component}
\rightarrow
\text{codeword/harmonic}
\rightarrow
\text{phenotype}
\rightarrow
\text{downstream physics}
}
$$

The detailed Prime Parts assemblers have not all been absorbed into the WRRA M core. Nevertheless, the **origin-preserving component ontology** identified in Prime Parts now functions as a formal bridge between upstream generation and downstream phenotype physics.

## 15.2 Negative results narrowed the structure

Two important hypotheses were not adopted.

First,

$$
\text{high }T
\Rightarrow
\text{population mixing}
\Rightarrow
\text{filter collapse}
$$

does not hold under the current frozen rule.

Second,

$$
\text{WRRA frame}=t_P
$$

is not required by the current calculation.

These negative results do not weaken the research. They more precisely locate where filter dynamics and clock dynamics must enter the architecture.

## 15.3 The micro-macro boundary is recast as a record problem

Rather than assigning the microscopic-macroscopic transition to one length, time, or mass constant, the study places it at

$$
B_D\cap B_R(\delta).
$$

This incorporates directly into the structure the fact that the boundary can move with measurement resolution and tolerance.

## 15.4 Harmonic structure is a phase ledger rather than a metaphor

The neutrino $0:5:29$ structure is organized not merely as a musical analogy but as integer cycles on a common rest-phase recurrence. "Harmonic" therefore has a concrete phase-bookkeeping meaning inside the model.

## 15.5 Growth of internal structure is separated from growth of cosmic energy

Even when the numbers of components, channels, generations, or harmonic modes increase,

$$
\sum E_{\phi,g,j}=E_\phi
$$

is preserved. This rule prevents increasing internal state-space complexity from being misread as an automatic increase in the cosmic energy budget.

# 16. Integrated Falsification Conditions

This study closes a structural chain while also stating the conditions under which a connection must be revised or rejected.

| Category | Falsification condition |
|---|---|
| probability/state | failure of trace, positivity, or branch completeness |
| conservation | failure of $Q/B/L/E$ or of declared normalization |
| filter | the same unique filter remains selected after contrast is removed |
| component | identical component history and isometry remain fully preserved after origin is removed |
| record | increasing $K$ produces a trend opposite to the declared stability behavior |
| energy | total cosmic energy increases merely with component/channel/generation/harmonic count |
| bridge | a genuine upstream population change produces no response in frozen downstream output |
| clock | proper-time and phase units contradict one another within the same ledger |
| observation | future observations under matched preparation significantly disagree with a conditional output |

A crucial distinction is maintained between an unresolved follow-up question and a falsification of a completed result. For example, the fact that a physical particle Hamiltonian has not yet been generated from primitive grammar is not a falsification of the stage-0.8 component boundary. Falsification occurs when the declared boundary violates its own input-output contract.

# 17. Research Questions After Stage 0.12

Once stages 0.1-0.12 are closed, four research axes remain. They are not a failure list for the present work; they are independent next-stage problems demanded by the closed structure.

## 17.1 From temperature to generation controls

There is not yet a physical generation law

$$
T\rightarrow\{\kappa,\alpha,\beta,K_*\}.
$$

Deriving such a law would directly connect thermal history to filter contrast, address admission, and the generation window.

## 17.2 From primitive grammar to a particle Hamiltonian

The component and assembly grammar are structurally defined, but a separate study is still required for

$$
\text{primitive grammar}
\rightarrow
H_{\mathrm{particle}}.
$$

Closing this adapter would complete, at executable-code level, the connection between Prime Parts assembly structure and the inherited internal Hamiltonian.

## 17.3 From $0:5:29$ to flavor dynamics

An integer phase ledger currently exists. The next question is how that phase structure appears as an observable flavor-mixing dynamics through an interaction/readout grammar:

$$
0:5:29
\rightarrow
\text{mixing dynamics}.
$$

## 17.4 Common SI geometry for homogeneous background and nonuniform local states

Homogeneous expansion and conditional local gravity are already connected in the same broad ledger, but an executable model that evolves background and nonuniform states simultaneously in one fully covariant SI geometry remains a separate research task.

# 18. Relation to Minimal Computation Cosmology 3.0

The 0.1-0.12 integration does more than add one new number to MCC 2.3.2. It fixes a new intermediate layer in the generation flow of the universe and therefore provides structural groundwork for version 3.0.

If the compact 2.3.2 flow is written as

$$
\text{common carrier}
\rightarrow
\text{filter}
\rightarrow
\text{phenotype}
\rightarrow
\text{forces/cosmology},
$$

the present architecture is

$$
\boxed{
\text{SOURCE/Actual}
\rightarrow
\text{filter}
\rightarrow
\text{record}
\rightarrow
\text{component}
\rightarrow
\text{codeword/harmonic}
\rightarrow
\text{phenotype}
\rightarrow
\text{energy/load}
\rightarrow
\text{gravity/expansion}
}
$$

The next major MCC revision should therefore not attach this research merely as an appendix. It is more natural to rewrite the **record/component layer** as a formal part of the core architecture following the common carrier.

# 19. Conclusion

This study fills the missing intermediate structure between the high-energy upstream side of WRRA M and the established phenotype-to-downstream physics through a staged 0.1-0.12 examination.

Stage 0.1 freezes the inherited cosmic ledgers and forbids retuning. Stage 0.2 converts temperature into a finite thermal probe, and stage 0.3 rejects the hypothesis that thermal population mixing alone removes the filter gap. Stage 0.4 constructs a filter-stabilization structure through a contrast order coordinate. Stage 0.5 separates channel selection from SOURCE branching, closes the $5\%/26.8\%/68.2\%$ address ledger through completeness, and shows that a finite generation window is required rather than unlimited recycling.

Stage 0.6 retains the frame as a record event while separating it from a universal minimum physical time. Stage 0.7 defines the micro-macro boundary as $B_D\cap B_R(\delta)$ and quantifies the record-stability crossover through repeated-shutter calculations. Stage 0.8 introduces the origin-preserving component as a formal bridge, connecting Prime Parts to the upstream-downstream integration. Stage 0.9 distinguishes stable assemblies from harmonic states and organizes the neutrino $0:5:29$ structure as a concrete integer phase ledger.

Stage 0.10 preserves normalized phenotype energy so that richer internal structure does not generate extra cosmic energy, while confirming that a genuine upstream population change propagates into the frozen downstream $q$. Stage 0.11 identifies the minimum interface required by the current execution through a reverse audit. Stage 0.12 integrates all of these connections into one Master Ledger.

The conclusion of the study is therefore summarized by one statement:

$$
\boxed{
\textbf{WRRA M 0.1-0.12 Structural Integration 1.0 - CLOSED}
}
$$

Here, CLOSED does not mean that there are no further research questions. It means that the starting points of the next questions are now explicit. The subsequent research axes are the law generating filter/admission/generation controls from temperature, the law generating a particle Hamiltonian from primitive grammar, the law connecting the $0:5:29$ phase ledger to flavor mixing, and a common covariant SI geometry for homogeneous and nonuniform states.

A central achievement of the integration is that these next-stage questions are not mixed into the completed 0.1-0.12 results. They are separated as the next interfaces of an already closed structural chain.

# Appendix A. Stage-by-Stage Verdict Ledger

| Stage | Core question | Main output | Verdict |
|---|---|---|---|
| 0.1 | What must be frozen? | address/energy/downstream baseline | PASS |
| 0.2 | How is temperature entered into a state? | finite thermal probe | PASS |
| 0.3 | Does high-$T$ mixing erase the filter? | gap remains positive | NEGATIVE RESULT |
| 0.4 | How are cooling and filter selection connected? | $m_F\rightarrow\kappa\rightarrow\Delta$ | PASS |
| 0.5 | How do addresses branch? | $\phi/D/R=0.05/0.268/0.682$ | PASS |
| 0.6 | Is a frame a minimum physical time? | event/physical-time separation | PASS |
| 0.7 | What is the micro/macro boundary? | $B_D\cap B_R(\delta)$ | PASS |
| 0.8 | What is a component? | origin-preserving component | PASS |
| 0.9 | How are stable states represented? | codeword/harmonic | PASS |
| 0.10 | How is the component layer reconnected downstream? | normalized energy + $q$ sensitivity | PASS |
| 0.11 | What is minimally required? | $G_{\min}$ | PASS |
| 0.12 | Does the whole chain close in one ledger? | Master Ledger | CLOSED |

# Appendix B. Core Numerical Ledger

| Quantity | Value |
|---|---:|
| uncalibrated phenotype residue | 4.876893353% |
| address phenotype | 5.0% |
| address resident nonphenotype | 26.8% |
| address return | 68.2% |
| inherited energy phenotype | 4.93% |
| inherited energy resident | 26.5% |
| inherited energy return | 68.57% |
| internal gap $\Delta E$ | 431.081244315 MeV |
| conditional excitation contribution | 34.4764357391 MeV |
| filter gap $\Delta_L=\Delta_R$ | 0.04669193039 |
| SOURCE $\alpha_0$ | 1.8996876950554356 |
| SOURCE $\beta_0$ | 0.8654570124136961 |
| odd-composite weight $O$ | 0.05777294456 |
| even-composite weight $E$ | 0.268 |
| prime weight $P$ | 0.6742270554 |
| proper-time step $\Delta\tau_*$ | $1.481301966416\times10^{-21}$ s |
| neutrino quantum $q_\nu$ | 1.725929280 meV |
| neutrino mass sum | 58.6816 meV |
| common rest-phase recurrence | $2.39619\times10^{-12}$ s |
| baseline $q_0$ | -0.52855 |
| reference rotation | 207.5109051266 km/s |
| conditional lensing | 0.5355865106 arcsec |

# Appendix C. Reproducibility and Public Records

This study is written on the public provenance chain of the following WRRA records.

- WRRA M Integrated Upstream and Downstream Model 1.0 r1 - DOI: 10.5281/zenodo.23126800
- WRRA M Integrated Measurement Case 1.0 - DOI: 10.5281/zenodo.23149260
- WRRA Prime Parts 0.1-0.12 Reviewed Collection - DOI: 10.5281/zenodo.23134716
- WRRA Address 105 Prime Parts Case Study - DOI: 10.5281/zenodo.23137504
- WRRA M High-Energy-to-Phenotype Extension 1.0 - DOI: 10.5281/zenodo.23176529

GitHub integration path:

`https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/main/integrated/high_energy_extension_v1_0`

This detailed integrated research manuscript expands the stage-by-stage calculations, negative results, intermediate ledgers, and connection logic of the existing 1.0 release. The original provenance of the sole-author Prime Parts public releases and the coauthored WRRA M public releases is preserved.