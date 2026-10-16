# Part XXII — Connecting Zeta Readout, Folding Classes and Prime Space

*Connection study v0.4, 16 October 2026. These calculations are separate from cosmic-composition calibration.*

## 130 Output Permission to Spatial Readout

### Verification input

The inputs are a finite SOURCE state, prime-symmetric classification with address 1 kept as a reference, numerical permission from the analytic residual R3(s), the existing prime-block generators, and the distance, information-ownership and massless-transport rules of Chapters 114–117. At N=1,015,000 there are 79,608 primes, 236 composite prime powers and 935,155 mixed-prime composites. These are address counts, not numbers of spatial axes or cosmic fractions.

The universal classification makes no prime exceptional: primes have label 1, powers p^k with k>=2 have label 2, and composites requiring at least two distinct primes have label 3. Folding labels and the independent-axis count of a spatial generator are tested separately. Special treatment of prime 2 can remain a candidate readout specific to our universe. The existing 2,3,5 taps in Chapter 115 are preserved; their selection is not derived here.

### WRRA-specific transformation

#### 130.1 Roles and physical readout

| Layer | Question | Execution object |
|---|---|---|
| Zeta readout | Under what condition is output allowed? | Permission G_zeta(s) |
| Folding class | Which information is selected? | Projector Pi_fold,3 |
| Prime operators | In which relational/spatial structure is it unfolded? | Address map J, block generators and Laplacian |
| Existing spatial Renderer | How is it read as distance, transport and observation? | d=c Delta t, physical H and observation map |

Here “when” first means permission, not physical time. The parameter s is not identified with a clock. Event timing requires a further connection to physical evolution and shutters; physical time is not imposed retroactively on prephenotypic allocation.

The declared permission is G_zeta=1(|R3(s)|<=10^(-9)). Rounded finite raw address sums do not replace the analytic residual. Neither unique necessity of this gate from arithmetic classification nor its autonomous physical realization is proved.

#### 130.2 Output and hold together

Let Pi3=Pi_fold,3, 0<=G<=1, extend address states with zero auxiliary slots as needed, let J be an injective isometry on selected addresses, and let U_prime implement the declared prime SOURCE unitarily. Then

$$
|\phi_{\rm out}\rangle=U_{\rm prime}J\sqrt G\Pi_3|\psi\rangle,
\qquad |\phi_{\rm hold}\rangle=[(I-\Pi_3)+\sqrt{1-G}\Pi_3]|\psi\rangle,
$$
$$
\|\phi_{\rm out}\|^2+\|\phi_{\rm hold}\|^2=\|\psi\|^2.
$$

Hold is neither deletion nor a new energy sector. With output/hold labels this is an isometry; viewing the output alone gives a quantum instrument whose probability remains in the ledger. A positive trace-preserving observation map on the specified output space reads

$$
\widetilde\rho_{\rm out}=\mathcal R_{\rm space}
\left(U_{\rm prime}J\sqrt G\Pi_3\rho\Pi_3\sqrt GJ^\dagger U_{\rm prime}^\dagger\right).
$$

Its trace is Tr(G Pi3 rho). Conditional normalization never discards that probability. Propagation can change the arithmetic label at an occupied coordinate: [U,Pi3]=0 is not assumed. Output originating in class 3 and support confined to class 3 at every later step are different conditions. Hold, reference and auxiliary slots and observable ownership must travel together.

#### 130.3 Prime generators and relation preservation

The reused prime blocks are (3,71),(5,13),(7,11), with axis periods (213,65,77) and capacity M=1,066,065. N is an address cutoff and M an implementation capacity; neither replaces the existing KZF N_U.

$$
J|n\bmod M\rangle=|n\bmod213,n\bmod65,n\bmod77\rangle.
$$

The mutually coprime periods give a bijection on the complete residue space. N<M prevents collisions for the current addresses. Writing m_a for an axis period,

$$
\delta_a=(M/m_a)[(M/m_a)^{-1}\bmod m_a]\pmod M,
\quad JS_{\delta_a}=U_aJ,
$$
$$
JL_{\rm address}=L_{\rm SOURCE}J,
\qquad L_{\rm SOURCE}=\sum_a(2I-U_a-U_a^\dagger).
$$

Prime-coordinate translation is addition, not integer prime multiplication. The separately tested map n->pn mod M is compatible with coordinatewise multiplication, but multiplication by a resource prime merges residues and is not independently unitary. Retaining preimage records allows a reversible extension. Preservation of arbitrary integer size, products beyond the boundary or physical proximity is not automatic.

Earlier sorted packing preserved norm but not the natural coordinatewise prime multiplication. The earlier capacity 1,006,005 produced 7,165 selected-address collisions when converted to CRT. Replacing resource prime 67 by 71 resolves this declared implementation problem, without a claim of unique global resource minimality.

#### 130.4 Existing spatial and three-dimensional conditions

Reuse Chapter 114's distance d=c Delta t for one neighboring site. The specified flat periodic geometry is

$$
D(\boldsymbol x,\boldsymbol y)=d\sqrt{\sum_a\min(|x_a-y_a|,m_a-|x_a-y_a|)^2}.
$$

This is a declared geometric readout, not a unique arithmetic derivation of meters. c and the shutter are inherited fixed inputs. Section 7.3 supplies conditional dimensional minimality: for local propagating spin-2 admitted in d>=3,

$$
N_{\rm grav}(d)=(d+1)(d-2)/2,\quad C(d)=c_Ed+c_TN_{\rm grav}(d),
$$
$$
c_E,c_T\ge0,\quad c_E+c_T>0
\quad\Rightarrow\quad C(d+1)-C(d)=c_E+c_Td>0.
$$

The least-cost dimension in that allowed family is 3. This includes physical admissibility conditions; the arithmetic label “3” alone does not enforce three spatial axes.

Chapter 117's massless transport reuses H=hbar c|k|. This physical Hamiltonian and dimensionless prime-graph L remain distinct. Fifteen internal channels couple through the same spatial factor with I15. Tests use a declared frequency band free of temporal aliasing. Spatial nonlocality of this spectral operator and untested strict microscopic causality retain the earlier scope.

### Outputs and execution scope

| Test | Result | Scope |
|---|---|---|
| Prime-coordinate, axis-shift and Laplacian correspondence | maximum error 0 | New CRT SOURCE |
| Residue multiplication by seven declared primes | zero violations | All M residue states |
| Heat-kernel dimension | 3.0242082 / 3.0119065 / 3.0059001 | Diffusion scales 16 / 32 / 64 |
| Neighbor distance | 0.444083157552045 pm | Inherited c Delta t |
| Address-owned kernel profile | difference 0 | Existing taps, uniform test payload on new selection |
| Light speed in seven directions | maximum relative difference 1.11e-16 | Declared low-frequency modes |
| Photon norm / energy error | 8.88e-16 / relative 1.11e-16 | Declared band below 0.8 pi |

Connection v0.3 executed 21 relational checks and v0.4 executed 12 spatial checks. The 50 earlier v0.2 records are retained historical evidence, not added to this new execution count. These are numerical checks, not independent physical experiments.

Chapter 115's K_r taps and address ownership were reconstructed, but the test payload is uniform on the new selected addresses. The original sector-specific B_s,r,j, supply probability and complete GR/CMB pipeline were not recomputed on this lattice. Earlier fractions, amplitudes and observational scores are not retrospectively attributed to the new output construction.

The old 500x29x70 graph and new 213x65x77 CRT graph are different geometries. An address correspondence does not equate their neighbors, distances or physical predictions. This is a separate candidate using inherited distance, ownership and transport rules, not a silent replacement of existing space.

### Falsification conditions

Failure means an unauthorized class is output or its probability ownership is lost; CRT collisions or shift/Laplacian correspondence fail; output, hold or auxiliary records are omitted and break conservation; declared distance/shutter/speed/energy relations fail on the specified band; or predictions are transferred between the old and new geometries without checking them.

The remaining tasks are autonomous physical permission, output-event timing, micro-to-macro scale generation, variable curvature, complete Maxwell/Lorentz implementation and full GR/CMB connection on the new lattice.

### Assessment and genealogy

Zeta readout supplies permission; folding selects information classes; existing prime operators supply relations and space; the existing Renderer reads distance, transport and observations. This conditionally implements minimal computation, common carrier and phenotype in one finite output architecture. Reproducing known distance/transport rules is explanatory achievement, not a new constant prediction.

The source is the prime-symmetric zeta hologram archive v0.4. Its relation-preserving bridge and MCC spatial bridge include executable Python files, JSON results and excerpts of the original prime-partition and spatial texts. Exact filenames are listed in the package manifest. Editorial integration does not imply new external review or observational confirmation.

