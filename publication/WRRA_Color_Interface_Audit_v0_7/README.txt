Finite Address Component Replay and an SU(3) Singlet Audit | v0.7
Authors: Wonsik Choi and Jeongin Choi
DOI: 10.5281/zenodo.23497198

This is the same particle/color study, compacted to four pages.
No new color representation, six-factor extension or cosmological dynamics
is included. The original 36 scientific checks and four dependency checks
are unchanged. The added claim_gate.py integrates the evidence into an
actual release decision, not a generic publication-merit classifier.

python3 -m venv .venv
.venv/bin/python -m pip install numpy==2.3.5 scipy==1.17.0 sympy==1.14.0
.venv/bin/python audit.py
.venv/bin/python dependency_audit.py
.venv/bin/python claim_gate.py

For a release, write a JSON array of requested claim identifiers and run
python3 claim_gate.py requested_claims.json
Supported list example: ["component_replay", "declared_color_consistency"].
Unsupported stronger example: ["arithmetic_derivation_of_color"].
Exit 0 accepts the declared request; exit 2 rejects it.
Unknown claims fail closed. Four integration scenarios and three actual CLI
invocations are recorded. This is a source-specific release policy,
not an automatic theorem of scientific adequacy.

Reruns overwrite result JSON files. Preserve reference bytes for hash checks.
RELEASE.json binds the exact final PDF and computational files.
