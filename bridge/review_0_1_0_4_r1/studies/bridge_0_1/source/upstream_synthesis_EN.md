# Abstract

We present a finite upstream construction connecting arithmetic source states, two-stage filtering, retained relations, selective readout, record formation and a common internal energy-current state. The construction consolidates the completed Wonsik Reality Renderer Architecture (WRRA) M upstream sequence through version 0.10. Prime-factor addresses carry normalized finite weights; a blurred admission filter followed by a normal return filter retains composite relations. Binary pairing provides an explicit readout of odd composite residues. At exponent two, the uncalibrated finite readout is 4.876893353% at address cutoff N=10⁶. Joint calibration of the exponent and admission rate reproduces adopted targets of 5% and 26.8%, with the remaining 68.2% fixed by completeness. A bounded spatial coupling supplies a 95-dimensional symmetric nucleon model whose calibrated ground state supports electromagnetic and weak currents. A completely positive residue preparation map then transfers source-dependent conditional address weights to a mixed internal state, from which energy and currents are evaluated together. Record channels conserve branch probabilities while changing coherence and subsequent interference. The integrated generator combines these operations with a conservative source-stock ledger. We distinguish arithmetic outputs, calibrated returns, fixed-parameter controls and conditional physical load mappings. Reproducible calculations and explicit failure criteria establish a closed computational handoff at version 0.10, while physical clock assignment, energy supply, particle-species selection and a durable record medium remain specified interfaces for subsequent applications.

Keywords: finite-state construction; arithmetic filtering; common carrier; quantum instruments; nucleon currents; reproducibility.

The central result is an executable connection: source preparation → admission and return → residue readout → recording → conditional internal state → joint energy and current readout. The same notation is used throughout, and quantities with different normalization or units occupy separate ledgers.

# 1 Physical question and finite construction

A composition model must specify how an initial informational state becomes retained structure and how retained structure acquires physical readouts. The minimum-computation question motivates a reuse of prime-factor relations, a common carrier and selective phenotype readout. Here minimum computation means a proposed organization of sufficient operations, including necessary slack and robustness. The implemented configuration is one adopted possible construction; no global uniqueness or optimality theorem is assumed.

The finite address space is spanned by |n⟩, 2 ≤ n ≤ N. Address 1 is the empty prime product and serves as a vacuum reference when an extended ledger is needed. It is excluded from the active normalization. The fold index Ω(n)−1 counts factor multiplicity relative to a prime; the relation label distinguishes primes from composites. These are arithmetic organization indices, rather than measured spatial dimensions. A composite admitted under a blurred prime-like readout retains its composite arithmetic identity.

$$
Z_N(\alpha)=\sum_{n=2}^{N}n^{-\alpha},\quad w_n=\frac{n^{-\alpha}}{Z_N(\alpha)},\quad \sum_{n=2}^{N}w_n=1.
$$

The finite sum is the primary object. Euler products explain the structural reuse of prime factors [1]; an infinite-series value may be used as an analytical comparison. No physically realized infinity is required. In the Infinity = Null convention, an unspecified infinite physical resource contributes no instantiated object to the execution ledger. This convention does not alter finite arithmetic or forbid mathematical limiting arguments.

The evidence chain is evaluated as verified input → WRRA transformation → calculated output → failure criterion → conclusion. Calibration to known quantities is an explicit theory-construction operation. A successful calibrated return is credited as reproduction, and fixed-parameter controls assess consequences of the constructed state. Unmeasured physical readouts computed after fixing verified inputs are conditional WRRA predictions, with the declared preparation and physical mapping specifying their scope. Originality resides in the finite architecture, transformations and connections; independent numerical novelty is not required. The reviewed early collection [2], spatial-current collection [3] and source-generator collection [4] define the upstream lineage. The separate downstream version family is used only through declared load interfaces.

# 2 Ordered filtering and retained relations

Let ρ be a positive unit-trace input, A an admission contraction and B a return contraction. Admission gives ρin=AρA†. Initial reflection and subsequent normal return are distinct microscopic channels but contribute to the same coarse return label R. The residue is the admitted component that the normal filter cannot return.

$$
A^\dagger A\le I,\quad B^\dagger B\le I,\quad q_\mathrm{res}=\operatorname{Tr}\rho A^\dagger(I-B^\dagger B)A.
$$

$$
q_R=1-\operatorname{Tr}A\rho A^\dagger+\operatorname{Tr}BA\rho A^\dagger B^\dagger,\quad q_R+q_\mathrm{res}=1.
$$

Completeness follows directly by adding the two expressions. The ordering matters when A and B do not commute. The numerical address implementation uses diagonal operators: the normal return projector selects primes, even composites are retained in D, and odd composites enter the selective residue with admission rate β. Thus static recognition of a composite and a dynamical unfolding rule are separate operations. A persistent residue additionally requires its retained subspace K=ker B to remain invariant under the chosen subsequent update.

$$
E_\phi=\beta P_\mathrm{odd,c},\quad E_D=P_\mathrm{even,c},\quad E_R=P_\mathrm{prime}+(1-\beta)P_\mathrm{odd,c},\quad E_\phi+E_D+E_R=I.
$$

Positive effects give fℓ=Tr(ρEℓ), with ℓ∈{φ,D,R}. A diagonal realization has four Kraus branches: √β Podd,c, Peven,c, √(1−β) Podd,c and Pprime. Their adjoint products sum to I. The last two branches represent initial reflection and normal return. Their coarse aggregation is a sum of density operators; it does not justify adding their amplitudes into a single pure return vector.

For the fixed source weight, all branch norms are computed with one denominator. Failure occurs if an effect loses positivity, the instrument loses completeness, a return branch is counted twice, or the declared retained update leaks outside K without an explicit leakage ledger. These criteria connect the initial two-stage hypothesis to the executable instrument of the later source studies [2,4].

# 3 Binary readout and composition calibration

The renderer provides an explicit arithmetic readout. Writing n=2m+r, r∈{0,1}, define the isometry V|n⟩=|m⟩⊗|r⟩. The r=1 port is the unpaired remainder of binary grouping. Composite selection before this port yields the effect in Section 2. Table 1 compares a fixed-exponent arithmetic calculation with a joint calibration.

$$
V^\dagger V=I,\quad E_\phi=\beta P_cV^\dagger(I\otimes|1\rangle\langle1|)VP_c.
$$

$$
f_\mathrm{even,c}=2^{-\alpha}\frac{Z_{\lfloor N/2\rfloor}(\alpha)}{Z_N(\alpha)},\quad f_\mathrm{odd,c}=1-f_\mathrm{even,c}-\frac{\sum_{p\le N}p^{-\alpha}}{Z_N(\alpha)}.
$$

The first row is an arithmetic output without a 5% target input. The second uses the adopted φ=5% and D=26.8% targets to determine α and β; R follows from completeness. These rounded targets reflect the scale of cosmological composition, rather than an exact Planck parameter triplet [5]. At fixed calibrated parameters, N=10⁴,10⁵,10⁶ gives φ=4.989044%,4.998716%,5.000000%. The mathematical infinite-series comparison at α=2 is 4.876952810%; the finite value remains the instantiated result.

The frame construction replaces constant admission by address-dependent attempts with depletion. Four low zeta-zero frequencies, eight frames and phase shift ξ=0.1 give a calibrated threshold h=1.4476731704. Its aggregate βeff equals the constant-entry β, although its address state differs. Holding α and h fixed, closing at four or sixteen frames yields φ=3.704795% or 5.682474%. At fixed h, stationary zeta phases, equally spaced frequencies and constant entry give 4.859796%,5.095593%,4.710550%.

After separately recalibrating each driver to 5%, conditional address-distribution distances from the baseline remain 0.0516382,0.0156483,0.0072180. Equal totals therefore leave discriminating address observables. Neither these comparisons nor the selected zeta phases identify a unique cosmic driver.

# 4 From residue families to common nucleon currents

The early particle construction selects residue markers 45 and 75 and prime families 3 and 5. Proton and neutron labels are assigned externally. These markers organize the constituent response and fold-decay ledger; they do not by themselves identify particle species from the number-theoretic distribution. The reviewed decay and internal-mixing stages supply the common spin-flavour state and a calibrated weak-transition normalization [2].

$$
\mathcal R_{35}=\left(\sum_{k\ge1,\,3^k\le N}3^{-\alpha k}\right)\left(\sum_{k\ge1,\,5^k\le N}5^{-\alpha k}\right)=0.00698600035273.
$$

We reserve ℛ35 for this prime-family activity, avoiding confusion with the return sector R. In the two-state representation, symmetric and mixed spin-flavour states have axial readouts 5/3 and 1/3. The calibrated mixture qE=0.293525 returns gA=1.2753 and gV=1. This internal mixture is distinct from the cosmological fraction D or the retained stock Actual.

$$
H_B(0)=(m_B-e_-)I+\Delta\begin{pmatrix}0&-x_c\\-x_c&1\end{pmatrix},\quad x_c=C\sqrt{\mathcal R_{35}},\quad g_A=\frac53-\frac43q_E.
$$

Upstream 0.4 realizes the spatial labels with a Gaussian in two Jacobi coordinates and two orthogonal quadratic modes. Their permutation-aligned contraction with spin-flavour transitions gives W_B=[[0,1],[1,0]] in the retained two-state block. Actual spatial integration therefore supports the coupling. Magnetic response is the field derivative of the same Hamiltonian, with a separately calibrated field-deformation coefficient η.

$$
H_B(b)=H_B(0)-bM_B,\quad M_B=D_B+c_0I+\tau_B\eta x_cW_B,\quad M_B=-\partial_bH_B.
$$

Here b=μNB is field energy, τp=+1 and τn=−1; DB is the projected single-slot magnetic response and c0 its calibrated isoscalar correction. The quantity e− is the lowest energy of the two-state Δ matrix before the mass offset. Joint calibration gives C=13.193474298, η=0.438092893 and the input moments 2.79284734463 and −1.91304276 nuclear magnetons. The induced collective contribution is ⟨ηxcW⟩=0.439987793. A constant collective-current model sharing these ground moments differs in excited and transition moments: the proton transition changes from −0.910757154 to −0.711259793 nuclear magnetons [3]. Equal anchor values thus coexist with different operator consequences.

Masses enter as calibrated offsets and effective constituent response energies. The construction credits their common return without treating them as independently derived quark masses. The unprojected quadratic coupling creates discarded higher modes, with squared norm 7/3 in the stated diagnostic; this is a norm diagnostic, not a probability. The next stage explicitly tests the spatial enlargement.

# 5 Bounded coupling and physical scales

The quadratic coupling does not remain stable under unrestricted spatial enlargement. Its large-distance coefficient is 1/4−xc/√6, and the two-state calibration xc=1.1027408857 exceeds √6/4=0.6123724357. Finite enlarged calculations already show downward drift. This failure motivates the bounded interaction of upstream 0.5, preserving the retained two-state coupling and permutation symmetry [3].

$$
W_\lambda=\frac{W_0}{k_\lambda(1+\lambda s)},\quad s=(x^2+y^2)/\ell^2,\quad \lambda>0.
$$

$$
k_\lambda=\frac12\left\langle\frac{X_1^2+X_2^2}{1+\lambda s}\right\rangle_0,\quad \|W_\lambda\|\le\frac1{\sqrt6\lambda k_\lambda}.
$$

A positive oscillator kinetic-confining part plus a bounded coupling gives a lower energy bound. At λ=1, kλ=0.1915144733. The implementation uses complete scalar positive-parity shells, projects the joint spatial-spin-flavour state with the six slot permutations, and diagonalizes h=diag(nx+ny+l)−xcWλ. At shell cutoff K=8 there are 165 spatial modes and 95 symmetric states; K=10 gives 286 and 161. The adopted rational bounding function is part of the declared effective model.

$$
H_B=(m_B-\Delta e_0)I+\Delta h,\quad \Delta=\frac{1370\ \mathrm{MeV}-\bar m}{e_1-e_0},\quad \bar m=(m_p+m_n)/2.
$$

The axial input recalibrates xc=0.8208877164. Assigning the first positive-parity excitation conditionally to the N(1440) real-pole centre at 1370 MeV gives Δ=507.032217686 MeV and gap 431.081244315 MeV. A Hermitian discrete eigenvalue represents the selected centre; a resonance width and complex pole require additional continuum dynamics. The excitation-centre choice is an input, not a species discovery.

The original point-charge fit gives ℓ=0.61619621794 fm and an uncalibrated neutron mean-square charge radius −0.186912 fm², differing from −0.1155 fm². This failed external comparison is retained. At fixed coefficients, K=10 changes the excitation gap by about 0.00854 MeV, demonstrating numerical stability of the finite configuration. The subsequent charge-current revision changes the length calibration while retaining the dimensionless Hamiltonian and excitation scale.

# 6 Finite currents and the decay ledger

Upstream 0.6 evaluates finite-momentum currents in the same 95-dimensional state. A zero-charge isovector counterterm and a common width jointly return both charge radii: ℓ=0.65715059784 fm and cE=−0.09708290347 fm². With HC=0.1973269804 GeV fm, the specified counterterm is [3]

$$
C_E(Q^2)=-\frac{Q^2c_E}{6HC^2}e^{-Q^2a_E^2/(6HC^2)},\quad a_E=\ell,\quad G_{E,p/n}=G^\mathrm{point}_{E,p/n}\pm C_E.
$$

$$
G_E^V=G_{E,p}-G_{E,n},\quad F_1=\frac{G_E+\tau G_M}{1+\tau},\quad F_2=\frac{G_M-G_E}{1+\tau},\quad \tau=\frac{Q^2}{4\bar M^2}.
$$

Here M̄ is expressed in GeV for Q² in GeV²; write the dimensional magnetic readout as M_B(Q²)=μN 𝓜_B(Q²). The dimensionless Sachs magnetic factor in the conversion above is G_M=(M̄/mp)𝓜_B, with 𝓜_B the numerical nuclear-magneton readout. The actual n→p slot transition agrees with the electromagnetic isovector difference. The projected longitudinal Fourier current [H,ρ(q)]/q obeys the transition continuity relation. Its odd Fourier adjoint convention is maintained. A complete transverse relativistic gauge current is a distinct physical construction.

At Q²=0.1 GeV² the ground-state readouts are GEp=0.7367799, GEn=0.0399134, Mp=1.9543552 μN, Mn=−1.4207472 μN and GA=0.9039833. The uncalibrated neutron magnetic radius remains 0.831987107 fm against the retained comparison 0.864 fm. Changing aE preserves the charge and its slope but changes finite-momentum curvature. These are concrete diagnostics after successful joint calibration.

$$
\Gamma_0=\frac{\kappa^2\mathcal R_{35}G_F^2|V_{ud}|^2(1+3g_A^2)I_0}{2\pi^3\hbar},\quad K_\beta=(K_\mathrm{tree}+\delta K_\mathrm{out})(1+\Delta_R^V).
$$

The inherited inputs are GF=1.1663787×10⁻⁵ GeV⁻², |Vud|=0.97367 and Coulomb-weighted allowed phase-space integral I0=0.0589405883156 MeV⁵; GF is converted to MeV⁻² in the rate. The three-body decay uses exact tree recoil, weak magnetism, a small timelike continuation of current slopes and leading electron-inclusive outer radiation [6]. The fixed inner input ΔRV=0.02467(22) is the 2018 reference [7]. The resulting multiplier is 1.03792926261. Keeping κ=12.200294834431 gives τ=846.204102380 s; separately fitting κ=11.975301265858 returns 878.3 s. These two ledgers must remain separate. Higher radiation-recoil terms, a microscopic γW box and induced pseudoscalar completion are outside the executed decay.

# 7 Source variation and conservative transport

Upstream 0.7 introduces a normalized coherent source with controlled log intensities and phases. The arithmetic filter is retained, so source modifications propagate to branch weights and conditional address states. Writing νp(n) for the exponent of prime p in n, a prime-family log-intensity εp multiplies probabilities by exp(εpνp(n)), hence amplitudes by its square root; the phase factor is exp(iθpνp(n)). The intensity controls and the coherent probe specify separate experiments [4].

$$
\lvert\psi_S\rangle=\frac1{\sqrt{\mathcal Z}}\sum_{n=2}^{N}n^{-\alpha/2}e^{\sum_p(\epsilon_p/2+i\theta_p)\nu_p(n)}\lvert n\rangle,\quad \rho_S=\lvert\psi_S\rangle\langle\psi_S\rvert.
$$

Diagonal filter effects see address populations. To test coherence, the finite N=161 probe mixes addresses 3 and 9 with angle 0.25 and scans relative phase 0, π/2 and π. Population-only maps later in the chain cannot inherit phase sensitivity merely because their source was initially coherent. The coherent probe and the dephased preparation map therefore retain separate observable contracts.

Source and Actual are conservative stocks. Let S and A be available-source and retained-stock fractions with S+A=1. Here A is a scalar stock, distinct from the admission operator A in Section 2. A step first releases leakage νA to Source and then processes the fraction u of the updated available source. For retained branch fraction r=fφ+fD, the update is

$$
\widetilde A=(1-\nu)A,\quad\widetilde S=S+\nu A,\quad A^+=\widetilde A+ur\widetilde S,\quad S^+=(1-ur)\widetilde S.
$$

The sum remains one, with 0≤u,ν,r≤1. A single complete release and seven zero releases reproduce the eight-step reference. Repeated u=0.2 for 32 steps without leakage yields Actual=0.8778861396212083. Under u=0.2 and ν=0.1 the stationary stock is 0.4044772322564214. Thus the calibrated one-pass r=0.318 is not a universal stock attractor; a chosen recycling-leakage balance is required.

Failure criteria include loss of source normalization, negative stocks, failure of conservation, or a source perturbation not reaching the relevant branch or address ledger. Stock fraction, individual draw probability and particle internal energy are retained as separate typed quantities.

# 8 Shutter recording and subsequent interference

Upstream 0.8 defines a shutter channel in the three-label representation φ,D,R. It interpolates between a coherent label state and a fully recorded label mixture. A recording channel is completely positive and trace preserving, leaves the branch probabilities unchanged, and suppresses off-diagonal coherence. Its parameter ηrec is distinct from the calibrated magnetic coefficient η.

$$
\mathcal S_{\eta_\mathrm{rec}}(\rho)=(1-\eta_\mathrm{rec})\rho+\eta_\mathrm{rec}\sum_\ell P_\ell\rho P_\ell,\quad 0\le\eta_\mathrm{rec}\le1.
$$

$$
\eta_\mathrm{eff}=\eta_1+\eta_2-\eta_1\eta_2,\quad \mathcal S_1^2=\mathcal S_1,\quad \operatorname{Tr}(P_\ell\mathcal S_{\eta_\mathrm{rec}}(\rho))=f_\ell.
$$

For the coherent coarse label state with probabilities 0.05,0.268,0.682, full recording gives purity 0.539448. Subsequent mixing can distinguish the order of operations. In the stored angle-0.25 comparison, rotate then record gives φ=0.007845982334803351, whereas record then rotate gives φ=0.06334350075394928. Recording therefore has an operational consequence despite leaving its immediate branch probabilities unchanged [4].

Table 2 resolves the two return processes. The address vectors and the three-label representation are different descriptions. The latter admits a specified coherent label experiment; it is not a proof that the microscopic return mixture is pure. In a recorded run, one draw selects a branch according to its norm and the selected conditional vector is normalized to one. Unselected branches remain in the ensemble ledger.

The executed result is a finite recording operation and its state-update contract. A stable physical record additionally needs a medium, coupling, storage energy, a time scale and a persistence test. These quantities are left unassigned in the generator rather than inferred from the existence of a mathematical channel. Failure means changed probabilities under the shutter alone, loss of positivity, inconsistent coarse aggregation, or disagreement of conditional sampling with the stated instrument.

# 9 Residue preparation and joint energy-current readout

Upstream 0.9 supplies the explicit connection between the φ address residue and the frozen internal Hamiltonian of Sections 5–6. Let g and e1 be its orthonormal ground and first excited vectors. The selector χ(n) marks odd ν3(n), and t is its probability within the normalized φ address state. Preparation strength a∈[0,1] controls a measure-and-prepare channel [4].

$$
\mathcal P_a(\sigma_\phi)=\sum_n\langle n|\sigma_\phi|n\rangle\{[1-a\chi(n)]|g\rangle\langle g|+a\chi(n)|e_1\rangle\langle e_1|\}.
$$

$$
L_{n,g}=\sqrt{1-a\chi(n)}|g\rangle\langle n|,\quad L_{n,e}=\sqrt{a\chi(n)}|e_1\rangle\langle n|,\quad \sum L^\dagger L=I_\phi.
$$

The Kraus identity proves complete positivity and trace preservation on the φ input space. The resulting internal state is ρint=(1−at)gg†+at e1e1†. The unnormalized sector density has trace fφ; the conditional internal density has trace one. D and R have no particle-current assignment in this adapter. The map transfers address populations to a declared internal ensemble; it does not create a MeV scale from dimensionless normalization.

$$
\langle E\rangle_B=m_B+at\Delta(e_1-e_0),\quad J_B(Q^2)=\operatorname{Tr}\rho_\mathrm{int}\widehat J_B(Q^2).
$$

The baseline gives t=0.3998832725128899. At a=0.2, the excited population is 0.07997665450257799 and conditional energy excess is 34.47643573911998 MeV. Both energy and current use this same density operator. Table 3 shows the resulting joint current readouts, which differ from the ground-state values in Section 6 without changing the frozen operator calibration.

At ε3=−0.15 and +0.15 the conditional excess becomes 34.7064126183 and 34.0222152399 MeV. A phase-only θ3=0.7 leaves this dephased preparation unchanged, as required by its population dependence. The executable current adapter uses the frozen real 95-dimensional modes and rejects unsupported complex current inputs. Orthogonal complex state preparation can be formulated, but a general complex-current adapter has not been executed.

# 10 Integrated generator and physical load interfaces

Upstream 0.10 executes the completed chain for six source cases: baseline, low/high prime-2 amplitude, low/high prime-3 amplitude and prime-3 phase. For each case the generator checks source normalization, four-branch instrument, record draw, conditional address state, internal preparation, same-state energy-current output and the stock protocols. Draws 0.02,0.10,0.32,0.90 test branch selection. When φ is selected, its actual conditional vector supplies the preparation; other branches retain null internal-current readouts [4].

The handoff includes source controls, branch probabilities, record label, conditional state scope, excitation population, energy excess, current momentum Q² and stock protocol. A named baseline anchors comparisons; array position does not define the baseline. The reference protocol has one full release followed by seven zero releases, and the recycling protocol uses 32 releases of 0.2. This closes upstream development at 0.10. The present integrated version reorganizes that frozen result without adding an upstream 0.11.

The Physics preparation also executed a conditional vacuum-reference and uniform-load bridge [8,9]. For an extended normalized state ρ̂ and vacuum reference ρ0, a declared physical energy operator gives the relative gravitational readout below. A common C(V)I cancels because both traces equal one; actual state-dependent energy changes remain.

$$
E_g(V)=\operatorname{Tr}[(\widehat\rho-\rho_0)H_\mu(V)]+E_R(V),\quad p_g=-\partial_VE_g.
$$

$$
E_g=u_*[(f_\phi+f_D)V_0+f_RV],\quad p_g=-f_Ru_*,\quad q_0=\tfrac12(1-3f_R)=-0.523.
$$

The second expression adopts pressureless fixed-total-energy φ,D and constant-density R. It reproduces the energy fractions at V0 and, with the declared uniform expansion response, q0=−0.523 at V=V0. Away from V0, the evolving energy fractions must be used in q(V); this value is not volume-independent. The reference test used common shifts up to 10¹²⁰u* and retained a state-specific δu=0.125u* change. The prepared extension reports 33 vacuum checks, 12 twist-load checks and 38 phase-ledger checks. These are physical-map calculations under specified load rules; the upstream information fractions alone do not fix absolute energy density or a covariant stress tensor.

# 11 Reproducibility and conclusions

The reviewed archives preserve source inputs, executable code, results, corrections and hash ledgers [2–4]. The 0.4–0.6 collection passes 112,150,128 stage checks plus five cross-stage checks, totalling 395. The 0.7–0.10 collection passes 113,431,318,465 stage checks plus 68 review checks, totalling 1395. Its clean archive replay contains 151 manifested files and reproduces 13 declared JSON outputs byte for byte. These are implementation and regression results, not empirical probabilities. Table 4 states the conclusions supported at each layer.

Calibration, internal control and external comparison answer different questions. A target return establishes a constructed correspondence; a fixed-parameter variation establishes a consequence of that correspondence; an uncalibrated discrepancy locates a missing physical ingredient. The neutron magnetic-radius difference, charge-curvature dependence, externally chosen species and excitation-centre assignment remain visible. Their presence does not erase the finite composition and common-state reproduction achieved by the construction.

The integrated result makes retained arithmetic relations operational. A finite instrument partitions their norm, binary readout selects a phenotype, recording modifies coherence, and a specified preparation map produces an internal state with joint energy and current expectations. Source controls propagate through this chain under documented cases. The scalar totals alone cannot select a unique phase driver, while address distributions and common-state currents provide additional diagnostics.

Upstream closure means that the specified finite state chain and handoff are complete through 0.10. Physical seconds require a clock calibration; excitation energy requires a supply and exchange ledger; species require a selection rule; durable records require a medium and stability dynamics. Subsequent applications can fill these interfaces and test the declared failure criteria without reopening the completed arithmetic and operator definitions.

# References and declarations

[1] NIST. Digital Library of Mathematical Functions, §27.4 Euler Products and Dirichlet Series. https://dlmf.nist.gov/27.4 (accessed 3 October 2026).

[2] Choi, W. WRRA M Upstream Studies Reviewed Collection r1: Two Stage Filters, Zeta Frames, Particle Decay and Internal Nucleon Currents (2026). https://doi.org/10.5281/zenodo.23092499

[3] Choi, W. WRRA M Upstream 0.4–0.6 Reviewed Collection r1: Spatial Coupling, Stability, Excitation Scales and Finite Currents (2026). https://doi.org/10.5281/zenodo.23112253

[4] Choi, W. WRRA M Upstream 0.7–0.10 Reviewed Collection r1: SOURCE, Filters, Shutter, Residue Currents and Integrated Generator (2026). https://doi.org/10.5281/zenodo.23115550

[5] Planck Collaboration, Aghanim, N. et al. Planck 2018 results VI: Cosmological parameters. Astronomy & Astrophysics 641, A6 (2020). https://doi.org/10.1051/0004-6361/201833910

[6] Seng, C.-Y. Radiative corrections to semileptonic beta decays: Progress and challenges. Particles 4, 397–467 (2021). https://doi.org/10.3390/particles4040034

[7] Seng, C.-Y., Gorchtein, M., Patel, H.H., Ramsey-Musolf, M.J. Reduced hadronic uncertainty in the determination of Vud. Physical Review Letters 121, 241804 (2018). https://doi.org/10.1103/PhysRevLett.121.241804

[8] Choi, W., Choi, J. Reproduction of the ordinary-matter 5% composition, terminology edition r9 (2026). Prepared manuscript and calculation sources: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/main/submission/matter_fraction_r9

[9] Choi, W., Choi, J. Extension possibilities and connection conditions, r8 (2026). Prepared manuscript: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/main/submission/extensions_r8

Data availability. The underlying reviewed code, fixed inputs and verification records are available in [2–4] and https://github.com/Wonsik-Choi-janefather/wrra-m-0.1. The present synthesis introduces no newly fitted upstream parameters. The prior Physics preparation manuscripts, “Reproduction of the ordinary-matter 5% composition” r9 and “Extension possibilities and connection conditions” r8 (2 October 2026), provide the renderer comparisons and conditional load discussion used here.

Statements and Declarations. Author contributions: Wonsik Choi and Jeongin Choi contributed to the conceptual framework represented in the Physics preparation; Wonsik Choi developed and organized the calculations and manuscript materials.

AI assistance. ChatGPT was used to assist synthesis, mathematical presentation, code inspection, translation and document preparation. The authors retain responsibility for the scientific claims and final submission text.