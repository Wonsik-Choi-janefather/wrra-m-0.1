# WRRA-M 접힘 전환과 입자 붕괴율 계산 0.2

**최원식 Wonsik Choi · 2026-10-02**

[입자 잔존과 붕괴 탐색 0.1](../particle_residue_decay_v0_1)의 선택한 핵자 주소 **45 = 3²×5, 75 = 3×5²**에서 실제 스핀·맛 상태와 전류의 행렬원소를 만들었다. 이 행렬에 유한 소수 계열의 응답, 최종 베타 상태공간과 알려진 약력 상수를 연결해 전환율을 계산한다.

**잔존 접힘 → 스핀·맛 전류 → 최종 상태공간 → 전환율 → Actual 내부 수송**을 한 실행으로 연결했다. 초기 통과 확률, 전체 물질 잔존율과 개별 입자 수명은 각자의 출력이다.

## 계산 결과

- 대칭 공간 바닥상태와 반대칭 색 단일항을 배정하고 64차원 스핀·맛 기저에서 **J=I=1/2 핵자 상태**를 선택했다. 각 상태의 비영 진폭 9개를 JSON에 저장했다.
- 전환 원소는 **벡터 1, 기본 축벡터 5/3**이다. 관측 λ=−1.2753으로 축벡터 상태 보정 ηA=0.76518을 정한다.
- 제타 분모에서 유한 국소 계열 **rₚ(N)=Σₖ₌₁ᴷ p⁻ᵅᵏ**를 사용한다. α=1.8996876950554356과 N=10⁶은 기존 산술 입력을 유지한다. 전환 진폭 κ√(r₃r₅)는 선언한 대칭 응답 커널이다.
- Q=0.78233355931 MeV의 쿨롱 근사 포함 베타 적분은 **fC=1.69166524**다. 알려진 GF·Vud·λ를 적용한 근사 수명은 **913.297225 s**다.
- 한 공통 κ를 관측 평균수명 **878.3 s**에 보정한다. κ≈12.200294834, κ²r₃r₅≈1.039846550. 이 유효 응답에는 생략한 방사·반동과 구성 보정도 들어간다.

## 보정을 고정한 출력

| 같은 전류와 접힘 커널의 방출 에너지 | 평균수명 |
| --- | --- |
| Q≤0 | 해당 채널 닫힘 |
| 0.25 MeV | 65,897.154334 s |
| 0.5 MeV | 4,974.761991 s |
| 0.78233355931 MeV | 878.3 s, 기준 보정 반환 |
| 1 MeV | 330.233016 s |
| 2 MeV | 18.501514 s |

에너지 시험은 같은 행렬원소와 점전하 쿨롱 근사를 유지한 사례이며 실재 원자핵의 수명으로 배정하지 않는다. 기준 Q에서 d log Γ/d log Q≈3.94313이다.

같은 Q·전류에서 u·d 표식을 3·7로 바꾸면 수명 1703.106948 s, 5·7로 바꾸면 4889.879089 s다. 이는 선택한 산술 커널의 응답 사례이고 새 입자를 식별한 결과는 아니다. 추가 상태 겹침 진폭을 절반으로 줄이면 율은 1/4, 수명은 3513.2 s가 된다. 겹침이 0이면 접힘 잔존에서도 그 채널은 닫힌다.

## 전자 에너지와 각도 응답

기준 자유 채널의 정규화 전자 운동에너지 분포는 수명 보정 κ에 의존하지 않는다. 현재 쿨롱·무반동 근사에서 **평균 0.301448183 MeV, 중앙 0.289729987 MeV, 최빈 0.245109345 MeV**를 반환한다. 반중성미자 평균 에너지는 0.480885376 MeV다.

관측 signed λ를 넣은 leading V−A 각도 계수는 a=−0.106543961, A=−0.119435252, B=0.987108710이다. PDG 2026 중심값과 차이를 결과에 기록했고 동시 재보정은 하지 않았다. κ는 정규화 각도 계수에서 상쇄되므로 전체 수명을 다시 맞춰 그 차이를 지울 수 없다.

## 보존 수송과 검증

최종 상태공간을 적분한 율에서 유효 Markov 전환 생성자와 정확한 Kraus 갱신을 계산했다. 중성자 표현형이 양성자·전자·반중성미자로 바뀌어도 **총 Actual 에너지 939.56542194 MeV, 전하 0, 바리온수 1**을 유지한다. 별도 SOURCE 복귀 누수는 켜지 않았다.

**30개 계산 검사가 통과했다.** 정규화와 교환 조건, 색 단일항, 전하·스핀과 벡터/축벡터 원소, 독립 적응 적분과 160점 Gauss 적분, 에너지 문턱과 보정 반환, 생성자·Kraus 갱신, 확률·Actual 보존과 분포 문턱을 확인했다.

## 자료

- [한국어 PDF 7쪽](paper/WRRA_M_Fold_Current_Beta_Rate_Bridge_v0_2_KO_2026_10_02.pdf) · [Word 원고](paper/WRRA_M_Fold_Current_Beta_Rate_Bridge_v0_2_KO_2026_10_02.docx)
- [GitHub 원고](manuscript_KO.md) · [전체 재현 ZIP](paper/WRRA_M_Fold_Current_Beta_Rate_Bridge_v0_2_Reproducibility_2026_10_02.zip)
- [계산 코드](code/compute.py) · [전체 결과 JSON](code/results.json)
- [고정한 핵자 입력과 출처](code/nucleon_reference.json) · [체크섬](SHA256SUMS)

## 재현

Python 3.12에서 계산했다. 계산은 인터넷을 사용하지 않는다.

```bash
python -m pip install -r requirements.txt
python code/compute.py
```

ZIP의 루트에서는 `python compute.py`로 실행한다. 코드와 입력을 함께 넣었고 원본 핵자 장부의 SHA256과 GitHub 커밋을 결과에 기록했다. Word 재생성은 `python code/build_doc.py`, ZIP에서는 `python build_doc.py`다. python-docx, lxml, matplotlib, Pandoc 및 Noto Sans CJK KR와 Latin Modern Math 글꼴이 필요하다.

## 구성과 보정의 범위

소수 표식 3·5와 대칭 바닥상태, 국소 오일러 계열 진폭은 구성 선택이다. λ와 수명은 두 응답 보정의 관측 입력이다. κ는 미시 접힘 결합과 생략한 방사·반동 응답을 아직 분리하지 않은 유효 세기다. 기본 셔터 시간과 완전한 QCD 결합 Hamiltonian은 이번 계산에서 새로 정하지 않았다.

다음 검사는 내부 상태에서 ηA를 읽는 공통 응답, κ에서 정밀 보정의 분리, 공통 질량·전류 규칙을 유지한 다른 실재 입자의 전환이다. 고정한 커널이 추가 응답을 재현하지 못하거나 보존 조건을 위반하면 해당 커널을 수정하거나 기각한다.

## English overview

An explicit symmetric three-valence-quark spin-flavor construction with antisymmetric color selects J=I=1/2 nucleon states on the chosen 45/75 arithmetic labels. It computes vector and bare axial transition elements 1 and 5/3. A finite Euler-factor family response and allowed beta phase space connect these matrix elements to rates using supplied masses, GF, Vud and the observed signed axial ratio.

The point-charge Coulomb approximation gives an unnormalized physical-kernel lifetime of 913.297225 s. One common fold-response strength is calibrated to the 878.3 s neutron mean life; controlled energy, prime-label, axial and overlap cases then use this fixed normalization. The normalized electron spectrum is independent of that lifetime anchor. Leading angular coefficients and their central differences from PDG are recorded without retuning.

Thirty checks pass, including spin/color symmetry, independent phase integrals, threshold behavior and a trace-preserving decay transport ledger. Effective axial dressing and response normalization still require a microscopic binding and radiative/recoil separation. The files distinguish these empirical inputs from the calculated finite matrices, response cases and conserved outputs.

[ORCID](https://orcid.org/0009-0001-4263-9772) · janefather@gmail.com · [Citation](CITATION.cff) · [CC BY 4.0](../../LICENSE)
