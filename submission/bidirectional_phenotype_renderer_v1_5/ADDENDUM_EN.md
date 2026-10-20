## Two-resolution rendering and measurement: conditional compatibility audit

### Verified inputs and engineering criterion

WRRA uses engineering reverse design: observed constants and physical structures are legitimate construction inputs. A mismatch is a reason to revise the interpreter or its interface. Reproducing known phenomena counts as compatibility and explanatory achievement. An independent prediction is an additional achievement, not a prerequisite for that status. A quantity calculated for an unmeasured regime after the model inputs and rules have been fixed is identified separately as a prediction. No such new empirical prediction is claimed by the present finite audit.

The adopted shutter proper period remains $\Delta\tau_{\rm sh}=1.4813019664158633\times10^{-21}$ s. With $c=299792458$ m/s its transport scale is $L_{\rm sh}=c\Delta\tau_{\rm sh}=4.440831575520451\times10^{-13}$ m, approximately 0.444083 pm. This revision adds a conditional internal lower interval for successive registered updates on the same local apparatus worldline: $\Delta\tau_{\rm obs}\ge t_P$. Its associated local internal length scale is $\ell_P=ct_P$. The Planck floor is an assumption, not a measured minimum duration or resolution.

Using the 2022 CODATA inputs $h$, $G$ and $c$ gives $t_P=\sqrt{\hbar G/c^5}\simeq5.39124645\times10^{-44}$ s and $\ell_P\simeq1.61625502\times10^{-35}$ m. These scales inherit the uncertainty of $G$; extra displayed digits in the JSON serve reproducibility. The ratio $\Delta\tau_{\rm sh}/t_P\simeq2.74760574\times10^{22}$ is not assumed to be an exact integer. No such number of internal updates was simulated. Importing $G$ does not derive gravity from WRRA.

Complex joint density states, unitary evolution, Born probabilities and projective measurement instruments are explicitly adopted as observed-structure interpreter rules. They have not been generated from the integer code by this audit. Their adoption is legitimate reverse engineering; the new contribution tested here is their connection to the two local update schedules.

### WRRA transformation and corrected operating rules

**A. Periodic representation and microscopic evolution.** The shutter specifies periodic phenotype output on a local source worldline. $L_{\rm sh}$ remains its representation scale, but is not a universal Cartesian lattice, a deletion threshold for shorter states, or a period during which all microscopic physics stops. Microscopic phase, joint correlations and permitted interactions persist between shutter opportunities. Macroscopic representation concerns stable apparatus and environment records. It neither copies an arbitrary unknown quantum state nor measures the whole universe on every shutter.

**B. Measurement-triggered conditional records.** The measurement permission gate $Q_{\rm obs}$ depends on physical apparatus/environment coupling and record formation, not human attention or consciousness. Premeasurement information owns phase and joint correlations; increasing resolution alone does not determine an outcome. For a prepared state $\rho$ and an allowed instrument $M_a$, use

$$p(a)=\operatorname{Tr}(M_a\rho M_a^\dagger),\qquad
\rho_a=\frac{M_a\rho M_a^\dagger}{p(a)},\qquad
\sum_aM_a^\dagger M_a=I.$$

An established record $a$ is definite for that measurement. Incompatible observables need not all become definite. Unobserved environmental correlations remain part of the inclusive description. This is an adopted operational record rule, not a new solution of every interpretation of measurement.

**C. Conditional Planck floor.** Successive registered updates on one apparatus worldline obey the assumed local proper-time threshold. $\ell_P$ specifies a conditional internal refinement limit in that apparatus's local rest frame. It does not promise that every detector resolves $\ell_P$, that every measurement completes in $t_P$, or that position and momentum can both be measured arbitrarily precisely. The two schedules are not synchronized across the universe, and no exact integer Planck lattice is imposed. The scales alone supply neither microscopic dynamics nor a computational resource budget.

**D. Relativistic connection.** Apply time thresholds to local massive apparatus proper time; do not apply them to arbitrary coordinate gaps between different apparatuses or to a photon's zero proper time. Spacelike-separated measurements have no mandatory common execution order. Their allowed local operations must commute in the implemented model, and joint statistics must be order independent. A conditional change in the description after learning a remote outcome is distinct from physically transmitting that outcome. Changing a remote setting may not alter the other party's nonselective outcome statistics. Preserve entangled joint states rather than replacing them with independent local outcome assignments. Tensor-factor commutativity is supplied in this finite model; interacting-field microcausality has not been derived.

**E. Production and measurement permissions.** Measurement registration does not advance the matter/antimatter shutter phase or create a new particle by observation alone. Equal-only splitting/recombination, next-shutter conjugate reservation, and source ownership of pending charge and four-momentum retain their previous scope. Apparatus and environment must own measurement energy and momentum exchanges. A degenerate-pointer, energy-preserving $Z$-QND instrument is implemented as one example. A general apparatus energy/momentum theory is not claimed.

### Rejected interpretations and repairs

1. Treating all premeasurement states as independent classical local numbers does not secure Bell correlations. The 16 deterministic local assignments in the audit have CHSH bound 2. An entangled singlet and the adopted joint measurement rule give $2\sqrt2$. The repair retains joint correlations without a controllable superluminal signal. This does not exclude every possible deterministic interpretation.
2. Automatically erasing path phase at a shutter destroys interference. The repair makes periodic macroscopic representation distinct from an unperformed which-path measurement. Actual which-path records require their physical coupling.
3. A literal uniform sampling grid of spacing $L_{\rm sh}$ with hard cutoff $k_{\max}=\pi/L_{\rm sh}$ would cap a represented photon's energy at approximately 1.395957 MeV. This calculated warning is conditional on that extra hard-grid interpretation; it is not a WRRA prediction. The repair permits shorter microscopic states and treats the shutter scale as representation scope.
4. A common simultaneous global update or identical Cartesian minimum grid in every inertial frame conflicts with the ordinary transformation of coordinates and spacelike event order. The repair uses local proper-time thresholds and local rest-frame scales without privileged global simultaneity. This does not prove covariance of an arbitrary minimum-length dynamics.
5. Definite records do not remove all quantum uncertainty. The repair retains incompatible-observable dispersions and does not equate internal refinement with unlimited experimental precision.

### Outputs: executed finite checks

Run `python3 audit.py` with Python 3 and NumPy. The fixed seed is 20261020; `results.json` records the input values, counts, numerical errors, negative controls and limits.

| Check | Executed output |
|---|---|
| Interference, 361 phases | $p_0=(1+\cos\phi)/2$; maximum error $5.55\times10^{-16}$; visibility 1 |
| Premature-dephasing control | Visibility approximately $1.11\times10^{-16}$ |
| Singlet CHSH | 2.82842712474619; local deterministic bound 2 over 16 assignments |
| Nonselective local instruments | 1,000 channels over 200 random mixed joint states; remote reduced-state change at most $2.22\times10^{-16}$ |
| Spacelike tensor-factor order | 4,000 unnormalized branch comparisons; difference at most $1.11\times10^{-16}$ |
| Probability normalization | Maximum error $3.33\times10^{-16}$ |
| Repeated same-observable record | Maximum error $2.22\times10^{-16}$ |
| Pauli dispersion bound | No violation of $(1-\langle X\rangle^2)(1-\langle Y\rangle^2)\ge\langle Z\rangle^2$ in the tested states |
| Local proper intervals | 101 boosts, 202 interval comparisons; maximum relative error $9.88\times10^{-15}$ |
| Conserving measurement example | Unitarity and total-energy commutator errors 0 for the declared QND example |
| Local scheduler | Four inter-shutter registrations leave the alternating shutter schedule unchanged |

The tests deliberately detect failed fringe visibility after premature dephasing, failure of independent local assignments to reach the singlet CHSH value, and noninvariance of an absolute spacelike order. Rejection of a $t_P/2$ interval checks enforcement of the assumed threshold, not its physical truth. The quantum checks are algebraic compatibility tests using adopted rules, not new experiments or a fit to raw experimental Bell data. They do not discriminate a Planck floor from other sufficiently short candidate floors. They are recorded separately from the retained 630-case audit and the book's earlier 288-case reverse-interpreter audit.

### Falsification conditions and remaining scope

Revise a connection if it produces negative or unnormalized probabilities; erases interference without a physical record; fails observed correlations; lets a remote setting alter local nonselective statistics; makes spacelike joint statistics depend on coordinate ordering; or violates inclusive apparatus/environment conservation. An empirical test of the internal time floor additionally requires a physical identification of the same apparatus's successive processing events and a measurable consequence. A chosen numerical scheduling threshold alone is not that test.

No dynamical curved metric, Einstein equation, quantum gravity calculation, general continuous interacting field, or integer-to-complex-amplitude generator is newly executed. Special-relativistic event kinematics and finite commuting instruments do not establish compatibility with every possible gravitational setting. The two-resolution construction passes its stated finite checks after the repairs above. This is a reverse-engineered compatibility result, while the Planck lower scale remains conditional.

### Sources and reproducibility

- NIST, 2022 CODATA complete listing: <https://physics.nist.gov/cuu/Constants/Table/allascii.txt>.
- Hensen et al., experimental Bell-correlation benchmark: <https://arxiv.org/abs/1508.05949>. The ideal singlet calculation here is separate from those experimental data.
- Fedida, relativistic measurement consistency and its additional assumptions: <https://arxiv.org/abs/2506.14693>. The present tensor-factor example is not a reimplementation of the complete field-theoretic result.
- Source, figures, code and results: <https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/main/submission/bidirectional_phenotype_renderer_v1_5>.
- Related integrated book, v0.25-r4: <https://zenodo.org/records/23486923>. This standalone v1.5 release adds the present result without declaring that the book's released PDF has already been revised.
