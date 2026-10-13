# Finite Energy-Conserving Frame Exchange and a Conditional Scalar Perturbation Bridge in WRRA

Wonsik Choi · v0.29 · 2026-10-13

DOI: https://doi.org/10.5281/zenodo.23328994

## Abstract

We present a reproducible finite-state toy model and a conditional effective-fluid completion. A finite excitation register supplies the exact source energy difference between carrier modes 8 and 72; an explicit unitary exchange preserves the joint energy, volume derivative and conjugated information observables. A separately prescribed spatial occupation perturbation is mapped using the arithmetic response derivative. For a vacuum-like component, its spatial gradient requires a momentum-transfer term. Including the declared transfer to dark dust closes a controlled scalar Einstein-fluid mode to approximately 1e-8 in common vacuum-source units, whereas omitting it produces an order-one violation. Earlier standard-completion CMB spectra reproduce familiar reference values under fixed inputs, but are not spectra of this new interacting mode. This report identifies what is calculated, what is assumed and what remains untested.

## 1. Definitions and scope

The construction uses 1,015,000 finite address labels, with one inactive address, and 128 load-balanced information-processing slots. These labels do not yet supply physical phase-space coordinates or local spatial cells. The model distinguishes internal finite-state response from physical frame readout. The intended scope is computational consistency and effective phenomenology, not a complete microscopic cosmology. Why 1,015,000? The interpretive premise does not grant our universe a privileged arithmetic size: in this particular construction the count is contingent. It is frozen for reproducibility, not inferred from observations or established as a uniquely derived constant. No probability law generating this count, or robustness across other counts, has yet been demonstrated.

## Terminology

Address: finite internal state label. Slot: carrier or information-processing unit. Shutter: finite-time averaging window. Frame: a declared readout state. Supply bit: finite excitation register with an explicit Hamiltonian. Energy ledger: accounting for the complete source and supply boundary. Only after a physical completion is declared does this become a candidate stress-energy conservation ledger. A finite-time window has a sinc response for frequency differences, but that fact alone proves neither removal of all UV divergences nor single-outcome quantum selection.

## 2. Finite exchange and volume response

The inherited source operator has eigenvalues A_k = 1 - cos(2 pi k/128). Modes 8 and 72 have the gap Delta A = A_72 - A_8 = 2 cos(pi/8). For each controlled address, q_n(a) = V0 [eta_D f_D(n) + eta_R a^3 f_R(n)]. The source Hamiltonian is H_n = eta_P V0 f_P(n) I + q_n A; the excitation register has H_B,n = q_n Delta A |1><1|. The controlled addresses are the existing complement of the n mod 3 = 0 preparation. The coefficients are eta = (7.5615824991e-10, 7.2857613288e-10, 7.6461028188e-10) J/m^3, with V0 = 1 m^3 and volume exponents nu = (0,0,3). Both address-size-weighted and unweighted branches are retained.

## Exact finite operation

The exchange swaps |8,B1,R0> with |72,B0,R1> and acts as the identity elsewhere. The logical record used here is energy-degenerate. It is not a previously defined energetic measurement pointer. The swap is a bijective unitary involution and commutes with the complete source-plus-register Hamiltonian for every declared volume. Therefore total energy and its volume derivative are preserved. Conjugating the complete information observable with the same unitary preserves its moments and finite-field partition function. The physical source-only readout A changes; it is not identical to the conjugated logical observable.

## Preparation and accounting

For E_s = eta_s V0 a^nu_s L_s, the physical density is u_s = E_s/(V0 a^3), and the fixed-load pressure is p_s = -nu_s u_s/3. A uniform excitation probability 1/2 restores the calibrated homogeneous source readout. A fixed Gibbs alternative has probability 1/(1+exp(1)) and gives a different background. Uniform preparation is consequently a model input, not an arithmetic uniqueness theorem. The weighted transferred energy at a=1 is 4.967352081978407e-10 J, split into 1.3321303783564441e-10 J for D and 3.6352217036219685e-10 J for R. This energy is already in the prepared finite register: the operation does not create total energy or raise the complete system Hubble rate.

## 3. Spatial derivative and conservation completion

Let M_C,s denote the actual arithmetic payload summed over controlled addresses. The source readout obeys dL_s/dp = Delta A M_C,s and du_s/dp = eta_s a^(nu_s-3) Delta A M_C,s. For a diagnostic occupation p(x)=1/2+epsilon cos(k.x), the calculation takes k=(0.05,0,0) Mpc^-1 and epsilon=1e-8. These spatial coordinates, scale and amplitude are supplied probe inputs, not derived primordial fluctuations. A local unitary exchange at fixed preparation cannot by itself create a new total density mode.

## Vacuum-like component

Adopting standard GR and T_R^(mu nu) = -u_R g^(mu nu) implies Q_R^nu = -nabla^nu u_R. We explicitly choose Q_D = -Q_R and Q_b = 0. Conservation fixes the total compensating transfer, but does not uniquely choose dark dust as its recipient. The fixed physical vacuum-density modulation gives delta p_R = -delta u_R and a spatial momentum transfer. A background value c_a^2 = dot(p)/dot(u) = 0 does not establish a rest-frame sound speed or justify dropping this pressure perturbation.

## 4. Controlled scalar mode

The test integrates a baryon-dust/dark-dust/vacuum subsystem from a=0.02 to a=1 in conformal Newtonian gauge, with zero anisotropic stress and psi=phi. Radiation and neutrinos are omitted only in this isolated late-epoch test. Write N=ln(a), Hc=aH/c and C_s=(3/2)Hc^2 Omega_s; comoving distances are in Mpc. The evolution equations are:

## Equations

phi_N = -phi + (C_b theta_b + C_D theta_D)/(k^2 Hc)
delta_b,N = -theta_b/Hc + 3 phi_N
delta_D,N = -theta_D/Hc + 3 phi_N
theta_b,N = -theta_b + k^2 phi/Hc
theta_D,N = -theta_D + k^2 [phi - delta u_R/u_D]/Hc

## Constraint and independent checks

Initial velocities and baryon contrast are zero; the dark contrast uses the arithmetic density derivative, and the initial metric solves the Einstein 00 constraint. Define S_R=C_R delta u_R/u_R and F=k^2 phi + 3 Hc(C_b theta_b+C_D theta_D)/k^2 + C_b delta_b + C_D delta_D + S_R. Including the transfer gives F_N+F=0. Omitting it gives F_N+F=3 S_R and F(a)=S_R(a)[1-(a_i/a)^3]. The spatial Einstein trace is checked separately: phi_NN+(4-1.5 Omega_m)phi_N+3 Omega_R phi = -S_R/Hc^2. DOP853 uses rtol=2e-11, component-specific absolute tolerances and a tighter-tolerance comparison. Finite differences check the ODEs independently; halving the amplitude checks linear scaling.

## 5. Results and meaning

The common-source residual is max|F| / max|S_R|, with the same denominator for positive and negative controls. It is not an observational sigma, probability or likelihood. The weighted and unweighted energy residuals are 9.9924e-9 and 1.03691e-8 with the transfer, compared with 0.999992 in both omission controls. Spatial-trace residuals are 3.49e-16 and 5.77e-16 with the transfer, and 1.0 without it. Relative tighter-tolerance differences are 1.38e-12 and 1.52e-12; amplitude scaling differences are 2.08e-12 and 2.03e-12. Maximum dust contrasts remain 1.81e-4 and 1.91e-4. The one-mode suite passes 26 checks, and a separate numerical/file/claim audit passes 28 checks. These counts test declared constructions and are not independent empirical confirmations.

## 6. Recorded cosmological reference calculation

The earlier homogeneous completion uses unmodified CAMB 2.0.4, standard GR, flatness, standard adiabatic perturbations and recombination. Its frozen external inputs include A_s=2.1e-9, n_s=0.9649, optical depth=0.0544, T_CMB=2.7255 K, neutrino mass=0.06 eV and N_eff=3.044. Photon and neutrino contributions are included separately. H0 is obtained from the frozen complete energy budget, not an optimizer. The weighted uniform-preparation case gives H0=67.4499 km/s/Mpc and TT peak multipoles (220,536,812); the unweighted case gives 66.9054 and (221,539,818). Fixed Gibbs controls give H0=56.4777 and 56.0236, with first peaks 236 and 237. These are informative known-value reproduction and preparation-sensitivity results.

## Observational limits

The new interacting scalar mode has not been inserted into full radiation, neutrino, recombination and CMB transfer calculations. Thus the displayed CMB spectra remain those of the earlier standard completion. Omega_total=1 is imposed by flatness, not predicted. D/H=2.44177424e-5 and helium mass fraction Y_He=0.245667206 come from inherited PRIMAT interpolation at omega_b=0.0223958068; the distinct helium nucleon fraction is Y_p=0.246998180. These are not a newly integrated nuclear network. Public Planck PR3 bin-centre comparisons use a diagonal diagnostic, not the official likelihood with windows, covariance and nuisance parameters. No official -2 ln L, model rejection, BAO covariance likelihood or blanket BBN agreement is claimed.

## 7. Reproducibility and falsification

The accompanying code, actual input arrays, positive/negative-control CSVs, raw C_l and D_l spectra, numerical ledgers and SHA-256 manifests specify the release. Run python single_mode.py followed by python review.py. The optional homogeneous reference rerun uses python frame_baseline/run.py with CAMB 2.0.4 and may require a Fortran compiler. Refutation conditions include a wrong arithmetic derivative, nonconservation with the declared transfer, nonconvergent integration, loss of linear scaling or failure of energy/pressure conservation. Remaining physical tasks are address-to-3D preparation, the primordial spectrum, an interaction action and micro-derived anisotropic stress. No arbitrary observational optimization was performed, but explicit physical completion assumptions remain.

## Conclusion

A finite source/register exchange and one conditional scalar fluid-gravity mode are conservation-complete within their declared boundaries. The missing-transfer control exposes why a spatially varying vacuum-like density cannot be inserted as an independently conserved constant-w component. The present contribution is a reproducible toy-model bridge and its limits; it does not establish a fully micro-derived CMB spectrum or an observationally accepted cosmology.

## References and computational assistance

Ma, C.-P. and Bertschinger, E. (1995), Astrophys. J. 455, 7-25; https://doi.org/10.1086/176550; arXiv:astro-ph/9506072.
CAMB 2.0.4 documentation: https://camb.readthedocs.io/en/stable/results.html and /bbn.html.
Planck PR3 public spectra: https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/cosmoparams/.
WRRA source framework: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1.
AI assistance was used for implementation, numerical auditing and language preparation. The audit is computational, not an independent peer review or publication recommendation.