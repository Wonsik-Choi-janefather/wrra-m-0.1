## 137. Particle/Component Replay and the Address–Color Interface

### 137.1 Inputs, transformation and provenance

This chapter integrates the color-interface audit through manuscript v0.8.2, separately from Book v0.27 and the cosmological junction v0.7-dev-r1 of Chapter 136. Its scientific scripts and frozen reference outputs are unchanged from color-audit v0.6. A later editorial number is not a new physical calculation. The book update reran `audit.py` and `dependency_audit.py`: 36/36 and 4/4 checks passed. These overlapping software checks establish the declared replay and algebraic contracts; they are not independent observations or an external peer-review verdict.

Verified inputs are the frozen Stage-3 source at commit `9d9daf21154e46e55b9fd0fd461c7c070156ab94`, $N=1{,}015{,}000$, $\alpha=1.8996877935161325$, $h=1.4476744689338703$, four adopted zeta-zero heights, eight admission frames, inherited assembly and charge rules, and a supplied three-color fundamental representation. The WRRA transformation applies admission to the finite address measure, assembles prime-labeled components and checks the dependency and information retained by the separate color branch. Outputs and falsification conditions are stated below. Known particle properties and mathematical representations remain legitimate interpreter inputs.

**Name control.** This book retains Wonsik Reality–Renderer Architecture, consistent with its established text and the 7 September Core 1.0 document headed “원식 현실-렌더러 구조의 범용 실행 아키텍처.” The expansion “Worldline-Residue-Resource-Action” printed in the v0.8.2 source is a conflicting label and is not adopted here. Worldlines, residues, resources and actions may be model concepts without redefining the architecture's name. This bibliographic discrepancy does not change the replay scripts or their mathematics.

### 137.2 Conditional component measure and actual order dependence

Address 1 is inactive. Define

$$w(n)=\frac{n^{-\alpha}}{\sum_{m=2}^{N}m^{-\alpha}},\qquad
p(n)=\frac{w(n)e_\phi(n)}{\sum_m w(m)e_\phi(m)}.$$

The admission effect is zero outside odd-composite addresses. The targeted replay returns 427,892 such addresses and phenotype weight $\sum_n w(n)e_\phi(n)=0.050000000000000065$. The measure $p$ is conditional on admission; it is not the full address measure or an observed particle abundance.

For a pool of the first $K$ primes, initialize $\lfloor n/\sum_j p_j\rfloor$ copies of each prime. Repeatedly traverse the declared ascending or descending order, taking at most one copy per prime per traversal when the residue permits, until the residue is below two. Every address retains exact integer reconstruction $n=\sum_j c_jp_j+r$. Define $a_j=\sum_n p(n)c_j(n)$ and $P_j=a_j/\sum_l a_l$. The reported candidate share counts the historically selected labels 5 and 47 in this component-number measure.

| Declared assembly | Conditional candidate share | Mean component count |
|---|---:|---:|
| K15 ascending | 0.129471986937 | 15.9763714572 |
| K15 descending | 0.127159411697 | 11.4294924701 |
| K16 ascending | 0.124982781217 | 15.2321441711 |
| K16 descending | 0.111240636923 | 10.5785808287 |

For K15, $\frac12\sum_j|P_j^{\rm asc}-P_j^{\rm desc}|=0.20472100116369085$. The upstream code already computed this order dependence; the audit reproduces it. Each fixed order is a valid declared algorithm. The nonzero distance rejects equality of these two aggregate distributions, not the legitimacy of a specified interpreter. Zero distance would not prove per-address equality or invariance under every possible order. Particle names, selected labels and the 16-channel charge table are supplied; exact rational neutrality of the declared motifs is a consistency achievement, not a new derivation of their charges.

### 137.3 What the color routine actually reads

The original `color_check()` has no arithmetic-state parameter. It constructs the signed six permutations of three colors and eight matrices internally. Recursive bytecode inspection and restricted-namespace execution find only NumPy, itertools, math and five builtins as external reads, with no captured state. This is a source-specific dependency result under ordinary unmodified libraries. Targeted AST extraction bypasses unrelated import-time modules, so it is not a full Stage-3 pipeline rerun.

Let $T_a$ be the fundamental generators with $\operatorname{Tr}(T_aT_b)=\delta_{ab}/2$ and

$$Q_a=T_a\otimes I\otimes I+I\otimes T_a\otimes I+I\otimes I\otimes T_a.$$

The original matrices equal $2T_a$; this changes normalization but not annihilation or the common kernel. The adopted state is

$$|S\rangle=(|rgb\rangle+|gbr\rangle+|brg\rangle-|rbg\rangle-|grb\rangle-|bgr\rangle)/\sqrt6.$$

All eight total generators annihilate it. The common kernel has dimension one, both numerically and symbolically. The recorded 32 collective-rotation trials have maximum error $5.847\times10^{-16}$; the joint-state factorization test has error $1.507\times10^{-16}$. Product-rgb and one-site-phase controls give nonzero charge norms 0.707106781 and 0.816496581 and are rejected. Supplied SU(3) consistency is thus tested; arithmetic selection of SU(3) is not established by this routine.

### 137.4 Exact information-retention restriction

For any finite address space $H_A$ and color space $(\mathbb C^3)^{\otimes3}$ carrying the same fundamental action, let $P$ project onto the common kernel. If the joint density operator has **exact singlet support**,

$$\Omega=(I_A\otimes P)\Omega(I_A\otimes P),$$

then

$$P=|S\rangle\langle S|,\qquad \Omega=\sigma_A\otimes|S\rangle\langle S|.$$

The diagonal traceless generators leave only equal occupation of the three colors. Raising operators force opposite signs for exchanged permutations; these relations connect all six permutations and leave one normalized state. Expanding $\Omega=\sum_{nm}|n\rangle\langle m|\otimes C_{nm}$, rank-one support gives $C_{nm}=PC_{nm}P=c_{nm}P$. Positivity and unit trace give the unique address density matrix $\sigma_A=[c_{nm}]$. This is a conditional application of standard finite linear algebra, not new general QCD representation theory.

Deleting the address register leaves the same color state for every address preparation. A color-only measurement cannot recover distinct component labels; address-controlled collective SU(3) rotations also leave the singlet unchanged. Retain the address/component register when its distinctions are needed. A larger representation, additional spatial/flavor/gluon factors or tracked nonsinglet intermediates may change the constraint, but none is implemented by this audit. Exact support is stronger than zero mean charge.

### 137.5 Falsification and next executable step

Failure of the fixed-input replay, normalization or integer reconstruction; a nonzero generator action; a second common-kernel vector; a counterexample to factorization under its stated support assumption; or an unexpected arithmetic-state read falsifies the associated claim. Physical adequacy requires an explicit mapping and comparison to observations. A new independent numerical prediction is not a condition for recognizing the present reproducibility and interface contribution.

The next step is to declare a concrete address-dependent decoder/coupling, retain its input register, calculate its output and repeat the conservation, dependency and symmetry-breaking controls. Spin, flavor, binding, confinement, reaction rates and a full particle spectrum remain open. This clarifies the connection without withdrawing the earlier conditional assembly achievement.

Source: [color audit v0.8.2, DOI 10.5281/zenodo.23497517](https://doi.org/10.5281/zenodo.23497517), based on [v0.6, DOI 10.5281/zenodo.23496836](https://doi.org/10.5281/zenodo.23496836). Matching scripts and manifest: [publication/WRRA_Color_Interface_Audit_v0_8_2](https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/1070a2aab2d17bcd0b4978ba696f486868fdc055/publication/WRRA_Color_Interface_Audit_v0_8_2). Standard SU(3) background: David Tong, *The Standard Model*, Chapter 3. Source manuscripts and this book have separately identified editorial scope.
