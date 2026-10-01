"""Generate matched manuscripts from executed 0.9 accounting tables."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def equation(number, body):
    return '\n\n$$\n'+body+r' \tag{'+str(number)+'}\n$$\n\n'


def table(headers, rows):
    return '\n\n| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,row))+' |\n' for row in rows)+'\n'


def build(lang):
    ko = lang == 'KO'; r = json.loads((ROOT/'results/results.json').read_text()); c = r['input_ledger']; u = c['upstream']
    v = json.loads((ROOT/'results/verification.json').read_text()); sections=[]
    def text(korean, english): sections.append(korean if ko else english)
    def eq(n, body): sections.append(equation(n, body))
    text('# WRRA M 0 9 세 부문의 공통 장부와 상류 입력 연결', '# WRRA M 0 9 Common Sector Accounting and the Upstream Input Contract')
    text('같은 분모의 산술 보정과 입자 채널 연결', 'Arithmetic calibration on one denominator and connection to particle channels')
    sections.append('최원식 Wonsik Choi\n\nWRRA-M 0.9 | 2026-10-01\n\nIndependent Researcher Seoul Republic of Korea\n\nORCID 0009-0001-4263-9772 | janefather@gmail.com')
    text('## 판정 범위와 완료 결과', '## Evaluation scope and completed calculation')
    text('0.9는 상류의 표현형·비표현형 잔존·복귀를 같은 주소 가중치와 분모로 계산하고, 채택한 0.8 필터의 입자 채널에 연결한다. 검증 입력은 WRRA Core 1.0, MCC 2.3.2, 동결한 0.8 입력과 상류 두 단계 필터 및 제타 영점 갱신 계산이다. 알려진 입자 배정과 구성비를 보정에 사용하는 것을 모형 구성 방법으로 인정한다.',
         'Version 0.9 computes phenotype, resident nonphenotype and return using one address measure, then connects the expressed budget to the selected 0.8 particle channels. Verification inputs are WRRA Core 1.0, MCC 2.3.2, frozen 0.8 inputs, and the upstream two-stage filter and zeta-zero update calculations. Known particle assignments and composition targets are legitimate calibration inputs for this constructed model.')
    text('WRRA 고유 변환은 주소별 상태와 스펙트럼을 받아 고갈되는 저장분의 누적 입장을 계산하고, 복귀 경계에서 세 부문 장부를 닫은 뒤, 정규화한 조건부 채널 배분과 실제 선택 순열을 적용하는 것이다. 산출값은 5%·26.8%·68.2%, 잔존 Actual 31.8%, 전체 집계 100%, 48개 채널 장부다. 26개 검증 묶음을 통과했으며 기존 0.8의 9개 결과와 전하표가 그대로 재현된다.',
         'The WRRA-specific transformation takes the address state and spectrum, accumulates admission from a depleted reservoir, closes the three-sector ledger at the recovery boundary, and applies normalized conditional channel routing followed by the computed selection permutation. Outputs are 5%, 26.8% and 68.2%, resident Actual 31.8%, total accounted weight 100%, and a 48-channel ledger. Twenty-six verification groups pass, and all nine 0.8 results and their charge assignments are reproduced unchanged.')
    text('반증조건은 고정 입력에서의 보정 재현 실패, 음수 또는 불완전한 부문 효과, 전환 장부 불일치, 채널·세대 중복 합산, 전하 불일치와 미공개 보정 변경이다. 산술 부하를 물리 에너지·압력으로 사상하는 작업은 0.10에, 개별 0/1 측정 결과와 기록은 0.13에 배정한다. 이번 판의 입장 가중치는 결정론적으로 계산한 기대 수송량이며 물리적 Born 측정확률을 새로 구현한 결과가 아니다.',
         'Falsification conditions are failure of frozen calibrated reproduction, negative or incomplete sector effects, inconsistent transition accounting, duplicated channel or generation weight, charge disagreement, or undisclosed calibration changes. Mapping arithmetic load to physical energy and pressure belongs to 0.10; individual 0/1 measurement outcomes and physical records belong to 0.13. Admission weights here are deterministic expected transport, with no newly implemented physical Born measurement rule.')
    text('## 같은 분모의 주소 상태와 보정', '## Address state and calibration on a common denominator')
    text('주소 n은 2부터 N_address=1,000,000까지다. 같은 n^-alpha 가중치를 모든 부문에 사용한다. 소수는 초기 SOURCE 저장분, 짝수 합성수는 비표현형 잔존 D, 홀수 합성수는 입장 가능한 표현형 지지로 배정한다. 이 소수 분류의 물리적 해석과 분기 기원은 구성 가정이며 상류 과제로 남는다.',
         'Addresses run from 2 through N_address=1,000,000. Every sector uses the same n^-alpha measure. Primes initially occupy the SOURCE reservoir, even composites form resident nonphenotype D, and odd composites support phenotype admission. The physical interpretation and origin of this arithmetic classification remain constitutive assumptions and upstream questions.')
    eq(1, r'w_n=\frac{n^{-\alpha}}{\sum_{m=2}^{N_{\mathrm{address}}}m^{-\alpha}},\qquad \sum_n w_n=1.')
    text(f"입력 alpha={u['state']['alpha']:.16f}는 D=0.268을 맞춘 산술 보정값이다. 아래의 h={u['update']['sigmoid_threshold_h']:.15f}는 표현형 0.05를 맞춘 보정값이다. 합이 1이므로 복귀 0.682는 나머지로 산출된다. 일정 입장 비교판의 beta와 제타 갱신판의 beta_eff는 역할이 다르다. 기본 갱신판에서 beta_eff={r['derived_effective_beta']:.16f}는 계산된 표현형을 입장 가능한 홀수 합성수 가중치로 나눈 산출값이며 추가 자유계수로 넣지 않는다.",
         f"The input alpha={u['state']['alpha']:.16f} is the arithmetic calibration fitting D=0.268. The threshold h={u['update']['sigmoid_threshold_h']:.15f} fits phenotype 0.05. Return 0.682 follows by closure. Beta in the constant-admission comparison and beta_eff in the zeta update have different roles. In the default update, beta_eff={r['derived_effective_beta']:.16f} is computed as phenotype divided by available odd-composite weight and is not supplied as an extra free coefficient.")
    text('4.8769%는 alpha=2에서 홀수 합성수 전체를 받아들인 비교값이고, 26.7942%는 alpha=1.9에서의 짝수 합성수 비교값이다. 서로 다른 행의 값을 더하지 않는다. 아래 두 행은 각각 자기 분모에서 합이 1이며, 이번 공동 보정의 기본 행은 alpha 약 1.899687695와 갱신 임계값 h를 사용한다.',
         'The 4.8769% comparison admits all odd composites at alpha=2, while 26.7942% is the even-composite comparison at alpha=1.9. Values across those rows are never added. Each row has its own normalized denominator; the joint reference instead uses alpha about 1.899687695 and the update threshold h.')
    sections.append(table(['alpha','Odd composite %','Even composite %','Prime %'], [[f"{x['alpha']:.1f}",f"{100*x['full_odd_composite_share']:.6f}",f"{100*x['even_composite_share']:.6f}",f"{100*x['prime_share']:.6f}"] for x in r['separate_exponent_comparisons']]))
    text('## 상류 입력과 갱신 경계', '## Upstream inputs and the update boundary')
    text('인터페이스 wrra.upstream-ledger/1은 주소 상태, 가중 규칙, 채택 스펙트럼, 결합 계수와 위상, 입장 갱신, 복귀 경계, 채널 결합과 출처 해시를 고정한다. 기본 주소 상태는 정규화한 대각 n^-alpha 분포다. 계산 API는 별도의 정규화 대각 상태도 검사한다. 일반적인 전체 주소 밀도행렬의 대규모 동역학은 이번 실행 범위에 포함하지 않는다. 하류 운반자의 rho와 주소 상태는 서로 다른 상태 공간의 입력이며 기준 채널 연결은 공개한 조건부 배분 규칙이다.',
         'Interface wrra.upstream-ledger/1 fixes the address state, measure, adopted spectrum, coefficients and phases, admission update, recovery boundary, channel coupling and source hashes. The reference address state is a normalized diagonal n^-alpha distribution; the computational API also checks supplied normalized diagonal states. Large-scale dynamics of a general full address density matrix are outside this run. Downstream carrier rho and the address state are inputs on different state spaces, coupled by the declared conditional routing rule.')
    text('스펙트럼은 독립 고정밀 계산과 Euler Maclaurin 전개로 다시 확인한 처음 네 양의 제타 영점 높이 gamma_j다. 각 계수는 1/2, 초기 위상은 0, xi=0.1, 입장 갱신 수 K=8이다. 제타 영점과 cos 구동을 채택하는 것은 상류 모형 입력이다. 갱신 번호 k와 xi는 차원 없으며 초 또는 고유시간을 부여하지 않는다. 스펙트럼을 물리 에너지 준위로 읽는 일은 0.12에서 허용 모드와 경계조건을 함께 계산한다.',
         'The spectrum is the first four positive zeta-zero heights gamma_j, rechecked by independent high-precision computation and Euler Maclaurin expansion. Each coefficient is 1/2, initial phases are zero, xi=0.1, and there are K=8 admission updates. Selecting zeta heights and cosine driving is an upstream model input. Update index k and xi are dimensionless; seconds and proper time are not assigned. Physical spectral energies require allowed modes and boundary conditions in 0.12.')
    eq(2, r'\delta_n(k)=\sum_{j=1}^{J}c_j\cos\!\left[\gamma_j(\log n+\xi k)+\theta_j\right].')
    eq(3, r'a_n(k)=\frac{1}{1+e^{h-\delta_n(k)}},\qquad T_n(K)=1-\prod_{k=0}^{K-1}(1-a_n(k)).')
    text('홀수 합성수의 아직 입장하지 않은 주소 가중치 r_n에서 새 입장량 b_n을 떼어낸다. 매 갱신의 시도량을 그대로 더하면 이미 입장한 부분을 중복 계산한다. 누적곱과 순차 고갈 계산을 따로 실행해 일치를 확인했다. 짝수 합성수는 시작부터 D에 있고, 소수와 아직 입장하지 않은 홀수 합성수는 복귀 경계까지 SOURCE 대기분 S로 남는다.',
         'New admission b_n is removed from the still-unadmitted odd-composite reservoir r_n. Adding attempts without depletion would count previously admitted weight again. Cumulative products and sequential depletion are computed independently and agree. Even composites occupy D from the start; primes and unadmitted odd composites remain pending SOURCE S until the recovery boundary.')
    eq(4, r'b_n(k)=r_n(k)a_n(k),\qquad r_n(k+1)=r_n(k)-b_n(k),\quad r_n(0)=w_n.')
    text('기준 경계 k=K에서 대기분 S를 복귀 장부 R로 옮긴다. 그 뒤 잔존 접힘에 항등 갱신을 적용하는 것이 이번 보존 규칙이다. 이 규칙의 기원이나 실제 우주 복귀의 동역학을 도출한 것은 아니다. 아래 S와 R은 같은 것을 두 번 합산하지 않는다. 시작 행 k=-1은 첫 입장 전 상태이며 물리적 음의 시간을 뜻하지 않는다.',
         'At the declared boundary k=K, pending S is transferred to the return ledger R. Subsequent resident folds use an identity update, the retention rule of this release. Its origin and dynamical cosmological recovery are not derived. S and R are never counted twice. Row k=-1 denotes the state before admission and is not a negative physical time.')
    eq(5, r'e_\varphi(n)=\mathbf1_{\mathrm{odd\ comp}}T_n(K),\quad e_D(n)=\mathbf1_{\mathrm{even\ comp}},\quad e_R(n)=1-e_\varphi(n)-e_D(n).')
    eq(6, r'f_s=\sum_n w_ne_s(n),\quad e_s(n)\geq0,\quad\sum_se_s(n)=1,\quad\sum_sf_s=1.')
    eq(7, r'\varphi_k+D_k+S_k+R_k=1,\quad R_{k<K}=0,\quad S_{k\geq K}=0.')
    sections.append(table(['k','Phenotype %','Resident D %','Pending S %','Return R %'], [[str(x['frame']),f"{100*x['phenotype']:.6f}",f"{100*x['resident_nonphenotype']:.6f}",f"{100*x['source_pending']:.6f}",f"{100*x['return']:.6f}"] for x in r['frame_transport']]))
    text('## 잔존 Actual과 전체 Actual의 범위', '## Resident Actual and complete Actual scopes')
    text('상류의 잔존 Actual은 복귀 경계 뒤 남는 phi+D이며 전체 주소 분모에서는 31.8%다. 하류의 전체 Actual 장부는 현재 모형의 표현형, 비표현형 잔존 및 복귀의 배경 응답 출처를 모두 집계하므로 100%다. R이 이미 복귀했는데도 잔존 주소 상태에 그대로 남았다는 뜻은 아니다. 복귀 출처를 하류 배경 응답에 대응시키는 장부를 별도로 포함한 것이다.',
         'Upstream resident Actual is phi+D after the recovery boundary and occupies 31.8% of the full address denominator. The downstream complete Actual ledger accounts for phenotype, resident nonphenotype and the returned provenance of a background response, totaling 100%. This does not mean returned R remains in the resident address state. Its provenance is represented separately in the downstream response ledger.')
    eq(8, r'A_{\mathrm{resident}}=f_\varphi+f_D=0.318,\qquad A_{\mathrm{complete\ ledger}}=f_\varphi+f_D+f_R=1.')
    eq(9, r'f_{\varphi\mid A}=\frac{f_\varphi}{f_\varphi+f_D},\quad f_{D\mid A}=\frac{f_D}{f_\varphi+f_D},\quad f_{R\mid A}=0.')
    text('잔존 범위 안에서 다시 정규화하면 표현형은 약 15.72327%, D는 약 84.27673%다. 이것을 전체 우주의 5%·26.8%·68.2%와 혼동하지 않는다. 표의 세 부문 및 잔존과 전체 행은 같은 원래 분모로 표시한다. 실제 입력과 장부는 반올림하지 않은 값을 저장하며 표만 표시 자릿수로 반올림한다.',
         'Renormalization within the resident scope gives about 15.72327% phenotype and 84.27673% D. These conditional shares differ from the full 5%, 26.8% and 68.2% partition. The following sector, resident and complete rows all use the original denominator. Stored inputs and ledgers remain unrounded; only displayed tables are rounded.')
    labels = ['표현형 phi','비표현형 잔존 D','복귀 R','잔존 Actual','전체 집계 Actual'] if ko else ['Phenotype phi','Resident nonphenotype D','Return R','Resident Actual','Complete accounted Actual']
    values = [r['terminal_common_arithmetic_ledger'][s] for s in ('phenotype','resident_nonphenotype','return')]+[r['upstream_resident_Actual'],r['complete_current_Actual']]
    sections.append(table(['Scope','Original denominator','Share %'], [[label,'1',f'{100*value:.8f}'] for label,value in zip(labels,values)]))
    text('## 선택된 입자 채널에 대한 조건부 연결', '## Conditional connection to selected particle channels')
    text('0.8의 실제 선택 F_DX와 16개 출처에서의 순열 P를 그대로 실행한다. 표현형 주소 가중치를 조건부 출처 커널 q_i(n)에 따라 배분한 뒤 선택 순열을 적용하고, 정규화한 세 세대 상태 p_g를 곱한다. 기본 커널은 주소에 공통인 1/16, 세대는 각각 1/3이다. 최소 소인수가 특정 홀수 소수인 주소군에는 다른 정규화 커널을 입력할 수 있고, 비균등 커널 및 세대 가중치를 실제 대조했다.',
         'The actual 0.8 selection F_DX and its permutation P on sixteen origins are executed unchanged. Phenotype address weight is routed through a conditional origin kernel q_i(n), then the selected permutation and normalized generation state p_g are applied. The reference uses an address-independent 1/16 kernel and 1/3 per generation. A family classified by its odd smallest prime can supply a different normalized kernel; nonuniform kernels and generation weights are executed as controls.')
    eq(10, r'x_i=\sum_nw_ne_\varphi(n)q_i(n),\quad\sum_iq_i(n)=1,\qquad y=Px.')
    eq(11, r'W_{g,i}=p_gy_i,\quad P^\dagger P=I,\quad\sum_gp_g=1,\quad\sum_{g,i}W_{g,i}=f_\varphi.')
    text('이 주소와 채널의 대응은 공개한 구성 입력이다. 소수 계보로부터 특정 입자 이름이나 질량을 고유하게 도출했다는 주장은 하지 않는다. 입자 채널의 Y와 Q는 0.8의 동일 연산자로 계산한다. 아래 가중치는 기준 커널에서 표현형 5%를 나눈 값이며 관측된 입자 점유율 또는 새 우주 구성비가 아니다. 표준모형 손지기 성분 45개와 조건부 중성 확장 슬롯 3개를 유지한다. 중성 확장 슬롯의 존재·질량·점유는 이번 계산으로 측정하지 않는다.',
         'The address-to-channel correspondence is a disclosed constitutive input. It does not uniquely derive particle identities or masses from prime genealogy. Y and Q use the same 0.8 charge operator. The weights below divide the reference 5% phenotype budget and are not measured particle populations or new cosmic composition fractions. The inventory retains 45 Standard-Model chiral components and three conditional neutral extension slots; their existence, mass and occupation are not measured here.')
    rows=[]
    for field in ('Q_L','L_L','u_c','d_c','nu_c','e_c'):
        selected=[x for x in r['channel_inventory'] if x['field']==field]
        rows.append([field,str(len(selected)),selected[0]['Y'],f"{100*sum(x['arithmetic_phenotype_weight'] for x in selected):.8f}"])
    sections.append(table(['Field','Count','Y','Full ledger weight %'],rows))
    text('## 물리 에너지와 압력으로 가는 다음 경계', '## The next boundary to physical energy and pressure')
    text('현재의 공통 산술 분할은 5%·26.8%·68.2%이고, 0.6~0.8의 물리 에너지 보정은 4.93%·26.5%·68.57%다. 두 값을 별도 장부로 보존하며 산술 보정으로 기존 에너지 입력을 덮어쓰지 않는다. 현재 0.8의 부하·압력에서 중력과 팽창으로 가는 계산은 그대로 재현된다. 새로운 복귀분이 배경 에너지를 유지하는 방식은 physical_bridge의 배경 응답 대응으로 명시하되 실제 에너지 함수와 압력 함수는 비워 둔다.',
         'The common arithmetic partition is 5%, 26.8% and 68.2%, while the 0.6 to 0.8 physical energy calibration remains 4.93%, 26.5% and 68.57%. Separate ledgers preserve both; arithmetic calibration never silently overwrites physical inputs. Existing 0.8 load and pressure calculations leading to gravity and expansion are reproduced. Returned provenance is structurally assigned to the background-response branch in physical_bridge, but its energy and pressure functions remain unset.')
    text('0.10은 주소별 물리 에너지 부하 epsilon_s(n,V), 부문 결합과 부피 의존성을 명시해야 한다. 다음 식은 그 인터페이스가 충족해야 할 에너지·압력 관계이며 0.9가 실행한 산출식이 아니다. R=68.2%만으로 압력이 정해지지 않고, 95:5만으로 길이가 정해지지 않는다. 실제 팽창 응답과 앞으로 검증할 뒤틀림의 인과 설명도 구분한다. c는 SI 정의값을 고정 입력으로 유지한다.',
         'Version 0.10 must specify physical energy load epsilon_s(n,V), sector coupling and volume dependence. The following relation is a requirement for that interface, not an executed 0.9 output. R=68.2% alone does not determine pressure, and 95:5 alone does not determine length. Existing expansion response and the future causal account of twist remain distinct. The SI defining value of c stays a fixed input.')
    eq(12, r'E_s(V)=\sum_nw_ne_s(n)\epsilon_s(n,V),\qquad P_s=-\left.\frac{\partial E_s}{\partial V}\right|_{\mathcal S}.')
    text('갱신 순서와 물리 시간, 주소 컷오프와 제타 영점 컷오프 및 정보 용량, 국소 임계값과 전역 Capacity는 후속 단계에서 구분하여 닫는다. 상류 입력의 미시적 생성 기원, 전 우주 과부하와 리셋, 초기 개폐와 최초 컷오프의 선택은 상류 과제로 남는다. 장부의 코드 실행 기록은 재현 출처이며 물리 관측 기록이나 누적 꼬임 기록으로 부르지 않는다.',
         'Subsequent stages separate update order from physical time, address cutoff from zeta cutoff and information capacity, and local thresholds from global Capacity. Microscopic generation of upstream inputs, global overload and reset, initial opening and initial cutoff selection remain upstream questions. Software execution provenance is not called a physical observation record or an accumulated twist record.')
    text('## 검증과 재현', '## Verification and reproduction')
    text('26개 묶음은 독립 소수 분류, 동결한 상류 코드와 결과, 제타 영점 재검산, 누적곱과 고갈 수송, 각 주소와 각 갱신의 보존, Actual 분모, 0.8 전체 결과의 동일성, 비균등 채널 결합, 임의 대각 상태와 작은 결맞음 상태의 효과 양성, 명시적 산술 재보정, 경계 변경, 서로 다른 미시 규칙의 같은 총량, 컷오프 구분, 잘못된 입력 16개의 차단과 출처 해시를 포함한다.',
         'The 26 groups cover independent primality, frozen upstream code and results, independently checked zeta heights, cumulative products versus depletion, address and frame conservation, Actual denominators, equality of all 0.8 results, nonuniform channel coupling, arbitrary diagonal states and effect positivity on a small coherent state, explicit arithmetic refitting, boundary changes, equal aggregates from different microscopic rules, separate cutoffs, rejection of sixteen invalid inputs, and provenance hashes.')
    text('K를 4와 16으로 바꾸고 나머지 보정을 고정하면 표현형은 약 3.704795%와 5.682474%가 된다. xi=0에서 h를 명시적으로 다시 보정하면 5%를 다시 맞추지만 주소별 입장은 달라진다. 따라서 총량 재현은 내부 주소 규칙의 유일성을 뜻하지 않는다. 검증된 보정값과 공개한 규칙 아래의 설명 성과를 인정하며, 모형을 확정한 뒤 미측정 값을 산출하는 단계에서 예측을 구분한다.',
         'Changing K to 4 and 16 with other calibrations frozen gives phenotype about 3.704795% and 5.682474%. With xi=0, explicitly refitting h restores 5% while address admissions differ. Aggregate reproduction therefore does not establish a unique microscopic rule. Explanatory reproduction under validated calibration and declared rules is accepted; prediction is reserved for later unmeasured outputs after model fixation.')
    sections.append('```bash\npython -m pip install -r calculations/wrra_m_0_9/requirements.txt\npython calculations/wrra_m_0_9/run_release.py\n```')
    text('압축파일 루트에서 위 명령을 실행하면 입력 장부·결과 JSON, 갱신·분모·주소·채널 CSV와 검증 결과가 생성된다. parameters.json이 유일한 구성 입력이며 상류 원본 5개와 0.8 입력을 함께 동결한다. 깨끗한 복사본에서 저장 산출물을 지우고 실행해 바이트 단위 재현과 SHA256 목록을 확인한다. 문서의 한영 수식 및 계산 표를 대조한다.',
         'From the archive root, the command generates the input and result JSON, frame, scope, address and channel CSVs, and verification report. Parameters.json is the single configuration input, embedding the 0.8 input and five upstream snapshots. A clean copy removes captured outputs before execution and checks byte-identical reproduction and the SHA256 manifest. Bilingual equations and calculated tables are matched.')
    sections.append('Input SHA256 '+r['input_hash_sha256'])
    text('## 후속 개발 순서', '## Subsequent development order')
    text('다음은 0.10 에너지·압력 사상, 0.11 첫 다섯 입력의 순차 보정 G → H0 → f_phi → f_c → m_e c^2, 0.12 셔터와 고유시간 및 스펙트럼, 0.13 양자화와 관측 및 기록, 0.14 컷오프와 정보 용량, 0.15 응력과 뒤틀림 및 크기, 0.16 중성미자 질량·혼합·진동, 0.17 같은 기하의 전파, 1.0 통합 검증과 확정이다. 각 판은 검증 입력 → WRRA 고유 변환 → 산출값 → 반증조건으로 닫는다.',
         'The sequence continues with 0.10 energy and pressure mapping; 0.11 sequential calibration G → H0 → f_phi → f_c → m_e c^2; 0.12 shutter, proper time and spectra; 0.13 quantization, observation and records; 0.14 cutoffs and capacity; 0.15 stress, twist and size; 0.16 neutrino mass, mixing and oscillation; 0.17 propagation in the same geometry; and 1.0 integration audit and fixation. Each version closes through verification input, WRRA-specific transformation, output and falsification conditions.')
    text('## 참고 자료', '## References')
    sections.append('Choi Wonsik. WRRA-M 0.1 to 0.8 and upstream hypotheses. GitHub research repository. https://github.com/Wonsik-Choi-janefather/wrra-m-0.1\n\nChoi Wonsik. Upstream two stage filter v1.0 and zeta frame v0.1. Source commit 9ca21c547e5238be34ceace5a1015db50cb824ff. Included reference snapshots.\n\nChoi Wonsik. Minimal Computation Cosmology 2.3.2. Common carrier baseline. https://github.com/Wonsik-Choi-janefather/minimal-computing-cosmology-2.3.2\n\nNIST Digital Library of Mathematical Functions. Sections 25.10 and 25.11 iii. Zeta zeros and Euler Maclaurin representation. https://dlmf.nist.gov/25.10 https://dlmf.nist.gov/25.11\n\nCopyright 2026 Wonsik Choi. CC BY 4.0. https://creativecommons.org/licenses/by/4.0/')
    (ROOT/f'source_{lang.lower()}.md').write_text('\n\n'.join(sections)+'\n')


if __name__ == '__main__':
    build('KO'); build('EN')
