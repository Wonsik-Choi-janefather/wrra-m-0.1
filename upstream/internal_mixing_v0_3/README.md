# WRRA-M 내부 접힘 혼합과 핵자 전류 0.3

**최원식 Wonsik Choi · 2026-10-02**

[접힘 전환과 붕괴율 0.2](../fold_decay_v0_2)의 축벡터 보정 ηA를 **내부 구성 혼합의 고유상태**로 바꾸는 상류 후속 계산이다. 선택한 핵자 주소 **45 = 3²×5, 75 = 3×5²**를 유지하고, 제타의 유한 소수 계열을 2상태 Hamiltonian의 결합에 연결한다.

**소수 계열 → 내부 Hamiltonian → 고유상태 → 서로 구분한 전자기·약한 전류 → 전환율**을 계산했다. 같은 내부 상태에 두 전류를 적용한다.

## 핵심 결과

| 출력 | 자기모멘트만 보정하고 c1=0 | 축벡터를 함께 보정 |
| --- | --- | --- |
| 혼합 구성 점유 q | 0.0735319384 | 0.2935250000 |
| 축벡터 크기 gA | 1.5686240822 | 1.2753000000 |
| 무차원 결합 C | 3.6611913193 | 13.1934742975 |
| 공통 정적 자기 응답 c0, μN | −0.0628526596 | −0.0628526596 |
| 반대 부호 정적 자기 응답 c1, μN | 0으로 고정 | 0.4399877929 |
| 두 자기모멘트 | 관측 입력 반환 | 관측 입력 반환 |
| 부모 κ를 고정한 수명 | 616.062113 s | 878.300000 s |

첫 경로의 축벡터는 관측 1.2753보다 **23.0004% 크다**. 공동 경로는 관측 축벡터로 q를 정하고 실제 집단 연산자 `(2Iz)(2Jz)`를 전자기 응답에 포함해 두 자기모멘트와 축벡터를 반환한다. 양성자·중성자에 반대 부호로 필요한 성분은 **0.4399877929 μN**이다.

공동 경로의 **29.3525%는 핵자 내부 혼합 점유**다. 우주 암흑 물질 26.8%나 표현형 잔존 5%와 별도 장부다. 부모 κ는 이미 관측 λ와 수명을 사용했으므로 878.3 s는 그 보정의 반환이다.

## 실제 유한 상태와 연산자

- 스핀·맛 64차원 × 추상 공간 표지 3차원 = **192차원**. 색은 반대칭 단일항이다.
- 대칭 구성 S와 혼합 구성 M 모두 J=I=1/2이며, 스핀·맛과 공간을 결합한 교환대칭을 직접 검사했다.
- 구성 기저의 전류는 **V=diag(1,1), Az=diag(5/3,1/3)**. 따라서 `gA(q)=5/3−4q/3`이다.
- `H_B=(m_B−e_min)I+Δ[[0,−C√(r_u r_d)],[−C√(r_u r_d),1]]`에서 혼합 고유상태를 계산한다.
- `M=μu U+μd D+c0(2Jz)+c1(2Iz)(2Jz)`는 두 핵자에 적용하는 공통 정적 자기 연산자다.

공간 표지는 L=0 짝수 패리티를 배정한 교환 표현이다. 방사형 파동함수와 QCD 결합 동역학은 아직 지정하지 않았다. 응답 에너지 `mu*=(2mp−mn)/3`, `md*=(2mn−mp)/3`는 기존 가산 질량 규칙의 유효 Dirac 선택이며 current quark 질량으로 배정하지 않는다. 기준 Δ=(mp+mn)/6은 에너지 척도 선택이고 질량 기준점은 입력 mp·mn을 반환한다.

## 보정을 고정한 소수 계열 응답

공동 C·c0·c1, 응답 에너지, Q와 약력 상수 및 부모 κ를 고정한다.

| u d 표식 | p n 주소 | 혼합 q | 축벡터 gA | 수명 s |
| --- | --- | --- | --- | --- |
| 3 5 | 45 75 | 0.293525 | 1.275300 | 878.300 |
| 3 7 | 63 147 | 0.233061 | 1.355918 | 1536.765 |
| 5 7 | 175 245 | 0.134723 | 1.487036 | 3765.925 |
| 3 11 | 99 363 | 0.150579 | 1.465895 | 3219.749 |
| 5 11 | 275 605 | 0.072018 | 1.570642 | 8194.355 |

각 경우 자기모멘트도 같은 상태에서 변하며 전체 수치를 JSON에 저장했다. 이 표는 고정한 산술 규칙의 통제 시험이고 새 실재 입자의 식별 목록은 아니다.

c1이 자유로우면 여러 q가 동일한 두 자기모멘트를 반환한다. 그 연속 자유도를 식 (8)과 네 사례로 기록했다. Δ를 100, 312.972918562, 1000 MeV로 바꾸어도 같은 q와 전류를 반환하므로 정적 전류만으로 절대 내부 에너지·셔터 시간을 정할 수 없다.

## 검증과 재현

**38개 구현 검사 통과**: 교환 표현, 상태 정규화·양자수·전하·색, 전류 블록, 수치 역산과 닫힌 식, 두 보정 반환, 독립 위상공간 적분 및 Kraus 수송. 단순 경로의 관측 축벡터 불일치는 그대로 기록했다.

부모의 수송을 적용해 총 Actual 에너지 939.56542194 MeV, 전하 0, 바리온수 1을 유지했다. 별도 SOURCE 복귀는 0이다.

```bash
python -m pip install -r requirements.txt
python code/compute.py
```

ZIP 루트에서는 `python compute.py`다. Python 3.12에서 계산했고 인터넷 없이 재현한다. 입력과 고정한 부모 코드의 SHA256 및 부모 커밋을 포함한다. Word 재생성은 `python code/build_doc.py`이며 python-docx, lxml, matplotlib, Pandoc, Noto Sans CJK KR와 Latin Modern Math가 필요하다.

## 자료

- [한국어 PDF 7쪽](paper/WRRA_M_Internal_Fold_Mixing_Shared_Currents_v0_3_KO_2026_10_02.pdf) · [Word](paper/WRRA_M_Internal_Fold_Mixing_Shared_Currents_v0_3_KO_2026_10_02.docx)
- [원고](manuscript_KO.md) · [재현 ZIP](paper/WRRA_M_Internal_Fold_Mixing_Shared_Currents_v0_3_Reproducibility_2026_10_02.zip)
- [계산](code/compute.py) · [전체 결과](code/results.json) · [입력](code/inputs.json) · [체크섬](SHA256SUMS)

## 다음 상류 제약

공통 내부 결합에서 c1과 축벡터 혼합을 산출하고, 방사형 상태·물리적 들뜸 응답으로 Δ를 정한다. 부모 κ의 방사·반동 보정을 분리한 뒤 다른 실재 입자의 전환을 같은 규칙으로 계산한다. 고정한 추가 규칙이 전류·채널 응답을 재현하지 못하거나 교환·보존 조건을 어기면 해당 규칙을 수정하거나 기각한다.

## English overview

This follow-up constructs symmetric and mixed-permutation configurations in a 192-dimensional spin-flavor/spatial-label space, with antisymmetric singlet color. Their projected weak currents are V=I and Az=diag(5/3,1/3). A finite Euler-family two-state Hamiltonian supplies the common nucleon eigenstate.

The magnetic-only inverse with zero collective isovector correction gives q=0.0735319384 and gA=1.5686240822, 23.0004% above the observed axial magnitude. A joint calibrated realization uses q=0.293525 and a collective static magnetic coefficient c1=0.4399877929 nuclear magnetons to return both observed magnetic moments and the axial input. The parent lifetime normalization is retained. Fixed prime-family controls change the state, both currents and rate together. Thirty-eight mathematical/numerical checks pass; calibration roles and unresolved radial, energy-scale and exchange-current dynamics are recorded.

[ORCID](https://orcid.org/0009-0001-4263-9772) · janefather@gmail.com · [Citation](CITATION.cff) · [CC BY 4.0](../../LICENSE)
