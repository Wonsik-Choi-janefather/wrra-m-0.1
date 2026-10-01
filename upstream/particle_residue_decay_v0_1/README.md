# WRRA-M 입자 잔존 주소와 접힘 붕괴 탐색 0.1

**최원식 Wonsik Choi · 2026-10-01**

[두 단계 차원필터 상위 가설](../two_stage_filter_v1_0)과 [제타 영점 프레임 필터](../zeta_frame_v0_1)의 잔존 주소에서 입자 구조를 읽는 후속 탐색이다. **입자는 접힘 잔존의 표현형이며, 붕괴는 Actual 안의 접힘 관계 전환**이라는 가설을 계산 장부로 구현했다.

구성 소립자, 색과 강력, 핵자 사이 잔여 핵력, 약력 전환, 전자기 전류, 스핀을 분리한다. 같은 주소에도 내부 상태·결합·환경에 따른 여러 표현형을 허용한다. 상태 구조는 **주소 + 물리 채널 + 순 가쿼크 구성 + 내부 상태 + 환경**이며 바다 쿼크와 글루온은 확장 상태에 기록한다.

## 실행 결과

| 시험 | 계산 출력 |
| --- | --- |
| A 질량비 역산 | 전자 주소 9와 공통 거듭제곱 판독에서 Ω=3 홀수 양성자 주소 141,790개 검사. 중성자 비율 선별 폭에 맞는 후보쌍 15개. 같은 판독의 뮤온 검사는 15개 모두 불일치. |
| B 공통 핵자 곱 | a²b·ab² 소수쌍 735개 검사. 가장 가까운 중성자 에너지는 956.902279 MeV로, 이 고정 판독은 관측 핵자 차이에 맞지 않음. |
| C 보정된 핵자 구성 | u 표식 3, d 표식 5를 선택해 양성자 45와 중성자 75의 공통 에너지·전류 판독 구성. 관측 질량과 자기모멘트로 보정하고 전하 +1·0 반환. |
| D 별도 채널 연산자 | 주어진 한 세대 15 카이럴 채널의 전하·약력·색 관계, 세 쿼크 색 단일항과 세 스핀 합성에서 10개 검사 통과. |
| E 자유 베타 전환 | 중성자 Q=0.78233355931 MeV. 반대 자유 양성자 베타 채널 Q=−1.80433146069 MeV. 보정된 평균수명 878.3 s의 기대 장부에서 에너지·전하·바리온수·렙톤수 보존. |

45·75는 최소 홀수 소수로 만든 **보정된 구성 선택**이다. 소수 표식 자체를 상수에서 유일하게 결정했다고 배정하지 않는다. 핵자 질량 2개·자기모멘트 2개·자유 중성자 수명이 보정 입력이며 전하·가쿼크 구성·표준모형 표현은 공개 입력이다.

## 자료

- [한국어 PDF 7쪽](paper/WRRA_M_Particle_Residue_Decay_Trial_v0_1_KO_2026_10_01.pdf) · [Word 원고](paper/WRRA_M_Particle_Residue_Decay_Trial_v0_1_KO_2026_10_01.docx)
- [GitHub 원고](manuscript_KO.md) · [전체 재현 ZIP](paper/WRRA_M_Particle_Residue_Decay_Trial_v0_1_Reproducibility_2026_10_01.zip)
- [입자 계산 결과](code/results.json) · [채널 계산 결과](code/channel_results.json)
- [입자 계산 코드](code/compute.py) · [분리한 채널 코드](code/channel_readout.py)
- [입력 제타 필터 장부](code/zeta_reference.json) · [SHA256 체크섬](SHA256SUMS)

## 독립적인 응답 항목

| 항목 | 실행 범위와 다음 연결 |
| --- | --- |
| 강력 | 8개 색 생성자와 세 쿼크 색 단일항 검사. 강한 결합 에너지와 αs의 척도 의존성은 별도 응답 입력. |
| 잔여 핵력 | 핵자 사이 결합과 환경에 따른 전환 문턱은 다음 유효 핵력 판독. |
| 약력 | 왼손 d→u 및 e→ν 올림과 교환 조건 계산. 실제 수명 행렬원소·혼합·상태밀도는 후속 연결. |
| 전자기력 | Q=T₃+Y와 부호를 가진 자기 전류를 분리. 이 Y는 PDG 초전하의 절반. |
| 스핀 | 1/2⊗1/2⊗1/2=1/2⊕1/2⊕3/2 확인. 실제 핵자 가지는 완전한 색·스핀·맛·공간 상태로 선택. |
| 질량과 붕괴 | 핵자 바닥상태 이중항의 보정 판독과 지배적 자유 베타 장부. 핵자 에너지차의 강력·전자기 분해 및 새 입자 응답은 다음 시험. |

## 재현

Python 3.12, numpy와 scipy를 사용한다. 계산에는 인터넷 접속이 필요 없다.

```bash
python -m pip install -r requirements.txt
python code/compute.py
python code/channel_readout.py
```

재현 ZIP에서는 두 스크립트와 입력 JSON이 루트에 함께 있다. 추출한 디렉터리에서 `python compute.py`, `python channel_readout.py`로 실행한다. 입력 제타 JSON의 SHA256과 원본 GitHub 커밋은 입자 결과에 기록되어 있다.

Word 재생성은 `python code/build_doc.py`로 실행한다. python-docx, lxml, matplotlib, Pandoc 및 Noto Sans CJK KR와 Latin Modern Math 글꼴이 필요하다. ZIP에서는 `python build_doc.py`로 실행한다. 실제 기본 셔터 시간은 이번 관측 간격 Δt에 배정하지 않았다.

## 판단 기준

**검증 입력 → WRRA 변환 → 계산 출력 → 수정 또는 기각 조건**을 기록한다. 질량의 수치 선별은 인용 표준불확도만 사용한 조건부 시험이며 전체 상관 통계 검정은 아니다. 고정한 판독이 추가 입자 응답을 재현하지 못하거나 색·전하·확률·에너지 보존 조건을 위반하면 해당 판독을 수정하거나 기각한다. 내부 상태와 환경을 늘릴 때에는 매개변수의 보정 출처를 고정하고 공통 커널로 다른 사례를 비교한다.

## English overview

This trial treats particle phenotypes as retained composite-fold states and decay as an internal reconfiguration. A finite mass-ratio scan produces 15 candidate address pairs; the same one-power readout fails the muon check and a shared uud/udd factor constraint. A calibrated valence-energy and signed-current response on the chosen 45/75 nucleon labels reproduces the supplied masses and magnetic moments.

Separate operators audit a supplied one-generation 15-chiral-channel carrier: color singlet response, weak raising, electric charge and three-spin addition. Ten algebraic checks pass. Force strengths, QCD binding, full spin-flavor state selection and microscopic decay matrix elements remain separate response work. The free neutron beta ledger preserves energy, charge, baryon and lepton number using the observed mean life, while source-return leakage is kept distinct.

[ORCID](https://orcid.org/0009-0001-4263-9772) · janefather@gmail.com · [Citation](CITATION.cff) · [CC BY 4.0](../../LICENSE)
