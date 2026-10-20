WRRA Full-State Junction Development v0.7-dev-r1

STATUS: PARTIAL DEVELOPMENT. Full-state CAMB injection has NOT been executed.

New calculations:
1. All 64 frozen v0.4 smooth-source states transformed to the CDM-comoving synchronous frame, including constraints and all retained neutrino moments.
2. Independent v0.5/v0.6 local thermal histories differentiated with exact event-time saltation on a common proper-time slice (k=0 only).
3. Packet-produced physical dark-matter density compared to the inherited late input and conversion fraction recalibrated.

These calculations are separate branches, not a completed finite-k packet-to-CMB chain. See results/full_state_gate.json for missing physical requirements. No new angular covariance model, CMB spectrum, nonlinear lensing or likelihood was computed. The prior releases are unchanged.

Reproduce: python -m pip install -r requirements.txt
python run_all.py
python revalidate_release.py

The scientific runs need no CAMB, external likelihood or network. PDF rebuilding optionally requires pandoc, xelatex and Noto Sans CJK KR, using python make_reports.py.

Contains inherited frozen seed/states and EOS scripts, new numerical scripts, audit, original and recalibrated results, and Korean/English development reports. Release DOI: 10.5281/zenodo.23492328.

R1 numerical correction: preserve hprime+6etaprime directly from scaled shear and gauge shift. Reconstructing this small combination from separately rounded derivatives causes up to 16.66% Bardeen-potential error; the stable formulation agrees under the gauge transform within 4.35e-12 relatively. Ten additional release checks, including an independent fixed-event-clock tangent and SI-unit density conversion, pass. See REVALIDATION.json.
