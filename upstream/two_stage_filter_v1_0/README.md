# WRRA-M 상위 구조의 두 단계 차원필터 가설 1.0

**최원식 Wonsik Choi · 2026-10-01**

초기 진입 필터의 변동으로 통과한 합성 관계가, 정상화된 0차원 복귀 필터에서는 보존된 접힘 때문에 돌아가지 못해 Actual로 남는다는 상류 구조 가설이다. 잔존은 표현형과 비표현형 Actual로 판독되고, 현재의 갱신 순서는 시간 프레임으로 읽힌다.

고정한 제타 가중치 시험에서 **4.876893353%** 잔존을 계산했다. 하나의 공통 가중 지수와 초기 통과율을 보정한 두 단계 구성은 **표현형 5% · 비표현형 Actual 26.8% · 상류 복귀 68.2%**를 같은 분모에서 재현한다. 전체 Actual은 **31.8%**이며 표현형 5%를 포함한다.

## 논문과 재현 자료

- [한국어 논문 PDF 14쪽](paper/WRRA_M_Upper_Two_Stage_Filter_Hypothesis_v1_0_KO_2026_10_01.pdf)
- [수정 가능한 수식이 있는 Word 원고](paper/WRRA_M_Upper_Two_Stage_Filter_Hypothesis_v1_0_KO_2026_10_01.docx)
- [GitHub에서 읽는 원고](manuscript_KO.md)
- [논문과 재현 코드 전체 ZIP](paper/WRRA_M_Upper_Two_Stage_Filter_Hypothesis_v1_0_Reproducibility_2026_10_01.zip)
- [공통 분할 결과 장부](code/results_26_8.json)
- [지수 2의 잔존 탐색 장부](code/results.json)
- [산술적 극한 계산](code/analytic_limit.json)
- [자세한 재현 안내](README_KO.txt)

## 검증 입력과 WRRA 변환 및 산출값과 반증조건

| 평가 단계 | 내용 |
| --- | --- |
| 검증 입력 | 유한 주소, 소수 판정과 인수분해, 제타 가중치 및 공개 구성비 목표 |
| WRRA 고유 변환 | 초기 진입과 정상 복귀의 두 단계 필터 및 잔존의 표현형 판독 |
| 산출값 | 4.8769% 고정 시험과 5%·26.8%·68.2% 공동 보정 장부의 양수성 및 완전성 |
| 반증조건 | 장부 재현 실패, 접힘 보존 실패 또는 공통 물리 응답의 불일치 |

공동 보정값은 α=1.8996876950554356, β=0.8654570124136961이다. 보정 출처와 구성 규칙은 원고에 공개했다. 프레임 간격, 입자 상수 역산, 제타 영점의 초기 변동 및 에너지·압력 연결을 다음 구현의 명세로 포함한다. WRRA Core 1.0과 MCC 2.3.2 및 기존 하류 계열은 이 상류 원고의 기준 구조다.

## Reproduce

```bash
python -m pip install -r requirements.txt
cd code
python compute.py --max-N 1000000 --out results.json
python partition_26_8.py
python analytic_limit.py
```

## English overview

This upper-structure hypothesis separates initial admission from normalized zero-dimensional return. Composite relation states admitted during early filter fluctuations remain in Actual when retained folds block return. Phenotype and unexpressed Actual are readouts of the same residue; frame updates provide the proposed interpretation of physical time.

A fixed exponent-two arithmetic test yields 4.876893353% odd-composite residue. A common weighted two-stage construction calibrated with α and β reproduces phenotype 5%, unexpressed Actual 26.8%, and return 68.2% in one denominator. Total Actual is 31.8%. The paper specifies the next interfaces for particle constants, fold dynamics, frame spacing, zeta-zero phases and physical energy/pressure response.

## Author and citation

[ORCID 0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772) · janefather@gmail.com

[Citation metadata](CITATION.cff) · [SHA256 checksums](SHA256SUMS)

The paper and documentation follow the repository's [CC BY 4.0 license](../../LICENSE).

