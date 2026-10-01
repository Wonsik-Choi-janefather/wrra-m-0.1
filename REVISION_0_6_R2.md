# WRRA-M 0.6-r2 correction record / 교정 기록

Wonsik Choi · 2026-10-01 · CC BY 4.0

Version DOI: 10.5281/zenodo.23076547

Previous series release: 10.5281/zenodo.23075976 (0.6-r1).

## Changes

The 0.6 information-load grid and inherited carrier-test grid previously read independent parameters. With `lattice_N=64` and the inherited `internal_lattice_N=128`, the original implementation calculated state loads on 64 sites but tested transport on 128 sites. This mismatch was reproduced before correction.

The 0.6 `lattice_N` now controls both calculations. The inherited input remains unchanged as calibration provenance; only a private carrier-input copy receives the shared grid value. `lattice_contract` records the original configured size and both effective sizes. Public regression checks exercise both 64/128 and 128/64 input pairs, require equal effective grids, preserve the original input, and compare the uniform reference outputs.

“Accumulated twist record” is replaced with “global twist record magnitude” in both manuscript editions and the expansion/twist figure. This quantity is calculated from instantaneous load density and spatial size at the current state and scale. An independent temporal accumulation law is not part of the executed model. The quadratic aggregate W and its norm retain their existing formulas.

## Verified results

`compute.py` and `verify.py` were rerun. Pressure from finite volume variation, state normalization, continuity, internal exchange cancellation, independent propagation and acceleration checks pass. The shared-grid regression tests pass.

The adopted 128-site baseline remains q₀ = −0.52855, reference rotation speed = 207.510905 km/s and conditional deflection = 0.535586511 arcsec. Symmetric-carrier filter gaps remain zero. Changing the lattice can change nonuniform state loads; unchanged reference outputs refer specifically to the uniform state and fixed disclosed calibration.

Both DOCX editions preserve all 22 numbered native equations. Their five numerical/claim tables use the executed result ledger; figures are refreshed and PDFs are rendered from the corrected Word documents. Versions 0.1–0.5 and the r1 correction record are retained.

The constitutive choices nc=0, nb=3, load operators and information clock remain disclosed. The finite homogeneous construction and conditional calibrated local response retain their original completion scope; the microscopic origin of nb=3 and a complete covariant local theory remain open.

## 한국어

0.6의 정보부하 격자와 기존 수송 전달자 검사 격자가 별도 입력을 읽는 문제를 재현하고 수정했다. 이제 0.6의 `lattice_N`을 두 계산에 공통 적용한다. 기존 보정 입력은 그대로 보존하고 계산용 복사본에만 값을 연결한다. 결과의 `lattice_contract`에 원래 입력과 적용값을 표시한다. 64/128 및 128/64 교차 입력에서 격자 일치·원본 보존·균등 기준값 유지를 검증했다.

한영 원고와 그림의 “누적 뒤틀림 기록”을 “전역 뒤틀림 기록의 크기”로 교정했다. 현재 상태의 부하 밀도와 공간 크기로 계산한 집계값이며, 시간에 걸쳐 누적하는 별도 법칙을 계산한 것은 아님을 명시했다. 기존 수식과 핵심 연결을 유지한다.

전체 계산과 검증을 다시 실행했고 압력 미분·상태 보존·연속 방정식·에너지 교환 상쇄·별도 전달 및 가속도 계산 검사를 통과했다. 기준 감속계수 −0.52855, 회전속도 207.510905 km/s, 조건부 렌즈 편향 0.535586511각초를 재현했다. 격자 변경 시 비균등 상태의 부하까지 같다고 주장하지 않는다.

0.1~0.5와 앞선 r1 교정 기록을 유지하며, 수정된 0.6 한국어·영문 DOCX/PDF·원고·코드·검증 결과를 함께 공개한다. 배경 지수 3의 선택과 미시적 기원의 구분, 유한·동질 구성 모형의 완료 범위도 유지한다.
