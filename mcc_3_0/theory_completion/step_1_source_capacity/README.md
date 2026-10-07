# WRRA / MCC 3.0 theory completion — Step 1: SOURCE capacity

**Reviewed release r1 · 8 October 2026**

Step 1 closes the declared conditional finite-SOURCE construction and its capacity-dependent transport through the existing uniform carrier, energy-pressure, expansion and conditional local-gravity branch. All 13 registered replay checks pass. The completion label applies to this scope.

- [한국어 연구 정리 및 완료 판정](REPORT_KO.md)
- [English research report and completion decision](REPORT_EN.md)
- [Review changes](REVIEW_NOTES.md)
- [SOURCE inputs and held-fixed quantities](source_contract.json)
- [Capacity transport results](capacity_transport_results.json)
- [Exact arithmetic and sensitivity audit](results.json)
- [Pinned source provenance](source_manifest.json)

## Assessment

| Verified inputs | WRRA-specific transformation | Outputs | Falsification conditions |
|---|---|---|---|
| Frozen calibrated address fractions, inherited H=29 and C=70, published filter/SI/local coefficients | LCM resolution → finite SOURCE → prime/composite phase filter → address load → SI energy → volume pressure → shared local gravity and homogeneous expansion | Three SOURCE sizes propagated without refitting | Incomplete normalization, inconsistent handoffs, pressure/continuity failure, hidden refit, separate rotation/lensing gravity scales |

| SOURCE codes N | q at a=1 | Rotation (km/s) | Conditional lensing (arcsec) |
|---:|---:|---:|---:|
| 1,015,000 | -0.5285585894376318 | 207.5102418659153 | 0.5355822400088303 |
| 4,060,000 | -0.5292825795228291 | 207.4541349970819 | 0.5352210185078975 |
| 20,300,000 | -0.529977941992902 | 207.40039181157826 | 0.5348750792521283 |

## Reproduce

Tested with Python 3.12.14 and the pinned packages below. From this directory:

```bash
python -m pip install -r requirements.txt
python reproduce.py
```

The arithmetic audit and three capacity probes are executed, original-source hashes are checked, and regenerated outputs are compared with the registered results. No network access is required during replay. The scripts reuse pinned original pure functions through AST extraction; they do not execute every historical repository stage.

## Interpretation

N is the finite SOURCE address-code count. Address 1 is an inactive reference, so the executable address count is N−1. N, the rational resolution L, the internal channel inventory and the conditional-readout rank are different quantities.

Changed fractions in the probes select SOURCE sizes; the filter is held fixed and is not fitted to those new targets. Output residuals are recorded. The probes are distinct model configurations, not a time trajectory of our universe.

Capacity invariance is not a completion requirement. Known-value reproduction is an explanatory/consistency achievement, and calibration is a legitimate disclosed model input. This release retains the assumptions H=29, C=70 and N=LHC. It does not promote those assumptions into a proof of necessary physical capacity. The provisional composition-to-phase bridge was not adopted.

Stage numbering here refers to the October theory-completion work, separately from the earlier six integration stages.
