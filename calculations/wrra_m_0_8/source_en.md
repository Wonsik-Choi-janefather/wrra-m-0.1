# WRRA M 0 8 Calibrated Particle Filter Selection in the Shared Actual Ledger

Common carrier responses with executed placement and charge calculation

Wonsik Choi

WRRA-M 0.8 | 2026-10-01

Independent Researcher Seoul Republic of Korea

ORCID 0009-0001-4263-9772 | janefather@gmail.com

## Evaluation order and completed result

Verification inputs are WRRA Core 1.0, MCC 2.3.2, the representation, charge and selection calculations of 0.1 to 0.4, and the shared 0.7 ledger. Known particle assignments and three generations are adopted calibration material. Response offsets and the origin orientation table are disclosed constitutive choices.

The WRRA-specific transformation computes responses from the same carrier state, evaluates all four filters with one positive-distance rule, and generates placement and charges from the selected permutation. Outputs are selection of F_DX, the sixteen-channel charge table, and replication into 45 Standard-Model chiral components plus three conditional neutral slots. The same input also enters the inherited energy, pressure, gravity and expansion ledger.

Failure conditions are a tie or incompatible assignment under fixed calibration, loss of transport rank or positivity, disagreement in charges, anomalies or energy accounting, and undisclosed input changes. Twenty-two check groups pass. Completion means executed calibrated selection of the adopted our-universe assignment within the declared four-filter family. Calibration is legitimate model construction; independent prediction is not a completion requirement.


## The inherited tie and this release input ledger

Two complexified seven sectors and an invariant channel from 0.1 give fifteen color components. Versions 0.2 to 0.4 add the transported neutral channel 1_N. Independent complex left-handed Weyl fields are a physical assumption. Interpreting 1_N as the conjugate right-handed neutrino is a constitutive assumption of this branch; this calculation does not measure its particle existence, mass or occupation.


$$
\mathcal C_{16}=\mathbf1_0\oplus\mathbf7_A\oplus\mathbf7_B\oplus\mathbf1_N,\quad \mathbf7\downarrow SU(3)=\mathbf3\oplus\overline{\mathbf3}\oplus\mathbf1. \tag{1}
$$
The simplest homogeneous carrier in 0.5 gave the same scalar response to every origin. Its transport rank was sixteen, yet both selection gaps were zero. Version 0.8 retains the common periodic lattice Kc and adds origin-specific scalar offsets to the readout operator. These calibrate distinguishable responses while retaining the same highest-order transport matrix.


$$
K_c=2I-T-T^\dagger,\quad K_i^{\mathrm{read}}=K_c+\mu_i I. \tag{2}
$$
Calibration uses mu0=1, kappa=0.25, Qnu=0, Qe=-1, YN=0 and Y0=1. Both contrasts are 0.25 and offsets are 0.75 or 1.25. Signs in the orientation table are calibration inputs preserving the 0.2 particle-origin assignment. Neither the output name F_DX nor a positive gap is inserted as a score. The calibrated orientation does use known assignments, so its microscopic origin is not newly derived.


$$
\mu_i=\mu_0+s_i\delta_{L,R},\quad \delta_L=\kappa(Q_\nu-Q_e),\quad\delta_R=\kappa(Y_0-Y_N). \tag{3}
$$
Offsets are dimensionless auxiliary readout calibration. They add neither a new particle mass nor a separate energy sector, and do not replace the inherited state-evolution Hamiltonian. Equal responses within each color triplet preserve the color action. Component-dependent readout is a fixed weak-basis background, not an unbroken SU(2)-invariant Hamiltonian. Joint background and basis covariance is checked; Higgs or symmetry-breaking dynamics are not newly calculated here.


## Responses and selection computed from one carrier

The grid N=128 and internal state rho are shared with 0.7. Probes use inherited squared frequencies 0.1, 0.5, 1, 2 and 3.5 with damping gamma=0.2. The response averages positive resolvent intensities in that same state. Iref is the common normalization computed at zero offset in that state; individual channel normalization does not erase their differences.


$$
I_i(\rho)=\frac1M\sum_{j=1}^{M}\mathrm{Tr}\!\left[\rho\left((K_c+\mu_i I-w_jI)^2+\gamma^2I\right)^{-1}\right]. \tag{4}
$$

$$
u_i=\sqrt{I_i/I_{\mathrm{ref}}},\quad I_{\mathrm{ref}}=I_{\mu=0}(\rho),\quad c(i,j)=-(u_i-u_j)^2. \tag{5}
$$

| Origin | Sign | Offset | Response u |
| --- | --- | --- | --- |
| 3_A | 1 | 1.25 | 0.672634137 |
| 3_B | -1 | 0.75 | 0.825428002 |
| 1_A | 1 | 1.25 | 0.672634137 |
| 1_B | -1 | 0.75 | 0.825428002 |
| anti3_A | -1 | 0.75 | 0.825428002 |
| anti3_B | 1 | 1.25 | 0.672634137 |
| 1_N | -1 | 0.75 | 0.825428002 |
| 1_0 | 1 | 1.25 | 0.672634137 |

Direct distance differences agree with the alignment identities of 0.4. Scores are evaluated by the 0.3 code in the order F_DX, F_XX, F_DD and F_XD. Adoption checks a unique maximum, positive selection rate and nonzero initial support for that maximum.


$$
\Delta_L=2(u_{3_A}-u_{3_B})(u_{1_A}-u_{1_B}),\quad\Delta_R=2(u_{\bar3_A}-u_{\bar3_B})(u_{1_N}-u_{1_0}). \tag{6}
$$

$$
C=(C_{DX},\ C_{DX}-\Delta_L,\ C_{DX}-\Delta_R,\ C_{DX}-\Delta_L-\Delta_R). \tag{7}
$$
At the uniform reference both gaps are 0.04669193039. Scores are 0, -0.04669193039, -0.04669193039 and -0.09338386078. F_DX is the unique maximum. These are computed carrier responses rather than a copied gap-eight witness from 0.4.


| State | Gap L | Gap R | Selected |
| --- | --- | --- | --- |
| Uniform a 0.5 | 0.046691930 | 0.046691930 | F_DX |
| Uniform a 1 | 0.046691930 | 0.046691930 | F_DX |
| Uniform a 2 | 0.046691930 | 0.046691930 | F_DX |
| Low mode | 0.302255406 | 0.302255406 | F_DX |
| High mode | 0.024286779 | 0.024286779 | F_DX |
| Zero mode | 0.079817893 | 0.079817893 | F_DX |
| Coherent packet | 0.150301512 | 0.150301512 | F_DX |
| Uniform noncommuting | 0.046691930 | 0.046691930 | F_DX |
| Packet noncommuting | 0.150301512 | 0.150301512 | F_DX |

Table states are fixed structural test inputs, not new observations of the present universe. Selection and rank are also checked at N=32, 64, 128 and 256. The same N input controls both information loads and filter responses. Numerical values are reproduced in the JSON and CSV outputs.


## Executed selection flow and controls


$$
p_f(\tau)=\frac{p_f(0)e^{\eta C_f\tau}}{\sum_g p_g(0)e^{\eta C_g\tau}},\quad\dot p_f=\eta p_f(C_f-\overline C). \tag{8}
$$

$$
\tau\geq\frac{\log((1-p_*(0))/(p_*(0)\varepsilon))}{\eta\Delta_{\min}}\quad\Longrightarrow\quad 1-p_*(\tau)\leq\varepsilon. \tag{9}
$$
Initial weights are one quarter each, eta=1 and the residual target is 10^-8. The sufficient construction time at the reference is about 418.04425027, with final F_DX weight 0.999999993333 and residual about 6.666667 times 10^-9. Independent integration of the selection differential equation differs from the closed form by at most 2.362 times 10^-14.

These are candidate weights in a model-construction optimizer. They are not particle Born probabilities, physical time or observation records. Finite-time weight is not asserted to equal exactly one; adopted placement follows the checked unique-maximum selection rule.

At kappa=0 all four candidates tie. Fixed reference calibrations kappa=0.1, 0.25 and 0.5 select F_DX. Reversing left or right singlet orientation selects F_XX or F_DD; reversing both selects F_XD. A global sign-convention reversal preserves gaps and F_DX. Some assignments can represent the same particle content after origin relabeling. This is therefore selection in a fixed calibrated origin convention, not proof that every candidate defines a different observed universe.


## Placement and charges generated from the selected permutation

The selected filter is implemented as a sixteen-by-sixteen permutation. Triplets A and B form upper and lower Q_L components; singlets A and B form upper and lower L_L components. Antitriplet A pairs with neutral N and antitriplet B with invariant 0. No input channel is discarded. Matrix checks verify color intertwining.


$$
P_{DX}^\dagger P_{DX}=I_{16},\quad\rho_{\mathrm{ch}}^{\prime}=P_{DX}\rho_{\mathrm{ch}}P_{DX}^\dagger. \tag{10}
$$
Color tracelessness and lepton B-L normalization generate the quark B-L values. On the selected placement, rational arithmetic solves one hypercharge operator satisfying Y(1_N)=0 and Y(1_0)=1, then applies it to every channel. Superscript c denotes a charge-conjugate left-handed field; u_c and d_c therefore have charges opposite to physical right-handed quarks.


$$
3b_q+b_\ell=0,\quad b_\ell=-1,\quad b_q=\frac13;\qquad \overline b_q=-\frac13,\quad\overline b_\ell=1. \tag{11}
$$

$$
Y=\alpha T_{3R}+\beta(B-L),\quad -\alpha/2+\beta=0,\quad\alpha/2+\beta=1\quad\Longrightarrow\quad(\alpha,\beta)=(1,1/2). \tag{12}
$$

$$
Q=T_{3L}+Y. \tag{13}
$$

| Group | Count | Y | Charge Q | Origin |
| --- | --- | --- | --- | --- |
| Q_L | 6 | 1/6 | 2/3, -1/3 | 3_A and 3_B |
| L_L | 2 | -1/2 | 0, -1 | 1_A and 1_B |
| u_c | 3 | -2/3 | -2/3 | anti3_A |
| d_c | 3 | 1/3 | 1/3 | anti3_B |
| nu_c | 1 | 0 | 0 | 1_N |
| e_c | 1 | 1 | 1 | 1_0 |

Calculated SU(3)^3, SU(3)^2 U(1), SU(2)L^2 U(1), U(1)^3 and mixed gravitational-U(1) anomaly sums vanish exactly. Left and right SU(2) sectors each contain four doublets. The gravitational anomaly is a representation-consistency check, separate from spacetime gravity calculation. Weak-generator commutators and B-L compatibility also pass.


## Connection to the shared Actual ledger and three generations

The filter permutes channel placement while 0.7 energy operators act commonly on channels. Phenotype, clustering-hidden and background-hidden energy budgets are therefore preserved by this reorganization. Nonuniform and entangled channel tests preserve the same loads. This check is distinct from energy transfer in a physical quantization event.


$$
\widetilde A_s=I_{16}\otimes A_s^{(0.7)},\quad\mathrm{Tr}(\rho^{\prime}\widetilde A_s)=\mathrm{Tr}(\rho\widetilde A_s). \tag{14}
$$
All nine physical ledgers match the 0.7 originals. The reference retains phenotype 4.93%, hidden share 95.07%, q=-0.52855, test rotation 207.510905 km/s and conditional lens deflection 0.535586511 arcsec. The selection calculation does not refit these outputs. The five-percent allocation, sixteen-channel state weights and four-filter optimizer weights are distinct accounts.


$$
\mathcal C_{48}=\mathbb C^3\otimes\mathcal C_{16},\quad G_{48}=I_3\otimes G_{16},\quad \mathrm{Tr}\rho_{\mathrm{fam}}=1. \tag{15}
$$
Three generations are adopted from known particle information as the configured replication count. The same channel rule generates charges for u,d / c,s / t,b, e,mu,tau and the three active neutrino families. Particle_inventory.csv records all 48 components: 45 Standard-Model chiral components and three conditional neutral extension slots N1_c,N2_c,N3_c. Transport rank 48 is computed from the actual matrix. Normalized family state avoids multiplying the original energy budget by three.

Family count is calibration input and family replication is an executed transformation. Masses, mixing, Yukawa structure and interaction dynamics are not newly derived by this inventory. Version 0.9 attaches physical quantization outcomes, probabilities, post-observation states and records to the selected placement.


## Verification and reproduction


| No | Check | Result |
| --- | --- | --- |
| 1 | Inherited exact checks 0.1 to 0.4 | Pass |
| 2 | Color inventory and neutral extension | Pass |
| 3 | Independent periodic spectrum | Pass |
| 4 | Direct complex resolvent | Pass |
| 5 | Zero calibration and homogeneous tie | Pass |
| 6 | Four filter costs and gap identities | Pass |
| 7 | Selection in nine cases | Pass |
| 8 | Positive full rank transport | Pass |
| 9 | Bijective color preserving filter | Pass |
| 10 | One hypercharge and exact anomalies | Pass |
| 11 | Three calibrated generations | Pass |
| 12 | Weak representation algebra | Pass |
| 13 | Same nine physical ledgers | Pass |
| 14 | Nonuniform channel energy accounting | Pass |
| 15 | Entangled channel load accounting | Pass |
| 16 | Shared grid input | Pass |
| 17 | Contrast sensitivity | Pass |
| 18 | Orientation and convention controls | Pass |
| 19 | Joint background and basis covariance | Pass |
| 20 | Flow equation and zero support | Pass |
| 21 | Invalid calibrations and records | Pass |
| 22 | Hash and explicit recalibration | Pass |

Checks include inherited exact code, independent periodic spectra, direct complex matrix inverses, selection-ODE integration, representations and anomalies, grid changes, reversed calibration, zero initial support and twelve invalid inputs. Failure to retain positive response, full rank, selection gaps or consistent placement charges and accounting requires revision of that configuration.

From the archive root run python calculations/wrra_m_0_8/run_release.py. Parameters.json is the sole configuration input and embeds the 0.7 ledger. Outputs record both input hashes. Canonical SHA256 of the full 0.8 input is 8403336558879543b0784d6f5e009c02429107c65cfe3c09a93d4126a256af3c. A clean-copy reproduction check removes captured numerical outputs before execution, and the archive includes a file SHA256 manifest.

Computation requires numpy and scipy. Write_papers.py generates manuscripts; build_reports.py uses pandoc and python-docx for Word. PDF is rendered with LibreOffice, and document checks additionally use pypdf. Random-state tests use seed 808. Results separate constitutive choices, calibrations, internal outputs and subsequent work. This development version is published on GitHub.


## References

Choi Wonsik. WRRA-M 0.1 to 0.7. GitHub research repository. https://github.com/Wonsik-Choi-janefather/wrra-m-0.1

Choi Wonsik. WRRA-M 0.6-r2 frozen archive. https://doi.org/10.5281/zenodo.23076547

Choi Wonsik. Minimal Computation Cosmology 2.3.2. Chapter 11 The Common Carrier and Fifteen Channels. Adopted constraints on a common carrier. https://github.com/Wonsik-Choi-janefather/minimal-computing-cosmology-2.3.2

Particle Data Group. Grand Unified Theories. 2025 update, sections 92.1 and 92.2.1. The convention here rescales PDG hypercharge by one half, giving Q=T3+Y. Standard-Model representations and the Pati Salam charge relation are external verification inputs. https://pdg.lbl.gov/2025/reviews/rpp2025-rev-guts.pdf

Copyright 2026 Wonsik Choi. CC BY 4.0. https://creativecommons.org/licenses/by/4.0/
