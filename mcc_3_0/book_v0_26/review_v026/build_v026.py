from pathlib import Path
import json,re,hashlib,difflib
HERE=Path(__file__).resolve().parent
P=HERE.parent if HERE.name=='review_v026' else HERE/'book_v0_26'
R=P/'review_v026';R.mkdir(exist_ok=True)
S=P if HERE.name=='review_v026' else HERE.parent/'book026_source'
chapter_ko=r'''## 136장 잔여 씨앗에서 유한 방출·열역사·관측 계산까지

### 136.1 검증 입력과 판본의 소유권

이 장은 v0.25-r5의 기존 1–135장과 예술적 서두를 유지하면서, 2026년 10월 20일 공개한 잔여·CMB 연결 연구 v0.4, v0.5, v0.6, v0.7-dev-r1을 책의 계산 계보에 추가한다. 책의 편집 번호 v0.26과 개별 계산의 버전 번호는 서로 다른 번호다. 이 장은 해당 원전의 실행 기록을 통합 편집하며, 책 갱신 자체를 새 물리 계산이나 관측 확증으로 세지 않는다.

검증 입력은 기존 양자화에서 얻은 128셀 씨앗, 실제 진화한 64개 파수 모드, 보정된 배경·고유 시간, 관측 상수와 전자·양전자 EOS, 공개된 SPT–Planck 렌징 관측량·공분산·창 함수다. 실제 계산 파일의 소유권은 아래 원전과 GitHub의 각 경로에 있다. 알려진 상수와 관측값의 도입 및 그에 따른 모형 수정은 정당한 구성·보정이다.

| 계산 원전 | 실행한 WRRA 연결 | 원전 검사 기록 | 현행 범위 |
|---|---|---|---|
| v0.4 | 유한 파수 전환·메트릭·운동량·자유 비행 중성미자와 같은 구성계의 보존 접합 | 643개 | 선형 진폭, 64모드; 생산용 CAMB 전체 상태 주입은 아님 |
| v0.5 | 유한 패킷 방출 시각·기록 허가·열 비용·국소 팽창 | 444개 및 발행 검산 12개 | 독립 국소 FLRW 셀; 유한 파수 사건 진화는 아님 |
| v0.6 | WRRA 배경의 조건부 비선형 렌징·우도 및 별도의 MeV 열역사 | 54개 및 발행 검산 8개 | 선언한 보정 원시 스펙트럼 완성과 열역사 계산 |
| v0.7-dev-r1 | 64모드 좌표 변환·방출 시각 접선·열역사 밀도 보정·안정적 메트릭 조합 | 472개 및 발행 검산 10개 | 전체 상태 접합의 부분 구현 |

이 검사 수는 서로 독립적인 관측 증거의 개수가 아니다. 각 원전의 보존·정규화·수렴·대조 검사 기록이다. 같은 자료의 재실행을 새로운 우주 관측으로 세지 않는다. 기존 실제 SOURCE CMB 분기의 산출을 이 장의 조건부 v0.6 분기로 대체하지도 않는다.

### 136.2 WRRA 고유 변환: 유한 구배와 보존 접합

v0.4는 잔여 씨앗의 전환율 변조를 유효 상대론적 저장 부문에서 먼지형 물질 부문으로 전달한다. 동기 게이지 메트릭, 각 부문의 밀도·운동량과 질량 없는 자유 비행 중성미자 계층을 함께 적분했다. 물리적 파수는 $k=0.05,0.10,\ldots,3.20\ {\rm Mpc}^{-1}$의 64개이며, 저장된 중성미자 모멘트는 $F_{\nu0}$부터 $F_{\nu12}$까지다. 유한 공간 구배를 유지하지만 섭동 진폭에는 선형인 계산이다.

전달 법칙은 전체 스트레스–에너지의 보존을 요구한다.

$$\nabla_\mu T_A^{\mu\nu}=Q_A^\nu,\qquad \sum_A Q_A^\nu=0.$$

메트릭·운동량을 버리고 엔트로피 하나만 전달하지 않는다. 남은 유효 완전복사를 광자형 완전복사에 합칠 때도 밀도와 운동량을 함께 옮기고 중성미자 계층을 유지했으며, 같은 입자 구성계에서 접합 뒤의 진화를 실제로 비교했다. 이는 두 모멘트 유체 대체를 넘은 유한 구배 연결 성과다. 실제 입자종의 생성 반응률, 바리온·광자 긴밀 결합과 질량 중성미자의 전체 분포를 자동으로 생성한 계산은 아니다.

### 136.3 유한 방출 시각과 기록 비용

v0.5는 기준 셀의 가변 복사 예산을 256분할하고, 누적 전달 신용이 패킷 문턱에 이르며 기록 허가가 있을 때 방출한다. 신용은 별도의 에너지 저장고가 아니다. 자원이 닫히면 신용 생성을 멈추며 펄스 끝에 남은 신용을 강제 방출하지 않는다. 기준 실행에서는 128회 사건이 발생했다.

$$\dot r=\Gamma(1+\xi)C,\qquad r=q\ \hbox{and recording permission}\ \Longrightarrow\ \hbox{emission}.$$

$$C^+=C^--q,\qquad M^+=M^-+\frac{(1-\epsilon)q}{a_j},\qquad J^+=J^-+\epsilon q.$$

여기서 $q$는 기준 셀의 공변 복사 에너지 차감량이고 $\epsilon=0.01$은 선언한 기록 열 비용이다. 이 패킷을 보편적인 입자 정지에너지나 새 기본 양자로 해석하지 않는다. $C,M,J$의 물리적 에너지 희석률이 다르므로 $a_j$를 생략하면 보존이 깨진다. 열역사에서는 $J$를 단순 완전복사 상수로 대신하지 않고 전자·양전자의 실제 열용량을 통해 온도 증가로 바꾼다.

첫 사건과 마지막 사건의 고유 시간은 각각 약 0.00268883초와 0.475779초다. 0.47712081326446576초라는 이 계산의 고유 시간 단위는 별도의 보정된 초기 우주 시간이며, 기존 미시 셔터 시간과 동일시하지 않는다. 고정 패킷 수에서 작은 씨앗의 응답과 패킷 크기를 0으로 보내는 연속 한계의 순서는 중요하다. 따라서 연속 전환의 응답을 유한 방출에 그대로 복사하지 않는다.

### 136.4 관측 우도와 MeV 열역사의 실제 산출

v0.6의 관측 분기는 기존 WRRA dark-weight-only 배경 $H_0=67.2568374662005$, $\omega_b=0.022395806792949086$, $\omega_c=0.12037806177378184$에서 실행했다. 초기 원시 스펙트럼은 선언한 보정값 $A_s=2.1\times10^{-9}$, $n_s=0.9649$의 표준 단열 완성이다. $\tau=0.0544$, $N_{\rm eff}=3.044$, $T_{\rm CMB}=2.7255$ K도 입력이다. CAMB 2.0.4와 채택한 HMCode 2020 처방으로 비선형 렌징을 계산하고 공개 SPT–Planck 18빈의 전체 공분산과 TT/PP 응답 보정을 사용했다.

$$b=(W+R_{PP})D^{\phi\phi}+R_{TT}D^{TT}-f,\qquad
\chi^2=(b-d)^T\Sigma^{-1}(b-d).$$

| 선언한 비교 | 18빈 고정 모형의 $\chi^2$ |
|---|---:|
| 선형 렌징 | 11.6855836908 |
| 채택한 비선형 렌징 | 10.6060135496 |
| 정확도 강화 비선형 렌징 | 10.6032279730 |

독자 우도 구현은 별도 공식 CosmoMC 구현과 최대 $1.60\times10^{-14}$ 차이로 일치했다. 수치 강화의 관측 공분산 거리는 약 0.00383078 sigma다. 이는 WRRA 배경과 선언한 원시 준비의 조건부 관측 비교다. v0.4 전체 상태와 v0.5 사건 섭동을 이 CAMB 실행에 주입한 결과는 아니다. 알려진 준비를 사용한 재현·설명 성과를 인정하면서, 실행하지 않은 연결까지 통합되었다고 부르지 않는다. HMCode는 채택한 경험 처방이며 새 WRRA 비선형 법칙의 유도가 아니다. 우도 꼬리확률을 이론이 참일 확률로 해석하지 않는다.

별도의 유한 방출 열역사는 유한 질량 전자·양전자 평형 EOS와 선언한 즉시 상대론적 중성미자 분리 분기를 사용한다. 같은 고유 시간 단위를 유지하면 초기 광자 온도는 1.7584850895 MeV, 현재 광자 엔트로피에 연결한 초기 축척은 $a_i=9.55163454815\times10^{-11}$이다. 이전 $10^{-10}$보다 약 4.48% 작다. 따라서 시간 단위·축척·입자 구성 모두를 이전 값으로 고정한 채 열역사를 덧붙일 수 없다.

| 광자 온도 | 펄스 시작 뒤 경과 시간 |
|---|---:|
| 1 MeV | 0.5045894421초 |
| 0.5 MeV | 2.8257151242초 |
| 0.1 MeV | 118.6213275533초 |

이 시간은 우주의 절대 나이가 아니다. $N_{\rm eff}$는 입력이며 중성미자 충돌 적분·풍미 수송·약한 상호작용 동결·BBN 원소 수율은 계산하지 않았다. 표준 우주론 자료는 검증·보강에 쓰되, 최종 WRRA 내부에서 실제 실행한 연결만 실행 성과로 집계한다.

### 136.5 전체 상태 접합의 개발 성과와 수치 수정

v0.7-dev-r1은 v0.4의 사용 가능한 64모드 전체 스칼라 상태를 전환 뒤 CDM 정지 동기 게이지로 옮겼다. 속도만 0으로 삭제하지 않고 밀도·메트릭 도함수·중성미자 단극과 쌍극을 함께 바꾼다.

$$\alpha=\frac{\theta_m}{k^2},\quad
\theta_i^c=\theta_i-k^2\alpha,\quad
\delta_i^c=\delta_i+3(1+w_i){\cal H}\alpha,\quad
\eta^c=\eta+{\cal H}\alpha.$$

변환 뒤 Hamiltonian 제약과 운동량 제약의 정규화 잔차는 각각 최대 $3.29\times10^{-16}$, $4.31\times10^{-16}$였다. 다만 큰 도함수 두 개를 따로 반올림한 뒤 작은 조합을 복원하면, 낮은 파수에서 Bardeen 퍼텐셜의 상대오차가 최대 약 16.66%에 이르렀다. r1은 원래의 스케일된 전단 $g$와 게이지 이동에서 그 조합을 직접 보존한다.

$$h^{c\prime}+6\eta^{c\prime}=2k^2(g/2+\alpha).$$

안정적인 조합을 사용한 퍼텐셜의 게이지 불변성은 64모드 모두에서 상대오차 $4.35\times10^{-12}$ 이내였다. 단순 도함수 차감은 실패 대조군으로 남겼다. 별도 도함수는 반올림된 진단값이며, 향후 실제 CAMB 운반에서도 안정적인 제약 평가를 검증해야 한다.

별도로 v0.5/v0.6의 국소 셀 모형에 사건 시각의 미분을 포함했다. 같은 시간면에서의 접선 $z=\partial y/\partial\xi$는 사건 리셋 $R$에서 다음과 같이 바뀐다.

$$z^+=DR\,z^-+(DR\,f^--f^+)t_j',\qquad t_j'=-\frac{t_j}{1+\xi}.$$

유한 방출·열역사의 $k=0$ 엔트로피 응답은 0.194818034056이며, 연속 전환의 0.723567385056과 다르다. 원래 씨앗을 진폭 재맞춤 없이 적용한 엔트로피 RMS는 $4.80262944810\times10^{-9}$다. 독립 시간좌표 $u=(1+\xi)t$로 사건을 고정한 접선 적분은 이 응답과 상대 $8.39\times10^{-9}$ 이내로 일치했다. 이 국소 접선을 유한 파수의 전체 상태로 대체하지 않는다.

기존 전환량을 열역사의 물리 단위로 환산한 암흑물질 밀도는 $\omega_c=0.103663511129$로, 후단 목표보다 약 13.885% 낮았다. 해당 분기의 전환 분율 $\beta$를 $7.62452468358\times10^{-7}$에서 $8.85389093544\times10^{-7}$로 보정하면 기존 목표를 재현한다. 이는 정당한 배경 보정이다. 이 $\beta$는 초기 가변 복사 분율이며 책의 기존 우주 구성비나 다른 장의 같은 기호와 동일하지 않다. 보정 배경에서 64개 모드 전체를 다시 진화한 계산은 아직 없으며, 기존 구성비·셔터·은하·GR/CMB 분기의 수치를 소급하여 바꾸지 않는다.

### 136.6 반증조건과 다음 접합의 정확한 범위

이 계보의 반증·수정 조건은 전체 보존 또는 Einstein 제약의 실패, 게이지 불변량·중성미자 정규화의 불일치, 방출 시각·수령 운동량·기록 열의 누락, EOS·시간·계층 절단에 대한 비수렴, 우도 공분산·관측 창·정규화의 오류와 선언한 관측 비교의 실패다. 매번 입력과 준비를 공개하고 같은 기준을 기존 이론과 WRRA에 적용한다.

| 연결 | 현행 판정 | 남은 실제 계산 |
|---|---|---|
| 연속 유효 전환의 유한 파수·메트릭·중성미자 | 실행·보존 검증 | 실제 입자종 반응률·물리 종 완성 |
| 유한 방출 시각·기록 열과 국소 열역사 | 실행·검증 | 사건면을 가로지르는 유한 파수 에너지·운동량 전달 |
| 보정된 WRRA 배경의 비선형 렌징 우도 | 조건부 실행 | 자체 초기상태·사건 섭동을 포함한 동일 관측 경로 |
| 64모드 CDM 정지 게이지와 안정적 메트릭 조합 | 부분 접합 실행 | 바리온·전자·질량 중성미자 상태와 후단 운반 |
| 전체 씨앗→방출→열역사→관측량 | 미완료 | 재보정 배경 모드 재적분과 3차원·각도 공분산 완성 |

v0.25-r5의 평균 준비에서 개별 우주로 가는 동역학 문제도 그대로 남는다. 유한 씨앗에 대한 응답을 계산했다는 사실만으로 씨앗 선택·준비·확률의 소유권까지 유도했다고 표시하지 않는다. 유한 분기·보정·각도 완성을 추가할 수 있으나 가정을 명시하고 실제로 실행한 뒤에만 통합 상태를 바꾼다.

결론적으로, 하나의 방법으로 잔여·전환·기록·열역사·중력과 관측을 연결하는 구체적 계산 모듈이 늘어났다. 알려진 값의 재현은 현실 정합성과 설명 성과이며, 독창성은 이 변환과 보존·연결 구조에서 판정한다. 원전 v0.7-dev-r1까지의 범위는 전체 우주론 모형의 완성 선언이 아닌 실행·검증된 부분 연결이다.

### 136.7 공개 원전과 재현 경로

| 원전 | DOI | GitHub의 submission/ 하위 경로 |
|---|---|---|
| 유한 구배 v0.4 | [10.5281/zenodo.23490141](https://zenodo.org/records/23490141) | finite_gradient_matching_v0_4 |
| 유한 방출 v0.5 | [10.5281/zenodo.23491041](https://zenodo.org/records/23491041) | finite_emission_v0_5 |
| 관측·열역사 v0.6 | [10.5281/zenodo.23491673](https://zenodo.org/records/23491673) | observation_thermal_v0_6 |
| 상태 접합 개발 v0.7-dev-r1 | [10.5281/zenodo.23492328](https://zenodo.org/records/23492328) | full_state_junction_v0_7 |

공개 저장소는 [wrra-m-0.1](https://github.com/Wonsik-Choi-janefather/wrra-m-0.1)이다. 각 원전의 실제 입력·출력·검사·정규화·검산 기록을 유지한다. 새 책 v0.26의 편집 감사는 그 원전 검사의 대체물이 아니다. Zenodo에는 국문·영문 완전 PDF를 게시하고 데이터·코드는 GitHub로 제공한다.
'''
chapter_en=r'''## 136. From Residue Seeds to Finite Emission, Thermal History and Observational Calculation

### 136.1 Verified inputs and ownership of versions

This chapter preserves Chapters 1–135 and the artistic opening of v0.25-r5 and adds the residue/CMB studies v0.4, v0.5, v0.6 and v0.7-dev-r1 published on 20 October 2026. Book revision v0.26 and individual calculation versions are different numbering systems. This is an integration of executed source records; editing the book is not counted as a new physical run or empirical confirmation.

Verified inputs are the original quantized 128-cell seed, 64 evolved physical modes, calibrated background and proper-time unit, observed constants and electron/positron EOS, and released SPT–Planck lensing bandpowers, covariance and windows. Ownership of numerical results remains with the source studies and their GitHub paths below. Adopting verified constants and observations, and revising a model accordingly, is legitimate construction and calibration.

| Calculation source | Executed WRRA connection | Source check record | Present scope |
|---|---|---|---|
| v0.4 | Finite-k conversion, metric, momentum, free-streaming neutrinos and conserving same-content matching | 643 | Linear amplitude, 64 modes; not production CAMB full-state injection |
| v0.5 | Finite-packet event timing, record permission, heat cost and local expansion | 444 plus 12 release checks | Independent local FLRW cells; not finite-k event evolution |
| v0.6 | Conditional nonlinear lensing/likelihood for a WRRA background and separate MeV thermal history | 54 plus 8 release checks | Declared calibrated primordial completion and thermal calculation |
| v0.7-dev-r1 | 64-mode frame adapter, event-time tangent, thermal density calibration and stable metric combination | 472 plus 10 release checks | Partial full-state junction development |

These counts are numerical conservation, normalization, convergence and control checks, not independent observations. Reruns do not become new cosmic measurements. Earlier actual-SOURCE CMB branch outputs are retained and are not replaced by the conditional v0.6 branch in this chapter.

### 136.2 WRRA-specific transformation: finite gradients and conserving matching

Version 0.4 carries seed modulation of the conversion rate from an effective relativistic reservoir into a dust-like matter component. It evolves synchronous metric variables, species densities and momenta, and a massless free-streaming neutrino hierarchy together. The 64 physical modes are $k=0.05,0.10,\ldots,3.20\ {\rm Mpc}^{-1}$, with stored moments $F_{\nu0}$ through $F_{\nu12}$. Spatial gradients are retained while perturbation amplitudes remain linear.

The exchange law requires total stress-energy conservation:

$$\nabla_\mu T_A^{\mu\nu}=Q_A^\nu,\qquad \sum_A Q_A^\nu=0.$$

The calculation does not discard metric and momentum in favor of one entropy value. Merging the remaining effective perfect radiation into photon-like perfect radiation transports both its density and momentum and retains the neutrino hierarchy. Continued evolution is explicitly compared in the same-content system. This is a finite-gradient advance beyond a two-moment fluid substitute. It does not automatically generate physical species-production rates, baryon/photon tight coupling or a massive-neutrino phase-space distribution.

### 136.3 Finite emission times and recording cost

Version 0.5 partitions a reference cell's convertible radiation budget into 256 packets. Emission occurs when accumulated transfer credit reaches the packet threshold and record permission is available. Credit is not a second energy reservoir. Gate closure pauses credit production; there is no forced flush at pulse closure. The reference run emits 128 events.

$$\dot r=\Gamma(1+\xi)C,\qquad r=q\ \hbox{and recording permission}\ \Longrightarrow\ \hbox{emission}.$$

$$C^+=C^--q,\qquad M^+=M^-+\frac{(1-\epsilon)q}{a_j},\qquad J^+=J^-+\epsilon q.$$

Here $q$ is a reference-cell comoving radiation-energy debit and $\epsilon=0.01$ is a declared recording heat cost. The packet is not identified with a universal particle rest energy or a new fundamental quantum. The different dilution laws of $C,M,J$ make the factor $a_j$ essential for conservation. In the thermal completion the heat changes the actual electromagnetic temperature through the finite-electron heat capacity, rather than being replaced by a perfect-radiation constant.

The first and last events occur at approximately 0.00268883 s and 0.475779 s. The inherited 0.47712081326446576 s unit is a calibrated early-universe proper-time unit, not the book's microscopic shutter time. At fixed packet number the small-seed response depends on the order of the small-seed and continuum limits. The smooth-source response is therefore not copied into the finite-event model.

### 136.4 Executed likelihood and MeV thermal outputs

The v0.6 observational branch uses the inherited WRRA dark-weight-only background $H_0=67.2568374662005$, $\omega_b=0.022395806792949086$, $\omega_c=0.12037806177378184$. It declares the calibrated standard adiabatic primordial completion $A_s=2.1\times10^{-9}$, $n_s=0.9649$, with inputs $\tau=0.0544$, $N_{\rm eff}=3.044$, $T_{\rm CMB}=2.7255$ K. CAMB 2.0.4 and the adopted HMCode 2020 prescription provide nonlinear lensing. The likelihood uses the released 18-bin SPT–Planck full covariance, windows and TT/PP response corrections.

$$b=(W+R_{PP})D^{\phi\phi}+R_{TT}D^{TT}-f,\qquad
\chi^2=(b-d)^T\Sigma^{-1}(b-d).$$

| Declared comparison | Fixed-model $\chi^2$, 18 bins |
|---|---:|
| Linear lensing | 11.6855836908 |
| Adopted nonlinear lensing | 10.6060135496 |
| Accuracy-refined nonlinear lensing | 10.6032279730 |

The native likelihood agrees with a separate official CosmoMC implementation within $1.60\times10^{-14}$. The covariance distance under refinement is approximately 0.00383078 sigma. These are conditional comparisons of a WRRA background and a declared primordial preparation. They do not inject the complete v0.4 state or v0.5 event perturbations into CAMB. Reproduction and explanation using verified preparation inputs are achievements, while connections not executed are not called integrated. HMCode is an adopted empirical prescription, not a newly derived WRRA nonlinear law. A likelihood tail probability is not the probability that a theory is true.

The separate finite-event thermal history uses finite-mass equilibrium electrons/positrons and a declared instantaneous relativistic-neutrino-decoupling branch. Retaining the inherited clock gives initial photon temperature 1.7584850895 MeV and present-photon-entropy-connected initial scale $a_i=9.55163454815\times10^{-11}$, about 4.48% below the earlier $10^{-10}$. One cannot add this thermal content while keeping the old clock, scale and species content all unchanged.

| Photon temperature | Elapsed time after pulse start |
|---|---:|
| 1 MeV | 0.5045894421 s |
| 0.5 MeV | 2.8257151242 s |
| 0.1 MeV | 118.6213275533 s |

These are not absolute cosmic ages. $N_{\rm eff}$ is an input. Collision integrals, flavor transport, weak freezeout and BBN element yields are not computed. Standard cosmology supplies verification and reinforcement; only connections actually calculated within the resulting WRRA model count as executed integration.

### 136.5 Full-state junction development and numerical correction

Version 0.7-dev-r1 transforms all available scalar variables of the 64 v0.4 modes into the post-exchange CDM-comoving synchronous frame. It does not simply set velocity to zero: densities, metric derivatives and the neutrino monopole/dipole transform together.

$$\alpha=\frac{\theta_m}{k^2},\quad
\theta_i^c=\theta_i-k^2\alpha,\quad
\delta_i^c=\delta_i+3(1+w_i){\cal H}\alpha,\quad
\eta^c=\eta+{\cal H}\alpha.$$

Maximum normalized Hamiltonian and momentum residuals after transformation are $3.29\times10^{-16}$ and $4.31\times10^{-16}$. However, reconstructing a small combination from separately rounded large derivatives produces up to approximately 16.66% relative Bardeen-potential error at low k. Revision r1 retains that combination directly from the inherited scaled shear $g$ and gauge shift:

$$h^{c\prime}+6\eta^{c\prime}=2k^2(g/2+\alpha).$$

With this stable combination, Bardeen-potential gauge invariance agrees within relative $4.35\times10^{-12}$ over all 64 modes. Naive subtraction is retained as a negative control. Separate derivatives are rounded diagnostics; any future actual CAMB transport must also verify stable constraint evaluation.

Separately, the local-cell v0.5/v0.6 model includes the derivative of event time. Its common-time tangent $z=\partial y/\partial\xi$ changes across event reset $R$ according to

$$z^+=DR\,z^-+(DR\,f^--f^+)t_j',\qquad t_j'=-\frac{t_j}{1+\xi}.$$

The finite-event thermal $k=0$ entropy response is 0.194818034056, differing from the smooth-source 0.723567385056. Applying the unchanged seed without amplitude refitting gives entropy RMS $4.80262944810\times10^{-9}$. An independent clock $u=(1+\xi)t$ keeps events fixed and reproduces the response within relative $8.39\times10^{-9}$. This local tangent is not substituted for a finite-k full state.

The old conversion budget gives thermally normalized dark matter $\omega_c=0.103663511129$, approximately 13.885% below the downstream target. Recalibrating this branch's conversion fraction $\beta$ from $7.62452468358\times10^{-7}$ to $8.85389093544\times10^{-7}$ reproduces the inherited target. This is legitimate background calibration. This $\beta$ is an early convertible-radiation fraction, not the book's cosmic composition or identically written symbols in other chapters. The 64 finite-k modes have not been rerun on that calibrated background. Earlier composition, shutter, galaxy and GR/CMB branch values are not retroactively changed.

### 136.6 Falsification conditions and the exact remaining junction

Failure or revision conditions are violated total conservation or Einstein constraints; inconsistent gauge invariants or neutrino normalization; omitted event-time motion, recipient momentum or recording heat; failed EOS, time or hierarchy convergence; incorrect covariance, windows or likelihood normalization; and disagreement with the declared observational comparison. Inputs and preparations remain disclosed, and WRRA and established models receive the same evidentiary standard.

| Connection | Present assessment | Remaining executed calculation |
|---|---|---|
| Smooth effective finite-k conversion, metric and neutrinos | Executed; conserving | Physical species rates and state completion |
| Finite event times, recording heat and local thermal history | Executed; checked | Finite-k energy/momentum transfer across event hypersurfaces |
| Nonlinear lensing likelihood for a calibrated WRRA background | Conditional execution | The same observational path with native full states/event perturbations |
| 64-mode CDM frame and stable metric combination | Partial junction executed | Baryon/electron and massive-neutrino states and downstream transport |
| Entire seed-to-emission-to-thermal-to-observation chain | Incomplete | Recalibrated-background mode rerun and 3D/angular covariance completion |

The v0.25-r5 problem of mean preparation versus one individual universe remains open. Computing response to a supplied finite seed does not derive selection, preparation and probability ownership of that seed. Additional finite branches, calibrations or angular completions may be introduced, with assumptions declared and execution verified before integration status changes.

The result is a larger set of concrete modules linking residue, conversion, recording, thermal history, gravity and observation through one method. Reproducing known values is compatibility and explanatory achievement; originality lies in the transformations and conserving connection structure. The executed scope through source v0.7-dev-r1 remains partial connection, not a declaration of a completed cosmological theory.

### 136.7 Published sources and reproduction paths

| Source | DOI | Path below GitHub submission/ |
|---|---|---|
| Finite gradients v0.4 | [10.5281/zenodo.23490141](https://zenodo.org/records/23490141) | finite_gradient_matching_v0_4 |
| Finite emission v0.5 | [10.5281/zenodo.23491041](https://zenodo.org/records/23491041) | finite_emission_v0_5 |
| Observation/thermal v0.6 | [10.5281/zenodo.23491673](https://zenodo.org/records/23491673) | observation_thermal_v0_6 |
| Junction development v0.7-dev-r1 | [10.5281/zenodo.23492328](https://zenodo.org/records/23492328) | full_state_junction_v0_7 |

The repository is [wrra-m-0.1](https://github.com/Wonsik-Choi-janefather/wrra-m-0.1). Preserve each source's inputs, outputs, checks, normalization and release verification. The book v0.26 editorial audit does not replace those source checks. Zenodo carries the complete Korean/English PDFs; code and data are supplied through GitHub.
'''

fronts={
'KO':'## 개정판 v0.26: 유한 구배·양자 방출·열역사와 관측 접합\n\n최원식 · 최정인 | 2026년 10월 20일\n\n**v0.26 통합 안내.** v0.25-r5의 1–135장과 예술적 서두, 두 해상도·상류 교환·초기 준비·블랙홀 보강을 유지하고 제136장을 추가했다. 유한 구배 v0.4, 유한 방출 v0.5, 조건부 비선형 렌징·MeV 열역사 v0.6, 전체 상태 접합 개발 v0.7-dev-r1의 실제 산출과 한계를 반영한다. 전체 CAMB 초기상태 접합과 평균–개별 우주 준비는 미완료다. 책 DOI: https://doi.org/10.5281/zenodo.23492729. 데이터·코드는 GitHub로 제공한다.\n\n',
'EN':'## Revision v0.26: Finite Gradients, Quantum Emission, Thermal History and Observational Junctions\n\nWonsik Choi · Jeongin Choi | 20 October 2026\n\n**v0.26 integration note.** Preserve Chapters 1–135 and the artistic opening of v0.25-r5, including two-resolution measurement, upstream exchange, initial preparation and black-hole reinforcement. Add Chapter 136 for the executed outputs and scope of finite gradients v0.4, finite emission v0.5, conditional nonlinear lensing/MeV thermal history v0.6 and full-state junction development v0.7-dev-r1. Complete CAMB initial-state injection and mean-to-individual preparation remain incomplete. Book DOI: https://doi.org/10.5281/zenodo.23492729. Code and data are supplied through GitHub.\n\n'}
synthesis={
'KO':r'''**v0.26 현행 보강.** 검증 입력은 원래 128셀 씨앗·64모드 상태·보정된 고유 시간과 배경·전자 EOS·공개 렌징 공분산이다. WRRA 고유 변환은 보존하는 유효 전환, 기록 허가를 가진 패킷 사건, 실제 열용량, 배경–우도 연결 및 전체 스칼라 상태의 좌표 변환이다. 산출값은 제136장의 유한 구배·128사건·조건부 렌징 $\chi^2=10.6060135496$·MeV 경과 연대기·안정적인 메트릭 조합과 배경 재보정이다. 반증조건은 보존·게이지·단위·시간/계층 수렴·관측 공분산과 같은 상태의 후단 접합 실패다. 이 연결은 설명·재현 성과이며, v0.7-dev-r1까지 전체 초기상태를 넣은 새 CMB 결과는 계산하지 않았다.

제136장의 배경 보정은 초기 전환량의 별도 분기다. 기존 구성비·셔터·은하·GR/CMB 수치를 소급하여 변경하지 않는다. 이전 결론의 현재·PASS는 해당 조건의 실행 범위를 유지하며, 전체 접합의 현행 상태는 제136.6절을 따른다. 아래 v0.25-r5까지의 종합은 누적 성과와 계보로 보존한다.

'''.replace('\n+','\n'),
'EN':r'''**Current v0.26 reinforcement.** Verified inputs are the original 128-cell seed, 64-mode states, calibrated clock/background, electron EOS and released lensing covariance. WRRA-specific transformations are conserving effective conversion, record-permitted packet events, actual heat capacity, background-to-likelihood connection and a full available scalar frame transform. Outputs are Chapter 136's finite-gradient evolution, 128 events, conditional lensing $\chi^2=10.6060135496$, MeV elapsed chronology, stable metric combination and background recalibration. Failure conditions are conservation, gauge, unit, time/hierarchy-convergence, observational covariance and same-state downstream-junction failures. These are explanatory and reproduction achievements; no new CMB result with complete initial-state injection is computed through v0.7-dev-r1.

The Chapter 136 calibration is a separate early-conversion branch. Earlier composition, shutter, galaxy and GR/CMB values are not retroactively changed. Earlier current/PASS statements retain their declared execution domains; Section 136.6 governs the present full-junction status. The synthesis through v0.25-r5 below is preserved as cumulative achievement and genealogy.

'''.replace('\n+','\n')}
records={}
for lang,chapter in [('KO',chapter_ko),('EN',chapter_en)]:
 old=(S/f'MCC_3_0_Full_Book_{lang}_v0.25.md').read_text()
 marker='## 연구 목적과 설계 원칙' if lang=='KO' else '## Research Purpose and Design Principle'
 start=old.index(marker)
 new=old.splitlines()[0]+'\n\n'+fronts[lang]+old[start:]
 synmark='## 현행 종합 결론 — v0.25-r5' if lang=='KO' else '## Current synthesis — v0.25-r5'
 assert new.count(synmark)==1
 new=new.replace(synmark,chapter+'\n\n'+synmark.replace('v0.25-r5','v0.26')+'\n\n'+synthesis[lang],1)
 if lang=='KO':
  new=new.replace('전권 1–135장.','전권 1–136장.',1)
  toc='- 135. 양방향 표현형 출력기·단일 짝수 전환과 셔터 위상'
  new=new.replace(toc,toc+'\n- 136. 잔여 씨앗에서 유한 방출·열역사·관측 계산까지',1)
 else:
  new=new.replace('Chapters 1–135','Chapters 1–136',1) if False else new
  # The preserved-135 statement in the new integration note stays 1–135.
  new=new.replace('Current Chapters 1–135','Current Chapters 1–136',1)
  new=new.replace('Complete Chapters 1–135','Complete Chapters 1–136',1)
  new=new.replace('Full Chapters 1–135','Full Chapters 1–136',1)
  toc='- 135. Bidirectional phenotype rendering, singly even transitions and shutter phase'
  new=new.replace(toc,toc+'\n- 136. From residue seeds to finite emission, thermal history and observational calculation',1)
  new=new.replace('No new DOI is assigned to this book revision.','The current book DOI and subsequent publication state are recorded in PUBLICATION_STATUS.json.',1)
 name=f'MCC_3_0_Full_Book_{lang}_v0.26.md';(P/name).write_text(new)
 (R/f'Chapter136_{lang}.md').write_text(chapter)
 (R/f'Current_Synthesis_Addition_{lang}.md').write_text(synthesis[lang])
 (R/f'Front_{lang}.md').write_text(fronts[lang])
 patch=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=f'v0.25-r5/{lang}',tofile=f'v0.26/{lang}'))
 (R/f'changes_{lang}.patch').write_text(patch)
 records[lang]=dict(source_library_file='libfile_c87d6e336cb88191aff11b4e987a21c3' if lang=='KO' else 'libfile_4ea8a327688c8191a6c9e7941687d3bc',
  source_sha256=hashlib.sha256(old.encode()).hexdigest(),new_sha256=hashlib.sha256(new.encode()).hexdigest(),source_bytes=len(old.encode()),new_bytes=len(new.encode()),chapter_added=136)
 # Require the whole pre-synthesis body to survive, except the explicit TOC edit.
 body=old[start:old.index(synmark)]
 body=body.replace('전권 1–135장.','전권 1–136장.',1) if lang=='KO' else body
 body=body.replace('Current Chapters 1–135','Current Chapters 1–136',1)
 body=body.replace('Complete Chapters 1–135','Complete Chapters 1–136',1).replace('Full Chapters 1–135','Full Chapters 1–136',1)
 body=body.replace(toc,toc+'\n'+('- 136. 잔여 씨앗에서 유한 방출·열역사·관측 계산까지' if lang=='KO' else '- 136. From residue seeds to finite emission, thermal history and observational calculation'),1)
 assert body in new,lang+' original chapters lost'
 records[lang]['prior_chapters_preserved']=True
 # Artistic opening is protected byte for byte.
 op='## 서두 —' if lang=='KO' else '## Opening —'
 aa=old.index(op);bb=old.find('\n---',aa)
 if bb==-1:bb=old.find('\n# ',aa)
 assert old[aa:bb] in new
 records[lang]['artistic_opening_preserved']=True
 # Frozen Appendix G is also preserved unchanged.
 app='# 공통 보존 부록 G' if lang=='KO' else '# Shared Historical Appendix G'
 xx=old.index(app);end='# 원본 자료와 재현 경로' if lang=='KO' else '# Source archives and reproduction paths'
 yy=old.index(end,xx);assert old[xx:yy] in new
 records[lang]['historical_appendix_preserved']=True
(R/'EDITORIAL_PROVENANCE.json').write_text(json.dumps(dict(book_version='0.26',previous='0.25-r5',sources=records,
 new_scientific_run_claimed=False,new_CMB_full_state_injected=False,chapter_source_versions=['0.4','0.5','0.6','0.7-dev-r1'],
 evaluation_order=['verified inputs','WRRA transformation','outputs','falsification conditions']),indent=2)+'\n')
print(json.dumps(records,indent=2))
