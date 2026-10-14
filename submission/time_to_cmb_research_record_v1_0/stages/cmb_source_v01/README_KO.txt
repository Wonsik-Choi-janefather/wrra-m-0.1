최소계산우주론 — SOURCE 모드 CMB 조건부 검증 v0.1
2026-10-14 / 연구 맥락: 최원식·최정인

결과

기존 SOURCE/공급 장부에서 계산해 둔 실제 7개 공간 조화 모드를 광자·중성미자·재결합을 포함하는 CAMB 2.0.4의 선형 섭동 계산에 연결했다. 기존 표준 스펙트럼을 다시 그린 것에 그치지 않고, 공간적으로 변하는 진공 성분과 그에 따라 움직이는 암흑 성분의 실행 방정식을 추가하여 새 TT·TE·EE 기여를 계산했다.

최종 정밀도 AccuracyBoost=2.5, ell=2…2508. 관측에 맞추기 위한 새 최적화는 수행하지 않았다.

                    가중치 분기       비가중치 분기
Plik-lite high-l Q   591.5703358        1217.7512273
자료 구간 수          613                613
SOURCE TT 최대       1.53935e-5          1.46949e-5 microK^2
공개 구간 잔차 RMS     1.08137             2.01223 sigma

Q는 공개 Plik-lite TT·TE·EE 자료의 전체 공분산과 실제 bin 가중치를 이용한 고정 보정 Gaussian quadratic form이다. A_planck=1, TT 215개, TE 199개, EE 199개. 공식 clik 실행 프로그램을 사용한 값은 아니며, low-l 및 lensing likelihood를 포함하지 않는다. 공개 구간 잔차 RMS는 별도의 간이 진단이다. 두 통계량을 동일한 것으로 해석하면 안 된다.

이 조건에서 가중치 분기는 관측 정합성이 좋은 구성 후보를 제공한다. 비가중치 분기는 훨씬 큰 관측 불일치를 보여 수정할 지점이 뚜렷하다. 초기 입력 중 일부가 이미 알려진 우주론 수치에 교정되었다는 사실은 숨기지 않는다. 따라서 이를 독립적인 맹검 예측 성공이라고 주장하지 않는다. 알려진 관측값의 재현과 구조적 정합성은 이번 검증의 유효한 산출물이다.

새 SOURCE를 넣었을 때 Q의 변화는 가중치에서 +5.53e-7, 비가중치에서 +2.65e-6에 불과하다. 기준선의 정밀도 1.5→2.5 변화만으로 Q가 각각 약 0.145, 0.247 변한다. 따라서 SOURCE 추가에 따른 작은 Q 차이에 통계적 개선·악화의 의미를 부여하지 않는다. 현재 진폭으로 CMB가 SOURCE의 존재를 분리해서 확인했다고 할 수 없다.

검증 입력 → 고유 변환 → 산출값 → 반증조건

입력: v0.2의 주소·잔여 분해를 거친 공급 확률 p_r=.5+epsilon(K_r-1), epsilon=1e-8, 8→72 공급/소스 에너지 전환, 고정 eta와 두 배경 장부. CMB 단계는 확정된 Fourier 벡터를 입력받으며, 주소 배열의 합산을 이 패키지에서 다시 수행하지 않는다. 그 상류 계산의 결과와 해시는 inputs/upstream_SOURCE_results.json 및 source_frozen_inputs.json에 남겼다.

변환: 잔여 커널 → 공급 확률 → delta_u_D, delta_u_R → 보존된 암흑/진공 스트레스 → 수정 CAMB의 광자·중성미자 실행 → 정확한 7개 k에서의 전달함수 → 공간 위상·방향 앙상블의 TT·TE·EE.

산출: 기준선·새 모드·합성 스펙트럼, D/R 위상 공분산을 유지한 조화 성분별 기여, 실제 장부·운동량 진화, CMB 물리적 시간의 기존 셔터 단위 표현, 두 종류의 관측 비교. results/results.json에 전체 수치가 있다.

반증: 고정된 변환에서 보존식 위반, 선형 구간 이탈, SOURCE=0 복원 실패, 수치 또는 초기 시각 변경에 대한 비수렴, 합의된 관측 조건에서의 불일치, 요구되는 초기 준비·공분산·렌즈 연결을 모델 내부에서 구성하지 못하는 경우.

추가로 명시한 구성 조건

1. 기존 SOURCE 스트레스 검사는 a=.02…1의 후기 구간이었다. 이번 CMB 계산은 새 조건부 초기 우주 확장이다. delta_u_D0/u_D0를 정규 CDM isocurvature entropy 초기 진폭으로 읽는다. 이는 이전 a=.02 초기 데이터를 역적분해 그대로 재현한 것과는 다르다. 이 초기 준비 자체의 상류 구성을 확인해야 한다.
2. delta_R=delta_u_R/u_R0는 시간에 대해 일정하다. 진공의 압력 섭동은 delta_p_R=-delta_u_R이다. 진공에는 임의의 속도를 주지 않는다.
3. k_n=.05*n Mpc^-1, n=1…7. 기존 .05 Mpc^-1 거시 교정 기준을 유지했다. 주소 수가 이 거시 길이를 독립적으로 유도했다고 주장하지 않는다.
4. 공통 공간 위상과 방향을 각각 균일하게 평균하는 앙상블을 택했다. 각 조화 모드에서 D/R의 cosine/sine 벡터를 함께 전달해 교차항을 유지했다. 기존 표준 adiabatic 모드와 SOURCE는 독립이라고 정했다.
5. SOURCE 각 스펙트럼은 선형·unlensed이다. 이를 표준 lensed 기준선에 더한 값은 명시한 1차 관측 진단이다. SOURCE 자체가 만드는 렌즈 퍼텐셜과 완전한 비선형 렌즈 합성은 이번에 닫히지 않았다.
6. 배경은 기존 FRW/CAMB 완성을 채택했다. SI 초 또는 광속을 SOURCE 주소만으로 새로 유도했다는 뜻이 아니다.

실행 방정식

geodesic synchronous gauge, conformal time tau, v_D는 geodesic 기준 관찰자에 대한 암흑 성분 속도다.

  delta_R' = 0
  delta_D' = -k(z + v_D)
  v_D' = -H_conformal v_D - k*(rho_R/rho_D)*delta_R
  delta_rho_total = rho_D*delta_D + rho_R*delta_R
  delta_p_total = -rho_R*delta_R
  q_total = rho_D*v_D

이 조합은 암흑+진공 계의 에너지 및 운동량 보존식을 만족한다. CAMB의 기존 CDM-comoving 속도 0 가정을 SOURCE 분기에서 그대로 유지하지 않고, 위 v_D를 별도로 진화시켜 metric momentum과 CDM continuity에 함께 반영했다. SOURCE 실행에서는 후기 radiation truncation을 껐고, ISW를 포함한 후기 소스를 계산하도록 했다. 7개 실제 k만 직접 계산해 보간된 연속 primordial spectrum으로 바꾸지 않았다.

각 실수 성분의 전달 결과를 T,E라고 하면, 위상 평균이 주는 계수 1/2 때문에:
  C_l^TT = 2*pi*sum(T_cos^2 + T_sin^2)
  C_l^TE = 2*pi*sum(T_cos*E_cos + T_sin*E_sin)
  C_l^EE = 2*pi*sum(E_cos^2 + E_sin^2)
T/E에는 해당 D/R 초기 벡터의 실제 진폭이 이미 반영된다. E 전달함수에는 sqrt((l-1)l(l+1)(l+2))를 적용했다.

검사

- 동일 lmax=2500 조건에서 원래 스펙트럼 재현: 최대 상대 TT/EE 오차 2.14e-11, 1.68e-10.
- SOURCE=0 복원: 최대 상대 TT/EE 오차 1.25e-10, 9.08e-11 이하.
- SOURCE 정밀도 1.5→2.5 수렴: TT/EE/TE 각 채널의 최대 크기로 정규화한 최대 차이, 두 분기 모두 0.11% 이하. 영점 부근의 상대 오차를 전체 정확도로 쓰지 않았다.
- 초기 시각을 10배 앞당긴 vacuum basis: T/E 차이 0.0047% 이하.
- 독립 적분 검사: (a*v_D)'=-k*(rho_R0/rho_D0)*a^4*delta_R. 진화 결과와 시간 적분의 차이 2.70e-8 이하.
- 필요한 vacuum force를 생략한 대조: 위 운동량 적분 잔차 1.0, 실패.
- 모든 실제 조화 성분을 합친 암흑 밀도 섭동의 triangle bound: 0.00771/0.00817. 선언한 |delta|<.1 선형 문턱 이내.
- TT/EE 비음수, TE 공분산 한계, 일정한 vacuum contrast도 확인했다.

이 검사들은 구현·보존·수치 검사를 뜻한다. 관측 결과와 별개이며, '18개 검사를 통과했으니 우주론 전체가 증명되었다'는 뜻이 아니다.

시간 표현

기존 dt=1.481301966415863e-21 s를 유지했다. 가중치 분기의 last-scattering epoch는 z*=1089.9071, 물리적 나이 약 371,438년, 약 7.91310e33 셔터 단위다. 오늘의 나이는 약 13.7781 Gyr다. 이 물리적 시간은 채택한 배경 방정식의 산출값을 셔터 단위로 표현한 것이다. 미시 주소 실행에서 동일한 거시 배경 시간을 유도하는 작업의 완료 선언이 아니다.

실행

Python 환경에 requirements.txt를 설치하고 실행:
  python reproduce.py

runtime/camb는 이번에 실제 사용한 수정 CAMB와 Linux x86_64 공유 라이브러리를 포함한다. 실행기가 runtime을 먼저 읽는다. 다른 플랫폼에서는 gfortran, make, setuptools가 있는 환경에서 python build.py로 원본 archive에 같은 patch를 적용해 새로 빌드한다. 성공 여부를 build/build.log와 binary 존재로 검사한다. 이미 패치된 build 폴더를 다시 패치하지 않도록 막았다.

자료·방법 출처

CAMB 2.0.4 원본과 라이선스: inputs/camb-2.0.4.tar.gz, runtime/camb 및 inputs/CAMB_LICENSE.txt.
CAMB 전달함수 문서: https://camb.readthedocs.io/en/stable/results.html
Planck 2018 V, CMB power spectra and likelihoods: https://doi.org/10.1051/0004-6361/201936386
Planck PR3 자료: https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/
공개 native Plik-lite 데이터: https://github.com/CobayaSampler/planck_native_data/releases/download/v1/plik_lite_2018_AL.zip
native 식과 자료 형식: Cobaya PlanckPlikLite, E. Calabrese / A. Lewis, https://github.com/CobayaSampler/cobaya/blob/master/cobaya/likelihoods/base_classes/planck_pliklite.py
상류 SOURCE/supply 및 Afshordi 회신 자료의 원본 맥락: DOI 10.5281/zenodo.23329214. 이번 추가 CMB 계산이 이미 그 DOI에 등록되었다는 뜻은 아니다.

다음 수정 포인트

비가중치 배경의 불일치를 낳는 물리적 장부·배경 성분을 점검하고, 가중치 초기 준비의 상류 구성을 닫는 것이 우선이다. 두 분기의 낮은 SOURCE 진폭을 임의로 키워 관측 확인인 것처럼 만들지 않는다. 이어 SOURCE lensing, low-l likelihood, 초기 준비와 표준 adiabatic 공분산의 실제 모델 연결을 완성하면 전체 likelihood 검증을 확대할 수 있다.
