WRRA Finite-Gradient Matching v0.4 - working calculation, 20 October 2026
Authors: Wonsik Choi and Jeongin Choi, independent researchers.

Run: python run_checks.py
Numerical requirements: Python 3.12, numpy==2.3.5, scipy==1.17.0
Report rebuild: python make_reports.py (also matplotlib, pandoc, xelatex and Noto Sans CJK KR)

Inputs are frozen v0.3 dynamics_results.json and quantized_seed.npz.
No CAMB runtime or network is required for numerical reproduction.
The rate perturbation response is normalized to one; actual small WRRA seed
amplitudes are then applied in Fourier space. This is linear-amplitude finite-k
evolution of a declared effective reservoir, photon-like perfect radiation,
massless collisionless neutrinos and generated pressureless matter.
It does not compute particle reactions, detailed thermal history or new CMB spectra.

finite_gradient.py: scaled-shear metric and rescaled neutrino hierarchy.
independent_metric.py: independently integrated trace metric, raw hierarchy.
run_checks.py: named tests, all 64 physical modes, seven diagnostic comparisons,
actual seed application, matching, convergence, and three rejecting controls.
results/audit.json: all checks and scope; previous v0.3 checks are not recounted.
results/matching_states.json: per-unit response before/after matching.
Unqualified theta fields use dimensionless conformal-time units; fields ending
_Mpc_inverse provide physical inverse-Mpc velocity-divergence responses.
all_64_transition_responses.npz stores the pre-match internal unit-response state.
actual_128_cell_matched_fields.npz stores actual seed-applied post-match fields.
Curvature and entropy diagnostics at matching are post-exchange quantities.

New original material: CC BY 4.0. Source field equations cited in both reports.
No new Zenodo/GitHub release is asserted by this local working package.
