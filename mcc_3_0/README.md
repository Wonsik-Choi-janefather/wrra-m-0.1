# Minimal Computing Cosmology 3.0

**Development status:** Stage 3 complete / 6 planned stages.

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
4. Single load/energy Master Ledger
5. Macro-universe replay
6. End-to-end closure and MCC 3.0 release

See `stage_1_baseline_freeze/` for the frozen provenance ledger and Stage-2 contract.


## Current handoff

Stage 2 is complete. See `stage_2_finite_source_insertion/` for the executable insertion wrapper, candidate parameter patch, verified results, and Stage-3 handoff.


## Verification data

Every stage publishes machine-readable verification evidence under the repository-wide [verification-data policy](VERIFICATION_DATA_POLICY.md). Stage 1–3 verification JSON files are committed with their stage results.

Stage 3: `stage_3_particle_component_replay/` — finite-SOURCE component, charge and color replay; spin/binding and unique species decoding remain OPEN.
