# WRRA-M 0.7

Run from the repository or release archive root:

```bash
python -m pip install -r calculations/wrra_m_0_7/requirements.txt
python calculations/wrra_m_0_7/run_release.py
```

The single authoritative input is `parameters.json`. The result and verification
files record its canonical SHA256 hash. `results/case_table.csv` contains nine
representative ledgers; sixteen physical-accounting check groups include twenty-four
additional mixed-state/exponent cases and nine rejected invalid inputs/states.

Actual 100 percent is normalized **energy-weighted information load**. The 4.93 percent
reference is a calibrated sector allocation, not a measurement outcome probability or
a bit count. Quantization outcomes, particle-filter selection and physical records are
not executed in this release. The frozen sibling `wrra_m_0_6` supplies the inherited
energy/pressure/gravity/expansion bridge and its `baseline_0_5` local renderer.

원고의 Actual 100%는 에너지 가중 정보부하의 전체다. 기준 표현형 4.93%와 비표현형
95.07%를 재현하고 상태와 공간 크기 변경 시 다시 계산한다. 입자 선택과 물리적 관측
사건은 후속 판에서 실행한다. 계산 로그와 물리적 관측 기록을 구분한다.

License: CC BY 4.0. Author: Wonsik Choi / 최원식.
ORCID: https://orcid.org/0009-0001-4263-9772 . Email: janefather@gmail.com.

Optional authoring: `write_papers.py` generates both Markdown sources;
`build_reports.py` requires pandoc and python-docx. Render the DOCX files to PDF
with LibreOffice, then run `document_checks.py` with python-docx and pypdf.
`package_release.py` builds the bilingual ZIP after checking a clean copy with
the captured numerical outputs removed. Its SHA256SUMS covers every packaged file.

This 0.7 development version is available on GitHub. The 0.6-r2 DOI identifies
the frozen baseline, not version 0.7. Use the included 0.7 CITATION.cff for this release.
