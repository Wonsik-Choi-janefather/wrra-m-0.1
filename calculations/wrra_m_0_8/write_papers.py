"""Matched Korean and English manuscripts generated from release outputs."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'results/results.json').read_text())
v=json.loads((ROOT/'results/verification.json').read_text())
ref=next(c for c in r['cases'] if c['case_name']=='uniform_a1.0')

E=[
r'\mathcal C_{16}=\mathbf1_0\oplus\mathbf7_A\oplus\mathbf7_B\oplus\mathbf1_N,\quad \mathbf7\downarrow SU(3)=\mathbf3\oplus\overline{\mathbf3}\oplus\mathbf1.',
r'K_c=2I-T-T^\dagger,\quad K_i^{\mathrm{read}}=K_c+\mu_i I.',
r'\mu_i=\mu_0+s_i\delta_{L,R},\quad \delta_L=\kappa(Q_\nu-Q_e),\quad\delta_R=\kappa(Y_0-Y_N).',
r'I_i(\rho)=\frac1M\sum_{j=1}^{M}\mathrm{Tr}\!\left[\rho\left((K_c+\mu_i I-w_jI)^2+\gamma^2I\right)^{-1}\right].',
r'u_i=\sqrt{I_i/I_{\mathrm{ref}}},\quad I_{\mathrm{ref}}=I_{\mu=0}(\rho),\quad c(i,j)=-(u_i-u_j)^2.',
r'\Delta_L=2(u_{3_A}-u_{3_B})(u_{1_A}-u_{1_B}),\quad\Delta_R=2(u_{\bar3_A}-u_{\bar3_B})(u_{1_N}-u_{1_0}).',
r'C=(C_{DX},\ C_{DX}-\Delta_L,\ C_{DX}-\Delta_R,\ C_{DX}-\Delta_L-\Delta_R).',
r'p_f(\tau)=\frac{p_f(0)e^{\eta C_f\tau}}{\sum_g p_g(0)e^{\eta C_g\tau}},\quad\dot p_f=\eta p_f(C_f-\overline C).',
r'\tau\geq\frac{\log((1-p_*(0))/(p_*(0)\varepsilon))}{\eta\Delta_{\min}}\quad\Longrightarrow\quad 1-p_*(\tau)\leq\varepsilon.',
r'P_{DX}^\dagger P_{DX}=I_{16},\quad\rho_{\mathrm{ch}}^{\prime}=P_{DX}\rho_{\mathrm{ch}}P_{DX}^\dagger.',
r'3b_q+b_\ell=0,\quad b_\ell=-1,\quad b_q=\frac13;\qquad \overline b_q=-\frac13,\quad\overline b_\ell=1.',
r'Y=\alpha T_{3R}+\beta(B-L),\quad -\alpha/2+\beta=0,\quad\alpha/2+\beta=1\quad\Longrightarrow\quad(\alpha,\beta)=(1,1/2).',
r'Q=T_{3L}+Y.',
r'\widetilde A_s=I_{16}\otimes A_s^{(0.7)},\quad\mathrm{Tr}(\rho^{\prime}\widetilde A_s)=\mathrm{Tr}(\rho\widetilde A_s).',
r'\mathcal C_{48}=\mathbb C^3\otimes\mathcal C_{16},\quad G_{48}=I_3\otimes G_{16},\quad \mathrm{Tr}\rho_{\mathrm{fam}}=1.'
]


def eq(n):return '\n$$\n'+E[n-1]+rf' \tag{{{n}}}'+'\n$$\n'
def table(headers,rows):return '\n| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,row))+' |\n' for row in rows)+'\n'
case_labels_en=['Uniform a 0.5','Uniform a 1','Uniform a 2','Low mode','High mode','Zero mode','Coherent packet','Uniform noncommuting','Packet noncommuting']
case_labels_ko=['균등 a 0.5','균등 a 1','균등 a 2','낮은 모드','높은 모드','영 모드','중첩 상태','균등 비가환','중첩 비가환']
checks_en=['Inherited exact checks 0.1 to 0.4','Color inventory and neutral extension','Independent periodic spectrum','Direct complex resolvent','Zero calibration and homogeneous tie','Four filter costs and gap identities','Selection in nine cases','Positive full rank transport','Bijective color preserving filter','One hypercharge and exact anomalies','Three calibrated generations','Weak representation algebra','Same nine physical ledgers','Nonuniform channel energy accounting','Entangled channel load accounting','Shared grid input','Contrast sensitivity','Orientation and convention controls','Joint background and basis covariance','Flow equation and zero support','Invalid calibrations and records','Hash and explicit recalibration','Tiny positive winner support']
checks_ko=['0.1부터 0.4의 기존 정확 검산','색 배치와 중성 채널 확장','별도 주기 스펙트럼 응답','직접 복소 resolvent 응답','영 보정과 균질 동률','네 필터 비용과 간격 항등식','대표 상태 9개의 선택','양의 전체 랭크 수송','색 작용을 보존하는 일대일 필터','단일 초전하와 정확 이상 합','보정된 세 세대의 배치','약한 표현의 교환 관계','기존 물리 장부 9개 대조','비균등 채널의 에너지 장부','얽힌 채널의 부하 장부','공통 격자 입력의 전달','응답 대비의 민감도','방향 보정과 명명 규약 대조','배경과 기저의 동시 변환','선택 흐름과 영 초기 지지','잘못된 보정과 기록의 차단','해시와 명시적 재보정','작은 양의 우승 지지의 수렴']
assert len(v['checks'])==len(checks_en)==len(checks_ko)==23


def build(lang):
    ko=lang=='KO';title='WRRA M 0 8 공통 Actual 장부에서 보정된 입자 필터 선택' if ko else 'WRRA M 0 8 Calibrated Particle Filter Selection in the Shared Actual Ledger'
    subtitle='공통운반자 응답과 실제 배치 및 전하 계산' if ko else 'Common carrier responses with executed placement and charge calculation'
    text='# '+title+'\n\n'+subtitle+'\n\n'+('최원식 Wonsik Choi' if ko else 'Wonsik Choi')+'\n\nWRRA-M 0.8-r1 | 2026-10-02\n\nIndependent Researcher Seoul Republic of Korea\n\nORCID 0009-0001-4263-9772 | janefather@gmail.com\n'
    def section(k,e):
        nonlocal text;text+='\n## '+(k if ko else e)+'\n\n'
    def para(k,e):
        nonlocal text;text+=(k if ko else e)+'\n\n'
    section('판정 순서와 완료 결과','Evaluation order and completed result')
    para('검증 입력은 WRRA Core 1.0과 MCC 2.3.2, 0.1~0.4의 표현·전하·선택 계산, 0.7의 공통 장부다. 알려진 입자 배정과 세 세대 수는 보정 자료로 채택한다. 응답 오프셋과 출처 방향표는 별도로 공개한 구성 선택이다.',
         'Verification inputs are WRRA Core 1.0, MCC 2.3.2, the representation, charge and selection calculations of 0.1 to 0.4, and the shared 0.7 ledger. Known particle assignments and three generations are adopted calibration material. Response offsets and the origin orientation table are disclosed constitutive choices.')
    para('WRRA 고유 변환은 같은 운반자 상태에서 응답을 계산하고, 하나의 양의 거리 규칙으로 네 필터의 점수를 만든 뒤, 실제 선택된 순열에서 배치와 전하를 산출하는 것이다. 산출값은 F_DX 선택, 16개 기본 채널의 전하, 세 세대로 확장한 45개 표준모형 손지기 성분과 3개 조건부 중성 슬롯이다. 같은 입력은 기존 에너지·압력·중력·팽창 장부에도 들어간다.',
         'The WRRA-specific transformation computes responses from the same carrier state, evaluates all four filters with one positive-distance rule, and generates placement and charges from the selected permutation. Outputs are selection of F_DX, the sixteen-channel charge table, and replication into 45 Standard-Model chiral components plus three conditional neutral slots. The same input also enters the inherited energy, pressure, gravity and expansion ledger.')
    para('반증조건은 고정 보정에서의 동률 또는 기준 배정 실패, 수송 랭크·양성 상실, 전하·이상 합·에너지 장부 불일치, 미공개 입력 변경이다. 검증 23개 묶음을 통과했다. 완료 판정은 공개된 네 필터 계열에서 보정된 우리 우주 배치를 실제 선택했다는 뜻이다. 보정은 정당한 모형 구성 방법이며 독립예측을 이 판의 완료 조건으로 두지 않는다.',
         'Failure conditions are a tie or incompatible assignment under fixed calibration, loss of transport rank or positivity, disagreement in charges, anomalies or energy accounting, and undisclosed input changes. Twenty-three check groups pass. Completion means executed calibrated selection of the adopted our-universe assignment within the declared four-filter family. Calibration is legitimate model construction; independent prediction is not a completion requirement.')
    section('기존 동률과 이번 판의 입력 장부','The inherited tie and this release input ledger')
    para('0.1의 두 복소화된 일곱 부문과 불변 채널은 15개 색 성분을 준다. 0.2~0.4는 운반되는 중성 채널 1_N을 추가했다. 각 성분을 독립 복소 왼손 Weyl 장으로 읽는 것은 물리 가정이다. 1_N을 nu_R의 켤레 채널로 해석하는 것은 이번 분기의 구성 가정이며, 이 계산으로 그 입자의 실재·질량·점유를 관측한 것은 아니다.',
         'Two complexified seven sectors and an invariant channel from 0.1 give fifteen color components. Versions 0.2 to 0.4 add the transported neutral channel 1_N. Independent complex left-handed Weyl fields are a physical assumption. Interpreting 1_N as the conjugate right-handed neutrino is a constitutive assumption of this branch; this calculation does not measure its particle existence, mass or occupation.')
    text+=eq(1)
    para('0.5의 가장 단순한 균질 운반자는 모든 출처에 같은 스칼라 응답을 주었다. 랭크 16이어도 선택 간격은 양쪽 모두 0이었다. 0.8은 공통 주기 격자 Kc를 유지하면서 읽기 연산자에 출처별 스칼라 오프셋을 넣는다. 이 항은 같은 높은 차수의 수송 구조 위에서 응답을 구분하는 보정이다.',
         'The simplest homogeneous carrier in 0.5 gave the same scalar response to every origin. Its transport rank was sixteen, yet both selection gaps were zero. Version 0.8 retains the common periodic lattice Kc and adds origin-specific scalar offsets to the readout operator. These calibrate distinguishable responses while retaining the same highest-order transport matrix.')
    text+=eq(2)
    para('보정은 mu0=1, kappa=0.25, Qnu=0, Qe=-1, YN=0, Y0=1을 사용한다. 양쪽 대비는 0.25이며 오프셋은 0.75 또는 1.25다. 방향표의 부호는 기존 0.2의 입자 출처 배정을 유지하는 보정 입력이다. F_DX라는 결과 이름이나 양의 간격 수치를 직접 점수 입력으로 쓰지 않는다. 대신 알려진 배정에 맞춘 방향을 입력했으므로, 그 방향의 미시적 기원을 새로 도출했다는 주장도 하지 않는다.',
         'Calibration uses mu0=1, kappa=0.25, Qnu=0, Qe=-1, YN=0 and Y0=1. Both contrasts are 0.25 and offsets are 0.75 or 1.25. Signs in the orientation table are calibration inputs preserving the 0.2 particle-origin assignment. Neither the output name F_DX nor a positive gap is inserted as a score. The calibrated orientation does use known assignments, so its microscopic origin is not newly derived.')
    text+=eq(3)
    para('오프셋은 차원 없는 보조 읽기 보정이다. 이를 새 입자 질량이나 별도 에너지 성분으로 장부에 더하지 않으며, 기존 상태 진화의 Hamiltonian을 대체하지 않는다. 색 삼중항 안에서는 동일한 응답이므로 색 작용을 보존한다. 약한 성분을 구분하는 고정 배경이므로 깨지지 않은 SU(2) 대칭의 Hamiltonian이라고 해석하지 않는다. 배경과 기저를 함께 변환하는 응답 대조를 검증했고, Higgs나 대칭 깨짐의 동역학은 이 판에서 새로 계산하지 않는다.',
         'Offsets are dimensionless auxiliary readout calibration. They add neither a new particle mass nor a separate energy sector, and do not replace the inherited state-evolution Hamiltonian. Equal responses within each color triplet preserve the color action. Component-dependent readout is a fixed weak-basis background, not an unbroken SU(2)-invariant Hamiltonian. Joint background and basis covariance is checked; Higgs or symmetry-breaking dynamics are not newly calculated here.')
    section('같은 운반자에서 계산한 응답과 선택','Responses and selection computed from one carrier')
    para('격자 크기 N=128과 내부 상태 rho는 0.7과 같다. 탐침은 기존 장부의 제곱 주파수 0.1, 0.5, 1, 2, 3.5와 감쇠 gamma=0.2를 사용한다. 아래 응답은 같은 상태의 양의 resolvent 강도를 평균한다. Iref는 같은 상태에서 오프셋 0으로 계산한 공통 정규화다. 입자별로 따로 정규화해서 구분을 지우지 않는다.',
         'The grid N=128 and internal state rho are shared with 0.7. Probes use inherited squared frequencies 0.1, 0.5, 1, 2 and 3.5 with damping gamma=0.2. The response averages positive resolvent intensities in that same state. Iref is the common normalization computed at zero offset in that state; individual channel normalization does not erase their differences.')
    text+=eq(4)+eq(5)
    rows=[[o,cfgsign, f'{ref["response"]["dimensionless_shifts"][o]:.2f}',f'{ref["response"]["normalized_signatures"][o]:.9f}'] for o,cfgsign in r['input_ledger']['filter_calibration']['response_tags'].items()]
    text+=table(['출처','부호','오프셋','응답 u'] if ko else ['Origin','Sign','Offset','Response u'],rows)
    para('직접 계산한 거리 차이는 0.4의 정렬 항등식과 일치한다. F_DX, F_XX, F_DD, F_XD 순서의 점수를 0.3 코드로 계산한다. 선택은 최대점수의 유일성, 양의 선택속도, 최대 후보의 초기 지지를 확인한 뒤 이루어진다.',
         'Direct distance differences agree with the alignment identities of 0.4. Scores are evaluated by the 0.3 code in the order F_DX, F_XX, F_DD and F_XD. Adoption checks a unique maximum, positive selection rate and nonzero initial support for that maximum.')
    text+=eq(6)+eq(7)
    para(f'현재 균등 기준에서 두 간격은 {ref["selection"]["Delta_L"]:.11f}이다. 점수는 0, -0.04669193039, -0.04669193039, -0.09338386078이다. 최대점수는 F_DX 하나다. 이는 0.4의 구성 증인 간격 8을 그대로 복사한 결과가 아니라 이번 운반자 응답에서 계산한 값이다.',
         f'At the uniform reference both gaps are {ref["selection"]["Delta_L"]:.11f}. Scores are 0, -0.04669193039, -0.04669193039 and -0.09338386078. F_DX is the unique maximum. These are computed carrier responses rather than a copied gap-eight witness from 0.4.')
    text+=table(['상태','간격 L','간격 R','선택'] if ko else ['State','Gap L','Gap R','Selected'],[[label,f'{c["selection"]["Delta_L"]:.9f}',f'{c["selection"]["Delta_R"]:.9f}',c['selection']['selected_filter']] for label,c in zip(case_labels_ko if ko else case_labels_en,r['cases'])])
    para('표의 상태들은 계산 구조를 검사하는 고정 시험 입력이다. 각 상태를 현재 우주의 새 관측값으로 부르지 않는다. N=32, 64, 128, 256에서도 선택과 랭크를 확인했고, N 입력은 정보부하와 필터 응답에 함께 연결된다. 실제 숫자는 결과 JSON과 CSV에서 재현된다.',
         'Table states are fixed structural test inputs, not new observations of the present universe. Selection and rank are also checked at N=32, 64, 128 and 256. The same N input controls both information loads and filter responses. Numerical values are reproduced in the JSON and CSV outputs.')
    section('실행한 선택 흐름과 대조 조건','Executed selection flow and controls')
    text+=eq(8)+eq(9)
    para('초기 네 가중치는 각각 1/4, eta=1, 목표 잔여는 10^-8이다. 균등 기준의 충분한 구성 시간은 약 418.04425027이고, 마지막 F_DX 가중치는 0.999999993333이다. 잔여는 약 6.666667×10^-9다. 독립적으로 적분한 선택 미분방정식과 닫힌 해의 최대 차이는 @ODE@였다.',
         'Initial weights are one quarter each, eta=1 and the residual target is 10^-8. The sufficient construction time at the reference is about 418.04425027, with final F_DX weight 0.999999993333 and residual about 6.666667 times 10^-9. Independent integration of the selection differential equation differs from the closed form by at most @ODE@.')
    para('이 가중치는 모형을 구성하는 최적화 흐름의 후보 가중치다. 개별 입자의 Born 발생확률, 물리 시간 또는 관측 기록으로 해석하지 않는다. 유한 시간의 가중치가 정확히 1이 되었다고 주장하지 않으며, 이번 배치 채택은 확인된 유일 최대점수의 선택 규칙이다.',
         'These are candidate weights in a model-construction optimizer. They are not particle Born probabilities, physical time or observation records. Finite-time weight is not asserted to equal exactly one; adopted placement follows the checked unique-maximum selection rule.')
    para('kappa=0이면 네 후보가 동률이다. kappa=0.1, 0.25, 0.5의 고정 기준에서는 F_DX가 선택된다. 왼쪽 또는 오른쪽 싱글릿 방향을 바꾸면 각각 F_XX 또는 F_DD, 둘 다 바꾸면 F_XD가 선택된다. 모든 부호를 함께 뒤집는 명명 규약 변경에서는 간격과 F_DX 선택이 유지된다. 출처를 고정하지 않고 다시 이름 붙이면 일부 배정은 같은 입자 내용을 나타낼 수 있다. 따라서 이 결과를 네 후보가 모두 서로 다른 관측 우주라는 증명으로 사용하지 않는다.',
         'At kappa=0 all four candidates tie. Fixed reference calibrations kappa=0.1, 0.25 and 0.5 select F_DX. Reversing left or right singlet orientation selects F_XX or F_DD; reversing both selects F_XD. A global sign-convention reversal preserves gaps and F_DX. Some assignments can represent the same particle content after origin relabeling. This is therefore selection in a fixed calibrated origin convention, not proof that every candidate defines a different observed universe.')
    section('선택된 순열에서 산출한 입자 배치와 전하','Placement and charges generated from the selected permutation')
    para('선택된 필터를 실제 16×16 순열 행렬로 만든다. 삼중항 A와 B는 Q_L의 위·아래 성분이 되고, 싱글릿 A와 B는 L_L의 위·아래 성분이 된다. 반삼중항 A는 중성 채널 N과, 반삼중항 B는 불변 채널 0과 짝을 이룬다. 입력 채널은 추가로 버리지 않으며 색 작용의 intertwining을 행렬로 대조한다.',
         'The selected filter is implemented as a sixteen-by-sixteen permutation. Triplets A and B form upper and lower Q_L components; singlets A and B form upper and lower L_L components. Antitriplet A pairs with neutral N and antitriplet B with invariant 0. No input channel is discarded. Matrix checks verify color intertwining.')
    text+=eq(10)
    para('색 traceless 조건과 렙톤의 B-L 정규화에서 쿼크의 B-L 값을 산출한다. 선택된 배치에서 Y(1_N)=0과 Y(1_0)=1을 동시에 만족시키는 하나의 초전하 연산자를 유리수로 풀고, 모든 채널에 적용한다. 아래 c는 왼손 표기의 전하 켤레 장을 뜻하므로 u_c와 d_c의 전하 부호는 물리적인 오른손 쿼크와 반대다.',
         'Color tracelessness and lepton B-L normalization generate the quark B-L values. On the selected placement, rational arithmetic solves one hypercharge operator satisfying Y(1_N)=0 and Y(1_0)=1, then applies it to every channel. Superscript c denotes a charge-conjugate left-handed field; u_c and d_c therefore have charges opposite to physical right-handed quarks.')
    text+=eq(11)+eq(12)+eq(13)
    origins={'Q_L':'3_A and 3_B','L_L':'1_A and 1_B','u_c':'anti3_A','d_c':'anti3_B','nu_c':'1_N','e_c':'1_0'}
    text+=table(['부문','성분 수','Y','전하 Q','출처'] if ko else ['Group','Count','Y','Charge Q','Origin'],[[field,data['multiplicity'],data['Y'],', '.join(data['Q']),origins[field]] for field,data in ref['placement_and_charge']['field_groups'].items()])
    para('계산된 SU(3)^3, SU(3)^2 U(1), SU(2)L^2 U(1), U(1)^3 및 중력과 U(1)의 혼합 이상 합은 모두 정확히 0이다. SU(2)의 왼쪽·오른쪽 이중항은 각각 4개로 짝수다. 여기서 중력 혼합 이상은 전하 표현의 정합성 검사이며 시공간 중력 계산과 별개다. 약한 생성자의 교환 관계와 B-L 가환성도 검사했다.',
         'Calculated SU(3)^3, SU(3)^2 U(1), SU(2)L^2 U(1), U(1)^3 and mixed gravitational-U(1) anomaly sums vanish exactly. Left and right SU(2) sectors each contain four doublets. The gravitational anomaly is a representation-consistency check, separate from spacetime gravity calculation. Weak-generator commutators and B-L compatibility also pass.')
    section('공통 Actual 장부와 세 세대의 연결','Connection to the shared Actual ledger and three generations')
    para('필터는 채널 배치를 바꾸는 순열이며 0.7 에너지 연산자는 채널에 공통으로 작용한다. 따라서 이 재배치에서 표현형·모이는 비표현형·배경 비표현형의 에너지 합은 변하지 않는다. 비균등 채널 상태와 얽힌 채널 시험에서도 같은 부하를 확인했다. 실제 양자화 사건의 에너지 이동을 수행한 결과와는 구분한다.',
         'The filter permutes channel placement while 0.7 energy operators act commonly on channels. Phenotype, clustering-hidden and background-hidden energy budgets are therefore preserved by this reorganization. Nonuniform and entangled channel tests preserve the same loads. This check is distinct from energy transfer in a physical quantization event.')
    text+=eq(14)
    para('대표 상태 9개의 0.7 장부는 원본과 동일하다. 현재 기준 표현형 4.93%, 비표현형 95.07%, q=-0.52855, 시험 회전속도 207.510905 km/s와 조건부 렌즈 편향 0.535586511각초를 유지한다. 새 선택 계산은 이 수치를 바꾸기 위해 보정값을 재조정하지 않는다. 5% 비율, 16개 채널의 상태 가중치, 네 필터의 최적화 가중치는 서로 다른 장부다.',
         'All nine physical ledgers match the 0.7 originals. The reference retains phenotype 4.93%, hidden share 95.07%, q=-0.52855, test rotation 207.510905 km/s and conditional lens deflection 0.535586511 arcsec. The selection calculation does not refit these outputs. The five-percent allocation, sixteen-channel state weights and four-filter optimizer weights are distinct accounts.')
    text+=eq(15)
    para('세 세대는 알려진 입자 정보에 맞춰 구성 수 3으로 채택한다. 동일한 채널 규칙을 반복해 u,d / c,s / t,b와 e,mu,tau 및 세 활성 중성미자 계열의 전하를 계산한다. 출력 particle_inventory.csv는 48개 성분을 모두 기록한다. 45개는 표준모형 손지기 성분이며 나머지 3개 N1_c,N2_c,N3_c는 조건부 중성 확장 슬롯이다. 수송 랭크 48은 실제 행렬에서 계산한다. 세대 상태를 정규화하므로 원래 에너지를 3배로 더하지 않는다.',
         'Three generations are adopted from known particle information as the configured replication count. The same channel rule generates charges for u,d / c,s / t,b, e,mu,tau and the three active neutrino families. Particle_inventory.csv records all 48 components: 45 Standard-Model chiral components and three conditional neutral extension slots N1_c,N2_c,N3_c. Transport rank 48 is computed from the actual matrix. Normalized family state avoids multiplying the original energy budget by three.')
    para('이 판의 세대 수는 보정 입력이고 세대 복제는 실행한 변환이다. 질량·혼합·Yukawa·상호작용의 동역학을 이 출력으로 새로 도출했다고 주장하지 않는다. 0.9는 이 배치에 상류 입력과 공통 산술 장부를 연결한다. 0.10의 물리 에너지·압력 사상과 0.12의 시간·스펙트럼을 거쳐, 0.13에서 양자화 결과·확률·관측 뒤 상태·기록을 실행한다.',
         'Family count is calibration input and family replication is an executed transformation. Masses, mixing, Yukawa structure and interaction dynamics are not newly derived by this inventory. Version 0.9 connects upstream inputs and common arithmetic accounting to this placement. Physical energy and pressure mapping in 0.10 and time and spectra in 0.12 precede physical quantization outcomes, probabilities, post-observation states and records in 0.13.')
    section('검증과 재현 방법','Verification and reproduction')
    text+=table(['번호','검사','결과'] if ko else ['No','Check','Result'],[[i+1,name,'통과' if ko else 'Pass'] for i,name in enumerate(checks_ko if ko else checks_en)])
    para('검증은 기존 정확 코드, 주기 스펙트럼의 별도 계산, 직접 복소 행렬 역행렬, 선택 미분방정식 적분, 표현·이상 합, 격자 변경, 반대 방향 보정, 초기 지지 0, 잘못된 입력 12개를 포함한다. 허용 상태에서 양의 응답·전체 랭크·선택 간격이 나오지 않거나, 같은 배치의 전하와 장부가 맞지 않으면 해당 구성은 수정해야 한다.',
         'Checks include inherited exact code, independent periodic spectra, direct complex matrix inverses, selection-ODE integration, representations and anomalies, grid changes, reversed calibration, zero initial support and twelve invalid inputs. Failure to retain positive response, full rank, selection gaps or consistent placement charges and accounting requires revision of that configuration.')
    para('압축파일의 루트에서 python calculations/wrra_m_0_8/run_release.py를 실행한다. parameters.json은 이번 판의 유일한 구성 입력이며 0.7 장부를 내부에 포함한다. 결과에 두 입력 해시를 기록한다. 전체 0.8 입력의 정규 SHA256은 '+r['input_hash_sha256']+'이다. 저장 결과를 지운 깨끗한 복사본에서 다시 실행하는 재현 검사와 파일 SHA256 목록을 제공한다.',
         'From the archive root run python calculations/wrra_m_0_8/run_release.py. Parameters.json is the sole configuration input and embeds the 0.7 ledger. Outputs record both input hashes. Canonical SHA256 of the full 0.8 input is '+r['input_hash_sha256']+'. A clean-copy reproduction check removes captured numerical outputs before execution, and the archive includes a file SHA256 manifest.')
    para('계산에는 numpy와 scipy가 필요하다. 원고 생성은 write_papers.py, Word 생성은 pandoc와 python-docx를 사용하는 build_reports.py가 담당한다. PDF는 LibreOffice로 렌더링하며, 문서 대조는 pypdf를 추가로 사용한다. 임의 상태 검증은 seed 808이다. 코드는 구성 가정, 보정 입력, 내부 산출값과 후속 작업을 결과에 구분한다. r1은 초기 우승 지지 10^-320에서도 로그 합산으로 수렴시킨다. 수정 계열을 GitHub와 Zenodo에 공개한다.',
         'Computation requires numpy and scipy. Write_papers.py generates manuscripts; build_reports.py uses pandoc and python-docx for Word. PDF is rendered with LibreOffice, and document checks additionally use pypdf. Random-state tests use seed 808. Results separate constitutive choices, calibrations, internal outputs and subsequent work. Revision r1 converges with initial winner support 10^-320 using log-space arithmetic. The reviewed series is published on GitHub and Zenodo.')
    section('참고 자료','References')
    text+='Choi Wonsik. WRRA-M 0.1 to 0.7. GitHub research repository. https://github.com/Wonsik-Choi-janefather/wrra-m-0.1\n\n'
    text+='Choi Wonsik. WRRA-M 0.6-r2 frozen archive. https://doi.org/10.5281/zenodo.23076547\n\n'
    text+='Choi Wonsik. Minimal Computation Cosmology 2.3.2. Chapter 11 The Common Carrier and Fifteen Channels. '+('동일 공통운반자의 제약을 기준으로 채택한다.' if ko else 'Adopted constraints on a common carrier.')+' https://github.com/Wonsik-Choi-janefather/minimal-computing-cosmology-2.3.2\n\n'
    text+='Particle Data Group. Grand Unified Theories. 2025 update, sections 92.1 and 92.2.1. '+('PDG의 초전하를 절반으로 환산한 Q=T3+Y 규약을 쓴다. 알려진 표준모형 표현과 Pati Salam 관계는 외부 검증 입력이다.' if ko else 'The convention here rescales PDG hypercharge by one half, giving Q=T3+Y. Standard-Model representations and the Pati Salam charge relation are external verification inputs.')+' https://pdg.lbl.gov/2025/reviews/rpp2025-rev-guts.pdf\n\n'
    text+='Copyright 2026 Wonsik Choi. CC BY 4.0. https://creativecommons.org/licenses/by/4.0/\n'
    ode=next(x['ODE_maximum_error'] for x in v['checks'] if x['name']=='flow_equation_and_zero_support_boundary')
    text=text.replace('@ODE@',f'{ode:.3e}')
    ode=next(x['ODE_maximum_error'] for x in v['checks'] if x['name']=='flow_equation_and_zero_support_boundary')
    text=text.replace('@ODE@',f'{ode:.3e}')
    (ROOT/f'source_{lang.lower()}.md').write_text(text)


if __name__=='__main__':build('KO');build('EN')
