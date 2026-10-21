Taken together, these are a toy-model proposal whose specified connections are assessed by the computations below. They are not presented as three completed resolutions. Each output is assessed through its disclosed transformation and failure conditions.

## 85 Verified inputs and the finite construction

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

### Reference state and coefficient provenance

The address-share targets (0.05, 0.268, 0.682) and the inherited SI-energy targets (0.0493, 0.265, 0.6857) are distinct inputs. In `snapshots/source_step2/dependencies/original/m10_results.json`, the frozen 0.9 address measure with uniform carrier I/d has reference moments (0.0500000000000009, 0.2789373775449565, 0.687748727555431). Since Tr[(I/d)A_s]=1, the original calibration is eta_s = u_crit F_s / mu_s(ref), at a=1 and V0=1 m³. This reproduces the eta values above. Subsequent arithmetic and correlation probes retain these coefficients; their changed moments need not reproduce the original energy fractions exactly. Thus 5/26.8/68.2 is an address-admission calibration, not a second assertion about the same energy ledger.

H0=67.4 km/s/Mpc is the adopted Planck 2018 base-Lambda-CDM reference [8]; u_crit=3 H0² c²/(8 pi G) is calculated from that anchor. The historical energy fractions are the project's frozen rounded reference convention, not claimed here as the exact entries of a newly fitted Planck likelihood. The address targets are the project's separate rounded construction targets. The frame offset is xi k with xi=0.1 and k=0,...,7; no independent xi_k parameter is introduced.

## 86 Exact correlation-preserving interface

Define the three unnormalized sector-weighted carrier operators and scalar loads:

$$
\Sigma_s=\sum_n w_nf_s(n)\rho_n,\qquad L_s=\operatorname{Tr}(\Sigma_s A_s).
$$

