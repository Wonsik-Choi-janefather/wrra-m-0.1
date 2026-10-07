# Minimal Computing Cosmology 3.0 — Dataset Index

This folder is the public dataset index for MCC 3.0. It does not duplicate the stage outputs; it points to the machine-readable source-of-truth files committed with each stage.

## Core release data

- Release manifest: [../RELEASE_MANIFEST.json](../RELEASE_MANIFEST.json)
- Final claim ledger: [../FINAL_CLAIM_LEDGER.md](../FINAL_CLAIM_LEDGER.md)
- Verification-data policy: [../VERIFICATION_DATA_POLICY.md](../VERIFICATION_DATA_POLICY.md)
- Single replay entry point: [../reproduce_mcc_3_0.py](../reproduce_mcc_3_0.py)

## Stage datasets

### Stage 1 — Baseline freeze
- [Baseline manifest](../stage_1_baseline_freeze/baseline_manifest.json)
- [Verification data](../stage_1_baseline_freeze/results/verification.json)

### Stage 2 — Finite SOURCE insertion
- [Results](../stage_2_finite_source_insertion/results/results.json)
- [Verification](../stage_2_finite_source_insertion/results/verification.json)
- [Candidate parameter patch](../stage_2_finite_source_insertion/results/candidate_patch.json)

### Stage 3 — Particle/component replay
- [Input manifest](../stage_3_particle_component_replay/inputs_manifest.json)
- [Results](../stage_3_particle_component_replay/results/results.json)
- [Verification](../stage_3_particle_component_replay/results/verification.json)

### Stage 4 — Single load/energy Master Ledger
- [Input manifest](../stage_4_single_load_energy_master_ledger/inputs_manifest.json)
- [Results](../stage_4_single_load_energy_master_ledger/results/results.json)
- [Verification](../stage_4_single_load_energy_master_ledger/results/verification.json)
- [Master sector ledger CSV](../stage_4_single_load_energy_master_ledger/results/master_sector_ledger.csv)
- [Component energy ledger CSV](../stage_4_single_load_energy_master_ledger/results/component_energy_ledger.csv)
- [Field/channel energy ledger CSV](../stage_4_single_load_energy_master_ledger/results/field_channel_energy_ledger.csv)

### Stage 5 — Macro-universe replay
- [Input manifest](../stage_5_macro_universe_replay/inputs_manifest.json)
- [Results](../stage_5_macro_universe_replay/results/results.json)
- [Verification](../stage_5_macro_universe_replay/results/verification.json)

### Stage 6 — End-to-end closure
- [End-to-end audit](../stage_6_end_to_end_closure/results/end_to_end_audit.json)
- [Verification](../stage_6_end_to_end_closure/results/verification.json)

## Headline finite-source output

[
N_U = 1,015,000
]

Integrated status: six-stage computational closure **PASS**; scientific model **PASS-C**.

The 65 declared checks are implementation, numerical, ledger and provenance checks; they are not 65 independent physical experiments.
