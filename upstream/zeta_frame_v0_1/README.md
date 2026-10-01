# WRRA-M 제타 영점 프레임 필터 계산 부록 0.1

**최원식 Wonsik Choi · 2026-10-01**

[두 단계 차원필터 상위 구조 가설 1.0](../two_stage_filter_v1_0)의 초기 필터 변동을 주소별·프레임별 통과 확률로 구현했다. 첫 4개 양의 제타 영점으로 초기 8프레임을 구동하고, 미진입 잔량만 다음 시도에 넘긴다. 정상화된 0차원 복귀 필터는 보존된 접힘을 차단한다.

기준 모형은 **α를 비표현형 Actual 26.8%에, h를 표현형 5%에 보정**한다. K=8, J=4, ξ=0.1을 미리 고정했고, 최종 같은 분모의 장부는 표현형 5%·비표현형 Actual 26.8%·복귀 68.2%다. α=1.8996876950554356, h=1.44767317035244. 일정한 β는 입력하지 않았다.

## 새 계산 출력

| 임계값 h를 고정한 초기 구간 | 표현형 잔존 |
| --- | --- |
| 4프레임 뒤 정상화 | 3.704795% |
| 8프레임 뒤 정상화 | 5.000000% |
| 16프레임 뒤 정상화 | 5.682474% |

소수 2 가족의 26.8%에서 시작해 최소 소인수 가족을 작은 소수부터 누적하면 전체 Actual 31.8%에 접근한다. **3·5·7·11 가족은 표현형 5%의 98.7275%**를 차지한다. 가족별 기여, 주소별 초기 통과, 거듭제곱 주소의 기여와 정상화 후 복귀 누수를 함께 계산했다.

## 자료

- [한국어 계산 부록 PDF 6쪽](paper/WRRA_M_Zeta_Zero_Frame_Filter_Appendix_v0_1_KO_2026_10_01.pdf)
- [Word 원고](paper/WRRA_M_Zeta_Zero_Frame_Filter_Appendix_v0_1_KO_2026_10_01.docx)
- [GitHub에서 읽는 계산 부록](appendix_KO.md)
- [원고와 코드 전체 재현 ZIP](paper/WRRA_M_Zeta_Zero_Frame_Filter_v0_1_Reproducibility_2026_10_01.zip)
- [전체 결과 JSON](code/results.json) · [계산 코드](code/compute.py)
- [프레임 그림](assets/frames.png) · [체크섬](SHA256SUMS)

## 검증 입력과 변환 및 출력과 반증 조건

| 단계 | 내용 |
| --- | --- |
| 검증 입력 | 제타 영점 40·60자리 재계산과 독립 Euler–Maclaurin 평가, 소수 판정, 공통 제타 분모 가중치 |
| WRRA 변환 | 초기 위상 구동 통과, 잔량 소모, 정상화 후 접힘 복귀 차단의 두 필터 |
| 출력 | 프레임별 양수 장부, 최소 소인수 가족의 잔존 기여, 고정 임계값 민감도와 누수 보존 조건 |
| 반증 조건 | 장부 재현 또는 영점 검증 실패, 요구 수명과 접힘 보존의 충돌, 향후 공통 물리 판독과 관측 반응의 충돌 |

14개 수치 검증이 모두 통과했다. 개별 주소의 무작위 경로를 추출한 시뮬레이션이 아니라 기대 가중치를 순차 운반한 계산이다. 짝수 합성수의 비표현형 분기와 홀수 합성수의 표현형 분기는 1.0의 시험 규칙을 이어받는다. ξ와 프레임 수는 무차원이며 물리적 시간 간격은 후속 판독에서 정한다.

## 재현

Python 3.12에서 계산했다. 계산은 인터넷 접속을 사용하지 않는다.

```bash
python -m pip install -r requirements.txt
python code/compute.py --output code/results.json
```

`source/appendix.py`와 `source/build_doc.py`는 같은 디렉터리의 `results.json`에서 원고와 그림을 만든다. Word 재생성에는 python-docx, matplotlib, lxml, Pandoc, Noto Sans CJK KR와 Latin Modern Math 글꼴이 필요하다. 재현 ZIP은 이 파일들을 실행 가능한 배치로 포함한다.

## English overview

This computational appendix turns the v1.0 early filter fluctuation into address- and frame-dependent admission. Four verified positive zeta zeros drive eight early frames. Each attempt uses only remaining SOURCE weight; the normalized return filter retains admitted composite folds under the declared arithmetic proxy. Alpha is calibrated to 26.8% nonphenotypic Actual and the sigmoid threshold to 5% phenotype.

With that threshold frozen, recovery after four and sixteen frames yields 3.704795% and 5.682474% phenotype. Lowest-prime-factor families 3, 5, 7 and 11 account for 98.7275% of the baseline phenotype weight. The appendix computes address responses, cutoff and phase sensitivity, and the retention condition under a leaky return gate. Energy, gravity, charge and physical clock readout continue the v1.0 interfaces.

[ORCID](https://orcid.org/0009-0001-4263-9772) · janefather@gmail.com · [Citation](CITATION.cff) · [CC BY 4.0](../../LICENSE)
