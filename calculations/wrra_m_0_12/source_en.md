# WRRA_M 0.12 Proper-Time Updates and Mode Spectra under Finite Boundaries

Wonsik Choi · 2026-10-03 · WRRA Core 1.0 / MCC 2.3.2 · CC BY 4.0

## Abstract

The five calibrated inputs and electron mode 23 of 0.11 are frozen while shutter updates are assigned to the proper time of each timelike worldline. Flat, accelerated, finite weak-gravity and uniform-expansion clocks are executed together with finite fold and spatial spectra. Integer branches required to recover energy from update phases are disclosed. Continuous free dispersion and boundary-discretized modes are both calculated. Fixed-volume updates of the inherited SI energy ledger connect through an exact time conversion; the old slow expansion schedule fails identification with that SI phase clock. The failure and the scope of completed connections remain explicit.

## Verification inputs

The complete 0.11 input is frozen at SHA256 67de28abf0741c406178a2fe4ce07962e69bce827c3196b78e887da3bd0dab13. G=6.67430×10⁻¹¹ SI, H0=67.4 km/s/Mpc, energy shares 0.0493/0.265/0.6857 and electron rest energy 510998.95069 eV are retained. Arithmetic address shares 0.05/0.268/0.682 belong to a separate ledger. c=299792458 m/s, h=6.62607015×10⁻³⁴ J s and 1 eV=1.602176634×10⁻¹⁹ J are inherited; no new constant is fitted.

New constitutive inputs are phase interval epsilon=0.05, 128 finite modes, fold boundary phases eta=0/0.5, periodic/Dirichlet spatial boundaries and L=20 ell_mu. The accelerated beta(s)=0.2+0.5s path is prescribed, rather than derived from gravitational equations of motion. The R=200 kpc static patch and conditional Phi=Psi are inherited. Pages 5, 11 and 12 of upper hypothesis r1 supply the worldline-update and phase-energy-branch provenance. Epsilon, boundaries and length are choices, not a measured minimum time or identified physical particle confinement.

## WRRA-specific transformation

The electron calibration supplies mu_E=E_e/23, from which time/length units and the epsilon-scaled proper-time step follow. Ell_mu is a unit reference. The microscopic cavity length is not assigned to cosmic size or the undetermined 0.11 L0. Planck time is a comparison scale; c delta_tau does not prove an independent minimum spatial length.


$$
\mu_E=E_e/23,\quad t_\mu=\hbar/\mu_E,\quad \ell_\mu=ct_\mu,\quad \Delta\tau_*=\epsilon t_\mu,\quad \epsilon=0.05. \tag{1}
$$


| Quantity | Calculated value | Unit |
| --- | --- | --- |
| mu_E | 22217.345682174 | eV |
| t_mu | 2.962603932832e-20 | s |
| delta_tau | 1.481301966416e-21 | s |
| L_cavity | 1.776332630208e-10 | m |


The execution gives delta_tau=1.481301966416e-21 s and delta_tau/t_P=2.747605735737e+22. Doubling epsilon leaves the energy spectrum and electron calibration unchanged.

A timelike path uses accumulated proper time. In the weak static patch A=1+2Phi/c² and B=1−2Phi/c², beta_local is speed measured by a static observer, rather than the coordinate speed. A=B=1 in flat space. Different paths are not forced to share one global shutter tick.


$$
\begin{aligned}c^2d\tau^2&=A c^2dt^2-B\,d\mathbf{x}^2,\\\beta_{\mathrm{local}}^2&=\frac{B}{A c^2}\left|\frac{d\mathbf{x}}{dt}\right|^2,\quad \frac{d\tau}{dt}=\sqrt{A(1-\beta_{\mathrm{local}}^2)}.\end{aligned} \tag{2}
$$



$$
\tau(t)=\int_0^t\frac{d\tau}{dt^{\prime}}dt^{\prime},\quad k=\lfloor\tau/\Delta\tau_*\rfloor,\quad r_\tau=\tau/\Delta\tau_*-k,\quad \tau(t_k)=k\Delta\tau_*. \tag{3}
$$


For coordinate interval T=64 delta_tau, beta=0/0.6/0.8 gives 64/51/38 complete updates with a separate residual phase interval. The overlap column concerns an equally weighted fold-mode pair separated by mu_E; it is not an outcome probability or physical record. A null path has zero proper time, but no rest-clock update count is assigned. Photon propagation is not declared frozen.

| beta | tau / delta_tau | Complete ticks | Coherent overlap |
| --- | --- | --- | --- |
| 0.0 | 64.0 | 64 | 0.000852612 |
| 0.6 | 51.2 | 51 | 0.082205611 |
| 0.8 | 38.4 | 38 | 0.328925174 |



$$
t^{\prime}=\gamma_u(t-ux/c^2),\quad x^{\prime}=\gamma_u(x-ut),\quad c^2\Delta t^{\prime 2}-\Delta x^{\prime 2}=c^2\Delta t^2-\Delta x^2. \tag{4}
$$


The accelerated path is divided into 16/32/64/128 chords and each proper interval compared in a frame boosted by u/c=0.3. Errors against the path integral tau/T=0.877980386396 decrease by approximately four per refinement. Inverting accumulated proper time generates 57 update events. This is a numerical convergence check on a finite path.

The static local-clock potential integrates the inherited g(r) to finite boundary R. Phi(R)=0 normalizes the boundary clock. No reference at infinite distance is introduced. Independent numerical differentiation of the potential returns the same gravitational acceleration.


$$
\Phi(r)=-\int_r^R g(s)\,ds,\quad R=200\,\mathrm{kpc},\quad \Phi(R)=0,\quad \frac{\nu_R}{\nu_r}=\sqrt{A(r)/A(R)}. \tag{5}
$$


| r / kpc | Phi / c² | Static d_tau / d_t |
| --- | --- | --- |
| 3 | -1.728306260831e-06 | 0.999998271692 |
| 8.2 | -1.248693279810e-06 | 0.999998751306 |
| 50 | -4.966030243693e-07 | 0.999999503397 |
| 200 | -0.000000000000e+00 | 1.000000000000 |


At 8.2 kpc, the inherited 207.510905127 km/s rotation gives a moving-clock d_tau/d_t=0.999998511748. The uniform carrier I/N is stationary under any Hamiltonian, allowing FRW clock integration while retaining the uniform energy, pressure and expansion outputs. Constant peculiar beta=0.6 specifies a path and assumes additional motion. Enormous update counts are floating-point order estimates, not exact integers or simulations of every event.


$$
H(a)=H_0\sqrt{(f_\varphi+f_c)a^{-3}+f_b},\quad \Delta\tau=\int_{a_0}^{a_1}\frac{\sqrt{1-\beta_{\mathrm{pec}}^2}}{aH(a)}\,da. \tag{6}
$$


A self-adjoint energy operator is now constructed on a finite fold basis. Every realized matrix has finite dimension N=128. F is the normalized Fourier matrix and eta the declared fold boundary phase; allowed modes run from −64 through 63. The construction uses a finite spectral projection of the derivative; grid error is not hidden by refitting the electron mode.


$$
F_{jn}=N^{-1/2}e^{2\pi i jn/N},\quad H_{\mathrm{fold},\eta}=F\,\operatorname{diag}(\mu_E|n+\eta|)F^{\dagger},\quad H=H^{\dagger}. \tag{7}
$$


F represents the periodic-gauge field phi(y). The physical fold field psi(y)=exp(2pi i eta y)phi(y) encodes its boundary phase through the derivative shift n+eta.


$$
\psi(y+1)=e^{2\pi i\eta}\psi(y),\quad \eta=0\ \mathrm{or}\ 1/2,\quad E_{23,0}=23\mu_E=E_e. \tag{8}
$$


Eta=0 reproduces the zero-intercept 0.11 mass branch. Eta=0.5 changes mode 23 to 522107.623531087 eV without recalibration. This is boundary sensitivity under the same calibration, not a claim that the physical electron boundary changed or a new particle identification. Equal ±23 energies at eta=0 do not determine charge sign; charge remains in the inherited filter ledger.

A separate finite spatial interval carries a free positive-energy operator with the electron rest energy. K is the positive squared-wave-number operator for the chosen boundary. A periodic boundary allows zero momentum; Dirichlet constrains both endpoint values to zero. These are explicit finite-domain boundary constraints, rather than a modeled physically infinite energy barrier.


$$
K=F_B\operatorname{diag}(k_n^2)F_B^{\dagger},\quad H_{\mathrm{space}}=\sqrt{E_e^2I+(\hbar c)^2K},\quad L=20\ell_\mu. \tag{9}
$$



$$
k_n^{\mathrm{periodic}}=2\pi n/L,\quad k_n^{\mathrm{Dirichlet}}=\pi n/L,\quad \psi_n(x)\propto\sin(\pi nx/L),\quad n=1,\ldots,N. \tag{10}
$$


| Boundary / operator | Mode | Energy / eV | Kinetic / eV |
| --- | --- | --- | --- |
| fold periodic | 0 | 0.000000000 | — |
| fold periodic | 23 | 510998.950690000 | — |
| dirichlet | 1 | 511010.867747384 | 11.917057384 |
| dirichlet | 2 | 511046.617252180 | 47.666562180 |
| periodic | 0 | 510998.950690000 | 0.000000000 |
| periodic | 1 | 511046.617252180 | 47.666562180 |


The table distinguishes total energy from kinetic energy after subtracting rest energy. It is not fitted to atomic lines or an observed cavity. Finite L=20/40/80 ell_mu controls halve momentum spacing and approximately quarter the first kinetic-energy gap. These controls assume no physically realized infinite space.

Local free dispersion without a confinement boundary responds continuously to finite real momentum inputs. Noninteger pc/mu_E=0.1/0.5 runs under the same shutter update. Discrete time alone does not discretize every momentum or energy. The independent finite-difference electron-mode control has errors −5.2271%/−1.3225%/−0.3316% at N=128/256/512 while keeping mu_E fixed.


$$
E(p)=\sqrt{E_e^2+c^2p^2},\quad p\ \mathrm{real},\quad E^{\mathrm{FD}}_{23,N}=\mu_E\frac{N}{\pi}|\sin(23\pi/N)|. \tag{11}
$$


A proper-time update is the unitary of the same Hamiltonian. Eigenvalues of U are independently computed to read theta. At the default epsilon, fold and both spatial spectra agree with phase recovery to numerical precision. Phase alone leaves an integer energy branch ell undetermined, so the generator and branch must be disclosed.


$$
U_* = e^{-iH\Delta\tau_*/\hbar},\quad U_*v_j=e^{-i\theta_j}v_j,\quad 0\leq\theta_j<2\pi. \tag{12}
$$



$$
E_j=\frac{\hbar}{\Delta\tau_*}(\theta_j+2\pi\ell_j),\quad \ell_j\in\mathbb{Z},\quad E_{\mathrm{band}}=2\pi\hbar/\Delta\tau_*. \tag{13}
$$



$$
e^{-i(H+mE_{\mathrm{band}}I)\Delta\tau_*/\hbar}=U_*,\quad m\in\mathbb{Z}. \tag{14}
$$


At epsilon=0.25, 77 fold modes require nonzero integer branches. Discarding them produces a large energy-recovery failure. Reading U in the generator eigenbasis and adding the disclosed branches restores the energies. The branch integers are not newly inferred from U alone.

## Outputs and comparison with the inherited clock

The 0.10 fixed-volume E_star=ucrit V0 ledger and dimensionless xi coordinate convert exactly to SI proper time using the same energy matrix. Microscopic fold/spatial spectra are separate probes; their electron energy is not added again to macroscopic density. V0=1 m³ is the declared collective ledger volume, rather than a volume deriving a fundamental particle clock.


$$
U_{0.10}(\xi)=e^{-i\xi\widehat E/E_*}=e^{-i\widehat E\tau/\hbar},\quad \xi=E_*\tau/\hbar,\quad \rho(\tau)=U\rho_0U^{\dagger}. \tag{15}
$$


States and D/R loads are executed at k=0/1/2/4/8 actual delta_tau intervals. Total energy remains 3.200810499959×10⁻¹⁰ J while the D-load range is 0.038059728227. Normalization and positivity hold within numerical tolerances. This fixed-volume internal exchange includes no measurement apparatus or physical record generation yet.


$$
\operatorname{Tr}\rho=1,\quad \operatorname{Tr}(\rho\widehat E)=\mathrm{constant},\quad |\langle\psi_0|U(\tau)|\psi_0\rangle|^2=\cos^2(\mu_E\tau/2\hbar). \tag{16}
$$


However, the slow omega_info=0.7H0 used in the 0.10 expansion-state schedule is not E_star/hbar. The frequencies are 1.528999668760×10⁻¹⁸ s⁻¹ and 7.272096256981×10²⁴ s⁻¹, respectively, with a ratio near 2.10×10⁻⁴³. Identifying the slow schedule as the physical SI phase of the same energy generator is falsified by this comparison. Retaining that schedule would require separate justification for another effective generator or interaction; this release does not claim to resolve it by substitution.


$$
r_{\mathrm{clock}}=\frac{\hbar\omega_{\mathrm{info}}}{E_*}\ne1,\quad H_{\mathrm{eff}}=r_{\mathrm{clock}}\widehat E\ne\widehat E. \tag{17}
$$


| Computed comparison | Value | Unit / role |
| --- | --- | --- |
| Default U eigenphase error | 6.519258022308e-09 | eV |
| Aliased naive error | 8.664764816048e+05 | eV |
| Declared-branch error | 4.656612873077e-10 | eV |
| Old / SI frequency | 2.102556972196e-43 | ratio |


The old nonuniform slow expansion histories remain records of a constitutive schedule. The new physical phase is executed on the fixed-volume ledger; the uniform FRW clock connects through the stationary I/N state. Fully covariant nonuniform carrier/gravity/expansion dynamics are not closed here. Numerical small-step controls approach the same continuous Hamiltonian generator; this approximation requires no physically infinite spatial or temporal support.


$$
\frac{i\hbar(U(\delta\tau)-I)}{\delta\tau}\longrightarrow H,\quad \delta\tau\longrightarrow0. \tag{18}
$$


## Falsifiers and reproduction

The connection must be revised if Lorentz transformations change proper time, the static-potential derivative fails to reproduce g, boundary energies and update phases disagree, integer branches are dropped or fixed-volume energy conservation fails. The failed identification of the old slow schedule with the SI phase is included in the verdict. All 36 new checks and 60 checks inherited from 0.11/0.10 pass. Invalid global/minimum-clock claims, unsupported infinite boundaries, out-of-patch paths and unexecuted physical-record inputs are rejected.

```bash
python -m pip install -r calculations/wrra_m_0_12/requirements.txt
python calculations/wrra_m_0_12/run_release.py
```

Parameters.json discloses inputs, provenance and constitutive choices. JSON and eight CSVs provide path clocks, update events, allowed modes, spatial dispersion and load exchange. A clean copy with captured results removed reproduces outputs and both manuscripts byte for byte. The 18 native Word equations and five computed tables are compared between editions, with every PDF page rendered and inspected. Numerical verification, document comparison and clean-copy reproduction verdicts are separate JSON records.

Input SHA256 c80742fa4d0e0bdbb94e3390a2cc02da4a535168eaf66fb28f7318ec9b7b8b3d

## Completion and subsequent scope

Under disclosed choices, 0.12 completes worldline proper-time updates, finite operator/boundary spectra and the fixed-volume SI-time conversion. The clock-identification failure and incomplete covariant connection are frozen alongside them. The origin or measured-minimum status of delta_tau and actual confinement boundary/length selection remain open. Version 0.13 executes physical binary outcomes, post-observation states and records; subsequent stages treat repeated uncertainty, stress, curvature, size, neutrinos and propagation. A new independent prediction or unique universe solution is not a prerequisite for this completion.

## References

Choi Wonsik. WRRA_M 0.11, frozen baseline commit 6e9e9c9162c650b71b78035abf02ec6c1f753d02. https://github.com/Wonsik-Choi-janefather/wrra-m-0.1

Choi Wonsik. WRRA_M Upper Two-Stage Filter Hypothesis 1.0-r1 (2026-10-02), pp. 5, 11–12; source contract in references/clock_contract.md.

Choi Wonsik. Minimal Computation Cosmology 2.3.2, chapter 23, frozen commit 21daec110c0cbecb228c445d587eac8302e7f767. https://github.com/Wonsik-Choi-janefather/minimal-computing-cosmology-2.3.2

Hughes Scott. MIT 8.033, Fall 2024 lecture notes, sections 18.2–18.3. https://ocw.mit.edu/courses/8-033-introduction-to-relativity-and-spacetime-physics-fall-2024/mit8_033_f24_lec_full.pdf

Copyright 2026 Wonsik Choi. CC BY 4.0. https://creativecommons.org/licenses/by/4.0/
