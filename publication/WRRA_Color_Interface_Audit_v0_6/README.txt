Finite Address Component Replay and an SU(3) Singlet Audit | v0.6
Authors: Wonsik Choi and Jeongin Choi
DOI: 10.5281/zenodo.23496836

python3 -m venv .venv
.venv/bin/python -m pip install numpy==2.3.5 scipy==1.17.0 sympy==1.14.0
.venv/bin/python audit.py
.venv/bin/python dependency_audit.py

Original suite: 36 checks. Separate provenance suite: 4 checks.
Reruns overwrite result JSON files; keep reference bytes for hash comparisons.
RELEASE.json identifies exact final PDF, scripts and reference results.
The original source treats its decoder as conditional. The failed-decoder example
is prospective implementation guidance, not an allegation of a deployed bug.
