최소계산우주론: 주소 생성 암흑 가중치 후보와 CMB 연결 v0.1
2026-10-14

검증 입력
N_U=1,015,000의 실제 주소 배열, 동결된 주소 가중치 w_n와 부문 효과 e_P/e_D/e_R, eta, 기존 잔여 커널(소수 2·3·5), 128개 슬롯 할당, 공급/소스 8→72 전환, epsilon=1e-8, CMB 완성 모듈 및 공개 Plik-lite TTTEEE 자료를 사용했다. 주소 1은 기존 규칙대로 별도 취급하여 이번 활성 합산에서 제외했다.
초기 우주 준비는 앞서 명시한 regular CDM isocurvature + constant vacuum contrast 확장을 유지했다. macro k_1=.05 Mpc^-1, As/ns/tau/mnu/nnu 등의 기존 입력도 유지했다. 추가 최적화는 수행하지 않았다.

WRRA 고유 변환
주소 가중치 → 부문별 로그 가중치 → 잔여/슬롯 재할당 → 유한 소스·공급 장부 → 평균 에너지 및 Fourier 스트레스 → 수정 CAMB의 실행 → TT·TE·EE → 공분산 평가.
CAMB는 채택한 외부 물리 모듈이며 이번 연결 내부에서 실제 실행됐다. 상류 Fourier 벡터 또는 배경 밀도를 사후 교환하는 입력 대신, 각 후보의 실제 주소 기여에서 슬롯과 공급 장부를 새로 생성했다.

산출값

주소 부문 가중치:
  c_s(n) = e_s(n) w_n [1 + lambda_s ln(n)/ln(N_U)]

이번에 실행한 세 후보:
  비가중치:       lambda=(0,0,0)
  기존 가중치:    lambda=(0,.25,.1)
  암흑 가중치만:  lambda=(0,.25,0)

세 번째 후보는 앞선 장부 교환 진단을 반영하여, 기존 부문별 가중치 함수 안에서 선택한 새 보정 분기다. 관측 자료를 이용한 선택임을 명시한다. 숫자의 독립적 예측이나 유일하게 강제되는 lambda 값이라고 주장하지 않는다. 알려진 검증값을 반영한 후보 구성과 실제 재현을 이번 성과로 판정한다.

1. 암흑 장부 차이의 상류 기원
  mu_D(0) = sum e_D(n)w_n = .2680000000000001
  L_D = sum e_D(n)w_n ln(n)/ln(N_U) = .04370244390697558
  mu_D(.25) = mu_D(0)+.25*L_D = .27892561097674395
  Delta mu_D = .010925610976743895
  Delta u_D = eta_D*Delta mu_D = 7.960139394787346e-12 J/m^3
  상대 증가분 = 4.0767205137%

mu_D는 무차원 평균 부하이며, 그 숫자를 우주의 에너지 밀도 비율로 곧바로 읽지 않는다. 물리적 에너지는 eta를 적용한 후 전체 배경 장부에서 정규화한다.

증가분의 주소 분해:
  주소 2–9:        43.9295711%
  주소 10–99:      44.8746341%
  주소 100–999:     9.2359442%
  주소 1000 이상:   약 1.96%
주소 100 미만이 약 88.8042052%를 차지한다.
가장 큰 개별 기여는 주소 4(21.9617%), 6(13.1393%), 8(8.8286%)다. 주소 번호를 특정 입자나 물체로 새로 동일시한 것은 아니다.
공급 제어 대상 n mod 3 !=0은 증가분의 68.4135%, 나머지 주소는 31.5865%를 만든다. 따라서 공간 공급 응답만 바꾸고 나머지 주소 부하를 누락하면 같은 배경 장부를 재현하지 못한다.

2. 잔여 및 공급 장부
전체 슬롯 용량은 전체 입력 부하로 결정되므로, vacuum 가중치를 바꾸면 dark 슬롯의 배치도 바뀐다. 이번에는 기존 dark 슬롯 배열을 그대로 가져오지 않고 실제 주소를 다시 할당했다. 기존 가중치 배열과 후보의 dark 슬롯 payload는 최대 .0003950121만큼 다르다. 그러나 해당 부문의 잔여 marginal과 mean load는 동일하며, 부문 소유 커널로 합산한 Fourier stress도 정확히 연결된다.

기존 규칙의 uniform supplier probability .5에 대해:
  A8 = 1-cos(pi/8), gap = 2 cos(pi/8)
  A8 + .5*gap = 1
  source_before_s = eta_s [U_s + A8 M_s]
  supplier_before_s = eta_s gap M_s/2
  total_mean_s = eta_s [U_s+M_s] = eta_s mu_s
P 부문은 공급 제어를 적용하지 않는다.
공간적으로는 p_r=.5+epsilon(K_r-1)을 사용하고, source + supplier를 함께 세어 delta_u를 계산했다. 최종 후보의 전체 에너지·압력 장부 오차는 2.07e-25 J/m^3 이하였다. 유한 permutation의 unitary 성질과 source/supplier Hamiltonian의 보존도 확인했다.

3. 주소 생성 후보의 물리적 배경
  u_P = 3.78079124955e-11 J/m^3
  u_D = 2.0321854300662739e-10 J/m^3
  u_R = 5.214642122421598e-10 J/m^3
  omega_b h^2 = .022395806792949086
  omega_c h^2 = .12037806177378184
  H0 = 67.2568374662005 km/s/Mpc
H0는 이 에너지 총량과 고정 thermal budget에서 계산했다. 별도의 최적화 변수가 아니다.

4. 실제 CMB 실행
Plik-lite high-l, 613개 TT·TE·EE 구간, 전체 공분산과 bin 가중치, A_planck=1:
  비가중치 주소 → 기준선:       chi2=1217.7512246828783
  기존 가중치 주소 → 기준선:   chi2=591.5703352409629
  암흑 가중치만 주소 → 기준선: chi2=585.913918450675
  마지막 후보 + 실제 SOURCE:  chi2=585.9139188511556

주소에서 생성한 마지막 기준선과 앞선 장부 교환 진단의 차이는 chi2 기준 3.47e-9다. 따라서 앞선 진단값을 실제 상류 생성 규칙의 실행 결과로 재현했다.
이 평가는 native Gaussian Plik-lite 식을 사용한 조건부 high-l 평가다. 공식 clik executable, low-l 및 lensing likelihood는 사용하지 않았다. SOURCE angular power는 선형·unlensed이며, 표준 lensed 기준선에 더하는 기존 1차 진단 조건을 유지한다.

SOURCE TT 최대는 1.53409e-5 microK^2, 실제 SOURCE의 score 변화는 약 4.00e-7에 불과하다. 좋은 CMB 재현의 주요 변화는 mean background이며, 작은 SOURCE 성분의 관측적 검출로 읽으면 안 된다.

반증조건 및 검사
주소 직접 합과 슬롯/잔여 합이 다르거나, 공급 에너지·압력 보존이 깨지거나, 기존 Fourier 벡터 및 CMB 기준선 재현에 실패하거나, SOURCE=0 복원 또는 정밀도 변경에 수렴하지 않거나, 실제 성분이 선언한 선형 구간을 벗어나면 구성 또는 연결을 수정한다. 합의한 완성된 관측 비교에서도 불일치가 유지되면 해당 후보를 수정한다.

실행된 41개 구성·수치 검사 모두 통과:
- 직접 주소 및 슬롯 재할당 합산.
- 기존 두 분기의 mean energy와 Fourier stress 재현.
- 새 후보 source/supplier 에너지 및 압력 보존.
- SI 배경 밀도 환산.
- SOURCE=0 최대 상대 TT/EE 복원 오차 1.74e-10 이하.
- 정밀도 1.5→2.5의 SOURCE TT/TE/EE 최대 크기 기준 차이 0.076% 이하.
- 독립 momentum integrating-factor 검사 오차 2.59e-8 이하.
- 모든 14개 실수 성분 상태 유한성; 총합 delta_D triangle bound .007698 이하.
- 기존 및 장부 교환 CMB 결과 재현.
검사 통과 개수를 우주론 전체의 증명으로 해석하지 않는다.

결론
관측 진단을 반영한 lambda=(0,.25,0) 후보는 실제 주소 단계에서 생성되며, 동일한 잔여·공급·에너지 장부를 거쳐 CMB 점수 585.91을 재현한다. 이번 범위의 상류–하류 연결과 알려진 CMB 관측에 대한 조건부 정합성이 확인됐다.
가중치 보정의 물리적 의미와 적용 범위, 초기 우주 준비의 상류 도출, SOURCE 자체의 렌즈 효과 및 전체 Planck likelihood는 후속 과제다. 초기 우주 확장 조건 자체는 이미 적용한 상태다.

재현
requirements.txt 설치 후 python reproduce.py. 실제 주소 입력과 실행한 Linux x86_64 수정 CAMB binary가 포함된다. 다른 플랫폼은 gfortran/make 환경에서 python build.py로 동일 patch를 빌드한다. SHA256SUMS.txt 및 provenance.json에 입력과 실행기 해시를 남긴다.
주요 파일: address_results.json, bridge_results.json, sector_residue_trace.csv, source_supply_mean_ledger.csv, generated_SOURCE_harmonics.csv, 후보 TT/TE/EE 및 그래프. 상류 주소 생성기 이전의 전체 단계는 이번에 재구성하지 않았으며, 동결된 주소 가중치와 부문 효과를 입력으로 사용했다.

출처
CAMB 2.0.4와 포함된 라이선스.
https://camb.readthedocs.io/en/stable/results.html
Planck 2018 V: doi:10.1051/0004-6361/201936386.
native Plik-lite 데이터: CobayaSampler/planck_native_data v1.
native likelihood conventions: Cobaya PlanckPlikLite, E. Calabrese/A. Lewis.
상류 원본 맥락: doi:10.5281/zenodo.23329214. 이번 새 후보가 그 DOI에 등록되었다는 뜻은 아니다.
