# WRRA source/carrier action v0.1

**Wonsik Reality-Renderer Architecture**. Task 2: a conditional finite dynamical/variational completion, grounded in the registered finite SOURCE-supplier-record swap and common carrier.

## Existing material checked first

- MCC 3.0 v0.27-r1: common-carrier definitions and the rank-one failure (Chapter 6); conditional transport (112/117); finite preparation and remaining dynamics (120).
- Finite frame spatial bridge v0.29.1: original 512-state SOURCE-mode/supplier/record permutation and resonant resource ledger. Its original `frame_baseline/run.py` and `finite_registers.npz` are frozen under `inputs/`.
- source_shutter_bridge_v02: original common spectral transport and residue-owned SOURCE-to-supply mapping.
- finite_scale_bridge_v0_1: frozen original payloads used without new fitting.

## New executed work

1. Construct K = pi (I-G)/2 from the registered involutory gate G. Under the fixed nonnegative generator convention, this is its minimum squared-norm Hermitian logarithm. It reproduces G exactly at one prescribed interval.
2. Derive finite Schrödinger equations from a constrained quadratic action.
3. Execute a NEW candidate coupling w(x)=I_SOURCE(x)/mean(I_SOURCE), multiplying the resonant exchange generator. w=1 is the registered-endpoint control. This spatial law is explicitly adopted, not uniquely selected by stationarity.
4. Execute both original weighting branches at N=64,128,256 over one interval; retain L=1024*c*tau. Carry the same spatial law through 15 untouched channel labels.
5. Conserve SOURCE+supplier resource and the FULL carrier+interaction generator energy. The interaction term is not free or omitted.
6. Verify through independent RK4 integration and full 2N-block matrix evolution.

## Reproduce

Python 3 and NumPy only (validated with NumPy 2.3.5):

```sh
python3 compute.py
python3 verify.py
```

Expected: 218/218 main internal checks. Independent RK4 final state error about 4.42e-14 against the reduced projector solution. Minor floating-point differences are normal.

Files: bilingual reports, `input_manifest.json`, `existing_materials_audit.json`, `results.json`, `resolution.csv`, `continuous_exchange.csv`, `coupled_time_history.csv`, and independent verification outputs.

## Status and boundaries

SOURCE address cardinality, timeless prephenotypic allocation slots, register mode labels, supply bits and added record bits are kept distinct. No time/flow is added to allocation slots. The SOURCE is not a newly proposed particle, nor is the common carrier a fifth force.

This is a conditional dynamical completion. It does not derive SOURCE cardinality, the initial supply prior, autonomous one-shot triggering/reset, physical matter interactions or metric stress of the new generator. It does not replace previous cosmological results. No fresh CAMB likelihood or cosmological refit is performed, and this package has not been published to Zenodo/GitBook/GitHub as a new release.

Registered sources: https://doi.org/10.5281/zenodo.23516661 and https://doi.org/10.5281/zenodo.23329214 . Repository: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1 .
