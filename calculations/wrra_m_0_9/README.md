# WRRA-M 0.9 common sector accounting

0.9는 상류의 세 부문을 같은 주소 분모로 실행하고 선택된 0.8 입자 채널과 연결한다. 물리 에너지·압력 사상은 0.10, 물리 양자화·관측 기록은 0.13에 이어진다.

| Evaluation | Completed in 0.9 |
| --- | --- |
| Verification input / 검증 입력 | Core 1.0, MCC 2.3.2, frozen 0.8 inputs and five upstream source snapshots. Editable arithmetic targets and disclosed channel routing. |
| WRRA-specific transformation / 고유 변환 | Common address weights → zeta-driven depleted admission → recovery boundary → positive complete sector effects → conditional origin routing → actual F_DX permutation and normalized generations. |
| Output / 산출값 | 5%, 26.8%, 68.2%; resident Actual 31.8%; complete accounted weight 100%; 48-channel ledger; nine inherited physical results unchanged. |
| Falsification / 반증조건 | Negative/incomplete effects, frozen calibration mismatch, failed transport conservation, duplicated multiplicity, charge disagreement, hidden recalibration or scope mismatch. |

```bash
python -m pip install -r calculations/wrra_m_0_9/requirements.txt
python calculations/wrra_m_0_9/run_release.py
```

Run from the repository or reproducibility archive root. The one-command run creates `results.json`, five CSV tables, `verification.json` and regenerated frozen 0.8 results under `results/baseline_0_8`. Twenty-seven check groups pass, including independent primality and zeta checks, per-address/per-frame conservation, conditional routing, source hashes and complete 0.8 regression. The release package removes captured outputs in a clean copy before repeating the run and compares bytes.

The arithmetic state uses addresses 2 through 1,000,000 and alpha=1.8996876950554356. Four adopted zeta heights, equal coefficients 1/2, zero phases, xi=0.1 and K=8 drive admission with h=1.44767317035244. Alpha and h fit two independent arithmetic targets; return closes the ledger. Effective beta is a derived output. A constant-beta upstream comparison is executed separately. Alpha=2 and alpha=1.9 comparisons are separate normalized rows.

Upstream resident Actual includes phenotype plus resident nonphenotype. Complete downstream accounting additionally includes returned provenance in the background-response branch. Before recovery, pending SOURCE and completed return are distinct fields. This bookkeeping does not establish the SI energy carried by that branch or its dynamical maintenance. Existing physical fractions 0.0493, 0.265 and 0.6857 remain separately frozen. `physical_bridge.energy_map` and `pressure_map` are null until 0.10.

The reference conditional origin kernel is 1/16, with three normalized generation weights. Optional odd smallest-prime family overrides are validated and exercised. The kernel is a constitutive input, not a derivation of individual particle identities from primes. Inventory weights allocate the arithmetic phenotype budget, not observed particle populations. Three neutral extension slots remain conditional. No physical measurement events or records are generated.

See [UPSTREAM_INTERFACE.md](UPSTREAM_INTERFACE.md) for fields, units and boundary rules, [ROADMAP_0_9_TO_1_0.md](ROADMAP_0_9_TO_1_0.md) for completion gates, and the bilingual papers in `paper/WRRA_M_0_9_*`.

Document rebuild: `write_papers.py`, then `build_reports.py` (pandoc and python-docx), render with LibreOffice, then `document_checks.py`. `package_release.py` verifies clean reproduction and builds the ZIP. Rendering and inspection of every final page precede publication.

Reviewed series 0.9-r1, 2026-10-02: https://doi.org/10.5281/zenodo.23091892 . See REVISION_0_7_TO_0_9_R1.md at the repository root.
