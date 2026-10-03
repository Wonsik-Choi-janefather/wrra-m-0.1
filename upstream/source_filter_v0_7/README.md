# WRRA M 상류 0.7 SOURCE 상태와 두 단계 필터의 생성 장부

최원식 Wonsik Choi · 2026-10-03 · version 0.7 · CC BY 4.0

소수 SOURCE의 로그 세기와 위상 변수를 합성 관계 진폭에 전달하고,
진입 A → 정상 복귀 B → 표현/비표현 잔존의 계산 장부로 연결한다.
두 단계 필터 1.0-r1의 α=1.8996876950554356과 β=0.8654570124136961은 동결한다.
이 두 수는 이전 공동 보정값이며 이번 단계에서 새로 유도하거나 재보정하지 않았다.

## 계산된 결과

| 조건 | 표현 잔존 φ | 비표현 잔존 D | 복귀 R |
| --- | --- | --- | --- |
| 기준 SOURCE N=1,000,000 | 5.000000% | 26.800000% | 68.200000% |
| 소수 2 ε=−0.15 | 5.638323% | 23.066975% | 71.294702% |
| 소수 2 ε=+0.15 | 4.359397% | 31.137151% | 64.503451% |

진폭 생성 규칙은 `z_p=p^(-alpha/2) exp(epsilon_p/2+i theta_p)` 및
`g_n=product(z_p^v_p(n))`이며, n=2…N에서 정규화한다.
수치는 정보 가중치이다. 물리 시간 단위와 에너지 사상은 아직 정의하지 않았다.

- 대각 필터에서는 SOURCE 위상만 바꿔도 출력 가중치가 변하지 않는다.
- N=161의 선언된 주소 3↔9 혼합과 결맞음이 함께 있을 때 위상 반응이 생긴다.
  혼합 각도 0.25 rad는 시험 가정이며 도출된 미시 결합이 아니다.
- 첫 전량 방출 뒤 생성 창을 닫고 잔존 누출을 없애면 Actual=31.8%가 유지된다.
- 복귀 stock을 같은 SOURCE 상태로 재준비하여 매회 u=0.2로 재방출하면,
  누출 없는 32회 뒤 Actual=87.788614%이고 무제한 재방출 극한은 100%이다.
  따라서 기준 비율은 일반적인 재방출 고정점이 아니다.
- 별도 누출 ν=0.1에서는 Actual 고정점이 40.447723%이다.
  31.8% 목표를 역으로 반환하는 ν=0.145664246049는 별도 보정 제어이며 새 예측이 아니다.

## 재현

Python 3.11 이상, NumPy 2.3.5를 사용한다. NumPy wheel과 플랫폼에 따라
마지막 비트가 달라질 수 있다. 본 공개 묶음은 Linux의 Python 3.12.14,
NumPy 2.3.5, BLAS thread 수 2에서 새 복사본의 JSON 바이트 일치를 확인했다.
물리 계산은 Word/PDF 렌더러를 요구하지 않는다.

```bash
python3 -m pip install -r requirements.txt
python3 reproduce_all.py
```

runner는 thread 수를 2로 고정하고 기본 계산과 독립 감사를 실행한다.
기본 검증 53개와 독립 감사 60개, 합계 113개가 통과한다.
소인수 직접 곱, 공분산 미분, 위상 회전 닫힌 식, Choi 양성·trace 보존,
stock 반복식과 고정점, 잘못된 입력 거부, 새 복사본 재현을 확인한다.
검증 통과는 유한 모형의 내부 일관성이며 물리 SOURCE의 실험 검증이 아니다.

`code/inputs.json`은 공개 기준이다. `code/compute.py --inputs <file> --out <file>`로
SOURCE 제어 스캔·유효 주소 상한·위상 대조·stock 프로토콜을 바꿀 수 있다.
본 release의 α·β는 동결되어야 한다. 다른 α·β는 하위 수학 함수에서 계산할 수 있지만
공개 기준 감사에서 계승 계약을 통과하지 않는다.
대각 SOURCE 세기 지원 구간은 ε∈[−2,2]이다. 유한 N의 정규화와 무한 급수의
수렴은 구분한다. 무한 확장에는 각 제어 소수의 ε_p<α log p가 추가로 필요하다.

## 자료 구성

- `paper/`: 한글 Word와 PDF 원고
- `manuscript_KO.md`: 같은 원고의 텍스트
- `code/inputs.json`, `compute.py`, `results.json`: 입력·계산·결과
- `code/handoff.json`: 0.8 이후의 주소·상태·필터·stock 계약
- `verify_release.py`, `verification/independent_audit.json`: 독립 감사
- `inherited/`: 변경하지 않은 계승 코드·결과와 `SHA256.json`
- `source/`: JSON으로 원고·수식·그림을 만드는 문서 소스
- `ROADMAP.md`, `provenance.json`, `SHA256SUMS`: 종료 계획·출처·무결성

계승 Python 파일은 역사적 원문 보존용이다. 실행 경로는 `code/compute.py`이다.
수학 식은 Word의 native OMML로 저장한다. 문서 재생성에는 python-docx,
lxml, matplotlib, pandoc, NanumGothic 및 Latin Modern Math가 필요하다.

## 공개와 인용

현재 공개 폴더:
https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/main/upstream/source_filter_v0_7

이 0.7 release에는 DOI를 아직 발급하지 않았다. `CITATION.cff`를 사용한다.
아래 DOI는 계승 자료에 대한 인용이며 0.7의 DOI가 아니다.

- 0.3까지의 자료 및 두 단계 필터: https://doi.org/10.5281/zenodo.23092499
- 0.4–0.6 교정 자료집: https://doi.org/10.5281/zenodo.23112253

SOURCE에서 입자 상태로 가는 물리 사상은 아직 연결하지 않았다.
0.6의 전류·수명·계수는 본 단계에서 변경하지 않는다. 다음 단계는
사건 번호를 시간과 구분하면서 셔터 갱신·프레임·최소 판독 단위를 정의하는 0.8이다.
