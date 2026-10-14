CMB 후속 점검: SI 단위·7개 모드·비가중치 배경 불일치 진단
2026-10-14 / 최소계산우주론 연구의 조건부 계산

검증 입력
동결된 SOURCE/supply Fourier 벡터, 두 분기의 물리적 에너지 장부, 앞선 수정 CAMB 2.0.4 결과, Plik-lite TT·TE·EE 공분산 및 bin 가중치. k=.05*n Mpc^-1, n=1…7, epsilon=1e-8, A_planck=1, 정밀도 2.5를 유지했다.

WRRA 고유 변환
잔여별 공급 응답에서 얻은 delta_u_D와 delta_u_R를 각 배경 에너지 밀도로 나누어 무차원 초기 성분을 구성한다. 공간 진공 성분의 힘과 암흑 운동량을 같은 장부로 진화시킨 후 TT·TE·EE로 전달한다. 이번 점검은 이 연결의 단위, 실제 solver의 선형 전달, 조화 성분별 진화를 확인한다. 추가로 암흑/진공 장부를 교환하여 관측 불일치의 원인을 분리했다.

산출값
1. 단위 계수
u는 J/m^3, k는 Mpc^-1, CAMB conformal time은 Mpc다. 에너지 밀도의 a^4 배경 출력 환산은 8*pi*G*a^4*u*Mpc^2/c^4이고, metric stress는 a^2 가중치를 사용한다. delta_u/u에는 추가 c 또는 G 인자를 넣지 않는다. 배경 밀도, vacuum stress, dark momentum, force ratio의 직접 SI 환산 오차는 모든 분기에서 5.56e-16 이하였다. 점검한 계수에서는 스케일 누락을 발견하지 않았다. 모든 가능한 물리적 연결을 증명했다는 뜻은 아니다.

2. 실제 solver의 진폭 검사
vacuum basis 초기 진폭을 1에서 .01 및 2로 바꾸어 다시 계산하고 나눈 결과가 일치했다. .01 검사에서 T의 상대 차이는 1.12e-7, E는 7.87e-4였다. 실제 D/R 혼합 벡터를 직접 진화시킨 결과와 두 basis의 합성 결과도 T 1.08e-8, E 4.22e-8 이내로 일치했다. 이는 새 신호가 단순한 기준선 차감의 반올림 찌꺼기라는 해석을 지지하지 않는다.

3. 7개 모드의 개별 진화
두 분기 × 7개 모드 × cosine/sine, 총 28개 실수 성분에 대한 밀도·속도·운동량 잔차를 분리했다. 각 basis는 6000개 시간 표본으로 추적했고, 성분별 CSV에는 100개 대표 시각을 담았다. 상태 궤적은 유한하게 유지됐다.
성장률 f_D=delta_D'/(H*delta_D)는 밀도 영점 근처에서 정의되지 않을 수 있다. 이 구간을 OPEN으로 기록했다. 성장률의 분모가 0이 되는 현상을 상태 폭주라고 해석하지 않았다. 무차원 임계값은 max|delta_D|의 1e-6 또는 1e-30이다.
이는 선언한 geodesic synchronous gauge에서의 진화·보존 검사다. 별도의 Newtonian gauge 실행기와 맞춘 완전한 gauge-equivalence 검사를 수행한 것은 아니다.

4. 비가중치 불일치 원인
새 최적화 없이 기존 두 장부의 암흑/진공 성분을 교환했다. H0는 독립 조정하지 않고 합계 에너지와 고정 thermal 성분에서 다시 계산했다. 표준 adiabatic 기준선만으로 원인을 진단했다. 실제 SOURCE 기여가 너무 작아 앞선 high-l Q에 미치는 영향이 수백만분의 몇 이하였기 때문이다.

배경 구성                            high-l Q
비가중치 원본                        1217.75122
암흑 장부만 가중치 값으로 교환          585.91392
진공 장부만 가중치 값으로 교환         1121.90312
가중치 원본                           591.57034

암흑 밀도 omega_c*h^2: .1156628122 → .1203780618.
암흑 장부만 교환한 경우 H0=67.2568375 km/s/Mpc.
진공 장부만 교환한 경우 H0=67.0994706 km/s/Mpc.

현재 구성에서는 암흑 성분의 배경 장부 차이가 비가중치 분기의 불일치에 더 큰 영향을 준다. 단위 계수를 임의로 곱하거나 SOURCE 진폭을 키우기보다, 암흑 성분의 주소 가중치·공급 응답·평균 에너지 연결을 먼저 점검할 근거를 얻었다.
교환 배경은 원인 진단용 조건부 구성이다. 전체 주소 규칙에서 독립적으로 생성한 새 WRRA 분기로 확정하지 않았다. Q=585.91이라는 더 작은 값만으로 그 혼합 배경을 새 이론으로 채택하지 않는다.

공분산을 유지한 TT→TE→EE 순서의 conditional whitening 분해:
가중치 원본: TT 210.739, TE|TT 180.896, EE|TT,TE 199.935.
비가중치 원본: TT 575.722, TE|TT 404.653, EE|TT,TE 237.376.
이 값들은 합이 전체 Q가 되며, 순서에 의존한다. 독립적인 TT/TE/EE marginal likelihood 점수처럼 읽으면 안 된다.

반증조건
직접 SI 환산과 실제 내부 계수가 일치하지 않거나, 초기 진폭을 변경한 solver 결과가 선형 합성에 수렴하지 않거나, 성분별 상태가 선형 문턱을 벗어나거나, 필요한 힘이 포함된 상태에서 운동량 보존이 실패하거나, 장부 교환 진단이 더 높은 정밀도에서 재현되지 않으면 연결 및 원인 판단을 수정한다.

결론과 진행 상태 정정
초기 우주 확장 조건은 앞선 CMB 계산에 이미 반영됐다. 미완료인 것은 그 초기 준비의 상류 도출과 SOURCE 자체의 lensing 완성이다. 이번에는 초기 우주 확장을 새로 도입한 것이 아니다.
가중치 분기의 알려진 CMB 관측 재현은 조건부 현실 정합성의 성과다. 이 작은 SOURCE 성분의 관측 검출이나 전체 우주론의 증명으로 확대하지 않는다. 새로운 스케일 최적화나 임의 증폭은 수행하지 않았다.

재현
requirements.txt 설치 후 python reproduce.py. 원래 실행 binary와 필요한 앞선 결과를 runtime 및 prior/results에 포함했다. 다른 플랫폼에서는 gfortran/make 환경에서 python build.py로 동일 patch를 빌드할 수 있다. 결과는 results/followup_results.json, *_seven_mode_evolution.csv, mixed-background npz에 있다.

자료 출처
CAMB 2.0.4 문서: https://camb.readthedocs.io/en/stable/results.html
https://camb.readthedocs.io/en/stable/transfer_variables.html
공개 Planck native Plik-lite 자료와 식: CobayaSampler/planck_native_data v1 및 Cobaya PlanckPlikLite (Calabrese/Lewis).
앞선 계산: MCC_SOURCE_CMB_Verification_v0_1_2026-10-14.zip.
