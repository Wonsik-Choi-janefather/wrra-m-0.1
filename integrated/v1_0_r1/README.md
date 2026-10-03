# WRRA M 상류·하류 통합 논문 1.0 검토판 r1

Wonsik Choi · Jeongin Choi / 최원식 · 최정인 · 2026-10-03

DOI: https://doi.org/10.5281/zenodo.23126800

검증 입력 → WRRA 고유 변환 → 산출값 → 반증조건 → 판정의 순서로 상류 생성, 공통 상태 에너지·전류, SI 장부, 압력·팽창, 고유시간, 측정·기록과 유효 공간 되먹임을 통합합니다. 상류 0.10, 하류 0.12, 연결 0.8의 종료를 유지한 통합 1.0입니다.

## Manuscripts and audit

- manuscripts/: Korean and English PDF, editable Word, source and generation script. Each edition contains 25 native display equations and 8 tables.
- numerical_claims.json: 55 numerical claims with actual Word-table or manuscript-line locations and exact JSON source paths.
- audit_release.py: run `python audit_release.py` from the extracted package root; it also works from another working directory.
- evidence/: fresh bridge and downstream replay results and logs. Published-document review receipts retained inside the downstream sources validate their earlier documents only.
- REVIEW_REPORT.md and validation.json: review corrections and validation scope.
- SHA256SUMS: every included file except itself.

## Physical calculation replay

Python dependencies are listed in requirements.txt. Set OPENBLAS_NUM_THREADS=1.

Extract source_archives/WRRA_M_Bridge_0_5_0_8_Reviewed_r1_2026_10_03.zip into a fresh directory, enter its package root and run `python reproduce_all.py`. It contains the frozen upstream and earlier bridge dependencies; dependency inputs propagate in stage order.

Extract source_archives/WRRA_M_0_12_r1_Series_Release.zip into another fresh directory. Run `python calculations/wrra_m_0_10/run_release.py`, then `python calculations/wrra_m_0_12/run_release.py`, then `python review/0_10_to_0_12_r1/review_contracts.py`. Distinct computational groups contain 32 + 28 + 36 = 96 checks; they are not 96 physical experiments. The new clean replay matched 37 registered files byte for byte.

## Source publications

Upstream integrated: https://doi.org/10.5281/zenodo.23119041
Downstream integrated: https://doi.org/10.5281/zenodo.23115883
Downstream executable series: https://doi.org/10.5281/zenodo.23113101
Bridge 0.1–0.4: https://doi.org/10.5281/zenodo.23119802
Bridge 0.5–0.8: https://doi.org/10.5281/zenodo.23120693

The manuscripts use CC BY 4.0; retained source distributions preserve their licenses and attribution. This is an author-reviewed computational preprint, without a claim of journal peer review or acceptance.
