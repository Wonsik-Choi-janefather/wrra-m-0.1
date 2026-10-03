# WRRA_M upstream 0.8-r1: finite shutter and conditional records

Wonsik Choi · 2026-10-03 · ORCID 0009-0001-4263-9772 · CC BY 4.0

| Evaluation | Evidence |
|---|---|
| Verification inputs | Frozen upstream 0.7 SOURCE and ordered filter code, N=1,000,000, alpha=1.8996876950554356, beta=0.8654570124136961; calibrated 5%/26.8%/68.2% ledger. |
| WRRA-specific transformation | Prime SOURCE amplitudes → microscopic filter branch vectors → finite shutter/readout → one conditional branch record and normalized address state. |
| Outputs | Baseline fractions retained; 28 microscopic bridge checks and 403 reproducible shutter audit checks pass. Coarse full-shutter purity 0.539448. |
| Falsification conditions | Failed positivity, norm/trace conservation, branch completeness, deterministic replay or normalized single-record ownership. Physical timing agreement becomes testable after an explicit time map is supplied. |

`address_bridge.py` directly imports upstream 0.7 functions. It calculates K_j psi and their squared norms on the million-address support. Initial reflection and normal return remain separate outcomes; their probabilities are combined only in the classical return ledger. A selected microscopic state is normalized by its own branch probability. No coherent sum of the distinct return outcomes is substituted for their mixture.

`compute.py` separately defines the declared three-label test state rho=|sqrt(p)><sqrt(p)|. This is a new conditional coherence test, not a derived reduction of the million-address state. Its shutter S_eta(rho)=(1-eta)rho+eta diag(rho) is a convex combination of completely positive trace-preserving maps. Composition uses eta_eff=eta1+eta2-eta1*eta2; the full shutter is idempotent. Label probabilities remain fixed while off-diagonal coherence decreases. An imposed 0.25-radian label rotation followed by readout gives phi=0.784598233%; reversing the order gives 6.334350075%. Those are construction outputs, not measured cosmic fractions.

A supplied draw in [0,1) selects exactly one conditional record. The model does not derive that draw's physical origin. A frame is the finite preparation/filter/shutter/record order; its minimum readout unit is one branch record. Physical seconds per frame, universal minimum physical time, energy mapping and physical record-medium stability remain open/null. No realized infinity is required; infinity=Null remains the adopted ontology.

Known-value calibration and reproduction are retained as legitimate construction and explanatory achievements. Independent predictions or numerical novelty are not additional completion requirements. Stage 0.8 closes this conditional finite execution contract; upstream 0.9 connects the residual address state to the frozen 0.6 particle/current readout, and 0.10 integrates the generator.

Run `python reproduce_all.py` with Python 3 and NumPy. `results.json`, `audit.json`, and `handoff.json` are deterministic calculation outputs. The handoff owns the microscopic state contract and explicitly preserves unresolved physical interfaces.


## 2026-10-03 reviewed collection

This executable implementation is reviewed in [0.7-0.10-r1](../review_0_7_0_10_r1/README.md), DOI 10.5281/zenodo.23115550. Physical baseline outputs are preserved; input validation, clean reproduction and named/Q2-matched references are corrected. Historical PDFs remain available; consult the bilingual review report for the corrected implementation contract. Upstream development ends at 0.10.
