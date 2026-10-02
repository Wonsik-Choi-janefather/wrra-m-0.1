"""Matched bilingual source papers from the executed 0.10 result ledger."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent


def build(lang):
    ko=lang=='KO';r=json.loads((ROOT/'results/results.json').read_text())
    verification=json.loads((ROOT/'results/verification.json').read_text())
    cfg=r['input_ledger'];cal=r['calibration'];s=[]
    ref=next(x for x in r['cases'] if x['case_name']=='uniform_a1.0')
    def text(k,e):s.append(k if ko else e)
    def eq(n,latex):s.append('\n$$\n'+latex+r' \tag{'+str(n)+'}\n$$\n')
    def table(headers,rows):s.append('| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,row))+' |\n' for row in rows))
    text('# WRRA M 0 10 주소별 정보 부하와 물리 에너지 및 압력 연결',
         '# WRRA M 0 10 Address Information Load and Physical Energy and Pressure')
    text('같은 에너지 함수로 계산하는 부문 교환과 중력 및 팽창',
         'Sector exchange gravity and expansion calculated from one energy functional')
    s.append('최원식 Wonsik Choi\n\n2026-10-02 · WRRA-M 0.10\n\nIndependent Researcher Seoul Republic of Korea\n\nORCID 0009-0001-4263-9772 · janefather@gmail.com')
    text('## 검증 입력과 계산 범위', '## Verification inputs and calculation scope')
    text('WRRA는 비특권적인 하나의 우주를 최소계산·공통운반자·표현형이라는 방법으로 설명하는 연구 구조다. WRRA_M은 고정된 WRRA Core 1.0과 최소계산우주론 MCC 2.3.2 위에서 우리 우주의 검증값과 채택 규칙을 실행하는 특화 모형이다. 이번 0.10은 0.9에서 실행한 주소별 산술 장부에 양의 SI 에너지 응답을 부여하고, 그 에너지의 부피 미분으로 압력을 계산한다.',
         'WRRA studies one nonprivileged universe through minimal computation, a common carrier and phenotype. WRRA_M specializes the frozen WRRA Core 1.0 and Minimal Computation Cosmology 2.3.2 to validated inputs and adopted rules for our universe. Version 0.10 supplies positive SI energy responses to the executable 0.9 address ledger and calculates pressure by differentiating that same energy with respect to volume.')
    text('검증 입력은 0.9-r1의 동결 입력, 0.6-r2부터 계승한 공통운반자 연산자와 G·H0·c 및 시험 질량·기하, 0.8의 입자 선택과 전하 장부다. 산술 구성비 5%·26.8%·68.2%와 기존 물리 에너지 보정 4.93%·26.5%·68.57%를 구분해 보존한다. 주소 응답 계수, 부피 지수와 주소·운반자 상태의 곱 구성은 공개한 모형 입력이다. c=299792458 m/s는 고정 입력이다.',
         'Verification inputs are the frozen 0.9-r1 ledger; inherited 0.6-r2 carrier operators, G, H0, c, test mass and geometry; and the 0.8 particle selection and charge ledger. The arithmetic partition 5%, 26.8%, 68.2% and the inherited energy calibration 4.93%, 26.5%, 68.57% remain distinct. Address-response coefficients, volume exponents and the product address-carrier state are disclosed constitutive inputs. The defining SI value c=299792458 m/s is fixed.')
    text('## WRRA 고유 변환', '## WRRA specific transformation')
    text('같은 주소 상태와 세 부문 효과에서 물리 응답을 가중 합산한다. 기준 상태에서 SI 계수를 한 번 보정한 뒤 주소와 운반자 상태가 바뀌어도 그 계수를 유지한다. 같은 에너지 연산자는 상태 갱신을 생성하고, 부피 의존성은 압력을 정한다. 모이는 D 에너지 밀도는 기존 국소 중력 응답으로, D와 R의 합은 뒤틀림 부하로, 전체 밀도와 압력은 동질 팽창으로 전달한다.',
         'The common address state and three sector effects are summed with physical response weights. SI coefficients are calibrated once on a frozen reference and held unchanged when address or carrier states change. The same energy operator generates state updates, while its volume dependence determines pressure. Clustering D density enters the inherited local gravity response, D plus R supplies the twist load, and total density and pressure enter homogeneous expansion.')
    text('## 산출값', '## Outputs')
    text(f'{verification["check_count"]}개 검사 묶음이 모두 통과했다. 기준 감속계수는 −0.52855, 회전속도는 207.5109051266 km/s, 조건부 유한 패치 렌즈 편향은 0.5355865106각초다. 0.8의 아홉 상태·부피 사례가 동일하게 재현됐다. 단위가 있는 주소별 에너지와 압력, 비가환 부문 교환, 입장 전환의 변환 일, 보정을 고정한 주소 규칙 변경의 물리 출력을 함께 산출했다.',
         f'All {verification["check_count"]} verification groups pass. The reference returns deceleration −0.52855, rotation 207.5109051266 km/s and conditional finite-patch deflection 0.5355865106 arcsec. All nine inherited 0.8 state-volume cases reproduce. Outputs include dimensional address energy and pressure, noncommuting sector exchange, admission conversion work and physical responses to changed address rules with calibration held fixed.')
    text('## 반증조건과 판정', '## Falsification conditions and assessment')
    text('허용 상태에서 음의 에너지가 나오거나, 고정 보정의 기준값 재현에 실패하거나, 독립 부피 미분과 압력이 어긋나거나, 내부 교환 합이 상쇄되지 않거나, 입장 전환의 에너지 차이에 교환 계정이 없으면 해당 연결을 수정한다. 입자 채널과 세대에 에너지를 중복 배정하거나 문서가 실행과 다르면 통합 판정도 실패한다. 이번 결과로 0.9의 비어 있던 에너지·압력 연결을 실제 계산으로 닫았다. 물리 측정 결과와 관측 기록 생성은 후속 0.13의 계산 대상이다.',
         'The connection must be revised if an admissible state yields negative energy, frozen calibration fails reference reproduction, pressure disagrees with an independent volume derivative, internal exchanges do not cancel, or admission energy changes have no exchange account. Duplicate channel or generation energy and disagreement between text and execution also reject integration. The previously empty 0.9 energy-pressure interface is now executed. Physical measurement outcomes and observation records remain the subsequent 0.13 calculation.')
    text('## 주소와 운반자의 공동 입력', '## Joint address and carrier inputs')
    text('주소 n=2…1000000의 정규화 상태 w_n과 부문 효과 e_s(n)는 0.9에서 그대로 받는다. s는 표현형 phi, 비표현형 잔존 D, 복귀 출처의 배경 응답 R이다. 잔존 Actual은 phi+D=31.8%, 복귀 응답까지 집계한 하류 장부는 100%다. 공통운반자의 rho는 같은 128칸 격자 위의 단위 대각합 양의 밀도행렬이다. 두 상태 공간의 연결은 아래 곱 상태 구성으로 명시한다.',
         'Normalized address weights w_n and sector effects e_s(n) on n=2…1000000 are inherited unchanged from 0.9. The sectors are phenotype phi, resident nonphenotype D and background response from returned provenance R. Resident Actual is phi+D=31.8%; the complete downstream ledger including returned response accounts for 100%. The carrier state rho is a positive unit-trace density matrix on the shared 128-site lattice. The two state spaces are joined by the following product-state construction.')
    eq(1,r'\sum_n w_n=1,\quad e_s(n)\geq0,\quad \sum_s e_s(n)=1,\qquad \sigma=\sum_n w_n|n\rangle\langle n|\otimes\rho.')
    text('地址 응답 g_s는 유한 주소 범위에서 양수인 구성 함수다. 기준 lambda_phi=0, lambda_D=0.25, lambda_R=0.1을 입력한다. 이 함수는 n과 부문의 에너지 응답을 연결하며 n을 물리 길이나 비트 수로 해석하지 않는다. 주소 상태를 바꾸면 같은 응답과 SI 계수로 다시 합산한다.',
         'The address response g_s is a positive constitutive function on the finite address domain. The reference adopts lambda_phi=0, lambda_D=0.25 and lambda_R=0.1. It connects address and sector energy response without identifying n with length or a bit count. Changed address states are summed with the same response and SI coefficients.')
    eq(2,r'g_s(n)=1+\lambda_s\frac{\log n}{\log N_{\mathrm{address}}},\qquad \mu_s=\sum_n w_ne_s(n)g_s(n).')
    eq(3,r'A_\varphi=I,\qquad A_D=\frac{K_c}{2},\qquad A_R=\frac{K_b}{2},\qquad L_s=\operatorname{Tr}(\rho A_s).')
    text('Kc는 기존 주기 격자의 양의 Laplacian이고, Kb는 공개한 비가환 국소 응답을 포함한 정규화 연산자다. 균질 혼합 상태 rho=I/N_carrier에서는 세 L_s가 모두 1이다. 기본 연산자와 비가환 시험 epsilon=8을 계승하며, 모든 양의 미소 부하를 유지한다.',
         'Kc is the inherited positive periodic-lattice Laplacian. Kb is the normalized operator containing the disclosed noncommuting local response. The uniform mixed carrier rho=I/N_carrier gives all three L_s=1. The release inherits the baseline operators and noncommuting test epsilon=8 and retains every positive load, including very small values.')
    text('## 한 번의 SI 보정과 주소별 에너지', '## One SI calibration and address energies')
    text('H0=67.4 km/s/Mpc와 G=6.6743×10⁻¹¹ m³/kg/s² 및 고정 c로 기준 에너지 밀도 ucrit를 계산한다. 대표 부피 V0=1 m³는 단위를 명시하는 계산 부피이며 우주 크기의 추정값이 아니다. 기준 주소 상태의 mu_s 별표와 균질 운반자에 목표 에너지 비율 t_s를 적용해 세 SI 응답 계수 eta_s를 구한다.',
         'The inherited H0=67.4 km/s/Mpc, G=6.6743×10⁻¹¹ m³/kg/s² and fixed c set the reference energy density ucrit. Representative V0=1 m³ specifies a calculation volume, not an estimated universe size. Target energy shares t_s on the frozen address moments mu_s star and uniform carrier determine three SI response coefficients eta_s.')
    eq(4,r'u_{\mathrm{crit}}=\frac{3H_0^2c^2}{8\pi G},\qquad \eta_s=\frac{u_{\mathrm{crit}}t_s}{\mu_s^*},\qquad [\eta_s]=\mathrm{J\,m^{-3}}.')
    table(['Sector','Arithmetic %','Energy target %','eta J m⁻³'],[[label,f'{100*r["common_arithmetic_ledger"][sector]:.6f}',f'{100*cfg["energy_map"]["reference_energy_fractions"][sector]:.6f}',f'{cal["eta_J_m3"][sector]:.10e}'] for label,sector in zip(['phi','D','R'],r['common_arithmetic_ledger'])])
    text('三 개의 eta는 검증된 에너지 목표에 대한 명시적 보정이다. 숫자를 보정으로 재현한 성과와, 보정 이후 상태 변화에 대한 내부 계산을 각각 장부에 기록한다. 별도의 대조에서는 목표를 5%·26.8%·68.2%로 바꾸어 보정하고 q0=−0.523을 얻는다. 이 대조는 목표를 바꾼 계산이며 기준 입력을 덮어쓰지 않는다.',
         'The three eta values are explicit calibrations to validated energy targets. Reproduction through calibration and subsequent calculated state responses are recorded separately. An alternate calculation explicitly calibrates to 5%, 26.8%, 68.2% and returns q0=−0.523. It is a changed-target calculation and does not overwrite the inherited reference.')
    eq(5,r'\epsilon_s(n,a,\rho)=V_0\eta_s a^{\nu_s}g_s(n)L_s,\qquad E_s=\sum_nw_ne_s(n)\epsilon_s(n,a,\rho).')
    eq(6,r'\widehat E(a)=V_0\sum_s\eta_s\mu_s a^{\nu_s}A_s,\qquad E=\operatorname{Tr}(\rho\widehat E)=\sum_s E_s.')
    text('epsilon_s는 주소 가중치와 부문 효과를 곱하기 전의 주소 응답 에너지이며 단위는 J다. 여러 주소와 48개 입자 슬롯은 같은 에너지 장부의 배분이다. 표현형 에너지를 0.8의 선택된 순열과 정규화된 세대 가중치로 배정하면 채널 에너지의 합은 E_phi와 같다. 세대 수를 다시 곱하지 않는다.',
         'epsilon_s is the address-response energy before multiplication by address weights and sector effects, in joules. Addresses and the 48 particle slots allocate one energy ledger. Applying the selected 0.8 permutation and normalized generation weights makes the channel-energy sum equal E_phi without multiplying the total by the generation count.')
    eq(7,r'V=V_0a^3,\qquad u_s=\frac{E_s}{V},\qquad P_s=-\left.\frac{\partial E_s}{\partial V}\right|_{w,e,g,\rho}=-\frac{\nu_s}{3}u_s.')
    text('기준 지수 nu_phi=nu_D=0, nu_R=3을 채택한다. 표현형과 D는 고정 공변 에너지를 가지므로 압력이 0이고, R 에너지는 부피에 비례하므로 P_R=−u_R이다. 같은 함수를 5점 부피 미분으로 검산했다. nu_R=0·1.5·3 대조의 상태방정식은 0·−0.5·−1로 계산된다. R의 산술 비율만으로 압력을 입력하지 않는다.',
         'The reference adopts nu_phi=nu_D=0 and nu_R=3. Fixed comoving phenotype and D energies give zero pressure, while R energy proportional to volume gives P_R=−u_R. An independent five-point volume derivative checks the same function. The controls nu_R=0, 1.5, 3 calculate equations of state 0, −0.5, −1. Arithmetic R share alone is not supplied as pressure.')
    text('## 같은 연산자의 상태 변화와 팽창', '## State evolution and expansion from the same operator')
    text('고정 부피에서 에너지 연산자를 기준 에너지 E_star=ucrit V0로 나누어 차원 없는 시계 좌표 tau의 갱신을 생성한다. 이 시계는 계승한 구성 시계이며 셔터의 고유시간 기원을 확정하는 0.12를 대신하지 않는다. 비가환 Kc와 Kb에서는 D와 R의 에너지가 실제로 교환되지만 교환 합은 0이다.',
         'At fixed volume, the energy operator divided by E_star=ucrit V0 generates updates in dimensionless clock coordinate tau. This inherits a constitutive clock and does not replace the later shutter-to-proper-time calculation. Noncommuting Kc and Kb transfer energy between D and R, with zero total internal exchange.')
    eq(8,r'\begin{aligned}U(\tau)&=e^{-i\tau\widehat E/E_*},\quad \rho(\tau)=U\rho_0U^\dagger,\\\frac{d\rho}{d\tau}&=-i[\widehat E/E_*,\rho],\quad \operatorname{Tr}\!\left(\widehat E\frac{d\rho}{d\tau}\right)=0.\end{aligned}')
    text('팽창 시험에서는 같은 생성자를 log a에 대해 적분하고 에너지 밀도에서 H를 계산한다. 압력은 앞 식의 같은 부피 미분이다. 고정 주소 구성 아래 상태 교환이 상쇄되므로 연속 방정식이 성립한다. 이 동질 평탄 배경과 국소 렌즈 조건은 계승한 물리 구현 범위다.',
         'The expansion test integrates the same generator against log a and calculates H from energy density. Pressure is the same volume derivative. At fixed address configuration, cancellation of state exchange gives the continuity relation. The homogeneous flat background and local lens condition retain the scope of the inherited implementation.')
    eq(9,r'\frac{H}{H_0}=\sqrt{\frac{u}{u_{\mathrm{crit}}}},\qquad q=\frac{u+3P}{2u},\qquad \frac{du}{d\log a}+3(u+P)=0.')
    eq(10,r'a_T=cH_0\sqrt{\frac{u_D}{8u_{\mathrm{crit}}}},\qquad \kappa_\Theta^2=\frac{16\pi G}{c^4}(u_D+u_R).')
    text('a_T는 0.5의 보정된 유한 국소 중력 응답에 전달한다. 렌즈 출력은 같은 패치에서 Phi=Psi를 채택한 조건부 결과다. 동일 부하에서 뒤틀림과 팽창을 함께 계산한 범위와, 뒤틀림이 팽창의 원인이라는 후속 설명을 구분한다. u=0에서는 H=0, q와 에너지 비율은 null로 기록한다.',
         'a_T enters the calibrated finite local gravity response inherited from 0.5. Lensing is conditional on Phi=Psi in the same patch. The executed joint calculation of twist and expansion from common load remains distinct from a subsequent causal claim that twist produces expansion. At u=0, H=0 and q and energy fractions are null.')
    table(['Quantity','Inherited reference','Alternate energy target'],[['u J m⁻³',f'{ref["total_density_J_m3"]:.10e}',f'{r["alternate_reference"]["total_density_J_m3"]:.10e}'],['P Pa',f'{ref["total_pressure_Pa"]:.10e}',f'{r["alternate_reference"]["total_pressure_Pa"]:.10e}'],['q',f'{ref["deceleration_q"]:.9f}',f'{r["alternate_reference"]["deceleration_q"]:.9f}'],['v km s⁻¹',f'{ref["local_readout"]["v_total_km_s"]:.9f}',f'{r["alternate_reference"]["local_readout"]["v_total_km_s"]:.9f}'],['Deflection arcsec',f'{ref["local_readout"]["finite_patch_lensing"]["alpha_patch_arcsec"]:.9f}',f'{r["alternate_reference"]["local_readout"]["finite_patch_lensing"]["alpha_patch_arcsec"]:.9f}']])
    text('## 地址 전환과 변환 일의 소유', '## Address transitions and conversion work ownership')
    text('0.9의 입장 순서는 아직 초 단위 우주 진화나 물리적 0/1 측정이 아니다. 이번에는 같은 대표 부피의 고정 운반자에서 기대 수송 S→phi에 필요한 에너지 교환을 계산한다. S 대기분에는 R과 같은 주소 응답을 주고, 각 입장량 b_n마다 목적 에너지와 출발 에너지의 차이를 변환 일 계정에 반대 부호로 기록한다. 이 계정은 계산계와 변환 일을 담당하는 환경 사이의 순교환량이며 네 번째 우주 구성비로 더하지 않는다. 환경의 미시 구현과 물리 측정 장치의 부하는 후속 전환 연구에서 다룬다.',
         'The 0.9 admission order is not yet cosmic evolution in seconds or a physical binary measurement. This stage calculates the required energy exchange for expected S-to-phi transport at fixed carrier state in one representative volume. Pending S receives the same address response as R. Each admitted b_n produces a destination-minus-source energy change and the opposite signed entry in a conversion-work account. This is net exchange between the calculation system and the environment owning conversion work; it is not added as a fourth cosmic fraction. Microscopic environment implementation and physical measurement-apparatus loads remain subsequent transition work.')
    eq(11,r'\Delta E_k=\sum_{n\in\mathrm{odd\ comp}}b_n(k)[\epsilon_\varphi(n)-\epsilon_R(n)],\qquad \Delta W_k=-\Delta E_k.')
    eq(12,r'E_{\varphi,k}+E_{D,k}+E_{S,k}+E_{R,k}+W_k=\mathrm{constant},\qquad \epsilon_S(n)=\epsilon_R(n).')
    work=r['frame_energy_transport'][-1]['conversion_work_account_J']
    text(f'기준 입장 완료까지 계산한 순교환 계정은 {work:.10e} J다. 이 교환을 누락하면 원래 계산계의 에너지 합은 일정하지 않아 검사가 실패한다. 복귀 경계에서 S를 R로 옮길 때는 주소별 에너지가 같으므로 교환량이 0이며 중복 에너지 배정도 없다. 이 계산은 필요한 교환량과 보존 장부를 닫으며, 변환을 구동하는 환경 법칙을 도출했다는 주장으로 확장하지 않는다.',
         f'The calculated net exchange account at admission completion is {work:.10e} J. Omitting this exchange makes the original system-energy sum nonconstant and fails the check. Relabeling S as R at recovery has zero exchange because their per-address energies agree and no energy is counted twice. This closes the required exchange quantity and conservation ledger; it does not derive the environmental law driving conversion.')
    text('## 보정 이후 주소 규칙의 응답', '## Address rule responses after calibration')
    text('입장 수 K와 위상 간격 xi를 바꿀 때 eta와 기존 물리 상수는 그대로 유지했다. 아래 산술 표현형과 q는 같은 에너지·압력 계산에서 나왔다. 이 수치는 변경한 입력에 조건부인 WRRA_M의 내부 산출값이며 기준 우주의 관측값 재현과 함께 보존한다.',
         'When admission count K and phase increment xi change, eta and physical constants remain fixed. The following arithmetic phenotype shares and q values come from the same energy-pressure calculation. They are conditional WRRA_M outputs under changed inputs and are preserved alongside reproduction of the reference universe.')
    table(['Case','Arithmetic phenotype %','Calculated q'],[[x['case'],f'{100*x["arithmetic_shares"]["phenotype"]:.9f}',f'{x["physical"]["deceleration_q"]:.9f}'] for x in r['frozen_coefficient_address_probes']])
    text('## 검증과 재현', '## Verification and reproduction')
    text('검사는 양의 에너지와 직접 주소 합산, 세 부문 SI 보정, 아홉 계승 사례, 별도 에너지 목표, 총 에너지 연산자의 양성, 독립 5점 압력 미분, 지수 대조, 대표 부피 변경, 주소·운반자 컷오프 분리, 주소 상태 변경, 0 부하와 미소 부하, 48채널 예산, 필터·전하 보존, 비가환 상태 갱신, 동질 연속 방정식, 네 필드 기대 수송, 변환 일과 복귀 경계 및 잘못된 입력 거부를 포함한다. 보존 검사를 통과한 뒤 저장 결과가 없는 새 복사본에서 같은 결과를 재실행한다.',
         'Checks cover positive energy and direct address sums, three-sector SI calibration, nine inherited cases, alternate energy targets, total-operator positivity, independent five-point pressure differentiation, exponent controls, representative-volume changes, separate address and carrier cutoffs, address-state changes, zero and tiny loads, 48-channel budgets, preserved filter charges, noncommuting updates, homogeneous continuity, four-field expected transport, conversion work and recovery, and invalid-input rejection. After conservation tests pass, a clean copy without saved outputs repeats the calculation.')
    s.append('```bash\npython -m pip install -r calculations/wrra_m_0_10/requirements.txt\npython calculations/wrra_m_0_10/run_release.py\n```')
    text('parameters.json는 전체 구성 입력이며 0.9 입력을 포함한다. results.json와 verification.json는 실행 결과와 반증 검사를 기록한다. 주소 에너지 표본, 상태·부피 결과, 프레임 교환 장부는 CSV로 함께 제공한다. run_release.py는 계산·검사와 한영 Markdown 원고를 생성한다. Word와 PDF는 동일 원고에서 만든 최종 판이며 원시 실행 결과와 구분한다.',
         'Parameters.json is the full configuration input and embeds the 0.9 input. Results.json and verification.json record calculation and falsification checks. CSV files contain address energy samples, state-volume results and frame exchange accounts. Run_release.py executes checks and generates both Markdown manuscripts. Word and PDF editions are final publications built from the same sources and are distinguished from raw execution outputs.')
    s.append('Input SHA256 '+r['input_hash_sha256'])
    text('## 후속 연결과 주장 범위', '## Subsequent connections and claim scope')
    text('현재 실행 순서는 0.10 에너지·압력, 0.11 첫 다섯 입력의 순차 보정, 0.12 셔터·고유시간·스펙트럼, 0.13 양자화·관측·기록, 0.14 컷오프·용량·불확실성, 0.15 응력·곡률·크기, 0.16 중성미자 질량·혼합·진동, 0.17 같은 기하의 전파, 1.0 통합 확정이다. 원래 여섯 단계 계획의 양자화·반복 전환·전환 부하·통합 검증 목표를 이 확장 순서에 보존한다.',
         'The current execution order is 0.10 energy-pressure mapping, 0.11 sequential calibration, 0.12 shutter/proper time/spectra, 0.13 quantization/observation/records, 0.14 cutoffs/capacity/uncertainty, 0.15 stress/curvature/size, 0.16 neutrino mass/mixing/oscillation, 0.17 propagation in the same geometry and 1.0 integration. It preserves the original six-stage goals of quantization, repeated transitions, transition loads and final integration.')
    text('이번 판의 확정 성과는 공개한 보정과 구성 규칙으로 계산된 에너지·압력 연결과 기존 물리 출력 재현이다. 주소 응답과 에너지 지수의 기원, 일반 주소·운반자 얽힘 동역학, 전체 4차원 공변 확장, 관측 장치의 미시 구현은 이번 완료 판정의 대상이 아니다. 미측정량을 산출할 때에는 모형과 보정을 고정한 뒤 사용한 입력과 반증조건을 함께 기록한다.',
         'The completed result is an executable energy-pressure connection and reproduction of inherited physical outputs under disclosed calibration and constitutive rules. Origins of address responses and energy exponents, general address-carrier entanglement dynamics, a full four-dimensional covariant extension and microscopic measurement apparatus are outside this completed stage. Unmeasured outputs are recorded after model and calibration fixation together with their inputs and falsifiers.')
    text('## 참고 자료와 공개 연결', '## References and public links')
    s.append('Choi Wonsik. WRRA-M 0.9-r1 reviewed 0.7 to 0.9 series. DOI 10.5281/zenodo.23091892. https://doi.org/10.5281/zenodo.23091892\n\nChoi Wonsik. WRRA-M 0.6-r2 Information Load and Twist Gravity and Expansion. DOI 10.5281/zenodo.23076547. https://doi.org/10.5281/zenodo.23076547\n\nWRRA-M repository. https://github.com/Wonsik-Choi-janefather/wrra-m-0.1\n\nMinimal Computation Cosmology 2.3.2. https://github.com/Wonsik-Choi-janefather/minimal-computing-cosmology-2.3.2\n\nCopyright 2026 Wonsik Choi. CC BY 4.0. https://creativecommons.org/licenses/by/4.0/')
    source='\n\n'.join(s)+'\n'
    # Korean manuscripts use Korean terms; prevent unintended CJK substitutions.
    source=source.replace('地址','주소').replace('三 개','세 개')
    (ROOT/f'source_{lang.lower()}.md').write_text(source)


if __name__=='__main__':build('KO');build('EN')
