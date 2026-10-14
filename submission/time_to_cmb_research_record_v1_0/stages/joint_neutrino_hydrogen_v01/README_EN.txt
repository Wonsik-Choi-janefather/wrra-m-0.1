Joint neutrino–hydrogen synchronization audit v0.1 — 14 October 2026

First audit: with all q,A,L and common phase-rate G free, the old leading
spectral model is non-identifiable: G->cG, q->q/sqrt(c), A->A/c,L->L/c
preserves the observables. A numerical profile verifies this degeneracy.
Thus concatenating the two datasets alone does not determine a universal clock.

Conditional anchored test: freeze the book q0=0.00172592928 eV
and an electron/alpha/reduced-mass energy scale A0=3288051231534945.500000 Hz.
Book q0 was historically calibrated to neutrino data. CODATA energy inputs
have correlations and include spectroscopy in their adjustment. No blind,
fully independent cross-domain prediction is claimed.

Adopted common-clock compatibility model: neutrino phase-equivalent splittings
G*q0^2*(25,816); hydrogen G*base_transition_frequency + ell*S_state_gap.
G is a phenomenological phase-rate compatibility parameter, not a derivation
of time or Planck's constant. The 2S-8D transition remains held out.

Tuning: add fixed leading one-loop self-energy with state-dependent Bethe
logarithms, using NIST formulas A41/A40 and reduced-mass factors. No coefficient
was fitted to the held-out line. A common residual S term remains calibrated.
This is an adopted physical module, not a derivation from the SOURCE grammar.

Results: held-out H residual 7.880336 -> 0.414264 MHz, a factor 19.023 improvement.
The gain is from the added atomic physics correction, not simply from joining data.
The new conditional G=0.999999994790629.
Neutrino centre residuals -0.705605%, -1.430381%, within published marginal errors.
Hydrogen anchor precision dominates the common G; neutrino data adds negligible
precision. G from H-only transfer and from joint training are practically identical.
H holdout remains outside experimental-summary errors: combined sigma about
5580.847 Hz, and theory truncation is unquantified.

Computed time markers: neutrino first full Pee minimum at 1 MeV
1.680176273 microseconds; atomic phase cycle
1.297606656000 femtoseconds. Not directly observed timestamps;
atomic phase period is not excitation waiting time, duration or level lifetime.

Scope: fixed Q0, fixed input constants, asymmetric summary errors and zero
cross-covariance. Reported conditional G error excludes anchor uncertainty,
CODATA covariance and missing atomic theory. G may absorb omitted theory terms.
Full QED/recoil/finite-size calculations and SOURCE-to-atom address derivation
remain open. No unique universal arithmetic clock or event identity established.
The MCC book and previous separate archives are unchanged.

Run python reproduce.py; numpy, scipy, matplotlib required. Source modules,
frozen inputs, output JSON, CSV and a plot are included.

Sources:
https://arxiv.org/abs/2312.12907
https://arxiv.org/abs/2211.14988
https://arxiv.org/abs/1107.3101
https://arxiv.org/pdf/1801.08816
https://arxiv.org/abs/2111.08554
https://physics.nist.gov/cuu/pdf/all.pdf
https://pml.nist.gov/cuu/pdf/RevModPhys_80_000633acc.pdf
