# WRRA_M 0.11 Sequential Calibration of the First Five Inputs

Wonsik Choi · 2026-10-02 · WRRA Core 1.0 / MCC 2.3.2 · CC BY 4.0

## Abstract

On fixed WRRA Core 1.0 and MCC 2.3.2, WRRA_M calibrates its first five physical inputs in the order G→H0→f_phi→f_c→electron rest energy. Each partial stage reads only supplied anchors and reports available outputs and remaining coefficients. The 0.10 energy-pressure calculation and nine physical cases are retained. Address-exponent and effective-admission reparameterization explicitly discloses additional arithmetic inputs. Adopting electron mode 23 and zero intercept gives a mass unit of 22,217.345682 eV. Two response shapes fitting the same anchors demonstrate reproduction together with residual freedoms.

## Verification inputs

The complete 0.10 input is frozen by hash. G and electron energy use NIST 2022 CODATA; H0=67.4 is the Planck 2018 base-LambdaCDM calibration benchmark. Standard uncertainties are 1.5×10⁻¹⁵ SI for G, 0.00016 eV for electron energy and 0.5 km s⁻¹ Mpc⁻¹ for the adopted H0 benchmark. Physical fractions 4.93% and 26.5% are inherited rounded calibrations without a covariance assigned here. The first five candidate-sheet entries and the MCC electron-mode relation are recorded as provenance.

| Input | Adopted value | Unit / role |
| --- | --- | --- |
| G | 6.6743000e-11 | m³ kg⁻¹ s⁻² |
| H0 | 67.4 | km s⁻¹ Mpc⁻¹ |
| f_phi | 0.0493 | energy fraction |
| f_c | 0.265 | energy fraction |
| m_e c² | 510998.95069 | eV |


c=299792458 m/s is fixed. h=6.62607015×10⁻³⁴ J s and 1 eV=1.602176634×10⁻¹⁹ J are exact SI references. The parsec conversion, local masses/radii/response function and conditional Phi=Psi lensing are inherited. Address cutoff, four zeta heights, K=8, phase increment 0.1, response coefficients lambda_s, volume exponents and the electron-mode integer are constitutive inputs; the five numerical anchors do not derive them.

## WRRA-specific transformation

The partial calculator adds one anchor at a time. G fixes the SI action normalization and curvature response. Exact h and c additionally give Planck length/time as unit references. Replacing all future anchors with NaN must leave the corresponding earlier-stage outputs unchanged.


$$
C_G=\frac{c^4}{16\pi G},\qquad B_G=\frac{8\pi G}{c^4},\qquad \ell_P=\sqrt{\frac{\hbar G}{c^3}},\quad t_P=\ell_P/c. \tag{1}
$$


After converting H0 to inverse seconds, the critical energy density is calculated. c/H0 and 1/H0 are Hubble length/time references, not assignments of the total cosmic size or age.


$$
H_0=\frac{H_{0,\mathrm{km/s/Mpc}}\,10^3}{10^6\,\mathrm{pc}_{\mathrm m}},\qquad u_{\mathrm{crit}}=\frac{3H_0^2c^2}{8\pi G}. \tag{2}
$$


The phenotype fraction gives the total hidden load. Adding the clustering fraction f_c separates D from background R. eta_load is the homogeneous-carrier reference coefficient of 0.6, distinct from the address-sector eta_s coefficients of 0.10.


$$
f_h=1-f_\varphi,\quad f_b=1-f_\varphi-f_c,\quad u_h=f_hu_{\mathrm{crit}},\quad \eta_{\mathrm{load}}=u_h/2. \tag{3}
$$



$$
Q_h\equiv\zeta\kappa_h^2=\frac{16\pi G u_h}{c^4},\qquad L_*=Q_h^{-1/2},\qquad L_0=L_*\sqrt{W_0}. \tag{4}
$$


The identifiable quantity is weighted twist Q_h. Stiffness zeta and twist kappa_h are not separately determined. L_star is a calculated length coefficient; L0 remains undetermined without W0. The 95.07% hidden share alone does not fix cosmic length.

| Step | New input | Newly available outputs | Remaining anchors / choices |
| --- | --- | --- | --- |
| 1 | G | action coefficient; SI response | H0, f_phi, f_c, E_e |
| 2 | H0 | H0 in s⁻¹; critical density | f_phi, f_c, E_e |
| 3 | f_phi | hidden density; weighted twist | f_c, E_e |
| 4 | f_c | sector energies; a_T, P, q | E_e |
| 5 | E_e | mass unit; electron units | structural freedoms remain |


The 0.10 address effects e_s(n), normalized weights w_n and positive responses g_s(n) are retained. Each eta_s is fitted once on the reference address state and uniform carrier, then held fixed for address/state controls. Carrier operators are A_phi=I, A_D=Kc/2 and A_R=Kb/2, each with unit uniform reference expectation.


$$
\mu_s=\sum_nw_ne_s(n)g_s(n),\quad \eta_s=\frac{f_su_{\mathrm{crit}}}{\mu_s},\quad \widehat E(a)=V_0\sum_s\eta_s\mu_sa^{\nu_s}A_s. \tag{5}
$$


Pressure is the volume derivative of the same energy function. Retaining nu_phi=nu_D=0 and nu_R=3 gives pressureless D/phenotype and P_R=−u_R. Nonphenotype status does not delete energy or gravity.


$$
V=V_0a^3,\qquad E_s=\operatorname{Tr}(\rho\widehat E_s),\qquad P_s=-\partial E_s/\partial V=-\nu_su_s/3. \tag{6}
$$



$$
a_T=cH_0\sqrt{f_c/8},\qquad P_0=-f_bu_{\mathrm{crit}},\qquad q_0=(1-3f_b)/2. \tag{7}
$$


Electron mode n_e=23 is adopted in the zero-intercept MCC mass branch. The electron anchor fixes its common energy unit. Reported ±1, ±2, ±3 and ±23 are generic mode controls, not identifications of other particle masses. Mode sign has the same rest energy; charge remains separately inherited from the filter ledger. Mode number and zero intercept are additional constitutive choices.


$$
E_n=\sqrt{E_{\mathrm{off}}^2+n^2\mu_E^2},\qquad E_{\mathrm{off}}=0,\qquad \mu_E=E_e/23,\quad E_e=m_ec^2. \tag{8}
$$


The same total energy operator is expressed in electron-energy units. Multiplying back by E_e restores the original joule ledger. Electron energy is not separately added to cosmic density. Physical boundary conditions, the microscopic clock and general spectra remain for 0.12.


$$
\widetilde E_e=\widehat E/E_e,\qquad \widehat E=E_e\widetilde E_e,\qquad m_e=E_e/c^2. \tag{9}
$$


## Re-expression of address alpha and beta

Here alpha_addr is the address power-law exponent and beta_eff is the effective admission rate of odd composites. These differ from electromagnetic fine-structure alpha_EM. The two independent 0.9 arithmetic targets D=0.268 and phi=0.05 remain disclosed additional inputs; physical energy targets 0.265 and 0.0493 do not replace them. C_even excludes the prime address 2.


$$
w_n(\alpha_{\mathrm{addr}})=\frac{n^{-\alpha_{\mathrm{addr}}}}{\sum_{j=2}^{N}j^{-\alpha_{\mathrm{addr}}}},\qquad \sum_{n\in C_{\mathrm{even}}}w_n=0.268. \tag{10}
$$



$$
\sum_{n\in C_{\mathrm{odd}}}w_n b_n(h)=0.05,\qquad \beta_{\mathrm{eff}}=\frac{0.05}{\sum_{n\in C_{\mathrm{odd}}}w_n}. \tag{11}
$$


Resolving the fixed phase/filter gives alpha_addr=1.899687695055, h=1.447673170353 and beta_eff=0.865457012414. Alpha_addr and h fit the two arithmetic targets; beta_eff is then derived as their re-expression. A third independent beta input is unnecessary. The five physical anchors alone do not determine arithmetic targets or alpha_EM.

## Calculated outputs

| Quantity | Calculated value |
| --- | --- |
| ucrit J m⁻³ | 7.668947767822e-10 |
| u_hidden J m⁻³ | 7.290868642868e-10 |
| eta_load J m⁻³ | 3.645434321434e-10 |
| zeta kappa_h² m⁻² | 3.028112744666e-52 |
| Length coefficient m | 5.746639841098e+25 |
| a_T m s⁻² | 1.191812669106e-10 |
| P Pa | -5.258597484395e-10 |
| q0 | -5.285500000000e-01 |
| mu_E eV | 2.221734568217e+04 |


The reference retains q0=-0.528550000, local rotation speed 207.510905127 km/s and conditional lens deflection 0.535586511 arcsec. The mass unit is 22217.345682174 eV. These are reproduction of validated benchmarks and internal calculations under disclosed inputs. A new independent prediction is not a prerequisite for completion.

Residual freedoms are shown by calculated controls. Rescaling zeta and kappa_h as below preserves Q_h. Separately fitting eta_R at lambda_R=0 and 1 reproduces the same five targets and reference q, yet changing K to 4 after calibration gives different results. Fitting reference products eta_s mu_s and determining the full response shape are separate achievements.


$$
\zeta\mapsto r\zeta,\qquad \kappa_h\mapsto\kappa_h/\sqrt r,\qquad \zeta\kappa_h^2\mapsto Q_h. \tag{12}
$$


| lambda_R | Reference q | K=4 q after fitting |
| --- | --- | --- |
| 0.0 | -0.528550000 | -0.547819855 |
| 1.0 | -0.528550000 | -0.548643149 |


Independence of the five anchors is checked using the logarithmic sensitivity of (C_G,ucrit,u_h,u_c,mu_E). The numerical rank is five conditional on frozen constitutive choices. This is local identification of the five calibration anchors, not identification of every model coefficient.


$$
\frac{\partial\log(C_G,u_{\mathrm{crit}},u_h,u_c,\mu_E)}{\partial\log(G,H_0,f_\varphi,f_c,E_e)}=\begin{pmatrix}-1&0&0&0&0\\-1&2&0&0&0\\-1&2&-f_\varphi/(1-f_\varphi)&0&0\\-1&2&0&1&0\\0&0&0&0&1\end{pmatrix}. \tag{13}
$$


Ten runs changing each anchor by ±1% are construction-sensitivity controls, not observational confidence intervals. Changed physical targets are explicitly recalibrated; address controls hold SI coefficients fixed. Electron energy changes the mass unit but not macroscopic density, q or rotation speed. Critical density varies inversely with G and quadratically with H0.

The fixed-reference homogeneous expansion uses the same pressureless/background energy relation. Noncommuting-carrier internal exchange at fixed volume sums to zero and preserves state positivity/normalization. The required conversion work and its environmental account retain the 0.10 conservation checks.


$$
\frac{H(a)^2}{H_0^2}=(f_\varphi+f_c)a^{-3}+f_b,\qquad \frac{du}{d\log a}+3(u+P)=0. \tag{14}
$$


## Falsifiers and reproduction

The connection must be revised if an earlier stage reads future targets, input order changes, energy-pressure differentiation or inherited benchmark reproduction fails, electron energy is duplicated, or unidentified W0, zeta or alpha_EM is used as determined. This release executes 28 checks plus 32 inherited 0.10 checks, including zero/sign modes, five-point pressure differentiation, log sensitivities, explicit degeneracy controls, conservation and invalid-input rejection.

```bash
python -m pip install -r calculations/wrra_m_0_11/requirements.txt
python calculations/wrra_m_0_11/run_release.py
```

Parameters.json contains inputs, units, provenance and constitutive choices. Sequential calibration, physical cases, mass modes and input responses are supplied as JSON/CSV. A clean copy with all captured results removed compares regenerated outputs and bilingual sources byte for byte. Word/PDF are final publications built from those sources, with equations/tables checked against execution and every rendered page inspected.

Input SHA256 67de28abf0741c406178a2fe4ce07962e69bce827c3196b78e887da3bd0dab13

## Completion and subsequent scope

Version 0.11 completes staged calibration of the five disclosed anchors and reporting of residual freedoms. Their origins, a unique universe solution and calibration-free constants are not completion requirements. Version 0.12 treats clocks/boundaries/spectra, 0.13 physical quantization/post-observation states/records, and later stages uncertainty, stress, curvature, size and neutrino connections. Unmeasured outputs produced after fixing the model and calibration are recorded as WRRA predictions with their inputs and falsifiers.

## References

Choi Wonsik. WRRA_M 0.10, frozen baseline commit 24707c512c3994f2b19a96d6f257ef7d1249dab3. https://github.com/Wonsik-Choi-janefather/wrra-m-0.1

Choi Wonsik. Minimal Computation Cosmology 2.3.2, chapter 23, frozen commit 21daec110c0cbecb228c445d587eac8302e7f767. https://github.com/Wonsik-Choi-janefather/minimal-computing-cosmology-2.3.2

Choi Wonsik. WRRA_M_Calibration_Candidates.xlsx, first-sheet reference; source hash in parameters.json.

Planck Collaboration. Planck 2018 results VI, A&A 641 A6 (2020). https://doi.org/10.1051/0004-6361/201833910

NIST. CODATA 2022 constants table. https://physics.nist.gov/cuu/pdf/wall_2022.pdf

Copyright 2026 Wonsik Choi. CC BY 4.0. https://creativecommons.org/licenses/by/4.0/
