## 136. From Residue Seeds to Finite Emission, Thermal History and Observational Calculation

### 136.1 Verified inputs and ownership of versions

This chapter preserves Chapters 1–135 and the artistic opening of v0.25-r5 and adds the residue/CMB studies v0.4, v0.5, v0.6 and v0.7-dev-r1 published on 20 October 2026. Book revision v0.26 and individual calculation versions are different numbering systems. This is an integration of executed source records; editing the book is not counted as a new physical run or empirical confirmation.

Verified inputs are the original quantized 128-cell seed, 64 evolved physical modes, calibrated background and proper-time unit, observed constants and electron/positron EOS, and released SPT–Planck lensing bandpowers, covariance and windows. Ownership of numerical results remains with the source studies and their GitHub paths below. Adopting verified constants and observations, and revising a model accordingly, is legitimate construction and calibration.

| Calculation source | Executed WRRA connection | Source check record | Present scope |
|---|---|---|---|
| v0.4 | Finite-k conversion, metric, momentum, free-streaming neutrinos and conserving same-content matching | 643 | Linear amplitude, 64 modes; not production CAMB full-state injection |
| v0.5 | Finite-packet event timing, record permission, heat cost and local expansion | 444 plus 12 release checks | Independent local FLRW cells; not finite-k event evolution |
| v0.6 | Conditional nonlinear lensing/likelihood for a WRRA background and separate MeV thermal history | 54 plus 8 release checks | Declared calibrated primordial completion and thermal calculation |
| v0.7-dev-r1 | 64-mode frame adapter, event-time tangent, thermal density calibration and stable metric combination | 472 plus 10 release checks | Partial full-state junction development |

These counts are numerical conservation, normalization, convergence and control checks, not independent observations. Reruns do not become new cosmic measurements. Earlier actual-SOURCE CMB branch outputs are retained and are not replaced by the conditional v0.6 branch in this chapter.

### 136.2 WRRA-specific transformation: finite gradients and conserving matching

Version 0.4 carries seed modulation of the conversion rate from an effective relativistic reservoir into a dust-like matter component. It evolves synchronous metric variables, species densities and momenta, and a massless free-streaming neutrino hierarchy together. The 64 physical modes are $k=0.05,0.10,\ldots,3.20\ {\rm Mpc}^{-1}$, with stored moments $F_{\nu0}$ through $F_{\nu12}$. Spatial gradients are retained while perturbation amplitudes remain linear.

The exchange law requires total stress-energy conservation:

$$\nabla_\mu T_A^{\mu\nu}=Q_A^\nu,\qquad \sum_A Q_A^\nu=0.$$

The calculation does not discard metric and momentum in favor of one entropy value. Merging the remaining effective perfect radiation into photon-like perfect radiation transports both its density and momentum and retains the neutrino hierarchy. Continued evolution is explicitly compared in the same-content system. This is a finite-gradient advance beyond a two-moment fluid substitute. It does not automatically generate physical species-production rates, baryon/photon tight coupling or a massive-neutrino phase-space distribution.

### 136.3 Finite emission times and recording cost

Version 0.5 partitions a reference cell's convertible radiation budget into 256 packets. Emission occurs when accumulated transfer credit reaches the packet threshold and record permission is available. Credit is not a second energy reservoir. Gate closure pauses credit production; there is no forced flush at pulse closure. The reference run emits 128 events.

$$\dot r=\Gamma(1+\xi)C,\qquad r=q\ \hbox{and recording permission}\ \Longrightarrow\ \hbox{emission}.$$

$$C^+=C^--q,\qquad M^+=M^-+\frac{(1-\epsilon)q}{a_j},\qquad J^+=J^-+\epsilon q.$$

Here $q$ is a reference-cell comoving radiation-energy debit and $\epsilon=0.01$ is a declared recording heat cost. The packet is not identified with a universal particle rest energy or a new fundamental quantum. The different dilution laws of $C,M,J$ make the factor $a_j$ essential for conservation. In the thermal completion the heat changes the actual electromagnetic temperature through the finite-electron heat capacity, rather than being replaced by a perfect-radiation constant.

The first and last events occur at approximately 0.00268883 s and 0.475779 s. The inherited 0.47712081326446576 s unit is a calibrated early-universe proper-time unit, not the book's microscopic shutter time. At fixed packet number the small-seed response depends on the order of the small-seed and continuum limits. The smooth-source response is therefore not copied into the finite-event model.

### 136.4 Executed likelihood and MeV thermal outputs

The v0.6 observational branch uses the inherited WRRA dark-weight-only background $H_0=67.2568374662005$, $\omega_b=0.022395806792949086$, $\omega_c=0.12037806177378184$. It declares the calibrated standard adiabatic primordial completion $A_s=2.1\times10^{-9}$, $n_s=0.9649$, with inputs $\tau=0.0544$, $N_{\rm eff}=3.044$, $T_{\rm CMB}=2.7255$ K. CAMB 2.0.4 and the adopted HMCode 2020 prescription provide nonlinear lensing. The likelihood uses the released 18-bin SPT–Planck full covariance, windows and TT/PP response corrections.

$$b=(W+R_{PP})D^{\phi\phi}+R_{TT}D^{TT}-f,\qquad
\chi^2=(b-d)^T\Sigma^{-1}(b-d).$$

| Declared comparison | Fixed-model $\chi^2$, 18 bins |
|---|---:|
| Linear lensing | 11.6855836908 |
| Adopted nonlinear lensing | 10.6060135496 |
| Accuracy-refined nonlinear lensing | 10.6032279730 |

The native likelihood agrees with a separate official CosmoMC implementation within $1.60\times10^{-14}$. The covariance distance under refinement is approximately 0.00383078 sigma. These are conditional comparisons of a WRRA background and a declared primordial preparation. They do not inject the complete v0.4 state or v0.5 event perturbations into CAMB. Reproduction and explanation using verified preparation inputs are achievements, while connections not executed are not called integrated. HMCode is an adopted empirical prescription, not a newly derived WRRA nonlinear law. A likelihood tail probability is not the probability that a theory is true.

The separate finite-event thermal history uses finite-mass equilibrium electrons/positrons and a declared instantaneous relativistic-neutrino-decoupling branch. Retaining the inherited clock gives initial photon temperature 1.7584850895 MeV and present-photon-entropy-connected initial scale $a_i=9.55163454815\times10^{-11}$, about 4.48% below the earlier $10^{-10}$. One cannot add this thermal content while keeping the old clock, scale and species content all unchanged.

| Photon temperature | Elapsed time after pulse start |
|---|---:|
| 1 MeV | 0.5045894421 s |
| 0.5 MeV | 2.8257151242 s |
| 0.1 MeV | 118.6213275533 s |

These are not absolute cosmic ages. $N_{\rm eff}$ is an input. Collision integrals, flavor transport, weak freezeout and BBN element yields are not computed. Standard cosmology supplies verification and reinforcement; only connections actually calculated within the resulting WRRA model count as executed integration.

### 136.5 Full-state junction development and numerical correction

Version 0.7-dev-r1 transforms all available scalar variables of the 64 v0.4 modes into the post-exchange CDM-comoving synchronous frame. It does not simply set velocity to zero: densities, metric derivatives and the neutrino monopole/dipole transform together.

$$\alpha=\frac{\theta_m}{k^2},\quad
\theta_i^c=\theta_i-k^2\alpha,\quad
\delta_i^c=\delta_i+3(1+w_i){\cal H}\alpha,\quad
\eta^c=\eta+{\cal H}\alpha.$$

Maximum normalized Hamiltonian and momentum residuals after transformation are $3.29\times10^{-16}$ and $4.31\times10^{-16}$. However, reconstructing a small combination from separately rounded large derivatives produces up to approximately 16.66% relative Bardeen-potential error at low k. Revision r1 retains that combination directly from the inherited scaled shear $g$ and gauge shift:

$$h^{c\prime}+6\eta^{c\prime}=2k^2(g/2+\alpha).$$

With this stable combination, Bardeen-potential gauge invariance agrees within relative $4.35\times10^{-12}$ over all 64 modes. Naive subtraction is retained as a negative control. Separate derivatives are rounded diagnostics; any future actual CAMB transport must also verify stable constraint evaluation.

Separately, the local-cell v0.5/v0.6 model includes the derivative of event time. Its common-time tangent $z=\partial y/\partial\xi$ changes across event reset $R$ according to

$$z^+=DR\,z^-+(DR\,f^--f^+)t_j',\qquad t_j'=-\frac{t_j}{1+\xi}.$$

The finite-event thermal $k=0$ entropy response is 0.194818034056, differing from the smooth-source 0.723567385056. Applying the unchanged seed without amplitude refitting gives entropy RMS $4.80262944810\times10^{-9}$. An independent clock $u=(1+\xi)t$ keeps events fixed and reproduces the response within relative $8.39\times10^{-9}$. This local tangent is not substituted for a finite-k full state.

The old conversion budget gives thermally normalized dark matter $\omega_c=0.103663511129$, approximately 13.885% below the downstream target. Recalibrating this branch's conversion fraction $\beta$ from $7.62452468358\times10^{-7}$ to $8.85389093544\times10^{-7}$ reproduces the inherited target. This is legitimate background calibration. This $\beta$ is an early convertible-radiation fraction, not the book's cosmic composition or identically written symbols in other chapters. The 64 finite-k modes have not been rerun on that calibrated background. Earlier composition, shutter, galaxy and GR/CMB branch values are not retroactively changed.

### 136.6 Falsification conditions and the exact remaining junction

Failure or revision conditions are violated total conservation or Einstein constraints; inconsistent gauge invariants or neutrino normalization; omitted event-time motion, recipient momentum or recording heat; failed EOS, time or hierarchy convergence; incorrect covariance, windows or likelihood normalization; and disagreement with the declared observational comparison. Inputs and preparations remain disclosed, and WRRA and established models receive the same evidentiary standard.

| Connection | Present assessment | Remaining executed calculation |
|---|---|---|
| Smooth effective finite-k conversion, metric and neutrinos | Executed; conserving | Physical species rates and state completion |
| Finite event times, recording heat and local thermal history | Executed; checked | Finite-k energy/momentum transfer across event hypersurfaces |
| Nonlinear lensing likelihood for a calibrated WRRA background | Conditional execution | The same observational path with native full states/event perturbations |
| 64-mode CDM frame and stable metric combination | Partial junction executed | Baryon/electron and massive-neutrino states and downstream transport |
| Entire seed-to-emission-to-thermal-to-observation chain | Incomplete | Recalibrated-background mode rerun and 3D/angular covariance completion |

The v0.25-r5 problem of mean preparation versus one individual universe remains open. Computing response to a supplied finite seed does not derive selection, preparation and probability ownership of that seed. Additional finite branches, calibrations or angular completions may be introduced, with assumptions declared and execution verified before integration status changes.

The result is a larger set of concrete modules linking residue, conversion, recording, thermal history, gravity and observation through one method. Reproducing known values is compatibility and explanatory achievement; originality lies in the transformations and conserving connection structure. The executed scope through source v0.7-dev-r1 remains partial connection, not a declaration of a completed cosmological theory.

### 136.7 Published sources and reproduction paths

| Source | DOI | Path below GitHub submission/ |
|---|---|---|
| Finite gradients v0.4 | [10.5281/zenodo.23490141](https://zenodo.org/records/23490141) | finite_gradient_matching_v0_4 |
| Finite emission v0.5 | [10.5281/zenodo.23491041](https://zenodo.org/records/23491041) | finite_emission_v0_5 |
| Observation/thermal v0.6 | [10.5281/zenodo.23491673](https://zenodo.org/records/23491673) | observation_thermal_v0_6 |
| Junction development v0.7-dev-r1 | [10.5281/zenodo.23492328](https://zenodo.org/records/23492328) | full_state_junction_v0_7 |

The repository is [wrra-m-0.1](https://github.com/Wonsik-Choi-janefather/wrra-m-0.1). Preserve each source's inputs, outputs, checks, normalization and release verification. The book v0.26 editorial audit does not replace those source checks. Zenodo carries the complete Korean/English PDFs; code and data are supplied through GitHub.
