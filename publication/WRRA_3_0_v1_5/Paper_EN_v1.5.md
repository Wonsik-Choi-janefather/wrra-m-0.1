# Minimal Computing Cosmology 3.0 as a unified alternative for quantum gravity vacuum energy and the dark sectors

Wonsik Choi · Jeongin Choi

Independent Research, Seoul, Republic of Korea

Correspondence: janefather@gmail.com · ORCID 0009-0001-4263-9772

Paper v1.5 · 8 October 2026

## Abstract

Minimal Computing Cosmology (MCC) 3.0 proposes a unified alternative framework for three unresolved physical questions: the connection between quantum states and gravity, the relation between vacuum energy and cosmic expansion, and the origin of dark-matter and dark-energy effects. Worldline–Residue–Resource–Action (WRRA) organizes one nonprivileged universe through minimal computation, a common carrier and phenotype. Its executable chain connects a finite SOURCE and conditional carrier states to sector admission, phenotype, information loads, calibrated energy and pressure, and expansion and local gravity. Verified constants and observed sector shares are legitimate construction inputs. Originality is assessed in the WRRA structure, transformations and explanatory connections; reproducing known observations is a consistency result. This paper specifies the implemented segment of that proposal and its falsification conditions. Exact correlation-preserving reductions reproduce loads to 8.9×10⁻¹⁶ in a construction with 1,014,999 active addresses and a 128-dimensional carrier. States with identical separate marginals yield different return loads and deceleration, demonstrating why the joint carrier structure matters. The frozen WRRA acceleration scale applied through the credited empirical RAR kernel to 2,693 published SPARC points gives 0.13288 dex RMS without a new fit. These calculations establish an executable microscopic-to-macroscopic interface and observational consistency within its stated scope. The finite energy ledger provides an alternative construction for vacuum and expansion, but finiteness alone does not derive the observed small cosmological constant. String-theoretic material remains external support where it has not been implemented internally. The contribution is the common explanatory and computational chain across the three questions, with reduction audits as supporting verification.

Keywords: MCC 3.0; WRRA; quantum gravity; vacuum energy; dark sectors; common carrier; finite SOURCE

## 1. Three physical questions and the common WRRA structure

MCC 3.0 addresses three questions within a single framework: how quantum information can connect to gravity, how vacuum and expansion can be represented in a finite energy ledger, and how dark-sector effects can arise from resident nonphenotype and return sectors. The WRRA purpose is to explain one nonprivileged universe through minimal computation, a common carrier and phenotype. SOURCE is the finite address register; conditional quantum carrier states are mapped through disclosed admission rules into phenotype and other sectors. Sector loads then feed calibrated energy, pressure, expansion and local-gravity calculations. The central contribution claimed here is this WRRA organization and its implemented connections.

The numerical inputs, transformations, outputs and possible failures must be distinguished before evaluating that contribution. Independent predictions are not a prerequisite for constructing the theory or recognizing structural originality. Calibration against verified constants and observations is legitimate, and reproduction of known values counts as observational consistency and explanatory performance. An unmeasured quantity calculated after fixing the model is a model prediction; agreement with another theory does not remove its provenance. Externally supplied laws and kernels are credited and distinguished from transformations actually calculated inside WRRA.

Established sufficiency and reduction mathematics [1–3] supports the implementation. Its role is to audit what the common carrier must retain and when a reduced interface ceases to support the proposed dynamics. We do not claim new partial-trace or invariant-subspace mathematics. Computational timings are implementation diagnostics, not the definition of the cosmological contribution. The current finite construction and results are stated below; the broader MCC 3.0 research record is retained in [7].

**Evaluation of the three proposed connections**

**Quantum states and gravity.** Verified inputs: normalized carrier states, disclosed operators and calibrated physical coefficients. WRRA transformation: the joint address–carrier state is mapped to sector-weighted carrier operators, loads, energy and the downstream gravity response. Outputs: exact preservation of specified correlated readouts and calculated expansion, rotation and conditional lensing; identical marginals can give different loads and deceleration. Falsification conditions: loss of state positivity or normalization, disagreement between direct and reduced readouts, failure of shared-energy bookkeeping, or disagreement with specified physical observations. This is an implemented connection between quantum state information and gravity readouts. It is not yet an internally calculated microscopic quantum-gravity theory; heterotic-string support is not counted as internal integration without the corresponding WRRA calculation.

**Vacuum energy and cosmic expansion.** Verified inputs: reference energy density, sector shares and disclosed dimensional calibrations. WRRA transformation: finite SOURCE admission and resident/return loads feed a finite energy function whose volume dependence determines pressure and expansion. Outputs: finite sector energy and pressure and a computed deceleration. Falsification conditions: inconsistent units, nonconserved exchange, disagreement between pressure and the stated energy derivative, or failure of the fixed model to reproduce the specified expansion observations. The finite construction avoids an unbounded ledger, but the observed small energy scale currently enters through calibration; finiteness by itself is not a derivation of that scale or a completed solution of the cosmological-constant problem.

**Dark matter and dark energy.** Verified inputs: reference shares 5%, 26.8% and 68.2%, source parameters and published acceleration measurements. WRRA transformation: arithmetic admission separates phenotype, resident nonphenotype and return sectors; their loads enter the shared energy and twist/local-gravity response. Outputs: reproduction of the calibrated shares and calculated expansion, rotation and conditional lensing, with a descriptive published-data acceleration comparison. Falsification conditions: violation of the common ledger, separately refitted outputs that no longer follow the same fixed state, or failure against specified rotation, lensing or expansion data. The RAR function is inherited and credited; the comparison is not a complete lensing or cosmological-data validation.

Taken together, these are a unified alternative proposal supported by the computations below. They are not presented as three completed resolutions. Neither a calibrated input nor the use of established mathematical tools negates the explanatory contribution; each output is evaluated against its actual transformation and declared failure conditions.

## 2. Verified inputs and the finite construction

Let the active address set be n=2,…,N, with N=1,015,000. Address 1 is inactive. Each address carries a normalized d-dimensional density operator ρ_n. Its classical weight is w_n>0 with sum one. The complete classical–quantum state is

$$
\Omega=\sum_{n=2}^{N}w_n|n\rangle\langle n|\otimes\rho_n,\qquad \rho_n\succeq0,\quad \operatorname{Tr}\rho_n=1.
$$

This is a classical address register coupled to quantum carrier blocks; coherence between addresses is not part of this contract. Carrier coherence is allowed. In the numerical construction, d=128. Sector labels P,D,R denote phenotype, resident nonphenotype and return. Nonnegative admission effects e_s(n) sum to one at every address. Define f_s(n)=e_s(n)g_s(n), where g_s is a disclosed positive response. The general results below need no particular arithmetic classifier. The numerical instance uses the following rules.

$$
w_n=\frac{n^{-\alpha}}{\sum_{m=2}^{N}m^{-\alpha}},\quad
g_s(n)=1+\lambda_s\frac{\log n}{\log N},\quad
(\lambda_P,\lambda_D,\lambda_R)=(0,0.25,0.1).
$$

Primes have (e_P,e_D,e_R)=(0,0,1); even composites have (0,1,0). Odd composites use a calibrated four-mode, eight-frame admission:

$$
d_k(n)=\sum_{j=1}^{4}\frac12\cos[\gamma_j(\log n+\xi k)],\quad
t_k(n)=\frac{1}{1+e^{-(d_k(n)-h)}},
$$

$$
e_P(n)=1-\prod_{k=0}^{7}(1-t_k(n)),\quad e_D(n)=0,\quad e_R(n)=1-e_P(n).
$$

The gamma values are 14.134725141734695, 21.022039638771556, 25.010857580145690 and 30.424876125859512. These are adopted spectral inputs; four-mode truncation is specified rather than physically derived. The common carrier is a periodic 128-site lattice. With S the cyclic shift and D₀=|0⟩⟨0|, define

$$
K_c=2I-S-S^\dagger,\qquad K_b=\frac{K_c+\epsilon D_0}{1+\epsilon/(2d)},\qquad
(A_P,A_D,A_R)=(I,K_c/2,K_b/2).
$$

The denominator normalizes the trace of K_b to 2d. These operators are nonnegative; they need not be bounded by I. The diagnostic ε=0 and 8 changes the supplied carrier operator, without refitting dimensional coefficients.

| Input | Value or rule | Status and role |
| --- | --- | --- |
| Sector targets | 0.05, 0.268, 0.682 | Reference inputs; only two independent after normalization |
| N | lcm(20,250,500)×29×70 | Finite candidate based on rounded targets; no physical quantization law |
| α | 1.8996877935161325 | Joint calibration to address shares |
| h | 1.4476744689338703 | Joint calibration to address shares |
| ξ; frames | 0.1; 8 | Specified admission rule |
| d; ε | 128; 0 or 8 | Carrier size and diagnostic perturbation |
| η_P | 7.5615824991×10⁻¹⁰ J/m³ | Frozen reference-state SI calibration |
| η_D | 7.2857613288×10⁻¹⁰ J/m³ | Frozen reference-state SI calibration |
| η_R | 7.6461028188×10⁻¹⁰ J/m³ | Frozen reference-state SI calibration |
| V₀; n_P,n_D,n_R | 1 m³; 0,0,3 | Reference volume and constitutive volume exponents |
| H₀; u_crit | 67.4 km/s/Mpc; 7.6689477678×10⁻¹⁰ J/m³ | Inherited reference constants |
| Local diagnostic | Plummer M=6×10¹⁰ M_sun, b₀=3 kpc | Specified source; not inferred galaxy profile |
| RAR comparison | Official RAR.mrt, 2,693 rows | Published observations; no fit in this revision |

The rounded-target construction is not robust evidence for a unique capacity. For example, transferring 0.0001 from D to R changes the rational denominator and the candidate N to 20,300,000. Earlier frozen-response probes of large cutoffs are included in the reproduction package [7]. The model therefore retains a finite candidate and sensitivity analysis, not an observed measurement of the universe's storage size. Pure address and SI-energy fractions also remain distinct ledgers: equal address weights do not imply equal physical energies.

## 3. Exact correlation-preserving interface

Define the three unnormalized sector-weighted carrier operators and scalar loads:

$$
\Sigma_s=\sum_n w_nf_s(n)\rho_n,\qquad L_s=\operatorname{Tr}(\Sigma_s A_s).
$$

**Proposition 1 (readout sufficiency and positive realization).** For fixed f_s, each Σ_s is nonnegative and exactly preserves every sector carrier query Tr(Σ_s B), for arbitrary Hermitian B. The collection admits a completely positive trace-preserving realization when a failure branch is retained.

Proof. Positivity follows from nonnegative coefficients. Linearity of trace gives the query identity. Choose M≥max_n sum_s f_s(n). On the address-classical input, Kraus operators J_{s,n}=sqrt(f_s(n)/M)|s⟩⟨n|⊗I produce the flagged blocks Σ_s/M. Add J_{F,n}=sqrt(1−sum_s f_s(n)/M)|F⟩⟨n|⊗I. Their adjoint products sum to the identity. The resulting state has unit trace and is a valid quantum channel output. Reading a successful sector and multiplying by M recovers its weighted operator. Σ_s itself is an unnormalized bookkeeping operator, not a density matrix or an extra energy sector. ∎

For G diagnostic classes with common conditional states τ_k and address class k(n), one can stream

$$
B_{sk}=\sum_{n:k(n)=k}w_nf_s(n),\qquad \Sigma_s=\sum_{k=1}^{G}B_{sk}\tau_k.
$$

This keeps correlations between sector response and carrier state. It does not replace the joint state by separate marginals. The grouping is a test input, not a derivation that all physical addresses fall into these classes.

**Proposition 2 (restricted linear dimension).** Let F_{sn}=f_s(n) have rank r and fix strictly positive w_n. On the interior of the space of trace-one conditional carrier blocks, all-sector arbitrary-carrier readout variations have real dimension r(d²−1). An exact linear encoding for that entire query family requires at least this many variable real coordinates; r independent weighted operators attain the bound.

Proof. Expand each perturbation δρ_n in a traceless Hermitian basis with d²−1 elements. In each basis direction, δΣ=F diag(w) δx. Since diag(w) is invertible, its image has dimension r. Directions are independent; sufficiently small perturbations around I/d preserve positivity. Thus the total image dimension is r(d²−1). A lower-dimensional linear encoding has a nonzero kernel that changes a target expectation; an appropriate Hermitian query separates that direction. Choosing a basis of the row space of F attains the dimension, with known fixed trace components. ∎

This is a bound for a fixed query family and linear encodings. For three fixed A_s at one snapshot, just three scalar L_s suffice. Neither bound constrains nonlinear physical implementations or proves the physical necessity of the chosen arithmetic law. The dimension argument is standard linear algebra; its role is to define precisely what the WRRA compression preserves.

## 4. Product-marginal error and dynamical closure

Let μ_s=sum_n w_n f_s(n), the carrier marginal be ρ_bar=sum_n w_nρ_n, and b_s(n)=Tr(ρ_n A_s). The product approximation is L_s^prod=μ_s Tr(ρ_bar A_s). Its error is exactly

$$
L_s-L_s^{\mathrm{prod}}=\operatorname{Cov}_w(f_s,b_s),\qquad
|L_s-L_s^{\mathrm{prod}}|\le\frac{a_{s,\max}-a_{s,\min}}{2}\sqrt{\operatorname{Var}_w(f_s)}.
$$

The identity follows by subtracting the product of the two means. Cauchy–Schwarz bounds the covariance, and a random variable in the spectral interval of A_s has variance at most one quarter of that interval's squared width. This bound can be loose; the benchmark records both the observed error and bound. Zero spectral width makes the error zero, explaining preservation of the phenotype identity budget even when D or R loads change.

Snapshot sufficiency need not imply closed dynamics. A common carrier channel Φ independent of n obeys Σ_s'=Φ(Σ_s), so weighted operators remain sufficient. Address-controlled channels instead act before the weighted sum and generally require additional moments. In an equal-weight two-address qubit example, states (|0⟩⟨0|,|1⟩⟨1|) and the swapped pair have the same average I/2 and the same initial Z expectation zero. Applying I at the first address and X at the second yields average Z=+1 and −1, respectively. A marginal-only reduced state cannot replay this update.

Thus the correct contract is: fixed query operators at a snapshot, or a disclosed common carrier channel. An arbitrary new address-dependent update requires a fresh sufficiency or invariant-space check [3]. This prevents a compressed state from being described as a universally closed microscopic simulator. In the two-address example take all f_s constant: all three weighted operators are then equal between the two initial states. A stronger counterexample below uses the actual WRRA coefficients.

**Proposition 3 (class-controlled lift).** Partition addresses into fixed disjoint classes C_k, keep w and f fixed, and let class k evolve by its disclosed common carrier channel Φ_k. Define

$$
\Sigma_{sk}=\sum_{n\in C_k}w_nf_s(n)\rho_n,\qquad \Sigma'_s=\sum_k\Phi_k(\Sigma_{sk}).
$$

These class-resolved operators replay such updates exactly, and each block itself evolves as Φ_k(Σ_sk). For the complete class-resolved carrier-query family, Proposition 2 gives minimum variable linear dimension r_lift(d²−1), where r_lift is the rank of the rows f_s(n)1_{C_k}(n). This is sufficiency and a linear bound for that complete family; it is not a claim that every specified channel requires every class-resolved query. Proof: apply each linear channel inside its class sum and apply Proposition 2 to the lifted coefficient matrix. ■

**Closure criterion and reusable audit.** For arbitrary tuples of common CPTP maps on the specified classes, the original weighted interface is closed if the row space of F is invariant under multiplication by each class indicator. Equivalently, stacking the class-masked rows does not increase its rank. Then each Σ_sk is a linear combination of the original operators, so Proposition 3 supplies the update. Conversely, if a masked row leaves this row space, project it orthogonally onto the original null space. This yields a nonzero perturbation invisible to the original interface and visible to that class. Opposite small traceless carrier perturbations preserve positivity; an identity/bit-flip controlled update can distinguish the two states. Thus universal closure for this specified channel family cannot be asserted. This is an application of established invariant-space reduction [2,3], not a new general sufficiency theorem.

The audit has five reusable steps: (i) state the query family and form its address coefficient matrix F; (ii) compute its rank and the retained operator family; (iii) mask its rows by the proposed control classes and compare the lifted rank; (iv) when rank grows, construct a null-space counterexample and retain class-resolved blocks; (v) choose a representation by measuring construction, storage and the required query workload. It applies to finite classical–quantum mixtures beyond arithmetic addresses. A snapshot cache is useful only when its contract matches the computation to be performed.

For the actual WRRA f_s, use C₁={n:n mod 3=0}, C₂ its complement. The initial rank is three, while the lifted rank is six. For d=128 the complete class-resolved family has 98,298 variable coordinates, versus 49,149 for the original three-operator family. An exact rank witness uses addresses 3,6,9 in the divisible-by-three class and 2,4,25 in its complement. In each class the prime, even-composite and odd-composite columns give a triangular 3×3 minor with strictly positive R, D and P pivots. The disjoint class supports combine these minors into rank six; no floating-point rank decision is needed. This answers a concrete implementation question: three scalar loads suffice for frozen cosmological outputs; three operators support changing snapshot carrier queries; class-resolved operators support the specified address-controlled updates. These are different information contracts, not interchangeable definitions of a universal minimum.

## 5. Shared energy, records and observable equivalence

The supplied energy and volume laws are

$$
E_s(a)=\eta_sV_0a^{n_s}L_s,\quad V=V_0a^3,\quad
\rho_s=E_s/V,\quad P_s=-n_s\rho_s/3.
$$

They give pressureless P,D and constant-density R for frozen L. This matter-plus-constant-density behavior is a constitutive input, not a new derivation of accelerated expansion. Pressure is the derivative of the same E used for the density readout, at fixed L. Internal state evolution requires its own disclosed generator; this derivative is not the total derivative along evolving L.

Recording is checked in a boundary that includes its finite supplier. The same work cannot be counted both as new cosmic energy and as an already allocated phenotype resource:

$$
E_{\mathrm{sys,before}}+E_{\mathrm{supplier,before}}=E_{\mathrm{sys,after}}+E_{\mathrm{record,after}}+E_{\mathrm{supplier,after}}.
$$

Here the record starts blank, its final energy is displayed separately, and supplier work equals the system-energy change plus record energy. The inherited effective-record, magnetic internal and joint internal models are alternatives, not simultaneously added particle species. The frozen supplier branches and their numerical budgets are documented in Appendix B. Let ρ=sum_sρ_s and P=sum_sP_s. The homogeneous and local diagnostic readouts use

$$
H/H_0=\sqrt{\rho/u_{\mathrm{crit}}},\quad q=\tfrac12(1+3P/\rho),\quad
a_T=cH_0\sqrt{\rho_D/(8u_{\mathrm{crit}})}.
$$

The local rule is g(r)=g_b(r)ν(g_b/a_T), v²=rg, with ν(y)=1/[1−exp(−sqrt(y))]. This is the existing empirical RAR function of McGaugh, Lelli and Schombert [4], evaluated here at the state-derived a_T. We do not claim the function itself is a WRRA discovery. Conditional lensing integrates this same g under the stipulated weak-field condition Φ=Ψ. Neither this local prescription nor the homogeneous relation supplies a complete four-dimensional gravitational theory.

**Proposition 4 (three-load quotient and inverse within the renderer).** With coefficients, volume, local source and response kernel fixed, any two microscopic states with equal L_P,L_D,L_R have identical H,q,a_T,v and conditional lensing. At positive density, the three densities are uniquely determined by H,q,a_T:

$$
\rho=u_{\mathrm{crit}}(H/H_0)^2,\quad
\rho_R=\frac{1-2q}{3}\rho,\quad
\rho_D=8u_{\mathrm{crit}}\left(\frac{a_T}{cH_0}\right)^2,\quad
\rho_P=\rho-\rho_R-\rho_D.
$$

Proof. The forward map factors through the three loads, establishing equivalence. Since P=−ρ_R, the q relation yields the second inverse; the a_T relation yields the third. Remaining density follows by subtraction. At fixed r and positive g_b, g_b/[1−exp(−sqrt(g_b/a_T))] increases strictly with a_T, so a rotation value in its allowed range also determines a_T. Nonnegative recovered densities define the unrestricted scalar renderer domain. They are necessary but not sufficient to belong to the image of the fixed microscopic construction. ∎

For fixed w,f and scale factor, A_P=I fixes L_P=μ_P=∑w_nf_P(n)=0.05 independently of the conditional carrier states. Consequently the actual fixed-SOURCE macroscopic image has at most two variable loads. In this arithmetic instance, f_D f_R=0 at every address: D and R occupy disjoint supports. With otherwise arbitrary normalized conditional states, their exact attainable domain is

$$
L_P=\mu_P.
$$

$$
\mu_D\lambda_{\min}(A_D)\le L_D\le\mu_D\lambda_{\max}(A_D).
$$

$$
\mu_R\lambda_{\min}(A_R)\le L_R\le\mu_R\lambda_{\max}(A_R).
$$

Necessity follows from the spectral expectation bounds. Sufficiency follows by assigning independent extremal-state convex mixtures on the disjoint D and R supports. This rectangle is for the full conditional-state family, not for every constrained 32-group diagnostic family. At fixed a, convert the recovered densities to loads using the disclosed η and volume law and test this rectangle, including the fixed P equality. With ε=0, both D and R operators range from zero to two; ε=8 changes the R interval. The archive records these bounds and checks the reported states against them.

The unrestricted three-density renderer has information dimension at most three; its fixed-SOURCE microscopic image has at most two variable coordinates. A simpler three-load model is an exact baseline for these outputs. SOURCE structure is resolved by conditional address/carrier queries, not by declaring these already-equivalent macro numbers to be independent microscopic evidence. This equivalence is an explanatory constraint on what the present model can claim.

## 6. Numerical controls and published-data comparison

All tests preserve the supplied SI coefficients. A dense 256-address, eight-dimensional random pure-state reference is evaluated directly and via three Σ_s. Ninety additional positive-operator queries give maximum error 2.9×10⁻¹⁵. The full test has N−1 active addresses, d=128 and 32 fixed classes n mod 32 with seeded complex pure carrier states. Loads agree to 8.9×10⁻¹⁶. Storing all dense conditional matrices would require 266,075,897,856 bytes in complex128; storing three weighted matrices needs 786,432 bytes. This is a theoretical storage comparison, not measured allocation. The grouped input already has a much smaller representation, and source construction still costs O(N). No total-runtime speedup over all alternative implementations is claimed.

The same-marginals diagnostic uses two extremal eigenstates of K_c/2 and address groups n mod 3=0 versus the complement. Its paired correlated blocks have exactly the same carrier marginal as the product baseline and the same address distribution. Positivity is checked. The retained covariance changes D by −0.000406237 and R by +0.035378346; the error identity is satisfied to 3.1×10⁻¹⁶. This is a constructed state test, not an observed cosmic correlation.

| Diagnostic | Product marginals | Correlation retained |
| --- | --- | --- |
| P load | 0.050000 | 0.050000 |
| D load | 0.278926 | 0.278519 |
| R load | 0.687743 | 0.723121 |
| q | −0.52856 | −0.54501 |
| Rotation, km/s | 207.510 | 207.487 |
| Conditional lens, arcsec | 0.535582 | 0.535435 |

Twelve inherited shared-state configurations are reproduced by the scalar quotient with maximum printed-output discrepancy 2.9×10⁻¹⁴. Equal-load microscopic alternatives therefore remain indistinguishable under this renderer, while the product-marginal ablation does not generally preserve those loads. These are different tests and support different conclusions.

The exact same-marginals construction is as follows. Let P₀,P₁ be the minimum/maximum eigenprojectors of K_c/2, C=(P₀+P₁)/2 and D=(P₀−P₁)/2. With p=∑_{n mod 3=0}w_n=0.2894395421456772 and t=min(1,(1−p)/p)=1, set ρ₁=C+tD and ρ₂=C−ptD/(1−p). Their weighted average is C and both are positive and trace one. The product baseline assigns C to every address. The original twelve inherited cases instead use I/d at every address, or a packet on the mod-3 class and I/d elsewhere; the packet is (|8⟩+|16⟩+|24⟩)/√3. They cover ε∈{0,8} and a∈{0.5,1,2}.

Rotation is evaluated at r=8.2 kpc for g_b(r)=GM r/(r²+b₀²)^(3/2), M=6×10¹⁰ solar masses and b₀=3 kpc. Lensing uses impact b=10 kpc, patch radius R=200 kpc and

$$
\alpha(b)=\frac{4}{c^2}\int_0^{\sqrt{R^2-b^2}}g\!\left(\sqrt{b^2+z^2}\right)\frac{b}{\sqrt{b^2+z^2}}\,dz.
$$

Radians are converted to arcseconds. This is a finite-patch weak-field diagnostic, not a measured lens system. The inherited twelve cases also compare independent 512-node Gauss–Legendre and adaptive quadratures, agreeing below 10⁻⁹ arcsec.

**A fair representation comparison.** For the 32-class complex pure-state diagnostic, retaining 32 vectors and the 3×32 weight matrix costs 66,304 bytes; three dense weighted operators cost 786,432 bytes; three scalar loads cost 24 bytes. The weighted representation is therefore larger than this grouped input. Ninety seeded, changing Hermitian carrier queries, evaluated for every sector, agree between grouped and weighted representations to 6.94×10⁻¹⁸. The strengthened optimized workload sweep below evaluates practical utility including construction. Scalar loads cannot answer new carrier queries, while grouped states retain specified class-controlled information that a snapshot cache loses.

**Workload sweep with construction included.** We additionally test d∈{32,64,128}, G∈{8,32,128} and m∈{10,90,300}: 27 cases, five repetitions each, seeded complex pure states and positive 3×G weights. NumPy 2.3.5 uses OpenBLAS 0.3.30 on an AMD EPYC 9V74; OPENBLAS_NUM_THREADS, OMP_NUM_THREADS and MKL_NUM_THREADS are fixed to one before import. The maximum query discrepancy is 1.39×10⁻¹⁷. Grouped queries use a direct BLAS matrix product followed by row contractions, with the conjugate buffer prepared once; contraction-path planning is not repeated. Reported retained bytes exclude working buffers for both methods. Query generation and address-weight compilation are common excluded inputs; cache construction is included. The table reports 90-query medians, in milliseconds. Full per-run variation is retained in workload_sweep_results.json.

| d / G | Group / cache bytes | Group / cache total ms | Estimated break-even m |
|---|---|---|---|
| 32 / 8 | 4,288 / 49,152 | 0.739 / 0.581 | 28 |
| 32 / 32 | 17,152 / 49,152 | 1.433 / 0.680 | 19 |
| 32 / 128 | 68,608 / 49,152 | 3.914 / 1.952 | 38 |
| 64 / 8 | 8,384 / 196,608 | 1.519 / 1.693 | None |
| 64 / 32 | 33,536 / 196,608 | 3.823 / 1.766 | 8 |
| 64 / 128 | 134,144 / 196,608 | 12.209 / 6.993 | 46 |
| 128 / 8 | 16,576 / 786,432 | 6.219 / 12.924 | None |
| 128 / 32 | 66,304 / 786,432 | 13.739 / 8.277 | 11 |
| 128 / 128 | 265,216 / 786,432 | 38.370 / 7.824 | 4 |

The cache including construction is faster in 16 of 27 local cases; it loses in 11 cases. Per-query saving and median build cost give estimated break-even counts from 4 to 49. This linear estimate is workload-dependent, not a promised crossover on other hardware. The five-run minimum and maximum values are archived rather than treated as inferential uncertainty. For this complex128-vector/float64-weight layout, G<3d²/(d+1.5), the cache uses more storage; for larger G it can use less. No single representation dominates. These measured costs operationalize the audit rather than identifying a physical minimality law.

**Actual-interface failure and repair.** Let A_{sn}=w_nf_s(n) on the first 256 active addresses, z_n=+1 in the mod-3 class and −1 elsewhere, and u_n=A_{Rn}z_n. Define h=u−Aᵀ(AAᵀ)⁻¹Au and δ=h/max|h_n|. Set ρ_n^±=(I±δ_n Z)/2 on a carrier qubit for those addresses and I/2 elsewhere. All initial Σ_s coincide because Aδ=0; all traces are one and positivity is explicit from |δ_n|≤1. Apply I in the mod-3 class and X elsewhere. The difference of weighted Z queries becomes 2A diag(z)δ. The initial maximum difference is 1.12×10⁻¹⁶; after the update the R-sector difference is 0.6668017457457079. This embeds in the 128-dimensional carrier. The six lifted operators from Proposition 3 retain the missing class information and replay the update. Thus the failure concerns all three WRRA weighted operators, not merely an ordinary unweighted marginal. It gives a reproducible reason for retaining a larger state when moving from frozen outputs to address-controlled evolution.

## 7. Reproducibility and falsification

Exact v1.4 reproduction archive: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/blob/2f2b1c5e9e4c0625870fcddb5e2216737665e629/publication/WRRA_3_0_v1_4/WRRA_3_0_Reproduction_v1.4.zip. Archive SHA256: ea30c242fd374a04f39b3562f76f7de26fd4659e75f18cf33d5a3cd39b79775b. The adjacent manifest maps every included source and input to its hash.

The archive contains the full inherited sources for stages 1–7, their nested frozen dependencies and input manifests, the new benchmark, the official data bytes and a one-command reproduction entry point. The reference environment is Python 3.12, NumPy 2.3.5 and SciPy 1.17.0; Matplotlib is needed only for Figure 1. From the archive root:

```text
python reproduce_all.py
python benchmark.py
python rar_comparison.py
python workload_sweep.py
```

The first command runs 27 stage scripts in an isolated copy and records exit codes, stdout, stderr and expected PASS conditions. All completed successfully in this revision. Stages use their pinned dependency snapshots: this is a full rerun of the published stage checks, not a newly refitted model. Different floating-point libraries can change final digits and timing measurements. The second and third commands recreate the new numerical controls and comparison from fixed inputs. benchmark_results.json and rar_results.json provide the full machine-readable values, including spectral error bounds. SHA256 checks cover the input data and distributed sources.

Verification has three distinct levels. The proved identities require their stated mathematical assumptions. Numerical disagreement principally tests software conformance or reveals a violated assumption. Observational residuals test the physical renderer against data; physical selection additionally requires a specified comparison and uncertainty model. The following failure conditions describe implementation conformance, not observational refutation of a proved identity. The exact interface fails if an independently implemented direct joint readout differs from its weighted-operator counterpart beyond the declared numerical tolerance, or positivity is lost. The marginal-error result fails if its covariance identity or spectral bound fails. The three-load equivalence fails if the same fixed coefficients and equal loads produce different downstream outputs. Conversely, if address-controlled updates are introduced, snapshot sufficiency alone is no guarantee; the counterexample is a test that rejects that extension. Supplier execution is rejected below its maximum branch requirement, and energy duplication or separate output refits invalidate the shared-ledger contract.

For observational claims, the frozen response can be compared to specified data and residual summaries; its association with measured acceleration is explicit here. A stronger physical selection test would require galaxy-level nuisance parameters and covariance, a fixed test set and a comparison of inequivalent microscopic constructions. No universal numerical rejection threshold is invented retrospectively from the present residuals. Current observational consistency and microscopic identifiability are separate claims.

## 8. Conclusion

MCC 3.0 proposes a common finite execution structure for quantum-to-gravity connections, vacuum and expansion, and dark-sector effects. Its contribution is the WRRA chain from SOURCE and common carrier through sector admission and phenotype to loads, energy, pressure, gravity and expansion. Verified constants and calibrated observations support construction and known-value reproduction. The numerical and mathematical results here substantiate the implemented interface: correlations can affect macroscopic readouts, supported reductions preserve those readouts, and class-controlled evolution requires additional retained information. The SPARC comparison documents descriptive consistency of the fixed WRRA scale in the credited response kernel. These audits strengthen the common structure; computational speed is not the central claim.

The results also specify where completion is still required: internal microscopic quantum-gravity calculations, a structural derivation beyond calibration of the vacuum-energy scale, and broader jointly controlled dark-sector observations. Those remaining links do not erase the implemented alternative. The framework should be evaluated by its verified inputs, WRRA transformations, calculated outputs and falsification conditions, with the same evidential standards applied to competing explanations.

## Appendix A. Published-data consistency check

For an observational consistency comparison, we use all 2,693 rows of the official RAR.mrt release [5,6]. Its columns give log10 baryonic and observed acceleration and their marginal errors. The existing WRRA scale a_T=1.191787531397112×10⁻¹⁰ m/s² is fixed before this calculation. We change no stellar mass-to-light ratio, distance, inclination, cosmic fraction or response coefficient. The comparison is descriptive reuse of a previously published dataset and an inherited empirical function, not a blind validation or an independent discovery.

$$
r_i=\log_{10}g_{{\mathrm{obs}},i}-\log_{10}\!\left[\frac{g_{{\mathrm{bar}},i}}{1-e^{-\sqrt{g_{{\mathrm{bar}},i}/a_T}}}\right],\quad
{\mathrm{RMS}}=\sqrt{\frac1m\sum_i r_i^2}.
$$

| Acceleration prescription | Scale, m/s² | RMS residual, dex | Median residual, dex |
| --- | --- | --- | --- |
| Fixed WRRA state scale | 1.19179×10⁻¹⁰ | 0.132875 | −0.001555 |
| Published empirical RAR scale | 1.20000×10⁻¹⁰ | 0.132913 | −0.002462 |
| Baryons only | None | 0.513981 | 0.430000 |

![Published SPARC RAR points and fixed WRRA-scale residuals](RAR_frozen_comparison.png)

Figure 1. Left: published points and fixed response curve. Right: observed-minus-calculated log residuals. The published empirical-scale curve differs from the WRRA-scale curve by at most 0.00143 dex and would almost overlap it. The RMS difference is not evidence of statistical superiority. Rows share galaxy-level nuisance parameters; this four-column release does not provide galaxy identifiers or a joint covariance. We therefore do not treat 2,693 rows as independent likelihood factors, quote a significance or estimate physical parameter uncertainty from this table. This result establishes descriptive consistency of the supplied scale and kernel with these data. It does not select the microscopic address law or validate conditional lensing.

## Appendix B. Frozen supplier diagnostics

The three supplier branches are finite frozen inputs, not new particle constructions in this article. Their minimum budgets are maximum conditional branch-work requirements. At reference phenotype energy E_P=3.780791249536135×10⁻¹¹ J the retained values are:

| Supplier branch | Mean work, J | Required budget, J |
|---|---|---|
| Effective record | 7.029276088428041×10⁻¹² | 7.029707767554742×10⁻¹² |
| Principal magnetic | 6.015266344305666×10⁻¹² | 6.015700324113602×10⁻¹² |
| Joint calibrated | 1.2033019830228727×10⁻¹¹ | 1.2033440156388269×10⁻¹¹ |

The joint budget divided by E_P gives 31.8278354%. The first two suppliers are 20% of E_P; the joint branch is admitted at its disclosed required budget. Mean work alone is not sufficient for every conditional branch. `snapshots/source_step4/channel_record.py` and `mass_mixing_join.py` construct the three underlying branches; `snapshots/source_step5/record_load_join.py` tests their nested conservation. This paper takes these derived, pinned records as inputs and does not infer their microscopic origin from the conservation identity.

## References

[1] A. Jenčová and D. Petz. Sufficiency in quantum statistical inference. arXiv:math-ph/0412093. https://arxiv.org/abs/math-ph/0412093.

[2] O. Kabernik, J. Pollack and A. Singh. Quantum State Reduction: Generalized Bipartitions from Algebras of Observables. Physical Review A 101, 032303 (2020). https://doi.org/10.1103/PhysRevA.101.032303.

[3] T. Grigoletto, Y. Tao, F. Ticozzi and L. Viola. Exact Model Reduction for Continuous-Time Open Quantum Dynamics. Quantum 9, 1814 (2025). https://doi.org/10.22331/q-2025-07-29-1814.

[4] S. S. McGaugh, F. Lelli and J. M. Schombert. The Radial Acceleration Relation in Rotationally Supported Galaxies. Physical Review Letters 117, 201101 (2016). https://doi.org/10.1103/PhysRevLett.117.201101; arXiv:1609.05917, Eq. 4.

[5] F. Lelli, S. S. McGaugh and J. M. Schombert. SPARC: Mass Models for 175 Disk Galaxies with Spitzer Photometry and Accurate Rotation Curves. Astronomical Journal 152, 157 (2016). https://doi.org/10.3847/0004-6256/152/6/157.

[6] F. Lelli, S. S. McGaugh, J. M. Schombert and M. S. Pawlowski. One Law to Rule Them All: The Radial Acceleration Relation of Galaxies. Astrophysical Journal 836, 152 (2017). https://doi.org/10.3847/1538-4357/836/2/152. Official published data: https://astroweb.case.edu/SPARC/RAR.mrt, retrieved 8 October 2026, SHA256 24aa7059dab7fa44787f7c11191052489899819370f6508621674769f3b72833.

[7] W. Choi and J. Choi. Minimal Computing Cosmology 3.0, cumulative book and theory improvement stages. Previous public book release: https://doi.org/10.5281/zenodo.23202732. Frozen stage-six repository commit: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/commit/dfa336c5526fe3e3923cee16e2a42dc2b3006412. This revision includes snapshots for all preceding stages; no new DOI has been assigned to paper v1.5 or book v0.7.
