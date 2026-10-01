# WRRA-M 0.8

Common carrier response -> calibrated four-filter selection -> channel placement
-> one hypercharge operator -> three-generation charge inventory -> the same 0.7 ledger.

```bash
python -m pip install -r calculations/wrra_m_0_8/requirements.txt
python calculations/wrra_m_0_8/run_release.py
```

The single configuration input `parameters.json` embeds the frozen 0.7 ledger.
Nine representative states select F_DX. Twenty-three check groups include direct
resolvent evaluation, periodic spectra, the selection ODE, exact charges and anomalies,
orientation controls, grid changes and inherited 0.1–0.4 checks.
`results/particle_inventory.csv` records 45 Standard-Model chiral components and three
conditional neutral extension slots. Generation count is calibration; masses and
mixing are not newly derived. The gauge-neutral slots are not measured particles.

The origin orientation, dimensionless readout offset and contrast are disclosed
calibrations. Removing contrast restores the tie. These are auxiliary readout
operators in a calibrated weak-component basis, not new energy terms or an
unbroken SU(2)-invariant Hamiltonian. Optimizer weights are not Born probabilities.
Physical measurement events and records remain for 0.13.

0.8은 보정 규칙 아래에서 네 필터를 실제 비교하고 F_DX 배치와 전하를 산출한다.
세 세대 수는 알려진 입자 정보에 맞춘 입력이며, 45개 표준모형 성분과 조건부
중성 슬롯 3개의 전하 장부를 실행한다. 같은 상태·격자가 0.7의 물리 장부에도
들어가며 에너지를 채널 수나 세대 수만큼 중복 계산하지 않는다.

Authoring: `write_papers.py` generates both manuscripts; `build_reports.py` requires
pandoc and python-docx. Render DOCX to PDF with LibreOffice, then run
`document_checks.py` with python-docx and pypdf. `package_release.py` performs a
clean-copy run with captured numerical outputs removed and builds the bilingual ZIP.

Author: Wonsik Choi / 최원식. ORCID: https://orcid.org/0009-0001-4263-9772 .
Email: janefather@gmail.com. License: CC BY 4.0.
Revision 0.8-r1 is included in the reviewed 0.7–0.9 series, DOI 10.5281/zenodo.23091892. The 0.6-r2 DOI identifies the frozen baseline.

Reviewed series 0.9-r1, 2026-10-02: https://doi.org/10.5281/zenodo.23091892 . See REVISION_0_7_TO_0_9_R1.md at the repository root.
