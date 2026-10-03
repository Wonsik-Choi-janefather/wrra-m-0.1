# WRRA_M upstream 0.10 - integrated finite generator and handoff ledger

Wonsik Choi · 2026-10-03 · ORCID 0009-0001-4263-9772 · CC BY 4.0

| Evaluation | Execution evidence |
|---|---|
| Verification inputs | SOURCE/filter 0.7, microscopic branch records 0.8-r1, preparation/current bridge 0.9 and reviewed nucleon currents 0.6-r1. Inputs and calibration coefficients are frozen. |
| WRRA-specific transformation | SOURCE → relation amplitudes → ordered filters → residue/return → conditional record → internal density → same-state electromagnetic/weak currents and finite stock updates. |
| Outputs | Six SOURCE cases, baseline 5%/26.8%/68.2%, inherited 0.9 current outputs; 156 implementation and 309 independent checks pass. |
| Falsification conditions | Failed inherited-input identity, positivity, trace/stock conservation, record ownership, same-H energy/current/CVC agreement or reproducibility. An adopted physical map remains revisable on observational contradiction. |

**Upstream development ends at 0.10.** Uncomputed interfaces remain in this closure ledger and do not create additional development stages. A possible 1.0 edition only reviews, consolidates and freezes the work through 0.10.

A single `reproduce_all.py` run computes the actual million-address branch vectors, rather than relabeling parent result numbers. Archived results provide regression comparisons; hashes identify the inherited code/inputs/results. The pipeline directly passes the selected phi address vector to the 0.9 preparation function and verifies its agreement with the phi-conditional ensemble state.

The six cases include baseline, p2 and p3 log intensities ±0.15 and p3 phase 0.7 rad. N=1,000,000, alpha=1.8996876950554356, beta=0.8654570124136961 and the 0.9 lambda=0.2/selector-prime-3/mode-1 constitutive rules stay fixed. Source p2 changes branch volumes; p3 intensity also changes internal state/current readout. Phase-only invariance is specific to the declared diagonal preparation map, not a universal absence of phase physics.

Four supplied draws 0.02/0.1/0.32/0.9 test single branch labels and normalized conditional vectors. Their counts do not estimate cosmic fractions. D and return branches own no nucleon readout; only phi receives that readout. Each draw is a separate prepared-state diagnostic. The scalar stock calculation is expected branch accounting, not a sampled microscopic particle trajectory.

The reference generation window releases all initial SOURCE stock once and then closes for seven finite updates. It retains SOURCE/phi/D=68.2%/5%/26.8%. The separate u=0.2,32-event recycling control yields Actual=87.7886139621%; every finite stock sum remains one. Independent scalar recurrence and a_k=1-(1-u*r)^k agree. Thus 31.8% is conditional on the declared closed window, not an automatic recycling fixed point. No realized infinity or infinite iteration is needed; infinity=Null remains the adopted premise.

Baseline conditional excess energy=34.4764357391 MeV, GE(proton,0.1)=0.730176766651 and GA(0.1)=0.897125841478 match 0.9. State energy uses the same frozen H, and electromagnetic/weak currents use the same sigma. These are conditional readouts, not creation rest masses or cosmic energy densities. Information fractions are not directly converted to energy fractions.

Energy supply, physical seconds per update, species origin and record-medium stability remain null. Unsupported numerical values for the unimplemented time/energy maps are rejected. A downstream gravity/expansion simulator must supply its explicit state/energy map before claiming physical integration. The inherited neutron magnetic-radius mismatch 0.83198710743 versus 0.864 fm and finite-Q²/regulator/precision exclusions remain open.

Upstream 0.10 completes the declared finite conditional execution path. Upstream 1.0 is the review/freeze edition of these results and contracts; it does not silently add development stages or certify missing physical interfaces. WRRA Core 1.0 is unchanged. Calibration and reproduction of known values remain legitimate explanatory achievements; independent prediction and numerical novelty are not additional completion requirements.

Run `python reproduce_all.py` with Python 3, NumPy 2.x and SciPy. Audits cover 156 integrated and 309 independently formulated checks, plus byte-identical fresh-copy reproduction. Inherited reviewed 0.4-0.6 DOI: 10.5281/zenodo.23112253; no new 0.10 DOI has been issued.


## 2026-10-03 reviewed collection

This executable implementation is reviewed in [0.7-0.10-r1](../review_0_7_0_10_r1/README.md), DOI 10.5281/zenodo.23115550. Physical baseline outputs are preserved; input validation, clean reproduction and named/Q2-matched references are corrected. Historical PDFs remain available; consult the bilingual review report for the corrected implementation contract. Upstream development ends at 0.10.
