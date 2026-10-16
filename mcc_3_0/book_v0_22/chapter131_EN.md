## 131 Zeta-Zero Phase Superposition and the Shape of Spatial Output

### Verification input

Chapter 130 uses zeta readout for output permission. This chapter tests whether the permitted zero set also participates in output shape. Inputs are the first 70 positive zeros $\rho_j=1/2+i\gamma_j$, cutoff $N=1{,}015{,}000$, 935,155 class-3 addresses and the same CRT space $(213,65,77)$. Two normalized preparations within the selected sector are compared: uniform amplitude and $n^{-\alpha/2}$ with inherited $\alpha=1.8996877935161325$. These are test preparations, not a reconstruction of the original sector-specific SOURCE payload. Known zeros are fixed inputs; this does not prove the Riemann hypothesis.

### WRRA-specific transformation

Chapter 75 already uses a real cosine sum with four zero heights and log n+xi k for SOURCE admission. The logarithmic-address/zero-phase connection therefore exists in the earlier book. This addition connects it to conservative superposition of 70 complex phases and prime-space output. It neither replaces the four-mode/eight-frame admission formula nor reinterprets its composition fractions as the new port probabilities.

#### 131.1 A connection without arbitrary zero-to-eigenmode numbering

The termwise identity

$$
n^{-\rho_j}=n^{-1/2}\exp(-i\gamma_j\log n)
$$

directly provides an address-phase operator:

$$
D_j|n\rangle=e^{-i\gamma_j\log n}|n\rangle,
\qquad |\phi_j\rangle=UJ D_j|\psi\rangle.
$$

J is Chapter 130's CRT embedding and $U=\exp(-iL)$ is dimensionless test propagation under the existing prime Laplacian. Its parameter 1 is not seconds or shutter time, nor is L identified with the physical photon Hamiltonian $H=\hbar c|k|$. The zero-associated spatial wave packets $\phi_j$ are generally nonorthogonal and are not individual eigenmodes of L. No arbitrary matching of zero indices to spatial eigenmode indices is required.

This test separates the common magnitude $n^{-1/2}$ from zero phases and uses only the phase in the transformation. Choosing that magnitude for preparation would instead specify a separate alpha=1 input. The termwise identity does not assert convergence of the infinite Dirichlet series on the critical line, or equality of its finite truncation to analytically continued zeta.

#### 131.2 Conserving output and hold during superposition

Equal-amplitude, common-relative-phase combination of 70 zero branches is an explicitly added construction assumption. With C=70,

$$
K(n)=\frac1C\sum_{j=1}^{C}e^{-i\gamma_j\log n},
$$
$$
|\Psi_{\rm out}\rangle=UJK|\psi\rangle=\frac1C\sum_j|\phi_j\rangle,
\quad |\Psi_{\rm hold}\rangle=\sqrt{1-|K|^2}|\psi\rangle.
$$

Since |K|<=1, output and hold squared norms sum to the input squared norm. Prepare a uniform auxiliary register, apply controlled D_j and select the uniform combining port to implement K. Complementary ports carry the total held probability. The displayed hold is a minimal probability-preserving instrument, not a reconstruction of all complementary microscopic port states.

Spatial intensity is $I(x)=|\Psi_{\rm out}(x)|^2$. Record $P_{\rm out}=\sum_xI(x)$ before normalizing the conditional distribution I/P_out. The incoherent comparator is $C^{-1}\sum_j|\phi_j(x)|^2$ and omits cross terms. Individual zeta permission remains an upstream requirement: this experiment receives permitted zeros as inputs. It does not rerun the earlier R3 readout, but checks the zeta residuals of the zeros separately.

### Outputs

| Output | Uniform preparation | Inherited-alpha preparation |
|---|---:|---:|
| Selected coherent-port probability | 0.014262842604 | 0.004494840216 |
| Hold probability | 0.985737157396 | 0.995505159784 |
| Output-plus-hold norm error | 0 | $4.22\times10^{-15}$ |
| Conditional TV distance from incoherent mixture | 0.3741526991 | 0.5780259658 |
| TV from same-zero random-relative-phase control | 0.5484761134 | 0.7167374941 |
| TV from equally spaced height control | 0.6511396103 | 0.8812653410 |

$\mathrm{TV}(p,q)=\tfrac12\sum_x|p(x)-q(x)|$ is zero for identical distributions and one for disjoint support. Port probability is not a cosmic-composition or matter fraction. This shape calculation remains separate from composition research.

At 35-digit precision the largest zeta residual of the 70 inputs was $3.90\times10^{-34}$. Subsequent phase and spatial computations use double precision. Maximum spatial synthesis error was $3.11\times10^{-17}$ and inverse error $3.47\times10^{-18}$. Fifteen checks passed, including two diagnostics for visible interference under these preparations; they are not fifteen independent physical validations.

A common height shift delta=0.5 obeys $K_\delta(n)=e^{-i\delta\log n}K(n)$. It preserves intensity before propagation and total output probability but can change the propagated spatial distribution. Measured conditional TV differences were 0.2033147865 and 0.0295680194. Permuting zero order changed no result. Equally spaced and shifted-height controls force permission open to compare shapes only; they are not claimed to pass zeta permission.

### Falsification conditions

Address collisions, phase-rule violations, output/hold probability loss, failed linear synthesis or inverse transformation require correction. Failure to reproduce the declared phase-change and incoherent-control results for fixed inputs also revises this connection. Other height sets can generate patterns; interference alone does not establish physical uniqueness of zeta zeros.

### Assessment and remaining connections

**A computed example now connects folding selection, zero-derived phase superposition shaping a spatial distribution, and the existing prime operators supplying the unfolding geometry.** Output depends jointly on the zero list, input state, relative phases and propagation. Physical preparation of equal zero weights and relative phases, single-result selection through existing shutters and stable records, and unique selection of three dimensions are not derived here.

The source `WRRA_Zeta_Mode_Superposition_v0_1_2026-10-16.zip` contains code, zero heights, marginal-probability CSVs and results JSON. The existing GR/CMB pipeline has not been rerun with this superposed field.

