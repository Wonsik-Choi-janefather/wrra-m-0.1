# WRRA M reviewed 0 10 to 0 12 series

Latest reviewed release **0.12-r1** · [DOI](https://doi.org/10.5281/zenodo.23113101) · [English and Korean papers](review/0_10_to_0_12_r1/README.md) · [Corrections](REVISION_0_10_TO_0_12_R1.md)

The original overview follows for history.

# WRRA-M reviewed 0.7 to 0.9 series

Latest reviewed release 0.9-r1: https://doi.org/10.5281/zenodo.23091892 .

See [current overview](README.md), [review record](REVISION_0_7_TO_0_9_R1.md), and the bilingual 0.7, 0.8 and 0.9 papers under paper/. The material below retains the 0.6 historical overview.

# WRRA-M 0.6 정보부하와 뒤틀림 중력 및 팽창

최원식 Wonsik Choi · 2026-10-01 · CC BY 4.0

0.6은 유한·동질 구성 모형을 완료했다. 상태별 정보부하를 실제 계산하고, 같은 에너지 함수와 고전 배경 작용으로 상태 진화·압력·팽창·뒤틀림을 연결한다. 국소 회전·렌즈에는 그중 모이는 부하를 기존 보정 응답에 전달한다. WRRA Core 1.0과 MCC 2.3.2를 기준으로 유지한다.

| 단계 | 실행 내용 |
| --- | --- |
| 검증 입력 | 전체를 분모로 한 표현형 4.93%, 숨은 부하 95.07%, 모이는 부문 26.5%, 잔여 배경 68.57%; 기존 응답과 16채널 전달자 |
| WRRA 고유 변환 | 양의 부하 연산자의 상태 trace, 단일 에너지 함수, 부피 미분 압력, unitary 상태 갱신 및 동질 고전 작용 |
| 산출값 | 현재 q=-0.52855; 기존 aT=1.191812669e-10 m/s² 및 회전·렌즈 재현; 비가환 상태의 부하 변화와 상쇄되는 교환 |
| 반증조건 | trace·양의성 실패, 압력 미분 불일치, 총 보존 실패, 별도 가속도 해의 제약 위반, 같은 응답의 운동·렌즈 불일치 |

모이는 에너지 지수 nc=0, 배경 지수 nb=3, 부하 연산자와 정보 시계는 공개한 구성 선택이다. 압력과 보존은 그 선택에서 계산한 결과다. 실제 우주의 유일한 미시 법칙, 절대 우주 길이, 완전한 4차원 공변 국소 이론이나 공간 섭동의 안정성을 확정한 것은 아니다. 대칭 전달자 선택 격차는 0이다. 질량 표현형의 양자화와 근본 중력의 비양자 전제를 구분한다.

## 0.1–0.4 corrections / 0.1~0.4 수정

Correction r1 explicitly states complexification and independent Weyl-channel assumptions, the positive selection rate eta > 0 and nonzero target support, legitimate calibration provenance, and directly computed transport-Gram rank. Exact checks pass, including all 6,561 finite tables and 256 perturbation vertices. The 0.4 gap-eight construction and 0.5 gap-zero symmetric carrier are compatible. Stage 0.6 and its existing results are retained.

복소화·바일 채널 배정 가정, 양의 선택속도와 초기 지지, 보정 출처, 직접 계산한 랭크를 한영 원고에 명시했다. 기존 결과를 유지하며 네 검산 모두 통과했다.

- [Correction record / 수정 기록](REVISION_0_1_TO_0_4.md)
- [Reproduce 0.1–0.4 / 검산 실행](calculations/README_0_1_to_0_4.md)
- [Captured exact results](calculations/results/wrra_m_0_1_to_0_4)
- [Zenodo series release 0.6-r1](https://doi.org/10.5281/zenodo.23075976)

## 파일

- [0.6 한국어 PDF](paper/WRRA_M_0_6_KO.pdf) · [DOCX](paper/WRRA_M_0_6_KO.docx)
- [0.6 English PDF](paper/WRRA_M_0_6_EN.pdf) · [DOCX](paper/WRRA_M_0_6_EN.docx)
- [Complete reproducibility ZIP](paper/WRRA_M_0_6_Reproducibility.zip) · [Calculation directory](calculations/wrra_m_0_6)

## 재현

```bash
python -m pip install -r calculations/wrra_m_0_6/requirements.txt
python calculations/wrra_m_0_6/compute.py
python calculations/wrra_m_0_6/verify.py
```

compute.py는 parameters.json 및 baseline_0_5/parameters.json을 읽어 results/results.json과 요약·그림을 생성한다. verify.py는 0.5의 기록값, 기저 변환 및 경계 입력을 검사한다. 출력은 기본적으로 이 스크립트와 같은 디렉터리의 results에 저장된다. 다른 경로는 --out으로 지정할 수 있다. 원고 표를 다시 만들려면 기본 경로의 계산과 검사를 완료한 뒤 다음을 실행한다.

```bash
python calculations/wrra_m_0_6/write_papers.py
python calculations/wrra_m_0_6/build_reports.py
```

문서 생성에는 pandoc와 python-docx가 추가로 필요하다. 한글 출력은 Noto Sans CJK KR, 영문은 Liberation Serif/Sans 글꼴을 사용한다. Word 수식은 편집 가능한 네이티브 수식 22개이며, 두 언어는 동일한 수식·표 수치를 사용한다. PDF는 LibreOffice로 DOCX에서 변환했다.

전체 재현 ZIP에는 두 언어의 PDF·DOCX, 전체 궤도 results.json, 요약, 경계 검사, 그림, 원고와 코드가 포함된다. GitHub 계산 폴더에는 큰 전체 궤도를 제외한 요약·검사·그림을 제공하며 전체 궤도는 ZIP 또는 코드 실행으로 얻는다. baseline_0_5/results.json은 비교를 위해 고정한 수정된 0.5 기록이다.

정보 상태의 순수성·고윳값 보존은 unitary 구성의 결과다. 실험값과 맞는지에 대한 판단과 모형 내부 정합성 검사는 구분한다. 0.6 착수 모형의 고정 커널 제한은 기하 의존 에너지 연산자로 대체했으며 착수 기록은 별도 디렉터리에 보존한다.

---

# WRRA-M 0.5 한국어 개요

**정보부하와 뒤틀림 중력의 유한 계산**

최원식 Wonsik Choi · 2026년 10월 1일 · ORCID [0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772) · [janefather@gmail.com](mailto:janefather@gmail.com)

## 검증 입력 → WRRA 고유 변환 → 산출값 → 반증조건

| 단계 | 0.5의 내용 |
| --- | --- |
| 검증 입력 | 최소계산우주론 2.3.2, 0.4의 전달자 조건, 기존 WRRA 은하 원반면 논문에서 실제 채택한 구성응답과 변경 가능한 관측 보정값. |
| WRRA 고유 변환 | 이산 질량 표현형과 상류의 연속 기하 응답을 구분하고, 동일한 뒤틀림 응답으로 운동과 조건부 렌즈를 계산하며, 고정한 동질 16채널 전달자를 평가한다. |
| 산출값 | 전환 가속도 1.191812669 × 10⁻¹⁰ m/s², 유한 구형 응력과 회전속도, 200 kpc 패치의 조건부 렌즈 편향, 기존 우리은하 대수 계산의 선형화 Eilers 기준 대비 RMS 2.41784 km/s 재현, 수송 랭크 16 및 두 선택 격차 0. |
| 반증조건 | 수송 그람의 양의성·랭크 실패, 주장한 양의 선택 격차 미성립, 정적 구성응답의 음의 고유값, 같은 기하에서 운동과 렌즈의 불일치가 해당 주장의 기각·수정 조건이다. |

## 범위와 결과

0.5는 질량은 표현형이므로 양자화 가능하고 중력은 표현형 이전이므로 근본 양자자유도를 갖지 않는 B_C 가지를 모형 전제로 선택한다. 이를 중력 비양자화의 보편적인 실험·수학 증명으로 분류하지 않는다.

팽창과 뒤틀림을 동시에 둔다. 이번에 실행한 범위는 현재의 정적 뒤틀림 응력이며, 팽창 동역학은 후속 계산으로 남긴다. 표현형으로 출력되지 않은 정보의 에너지 가중 부하를 이차 응력 관계로 꼬임과 연결했다. 선언한 T³ 접합 예시는 유한하지만 경계 없는 공간의 조건부 구성을 주며, 실제 우주의 위상이나 크기를 확정하지 않는다.

기존에 보정한 구성응답을 WRRA 내부에 실제 넣어 계산했다. 공통전달자로부터 그 함수가 유일하게 유도되었다고 주장하지 않는다. 동질 전달자는 수송 조건을 통과하지만 ΔL = ΔR = 0이므로 목표 필터를 유일하게 선택하지 못한다. 양의 선택을 만드는 채널별 응답 차이는 아직 미해결이다.

약 5%와 95%는 변경 가능한 추정값이다. 전체 숨은 부하와 국소 추가 인력 척도에 사용하는 모이는 응력 부문을 구별한다.

## 파일과 재현

- [한글 PDF](paper/WRRA_M_0_5_KO.pdf) · [한글 DOCX](paper/WRRA_M_0_5_KO.docx)
- [영문 PDF](paper/WRRA_M_0_5_EN.pdf) · [영문 DOCX](paper/WRRA_M_0_5_EN.docx) · [영문 Markdown 원고](paper/WRRA_M_0_5_EN.md)
- [한글 Markdown 원고](paper/WRRA_M_0_5_KO.md)
- [전체 재현 ZIP](paper/WRRA_M_0_5_Reproducibility.zip)
- [계산 디렉터리](calculations/wrra_m_0_5) · [결과 장부](calculations/wrra_m_0_5/results/results.json)

영문 전체 번역본도 제공한다. 한글 원고의 수식 15개와 수치표 19개 행을 그대로 보존했다.

- [영문 재현 ZIP](paper/WRRA_M_0_5_Reproducibility_EN.zip)
- [영문 문서 생성기](calculations/wrra_m_0_5/build_report_en.py)

```bash
python -m pip install -r calculations/wrra_m_0_5/requirements.txt
python calculations/wrra_m_0_5/compute.py --out calculations/wrra_m_0_5/results
```

렌즈는 Φ = Ψ 조건과 200 kpc 패치 내부의 기여만 계산했다. 우리은하 RMS는 기존 선형화 기준과의 비교이며 실제 개별 관측점을 새로 적합한 결과가 아니다. 공변 작용 완성과 양자 물질·고전 기하의 혼합 갱신법칙은 후속 범위다.

CC BY 4.0. 이전 0.1–0.4 자료는 계속 제공한다.

---

# WRRA-M 0.4 한국어 개요

## 연구 결정

WRRA-M 0.4는 최소계산우주론의 공통전달자가 WRRA-M 0.3에서 미정으로 남은 적합도 규칙을 소유할 수 있는지 검토한다. 결론은 조건부로 가능하다는 것이다. 다만 기존 15채널 전달자를 그대로 16채널 해답이라고 부를 수는 없다.

## 검증 입력

0.2는 다음의 16채널 공간을 제시했다.

\[
\mathcal C_{16}=\mathbf1_0\oplus\mathbf7_A\oplus\mathbf7_B\oplus\mathbf1_N.
\]

0.3은 고정된 네 필터 집합 안에서 목표 필터가 유일하게 선택되는 필요충분조건을 증명했다.

\[
\Delta_L>0,\qquad\Delta_R>0.
\]

최소계산우주론은 표준모형의 15개 카이럴 채널이 공유하는 공통 수송 구조를 제공한다.

## WRRA 고유 변환

0.4는 공통전달자를 게이지 중성인 한 채널만큼 조건부로 확장한다.

\[
\mathcal H_{16}=\mathcal H_{15}\oplus\mathcal H_N.
\]

16개 채널이 하나의 주된 인과기하를 공유하고, 선언한 대역에서 응답 그람 연산자가 양의 준정부호이면서 완전계수 16을 가지며, 중성 채널의 전달자 노름이 양수여야 한다. 게이지 전류에 대한 중성과 수송의 부재는 구별해야 한다.

목표 결과와 독립적으로 고정한 응답 서명에 대해 다음 하나의 규칙을 둔다.

\[
c_C(i,j)=-\lVert u_i-u_j\rVert_C^2.
\]

그러면 자유변수였던 두 선택 간극이 정확히 다음의 정렬값으로 줄어든다.

\[
\Delta_L=2\operatorname{Re}\langle u_{3_A}-u_{3_B},u_{1_A}-u_{1_B}\rangle_C,
\]

\[
\Delta_R=2\operatorname{Re}\langle u_{\bar3_A}-u_{\bar3_B},u_{1_N}-u_{1_0}\rangle_C.
\]

## 산출값

기존 공통전달자 발상은 실제 15→16채널 확장을 거치면 WRRA-M에서 구조적으로 재사용할 수 있다. 하나의 양의 응답 계량이 자유로운 적합도 8개를 하나의 규칙과 계산해야 할 응답 서명 8개로 바꾼다. 정확한 유한 예시는

\[
\Delta_L=\Delta_R=8
\]

을 주어 양의 간극 영역이 비어 있지 않음을 증명한다.

## 반증조건

중성 채널이 수송 커널에 들어가거나, 채널에 따라 인과원뿔이 갈라지거나, 응답 그람 연산자가 양의 준정부호 또는 완전계수가 아니거나, 응답 구성이 게이지 불변이 아니거나, 독립적으로 고정한 전달자에서 두 정렬 중 하나가 0 이하이거나, 목표를 확인한 뒤 프로토콜을 바꾸면 0.4의 연결은 실패한다.

## 정확한 경계

유한 예시는 구성 가능성만 증명한다. 0.4는 미시적 전달자에서 물리적 응답 서명을 수치로 계산하지 않으며 자연이 양의 정렬을 준다고 주장하지 않는다. 0.5에서 동질 전달자의 수치 계산을 실행해 두 격차 0을 얻었다. 양의 선택을 주는 미시 응답은 여전히 미해결이다.

## 파일

- [한글 본문 PDF](paper/WRRA_M_0_4_KO.pdf)
- [한글 본문 DOCX](paper/WRRA_M_0_4_KO.docx)
- [한글 Markdown 원고](paper/WRRA_M_0_4_Common_Carrier_Metric_Origin_KO.md)
- [영문 본문 PDF](paper/WRRA_M_0_4_EN.pdf)
- [영문 본문 DOCX](paper/WRRA_M_0_4_EN.docx)
- [영문 Markdown 원고](paper/WRRA_M_0_4_Common_Carrier_Metric_Origin_EN.md)
- [정확 검증 스크립트](calculations/verify_wrra_m_0_4.py)
- [English overview](README_EN.md)
- [0.3 한국어 PDF](paper/WRRA_M_0_3_KO.pdf)

## 저자 정보

최원식 Wonsik Choi · ORCID [0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772) · [janefather@gmail.com](mailto:janefather@gmail.com)



## 검토 반영 및 0.6 착수

국소 계산 부문은 우주 전체 기준 26.5%이며, 숨은 전체 95.07% 안의 부분이다. 0.5의 정보부하 사상은 구성 가설이고 개별 정보 상태 가중치는 계산하지 않았다. 표현형 비율 0도 실행되며 정의할 수 없는 원천비는 null로 기록한다. 반경 응답비는 두 가속도 값을 계산해 산출한다. 기존 운동·렌즈·전달자 결과는 그대로 재현됐다.

[0.6 범위와 착수 계산](calculations/wrra_m_0_6_start/README_KO.md)은 선언한 전달자 부하 연산자를 실제로 계산하고 배경 압력 구성을 비교한다. 착수 모형의 역사적 기록이며, 완성된 유한 동질 0.6 원고는 위에 제공한다.
