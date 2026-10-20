WRRA finite emission v0.5, Wonsik Choi and Jeongin Choi, 20 October 2026.
Run python run_checks.py; numerical dependencies: numpy 2.3.5, scipy 1.17.0.
Rebuild reports: python make_reports.py (also matplotlib, pandoc, xelatex,
Noto Sans CJK KR). CC BY 4.0 for new original material.

Verified inputs -> WRRA transformation -> outputs -> falsification are given
in the Korean and English reports. Inputs retain the previous beta, Gamma,
pulse, time calibration and actual seed. N=256 and epsilon=0.01 are disclosed
closure parameters, not measured fundamental quantities. No amplitude refit.

emission.py: finite deterministic credit thresholds, exact event clock,
expanding local FLRW, recording heat, finite recording permission.
run_checks.py: independent event-root integration, smooth continuum solver,
packet/time refinement, actual 128 cells, seed-resolution study and rejecting
controls. results/audit.json contains all named checks and numerical outputs.
results/events.csv contains all baseline events. cells.json and
actual_seed_event_times.npz retain cell-level results and all event times.

q is a comoving radiation debit per reference cell, NOT constant physical
particle energy. Physical debit is q/a at the event. The accumulator is credit,
not additional stored energy. One record token consumes no extra energy beyond
the explicit heat split. Zero capacity pauses both emission and credit generation.
The pulse endpoint includes exact threshold equality; leftover credit is not
flushed. Capacity is fixed for the pulse; reopening a gate is not modeled.

Scope: local separate-universe event closure. No finite-k metric/momentum/
neutrino jump integration, quantum amplitudes, particle-specific rates or new
CMB spectra. Small seed and small packet limits must be resolved together.
Existing v0.4 remains frozen. No new public release asserted by this package.
