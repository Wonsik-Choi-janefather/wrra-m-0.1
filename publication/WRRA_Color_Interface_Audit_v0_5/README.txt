Particle/color audit v0.5. Title retained: Finite Address Component Replay and an SU(3) Singlet Audit.
Changes from v0.3: public code access, dependency table, environment instructions, and grouping of the unchanged 36 checks.
No new cosmology, dynamics, fixed-I/X paper or arithmetic-to-SU(3) derivation is added.

python3 -m venv .venv
.venv/bin/python -m pip install numpy==2.3.5 scipy==1.17.0 sympy==1.14.0
.venv/bin/python audit.py

Reruns overwrite audit_results.json. Preserve reference bytes for hash comparisons.
SOURCE_SHA256.json checks frozen source files before execution.
Existing public executable code is pinned in the manuscript; final v0.5 PDF is identified by RELEASE.json.

Four additional source-dependency checks: python3 dependency_audit.py.
The physical calculation and original 36-check suite are unchanged.

Immutable archive of the exact v0.5 PDF and RELEASE.json:
https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/7c9f851622499613ceb3ff4b2e1495bf2d7fa15e/publication/WRRA_Color_Interface_Audit_v0_5
