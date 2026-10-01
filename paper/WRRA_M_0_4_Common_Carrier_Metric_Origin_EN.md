---
title: "WRRA-M 0.4 Common-Carrier Metric Origin of Filter Compatibility"
subtitle: "Fifteen-to-Sixteen-Channel Extension, Null-Lift Criterion, and Exact Selection-Gap Identities"
author: "Wonsik Choi"
date: "1 October 2026"
lang: en-US
---

| Metadata | Value |
|---|---|
| Author | Wonsik Choi |
| ORCID | 0009-0001-4263-9772 |
| Email | janefather@gmail.com |
| Version | WRRA-M 0.4-r1 |
| Date | 1 October 2026 |
| Status | Conditional common-carrier extension theorem |

# Research decision

WRRA-M 0.4 imports one existing structure from Minimal Computation Cosmology: the common carrier. It does not import the older fifteen-channel result as if it already solved the sixteen-channel problem. The version first identifies the additional condition required to carry the gauge-neutral sixteenth channel, then uses common-carrier response geometry to replace the free compatibility entries of WRRA-M 0.3 by one fixed scalar rule. The scope ends at exact gap identities and a constructibility witness. It does not claim that a physical microscopic carrier has already supplied the required positive gaps.

# Abstract

WRRA-M 0.2 reorganized one invariant channel, two seven-dimensional sectors, and one null channel into the sixteen left-handed Weyl channels of a Pati-Salam generation, including the conjugate right-handed neutrino. WRRA-M 0.3 proved that the target filter is selected uniquely in a four-filter sector exactly when two compatibility gaps are positive, but it left the compatibility tables physically unspecified. Version 0.4 tests whether the common carrier of Minimal Computation Cosmology can supply that missing structure. The answer is conditionally yes. The established fifteen-channel carrier can be extended to a sixteen-channel carrier if the added neutral channel shares the same principal transport geometry, has positive carrier norm, and remains null only to the gauge-current owner rather than to transport itself. A positive common-carrier response metric then defines each pairing compatibility as the negative squared response mismatch. Under this single rule, the two free selection gaps reduce exactly to two carrier-metric alignment products. Their signs decide the same target filter as in 0.3. An exact finite witness shows that the admissible positive-gap region is nonempty. The numerical response signatures and their microscopic physical origin remain open.

# Result in one sentence

The existing common carrier can be used in WRRA-M 0.4 if its fifteen-channel transport is extended by a transported but gauge-neutral sixteenth channel; after that extension, one carrier-induced positive metric converts the two 0.3 selection gaps into exact alignment tests.

# Scope and stopping line

Version 0.4 closes a structural bridge, not the final physical calculation. It asks whether one already developed WRRA transport object can own the scalar compatibility rule required by 0.3.

## Included in 0.4

- The exact distinction between a gauge-null channel and a transport-null vector
- A conditional extension of the common carrier from fifteen to sixteen channels
- A positive common-carrier response metric
- One non-circular scalar rule for every left and right pairing compatibility
- Exact identities reducing the two selection gaps to carrier-metric alignments
- An exact finite witness and machine-checked algebra
- Explicit failure conditions and a fixed next calculation

## Reserved for 0.5 or later

- Numerical response signatures calculated from a microscopic Bessel, Jacobi, compactification, or other carrier
- Proof that the four-filter sector is complete in a deeper theory
- Three generations, Yukawa structure, masses, mixing, or symmetry breaking
- Gravity, dark matter, cosmology, or consciousness

# Fixed WRRA evaluation rule

| Stage | Question answered in this note |
|---|---|
| Verification input | Which results from WRRA-M 0.2, WRRA-M 0.3, and Minimal Computation Cosmology are held fixed |
| WRRA-specific transformation | How common transport responses become scalar pairing compatibilities and two gap values |
| Output | Whether a sixteen-channel carrier is structurally admissible and which exact carrier conditions select the target filter |
| Falsification condition | Which rank, causal-cone, null-lift, positivity, gap-sign, or protocol failure rejects the 0.4 bridge |

# Verified inputs

## The sixteen-channel filter problem

WRRA-M 0.2 fixed the input space

$$
\mathcal C_{16}=\mathbf 1_0\oplus\mathbf 7_A\oplus\mathbf 7_B\oplus\mathbf 1_N
$$

and conditionally reorganized it as

$$
\mathcal C_{16}\longrightarrow(\mathbf 4,\mathbf 2,\mathbf 1)\oplus(\overline{\mathbf 4},\mathbf 1,\mathbf 2).
$$

The resulting left-handed inventory is

$$
\mathcal H_{16}=Q_L\oplus u_R^c\oplus d_R^c\oplus L_L\oplus e_R^c\oplus\nu_R^c.
$$

The channel descending from $\mathbf 1_N$ is assigned to $\nu_R^c$ after filtering. It is neutral under the Standard-Model gauge currents, but neutrality does not by itself make it the zero vector of the transported state space.

## The four-filter selection problem

WRRA-M 0.3 fixed

$$
\mathcal F_4=\{F_{DX},F_{XX},F_{DD},F_{XD}\}
$$

and the two gaps

$$
\Delta_L=(\ell_{AA}+\ell_{BB})-(\ell_{AB}+\ell_{BA}),
$$

$$
\Delta_R=(r_{AN}+r_{B0})-(r_{A0}+r_{BN}).
$$

Within this fixed class, $F_{DX}$ is the unique maximizer if and only if $\Delta_L>0$ and $\Delta_R>0$.

## The existing fifteen-channel common carrier

Minimal Computation Cosmology defined the common carrier as a transport structure shared by the fifteen chiral components of one minimal Standard-Model generation:

$$
D_C^{(15)}:\bigoplus_{i=1}^{15}\mathcal H_i\longrightarrow\bigoplus_{i=1}^{15}\mathcal H_i.
$$

Its commonality is not identical particle content. The channels retain their representations and selection rules while sharing a local transport skeleton, principal kinematics, and boundary-recording rule. The relevant surviving constraints are:

1. the transported band must not leave physical channel directions dark;
2. carrier dependence must not split the principal causal cone;
3. channel differences may enter through lower-order gauge-covariant phenotype operators;
4. full abstract rank must not be confused with mass generation, particle occupancy, or an interacting Standard-Model completion.

# Conditional extension from fifteen to sixteen channels

Define

$$
\mathcal H_{16}=\mathcal H_{15}\oplus\mathcal H_N,
$$

where $\mathcal H_N$ is one complex left-handed Weyl channel that becomes $\nu_R^c$ under the 0.2 filter. A sixteen-channel extension is an operator

$$
D_C^{(16)}:\mathcal H_{16}\longrightarrow\mathcal H_{16}
$$

whose principal transport operator is common to all sixteen channel directions.

In the microscopic notation already proposed in Minimal Computation Cosmology, the corresponding conditional identification is

$$
D_C^{(16)}:=P_{16}\,\operatorname{Red}_{K}\!\left[\mathcal D_{\mathrm{micro}}\right]P_{16}.
$$

This equation does not assert that one particular compactification or microscopic theory is correct. It states the ownership requirement: the sixteen visible channels must be reductions of one operator rather than sixteen unrelated transport laws.

## Sixteen-channel carrier conditions

Let $\sigma_{\mathrm{pr}}(D_C^{(16)})(\xi)$ denote the principal symbol and let $G_{16}(I)$ be the carrier response Gram operator on a declared band $I$. The extension is admitted in 0.4 only if

$$
\frac{\partial\,\sigma_{\mathrm{pr}}}{\partial\,\text{channel}}=0,
\qquad
G_{16}(I)\succeq0,
\qquad
\operatorname{rank}G_{16}(I)=16.
$$

The first condition preserves one principal causal geometry. The second supplies a nonnegative response metric. The third blocks a dark transported direction.

## Null-lift criterion

The decisive distinction begins with gauge-current neutrality:

$$
J_1[N]=J_2[N]=J_3[N]=0.
$$

This does not imply absence from common transport. If the filtered $\mathbf 1_N$ is to become a physical $\nu_R^c$ channel, 0.4 instead requires

$$
\lVert N\rVert_C^2>0.
$$

Thus the word *null* is retained only as gauge-current neutrality before phenotype assignment. It cannot mean the zero Hilbert-space vector or the kernel of the common carrier.

## Anomaly preservation

Adding a channel with

$$
(SU(3),SU(2),Y)=(\mathbf 1,\mathbf 1,0)
$$

adds zero to every perturbative gauge anomaly, the mixed gauge-gravitational anomaly, and the global $SU(2)$ parity count. The fifteen-to-sixteen extension therefore changes the transport inventory without changing the anomaly sums already closed in 0.2.

# Common-carrier response metric

Let $u_i(\omega)$ be the response signature of channel origin $i$ under the same carrier on a fixed band $I$. Let $W(\omega)$ be a positive semidefinite weight fixed without using the desired filter output. Define

$$
\langle u,v\rangle_C
=\int_I\rho(\omega)\,u(\omega)^\dagger W(\omega)v(\omega)\,d\omega,
\qquad \rho(\omega)\ge0,\quad W(\omega)\succeq0.
$$

The induced squared mismatch is

$$
d_C^2(i,j)=\lVert u_i-u_j\rVert_C^2.
$$

Version 0.4 fixes every scalar pairing compatibility by one rule:

$$
c_C(i,j)=-d_C^2(i,j).
$$

Higher score means smaller mismatch under common transport. This is a scalar comparison of gauge-invariant response signatures. It is not a linear map that mixes a color triplet with a singlet, so the common $SU(3)$ action remains unchanged.

The score also has a direct least-mismatch interpretation. Pairing two channel origins incurs the quadratic carrier cost required to make their boundary responses agree. The filter receives the negative sum of those costs.

# Exact carrier-gap theorem

Assign the left compatibility entries by

$$
\ell_{ij}=-\lVert u_{3_i}-u_{1_j}\rVert_C^2,
\qquad i,j\in\{A,B\},
$$

and the right entries by

$$
r_{ij}=-\lVert u_{\bar3_i}-u_{1_j}\rVert_C^2,
\qquad i\in\{A,B\},\quad j\in\{N,0\}.
$$

Then the 0.3 gaps satisfy the exact identities

$$
\Delta_L
=2\,\operatorname{Re}\left\langle
u_{3_A}-u_{3_B},\,
u_{1_A}-u_{1_B}
\right\rangle_C,
$$

$$
\Delta_R
=2\,\operatorname{Re}\left\langle
u_{\bar3_A}-u_{\bar3_B},\,
u_{1_N}-u_{1_0}
\right\rangle_C.
$$

## Proof

Expand each squared norm with

$$
\lVert x-y\rVert_C^2
=\lVert x\rVert_C^2+\lVert y\rVert_C^2
-2\operatorname{Re}\langle x,y\rangle_C.
$$

In each gap, all four self-norm terms cancel. The remaining cross terms factor into the two difference-vector inner products displayed above. No approximation is used.

## Selection consequence

Combining the exact identities with the 0.3 selection theorem gives

$$
F_{DX}\text{ is unique}
\Longleftrightarrow
\begin{cases}
\operatorname{Re}\langle u_{3_A}-u_{3_B},u_{1_A}-u_{1_B}\rangle_C>0,\\
\operatorname{Re}\langle u_{\bar3_A}-u_{\bar3_B},u_{1_N}-u_{1_0}\rangle_C>0.
\end{cases}
$$

The formerly free signs now have a concrete meaning. The target filter wins exactly when the two pairs of carrier-response differences have the same orientation in the common positive metric.

# Exact finite witness

The theorem is not empty. In a two-dimensional Euclidean carrier-response space, choose

| Response signature | Vector |
|---|---:|
| $u_{3_A}$ and $u_{1_A}$ | $(1,0)$ |
| $u_{3_B}$ and $u_{1_B}$ | $(-1,0)$ |
| $u_{\bar3_A}$ and $u_{1_N}$ | $(0,1)$ |
| $u_{\bar3_B}$ and $u_{1_0}$ | $(0,-1)$ |

With $W=I$, the left direct assignment and right crossed assignment each have zero mismatch. Each swapped assignment has total squared mismatch eight. Therefore

$$
\Delta_L=8,
\qquad
\Delta_R=8,
$$

and the four total filter scores are

| Filter | Exact score |
|---|---:|
| $F_{DX}$ | $0$ |
| $F_{XX}$ | $-8$ |
| $F_{DD}$ | $-8$ |
| $F_{XD}$ | $-16$ |

This witness proves only constructibility and nonemptiness of the positive-gap region. It is not a witness for $\operatorname{rank}G_{16}=16$, which remains a separate carrier-extension requirement. It is not evidence that nature has these signatures. A physical test must calculate the signatures from an independently frozen carrier.

Relation to 0.5. The gaps of eight in this constructed witness and the zero gaps of the symmetric carrier actually tested in 0.5 are compatible: they use different response assignments. The former establishes possibility; the latter shows that the tested symmetric carrier does not select the target. Applying the 0.3 dynamical convergence result additionally requires eta > 0 and nonzero initial target support.

# Non-circular calculation protocol

1. Fix one admissible sixteen-channel carrier and the band $I$ without looking at the recovered particle charges.
2. Verify one principal causal cone, gauge covariance, $G_{16}(I)\succeq0$, full rank sixteen, and positive norm of the neutral channel.
3. Fix the response extraction map, $\rho$, and $W$ before inspecting either gap.
4. Calculate all eight channel-origin response signatures.
5. Construct the eight scalar compatibility entries with the single negative-squared-distance rule.
6. Publish $\Delta_L$, $\Delta_R$, uncertainty bounds, and the selected filter without relabeling channel origins.
7. Apply the unchanged 0.3 convergence and perturbation tests.

Known particle assignments may calibrate the response map, band, or metric as part of legitimate model construction. Record that calibration separately from selection calculated from carrier responses frozen before the target check. After the calibration is fixed, the mismatch rule still yields exact conditional scores and gaps. A later fit to the same target is not an independent carrier-selection test.

# Claim ledger

| Code | Status | Statement in WRRA-M 0.4 |
|---|---|---|
| E | Verified input | The 0.2 sixteen-channel mapping, the 0.3 four-filter theorem, and the existing fifteen-channel common-carrier constraints |
| D | Architecture definition | The sixteen-channel extension, null-lift criterion, carrier response metric, and one mismatch score rule |
| T | Exact theorem | Both 0.3 gaps equal twice a carrier-metric alignment product |
| T | Exact theorem | Adding a gauge-singlet zero-hypercharge channel leaves the stated anomaly sums unchanged |
| C | Conditional result | The existing common carrier is usable if the neutral channel has common principal transport and positive carrier norm |
| W | Constructibility witness | One exact finite response assignment gives $\Delta_L=\Delta_R=8$ and selects $F_{DX}$ uniquely |
| H | Unproved physical hypothesis | A microscopic carrier supplies independently fixed signatures with both alignments positive |
| O | Outside this version | Numerical microscopic signatures, three generations, masses, gravity, cosmology, dark matter, and consciousness |

# Falsification conditions

The 0.4 bridge fails within its declared scope if any of the following occurs.

- The sixteenth channel is in the kernel of the common carrier or has zero carrier norm.
- Extending the carrier splits the principal causal cone by channel.
- The response Gram operator is not positive semidefinite or does not have rank sixteen on the declared band.
- The response signature or metric is not gauge invariant and therefore mixes inequivalent representations physically rather than comparing scalar records.
- An independently fixed carrier gives either alignment product less than or equal to zero.
- The metric, band, channel labels, or response extraction rule is changed after the target result is inspected.
- A broader admissible filter class contains a candidate with score at least as large as $F_{DX}$.

# Exact boundary

Version 0.4 does not calculate a physical numerical compatibility table from first principles. It proves that the common carrier is a mathematically compatible owner of such a table and identifies the exact objects that must be calculated next. It also establishes a necessary semantic correction: the pre-filter channel $\mathbf 1_N$ may be gauge-null, but it cannot be transport-null if it is to become a carried right-handed-neutrino phenotype.

The result advances the chain as follows:

$$
\text{0.2 output of a chosen filter}
\longrightarrow
\text{0.3 exact selection criterion}
\longrightarrow
\text{0.4 common-carrier origin of the criterion}.
$$

# Conclusion

The common carrier from Minimal Computation Cosmology is usable in WRRA-M, but only after its ownership is stated precisely. Its fifteen-channel form cannot simply be renamed as a sixteen-channel solution. The added neutral channel must participate in the same principal transport and must have positive carrier norm. Once that condition is met, the common carrier supplies a natural positive geometry on response signatures. A single negative-squared-mismatch rule then generates every compatibility entry required by 0.3, and the two filter gaps collapse to exact alignment products. This replaces eight free scalar entries by one metric, one response extraction rule, and eight calculated signatures. The next version should stop asking what the compatibility values may be and calculate them from one frozen microscopic carrier.

# Appendix A Exact verification record

The accompanying verification script checks with exact rational arithmetic that:

- the squared-distance expansions give the two carrier-gap identities;
- the finite witness yields $\Delta_L=\Delta_R=8$;
- the four witness scores are $0,-8,-8,-16$;
- adding a zero-charge singlet leaves the anomaly sums unchanged;
- the script explicitly constructs I16 and computes rank 16 by exact Gaussian elimination, checks neutral-channel norm 1 and a singular rank-15 control; this separate transport-Gram example does not give rank 16 to the two-dimensional response witness.

# Appendix B References

1. Choi, W. *WRRA-M 0.2 Cross-Dimensional Filter Correspondence*. Version 0.2, 2026. DOI: [10.5281/zenodo.23072012](https://doi.org/10.5281/zenodo.23072012).
2. Choi, W. *WRRA-M 0.3 Source-Law Filter Selection*. Version 0.3, 2026. DOI: [10.5281/zenodo.23072042](https://doi.org/10.5281/zenodo.23072042).
3. Choi, W. *Minimal Computing Cosmology 2.3.2 Integrated Model*. Version 2.3.2, 2026. DOI: [10.5281/zenodo.22733000](https://doi.org/10.5281/zenodo.22733000).
4. Choi, W. *Common-Carrier Unification Without a Grand Unified Gauge Field*. Version 1.0, 2026. DOI: [10.5281/zenodo.22052565](https://doi.org/10.5281/zenodo.22052565).
5. Choi, W. *The Common Transport Operator and the Minimal Origin of Chiral Matter*. Version 1.0, 2026. DOI: [10.5281/zenodo.22056516](https://doi.org/10.5281/zenodo.22056516).
6. Choi, W. *Filter-Restored Revision of the Fifteen-Channel Common-Carrier Model*. Version 1.0, 2026. DOI: [10.5281/zenodo.22067895](https://doi.org/10.5281/zenodo.22067895).
7. Choi, W. *Minimum-Computational Filter-Spectral Revision of the Fifteen-Channel Common-Carrier Model*. Version 1.0, 2026. DOI: [10.5281/zenodo.22068573](https://doi.org/10.5281/zenodo.22068573).
8. Choi, W. *Ground-Subtracted Lossless-Angle Completion of the Fifteen-Channel Common-Carrier Model*. Version 1.0, 2026. DOI: [10.5281/zenodo.22069630](https://doi.org/10.5281/zenodo.22069630).

Copyright © 2026 Wonsik Choi. Licensed under CC BY 4.0.
