MCC neutrino synchronization — revision v0.2, 14 October 2026

Fixed integer modes: (0,5,29); mass-energy spectrum q*n; normal ordering, m1=0.
Squared differences: (25,841,816); fixed dm32^2/dm21^2=32.64.
Primary inputs: Solar+KamLAND 2024, 7.50(+0.19/-0.18)e-5 eV^2;
Daya Bay final 2023, 2.466(+/-0.060)e-3 eV^2. Known mixing weights adopted.

Revision: replace the main evolution's separate anchors with ONE common q,
jointly calibrated using asymmetric published marginal errors and zero
cross-covariance. Preserve separate-anchor cross-checks from v0.1.
Joint calibration is not independent validation. No integer refitting.
q=1.735336791 meV.
Conditional delta-chi2=1 interval: 1.720295418–1.750496719 meV.
Predicted solar/atmospheric splittings: 7.528484444e-05, 0.002457297322 eV^2.
Central residuals: +0.37979%, -0.35291%; each within marginal one-sigma errors.

Adopted physical evolution: coherent vacuum propagation at equal momentum,
H_i=sqrt(E^2+m_i^2)-E (rest energies m_i in eV), SI hbar.
At pc=1 MeV the first full Pee local minimum is 1.662008688 microseconds.
Conditional q-only interval: 1.633346161–1.691199234 microseconds.
These are calculated times, not directly observed event timestamps. Fixed
mixing, vacuum assumption, source spectrum and detector response restrict the scope.

Long-window maximum absolute probability residual to the calculated
published-parameter reference improves from 0.060212 (solar anchor) to
0.036694 (joint calibration). It does not vanish. The pointwise q envelope is
NOT a simultaneous confidence band and does not contain the entire reference.
At sample points, inclusion fractions are 98.161% (fast), 82.236% (slow).
The reference is a calculation, not raw event data.

The measured central splitting ratio is 32.88 vs fixed 32.64. A common q
cannot exactly match both centres. Exact matching with n2=5 would require
an effective n3=29.103264422 in the mass mapping. This is a diagnostic,
not an adopted change to the integer model. No new deformation parameter is
introduced merely to remove a discrepancy compatible with present errors.
The four PDG fit checks overlap in their input experiments and are sensitivity
checks, not four independent replications.

Checks: probability, initial state, units, phase limit, energy scaling,
profile-time ordering, numerical minimizer vs closed weighted solution.
Conditional correspondence remains compatible with parameter summaries;
event identity, uniqueness, a universal clock map and the 50-second FRB event
are not established by this computation.

Run python reproduce.py; dependencies numpy, scipy, matplotlib.
All inputs, CSVs, results and plot are included.
Sources:
https://arxiv.org/abs/2312.12907
https://arxiv.org/abs/2211.14988
https://pdg.lbl.gov/2026/reviews/rpp2026-rev-neutrino-mixing.pdf
https://www.bipm.org/en/publications/si-brochure
