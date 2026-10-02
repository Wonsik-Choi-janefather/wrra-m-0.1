"""Version 0.6 Korean manuscript, with numbers from the executed ledger."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
R=json.loads((ROOT/'code/results.json').read_text())
V=json.loads((ROOT/'verification.json').read_text())
P=R['new_charge_calibration'];S=R['slopes_and_radii'];D=R['beta']
TITLE='핵자 전하 반지름과 유한 운동량 전류'
SUBTITLE='WRRA M 상류 0.6-r1 · 공동 전류 보강과 β 붕괴의 반동·복사 보정'
B=[]
def p(t):B.append({'kind':'p','text':t})
def h(t):B.append({'kind':'h','text':t})
def eq(n,t):B.append({'kind':'eq','label':str(n),'tex':t})
def table(cap,headers,rows,widths):B.append({'kind':'table','caption':cap,'headers':headers,'rows':rows,'widths':widths})
def page():B.append({'kind':'break'})
def fig(name,cap):B.append({'kind':'fig','name':name,'caption':cap,'width':6.7})

h('초록')
p('상류 0.6은 0.5에서 남긴 중성자 전하 반지름의 불일치를 출발점으로 삼아, 같은 내부 상태의 유한 운동량 전자기·약한 전류를 구성한다. 기존 점전하 판독은 Sachs 전하 정의로 유지하고, 영전하 아이소벡터 보정항 하나와 공통 공간 폭을 양성자·중성자 전하 반지름에 공동 보정한다. 이 절차는 알려진 반지름을 반환하는 구성 보강이며, 중성자 반지름의 독립 예측이나 미시 교환 전하의 도출이 아니다.')
p(f'공동 보정은 ℓ={P["ell_fm"]:.9f} fm, cE={P["isovector_counterterm_radius_fm2"]:.9f} fm²를 정한다. 0.5의 제한 결합, 무차원 바닥상태, 에너지 척도와 영운동량 축벡터·자기모멘트는 유지한다. Sachs–Dirac–Pauli 변환, 아이소스핀 한계의 CVC 및 투영 공간의 종방향 연속 방정식을 실제 연산자로 확인한다. 유한 운동량 곡률은 선택한 보정항 길이에 의존한다.')
p(f'같은 전류의 기울기를 β 붕괴에 전달하고 정확한 세 입자 tree 반동, 약한 자기항, 선도 전자 포괄 외부 복사 보정과 고정된 2018년 내부 복사 기준을 적용한다. 부모 허용 근사에 대한 붕괴율 배율은 {D["full_rate_ratio_relative_parent"]:.9f}이다. 기존 κ를 고정하면 평균수명은 {D["frozen_parent_kappa_lifetime_s"]:.6f} s이며, 878.3 s를 다시 맞추는 별도 κ는 {D["separately_refitted_kappa"]:.9f}이다. 수명 반환을 새 예측으로 취급하지 않는다.')
p(f'구현·독립 검증 {V["total_checks"]}개가 통과한다. 보정 외 중성자 자기 반지름 {R["unfitted_diagnostic"]["neutron_magnetic_radius_fm"]:.6f} fm는 비교값 0.864 fm와 차이가 남는다. 본 단계는 재현 가능한 전류 보강과 보정의 분리 장부를 남기며, 완전한 정밀 β 이론이나 상대론적 미시 핵자 모형을 주장하지 않는다.')
h('1. 계승 기준과 연구 범위')
table('표 1. 상류 0.6의 입력과 산출',['구분','이번 단계의 계약'],[
['계승','0.5의 H·바닥상태·Δ·C·η·λ=1, 부모 κ와 활동 R'],
['새 보정 입력','양성자 rE=0.84075 fm, 중성자 rE²=−0.1155 fm²'],
['새 산출','ℓ·cE, 유한 Q² 전류, Foldy 분해, 붕괴율 제어와 별도 κ'],
['보정 외 진단','자기 반지름, 곡률의 구성 의존성, K=10 고정 입력 검증']],[1.35,5.55])
p('상류가 남길 것은 생성 모형의 명시적인 입력·변환·산출과 수정 가능한 계산 증거이다. 0.6은 내부 공간을 전류와 붕괴 판독으로 연결한다. Core 1.0·MCC 2.3.2 및 기존 하류·공개본은 별도 기준으로 보존한다. 이번 0.4–0.6 교정 자료집은 별도 Zenodo 기록으로 공개한다.')

page();h('2. 점전하 정의와 영전하 보정항')
p('기준은 K=8의 165개 공간 모드와 95개 순열 대칭 상태이다. 무차원 내부 결합과 바닥벡터 g는 0.5와 동일하다. 중심을 제거한 세 구성 좌표 rᵢ에서 구면 평균 j₀를 취하며, HC=ℏc=0.1973269804 GeV fm를 단위 변환에 쓴다. Q²는 비음수 공간꼴 운동량 제곱이다.')
eq(1,r'G_{E,B}^{\mathrm{point}}(Q^2)=\langle g\rvert\sum_{i=1}^{3}{q_{i,B}j_0(\sqrt{Q^2}\,r_i/HC)}\lvert g\rangle')
eq(2,r'C_E(Q^2)=-\frac{Q^2 c_E}{6HC^2}\exp\!\left[-\frac{Q^2 a_E^2}{6HC^2}\right],\quad a_E=\ell')
eq(3,r'G_{E,p}=G_{E,p}^{\mathrm{point}}+C_E,\quad G_{E,n}=G_{E,n}^{\mathrm{point}}-C_E')
p('C_E(0)=0이므로 양성자 전하 1과 중성자 전하 0은 바뀌지 않는다. aE는 유한 운동량 곡률을 정하는 공개된 구성 길이이다. 보정항은 투영 공간의 항등 연산자에 더하므로 독립적인 여기 전환을 생성하지 않는다. 그 미시적 기원을 현재 결합에서 유도하지 않았다.')
eq(4,r'r_{E,B}^2=-6HC^2G_{E,B}^{\prime}(0),\quad a_B=\langle g\rvert\sum_i{q_{i,B}r_i^2/\ell^2}\lvert g\rangle')
eq(5,r'\ell^2=\frac{r_{E,p}^2+r_{E,n}^2}{a_p+a_n},\quad c_E=r_{E,p}^2-\ell^2a_p')
table('표 2. 전하 반지름의 공동 보정; fm²',['핵자','점전하 부분','보정항','합'],[[n,f'{S[k]["point_radius_squared_fm2"]:.9f}',f'{S[k]["counterterm_signed_fm2"]:.9f}',f'{S[k]["sachs_charge_radius_squared_fm2"]:.9f}'] for n,k in [('양성자','proton'),('중성자','neutron')]],[1.0,1.95,1.95,2.0])
p('양성자 반지름은 NIST의 0.84075(64) fm, 중성자 평균제곱 반지름은 PDG 2026의 −0.1155(17) fm²를 보정 입력으로 삼는다 [1, 2]. 0.5의 ℓ=0.616196218 fm를 그대로 두고 추가항만 더하지 않고, 두 입력으로 ℓ와 cE를 함께 정했다. 결과는 선택한 전하 구성 아래의 유효 폭이다. 관측 입력의 오차를 완전한 모형 신뢰구간으로 전파한 단계는 아니다.')

page();h('3. 같은 상태의 자기·약한 전류와 연속 방정식')
p('모든 전류는 순열 투영 Q와 동일한 바닥상태 g를 사용한다. σzi는 구성 스핀, μi는 계승한 구성 자기 응답이며, jᵢ=j₀(√Q²rᵢ/HC), j̄=(j₁+j₂+j₃)/3으로 쓴다. τp=+1, τn=−1이다.')
eq(6,r'M_B(Q^2)=Q^\dagger\sum_i{\mu_i\sigma_{zi}j_i}Q+c_0Q^\dagger\bar jQ+\frac{\tau_B\eta x_c}{2}\{Q^\dagger\bar jQ,W_\lambda\}')
p('자기 기대값은 핵자 자석온 μN 단위이다. 마지막 반교환항은 Hermitian 결합 판독이며 Q²=0에서 기존 ηxcWλ로 돌아간다. 따라서 μp=2.79284734463 μN와 μn=−1.91304276 μN를 그대로 반환한다. 이 유한 운동량 자기 구성은 추가 관측 자료에 맞추지 않았다.')
eq(7,r'G_V^{\mathrm{point}}=\langle g\rvert\sum_i{\tau_i^+j_i}\lvert g\rangle,\quad G_A=\langle g\rvert\sum_i{\tau_i^+\sigma_{zi}j_i}\lvert g\rangle')
eq(8,r'G_V^{\mathrm{point}}=G_{E,p}^{\mathrm{point}}-G_{E,n}^{\mathrm{point}},\quad G_E^V=G_V^{\mathrm{point}}+2C_E')
p('벡터 전환은 실제 n→p 맛 연산자를 각 구성 슬롯에 적용하여 전자기 차와 별도로 계산한다. 같은 공간 상태와 아이소스핀 질량 관례 아래 두 경로가 일치한다. GA(0)=1.2753을 유지하며, 물리적 중성자·양성자 질량 차에 의한 동역학적 아이소스핀 파괴를 새로 계산하지 않는다.')
eq(9,r'J_L(q)=\frac{\left[H,\rho(q)\right]}{q},\quad q=1000\sqrt{Q^2}\,\mathrm{MeV},\quad q>0')
p('ρ는 짝수 운동량의 Hermitian 단극자 밀도이다. 이에 대한 JL은 홀수 Fourier 종방향 진폭으로, JL(q)†=JL(−q)=−JL(q)이다. 국소 위치 공간의 Hermitian 전류와 같은 행렬이라고 해석하지 않는다. 이 정의는 투영 연속 관계를 만족하는 종방향 구성으로, 횡전류나 완전한 상대론적 게이지 동역학을 결정하지 않는다.')
eq(10,r'q(J_L)_{mn}=(E_m-E_n)\rho_{mn},\quad \frac{d\rho}{dt}=i\left[H,\rho\right]\quad(\hbar=1)')
p('ρ(q)는 점전하와 보정항을 포함한 전체 투영 전하 행렬이다. 두 핵자에서 Q²=0.01·0.1 GeV²의 모든 전환 원소와 중첩 상태의 실제 시간 진화를 확인했다. 식 (9)는 이 유한 투영 공간에서 연속 방정식을 완성하는 종방향 구성이다. 이를 전체 사차원 게이지 이론의 도출이나 유일한 횡방향 전류로 해석하지 않는다.')

page();h('4. Sachs–Dirac–Pauli 변환과 Foldy 항의 분리')
p('공통 아이소스핀 질량 M̄=(mp+mn)/2=938.918755685 MeV를 사용한다. μN=e/(2mp) 단위의 자기 판독은 공통 질량 단위로 바꾸어 두 핵자에 같은 τ를 적용한다. 물리 질량은 β 위상 공간에 별도로 유지한다.')
eq(11,r'G_{M,B}=\frac{\bar M}{m_p}\langle M_B\rangle,\quad \tau=\frac{Q^2}{4\bar M^2},\quad \bar M/m_p=1.00068920973')
eq(12,r'F_{1,B}=\frac{G_{E,B}+\tau G_{M,B}}{1+\tau},\quad F_{2,B}=\frac{G_{M,B}-G_{E,B}}{1+\tau}')
eq(13,r'r_{E,B}^2=r_{1,B}^2+r_{F,B}^2,\quad r_{F,B}^2=\frac{3HC^2F_{2,B}(0)}{2\bar M^2},\quad r_{1,B}^2=-6HC^2F_{1,B}^{\prime}(0)')
p('0.5의 공간 점전하 판독은 Sachs 정의였다. 그러므로 거기에 Foldy 항을 추가하면 같은 변환을 중복 계산한다. 먼저 보강한 Sachs 함수를 구성하고 식 (12)로 F1·F2를 얻어 식 (13)을 확인한다. Foldy 분해는 총 반지름에 대한 항등 관계이며, 부족한 전하를 그 항 하나가 독립적으로 설명한다는 주장이 아니다 [3].')
table('표 3. 동일 Sachs 반지름의 분해; fm²',['핵자','Dirac 부분','Foldy 부분','합'],[[n,f'{S[k]["dirac_radius_squared_fm2"]:.9f}',f'{S[k]["foldy_radius_squared_fm2"]:.9f}',f'{S[k]["sachs_charge_radius_squared_fm2"]:.9f}'] for n,k in [('양성자','proton'),('중성자','neutron')]],[1.0,1.95,1.95,2.0])
eq(14,r'F_1^V=F_{1,p}-F_{1,n},\quad F_2^V=F_{2,p}-F_{2,n}')
table('표 4. β 붕괴로 넘기는 약한 전류',['항목','Q²=0 값','Q² 기울기 GeV⁻²'],[[x,f'{S["weak"][y]:.9f}',f'{S["weak"][z]:.9f}'] for x,y,z in [('F1V','F1V0','F1V_prime'),('F2V','F2V0','F2V_prime'),('GA','GA0','GA_prime')]],[1.35,2.6,2.95])
p('F2V(0)=3.709133450은 공통 질량에 맞춘 자석온 변환을 포함한다. M̄=mp 관례의 3.705890105와 정의가 다르다. 축벡터 평균제곱 반지름은 0.787922026 fm²이다. 이는 같은 상태의 구성 전류에서 얻은 조건부 값이며 새 실험 보정 입력이 아니다.')

page();h('5. 유한 운동량 산출과 구성 선택의 민감도')
table('표 5. 기준 aE=ℓ에서의 실제 전류 기대값',['Q² GeV²','GEp','GEn','GMp / μN','GMn / μN','GA'],[[f'{v["Q2_GeV2"]:.3f}',f'{v["proton"]["GE"]:.7f}',f'{v["neutron"]["GE"]:.7f}',f'{v["proton"]["GM_muN"]:.7f}',f'{v["neutron"]["GM_muN"]:.7f}',f'{v["weak"]["GAV"]:.7f}'] for v in R['form_factors']],[1.0,1.18,1.18,1.18,1.18,1.18])
p('표 5는 전류의 실제 구면 평균을 적분한 값이다. 선형 반지름 식을 유한 Q²까지 그대로 외삽한 값이 아니다. aE/ℓ=0.5·1·2를 바꾸면 전하와 원점 기울기는 같지만 유한 Q² 곡률은 달라진다. 이 단계에서는 유한 Q² 전자 산란 자료를 맞추지 않았으므로 곡선의 유일성이나 실험 정밀 일치를 주장하지 않는다.')
fig('finite_currents','그림 1. 보정항 길이에 따른 Sachs 전하 곡선. 선은 저장된 계산 지점 사이의 연결이며, 관측 자료나 신뢰구간이 아니다. 세 선택은 같은 전하 반지름을 반환한다.')
table('표 6. 보정 외 진단과 고정 입력 공간 확대',['항목','계산','판정'],[
['중성자 자기 반지름','0.831987107 fm','PDG 0.864 +0.009/−0.008 fm와 차이 [1]'],
['K=10 양성자 rE²','0.706850693 fm²','K=8과 차이 −0.000009869 fm²'],
['K=10 중성자 rE²','−0.115498192 fm²','K=8과 차이 +0.000001808 fm²'],
['Q²=0.1, K=10−K=8','|ΔGM / μN| <0.000016','ℓ·cE·내부 계수 재보정 없이 확인']],[2.1,2.0,2.8])
p('더 큰 공간은 286개 모드와 161개 대칭 상태를 사용한다. 수치 수렴과 물리 자료 일치는 다른 주장이다. 공간 확대의 작은 차이로 중성자 자기 반지름의 약 0.032 fm 차이가 해소되지는 않는다.')

page();h('6. 세 입자 β 붕괴와 전류의 작은 시간꼴 연속')
p('정지한 비편극 중성자의 n→p+e⁻+ν̄e를 계산하며 반중성미자 질량은 0으로 둔다. 계량은 (+,−,−,−), q=pp−pn이다. 이 부호에서 약한 자기항은 +iσq/(mp+mn)이며 축벡터 크기 GA>0의 앞에는 음의 부호가 온다 [4].')
eq(15,r'\Gamma^\mu=F_1^V\gamma^\mu+\frac{iF_2^V\sigma^{\mu\nu}q_\nu}{m_p+m_n}-G_A\gamma^\mu\gamma_5')
eq(16,r'L_{\mu\nu}=\mathrm{Tr}\left[(\not p_e+m_e)\gamma_\mu(1-\gamma_5)\not p_\nu\gamma_\nu(1-\gamma_5)\right]')
eq(17,r'H^{\mu\nu}=\frac12\mathrm{Tr}\left[(\not p_p+m_p)\Gamma^\mu(\not p_n+m_n)\bar\Gamma^\nu\right],\quad\bar\Gamma^\nu=\gamma^0(\Gamma^\nu)^\dagger\gamma^0')
p('전자 전체 에너지를 E, 전자와 반중성미자의 각도 코사인을 z로 놓는다. 에너지·운동량 보존으로 반중성미자 에너지 k와 적분 상한 Em을 직접 정한다. 양성자 질량 껍질 잔차는 최대 3.5×10⁻¹⁰ MeV²이며 확률은 양수·실수로 확인했다.')
eq(18,r'p=\sqrt{E^2-m_e^2},\quad D=m_n-E+pz,\quad k=\frac{m_n^2+m_e^2-m_p^2-2m_nE}{2D}')
eq(19,r'E_m=\frac{m_n^2+m_e^2-m_p^2}{2m_n},\quad\mathcal T(E,z)=\frac{pk}{D}L_{\mu\nu}H^{\mu\nu}')
eq(20,r'K_{\mathrm{tree}}=\frac{\int_{m_e}^{E_m}dE\,F(E)\int_{-1}^{1}dz\,\mathcal T(E,z)}{64m_n(1+3g_A^2)I_0}')
p('I0=0.0589405883156 MeV⁵는 기존 점 Coulomb 함수를 포함한 부모 허용 근사 적분이다. Em=1.292581317469 MeV는 부모 상한 mn−mp=1.29333251 MeV보다 작다. 식 (20)의 정규화는 독립 스피너 합과 매우 큰 핵자 질량의 허용 극한으로 검증했다.')
eq(21,r'F_j(t)=F_j(0)-tF_j^{\prime}(0),\quad Q^2=-t,\quad t=q^2,\quad j=1V,2V,A')
p('기울기는 표 4의 공간꼴 계산에서 가져온다. 적분 지점의 t 범위는 약 2.61×10⁻⁷…1.66×10⁻⁶ GeV²이므로 이번 구현은 작은 시간꼴 운동량에 대한 1차 분석적 연속이다. 시간꼴 자료 보정, 유도 의사스칼라 GP, pion pole 및 second-class 전류는 포함하지 않았다.')

page();h('7. 복사 보정의 명시적 조립')
p('부모 Coulomb 함수 F(E)=x/(1−e⁻ˣ), x=2παemE/p를 그대로 유지한다. 선도 외부 복사 보정은 Sirlin의 전자 포괄 스펙트럼 함수 g(E,Em)를 쓴다 [4, 식 108]. 전자 포괄은 관측하지 않은 실광자의 기여를 함께 포함하는 정의이다.')
eq(22,r'\beta=p/E,\quad A=\mathrm{atanh}\,\beta,\quad d=E_m-E')
eq(23,r'g=g_0+g_1+g_2,\quad g_0=3\ln(m_p/m_e)-3/4')
eq('23a',r'g_1=4(A/\beta-1)\left[\ln(2d/m_e)+d/(3E)-3/2\right]')
eq('23b',r'g_2=-\frac4\beta\mathrm{Li}_2\!\left(\frac{2\beta}{1+\beta}\right)+\frac A\beta\left[2+2\beta^2+d^2/(6E^2)-4A\right]')
eq(24,r'\delta K_{\mathrm{out}}=\frac1{I_0}\int_{m_e}^{E_m}dE\,pE(E_m-E)^2F(E)\frac{\alpha_{\mathrm{em}}}{2\pi}g(E,E_m)')
p('외부 항은 선도 허용 스펙트럼에 더한다. 정확한 반동 tree 결과 전체에 g를 곱해 혼합 복사·반동 항을 완성했다고 취급하지 않는다. 내부 기준 ΔRV=0.02467(22)는 Seng 등 2018의 공개값을 고정하여 사용한다 [5]. 이는 최신값이라는 주장이나 본 모형의 미시 γW 상자 계산이 아니다.')
eq(25,r'K_\beta=(K_{\mathrm{tree}}+\delta K_{\mathrm{out}})(1+\Delta_R^V)')
table('표 7. 부모 허용 근사 붕괴율에 대한 제어',['적용','붕괴율 비율 또는 증분'],[
['반동만',f'{D["tree_cases"][0]["rate_ratio_to_parent_allowed"]:.11f}'],
['반동 + 약한 자기항',f'{D["tree_cases"][1]["rate_ratio_to_parent_allowed"]:.11f}'],
['반동 + 유한 전류',f'{D["tree_cases"][2]["rate_ratio_to_parent_allowed"]:.11f}'],
['외부 복사 증분 δKout',f'{D["outer_rate_increment_relative_parent"]:.11f}'],
['내부 기준 ΔRV','0.02467 ± 0.00022'],
['전체 Kβ',f'{D["full_rate_ratio_relative_parent"]:.11f}']],[3.9,3.0])
p('경험적 λ=−1.2753은 재정규화된 축벡터/벡터 비로 사용한다. 그 비를 쓴 뒤 공통 내부 정규화를 적용하며, 별도 축벡터 내부항을 새 보정으로 넣지 않는다 [4]. 고차 QED, 완전한 αE/M 혼합항과 동역학적 아이소스핀 파괴가 빠져 있으므로 이 수치를 10⁻⁴ 수준의 완결된 물리 정밀도로 주장하지 않는다.')

page();h('8. 고정 κ의 변화와 별도 수명 재보정')
eq(26,r'\Gamma_0=\frac{\kappa^2 R G_F^2\lvert V_{ud}\rvert^2(1+3g_A^2)I_0}{2\pi^3\hbar},\quad\tau_{\mathrm{frozen}}=(\Gamma_0K_\beta)^{-1}')
eq(27,r'\kappa_{0.6}=\kappa_{\mathrm{parent}}\sqrt{\frac{\tau_{\mathrm{frozen}}}{878.3\,\mathrm s}}')
p('식 (26)은 GF를 MeV⁻²로 바꾸고 실제 입력 상수와 적분값으로 초당 붕괴율을 계산한다. 부모 τ를 코드에 그대로 반환하는 경로가 아니다. R=0.00698600035273, GF=1.1663787×10⁻⁵ GeV⁻²와 Vud=0.97367은 계승 기준이다 [6]. 두 κ를 명확히 다른 결과로 기록한다.')
table('표 8. κ와 수명 장부',['항목','부모 기준','0.6 제어·재보정'],[
['κ','12.200294834431','11.975301265858 (별도 보정)'],
['고정 κ의 평균수명','878.300000 s','846.204102380 s'],
['별도 κ 보정의 평균수명','—','878.300000 s (보정 반환)'],
['κ²R','1.039846550116','1.001847223675 (별도 보정)']],[2.05,2.0,2.85])
p('알려진 반동·복사 항을 적용하면 같은 목표 수명에 필요한 유효 활동 정규화가 1에 가까워진다. 이는 기존 수명 보정과 외부 물리 보정의 조합 결과이다. 소수 활동이 약한 결합의 절대 강도를 독립적으로 도출했다는 근거나 새 수명 예측으로 해석하지 않는다.')
fig('electron_spectrum','그림 2. 선도 외부 복사를 포함한 정규화 전자 스펙트럼. 저장된 구적 확률의 합은 1이며 평균 운동에너지는 0.300918944 MeV이다. 완전한 광자·전자·중성미자 배타적 사건 분포는 아니다.')
p('각도는 tree 위상 공간의 변수이다. 포괄 외부 복사로 바뀐 전자 스펙트럼을 동일한 광자 없는 tree 사건의 완전한 e–ν 각분포로 재해석하지 않는다. 내부 공통 인자는 정규화한 스펙트럼 모양에서는 소거된다.')

page();h('9. 자기장 이차 직접항과 독립 검증')
p('0.5의 내부 자기 응답에 더해 자기장 이차 직접항의 입력 계약을 명시한다. b=μNB의 MeV 값이며 dB는 미정 구성 계수이다. 기준은 dB=0, 제어는 ±0.0001 MeV⁻¹이다.')
eq(28,r'H_B(b)=H_B(0)-bM_B-\frac12b^2d_BI,\quad\chi_B^{\mathrm{total}}=\chi_B^{\mathrm{spectral}}+d_B')
p('dB는 영자기장 모멘트를 바꾸지 않는다. 전체 내부 응답은 기준 0.00092249478에서 양의 직접항 제어 시 0.00102249478, 음의 제어 시 0.00082249478 MeV⁻¹로 변한다. 두 핵자의 실제 작은 장 모멘트 미분과 일치한다. dB는 관측으로 정하지 않았으며 이 내부 응답을 완전한 실험 자기 편극률과 동일시하지 않는다.')
table(f'표 9. {V["total_checks"]}개 검사의 핵심 내용',['검증','결과'],[
['계승 코드·모형 및 투영 상태','0.5 해시·H·영운동량 기준 일치'],
['반지름·Sachs 변환·CVC','원점 기울기·분해·실제 슬롯 전환 일치'],
['투영 연속 방정식','전환 원소 및 시간 미분 일치'],
['스피너 대조·허용 극한','별도 스피너 합, Clifford 관계, 각상관 a 일치'],
['복사·붕괴 구적','적응 구적 및 120×16 대체 구적 일치'],
['구성 제어·오류 입력','길이 변화·관측 입력 변화·잘못된 입력 거부'],
['새 폴더 재현','결과 JSON 바이트 동일, 모든 검사 통과']],[2.3,4.6])
p(f'구현 검사 {V["implementation_checks"]}개와 별도 검증 {V["audit_checks"]}개가 통과했다. 스피너 검증은 서로 다른 세 (E,z) 지점에서 Dirac trace와 일치하며, 매우 큰 핵자 질량의 극한에서 허용 정규화와 a=(1−gA²)/(1+3gA²)를 반환한다. 검사 수는 경험적 타당성의 확률이 아니다.')
h('10. 다음 단계의 입력 계약과 결론')
p('0.6에서 남기는 것은 동일 상태의 유한 운동량 전류, 전하 보정항과 길이의 공동 보정, 명시적 CVC·투영 연속 관계, 반동·복사 보정 장부와 고정 κ/재보정 κ의 구분이다. 중성자 자기 반지름의 차이와 전하 곡률의 비유일성을 다음 단계의 검증 대상으로 넘긴다.')
p('다음 단계는 공개한 전류·ℓ·cE·aE·공통 질량 관례와 부모/재보정 κ를 구분하여 받아야 한다. 유한 Q² 자료의 외부 비교, 구성 전류의 추가 물리 근거 및 미정 직접항을 우선 점검한다. 보정값의 반환을 독립 예측으로 바꾸거나, 생략한 정밀 항을 검사 통과만으로 포함했다고 취급해서는 안 된다.')

page();h('재현 방법과 참고문헌')
p('Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0에서 실행했다. requirements.txt 설치 후 OPENBLAS_NUM_THREADS=2로 code/compute.py를 실행하고 verify_release.py로 검증한다. 원고의 수치는 실행된 results.json에서 읽는다. 자세한 입력·실행 순서·검증 한계는 README.md에, 출처와 계승 해시는 source/provenance.json에 있다. 원고 생성 코드는 source/note.py·build_doc.py이다.')
p('검사 판단은 반올림 전 값으로 수행하고, 결과 파일은 소수점 11자리로 직렬화한다. 복제 가능한 자료에는 실행 코드, 고정 입력, 결과·검증 장부, 원고 소스, Word와 PDF, SHA256SUMS가 포함된다. Word 수식은 편집 가능한 native 수식으로 생성하고 페이지 전체를 렌더링하여 확인한다.')
p('[1] Particle Data Group, Review of Particle Physics (2026), Baryon summary tables. 중성자 전하·자기 반지름, 축벡터와 수명 기준. https://pdg.lbl.gov/2026/tables/rpp2026-sum-baryons.pdf (확인 2026-10-03).')
p('[2] NIST, 2022 CODATA recommended value: proton rms charge radius, 0.84075(64) fm. https://physics.nist.gov/cgi-bin/cuu/Value?rp= (계승한 0.5 입력).')
p('[3] W. R. B. de Araújo, T. Frederico, M. Beyer and H. J. Weber, Neutron Charge Radius: Relativistic Effects and the Foldy Term, arXiv:hep-ph/0305120 (2003). https://arxiv.org/pdf/hep-ph/0305120. Sachs 정의와 Foldy 분해의 해석을 확인하는 참고 자료이며 그 논문의 동역학을 본 모형에 이식하지 않았다.')
p('[4] C.-Y. Seng, Radiative Corrections to Semileptonic Beta Decays: Progress and Challenges, Particles 4, 397–467 (2021), DOI 10.3390/particles4040034. 식 (108)의 전자 포괄 외부 함수와 식 (126)의 전류 관례. https://doi.org/10.3390/particles4040034.')
p('[5] C.-Y. Seng, M. Gorchtein, H. H. Patel and M. J. Ramsey-Musolf, Reduced hadronic uncertainty in the determination of Vud, Phys. Rev. Lett. 121, 241804 (2018), arXiv:1807.10197. ΔRV=0.02467(22)의 고정 참고 기준. https://arxiv.org/pdf/1807.10197.')
p('[6] Particle Data Group, CKM Quark-Mixing Matrix (2026). 계승 Vud 기준의 확인 자료. https://pdg.lbl.gov/2026/reviews/rpp2026-rev-ckm-matrix.pdf.')
p('[7] Wonsik Choi, 내부 공간의 안정성, 여기 척도와 핵자 크기, WRRA M 상류 0.5 (2026-10-02). GitHub commit 8ac07a7d33dcc29701e49d31650997ec77030eb6. https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/8ac07a7d33dcc29701e49d31650997ec77030eb6/upstream/spatial_scale_v0_5. 기존 검토 자료집 r1: DOI 10.5281/zenodo.23092499.')

h('교정판 r1의 변경 기록')
p('고정 Q²=0.1 GeV² 수렴점을 배열 위치와 분리했다. 운동량 목록의 역순·축소와 단일 조절 길이로 전체 실행을 검증했다. Fourier 전류의 수반 관계, 유한 차분 Dirac 반지름과 GF·Vud의 붕괴율 제곱 의존성을 추가 확인했다. 기존 물리 수치는 유지했다.')
p('이 교정 자료집 DOI: 10.5281/zenodo.23112253. 2026-10-03. 원본 0.4·0.5·0.6과 고정 계승 코드는 원래 해시로 보존하며, 교정 실행 경로와 새 검증 장부는 별도 공개한다. 검사 통과는 공개한 모형의 수치·입력 일관성에 대한 결과이며 실험적 타당성의 확률이 아니다.')
