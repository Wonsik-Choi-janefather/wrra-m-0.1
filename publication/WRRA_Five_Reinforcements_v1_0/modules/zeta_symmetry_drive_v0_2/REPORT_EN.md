---
title: 'WRRA Zeta-to-Physics: Symmetry and Driven Dynamics'
subtitle: 'Branch-blind combining contract, positive drive and phase noise | v0.2'
author: 'Won sik Choi · Jeongin Choi'
date: '21 October 2026 | Executable conditional research model'
lang: en
---

**WRRA = Wonsik Reality-Renderer Architecture.** Preserve the preceding v0.1 calculations while specifying an objective for equal combining and a finite dynamical law executing the phases. Assessment proceeds through verified inputs, WRRA transformations, outputs, falsification conditions and conclusion.

## 1. Verified inputs

Fix the existing 70 positive zeta-zero heights, $N_U=1{,}015{,}000$, 935,155 selected addresses, CRT space $(213,65,77)$, two test preparations and the v0.1 physical calibration. Reuse $d=c\tau$, $\tau=1.481301966415863\times10^{-21}\,\mathrm{s}$ and $H_0=\hbar c|k|$. Previous code, results and Gram matrices are frozen with hashes.

Zero heights remain mathematical inputs. No new zero-list selection or refit of original sector payloads, cosmic composition, RAR or GR/CMB results is made. Physical time is assigned only to a driven register after spatial embedding. Prephenotypic SOURCE addresses and allocation slots are not retroactively assigned physical time.

## 2. WRRA transformation A: a precise combining objective

The earlier maximum-pass port adapted its coefficients to the preparation. Here declare **one pure combining port that treats all branches alike and does not retune coefficients to the preparation or zero contents**. This is an explicit branch-blind contract for the combiner, not a theorem derived from cosmological nonprivilege alone. Content-dependent coefficients can also transform covariantly under relabeling; this contract is stronger than ordinary relabeling covariance.

For normalized $b\in\mathbb C^{70}$, define the branch-contrast cost

$$\mathcal C(b)=\frac1C\sum_{j<k}|b_j-b_k|^2
=1-\frac{|\sum_jb_j|^2}{C},\qquad\|b\|=1.$$

The cost is nonnegative, and zero occurs only at $b=e^{i\theta}(1,\ldots,1)/\sqrt C$. Thus the unique minimum-contrast port in this contract is the original equal combination. Applying the same contract to preparation of the branch register yields $K_0=C^{-1}\sum_jD_j$.

This measures **differentiation of combining coefficients**, not energy in joules or universal computational cost. General permutation-invariant mixed or multiport detectors admit other solutions. Uniqueness here concerns a normalized single pure port and the stated contrast objective.

| Objective | Result |
|---|---|
| Maximize pass probability for a fixed preparation | Previous largest-eigenvalue Gram vector |
| Minimize contrast of a content-independent single port | Original equal vector |
| Minimize apparatus energy, spatial nonlocality or total computing cost | Separate unresolved optimization |

The maximum-pass vectors have normalized contrast costs 0.976105 and 0.999669 for the two fixed preparations. Improving counts and satisfying the branch-blind contract are different objectives. The original rule can be retained with an explicit purpose.

## 3. WRRA transformation B: a positive phase-driving Hamiltonian

On the spatial embedding define $\Lambda=\sum_{n\le N_U}\log n\,|Jn\rangle\langle Jn|$, and on the auxiliary register define $\Gamma=\operatorname{diag}(\gamma_1,\ldots,\gamma_C)$. Unused slots have $\Lambda=0$. Introduce the prescribed drive

$$B=\frac{\hbar}{\tau}\Gamma\otimes\Lambda,\qquad
U_0(t)=I_C\otimes e^{-iH_0t/\hbar},$$
$$V(t)=U_0(t)BU_0(t)^\dagger,\qquad
H_{\rm tot}(t)=I_C\otimes H_0+V(t).$$

Since $H_0,B,V(t)\ge0$, the total Hamiltonian is positive. The exact solution of the time-dependent Schrödinger equation is

$$U_{\rm tot}(t)=U_0(t)e^{-iBt/\hbar}.$$

At $t=\tau$, each branch becomes $e^{-iH_0\tau/\hbar}JD_j|\psi\rangle$. **One driven interval exactly executes the previous phase-plus-physical-propagation endpoint.** Zero heights need not be equated with free-particle energies.

The control factorizes into one auxiliary/address product, $\Gamma\otimes\Lambda$. One is minimal among nonzero separable coupling-term counts. This is not a minimum circuit-gate count or proof of least-cost local hardware. The spatial rotation in $V(t)$ is generally nonlocal and requires prescribed clock/control. Autonomous apparatus and local field generation are not completed by this construction.

## 4. Executed dynamics and energy ownership

Both inherited pass probabilities, 0.014262842604 / 0.004494840216, and all-port mean energies are reproduced. Separately integrate the differential equation on a 3-branch, 11-address register without using the exact propagator in the integrator. Maximum state error is $2.71\times10^{-12}$; the work integral differs from the free-energy change by $4.00\times10^{-14}$ in dimensionless units.

For this drive $\langle V(t)\rangle=\langle B\rangle$ is constant. Ideal switch-on and switch-off energies are $+\langle B\rangle$ and $-\langle B\rangle$. Work supplied during the interval satisfies

$$\int_0^\tau\langle\partial_tV\rangle\,dt
=\Delta\langle H_0\rangle=W_{\rm phase}.$$

| Energy term | Uniform | Inherited alpha |
|---|---:|---:|
| Mean control potential during drive (MeV) | 624.490653 | 147.863326 |
| Within-interval mean work (keV/trial) | 1192.747800 | 7.444499 |
| Final all-port mean energy (keV/trial) | 1339.541271 | 1340.242336 |

Equal recovery at switching is an ideal bookkeeping property of this reference drive, not proof of perfect practical recovery or zero reset cost. The control potential is not a particle mass. Its large scale prevents identifying this implementation as universally energy-minimal.

The same endpoint phases can be generated with positive wrapped values $\gamma_j\log n\bmod2\pi$, bounded by $2\pi\hbar/\tau$. However, on the 70 branches and just 12 actual selected addresses, the unwrapped coefficient matrix has rank 1 and the wrapped matrix has rank 12. The full wrapped coupling therefore has separation rank at least 12. **Shared-coupling simplicity and generator energy scale present a concrete tradeoff.** The unwrapped generator is not declared optimal under every resource objective.

## 5. Executed phase-noise response

Declare independent, zero-mean Gaussian branch phase errors of standard deviation $s$ radians. This new noise parameter specifies a test condition, rather than an observational fit. Off-diagonal coherence is multiplied by $\eta=e^{-s^2}$. If $\rho_0$ is the original subnormalized selected output and $\rho_{\rm mix}$ the normalized incoherent branch mixture, then

$$\rho_{\rm out}(s)=\eta\rho_0+\frac{1-\eta}{C}\rho_{\rm mix},\qquad
P(s)=\eta P(0)+\frac{1-\eta}{C}.$$

This predicts the response of the same defined instrument. Apply the subnormalized state rule to band probability, energy and directional distributions before conditional normalization. A separate exact enumeration of discrete independent phase errors verifies the same density-matrix law for its matching coherence factor.

| Selected-port probability | Uniform | Inherited alpha |
|---|---:|---:|
| No phase error | 0.014262843 | 0.004494840 |
| Complete branch dephasing | 0.014285714 | 0.014285714 |

In particular, counts can increase when the inherited-alpha interference is destroyed. Maximizing throughput does not ensure retention of the original interference readout. This supplies a reason to measure distributions together with counts. Known interference/noise mathematics is executed inside WRRA's fixed address-to-physics construction.

\Needspace{18\baselineskip}
![](drive_and_noise.png){width=100%}

*Left: selected-port probabilities at sampled times of the exact post-embedding drive; the line connects those samples. Right: response to independent phase errors. Both panels are fixed-model calculations, not device measurements.*

## 6. Falsification conditions

1. A different normalized zero-contrast pure port satisfying the declared branch-blind contract would invalidate the symmetry argument. Different objectives outside that contract must not be confused with counterexamples.
2. Disagreement of direct integration with the stated exact solution or original endpoint, or loss of positivity, probability or work ownership, requires revision of the drive implementation.
3. In a device with fixed preparation, calibration and detection, independently distributed phase errors following the declared law must jointly reproduce probability, energy and directional responses. Otherwise revise this noise connection. Statistical significance and tolerances cannot be assigned before measurement data exist.

## 7. Assessment and remaining connections

The main calculation passes 79 checks, and separate verification passes 26. These are internal numerical checks, not independent observational confirmations. **A precise equal-combining objective, a positive finite drive executing the inherited phases, and a phase-noise response are now connected by actual WRRA calculations.** Quantum mechanics supplies established mathematics; the result is executed on this address model rather than asserted through citation alone.

Open tasks are an autonomous/local controller including its clock, full resource comparison of wrapped and unwrapped generators, record recovery/reset, original sector-specific SOURCE linkage and species-specific physics. The symmetry-port argument does not replace a physical selection principle for the zero list. Neither RH nor a unique particle spectrum is claimed.

Sources: MCC 3.0 v0.27-r1, Chapters 130–134, https://doi.org/10.5281/zenodo.23516661 ; preceding zeta physical readout v0.1. Mathematical definition background: NIST DLMF §25.2, https://dlmf.nist.gov/25.2 . Code, input hashes, CSV/JSON and bilingual reports are included. This research package is not yet registered as a new GitHub, GitBook or Zenodo edition.
