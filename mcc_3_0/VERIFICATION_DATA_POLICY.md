# MCC 3.0 Verification Data Policy

This policy is mandatory for every MCC 3.0 development stage.

Each stage must publish to GitHub:
1. README.md with scope, transformation, outputs, falsification conditions and verdict.
2. Machine-readable results.
3. Machine-readable verification data with explicit pass/fail checks and numerical evidence.
4. Exact input/provenance manifest or inherited baseline lock.
5. Executable code for every numerical calculation.
6. A handoff ledger when a next stage exists.

The fixed order is:

**verification input → WRRA-specific transformation → output → falsification condition → verdict**

Supplied values, calibration values, WRRA-specific rules, derived outputs and open assumptions must remain separately labeled.

A stage may not be marked PASS if its claimed verification data are absent from GitHub.

Historical MCC 2.3.2 and WRRA_M releases remain immutable provenance references. New MCC 3.0 candidate branches must be stored separately and compared against the frozen legacy branch.
