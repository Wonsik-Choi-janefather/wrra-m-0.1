# Constructing and testing the WRRA model: from a finite set of numbers to physical quantities

Wonsik Choi and Jeongin Choi  
Independent Research, Seoul, Republic of Korea  
Executive paper A · Revised version 1.0 · 8 October 2026  
Correspondence: janefather@gmail.com · Wonsik Choi ORCID 0009-0001-4263-9772

## A guide for readers from other fields

**The question.** WRRA is a model that assigns weights and classification rules to numbers and uses the resulting quantities in physical calculations. Which numbers should enter the calculation, how many should be included, and can the result be trusted when their labels or the calculation range change? This paper examines that starting point and how to test it.

**From inputs to outputs.** We first fix three adopted fractions and the model's inherited harmonic specification. The smallest number of equal units representing the three fractions exactly is 500. The harmonic maximum is 29, and the number of zeta zeros in the range linked to that maximum is 70. A declared rule using all combinations gives 500×29×70=1,015,000 codes. We apply weights and classification rules to the corresponding integers other than 1, then pass their aggregate values into the existing WRRA physical-quantity functions. Combining the three counts in this way is a model specification; the multiplication alone does not establish that nature must follow that rule.

**What was checked.** We prove that the codes and three coordinates convert exactly into one another. We show that changing display labels leaves outputs unchanged when their associated relations and weights are moved with them. We also bound, and numerically check, the change in the three classification shares when more integers are included without adjusting the existing parameters. The boundary used to count zeta zeros lies close to one zero; lowering it slightly changes the code count, a sensitivity reported explicitly.

**What follows.** The proofs establish mathematical properties within the declared construction. Numerical calculations check its operation and connection to existing physical-quantity functions. These results alone do not establish that the chosen rule is the unique law of the universe. The technical text proceeds through inputs, transformation, outputs and failure criteria.

**Reading the terminology.** A *source* is the set of integers used in the calculation and its selection rule. An *address* is a code identifying an integer. A *weight* is its relative contribution to an aggregate. A *readout* is the result obtained by aggregating weights under specified rules. The *common carrier* is the state space shared by different WRRA calculations. *Coordinate transport* means moving the associated rules when the same objects receive different display labels. A *cutoff* is the largest integer included. A *zeta zero* is a complex number at which the zeta function vanishes; this construction uses the count of its nontrivial zeros in a specified range. Each technical section states the precise conditions.

## Abstract

We formulate the finite source construction of Minimal Computing Cosmology 3.0 as an explicit, reproducible interface between calibrated arithmetic data and the WRRA common carrier. The construction combines the least exact denominator L=500 of the adopted sector fractions, the inherited harmonic maximum H=29, and the standard zeta-zero count C=70 below the declared boundary T=2πH. Under an all-tuples product contract it produces 1,015,000 address codes and 1,014,999 active addresses. We prove the scope of denominator minimality, give a bijection and its inverse, and show how arithmetic relations, weights and readouts must be transported under a change of display labels. A truncation-mixture identity bounds the change in each sector share by 7.88313×10⁻⁸ when the old cutoff is increased from 1,000,000 to 1,015,000 at frozen parameters. Fresh replay obeys that bound. A finite Euler–Maclaurin contour calculation gives numerical winding 70 under mesh and truncation refinement, while a boundary-crossing control gives 69. The boundary lies only 0.00529542 above the seventieth standard zero, making the source rule sensitive to that declared boundary. The contribution is the specified WRRA construction and its tested arithmetic-to-carrier interface. The results support a conditional model-development account with executable failure criteria and explicit distinctions between code capacity, carrier dimension and compressed readout size.

## 1 What is constructed and how it is assessed

WRRA seeks to describe one nonprivileged universe through minimal computation, a common carrier and phenotype. This paper supplies the number-theory and mathematical-physics entry point: how a finite source provides structured addresses to that common carrier. Its immediate purpose is to replace an externally chosen practical cutoff with a declared rule constructed from quantities already used in the model. Calibration with verified values is part of that construction. Originality is assessed in the WRRA assembly, transformation and explanatory connection; the arithmetic facts used below are standard.

**Verified inputs.** We use the frozen calibrated address fractions (0.05, 0.268, 0.682), the inherited harmonic ledger (0,5,29), standard zeta calculations and the released arithmetic filter parameters. These are construction inputs. In particular, the decimal fractions specify an exact rational model ledger; they do not assert unlimited precision in observed cosmic energy shares.

**WRRA transformation.** Least exact rational resolution → finite product source → structured arithmetic addresses → common-carrier admission and readout → information loads → the released energy, pressure and gravity interfaces.

**Outputs.** The declared source has 1,015,000 codes. Exact serialization, coordinate transport and a truncation stability bound specify its interface. Numerical replay preserves the calibrated arithmetic partition closely before any refit. The attached structural replay also carries the reference loads into the existing macro functions.

**Falsification conditions.** Failure of the exact arithmetic or inverse map, changed outputs under correctly transported passive coordinates, violation of the share bound at fixed effects, or a parameter change hidden inside a frozen replay invalidates the corresponding result. A corrected standard zero count or a revised boundary changes the specified source. Physical tests address frozen downstream outputs under their stated conditions.

The resulting assessment is a conditional executable construction with mathematical and numerical support. No criterion in this paper requires a numerically novel prediction before calibrated reproduction can count as an explanatory result.

## 2 Choosing the numbers used in the calculation

Write the adopted fractions as p=(25,134,341)/500. Define

$$L=\operatorname{lcm}(\operatorname{den}(p_1),\operatorname{den}(p_2),\operatorname{den}(p_3)),\quad H=29,\quad T=2\pi H,\quad C=N_\zeta(T).$$

Here Nζ(T) counts nontrivial zeta zeros with positive imaginary part at most T, including multiplicity. The present boundary is not a zero. H is inherited from the neutrino phase specification; T=2πH is the declared connection to the zeta count. C consequently depends on H. A Cartesian domain does not assert statistical or logical independence of these quantities.

**Proposition 1 — Exact equal-unit resolution.** The smallest positive integer L for which every $Lp_s$ is an integer is 500.

**Proof.** In reduced form the fractions are 1/20, 67/250 and 341/500. Every admissible L is divisible by each reduced denominator, hence by their least common multiple 500. Conversely L=500 gives integer counts (25,134,341) summing to L. ∎

This is minimality for an exact equal-unit representation of the specified fractions. A weighted three-state distribution also represents these fractions. The proposition therefore does not impose a 500-dimensional carrier. The actual address measure below is nonuniform; it is not the equal-unit register used in this proof. L is adopted as a source-selection quantity, with that bridging choice recorded as a model rule.

Trailing zeros in 0.0500 do not change L. An explicit recalibration to (0.0501,0.2680,0.6819) changes L to 10,000 and, at the same H and C, changes N to 20,300,000. A new observation first tests the frozen model; it does not silently mutate the calibrated source. Recalibration creates a new declared configuration.

## 3 Converting three coordinates into one code

Let

$$\mathcal X=\{0,\ldots,L-1\}\times\{0,\ldots,H-1\}\times\{0,\ldots,C-1\},\qquad N=LHC.$$

All tuples are admitted by the source contract. Define

$$f(\ell,h,z)=1+\ell+L(h+Hz).$$

**Proposition 2 — Bijection and inverse.** The map f is a bijection from X to {1,…,N}. For q=n−1 the inverse is

$$\ell=q\bmod L,\qquad h=\lfloor q/L\rfloor\bmod H,\qquad z=\lfloor q/(LH)\rfloor.$$

**Proof.** Successive Euclidean divisions give unique remainders in the stated ranges. Substitution recovers q. The smallest and largest codes are 1 and N. ∎

With L=500, H=29 and C=70, N=1,015,000. Code 1 is an inactive unit reference; the active domain is {2,…,N}. The new audit checks inverse reconstruction on all 1,015,000 codes.

**Corollary — Capacity under full tuple recovery.** Any encoding that must recover every admitted tuple needs at least N distinct codewords, by injectivity and the pigeonhole principle. The displayed serialization meets this bound. An encoding of only active tuples requires N−1. This bound concerns distinguishable source codes, not quantum carrier dimension, memory required for a particular algorithm, or the smallest state sufficient for a restricted observable family. Compressed common-carrier readouts have their own contract.

The historical name “Klein–Zeta source” records the geometric motivation of this branch. The formula N=LHC and the bijection do not use a continuum Klein-bottle theorem. A geometric closure or finite seam action supplies additional structure when specified; it is not inferred from a finite list of codes. This paper establishes the arithmetic interface without using topology to infer physical necessity of N.

## 4 Finite zeta computation and boundary sensitivity

Fresh 40-decimal-digit mpmath calculations [2] give

$$T=182.2123739082080078,\quad \gamma_{70}=182.2070784843664619,\quad \gamma_{71}=184.8744678483875088.$$

The library zero-count routine returns Nζ(T)=70. A bracket between two indexed zeros is useful provenance, but is not by itself our independent proof of exhaustive root count.

We additionally evaluate the explicit finite Euler–Maclaurin function [1]

$$F_{M,K}(s)=\sum_{n=1}^{M-1}n^{-s}+\frac{M^{1-s}}{s-1}+\frac12M^{-s}+\sum_{k=1}^{K}\frac{B_{2k}}{(2k)!}(s)_{2k-1}M^{1-s-2k},$$

where $(s)_r$ is the rising factorial and $B_{2k}$ are Bernoulli numbers. This meromorphic finite formula has its only pole at s=1, outside the contour used here. We sample the counterclockwise rectangle 1/4≤Re(s)≤3/4 and 0.1≤Im(s)≤T. The sum of principal successive argument increments, divided by 2π, yields the following numerical winding diagnostics. No imported zero heights enter the main contour samples.

| M and K | Segments per vertical side | Segments per horizontal side | Winding | Largest argument step |
|---|---:|---:|---:|---:|
| 256 and 12 | 4,096 | 256 | 70.000000 | 0.35336 |
| 256 and 12 | 8,192 | 512 | 70.000000 | 0.18237 |
| 512 and 16 | 8,192 | 512 | 70.000000 | 0.18237 |

The smallest sampled modulus is approximately 0.0265341. Lowering the top edge to γ₇₀−0.01 gives winding 69. With M=14,500 and K=4 the largest absolute function value at the first 70 imported standard zero locations is 5.28587×10⁻¹³ in double precision. Four 40-digit spot comparisons of F₂₅₆,₁₂ against mpmath ζ give maximum absolute difference 4.93×10⁻²⁶ or smaller; their coordinates are in the audit script.

These checks go beyond evaluating small residuals at supplied zeros: they inspect a whole enclosing contour numerically and include a control that changes the expected count. They remain floating-point diagnostics. Sampled modulus bounds and mesh agreement do not certify the unsampled contour, and the rectangle is narrower than the full critical strip. We therefore retain the standard-library count as the declared C input and do not promote the contour result to an interval-certified root-count theorem or a newly derived spectral operator.

The local boundary margins are

$$T-\gamma_{70}=0.00529542384,\qquad \gamma_{71}-T=2.66209394018.$$

C remains 70 for boundaries strictly between these adjacent heights under the standard spectrum. A downward shift of 0.01 changes the library count to 69, hence N to 1,000,500. The downward margin relative to T is approximately 2.90618×10⁻⁵. This is a sensitivity diagnostic for the chosen boundary; no probabilistic significance is assigned to its proximity to γ₇₀. A different boundary requires explicit recomputation of the source and downstream model.

## 5 When changing labels preserves the result

The source carries more than display labels. On {1,…,N} we specify a partial multiplication a⋆b=ab when ab≤N, prime-factor counts $v_p(n)$, and cost $c(n)=\sum_p v_p(n)\log p=\log n$. The unit has zero cost. Primes have $\sum_p v_p=1$; the selected dark-sector class consists of composites with v₂≥1; remaining composites are eligible for phenotype admission. This classifier and the distinguished least-cost prime 2 are constitutive readout choices.

At fixed arithmetic parameters, the released filter uses weights

$$w_N(n)=\frac{n^{-\alpha}}{Z_N},\qquad Z_N=\sum_{m=2}^{N}m^{-\alpha}.$$

Let P,D,R denote phenotype, resident nonphenotype and return. Set $e_D(n)=1$ on even composites and zero otherwise. On odd composites define $e_P$ by the released phase admission law; set it to zero elsewhere. Then $e_R=1-e_P-e_D$. Thus every $e_s$ lies in [0,1] and the three effects sum to one. The exact phase law and numerical coefficients are supplied in Appendix A.

**Proposition 3 — Passive transport.** For any bijection π of the code set fixing the unit, define c′(πn)=c(n), w′(πn)=w(n), $e'_s(\pi n)=e_s(n)$, and π(a)⋆′π(b)=π(a⋆b) whenever the original product exists. Every transported weighted sector sum is unchanged. The same is true of load sums when their response functions are transported.

**Proof.** Reindex each finite sum by π. Each effect, response and weight retains its original state association, so every summand is preserved. The transported partial product follows by its definition. ∎

This resolves the apparent dependence on how tuple coordinates are printed. In a fresh run of the pinned structural implementation, all six coordinate orders preserve shares and address loads within 2.0×10⁻¹⁴. Three additional random permutations pass the registered tolerances. In contrast, exchanging only the effects attached to addresses 2 and 4 while holding the weights and costs fixed changes the D share by approximately +0.26153125. Exchanging only the effects of 9 and 11 changes the P share by −0.00557202. These are active changes to the model, and provide controls showing that the invariance test is not vacuous.

The additive cost also gives c(ab)=c(a)+c(b) for allowed products and therefore exp(iγc(ab))=exp(iγc(a))exp(iγc(b)). The unnormalized power weights multiply; for active factors a,b≥2 with ab≤N, the normalized weights satisfy $w_N(ab)=Z_N w_N(a)w_N(b)$. These identities explain how arithmetic composition connects to the phase drive without identifying prime numbers themselves with particle species.

## 6 Frozen replay and a general cutoff bound

**Proposition 4 — Truncation mixture.** Let N₂>N₁, α be fixed, and $e_s(n)\in[0,1]$ be independent of the cutoff. Define $\varepsilon=\sum_{N_1<n\leq N_2}n^{-\alpha}/Z_{N_2}$. Then

$$p_s(N_2)=(1-\varepsilon)p_s(N_1)+\varepsilon p_s(\text{tail}),\qquad |p_s(N_2)-p_s(N_1)|\leq\varepsilon.$$

For the three normalized sector shares their total absolute change is at most 2ε.

**Proof.** Split the N₂ sum at N₁ and normalize each piece. Both $p_s(N_1)$ and $p_s(\mathrm{tail})$ lie in [0,1]. The sector vectors are probability distributions, whose total absolute difference is at most two. ∎

The released phase effects depend on n and frozen spectrum, frame, threshold and phase-step values, not on N. The proposition therefore applies to the frozen share comparison. It is not automatically a bound for address loads: their response includes log n/log N and changes with N.

| Frozen old-filter replay | P share | D share | R share |
|---|---:|---:|---:|
| N=1,000,000 | 0.0500000000 | 0.2680000000 | 0.6820000000 |
| N=1,015,000 | 0.0500000254 | 0.2680000183 | 0.6819999563 |

Here α=1.8996876950554356 and threshold b=1.44767317035244 are the original parameters. Direct summation gives ε=7.88312551×10⁻⁸. The largest observed change, approximately 4.37×10⁻⁸, obeys the bound. The result substantiates compatibility of the new source with the frozen arithmetic filter. It also explains why small cutoff changes can leave the partition nearly unchanged; partition stability alone does not select this particular N.

The separately declared MCC 3.0 recalibration uses α=1.8996877935161325 and b=1.4476744689338703 at N=1,015,000. The structural-coordinate tests in Section 5 use this configuration. Their reference macro replay gives q=−0.5285585894376319, rotation 207.5102418659153 km/s and conditional lensing 0.5355822400088303 arcsec. These are inherited model outputs freshly replayed through the supplied functions, not new measurements. The two calibrations are separate configurations; the new paper does not fit additional parameters.

The common carrier is the finite state substrate between arithmetic admission and physical loads. This paper's structural replay uses the released uniform-carrier and homogeneous macro branch and its conditional local lens patch. The code-count theorem does not identify source cardinality with carrier dimension. More general correlated-state readouts are documented in the companion WRRA paper [4].

## 7 Reproduction and the scope of the result

The accompanying package contains audit_A.py, its JSON output, the byte-pinned structural replay and dependency manifest, the frozen old-filter replay, and a one-command runner. The dependency manifest pins the Step 1 dependency release to commit 408602d166b3ec6635aff24803ef578580386112 and records file hashes. Its nested dependencies/source_manifest.json identifies the original function-source commit 41b3a2ec356033d58877a3c6bfea00421ae5f1e9. The structural script checks those hashes before executing. The local release manifest records every included source and result file. Run Python without optimization so the inherited assertion checks remain enabled. Tested versions are Python 3.12.14, NumPy 2.3.5 and mpmath 1.3.0.

The runner checks three distinct results: exact source coding and numerical zeta diagnostics; the no-refit old-filter comparison; and coordinate transport through the recalibrated MCC reference. A successful run must satisfy all registered predicates and the recorded numerical comparisons. The contour calculation is labeled numerical throughout. It is not counted as a proof merely because an assertion passes.

The precise contribution is an auditable finite-source rule connected to a structured arithmetic filter and the existing WRRA carrier interface. Exact arithmetic gives its representation and transport guarantees; calculation tests its declared realization and reveals its boundary sensitivity. The product-domain admission, T=2πH, inherited harmonic ledger, arithmetic classifier and physical response rules remain model specifications. Deriving them from a common physical principle would strengthen the model, but is distinct from testing whether this stated construction works. Under changed calibration or boundary data, the same disclosed rule defines a new configuration whose outputs can be tested again.

## Appendix A Explicit arithmetic readout

Let γ=(14.134725141734695,21.022039638771556,25.01085758014569,30.424876125859512). These four inherited drive frequencies are distinct in role from the count C=70 used for source size. With eight frames k=0,…,7, coefficient 1/2 on each frequency, zero offsets and phase step ξ=0.1, set

$$d_k(n)=\frac12\sum_{j=1}^{4}\cos[\gamma_j(\log n+\xi k)],\qquad a_k(n)=\frac{1}{1+\exp[-(d_k(n)-b)]}.$$

For eligible odd composites, $e_P(n)=1-\prod_{k=0}^{7}(1-a_k(n))$; for other addresses $e_P=0$. Even composites have $e_D=1$, and $e_R=1-e_P-e_D$. The threshold is denoted b here to distinguish it from the tuple coordinate h. The code computes the product via logaddexp and expm1 for numerical stability. The fitted fractions are address-weight shares; conversion to SI energy uses the separate released load and calibration rules.

## References

[1] NIST Digital Library of Mathematical Functions. Section 25.2, especially Euler–Maclaurin representations of the Riemann zeta function. https://dlmf.nist.gov/25.2 (accessed 8 October 2026).

[2] mpmath 1.3.0 documentation. Zeta functions, including zetazero and nzeros. https://mpmath.org/doc/current/functions/zeta.html.

[3] Choi, W. and Choi, J. Minimal Computing Cosmology 3.0 (2026). https://doi.org/10.5281/zenodo.23202732. Pinned source and reproduction metadata are included with this paper.

[4] Choi, W. and Choi, J. Developing a finite WRRA toy model to explore quantum gravity vacuum energy and dark sector connections, v1.8 (2026). https://doi.org/10.5281/zenodo.23233991.
