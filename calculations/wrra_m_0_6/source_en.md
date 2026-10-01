# WRRA M 0 6 Information Load and Twist Gravity with Expansion in a Finite Model

A continuous geometric model that computes energy load and pressure from common carrier states

Wonsik Choi  
WRRA-M 0.6-r2 | 1 October 2026  
Independent Researcher Seoul Republic of Korea  
ORCID 0009-0001-4263-9772 | janefather@gmail.com

## Result and computational scope

This work completes a finite constitutive model from common-carrier information states to physical load, twist, local gravity and global expansion. One energy functional supplies state evolution, pressure under volume variation and background dynamics. Individual weighted states therefore connect the carrier calculation to local gravity, while background pressure is computed from the same energy rather than inserted as a separate equation-of-state input.

Completion here is within the declared finite homogeneous model. The volume dependence of energy, load operators and information clock remain disclosed constitutive choices. Pressure and conservation are consequences of those choices. A unique microscopic law of the actual universe and a complete four-dimensional covariant gravity theory are not claimed. Local rotation and lensing are conditional outputs of the inherited calibrated response evaluated with the same clustering load.

WRRA Core 1.0 and Minimal Computation Cosmology MCC 2.3.2 remain the baseline. The B_C premise is preserved: mass may be quantized as a phenotype, whereas fundamental gravity precedes phenotype. Matrix information states are used without introducing an independent gravitational Hilbert space or gravitons. This premise is not classified as a universal theorem excluding gravity quantization.

## Structure inherited from the individual twist papers

The model inherits the quadratic load and calibrated response of twist-stress cosmology, the direct/clustering accounting of the dual-component gravity paper, and the distinction between global gluing and local curvature in the finite boundaryless paper. In particular, the global background and local stress in MCC 2.3.2 Chapters 28–29 are treated as two responses of the same prephenotypic load. No separate dark component is added over that load to count the same effect twice.

The present late-universe calibrations are phenotype 4.93%, entire hidden load 95.07%, clustering sector 26.5% and residual background 68.57%. Each is an energy-weighted fraction of the whole universe. The clustering share is a subset of the hidden total, rather than 26.5% of that total. These are editable inputs, not measured bit-count or particle-channel fractions.

## Weighted states on the common carrier

Sixteen witness channels share one internal lattice. The internal information state ρ is positive semidefinite with unit trace. Its load Js is evaluated by the trace of the state and a positive operator.

$$R=\frac{I_{16}}{16}\otimes\rho,\qquad \rho\succeq0,\quad\mathrm{Tr}\rho=1,\quad J_s=\mathrm{Tr}(\rho K_s). \tag{1}$$

A periodic cycle Laplacian on N=128 sites is the clustering operator. The background operator starts from the same Laplacian and adds a positive rank-one term only for the noncommuting test. The denominator maintains background load 2 in the uniform state.

Version 0.6 lattice_N controls the common grid for information loads and the transport carrier test. The original 0.5 input is retained as calibration provenance; the shared value is applied only to a private copy for the carrier calculation. The result lattice_contract discloses the configured and effective sizes. Cross-input tests at 64/128 and 128/64 confirm matching grids and unchanged uniform reference outputs.

$$K_c=2I-T-T^\dagger,\qquad K_b=\frac{K_c+\epsilon|0\rangle\langle0|}{1+\epsilon/(2N)}. \tag{2}$$

The reference uses ε=0 and the noncommuting test ε=8. The latter is a fixed experiment in exchange between two weighted loads of one state, not a preferred microscopic value for the physical universe. The same operators apply to every witness channel, so this modification does not solve channel-dependent filter selection.

The uniform reference has Jc=Jb=2. A single disclosed calibration of the hidden density supplies the physical density coefficient η.

$$u_{\mathrm{crit},0}=\frac{3H_0^2c^2}{8\pi G},\quad \eta=\frac{f_hu_{\mathrm{crit},0}}{2},\quad \chi=\frac{f_c}{f_h}. \tag{3}$$

Equal unit-trace states can carry different weighted loads. Information weight here depends on the expectation of the energy operator, rather than the normalized number of states alone. A universal rest mass or fixed energy is not assigned to an arbitrary bit.

## One energy functional and its pressure

For representative volume V₀a³, declare the following energy operator. The exponents nc and nb specify how the information load responds to volume and remain constitutive inputs.

$$h(a)=\chi a^{n_c}K_c+(1-\chi)a^{n_b}K_b,\quad \mathcal H(a)=\eta V_0h(a). \tag{4}$$

$$E_h=\mathrm{Tr}(\rho\mathcal H),\quad V=V_0a^3,\quad u_h=\frac{E_h}{V}=u_c+u_b. \tag{5}$$

$$u_c=\eta\chi a^{n_c-3}J_c,\qquad u_b=\eta(1-\chi)a^{n_b-3}J_b. \tag{6}$$

Pressure is the volume derivative at fixed state. Each component's comoving energy is proportional to a raised to its exponent, giving

$$p_s=-\left(\frac{\partial E_s}{\partial V}\right)_\rho=-\frac{n_s}{3}u_s,\qquad n_c=0,\quad n_b=3. \tag{7}$$

The choice nc=0 gives fixed comoving clustering energy and zero pressure. The choice nb=3 makes background energy proportional to physical volume, with pressure equal to minus its density. This version does not independently input w again. It also does not derive the microscopic origin of exponent 3. Constant density and negative pressure are exact consequences of the chosen volume dependence.

## Information evolution and total conservation

The same energy operator generates a lossless state update. Here ℓ is the lapse, set to 1 for calculation. The positive action scale A∗ sets the information clock and is not identified with Planck's constant. The present ω∗/H₀=0.7 is also a disclosed test input.

$$\dot\rho=-\frac{i\ell}{\mathcal A_*}[\mathcal H,\rho]=-i\ell\omega_*[h,\rho],\quad \mathcal A_*=\frac{\eta V_0}{\omega_*}. \tag{8}$$

On the unitary orbit ρ=Uρ₀U†, trace, positivity and the state's eigenvalues are preserved. Cyclicity of the trace makes the state-change contribution to the instantaneous energy vanish. Its change is the work associated with volume variation.

$$\mathrm{Tr}(\mathcal H\dot\rho)=0,\quad \dot E_h=-p_h\dot V,\quad \dot u_h+3H(u_h+p_h)=0. \tag{9}$$

This does not make the information state stationary. Individual Jc and Jb may change. Noncommuting operators transfer energy between the internal sectors while their exchange sums to zero. Pure-state phases and mixed-state spectral accounting can therefore be used together with global expansion.

## Classical background action and expansion

Choose an isotropic flat average on a finite T³. Spatial identification and extra local gravity remain distinct. The classical background action is

$$S_g=-\frac{3c^2V_0}{8\pi G}\int dt\,\frac{a\dot a^2}{\ell}. \tag{10}$$

Couple the state-orbit action and phenotype load to the same lapse. The pressureless phenotype has fixed comoving energy Eφ,0.

$$S_I=\int dt\left[i\mathcal A_*\mathrm{Tr}(\rho_0U^\dagger\dot U)-\ell(E_{\phi,0}+\mathrm{Tr}(\rho\mathcal H))\right]. \tag{11}$$

Varying the sum Sg+SI with respect to ℓ gives the Friedmann constraint; variation with respect to a gives the acceleration equation; and variation of U gives equation (8). Homogeneous state, energy, pressure and expansion consequently close in a single finite action.

$$H^2=\frac{8\pi G}{3c^2}u_{\mathrm{tot}},\qquad \frac{\ddot a}{a}=-\frac{4\pi G}{3c^2}(u_{\mathrm{tot}}+3p_h). \tag{12}$$

This is a minisuperspace action restricted to homogeneous degrees of freedom. It does not derive local photon transport, anisotropic stress, spatial perturbations or galactic backreaction in a full four-dimensional action. The Friedmann and continuity equations are established external mathematics [5]. The constitutive contribution here is the connection among weighted information load, state evolution, pressure and twist response.

Component continuity includes the state-dependent exchange, with χc=χ and χb=1−χ.

$$Q_s=\eta\chi_s a^{n_s-3}\dot J_s,\qquad \dot u_s+3H(u_s+p_s)=Q_s,\quad Q_c+Q_b=0. \tag{13}$$

$$q=\frac{u_{\mathrm{tot}}+3p_h}{2u_{\mathrm{tot}}},\qquad n_c=0,\ n_b=3:\quad q<0\ \Longleftrightarrow\ 2u_b>u_\phi+u_c. \tag{14}$$

Expansion and accelerated expansion are distinct. For nc=0 and nb=3, acceleration occurs when the background load satisfies the stated inequality relative to phenotype and clustering load. It is not asserted that every twist or information state accelerates the universe.

## The same load in twist and local gravity

The entire hidden energy density determines the global twist rate. Only its clustering part supplies the local additional-attraction scale.

$$\zeta\kappa_h^2=\frac{16\pi G}{c^4}u_h,\qquad a_T^2=\frac{\pi G}{3}u_c=\frac{\zeta c^4}{48}\kappa_c^2. \tag{15}$$

The second relation rewrites the existing 0.5 calibration aT=cH√(fc/8) using the critical density. Changes in state therefore change uc and aT by actual calculation. The global H and instantaneous source fractions are not held inconsistently fixed under changing load.

The local response retains the calibrated function adopted in the earlier galactic-disk paper.

$$y=\frac{g_M}{a_T},\quad \nu(y)=\frac{1}{1-e^{-\sqrt y}},\quad g=\nu(y)g_M,\quad v_c^2=rg. \tag{16}$$

The test source is a Plummer mass of 6×10¹⁰ solar masses with scale 3 kpc, and velocities are compared at 8.2 kpc. This is neither an observed galaxy's temporal history nor a new data fit. Under Φ=Ψ, the same acceleration supplies conditional lensing.

$$\widehat\alpha_R(b)=\frac{2}{c^2}\int_{-\sqrt{R^2-b^2}}^{\sqrt{R^2-b^2}}g(\sqrt{b^2+z^2})\frac{b\,dz}{\sqrt{b^2+z^2}}. \tag{17}$$

The patch radius is R=200 kpc and the impact radius b=10 kpc. Exterior geometry and observer-lens-source distance factors are excluded. Microscopic derivation of the local response and verification of gravitational slip remain outside the completion claim.

| Information state | J | aT m/s² | v km/s |
| --- | --- | --- | --- |
| Uniform reference | 2.000000 | 1.191813e-10 | 207.510905 |
| Low mode | 0.152241 | 3.288204e-11 | 177.250177 |
| Coherent packet | 0.657554 | 6.833742e-11 | 192.003913 |
| High mode | 4.000000 | 1.685478e-10 | 219.215978 |
| Zero mode | 0.000000 | 0.000000e+00 | 161.450511 |


The uniform reference reproduces aT=1.191812669e-10 m/s² and 207.510905 km/s. Its conditional lens deflection is 0.535586511 arcsec. These acceleration, rotation and lensing outputs agree with the recorded 0.5 results. The zero mode has no additional gravity; undefined fractions and uncomputed zero-load lensing are recorded as null.

## Finite boundaryless construction and geometric load

The representative T³ identification of the finite boundaryless paper is retained. Its reference length L₀ is unidentified and L=L₀a. At fixed positive stiffness, the quadratic loop-record aggregate obeys

$$L=L_0a,\quad Q=\sum_{i=1}^{3}\Theta_i^2,\quad W=\zeta Q=\frac{16\pi G}{c^4}u_hL^2. \tag{18}$$

$$E_h=\frac{c^4}{16\pi G}WL,\qquad L=\frac{16\pi GE_h}{c^4W}\quad(W>0). \tag{19}$$

For positive nonzero load, positive L₀ and finite a, volume is finite at each calculated instant and T³ has no boundary. This is an exact conditional identity of the chosen identification. It neither selects the actual universe's unique topology nor measures absolute cosmic length. A fixed volume upper bound over an indefinitely expanding future is not established.

For the uniform reference with nc=0 and nb=3, expansion and global twist record magnitude are

$$\frac{H^2}{H_0^2}=(f_\phi+f_c)a^{-3}+f_b,\qquad \frac{W}{W_0}=\frac{f_c/a+f_ba^2}{f_h}. \tag{20}$$

| a | H/H₀ | q | W/W₀ | κh/κh₀ | aT/aT₀ |
| --- | --- | --- | --- | --- | --- |
| 0.5 | 1.788882 | 0.178588 | 0.737798 | 1.717904 | 2.828427 |
| 1.0 | 1.000000 | -0.528550 | 1.000000 | 1.000000 | 1.000000 |
| 2.0 | 0.851462 | -0.918714 | 3.024403 | 0.869541 | 0.353553 |


Physical twist rate and global twist record magnitude evolve differently. The record magnitude is an aggregate computed from the load density and spatial size at the current state and scale; no independent law of temporal record accumulation has been calculated. Beyond the present, this global record magnitude can grow during expansion while the density-dependent physical twist rate declines. They are not combined into one scalar twist statement. The variable a is geometric scale; it is not automatically replaced by observed redshift before a twist photon-redshift kernel is derived.

![Figure 1 Expansion and twist calculated from one energy functional](results/expansion_twist.png){width=6.4in}

The start calculation attempted to express every background density with one fixed load kernel and failed the state-domain bound at a=0.5. The present version specifies the volume dependence of energy, so the physical load kernel itself depends on geometry.

$$K_{\mathrm{phys}}(a)=\frac{h(a)}{a^3},\qquad \lambda_{\min}(K_{\mathrm{phys}})\leq\mathrm{Tr}(\rho K_{\mathrm{phys}})\leq\lambda_{\max}(K_{\mathrm{phys}}). \tag{21}$$

Trace-one normalization and state positivity are retained. The operator spectrum varies with a, and every calculated uniform reference state from a=0.5 to 2 lies within that spectrum. This resolves the start model's restriction by an explicit new constitutive choice.

## Executed noncommuting state evolution

Modes 8, 16 and 24 are superposed with equal weights. For commuting operators, phases evolve while mean loads stay constant. In the noncommuting test, both mean loads actually change.

Jc spans 0.657554 to 0.764647 and Jb spans 0.763529 to 0.819446. These are calculated test results at ε=8 and the declared information clock. They follow from weighted states and geometry-dependent energy, rather than a change in normalized information count.

![Figure 2 Changing loads and cancelling internal stress exchange](results/state_exchange.png){width=6.4in}

The two sectors are not independently supplied by an external source. Equations (9) and (13) preserve their total. Directly calculated exchange sums nearly to zero, and an independent finite difference verifies total continuity.

## Verification and falsification

The state ODE is integrated in both directions with DOP853. An independent midpoint unitary exponential propagator starts from the same state and compares 320 and 640 steps. The noncommuting load error improves by approximately four at both endpoints, as expected for second-order convergence. A separate integration of the acceleration equation also checks endpoint state loads and time against integration using the H constraint.

| Check | Maximum error |
| --- | --- |
| Pressure from finite volume variation | 2.848e-11 |
| Noncommuting state norm error | 4.667e-12 |
| Total continuity residual | 4.105e-08 |
| Acceleration from derivative of H | 2.053e-08 |
| Internal exchange cancellation | 2.892e-15 |
| Finite T3 closure identity | 8.882e-16 |
| Constraint in independent acceleration solution | 4.805e-11 |


Additional checks cover pressure from finite volume variation, simultaneous basis-change invariance, the combined zero-phenotype/zero-hidden-load boundary, and a zero-residual-background boundary. Negative operator coefficients, zero scale and a nonfinite information clock are rejected. These establish homogeneous numerical consistency; they are not a test of spatial sound speed, perturbation stability or observed lens fits.

Negative kernel eigenvalues or loss of trace/positivity reject the load model. A mismatch between pressure and volume variation, or noncancelling exchanges, invalidates the single-energy construction. An acceleration solution inconsistent with the Friedmann constraint requires revising the background link. Failure of motion and lensing under the same response requires revising the conditional matching or slip assumption.

## Constitutive choices and completion claim

The dependence of expansion on energy homogeneity is evaluated explicitly. For the uniform reference,

$$\rho=I_N/N:\quad J_c=J_b=2,\qquad q_0=\frac{1-n_bf_b}{2}\quad(n_c=0). \tag{22}$$

| nb | wb | q₀ |
| --- | --- | --- |
| 0.0 | -0.000000 | 0.500000 |
| 1.0 | -0.333333 | 0.157150 |
| 1.5 | -0.500000 | -0.014275 |
| 2.0 | -0.666667 | -0.185700 |
| 3.0 | -1.000000 | -0.528550 |


Exponent 1 gives a w=−1/3 background associated with a fixed twist record and does not accelerate at the adopted calibration. Exponent 3 gives constant density and w=−1; the reference background has the ΛCDM expansion form. This identity is not presented as an independent observational prediction or microscopic proof of exponent 3. The result is a consistent pressure and dynamical calculation from the declared volume dependence of information energy.

| Claim | Status | Result in this version |
| --- | --- | --- |
| State-dependent information load | Executed within the chosen operators | Matrix trace agrees with mode calculation |
| State evolution pressure and conservation | Finite homogeneous construction and calculation | One energy functional and action |
| Expansion and twist together | Conditional background output | H records and twist rate calculated together |
| Information load to local gravity | Inherited calibrated matching | Rotation lensing and 0.5 reproduction |
| Finite boundaryless universe | Conditional chosen T3 construction | Length relation for load and loop record |
| Unique microscopic weights and exponents | Open | Disclosed constitutive choices |
| Four dimensional completion and spatial perturbations | Subsequent scope | Distinguished from the homogeneous action |

The 0.6 completion boundary is to calculate load from information states, close state evolution, pressure, expansion and twist with one energy functional and homogeneous action, and pass the same clustering load into the inherited local response. This version reaches that finite boundary. Symmetric-carrier selection gaps remain zero. Actual topology and length, lower-order filter origins, covariant local response and observational validation remain recorded physical questions.

## References and reproducibility

1. Choi W. Minimal Computation Cosmology MCC 2.3.2. 2026. Chapters 28–29 on global background and local stress accounting. https://doi.org/10.5281/zenodo.22733000.
2. Choi W. Twist Stress Universe and Dark Matter Mass Phenotypes. v1.0. 11 September 2026. https://doi.org/10.5281/zenodo.22700557.
3. Choi W. Dual Component Model of Mass Gravity and Spatial Twist Stress Gravity. v0.4. 27 September 2026. The individual original is used.
4. Choi W. WRRA Finite Boundaryless Universe. v1.0. 28 September 2026. The individual original is used.
5. Trodden M and Carroll SM. TASI Lectures Introduction to Cosmology. 2004. §2.2. arXiv:astro-ph/0401547. https://vo.ned.ipac.caltech.edu/level5/Sept03/Trodden/Trodden2_2.html.
6. Choi W. WRRA-M 0.5 Information Load and Twist Gravity in a Finite Model. 1 October 2026. Korean and English manuscripts with corrected computation.
7. Choi W. WRRA Spatial Twist Galactic Disk Plane Selection and Dark Mass Phenotypes. v1.0. 27 September 2026. https://doi.org/10.5281/zenodo.23003875.

The computation and both parameter files disclose calibrations, operators and clock. results.json records complete trajectories, summary.json the main outputs, and release_checks.json reproduction and boundary tests. verify.py compares the recorded 0.5 outputs. Both language sources are generated from the same equations and numerical ledger. Calculation needs numpy, scipy and matplotlib; native Word generation additionally needs pandoc and python-docx.

© 2026 Wonsik Choi. Manuscripts and calculations are distributed under CC BY 4.0.
