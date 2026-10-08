# Minimal Computing Cosmology 3.0

**Development status:** Stage 6 complete / MCC 3.0 integration closed.

MCC 3.0 integrates the frozen Minimal Computing Cosmology 2.3.2 corpus, the WRRA_M 1.0 executable physical model, and the finite Klein–Zeta SOURCE candidate into one end-to-end finite calculation.

Target execution chain:

```
finite generator
→ finite integer addresses
→ filter / residue
→ component / particle / phenotype
→ information load
→ SI energy and pressure
→ gravity / rotation / lensing
→ cosmic expansion
```

## Development stages

1. **Baseline freeze — COMPLETE**
2. **Finite SOURCE insertion — COMPLETE**
3. **Particle/component replay — COMPLETE (PASS-C)**
4. **Single load/energy Master Ledger — COMPLETE**
5. **Macro-universe replay — COMPLETE**
6. **End-to-end closure and MCC 3.0 release — COMPLETE (PASS; integrated model PASS-C)**

See `stage_1_baseline_freeze/` for the frozen provenance ledger and Stage-2 contract.


## Current handoff

Stage 2 is complete. See `stage_2_finite_source_insertion/` for the executable insertion wrapper, candidate parameter patch, verified results, and Stage-3 handoff.


## Verification data

Every stage publishes machine-readable verification evidence under the repository-wide [verification-data policy](VERIFICATION_DATA_POLICY.md). Stage 1–3 verification JSON files are committed with their stage results.

Stage 3: `stage_3_particle_component_replay/` — finite-SOURCE component, charge and color replay; spin/binding and unique species decoding remain OPEN.

Stage 4: `stage_4_single_load_energy_master_ledger/` — finite component/field views are nested inside the existing phenotype energy budget; the cosmic additive ledger remains phenotype + resident nonphenotype + return only.

Stage 5: `stage_5_macro_universe_replay/` — finite-SOURCE energy/pressure is propagated through the frozen homogeneous expansion and the same local gravity renderer for rotation and conditional lensing, with full verification deltas against the legacy branch.

Stage 6: `stage_6_end_to_end_closure/` — cross-stage audit, final verification ledger and end-to-end closure. Single replay entry point: `reproduce_mcc_3_0.py`.

Final claim status: see `FINAL_CLAIM_LEDGER.md` and `RELEASE_MANIFEST.json`. The six-stage integration is complete; the finite-SOURCE product law and selected microscopic particle claims remain conditional/open.


## Cumulative integrated book v0.4

- [Bilingual book edition (Korean / English)](book_v0_4/README.md)
- GitBook English: https://independent-research.gitbook.io/minimal-computing-cosmology-3.0/
- GitBook Korean: https://independent-research.gitbook.io/minimal-computing-cosmology-3.0/korean-edition/

## Public dataset and release documents

- Dataset index: `dataset/README.md`
- Machine-readable dataset index: `dataset/DATASET_INDEX.json`
- Integrated manuscripts and generated PDF/Word editions: `paper/`


## Zenodo

- MCC 3.0 DOI: https://doi.org/10.5281/zenodo.23202732

## Theory-completion follow-up — reviewed Step 1

- [SOURCE capacity: Korean and English reports, replay code and verification data](theory_completion/step_1_source_capacity/README.md)
- Reviewed on 8 October 2026. Conditional finite-SOURCE construction and capacity transport pass in the declared uniform/conditional local branch; the three probes use frozen filter and SI coefficients.
- This follow-up uses its own step numbering and does not rename the historical six integration stages.


## Theory improvement — Step 2 / 이론 보완 2단계

[Reviewed Step 2 package](theory_completion/step_2_address_readout/README.txt) · [한국어 검토](theory_completion/step_2_address_readout/STEP2_REVIEW_KO.txt) · [English review](theory_completion/step_2_address_readout/STEP2_REVIEW_EN.txt)

Structural arithmetic readout and its existing ledger connections: 52 computational contract checks. Scoped Stage-2 completion does not assert full theory completion.

## Theory improvement — Step 3 / 이론 보완 3단계

[Reviewed Step 3 package](theory_completion/step_3_structure_selection/README.txt) · [한국어 검토](theory_completion/step_3_structure_selection/STEP3_REVIEW_KO.txt) · [English review](theory_completion/step_3_structure_selection/STEP3_REVIEW_EN.txt)

Structure comparison, scoped minimum-state proof, equivalent rotation kernel and existing ledger integration: 38 checks passed after re-review. The full fixed four-mode spectral continuation requires eight real autonomous LTI states; the bound is not established for arbitrary implementations matching only eight admission samples; four modes and eight admission frames remain constitutive specifications. Scoped Step-3 completion does not assert universal physical minimality or full theory completion.

## Theory improvement — Step 4 / 이론 보완 4단계

[Reviewed Step 4](theory_completion/step_4_carrier_phenotype/README.txt) · [한국어 검토](theory_completion/step_4_carrier_phenotype/STEP4_REVIEW_KO.txt) · [English review](theory_completion/step_4_carrier_phenotype/STEP4_REVIEW_EN.txt)

Carrier response, calibrated selection, phenotype routing, internal mixing and finite record budgets: 51 connection checks plus 38 inherited internal checks. The joint calibrated branch requires a disclosed supplier of at least 31.82783539785394% of its phenotype allocation; baseline 20% rejects it. Branches are alternatives, not additive cosmic sectors. This completes the scoped connection review, not all species mass/mixing or full theory.

Step 3 re-review: [한국어](theory_completion/step_3_structure_selection/REREVIEW_KO.txt) · [English](theory_completion/step_3_structure_selection/REREVIEW_EN.txt). The added scope audit distinguishes continuation-based Hankel bounds from finite admission observations.

## Theory improvement — Step 5 / 이론 보완 5단계

[Reviewed Step 5](theory_completion/step_5_state_physical_load/README.txt) · [한국어](theory_completion/step_5_state_physical_load/STEP5_REVIEW_KO.txt) · [English](theory_completion/step_5_state_physical_load/STEP5_REVIEW_EN.txt)

Conditional address/carrier states to positive physical loads, same-energy pressure and nested record/supplier budgets: 23 checks and 36 combined cases. Frozen dependencies verified by SHA256. Constitutive operators, volume laws and calibrated SI inputs remain explicit; this is scoped connection completion, not full theory completion.

## Theory improvement — Step 6 / 이론 보완 6단계

[Reviewed Step 6](theory_completion/step_6_shared_gravity/README.txt) · [한국어](theory_completion/step_6_shared_gravity/STEP6_REVIEW_KO.txt) · [English](theory_completion/step_6_shared_gravity/STEP6_REVIEW_EN.txt)

Shared frozen density/pressure state feeds rotation, conditional lensing and homogeneous expansion: 20 checks, 12 states and 36 record/supplier boundaries. Independent lens quadrature and analytic zero-clustering projection agree. Known-value reproduction and scoped connection completion; no new observational fit or full covariant gravity derivation is asserted.
