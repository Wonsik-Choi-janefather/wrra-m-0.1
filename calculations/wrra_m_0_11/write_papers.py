"""Create matched manuscripts from executed sequential-calibration results."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent

def tables(r):
    v=r['input_ledger']['targets'];o=r['final_outputs']
    t1=[['G',f"{v['G_SI']:.7e}",'m³ kg⁻¹ s⁻²'],['H0',f"{v['H0_km_s_Mpc']:.1f}",'km s⁻¹ Mpc⁻¹'],['f_phi',f"{v['f_phi']:.4f}",'energy fraction'],['f_c',f"{v['f_c']:.3f}",'energy fraction'],['m_e c²',f"{v['electron_energy_eV']:.5f}",'eV']]
    t2=[['1','G','action coefficient; SI response','H0, f_phi, f_c, E_e'],['2','H0','H0 in s⁻¹; critical density','f_phi, f_c, E_e'],['3','f_phi','hidden density; weighted twist','f_c, E_e'],['4','f_c','sector energies; a_T, P, q','E_e'],['5','E_e','mass unit; electron units','structural freedoms remain']]
    names=[('ucrit J m⁻³','ucrit_J_m3'),('u_hidden J m⁻³','u_hidden_J_m3'),('eta_load J m⁻³','eta_load_J_m3'),('zeta kappa_h² m⁻²','weighted_twist_hidden_m_minus2'),('Length coefficient m','length_coefficient_m'),('a_T m s⁻²','aT_m_s2'),('P Pa','pressure_Pa'),('q0','q0'),('mu_E eV','mass_mode_scale_eV')]
    t3=[[label,f'{o[key]:.12e}'] for label,key in names]
    t4=[[f"{x['lambda_R']:.1f}",f"{x['reference_q']:.9f}",f"{x['K4_q']:.9f}"] for x in r['response_shape_degeneracy']]
    return [t1,t2,t3,t4]

def build(lang):
    ko=lang=='KO';r=json.loads((ROOT/'results/results.json').read_text());v=json.loads((ROOT/'results/verification.json').read_text());o=r['final_outputs'];rc=r['address_reparameterization'];s=[]
    def text(k,e):s.append(k if ko else e)
    def eq(n,latex):s.append('\n$$\n'+latex+r' \tag{'+str(n)+'}\n$$\n')
    def table(headers,rows):s.append('| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(row)+' |\n' for row in rows))
    text('# WRRA_M 0.11 첫 다섯 입력의 순차 보정','# WRRA_M 0.11 Sequential Calibration of the First Five Inputs')
    s.append('Wonsik Choi · 2026-10-02 · WRRA Core 1.0 / MCC 2.3.2 · CC BY 4.0')
    text('## 초록','## Abstract')
    text('고정된 WRRA Core 1.0과 MCC 2.3.2 위에서, 우리 우주에 특화된 WRRA_M의 첫 다섯 물리 입력을 G→H0→f_phi→f_c→전자 정지에너지 순서로 보정한다. 각 부분 단계는 아직 주어지지 않은 뒤의 목표를 읽지 않으며, 단계별 산출값과 남은 계수를 공개한다. 0.10의 에너지·압력 계산과 아홉 물리 사례를 유지하고, 주소 지수와 유효 입장률의 재표현 및 추가 산술 입력을 명시한다. 전자 모드 23과 영 절편을 채택하면 질량 단위는 22,217.345682 eV다. 동일 보정값을 만족하는 서로 다른 응답 형태를 계산하여 재현 성과와 식별되지 않은 자유도를 함께 기록한다.',
         'On fixed WRRA Core 1.0 and MCC 2.3.2, WRRA_M calibrates its first five physical inputs in the order G→H0→f_phi→f_c→electron rest energy. Each partial stage reads only supplied anchors and reports available outputs and remaining coefficients. The 0.10 energy-pressure calculation and nine physical cases are retained. Address-exponent and effective-admission reparameterization explicitly discloses additional arithmetic inputs. Adopting electron mode 23 and zero intercept gives a mass unit of 22,217.345682 eV. Two response shapes fitting the same anchors demonstrate reproduction together with residual freedoms.')
    text('## 검증 입력','## Verification inputs')
    text('전체 0.10 입력은 해시로 고정한다. G와 전자 에너지는 NIST 2022 CODATA 값을 사용하며, H0=67.4는 Planck 2018의 기본 LambdaCDM 보정 기준이다. G의 표준 불확도는 1.5×10⁻¹⁵ SI, 전자 에너지는 0.00016 eV, 채택 H0 기준은 0.5 km s⁻¹ Mpc⁻¹다. 물리 구성비 4.93%·26.5%는 계승한 반올림 보정값이며 이번 판에서 공분산을 부여하지 않는다. 후보표의 첫 다섯 행과 MCC의 전자 모드 관계를 출처로 기록한다.',
         'The complete 0.10 input is frozen by hash. G and electron energy use NIST 2022 CODATA; H0=67.4 is the Planck 2018 base-LambdaCDM calibration benchmark. Standard uncertainties are 1.5×10⁻¹⁵ SI for G, 0.00016 eV for electron energy and 0.5 km s⁻¹ Mpc⁻¹ for the adopted H0 benchmark. Physical fractions 4.93% and 26.5% are inherited rounded calibrations without a covariance assigned here. The first five candidate-sheet entries and the MCC electron-mode relation are recorded as provenance.')
    ts=tables(r);table(['Input','Adopted value','Unit / role'],ts[0])
    text('c=299792458 m/s는 고정 입력이다. h=6.62607015×10⁻³⁴ J s와 1 eV=1.602176634×10⁻¹⁹ J는 정확한 SI 기준이다. 파섹 환산과 기존 국소 질량·반경·응답 함수 및 Phi=Psi 렌즈 조건은 계승한다. 주소 컷오프, 제타 영점 네 개, K=8, 위상 간격 0.1, 응답 계수 lambda_s, 부피 지수와 전자 모드 정수는 구성 입력이다. 이것들은 다섯 수치에서 새로 도출되지 않는다.',
         'c=299792458 m/s is fixed. h=6.62607015×10⁻³⁴ J s and 1 eV=1.602176634×10⁻¹⁹ J are exact SI references. The parsec conversion, local masses/radii/response function and conditional Phi=Psi lensing are inherited. Address cutoff, four zeta heights, K=8, phase increment 0.1, response coefficients lambda_s, volume exponents and the electron-mode integer are constitutive inputs; the five numerical anchors do not derive them.')
    text('## WRRA 고유 변환','## WRRA-specific transformation')
    text('한 번에 한 입력만 추가하는 부분 계산을 실행한다. G는 작용의 SI 정규화와 곡률 응답을 고정한다. 정확한 h와 c를 함께 쓰면 플랑크 길이·시간도 단위 기준으로 계산된다. 뒤의 H0·구성비·전자 에너지를 NaN으로 바꿔도 해당 앞 단계 출력이 같아야 한다.',
         'The partial calculator adds one anchor at a time. G fixes the SI action normalization and curvature response. Exact h and c additionally give Planck length/time as unit references. Replacing all future anchors with NaN must leave the corresponding earlier-stage outputs unchanged.')
    eq(1,r'C_G=\frac{c^4}{16\pi G},\qquad B_G=\frac{8\pi G}{c^4},\qquad \ell_P=\sqrt{\frac{\hbar G}{c^3}},\quad t_P=\ell_P/c.')
    text('H0를 초의 역수로 환산한 뒤 임계 에너지 밀도를 계산한다. c/H0와 1/H0는 허블 길이·시간 기준이며 실제 우주의 전체 크기나 나이로 확정하지 않는다.',
         'After converting H0 to inverse seconds, the critical energy density is calculated. c/H0 and 1/H0 are Hubble length/time references, not assignments of the total cosmic size or age.')
    eq(2,r'H_0=\frac{H_{0,\mathrm{km/s/Mpc}}\,10^3}{10^6\,\mathrm{pc}_{\mathrm m}},\qquad u_{\mathrm{crit}}=\frac{3H_0^2c^2}{8\pi G}.')
    text('표현형 구성비가 주어지면 숨은 전체 부하를 계산한다. 이어 모이는 부하 f_c를 넣어 D와 배경 R을 분리한다. eta_load는 0.6의 균질 운반자 기준 부하 계수이며 0.10의 주소별 eta_s와 다른 기호다.',
         'The phenotype fraction gives the total hidden load. Adding the clustering fraction f_c separates D from background R. eta_load is the homogeneous-carrier reference coefficient of 0.6, distinct from the address-sector eta_s coefficients of 0.10.')
    eq(3,r'f_h=1-f_\varphi,\quad f_b=1-f_\varphi-f_c,\quad u_h=f_hu_{\mathrm{crit}},\quad \eta_{\mathrm{load}}=u_h/2.')
    eq(4,r'Q_h\equiv\zeta\kappa_h^2=\frac{16\pi G u_h}{c^4},\qquad L_*=Q_h^{-1/2},\qquad L_0=L_*\sqrt{W_0}.')
    text('식별되는 것은 가중 뒤틀림 Q_h다. 강성 zeta와 뒤틀림 kappa_h는 따로 정해지지 않는다. L_star는 계산된 길이 계수이고, W0가 주어지지 않아 L0는 미정이다. 95.07%라는 구성비만으로 우주 길이를 정하지 않는다.',
         'The identifiable quantity is weighted twist Q_h. Stiffness zeta and twist kappa_h are not separately determined. L_star is a calculated length coefficient; L0 remains undetermined without W0. The 95.07% hidden share alone does not fix cosmic length.')
    table(['Step','New input','Newly available outputs','Remaining anchors / choices'],ts[1])
    text('0.10의 주소 효과 e_s(n), 정규화 가중치 w_n과 양의 응답 g_s(n)를 그대로 사용한다. 각 eta_s는 기준 주소 상태와 균질 운반자에서 한 번 맞춘 뒤 주소·상태 대조에서는 고정한다. 운반자 연산자는 A_phi=I, A_D=Kc/2, A_R=Kb/2이며 기준 균질 기대값은 모두 1이다.',
         'The 0.10 address effects e_s(n), normalized weights w_n and positive responses g_s(n) are retained. Each eta_s is fitted once on the reference address state and uniform carrier, then held fixed for address/state controls. Carrier operators are A_phi=I, A_D=Kc/2 and A_R=Kb/2, each with unit uniform reference expectation.')
    eq(5,r'\mu_s=\sum_nw_ne_s(n)g_s(n),\quad \eta_s=\frac{f_su_{\mathrm{crit}}}{\mu_s},\quad \widehat E(a)=V_0\sum_s\eta_s\mu_sa^{\nu_s}A_s.')
    text('압력은 같은 에너지 함수의 부피 미분이다. 지수 nu_phi=nu_D=0, nu_R=3을 유지하므로 D와 표현형은 무압력이고 R은 P_R=−u_R다. 부하가 비표현형이라는 이유로 에너지나 중력을 지우지 않는다.',
         'Pressure is the volume derivative of the same energy function. Retaining nu_phi=nu_D=0 and nu_R=3 gives pressureless D/phenotype and P_R=−u_R. Nonphenotype status does not delete energy or gravity.')
    eq(6,r'V=V_0a^3,\qquad E_s=\operatorname{Tr}(\rho\widehat E_s),\qquad P_s=-\partial E_s/\partial V=-\nu_su_s/3.')
    eq(7,r'a_T=cH_0\sqrt{f_c/8},\qquad P_0=-f_bu_{\mathrm{crit}},\qquad q_0=(1-3f_b)/2.')
    text('MCC의 영 절편 질량 가지에서 전자 모드 n_e=23을 채택한다. 전자 입력은 이 가지의 공통 에너지 단위를 정한다. 보고하는 ±1·±2·±3·±23은 일반 모드 대조이며 다른 입자의 질량 동정이 아니다. 모드 부호는 같은 정지에너지를 주고, 전하는 기존 필터 장부에서 별도로 유지된다. 모드 수와 영 절편은 추가 구성 선택이다.',
         'Electron mode n_e=23 is adopted in the zero-intercept MCC mass branch. The electron anchor fixes its common energy unit. Reported ±1, ±2, ±3 and ±23 are generic mode controls, not identifications of other particle masses. Mode sign has the same rest energy; charge remains separately inherited from the filter ledger. Mode number and zero intercept are additional constitutive choices.')
    eq(8,r'E_n=\sqrt{E_{\mathrm{off}}^2+n^2\mu_E^2},\qquad E_{\mathrm{off}}=0,\qquad \mu_E=E_e/23,\quad E_e=m_ec^2.')
    text('같은 총 에너지 연산자를 전자 에너지 단위로 재표현한다. 차원 없는 값에 E_e를 다시 곱하면 원래 J 장부가 복원된다. 전자의 에너지를 우주 전체 밀도에 별도로 더하지 않는다. 미시 모드의 실제 경계조건과 시계 및 일반 스펙트럼은 0.12에 남긴다.',
         'The same total energy operator is expressed in electron-energy units. Multiplying back by E_e restores the original joule ledger. Electron energy is not separately added to cosmic density. Physical boundary conditions, the microscopic clock and general spectra remain for 0.12.')
    eq(9,r'\widetilde E_e=\widehat E/E_e,\qquad \widehat E=E_e\widetilde E_e,\qquad m_e=E_e/c^2.')
    text('## 주소 alpha와 beta의 재표현','## Re-expression of address alpha and beta')
    text('여기서 alpha_addr는 주소 가중치의 멱 지수, beta_eff는 홀수 합성수의 유효 입장률이다. 전자기 미세구조상수 alpha_EM과 구분한다. 0.9의 독립 산술 목표 D=0.268과 phi=0.05를 공개한 추가 입력으로 유지하며, 물리 에너지 목표 0.265·0.0493으로 대체하지 않는다. 짝수 합성수 집합 C_even은 소수 2를 제외한다.',
         'Here alpha_addr is the address power-law exponent and beta_eff is the effective admission rate of odd composites. These differ from electromagnetic fine-structure alpha_EM. The two independent 0.9 arithmetic targets D=0.268 and phi=0.05 remain disclosed additional inputs; physical energy targets 0.265 and 0.0493 do not replace them. C_even excludes the prime address 2.')
    eq(10,r'w_n(\alpha_{\mathrm{addr}})=\frac{n^{-\alpha_{\mathrm{addr}}}}{\sum_{j=2}^{N}j^{-\alpha_{\mathrm{addr}}}},\qquad \sum_{n\in C_{\mathrm{even}}}w_n=0.268.')
    eq(11,r'\sum_{n\in C_{\mathrm{odd}}}w_n b_n(h)=0.05,\qquad \beta_{\mathrm{eff}}=\frac{0.05}{\sum_{n\in C_{\mathrm{odd}}}w_n}.')
    text(f'고정한 위상·필터에서 다시 풀면 alpha_addr={rc["alpha"]:.12f}, h={rc["threshold_h"]:.12f}, beta_eff={rc["derived_effective_beta"]:.12f}다. alpha_addr와 h는 두 산술 목표에 맞춘 두 계수이며 beta_eff는 그 뒤의 재표현으로 계산된다. 세 번째 독립 beta 입력은 필요하지 않다. 다섯 물리 입력만으로 산술 목표나 alpha_EM을 정했다는 주장은 하지 않는다.',
         f'Resolving the fixed phase/filter gives alpha_addr={rc["alpha"]:.12f}, h={rc["threshold_h"]:.12f} and beta_eff={rc["derived_effective_beta"]:.12f}. Alpha_addr and h fit the two arithmetic targets; beta_eff is then derived as their re-expression. A third independent beta input is unnecessary. The five physical anchors alone do not determine arithmetic targets or alpha_EM.')
    text('## 산출값','## Calculated outputs')
    table(['Quantity','Calculated value'],ts[2])
    text(f'기준 q0는 {o["q0"]:.9f}이며 국소 회전 속도 {r["reference"]["local_readout"]["v_total_km_s"]:.9f} km/s와 조건부 렌즈 편향 {r["reference"]["local_readout"]["finite_patch_lensing"]["alpha_patch_arcsec"]:.9f} arcsec를 유지한다. 질량 단위는 {o["mass_mode_scale_eV"]:.9f} eV다. 이 결과는 공개 입력을 통한 현실 기준 재현과 내부 계산으로 판정한다. 새 독립 예측이 완료의 선행조건은 아니다.',
         f'The reference retains q0={o["q0"]:.9f}, local rotation speed {r["reference"]["local_readout"]["v_total_km_s"]:.9f} km/s and conditional lens deflection {r["reference"]["local_readout"]["finite_patch_lensing"]["alpha_patch_arcsec"]:.9f} arcsec. The mass unit is {o["mass_mode_scale_eV"]:.9f} eV. These are reproduction of validated benchmarks and internal calculations under disclosed inputs. A new independent prediction is not a prerequisite for completion.')
    text('남은 자유도는 계산 대조로 표시한다. zeta와 kappa_h를 다음처럼 바꾸어도 Q_h는 같다. 또한 lambda_R=0과 1에서 각각 기준 eta_R를 맞추면 같은 다섯 목표와 같은 기준 q를 얻지만, 보정 뒤 K를 4로 바꾼 결과는 서로 다르다. 따라서 기준의 곱 eta_s mu_s를 맞추는 것과 전체 응답 형태를 정하는 것은 구분된다.',
         'Residual freedoms are shown by calculated controls. Rescaling zeta and kappa_h as below preserves Q_h. Separately fitting eta_R at lambda_R=0 and 1 reproduces the same five targets and reference q, yet changing K to 4 after calibration gives different results. Fitting reference products eta_s mu_s and determining the full response shape are separate achievements.')
    eq(12,r'\zeta\mapsto r\zeta,\qquad \kappa_h\mapsto\kappa_h/\sqrt r,\qquad \zeta\kappa_h^2\mapsto Q_h.')
    table(['lambda_R','Reference q','K=4 q after fitting'],ts[3])
    text('다섯 입력의 독립성은 출력 (C_G,ucrit,u_h,u_c,mu_E)의 로그 민감도 행렬로 점검한다. 고정한 구성 선택 아래 수치 계수 5가 확인된다. 이는 다섯 보정 앵커의 국소 식별이며 모든 모형 계수의 완전 식별을 뜻하지 않는다.',
         'Independence of the five anchors is checked using the logarithmic sensitivity of (C_G,ucrit,u_h,u_c,mu_E). The numerical rank is five conditional on frozen constitutive choices. This is local identification of the five calibration anchors, not identification of every model coefficient.')
    eq(13,r'\frac{\partial\log(C_G,u_{\mathrm{crit}},u_h,u_c,\mu_E)}{\partial\log(G,H_0,f_\varphi,f_c,E_e)}=\begin{pmatrix}-1&0&0&0&0\\-1&2&0&0&0\\-1&2&-f_\varphi/(1-f_\varphi)&0&0\\-1&2&0&1&0\\0&0&0&0&1\end{pmatrix}.')
    text('각 물리 입력을 ±1% 바꾼 열 가지 실행은 구성 민감도 대조이며 관측 신뢰구간이 아니다. 입력을 바꾼 경우에는 해당 물리 목표에 명시적으로 재보정하고, 주소 대조에서는 SI 계수를 고정한다. 전자 입력은 질량 단위를 바꾸지만 거시 밀도·q·회전 속도를 바꾸지 않는다. G 변화는 임계 밀도를 역비례로 바꾸고, H0 변화는 제곱으로 바꾼다.',
         'Ten runs changing each anchor by ±1% are construction-sensitivity controls, not observational confidence intervals. Changed physical targets are explicitly recalibrated; address controls hold SI coefficients fixed. Electron energy changes the mass unit but not macroscopic density, q or rotation speed. Critical density varies inversely with G and quadratically with H0.')
    text('고정 기준의 균질 팽창 출력은 같은 무압력·배경 에너지 관계를 사용한다. 비가환 운반자의 고정 부피 내부 교환은 총합 0이며, 상태의 양성과 정규화가 유지된다. 주소 입장에 필요한 변환 일과 환경 소유 계정은 0.10의 보존 검사로 계승한다.',
         'The fixed-reference homogeneous expansion uses the same pressureless/background energy relation. Noncommuting-carrier internal exchange at fixed volume sums to zero and preserves state positivity/normalization. The required conversion work and its environmental account retain the 0.10 conservation checks.')
    eq(14,r'\frac{H(a)^2}{H_0^2}=(f_\varphi+f_c)a^{-3}+f_b,\qquad \frac{du}{d\log a}+3(u+P)=0.')
    text('## 반증조건과 재현','## Falsifiers and reproduction')
    text(f'앞 단계가 뒤 목표를 읽거나, 입력 순서가 바뀌거나, 에너지·압력 미분 및 0.10의 현실 기준 재현에 실패하거나, 전자 에너지를 중복 합산하거나, 식별되지 않은 W0·zeta·alpha_EM을 확정량으로 쓰면 해당 연결을 수정한다. 이번 판의 {v["check_count"]}개 검사와 계승한 0.10의 32개 검사를 실행한다. 영점·모드 부호, 5점 압력 미분, 로그 민감도, 실제 자유도 대조, 보존과 잘못된 입력 거부를 포함한다.',
         f'The connection must be revised if an earlier stage reads future targets, input order changes, energy-pressure differentiation or inherited benchmark reproduction fails, electron energy is duplicated, or unidentified W0, zeta or alpha_EM is used as determined. This release executes {v["check_count"]} checks plus 32 inherited 0.10 checks, including zero/sign modes, five-point pressure differentiation, log sensitivities, explicit degeneracy controls, conservation and invalid-input rejection.')
    s.append('```bash\npython -m pip install -r calculations/wrra_m_0_11/requirements.txt\npython calculations/wrra_m_0_11/run_release.py\n```')
    text('공개 패키지의 parameters.json는 입력·단위·출처·구성 선택을 포함한다. 순차 보정, 물리 사례, 질량 모드와 입력 변화는 JSON 및 CSV로 제공한다. 결과를 모두 삭제한 새 복사본에서 같은 실행 결과와 한영 원고를 바이트 단위로 대조한다. Word와 PDF는 원고에서 만든 최종 공개 판이며 계산 결과와 수식·표를 대조하고 모든 페이지를 렌더링 검토한다.',
         'Parameters.json contains inputs, units, provenance and constitutive choices. Sequential calibration, physical cases, mass modes and input responses are supplied as JSON/CSV. A clean copy with all captured results removed compares regenerated outputs and bilingual sources byte for byte. Word/PDF are final publications built from those sources, with equations/tables checked against execution and every rendered page inspected.')
    s.append('Input SHA256 '+r['input_hash_sha256'])
    text('## 판정과 후속 범위','## Completion and subsequent scope')
    text('0.11은 공개한 다섯 입력의 순차 보정과 남은 자유도 표시를 완료한다. 보정값의 기원, 유일한 우주 해, 무보정 상수 도출은 이 판의 완료 조건이 아니다. 후속 0.12에서 시계·경계조건·스펙트럼, 0.13에서 물리 양자화·관측 뒤 상태·기록, 0.14 이후에서 불확실성·응력·곡률·크기와 중성미자 연결을 계산한다. 모형과 보정을 고정한 뒤 미측정량을 산출하면 그 입력과 반증조건을 붙여 WRRA의 예측으로 기록한다.',
         'Version 0.11 completes staged calibration of the five disclosed anchors and reporting of residual freedoms. Their origins, a unique universe solution and calibration-free constants are not completion requirements. Version 0.12 treats clocks/boundaries/spectra, 0.13 physical quantization/post-observation states/records, and later stages uncertainty, stress, curvature, size and neutrino connections. Unmeasured outputs produced after fixing the model and calibration are recorded as WRRA predictions with their inputs and falsifiers.')
    text('## 참고 자료','## References')
    s.append('Choi Wonsik. WRRA_M 0.10, frozen baseline commit 24707c512c3994f2b19a96d6f257ef7d1249dab3. https://github.com/Wonsik-Choi-janefather/wrra-m-0.1\n\nChoi Wonsik. Minimal Computation Cosmology 2.3.2, chapter 23, frozen commit 21daec110c0cbecb228c445d587eac8302e7f767. https://github.com/Wonsik-Choi-janefather/minimal-computing-cosmology-2.3.2\n\nChoi Wonsik. WRRA_M_Calibration_Candidates.xlsx, first-sheet reference; source hash in parameters.json.\n\nPlanck Collaboration. Planck 2018 results VI, A&A 641 A6 (2020). https://doi.org/10.1051/0004-6361/201833910\n\nNIST. CODATA 2022 constants table. https://physics.nist.gov/cuu/pdf/wall_2022.pdf\n\nCopyright 2026 Wonsik Choi. CC BY 4.0. https://creativecommons.org/licenses/by/4.0/')
    (ROOT/f'source_{lang.lower()}.md').write_text('\n\n'.join(s)+'\n')

if __name__=='__main__':build('KO');build('EN')
