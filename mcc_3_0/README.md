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


## Public dataset and release documents

- Dataset index: `dataset/README.md`
- Machine-readable dataset index: `dataset/DATASET_INDEX.json`
- Integrated manuscripts and generated PDF/Word editions: `paper/`
