MCC 3.0: Muon–Tau Decay Event/Time Synchronization Audit v0.1
Research context: Wonsik Choi and Jeongin Choi. Date: 2026-10-14.

Run: python reproduce.py (Python 3, numpy, matplotlib).
All inputs are frozen; no network access is required for reproduction.

Validation input
The measured muon mean lifetime calibrates one weak-rate normalization. Electron,
muon, tau and W masses are adopted external inputs. Tau lifetime and branching
fractions provide observed partial rates B_l/t_tau. They do not calibrate the
primary muon-to-tau transfer. Sources and uncertainties are in frozen_inputs.json.

Architectural transformation / adopted physics
The finite event ledger follows the book's positive decay transitions and daughter
cohort accounting. The m^5 weak-decay law, massive final-state phase space and
leading W-propagator correction are adopted physics, not derived from SOURCE.
The universal fixed-alpha, massless first-order QED factor cancels in the ratio.
Channel-specific finite-mass and higher-order radiative terms are not implemented.

A chosen N_mu=2^k resolution defines dt=t_mu/N_mu. For competing rates, exact
per-tick probabilities are p_i=(Gamma_i/Gamma_total)*(1-exp(-Gamma_total*dt)).
This resolution is an operational convention, not a predicted fundamental tick.
Both expected cohorts and seeded integer cohorts are tracked. One leptonic cohort
contains one charged daughter and two neutrino daughters. Total parent-frame energy
is carried into each complete daughter cohort; individual spectra and momentum
are not simulated. Conserved cohort identities are not conserved particle number.

Output
Electron channel: predicted 6.1265152383e11 s^-1 versus 6.1488115742e11 s^-1;
relative difference -0.362612%, marginal measurement/input residual -1.27790 sigma.
Muon channel: predicted 5.9584387804e11 s^-1 versus 5.9834653806e11 s^-1;
relative difference -0.418263%, marginal residual -1.44880 sigma.
Theory truncation is excluded from those diagnostics. Input-summary correlations
are approximated as zero. No fabricated HFLAV covariance or joint significance is
used; ALEPH and L3 comparisons include their published branch correlations.
These older datasets contribute to the averages and are not extra independent tests.

Inverse partial rates (1.632249 and 1.678292 ps) differ from the total tau lifetime
(0.2903 ps). Unmodelled hadronic/other rates are closed with the measured total
lifetime for the full ledger simulation. That survival curve is conditional, not
an independent total-lifetime prediction.

Separate additional calibration to the tau electron channel gives a normalization
multiplier 1.0036393178. The remaining muon channel then has a -0.0558531% residual.
This secondary calibration is clearly separated from the primary transfer.

Positive probabilities, probability conservation, integer-cohort accounting and
aggregate energy conservation pass. Exact finite propagation agrees with the
analytic survival curve to about 3.2e-15. First-order Euler error decreases with
resolution. Actual rounded elapsed times are recorded for every resolution.

Cross-domain link
prior_time_anchor.json records the prior conditional neutrino/hydrogen G and time
observables. Under an assumed common multiplicative G for rates, calibration to
the muon absorbs G. Numerical rescaling checks confirm the cancellation; this
test does not independently constrain a universal clock. Atomic phase periods,
flavour-oscillation minima and decay lifetimes remain distinct observables.
Known hbar converts rates into widths; it is adopted, not derived.

Falsification
Failure means inconsistent frozen tau partial rates beyond measurement uncertainty
and the declared truncation, negative residual hazards/probabilities, lost or
double-counted cohorts/energy, or failed resolution convergence. The small common
deficit motivates precision radiative/input checks, not a claim of new physics.
A SOURCE-derived event map and a nondegenerate constraint are still needed to
establish arithmetic/physical event identity or a unique fundamental time scale.

Conclusion
Muon-anchored operational rate/time transfer is compatible at this approximation
level and can run in a finite positive ledger. It is a conditional implementation
and cross-check with an adopted weak-interaction module, not a new derivation of it.

Sources
PDG 2026 muon, tau and W listings; PDG tau branching-fraction review; NIST CODATA
2022 constants; A. Pich, Precision Tau Physics, arXiv:1310.7922, equations (2)-(4).
Exact URLs, frozen values and assumptions are in frozen_inputs.json.
