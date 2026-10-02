# Reviewed upstream 0.5-r1

Review date: 2026-10-03. Collection DOI: https://doi.org/10.5281/zenodo.23112253. Run `python code/compute.py` then `python verify_release.py`; see `verification.json` for the current check count. The original study and frozen kernels remain preserved in their historical GitHub paths.

# WRRA M 상류 0.5 · 내부 공간의 안정성, 여기 척도와 핵자 크기

0.4의 유한 두 상태 결합을 실제 고차 공간으로 확대했습니다. 원래 이차 결합은 기존 결합값에서 에너지가 아래로 제한되지 않으므로 실패를 기록하고, 순열 대칭과 두 상태 결합 원소를 보존하는 제한 결합으로 보강했습니다.

같은 바닥상태에서 알려진 축벡터·자기모멘트를 공동 보정하며, N(1440)의 실수 극 중심 1370 MeV를 첫 여기 중심에 조건부 배정하고 양성자 반지름 0.84075 fm를 점전하 모형으로 판독합니다. 기준 λ=1, K=8에서 **Δ=507.032217686 MeV, ℓ=0.61619621794 fm**입니다. 보정값을 고정한 K=10 검증에서 여기 간격의 변화는 **0.00854213 MeV**입니다.

보정하지 않은 중성자 전하 평균제곱 반지름 **−0.186911738 fm²**는 비교값 **−0.1155±0.0017 fm²**와 다릅니다. 구성의 자체 크기·상대론·교환 전하를 포함하지 않은 점전하 completion의 한계로 기록합니다. λ 선택은 아직 유일하게 결정되지 않았고 공명 폭은 계산하지 않습니다. 아래로 제한되는 유효 공간 모형의 보정과 검사 결과이며 미시 QCD 도출을 주장하지 않습니다.

**구현 118개 + 별도 검증 32개 = 총 150개 통과**, 새 디렉터리의 결과 JSON 바이트 재현을 확인했습니다. 기존 Core 1.0, MCC 2.3.2와 0.4 출판 기록을 유지합니다.

- [한글 원고](manuscript_KO.md)
- [PDF](paper/WRRA_M_Spatial_Stability_Excitation_Scale_v0_5_r1_KO_2026_10_03.pdf) · [Word](paper/WRRA_M_Spatial_Stability_Excitation_Scale_v0_5_r1_KO_2026_10_03.docx)
- [전체 재현 ZIP](paper/WRRA_M_Spatial_Stability_Excitation_Scale_v0_5_Reproducibility_2026_10_02.zip)
- [입력](code/inputs.json) · [결과](code/results.json) · [검증](verification.json) · [문서 검사](document_checks.json)
- [구현](code/compute.py) · [공간 기저](code/model.py) · [별도 검증](verify_release.py)

## 재현

Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0에서 실행했습니다.

```bash
python -m pip install -r requirements.txt
export OPENBLAS_NUM_THREADS=2
python code/compute.py
python verify_release.py
```

원고 재생성에는 source/requirements.txt, Pandoc, NanumGothic과 Latin Modern Math 글꼴이 추가로 필요합니다.

```bash
python -m pip install -r source/requirements.txt
python source/build_doc.py
```

표와 수식은 실행 결과에서 생성합니다. PDF 렌더링은 LibreOffice와 Poppler로 할 수 있습니다. 결과 JSON은 소수점 11자리로 직렬화하고 검사 판정에는 반올림 전 수치를 사용합니다.

## 입력의 역할

| 입력 | 역할 |
| --- | --- |
| 부모 α·N·κ 및 핵자 질량 | 기존 기준과 약한 수명 보정 유지 |
| gA·두 자기모멘트 | C·c₀·η 및 공유 바닥상태 보정 |
| N(1440) 실수 극 중심 | 첫 양의 패리티 여기 중심 배정, Δ 보정 |
| 양성자 반지름 | 공개한 점전하 모형의 ℓ 보정 |
| 중성자 반지름 | 보정 외 비교; 불일치를 기록 |
| λ=1 및 λ=0.5·2 | 공개한 제한 결합 선택과 민감도 |

극 중심 1360–1380 MeV와 양성자 반지름의 ±1σ 범위는 다른 입력과 모형을 고정한 조건부 척도 범위입니다. λ 민감도와 공간 절단 오차는 이 입력 범위와 별도입니다. λ=0.5·2의 고차 공간 수렴은 기준 λ=1과 같은 수준으로 검증했다고 주장하지 않습니다.

상류 0.5-r1은 0.4–0.6 교정 자료집 DOI 10.5281/zenodo.23112253으로 함께 공개합니다. 이전 상류 검토 자료집은 [DOI 10.5281/zenodo.23092499](https://doi.org/10.5281/zenodo.23092499)입니다.

저자 최원식 Wonsik Choi · [ORCID 0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772) · 2026-10-02. 원고·문서 CC BY 4.0.
