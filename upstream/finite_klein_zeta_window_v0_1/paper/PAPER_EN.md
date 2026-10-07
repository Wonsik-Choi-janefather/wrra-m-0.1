# WRRA_M Finite Klein–Zeta Generation Window v0.1

## A finite, boundaryless address generator for the WRRA_M upstream model

**Wonsik Choi, Jeongin Choi**  
7 October 2026  
WRRA_M research program

### Abstract

WRRA_M has previously used a finite address domain \(n=2,\ldots,10^6\) to implement its upstream arithmetic ledger, but the value \(10^6\) functioned as a computational cutoff rather than as an internally generated property of the model. The present work asks whether a finite generation window can be constructed from quantities already present in WRRA_M without introducing a realized infinite address set. We combine three finite coordinates: (i) the minimal exact integer ledger compatible with the adopted arithmetic partition \(0.05/0.268/0.682\), giving \(L=500\); (ii) the existing WRRA_M harmonic ledger \((0,5,29)\), giving \(H=29\); and (iii) the number \(C\) of positive nontrivial Riemann-zeta zeros below the finite phase boundary \(T=2\pi H\), giving \(C=70\). The resulting candidate window is

\[
N_U=LHC=500\times29\times70=1,015,000.
\]

The construction is embedded in a Klein-type quotient so that closure is finite and orientation-reversing rather than a hard terminal boundary. We then replace the legacy cutoff \(10^6\) by \(1,015,000\) in the executable WRRA_M address filter. With the old arithmetic parameters frozen, the sector ledger changes only to \(5.000002539\%/26.800001829\%/68.199995632\%\). A minimal recalibration of the two previously calibrated arithmetic parameters, \(\alpha\) and the admission threshold \(h\), restores \(5\%/26.8\%/68.2\%\) exactly within numerical precision, with changes of only \(9.85\times10^{-8}\) and \(1.30\times10^{-6}\), respectively. Holding the downstream SI response coefficients fixed then gives \(q_0=-0.5285585894\), a reference rotation speed of \(207.5102419\,\mathrm{km\,s^{-1}}\), and conditional finite-patch lensing of \(0.5355822400''\). The inherited finite carrier remains positive and its proper-time update conserves total energy to a maximum relative drift of \(9.99\times10^{-16}\).

Under the fixed WRRA assessment rule, the result is classified **PASS-C**: \(N_U=1,015,000\) is accepted as a finite-generation-window candidate and a conditional WRRA_M prediction under the stated \(L\times H\times C\) construction. It is not yet claimed to be a measured universal constant. The principal unresolved condition is whether the three coordinates \(L,H,C\) are physically and structurally compelled to form an independent Cartesian product.

---

## 1. Evaluation protocol

This work uses the same four-part judgment rule throughout:

\[
\boxed{\text{verification input} \rightarrow \text{WRRA-specific transformation} \rightarrow \text{output} \rightarrow \text{falsification condition}}.
\]

Independent prediction is not imposed as a prerequisite for theoretical construction. Previously validated constants and observationally adopted values may be used to fix a model. Once those inputs and calibrations are fixed, quantities produced by the WRRA_M transformation are treated as model outputs. Reproduction of known values counts as reality-consistency of the model rather than as a null result. At the same time, each construction assumption is recorded explicitly so that a numerically successful result is not confused with a unique derivation.

The immediate problem is narrow. The earlier WRRA_M upstream model established that the \(31.8\%\) resident Actual share is not the automatic fixed point of unlimited recycling. A finite generation window or an independent balance closure is therefore required. The earlier implementation used \(N=10^6\) as a practical finite domain. This paper replaces that convenience cutoff with a candidate generated from existing WRRA_M structure.

---

## 2. Verification inputs

### 2.1 Adopted arithmetic ledger

The common upstream ledger is

\[
(f_\phi,f_D,f_R)=(0.05,0.268,0.682),
\]

where \(\phi\) is the phenotype branch, \(D\) is resident nonphenotype, and \(R\) is return. These values are the already adopted WRRA_M arithmetic targets. They are not reinterpreted here as exact measured cosmic energy fractions.

Written as reduced rational numbers,

\[
0.05=\frac1{20},\qquad
0.268=\frac{67}{250},\qquad
0.682=\frac{341}{500}.
\]

The least common exact denominator is therefore

\[
\boxed{L=500},
\]

with integer counts

\[
(25,134,341).
\]

The role of \(L\) is purely model-internal: it is the minimal exact integer ledger compatible with the adopted rounded targets.

### 2.2 Existing harmonic ledger

The previous WRRA_M harmonic representation contains

\[
(n_1,n_2,n_3)=(0,5,29),
\]

so the largest existing harmonic address is

\[
\boxed{H=29}.
\]

No new fit is performed to obtain 29 in this paper.

### 2.3 Frozen address-filter parameters

For regression against the existing executable upstream filter we retain

\[
\alpha_0=1.8996876950554356,
\]

\[
h_0=1.44767317035244,
\]

together with \(K=8\) admission frames, phase step \(\xi=0.1\), and the first four positive nontrivial zeta-zero heights

\[
\gamma_1=14.134725141734695,\quad
\gamma_2=21.022039638771556,
\]

\[
\gamma_3=25.010857580145690,\quad
\gamma_4=30.424876125859512.
\]

The legacy scalar effective admission value is

\[
\beta_0=0.8654570124136961.
\]

### 2.4 Frozen downstream coefficients

The SI address-energy bridge is not recalibrated when the new window is tested. The inherited coefficients are

\[
\eta_\phi=7.561582499072265\times10^{-10},
\]

\[
\eta_D=7.285761328795971\times10^{-10},
\]

\[
\eta_R=7.646102818811323\times10^{-10}
\quad \mathrm{J\,m^{-3}}.
\]

The inherited reference energy density is

\[
u_{\rm crit}=7.668947767821907\times10^{-10}
\quad\mathrm{J\,m^{-3}}.
\]

These are held fixed in the downstream test.

---

## 3. WRRA-specific finite generator

### 3.1 Finite zeta phase boundary

We define the phase boundary from the already existing harmonic maximum,

\[
\boxed{T=2\pi H}.
\]

For \(H=29\),

\[
T=182.212373908208.
\]

The positive nontrivial zeta zeros are generated sequentially only until the first zero beyond this finite boundary is encountered. Thus the calculation never requires a physically realized infinite set of zeros.

The last zero inside the boundary is

\[
\gamma_{70}=182.20707848436646,
\]

whereas the next one is

\[
\gamma_{71}=184.87446784838750.
\]

Therefore

\[
\boxed{C=N_\zeta(T)=70}.
\]

The boundary lies only

\[
T-\gamma_{70}=0.005295423841545
\]

above the 70th zero, while the 71st zero is

\[
\gamma_{71}-T=2.66209394017949
\]

outside it.

As an auxiliary diagnostic, \(m=29\) is the closest of the boundaries \(2\pi m\), \(1\le m\le29\), to a zeta zero both in absolute distance and after normalization by the local mean zero spacing. The normalized distance for \(m=29\) is \(0.00213612\). This alignment is **not** used to fit \(H\); 29 is inherited from the WRRA_M harmonic ledger.

### 3.2 Finite Euler–Maclaurin cross-check

To avoid treating the full infinite Dirichlet series as a physically realized computation, we cross-check the first 70 zero locations with a finite Euler–Maclaurin approximation. The finite cutoff is itself constructed from the two existing coordinates,

\[
M=LH=500\times29=14,500.
\]

For \(s=1/2+it\),

\[
\zeta_M(s)=
\sum_{n=1}^{M-1}n^{-s}
+\frac{M^{1-s}}{s-1}
+\frac12M^{-s}
+\frac{s}{12}M^{-s-1}
-\frac{s(s+1)(s+2)}{720}M^{-s-3}.
\]

At the first 70 standard zero heights, the maximum absolute residual of this finite approximation is

\[
5.286\times10^{-13},
\]

and the residual at \(\gamma_{70}\) is

\[
6.978\times10^{-14}.
\]

This is a numerical validation of the finite surrogate; it is not a proof that the Euler–Maclaurin truncation is a fundamental physical law.

### 3.3 Klein-type closure

A Möbius strip is nonorientable but has a boundary. Because the intended upstream state space is finite **and** boundaryless, the present construction instead adopts a Klein-type quotient. A convenient schematic identification is

\[
(-T,\theta)\sim(T,-\theta),
\]

with the transverse coordinate periodic. Crossing one cycle therefore returns to the finite state space with an orientation reversal rather than terminating at a boundary.

The quotient is a model-level topological rule. This paper does not claim that the observed four-dimensional spacetime has been measured to possess Klein-bottle topology. Its role is to implement a finite, nonterminal closure of the WRRA address generator.

### 3.4 Address product and integer creation

The three finite coordinate sets are

\[
0\le\ell<L,\qquad
0\le h<H,\qquad
1\le z\le C.
\]

The candidate rule treats them as independent WRRA address coordinates. A bijection to integer labels is

\[
\boxed{
n=1+\ell+L[h+H(z-1)]
}.
\]

Therefore

\[
1\le n\le LHC.
\]

The generated maximum address is

\[
\boxed{
N_U=LHC=500\times29\times70=1,015,000
}.
\]

The label \(n=1\) retains its inherited role as the inactive multiplicative/vacuum reference. The executable active address domain is consequently

\[
n=2,\ldots,1,015,000.
\]

In this sense the integers are not postulated as a pre-existing infinite set inside the physical model. They are order labels of a finite WRRA worldline/state product.

---

## 4. Regression against the legacy WRRA_M cutoff

Before testing the new window, the reconstructed calculator was required to reproduce the legacy \(N=1,000,000\) result. Using the frozen values \(\alpha_0\) and \(h_0\), the recalculation returned

\[
(\phi,D,R)
=
(0.0500000000000009,\,
0.2679999999999986,\,
0.6820000000000007).
\]

The same downstream implementation returned

\[
q_0=-0.52855,
\]

\[
v_{\rm ref}=207.5109051266\ \mathrm{km\,s^{-1}},
\]

\[
\alpha_{\rm lens}=0.5355865106''.
\]

Thus the verification implementation reproduces the existing WRRA_M baseline before any new claim is evaluated.

---

## 5. Candidate insertion with no arithmetic refit

We next replace only the finite address cutoff,

\[
10^6\rightarrow1,015,000,
\]

while keeping \(\alpha_0\), \(h_0\), \(K\), \(\xi\), and the zeta drive unchanged.

The new active domain contains

- \(1,014,999\) active addresses,
- \(79,608\) prime addresses,
- \(507,499\) even composite addresses,
- \(427,892\) odd composite addresses.

With no arithmetic refit, the common ledger becomes

\[
\phi=0.05000002538983289,
\]

\[
D=0.26800001828881304,
\]

\[
R=0.6819999563213559.
\]

Equivalently,

\[
\boxed{
5.000002539\%,\quad
26.800001829\%,\quad
68.199995632\%
}.
\]

The ledger remains positive and complete. A 1.5% extension of the maximum address therefore causes only a few \(10^{-8}\) absolute changes in the normalized sector fractions.

This is an important stability result, but it is not used as evidence that \(1,015,000\) was secretly encoded in the old cutoff. The old value \(10^6\) remains a legacy numerical choice.

---

## 6. Minimal recalibration at the generated window

The adopted WRRA rule permits the model to be fixed to validated target values. At \(N_U=1,015,000\), we therefore repeat only the same two calibrations that were already present in the arithmetic model:

1. choose \(\alpha\) so that the even-composite branch equals \(0.268\);
2. choose \(h\) so that the admitted odd-composite phenotype equals \(0.05\).

No SI energy coefficient is refitted.

The resulting values are

\[
\boxed{
\alpha'=1.8996877935161325
},
\]

\[
\boxed{
h'=1.4476744689338703
}.
\]

Relative to the legacy values,

\[
\Delta\alpha=9.8461\times10^{-8},
\]

\[
\Delta h=1.2986\times10^{-6}.
\]

The effective scalar admission is then read out rather than independently fitted:

\[
\boxed{
\beta'_{\rm eff}=0.8654567230719301
},
\]

with

\[
\Delta\beta_{\rm eff}
=-2.8934\times10^{-7}
\]

relative to the old scalar comparison value.

The recalibrated ledger is

\[
\phi=0.05000000000000018,
\]

\[
D=0.2680000000000007,
\]

\[
R=0.6820000000000006,
\]

which closes to the adopted \(5\%/26.8\%/68.2\%\) target within floating-point precision.

Under the WRRA evaluation rule this is legitimate model fixing, not a new observational prediction.

---

## 7. Frozen downstream propagation

After the arithmetic model is fixed at \(N_U\), the candidate address state is passed to the existing downstream response **without refitting** the SI coefficients \(\eta_\phi,\eta_D,\eta_R\).

The address response remains

\[
g_s(n)
=
1+\lambda_s\frac{\log n}{\log N_U},
\]

with

\[
(\lambda_\phi,\lambda_D,\lambda_R)=(0,0.25,0.1).
\]

The new address moments are

\[
\mu_\phi=0.0500000000000002,
\]

\[
\mu_D=0.278925610976744,
\]

\[
\mu_R=0.687742539854239.
\]

Using the old SI coefficients gives energy fractions

\[
(0.04930085527,\,
0.26499341844,\,
0.68570572629).
\]

The total uniform-reference energy density becomes

\[
7.6688147276\times10^{-10}\ \mathrm{J\,m^{-3}},
\]

without coefficient refitting.

The principal downstream outputs are

\[
\boxed{
q_0=-0.5285585894
},
\]

\[
\boxed{
v_{\rm ref}=207.5102419\ \mathrm{km\,s^{-1}}
},
\]

\[
\boxed{
\alpha_{\rm lens}=0.5355822400''
}.
\]

Compared with the legacy outputs, the changes are

\[
\Delta q=-8.5894\times10^{-6},
\]

\[
\Delta v=-6.6326\times10^{-4}\ \mathrm{km\,s^{-1}},
\]

\[
\Delta\alpha_{\rm lens}=-4.2705\times10^{-6}''.
\]

Their absolute relative changes are approximately

\[
1.63\times10^{-5},\quad
3.20\times10^{-6},\quad
7.97\times10^{-6},
\]

respectively.

These numbers are not claimed as new measurements. They are the consequences of inserting the newly generated finite window into the already calibrated downstream WRRA_M map while keeping the physical response coefficients frozen.

---

## 8. Proper-time energy and state checks

The candidate was also propagated through the inherited 128-site finite carrier using the same noncommuting strength \(\epsilon=8\). The energy operator is a positive sum of the phenotype identity operator, the clustering periodic-lattice operator, and the normalized background operator.

For the candidate state the minimum eigenvalue of the dimensionless energy operator is

\[
0.0495770351>0.
\]

Using the inherited proper-time step

\[
\Delta\tau=1.4813019664\times10^{-21}\ \mathrm{s},
\]

we evaluated proper frames

\[
k=0,1,2,4,8.
\]

Internal \(D/R\) loads change with frame, so the evolution is not a trivial frozen state. Nevertheless the maximum relative total-energy drift is

\[
\boxed{
9.99\times10^{-16}
},
\]

and state traces remain unity to numerical precision. Minimum density-matrix eigenvalues remain above \(-10^{-12}\), with the small negative values attributable to floating-point Hermitian eigensolver roundoff.

Therefore the generated window does not break the existing finite energy-conservation ledger.

---

## 9. What is new and what is not

The new result is **not** the numerical existence of zeta zeros, the topology of a Klein bottle, or the observational estimates used to calibrate WRRA_M. Those are mathematical or empirical inputs.

The WRRA-specific contribution in this study is the executed connection

\[
\boxed{
\text{adopted finite sector ledger}
\rightarrow L
\rightarrow H
\rightarrow C(T=2\pi H)
\rightarrow LHC
\rightarrow N_U
\rightarrow
\text{WRRA address filter}
\rightarrow
\text{frozen downstream renderer}
}.
\]

In particular, the legacy computational cutoff is replaced by a number produced internally by the candidate generation rule.

Under the stated construction,

\[
\boxed{N_U=1,015,000}
\]

is therefore a conditional **WRRA_M model prediction**: it is an unmeasured quantity generated after the model inputs and transformation rule are specified.

The ownership of this result does not depend on whether another mathematical framework could produce the same integer. What matters for WRRA is that this value is obtained through the declared WRRA transformation and survives its internal ledger tests.

---

## 10. Falsification conditions

The candidate must be rejected or revised if any of the following occurs.

1. **Zeta-count failure.** Independent recomputation does not give exactly 70 positive nontrivial zeros below \(2\pi\times29\), or the finite zeta cross-check fails its declared tolerance.

2. **Coordinate-independence failure.** \(L\), \(H\), and \(C\) cannot consistently be represented as independent WRRA state coordinates. This is the most important unresolved condition.

3. **Closure-rule failure.** A more complete WRRA state law requires a different closure than the declared Cartesian product and orientation-reversing quotient.

4. **Arithmetic-ledger failure.** The candidate window cannot reproduce the adopted common ledger under the same two declared arithmetic calibration freedoms.

5. **Physical-ledger failure.** With downstream SI coefficients frozen, the candidate produces negative admissible energy, violates energy conservation, or fails an inherited physical constraint.

6. **Input-revision failure.** Better validated sector or harmonic inputs remove the \(L=500\), \(H=29\), or \(C=70\) structure and the model cannot update coherently.

The second condition is particularly important. Numerical stability alone does not prove that

\[
N_U=LHC
\]

is the unique generation law.

---

## 11. Assessment

The fixed WRRA assessment is

\[
\boxed{\textbf{PASS-C}}.
\]

This means:

- the construction is finite and executable;
- the integer window is generated rather than manually set to one million;
- the old arithmetic result is reproduced before modification;
- the new window is stable under frozen parameters;
- the existing two-parameter arithmetic calibration restores the common ledger with only minute changes;
- the downstream SI map runs without refitting and remains close to the inherited reference;
- the finite carrier remains positive and energy-conserving;
- one structural assumption remains unresolved: the necessity and uniqueness of the \(L\times H\times C\) product.

Accordingly,

\[
\boxed{
N_U=1,015,000
}
\]

is accepted as the current **WRRA_M finite-generation-window candidate** and as a **conditional WRRA_M prediction under the declared construction**. It is not yet promoted to an experimentally established fundamental constant of nature.

---

## 12. Reproducibility

The accompanying \`code/compute.py\` performs the full calculation reported here:

1. derive \(L=500\) from the adopted arithmetic ledger;
2. inherit \(H=29\);
3. generate zeta zeros until the first one beyond \(2\pi H\);
4. validate the finite Euler–Maclaurin surrogate;
5. construct \(N_U=1,015,000\);
6. reproduce the \(N=10^6\) legacy address ledger and downstream reference;
7. run \(N_U\) with old arithmetic parameters frozen;
8. refit only \(\alpha\) and \(h\);
9. run the frozen SI downstream response;
10. test finite-carrier positivity and proper-time energy conservation.

All numerical outputs and boolean checks are written to \`results/results.json\`.

### Internal WRRA_M provenance

This study directly extends the repository components:

- \`upstream/zeta_frame_v0_1/\`
- \`upstream/two_stage_filter_v1_0/\`
- \`calculations/wrra_m_0_9/\`
- \`calculations/wrra_m_0_10/\`
- \`calculations/wrra_m_0_11/\`
- \`calculations/wrra_m_0_12/\`
- \`integrated/v1_0_r1/\`

### Mathematical references

1. NIST Digital Library of Mathematical Functions, Riemann zeta function: zeros and Euler–Maclaurin representations.
2. mpmath documentation, \`zetazero\`.
3. Standard classification of the Klein bottle as a compact, boundaryless, nonorientable two-dimensional manifold.

---

## Conclusion

WRRA_M previously required a finite generation window but supplied only a practical cutoff. The present calculation closes that missing slot with a concrete candidate:

\[
\boxed{
500
\rightarrow
29
\rightarrow
70
\rightarrow
1,015,000.
}
\]

The central result is not merely that \(1,015,000\) is numerically near the old cutoff. The stronger result is that it is generated from three already present model structures and can replace the convenience cutoff while preserving the arithmetic ledger and downstream calculation after only the same minimal calibration freedoms already allowed by WRRA_M.

The remaining research question is therefore sharply defined: **is the Cartesian independence of the ledger, harmonic, and zeta-focus coordinates a necessary WRRA law, or only one viable closure?** The answer to that question determines whether \(N_U=1,015,000\) advances from PASS-C candidate status to a frozen WRRA_M generation law.
