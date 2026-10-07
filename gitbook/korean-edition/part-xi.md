# **제11부 3.0의 하류 실행 - 정보부하에서 우주 팽창까지**

제10부가 생성의 중간층을 닫았다면, 제11부는 그 결과가 기존 WRRA_M의 SI 에너지·압력·중력·은하·우주 팽창 계산으로 어떻게 내려가는지를 3.0의 finite SOURCE branch에서 다시 확인한다.

# **59장 정보부하와 에너지**

Stage 4의 핵심은 component를 발견했다고 우주 에너지를 새로 더하지 않는 것이다. cosmic additive ledger는 오직

$$\boxed{\phi \oplus D \oplus R}$$

이다.

주소응답은

$$g_{s}(n) = 1 + \lambda_{s}\frac{\log n}{\log N_{U}},\quad\quad\left( \lambda_{\phi},\lambda_{D},\lambda_{R} \right) = (0,0.25,0.1).$$

address moment는 $\mu_{s} = \sum_{n}^{}w_{n}e_{s}(n)g_{s}(n)$이며 finite SOURCE에서

(μ_φ, μ_D, μ_R) =  
(0.0500000000000001, 0.278925610976744, 0.687742539854239)

SI 계수는 WRRA_M reference에서 한 번 보정된 값을 그대로 고정한다.

η_φ = 7.561582499072265×10^-10  
η_D = 7.285761328795971×10^-10  
η_R = 7.646102818811323×10^-10 J m^-3

기준부피 $V_{0} = 1\, m^{3}$에서

$$E_{\phi} = 3.78079124953614 \times 10^{- 11}J,$$

$$E_{D} = 2.03218543006515 \times 10^{- 10}J,$$

$$E_{R} = 5.25855017259595 \times 10^{- 10}J,$$

$$\boxed{E_{total} = 7.668814727614716 \times 10^{- 10}J}.$$

Prime-Parts small-first, large-first, 48 field/channel slots는 모두 phenotype의 내부분해다. 한 view의 normalized component fraction을 $c_{j}$라 하면 $\mu_{\phi,j} = \mu_{\phi}c_{j}$, $E_{\phi,j} = \eta_{\phi}\mu_{\phi,j}$이고 $\sum_{j}^{}E_{\phi,j} = E_{\phi}$다. internal view를 cosmic total에 다시 더하는 것은 금지된다.

# **60장 중력과 뒤틀림**

구정아 전시에서 출발한 선행연구는 전체에 걸쳐 누적되는 꼬임을 twist stress의 개념적 owner로 제안했다 \[3.0-R1\]. 이후 WRRA twist-stress 연구에서는 dark mass phenotype을 spatial stress의 중력적 표현으로 해석하고, 우주 규모 fraction과 은하 low-acceleration scale을 연결했다 \[3.0-R5\].

MCC 3.0은 이 아이디어를 독립 force로 추가하지 않는다. 하나의 energy/load ledger에서 resident nonphenotype D가 국소 추가중력 response를 소유하도록 한다.

동결된 local clustering reference $f_{c} = 0.265$에 대해

$$a_{T,0} = cH_{0}\sqrt{\frac{f_{c}}{8}}$$

를 기준으로 하고, candidate state에서는

$$a_{T} = a_{T,0}\sqrt{\frac{\rho_{D}}{u_{crit}f_{c}}}.$$

현재 $a = 1$에서

$$\boxed{a_{T} = 1.1917875313971119 \times 10^{- 10}\ m\, s^{- 2}}.$$

이 $a_{T}$ 하나가 rotation과 lensing에 같이 들어간다.

# **61장 은하 회전과 렌즈**

Stage 5에서는 동일한 finite-SOURCE D load를 Plummer reference source에 전달한다. 시험 source는 mass $6 \times 10^{10}M_{\odot}$, scale radius 3 kpc, test radius 8.2 kpc, lens patch radius 200 kpc, impact 10 kpc이다.

현재 $a = 1$에서 직접 baryonic rotation은 $161.4505105\ km\, s^{- 1}$이다. 같은 $a_{T}$를 적용한 total reference rotation은

$$\boxed{207.5102419\ km\, s^{- 1}}.$$

동일한 중력 response를 조건부 finite-patch lens calculation에 넣으면

$$\boxed{0.5355822400''}$$

를 얻는다.

legacy $N = 1,000,000$과의 차이는 $\Delta v = - 6.63261 \times 10^{- 4}\ km\, s^{- 1}$, $\Delta\theta = - 4.27055 \times 10^{- 6}''$이다. 이 값들은 새 astronomical measurement가 아니라 기존 동결 renderer가 새 finite SOURCE에서도 깨지지 않는지 보는 continuity output이다.

# **62장 우주 팽창**

volume exponent는 $\left( n_{\phi},n_{D},n_{R} \right) = (0,0,3)$으로 상속한다. 따라서

$$\rho_{\phi}(a) = \frac{E_{\phi}}{a^{3}},\quad\quad\rho_{D}(a) = \frac{E_{D}}{a^{3}},\quad\quad\rho_{R}(a) = E_{R}.$$

pressure는 $P_{\phi} = P_{D} = 0$, $P_{R} = - \rho_{R}$이다. total density에서

$$\frac{H(a)}{H_{0}} = \sqrt{\frac{\rho(a)}{u_{crit}}},\quad\quad q(a) = \frac{1}{2}\frac{\rho(a) + 3P(a)}{\rho(a)}$$

를 계산한다.

| **a** | **ρ (J/m³)**     | **H/H0**     | **q**         |
|-------|------------------|--------------|---------------|
| 0.5   | 2.4540666613e-9  | 1.7888556123 | 0.1785814590  |
| 1.0   | 7.6688147276e-10 | 0.9999913260 | -0.5285585894 |
| 2.0   | 5.5598332420e-10 | 0.8514575347 | -0.9187161585 |

전환조건 $q = 0$으로부터

$$\boxed{a_{trans} = 0.6119598067968817}$$

를 얻는다.

# **63장 proper-time과 기록**

WRRA_M 0.12는 event/order discreteness와 physical minimum time을 구분한다 \[3.0-R3\]. MCC 3.0은 이 구분을 유지한다.

상속된 proper-time step은

$$\Delta\tau = 1.4813019664158691 \times 10^{- 21}s$$

이다. 이 값은 Planck time이 아니며 우주의 절대 최소 시간이라고 주장하지 않는다.

finite carrier의 noncommuting update에서 내부 D/R load는 변하지만 전체 에너지는 수치정밀도 안에서 보존된다. KZF candidate의 최대 relative energy drift는

$$\boxed{9.99 \times 10^{- 16}}$$

수준이다. state trace도 1을 유지한다.

MCC는 현재 실행과 Record를 구분한다. 그러나 autonomous physical apparatus가 실제 irreversible record를 만드는 full measurement dynamics는 아직 3.0의 완료항목이 아니다.

# **64장 End-to-End Master Ledger**

MCC 3.0의 최종 실행사슬은

finite rule → finite addresses → prime/composite filter  
→ residue → component/phenotype

→ information load → energy → pressure/gravity  
→ rotation/lensing → expansion

이다.

| **단계**         | **소유 정보**          | **additive 여부**    |
|------------------|------------------------|----------------------|
| finite SOURCE    | L,H,C,N_U              | 주소생성             |
| address filter   | φ,D,R share            | normalized partition |
| component views  | prime/channel 내부구성 | nonadditive          |
| SI ledger        | Eφ,ED,ER               | additive             |
| pressure         | same ER                | derived              |
| local gravity    | same D density         | derived              |
| rotation/lensing | same a_T               | derived              |
| expansion        | same sector densities  | derived              |

이 구조가 3.0의 핵심이다. 서로 다른 설명을 같은 우주에 적용한다고 해서 별도의 에너지나 중력을 다시 만들지 않는다.

# **65장 검증값 재현**

legacy $N = 1,000,000$ 장부는 $(0.05,0.268,0.682)$를 재현한다. reference macro output은

$$q_{0} = - 0.52855,\quad\quad v = 207.5109051266\ km\, s^{- 1},\quad\quad\theta = 0.5355865106''.$$

MCC 3.0 finite SOURCE branch는

$$q_{0} = - 0.5285585894,\quad\quad v = 207.5102418659\ km\, s^{- 1},\quad\quad\theta = 0.5355822400''.$$

legacy 대비 현재값 상대변화는 q 약 1.63×10^-5, rotation 3.20×10^-6, lensing 7.97×10^-6이다.

repository에 공개된 검사는 Stage 1: 5, Stage 2: 7, Stage 3: 16, Stage 4: 12, Stage 5: 14, Stage 6 cross-stage: 11로 총

$$\boxed{65}$$

개다. 모두 PASS다. 이는 65개의 독립 물리실험을 뜻하지 않고 계산, 구현, provenance, 장부 일치 검증의 합이다.

# **66장 WRRA/MCC 예측값**

## **66.1 finite SOURCE size**

$$\boxed{N_{U} = 1,015,000}$$

은 선언된 $N_{U} = LHC$ 규칙을 고정한 뒤 산출한 미측정량이다. 따라서 현재 지위는 **conditional MCC/WRRA prediction**이다. 단, LHC의 유일성이 아직 OPEN이므로 fundamental constant로 확정하지 않는다.

## **66.2 acceleration-transition scale**

현재 uniform constitutive branch에서

$$\boxed{a_{trans} = 0.6119598068}$$

이 나온다. 이는 frozen energy/pressure law의 derived output이다.

## **66.3 중성미자 absolute mass 후보의 상속**

MCC 2.3.2에서 observation-guided harmonic ledger (0,5,29)를 고정한 후

$$m_{1} = 0,\quad m_{2} = 8.62965\ meV,\quad m_{3} = 50.05195\ meV,$$

$$\sum m_{\nu} = 58.6816\ meV$$

를 frozen holdout prediction으로 기록했다 \[3.0-R2\]. MCC 3.0은 이 값을 새로 도출한 것이 아니라 H=29를 finite SOURCE generator에 상속했다.

# **67장 열린 가정과 반증조건**

다음은 OPEN이다.

- $T = 2\pi H$가 유일한 physical phase boundary인가?

- $L,H,C$가 정말 독립 Cartesian coordinate인가?

- $N_{U} = LHC$ 외의 동일하게 단순한 closure가 있는가?

- Klein형 orientation reversal이 실제 우주 topology와 관련있는가?

- zeta-focus가 물리적 microscopic mechanism인가, 수학적 organizing rule인가?

- Prime-Parts가 particle species를 유일하게 정하는가?

- full spin/flavor/confinement/binding Hamiltonian을 WRRA 내부에서 닫을 수 있는가?

- baryon/lepton asymmetry의 생성자가 무엇인가?

- full covariant background + inhomogeneous perturbation theory가 가능한가?

- autonomous measurement/record dynamics를 같은 ledger에서 닫을 수 있는가?

MCC 3.0은 다음 중 하나가 발생하면 수정되어야 한다.

- KZF가 frozen rule에서 N_U=1,015,000을 재현하지 못한다.

- finite SOURCE insertion 후 address effects가 음수 또는 불완전해진다.

- 동일한 두 arithmetic calibration으로 장부를 닫을 수 없다.

- 숨은 세 번째 fit이 필요해진다.

- component internal view가 추가 cosmic energy로 중복계상된다.

- same state에서 rotation과 lensing이 서로 다른 a_T 보정을 요구한다.

- proper-time update가 energy/trace를 보존하지 못한다.

- Stage 1–6 handoff가 서로 다른 값을 소유한다.

- 문서의 식과 실행코드가 다르다.

- OPEN으로 기록한 microscopic rule이 실제 계산을 위해 필수인데 일관된 closure를 제공할 수 없다.

필요한 계산이 정의되지 않으면 OPEN으로 남긴다. undefined를 PASS로 처리하지 않는다.

## 67.1 표준물리와 수렴하는 영역

MCC 3.0은 표준모형·일반상대론·FLRW가 이미 정밀하게 계산하는 영역에서 무조건 다른 숫자를 내는 것을 목표로 하지 않는다. 동일한 입력·경계조건·Reality 계산 모듈을 채택하는 범위에서는 같은 관측값으로 수렴하는 것이 정상이다. 이 영역의 성과는 “새 수치”보다 SOURCE·공통운반자·component·phenotype·중력의 소유권과 실행 순서를 한 장부에 연결하는 데 있다.

## 67.2 WRRA/MCC가 달라질 수 있는 영역

독립적인 판별력은 WRRA 고유 구조가 표준 해석과 다른 물리적 의존성을 만들 때 생긴다. 현재 원고에서 가장 분명한 후보는 경계조건에 민감한 중력응답, 같은 D-sector가 동시에 소유하는 rotation/lensing, 비구면 응력 분포, 전역 holonomy 상관, 그리고 finite SOURCE perturbation이 frozen downstream coefficient를 통과해 거시 출력까지 전달되는 경로다. 아래 표는 “이미 같은 계산을 상속하는 영역”과 “향후 실제 판별 시그니처가 될 수 있는 영역”을 분리한다.

| **영역**                | **현재 관계/등급**                                             | **판별 조건 또는 시그니처**                                                                               |
|-------------------------|----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| 입자 산란·붕괴          | 표준모형 계산 상속 / 해석·소유권 통합                          | 같은 S-matrix 영역에서는 차이를 강제하지 않음; component decoder가 고정 규칙으로 새 제약을 내면 판별 가능 |
| 우주 배경 팽창          | FLRW 입력 상속 + 3.0 finite-SOURCE branch의 DERIVED q, a_trans | 사전 동결한 장부로 q(a), transition scale을 데이터에 비교하고 추가 dark-energy 재보정이 필요하면 실패     |
| 은하 회전 + 렌즈        | 같은 D-sector, 같은 a_T를 공유                                 | 회전과 렌즈가 서로 다른 별도 a_T 또는 독립 정규화를 요구하면 현재 연결이 실패                             |
| 경계조건 민감 중력      | OPEN 판별 후보                                                 | δg(x)/δB_boundary(y) ≠ 0 형태의 비국소 응답이 재현 가능하게 나타나는지 시험                               |
| 충돌 은하단·비구면 렌즈 | OPEN 판별 후보                                                 | 바리온 중심과 stress/lensing 중심의 상대 이동, 비구면 shear 패턴이 하나의 응력 규칙으로 설명되는지 시험   |
| 전역 위상·holonomy      | OPEN 판별 후보                                                 | matched-circle/반복영상/거리상관 등 전역 접합의 재현 가능한 상관이 존재하는지 시험                        |
| finite SOURCE 상류 교란 | CONDITIONAL / 내부 민감도 확보                                 | 상류 population을 바꿨을 때 frozen SI 계수 아래 q·rotation·lensing이 예측된 방향으로 함께 이동해야 함     |

## 67.3 OPEN·CALIBRATED에서 독립 예측으로 승격되는 조건

• 관측자료를 보기 전에 관련 입력, 보정 자유도, owner와 readout rule을 동결한다.

• 같은 물리 상태를 회전·렌즈·팽창처럼 여러 데이터 영역에 전달할 때 영역별 숨은 재보정을 허용하지 않는다.

• 효과의 부호·크기·스케일 의존성을 미리 산출하고, 측정 불확실도보다 작다면 독립 예측이 아니라 해석 또는 내부 민감도로 분류한다.

• 표준모형과 같은 수치를 내는 영역은 “예측 성공”으로 중복 계산하지 않고 현실 정합성·모듈 상속으로 기록한다.

• 반복 가능한 관측이 사전 동결된 WRRA 조건부 출력과 유의하게 불일치하면 해당 인터페이스를 수정하거나 기각한다.
