"""Generate matched KO/EN mathematical sources from the actual result ledger."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
R=json.loads((ROOT/'results/results.json').read_text())
CHECK=json.loads((ROOT/'results/release_checks.json').read_text())
C=R['calibration'];H=R['state_histories'][1];V=H['verification']

EQ={
1:r'R=\frac{I_{16}}{16}\otimes\rho,\qquad \rho\succeq0,\quad\mathrm{Tr}\rho=1,\quad J_s=\mathrm{Tr}(\rho K_s).',
2:r'K_c=2I-T-T^\dagger,\qquad K_b=\frac{K_c+\epsilon|0\rangle\langle0|}{1+\epsilon/(2N)}.',
3:r'u_{\mathrm{crit},0}=\frac{3H_0^2c^2}{8\pi G},\quad \eta=\frac{f_hu_{\mathrm{crit},0}}{2},\quad \chi=\frac{f_c}{f_h}.',
4:r'h(a)=\chi a^{n_c}K_c+(1-\chi)a^{n_b}K_b,\quad \mathcal H(a)=\eta V_0h(a).',
5:r'E_h=\mathrm{Tr}(\rho\mathcal H),\quad V=V_0a^3,\quad u_h=\frac{E_h}{V}=u_c+u_b.',
6:r'u_c=\eta\chi a^{n_c-3}J_c,\qquad u_b=\eta(1-\chi)a^{n_b-3}J_b.',
7:r'p_s=-\left(\frac{\partial E_s}{\partial V}\right)_\rho=-\frac{n_s}{3}u_s,\qquad n_c=0,\quad n_b=3.',
8:r'\dot\rho=-\frac{i\ell}{\mathcal A_*}[\mathcal H,\rho]=-i\ell\omega_*[h,\rho],\quad \mathcal A_*=\frac{\eta V_0}{\omega_*}.',
9:r'\mathrm{Tr}(\mathcal H\dot\rho)=0,\quad \dot E_h=-p_h\dot V,\quad \dot u_h+3H(u_h+p_h)=0.',
10:r'S_g=-\frac{3c^2V_0}{8\pi G}\int dt\,\frac{a\dot a^2}{\ell}.',
11:r'S_I=\int dt\left[i\mathcal A_*\mathrm{Tr}(\rho_0U^\dagger\dot U)-\ell(E_{\phi,0}+\mathrm{Tr}(\rho\mathcal H))\right].',
12:r'H^2=\frac{8\pi G}{3c^2}u_{\mathrm{tot}},\qquad \frac{\ddot a}{a}=-\frac{4\pi G}{3c^2}(u_{\mathrm{tot}}+3p_h).',
13:r'Q_s=\eta\chi_s a^{n_s-3}\dot J_s,\qquad \dot u_s+3H(u_s+p_s)=Q_s,\quad Q_c+Q_b=0.',
14:r'q=\frac{u_{\mathrm{tot}}+3p_h}{2u_{\mathrm{tot}}},\qquad n_c=0,\ n_b=3:\quad q<0\ \Longleftrightarrow\ 2u_b>u_\phi+u_c.',
15:r'\zeta\kappa_h^2=\frac{16\pi G}{c^4}u_h,\qquad a_T^2=\frac{\pi G}{3}u_c=\frac{\zeta c^4}{48}\kappa_c^2.',
16:r'y=\frac{g_M}{a_T},\quad \nu(y)=\frac{1}{1-e^{-\sqrt y}},\quad g=\nu(y)g_M,\quad v_c^2=rg.',
17:r'\widehat\alpha_R(b)=\frac{2}{c^2}\int_{-\sqrt{R^2-b^2}}^{\sqrt{R^2-b^2}}g(\sqrt{b^2+z^2})\frac{b\,dz}{\sqrt{b^2+z^2}}.',
18:r'L=L_0a,\quad Q=\sum_{i=1}^{3}\Theta_i^2,\quad W=\zeta Q=\frac{16\pi G}{c^4}u_hL^2.',
19:r'E_h=\frac{c^4}{16\pi G}WL,\qquad L=\frac{16\pi GE_h}{c^4W}\quad(W>0).',
20:r'\frac{H^2}{H_0^2}=(f_\phi+f_c)a^{-3}+f_b,\qquad \frac{W}{W_0}=\frac{f_c/a+f_ba^2}{f_h}.',
21:r'K_{\mathrm{phys}}(a)=\frac{h(a)}{a^3},\qquad \lambda_{\min}(K_{\mathrm{phys}})\leq\mathrm{Tr}(\rho K_{\mathrm{phys}})\leq\lambda_{\max}(K_{\mathrm{phys}}).',
22:r'\rho=I_N/N:\quad J_c=J_b=2,\qquad q_0=\frac{1-n_bf_b}{2}\quad(n_c=0).'
}
def E(i):return '\n$$'+EQ[i]+' \\tag{'+str(i)+'}$$\n'
def table(headers,rows):return '\n| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,row))+' |\n' for row in rows)+'\n'
state_names_ko=['균등 기준','낮은 모드','일관된 중첩','높은 모드','영 모드']
state_names_en=['Uniform reference','Low mode','Coherent packet','High mode','Zero mode']
def states(lang):
    names=state_names_ko if lang=='KO' else state_names_en
    return table(['정보 상태' if lang=='KO' else 'Information state','J','aT m/s²','v km/s'],
      [[name,f"{s['J']:.6f}",f"{s['aT_m_s2']:.6e}",f"{s['v_total_km_s']:.6f}"] for name,s in zip(names,R['present_information_state_outputs'])])
def backgrounds(lang):
    rows=[next(x for x in R['reference_background']['rows'] if x['a']==a) for a in [.5,1.,2.]]
    return table(['a','H/H₀','q','W/W₀','κh/κh₀','aT/aT₀'],[[f"{x['a']:.1f}",f"{x['H_over_H0']:.6f}",f"{x['deceleration_q']:.6f}",f"{x['zeta_Q_over_reference']:.6f}",f"{x['twist_rate_over_reference']:.6f}",f"{x['aT_over_reference']:.6f}"] for x in rows])
def scans():return table(['nb','wb','q₀'],[[f"{x['background_energy_exponent']:.1f}",f"{x['derived_w_background']:.6f}",f"{x['q_present_uniform']:.6f}"] for x in R['energy_homogeneity_scan']])
verification_rows=[
 ('에너지의 부피 미분과 압력','Pressure from finite volume variation',R['verification']['pressure_from_finite_volume_variation_max_relative_error']),
 ('비가환 상태의 노름 오차','Noncommuting state norm error',V['raw_norm_max_error']),
 ('총 연속 방정식 잔차','Total continuity residual',V['continuity_finite_difference_max_scaled_residual']),
 ('H 미분과 가속도 일치','Acceleration from derivative of H',V['acceleration_from_H_max_absolute_error']),
 ('응력 교환 상쇄','Internal exchange cancellation',V['internal_exchange_cancellation_max_scaled_error']),
 ('유한 T³ 접합 관계','Finite T3 closure identity',V['finite_T3_closure_max_absolute_error']),
 ('별도 가속도 해의 제약 오차','Constraint in independent acceleration solution',max(x['acceleration_solver_constraint_max_relative_error'] for x in H['independent_propagation_checks']))]
def verifications(lang):return table(['검사' if lang=='KO' else 'Check','최대 오차' if lang=='KO' else 'Maximum error'],[[x[0 if lang=='KO' else 1],f'{x[2]:.3e}'] for x in verification_rows])

ko='''# WRRA M 0 6 정보부하와 뒤틀림 중력 및 팽창의 유한 연결

공통전달자 상태에서 에너지 부하와 압력을 계산하는 연속 기하 모형

최원식 Wonsik Choi  
WRRA-M 0.6-r2 | 2026년 10월 1일  
Independent Researcher Seoul Republic of Korea  
ORCID 0009-0001-4263-9772 | janefather@gmail.com

## 연구 결과와 계산 범위

본 연구는 공통전달자의 정보 상태를 물리적 부하로 변환하고, 그 부하를 뒤틀림과 국소 중력 및 전역 팽창에 전달하는 유한 구성 모형을 완성한다. 하나의 에너지 함수가 정보 상태의 진화, 부피 변화에 대한 압력, 배경의 팽창을 함께 정한다. 따라서 전달자 시험과 국소 중력 계산 사이에 상태별 가중치 계산을 넣고, 기존에 따로 선언했던 배경 압력을 같은 함수의 미분으로 계산할 수 있다.

이 완성은 선언한 유한·동질 모형 안의 완성이다. 에너지의 부피 의존성, 부하 연산자와 정보 시계는 구성 선택으로 공개한다. 압력과 보존식은 그 선택에서 따라 나오는 결과다. 실제 우주의 유일한 미시 법칙이나 완전한 4차원 공변 중력 이론을 발견했다고 주장하지 않는다. 국소 회전과 렌즈는 기존에 보정한 응답에 같은 모이는 부하를 넣어 계산하는 조건부 산출값이다.

WRRA Core 1.0과 최소계산우주론 MCC 2.3.2를 기준으로 유지한다. 질량은 표현형이므로 양자화 가능하고 근본 중력은 표현형 이전이라는 B_C의 비양자 전제를 보존한다. 정보 상태의 행렬 표현은 사용하지만 중력 자체의 독립 힐베르트 공간이나 중력자를 도입하지 않는다. 이 선택을 중력 양자화 불가능성의 보편적인 정리로 분류하지 않는다.

## 개별 뒤틀림 논문에서 이어받은 구조

뒤틀림 응력 우주 논문의 이차 에너지 부하와 보정 응답, 이중 성분 중력 논문의 직접 성분·모이는 응력 회계, 유한 무경계 논문의 전역 접합과 국소 곡률의 구분을 이어받는다. 특히 MCC 2.3.2 제28–29장의 전역 배경과 국소 응력은 같은 표현형 이전 부하의 두 응답으로 취급한다. 여기에 별도의 암흑 성분을 더해 같은 효과를 두 번 세지 않는다.

현재의 후기 우주 보정은 표현형 4.93%, 전체 숨은 부하 95.07%, 모이는 부문 26.5%, 잔여 배경 68.57%다. 모두 우주 전체를 분모로 한 에너지 가중 비율이다. 26.5%는 숨은 95.07% 안의 부분이며, 정보 비트 수나 입자 채널 수의 측정비가 아니다. 이 비율들은 재현 입력으로 공개하고 갱신 가능하게 둔다.

## 공통전달자에서 상태별 부하까지

16개 시험 채널은 같은 내부 격자를 공유한다. 내부 정보 상태 ρ는 양의 준정부호 행렬이고 trace가 1이다. 부하 Js는 상태와 양의 연산자의 trace로 계산한다.
'''+E(1)+'''
N=128인 주기 격자의 순환 라플라시안을 모이는 부문의 연산자로 사용한다. 배경 연산자는 같은 연산자에서 출발하고, 비가환 시험에서만 양의 rank 1 항을 추가한다. 분모는 균등 상태의 배경 부하가 2가 되도록 고정한다.

0.6의 lattice_N을 정보부하와 수송 전달자 검사의 공통 격자 크기로 적용한다. 기존 0.5 입력은 보정 출처로 보존하고, 전달자 계산용 복사본에만 공통 값을 적용한다. 결과의 lattice_contract는 원래 입력과 실제 적용값을 함께 공개한다. 64/128 및 128/64의 교차 입력 시험에서 두 계산의 격자가 일치하고 균등 기준 산출값이 유지됨을 확인했다.
'''+E(2)+'''
기준 계산은 ε=0이고, 비가환 시험은 ε=8이다. ε=8을 실제 우주의 선호값으로 제시하지 않는다. 이는 서로 다른 두 부하 가중치가 같은 정보 상태에서 교환하는지를 검사하는 고정 시험이다. 두 연산자는 모든 채널에 동일하게 적용하므로 이 변경이 채널별 필터 선택을 해결하지는 않는다.

기준 균등 상태에서는 Jc=Jb=2다. 물리 단위를 주는 에너지 밀도 계수 η는 기존 숨은 부하를 한 번 보정해 정한다.
'''+E(3)+'''
같은 trace=1 상태라도 가중치가 다른 부하를 만든다. 여기서 정보의 무게는 정규화된 상태의 개수만이 아니라 그 상태가 에너지 연산자에 주는 기대 부하다. 임의의 비트 하나에 보편적인 정지질량이나 고정 에너지를 부여하지 않는다.

## 한 에너지 함수와 압력

대표 부피를 V₀a³으로 두고, 다음 에너지 연산자를 선언한다. 지수 nc와 nb는 정보부하가 부피 변화에 어떻게 반응하는지를 정하는 구성 입력이다.
'''+E(4)+E(5)+E(6)+'''
압력은 상태를 고정한 부피 미분으로 계산한다. 각 부문의 에너지는 a의 ns승에 비례하므로 미분 결과는 다음과 같다.
'''+E(7)+'''
nc=0은 모이는 부문의 고정된 공변 부피 에너지와 압력 0을 뜻한다. nb=3은 배경 에너지가 물리적 부피에 비례하고 압력이 배경 에너지 밀도의 음수인 구성이다. 이 판에서는 w를 별도 입력으로 다시 넣지 않는다. 그러나 지수 3의 미시적 기원까지 유도한 것은 아니다. 일정한 에너지 밀도와 음의 압력은 선택한 부피 의존성의 정확한 결과다.

## 정보 상태의 진화와 총 보존

같은 에너지 연산자가 손실 없는 상태의 진화를 생성하도록 구성한다. ℓ은 시간 lapse이고, 계산에서는 ℓ=1을 사용한다. 양의 작용 척도 A*는 정보 시계를 정하며 플랑크 상수와 동일시하지 않는다. 현재의 ω*/H₀=0.7도 공개한 시험 입력이다.
'''+E(8)+'''
ρ=Uρ₀U†인 unitary 궤도에서는 trace와 양의 준정부호성, 상태의 고윳값이 보존된다. trace의 순환 성질에 따라 상태 변화가 같은 순간의 에너지 연산자에 주는 부하는 0이다. 에너지 변화에는 부피에 대한 일만 남는다.
'''+E(9)+'''
이는 정보 상태가 변하지 않는다는 뜻이 아니다. 개별 Jc와 Jb는 변할 수 있다. 두 연산자가 교환하지 않으면 내부 부문 사이의 에너지 교환이 생기지만 그 합은 상쇄된다. 순수 상태의 위상과 혼합 상태의 고윳값 회계를 전역 팽창과 함께 사용할 수 있다.

## 고전 배경 작용과 팽창

유한 T³의 등방적인 평탄 평균을 선택해 고전적인 배경 작용을 쓴다. 공간 접합의 선택과 국소 추가 중력은 별개다. 고전 중력 작용은 다음과 같다.
'''+E(10)+'''
상태 궤도의 작용과 표현형 부하를 같은 lapse에 연결한다. Eφ,0는 압력 없는 표현형의 고정된 공변 부피 에너지다.
'''+E(11)+'''
Sg와 SI를 합해 ℓ을 변분하면 Friedmann 제약을 얻고, a를 변분하면 가속도 방정식을 얻는다. U를 변분한 상태 방정식은 식 (8)이다. 이로써 동질 배경의 상태·에너지·압력·팽창은 하나의 유한 작용으로 닫힌다.
'''+E(12)+'''
이 작용은 동질 자유도로 제한한 minisuperspace 작용이다. 국소 광자 전달, 비등방 응력, 공간 섭동이나 은하의 배경 역반응을 유도한 완전한 4차원 작용으로 확대하지 않는다. Friedmann 및 연속 방정식은 표준적인 외부 수학이며 [5], 이번 모형의 구성 소유권은 정보부하 연산자와 진화·압력·뒤틀림 응답의 연결에 있다.

부문별 보존식에는 상태의 변화에 따른 교환항을 넣는다. χc=χ, χb=1−χ이다.
'''+E(13)+E(14)+'''
따라서 팽창과 가속 팽창은 구분된다. 선택한 nc=0, nb=3 구성에서 가속 팽창은 배경 부하가 직접 성분과 모이는 부하의 합에 대해 위 부등식을 만족할 때 생긴다. 모든 뒤틀림이나 모든 정보 상태가 자동으로 가속 팽창을 만든다고 말하지 않는다.

## 같은 부하에서 뒤틀림과 국소 중력까지

전체 숨은 에너지 밀도는 전역 뒤틀림률을 정하고, 그중 모이는 밀도만 국소 추가 인력 척도에 넣는다.
'''+E(15)+'''
두 번째 관계는 0.5의 aT=cH√(fc/8)을 임계 밀도로 정리한 기존 보정 관계다. 상태 변화에 따라 uc가 달라지면 aT도 실제 계산으로 달라진다. 전역 H를 바꾸고도 현재의 원천 분율을 고정하는 불일치는 사용하지 않는다.

국소 응답은 기존 은하 원반 논문의 보정 함수를 유지한다.
'''+E(16)+'''
시험 원천은 Plummer 질량 6×10¹⁰ 태양질량과 척도 3 kpc이고, 회전속도는 반경 8.2 kpc에서 비교한다. 실제 은하의 시간 진화나 새 관측 적합으로 분류하지 않는다. Φ=Ψ라는 조건 아래 같은 가속도에서 렌즈 편향도 계산한다.
'''+E(17)+'''
렌즈 반경 R=200 kpc와 충격반경 b=10 kpc를 사용한다. 패치 밖 기하와 관측자·렌즈·광원의 거리인자는 포함하지 않는다. 국소 응답의 미시 유도와 중력 slip 검증은 이 판의 완료 주장 밖이다.
'''+states('KO')+f'''
균등 기준은 aT={C['aT0_m_s2']:.9e} m/s²와 207.510905 km/s를 재현한다. 같은 조건의 렌즈 편향은 0.535586511 각초다. 0.5의 가속도·회전·렌즈 산출값과 비교해 일치함을 확인했다. 영 모드에서는 추가 중력이 0이고 정의할 수 없는 비율이나 미계산 렌즈는 null로 기록한다.

## 유한 무경계 구성과 기하 의존 부하

유한 무경계 논문의 대표 접합을 T³로 유지한다. L₀는 미확정 대표 길이이고 L=L₀a다. 양의 강성을 고정하면 뒤틀림 기록의 이차 집계는 물리적 뒤틀림률과 다음처럼 연결된다.
'''+E(18)+E(19)+'''
양의 비영 부하와 유한한 a, 양의 L₀를 둔 각 계산 시점에서 부피는 유한하고 T³의 경계는 없다. 이 관계는 선택한 접합의 정확한 조건부 관계다. 정보부하가 실제 우주의 위상을 유일하게 선택했다거나 절대 우주 길이를 측정했다고 말하지 않는다. a가 무한히 커지는 미래까지 부피의 고정 상한을 증명한 것도 아니다.

균등 기준 상태의 nc=0, nb=3에서 팽창과 전역 뒤틀림 기록의 크기는 다음과 같다.
'''+E(20)+backgrounds('KO')+'''
물리적 뒤틀림률과 전역 뒤틀림 기록의 크기는 다르게 변한다. 기록의 크기는 그 순간의 부하 밀도와 공간 크기로 계산한 집계값이며, 시간에 걸쳐 기록을 누적하는 별도 진화 법칙을 계산한 것은 아니다. 현재 이후에는 팽창과 함께 이 전역 기록의 크기가 커질 수 있지만 밀도에 따른 물리적 뒤틀림률은 줄어든다. 둘을 한 숫자의 꼬임으로 합치지 않는다. a는 여기서 기하의 크기 변수다. 뒤틀림 광자 적색편이 커널을 계산하기 전에는 관측 적색편이로 자동 치환하지 않는다.

![그림 1 한 에너지 함수에서 함께 계산한 팽창과 뒤틀림](results/expansion_twist.png){width=6.4in}

착수 계산은 고정된 부하 연산자로 모든 배경 밀도를 표현하려 해 a=0.5에서 상태 허용 범위를 벗어났다. 이번 판은 에너지의 부피 의존성을 명시했으므로 물리적 부하 연산자도 기하에 따라 변한다.
'''+E(21)+'''
ρ의 trace=1 조건이나 양의성을 완화하지 않았다. 연산자의 스펙트럼 자체가 a에 따라 변하고, 계산한 a=0.5에서 2까지의 기준 상태는 모두 해당 스펙트럼 범위 안에 있다. 이는 새 구성 선택으로 착수 모형의 제한을 해결한 것이다.

## 비가환 상태의 실행 결과

모드 8, 16, 24를 같은 가중치로 중첩해 상태 진화를 실행했다. 교환하는 연산자에서는 위상이 실제로 바뀌어도 평균 부하가 보존된다. 비가환 시험에서는 두 평균 부하가 실제로 달라진다.

Jc는 '''+f"{H['Jc_range'][0]:.6f}에서 {H['Jc_range'][1]:.6f}"+'''까지, Jb는 '''+f"{H['Jb_range'][0]:.6f}에서 {H['Jb_range'][1]:.6f}"+'''까지 변했다. 이는 ε=8과 지정한 정보 시계에서 계산한 시험 결과다. 숨은 정보의 개수가 달라져서가 아니라 같은 상태의 가중치와 기하 의존 에너지에서 나온 변화다.

![그림 2 부하 변화와 상쇄되는 내부 응력 교환](results/state_exchange.png){width=6.4in}

두 부문을 각각 외부에서 독립적으로 공급하지 않았다. 총 보존은 식 (9)와 (13)에서 성립한다. 수치적으로도 직접 계산한 교환항의 합이 0에 가깝고, 별도의 유한차분으로 총 연속 방정식을 확인했다.

## 검증과 반증 조건

상태 ODE는 DOP853으로 양방향 적분했다. 같은 초기 상태에서 별도의 중점 unitary 지수 전파를 실행하고 320단계와 640단계의 부하 오차를 비교했다. 비가환 시험의 오차 개선 배수는 두 끝점에서 약 4로, 두 번째 차수의 수렴을 확인했다. 또한 H 제약을 사용해 시간을 적분하는 계산과 별도로 가속도 방정식을 직접 풀어 같은 끝점의 상태 부하와 시간을 비교했다.
'''+verifications('KO')+'''
부피 미분으로 계산한 압력, 동시 기저 변환의 부하 불변성, 표현형 비율 0과 숨은 부하 0의 결합 경계, 잔여 배경 비율 0의 경계도 검사했다. 음의 연산자 계수, 0인 크기 변수와 비유한 정보 시계는 입력에서 거부한다. 이 검증은 동질 모형의 계산 정합성이다. 공간 섭동의 소리속도·안정성이나 실제 렌즈 관측 적합을 검증한 것으로 표시하지 않는다.

선언한 연산자가 양의성을 잃거나 상태의 trace와 양의성이 깨지면 부하 모형을 기각한다. 부피 미분과 압력이 맞지 않거나 교환항이 상쇄되지 않으면 단일 에너지 구성 주장이 실패한다. 별도의 가속도 계산이 Friedmann 제약과 어긋나면 배경 연결을 수정해야 한다. 운동과 렌즈가 같은 응답에서 맞지 않으면 조건부 국소 matching 또는 slip 조건을 수정해야 한다.

## 구성 선택과 완료 주장

에너지 지수의 선택이 팽창에 주는 영향도 실제 계산한다. 균등 기준 상태에서 다음 관계를 사용한다.
'''+E(22)+scans()+'''
배경 지수 1은 고정된 뒤틀림 기록에 해당하는 w=−1/3 부문이며 이 보정에서 가속 팽창을 만들지 못한다. 지수 3은 일정 에너지 밀도와 w=−1을 만들고 기준 배경은 ΛCDM과 같은 팽창 형태다. 이 동일성을 새 독립 관측 예측이나 지수 3의 미시 증명으로 포장하지 않는다. 이미 선언한 정보 에너지의 부피 의존성에서 압력과 동역학을 일관되게 계산한 것이 0.6의 성과다.

| 주장 | 지위 | 이번 결과 |
| --- | --- | --- |
| 상태별 정보부하 | 선택한 연산자 안의 실행 결과 | 행렬 trace와 모드 계산 일치 |
| 상태 진화와 압력 및 총 보존 | 유한 동질 모형의 구성과 계산 | 같은 에너지 함수와 작용 |
| 팽창과 뒤틀림의 공존 | 조건부 배경 산출 | H와 기록 및 뒤틀림률 동시 계산 |
| 정보부하에서 국소 중력까지 | 기존 보정 응답의 조건부 연결 | 회전과 렌즈 계산 및 0.5 재현 |
| 유한 무경계 우주 | 선택한 T³ 구성의 조건부 관계 | 부하와 접합 기록의 길이 관계 |
| 미시 가중치와 에너지 지수의 유일한 기원 | 미해결 | 구성 선택으로 공개 |
| 4차원 공변 완성과 공간 섭동 | 후속 범위 | 동질 작용과 구분 |

0.6의 종료선은 정보 상태에서 부하를 실제로 계산하고, 하나의 에너지 함수와 동질 작용으로 상태 진화·압력·팽창·뒤틀림을 닫으며, 같은 모이는 부하를 기존 국소 응답에 전달하는 것이다. 이 판은 그 유한 종료선까지 계산했다. 대칭 전달자의 선택 격차는 여전히 0이고, 실제 우주의 위상과 길이, 하위차수 필터 기원, 공변 국소 응답과 관측 검증은 남은 물리 과제로 분명히 기록한다.

## 참고문헌과 재현 자료

1. Choi W. 최소계산우주론 MCC 2.3.2. 2026. 제28–29장 전역 배경과 국소 응력 회계. https://doi.org/10.5281/zenodo.22733000.
2. Choi W. 뒤틀림 응력 우주와 암흑물질의 질량 표현형. v1.0. 2026년 9월 11일. https://doi.org/10.5281/zenodo.22700557.
3. Choi W. 질량중력과 공간 뒤틀림 응력 중력의 이중 성분 모형. v0.4. 2026년 9월 27일. 개별 원문을 기준으로 사용.
4. Choi W. WRRA Finite Boundaryless Universe. v1.0. 2026년 9월 28일. 개별 원문을 기준으로 사용.
5. Trodden M and Carroll SM. TASI Lectures Introduction to Cosmology. 2004. §2.2. arXiv:astro-ph/0401547. https://vo.ned.ipac.caltech.edu/level5/Sept03/Trodden/Trodden2_2.html.
6. Choi W. WRRA-M 0.5 Information Load and Twist Gravity in a Finite Model. 2026년 10월 1일. 한글·영문 원고와 수정된 계산 코드.
7. Choi W. WRRA 공간 뒤틀림의 은하 원반면 선택과 암흑질량 표현형. v1.0. 2026년 9월 27일. https://doi.org/10.5281/zenodo.23003875.

compute.py와 두 입력 파일에 보정값·연산자·정보 시계를 명시했다. results.json은 전체 궤도, summary.json은 주요 결과, release_checks.json은 재현과 경계 검사를 기록한다. verify.py는 기존 0.5의 산출값과 비교한다. 한글·영문 원고는 같은 수식과 결과 장부에서 생성한다. 계산에는 numpy, scipy, matplotlib이 필요하고 Word 원고 생성에는 pandoc와 python-docx가 추가로 필요하다.

© 2026 Wonsik Choi. 원고와 계산 자료는 CC BY 4.0으로 배포한다.
'''

en='''# WRRA M 0 6 Information Load and Twist Gravity with Expansion in a Finite Model

A continuous geometric model that computes energy load and pressure from common carrier states

Wonsik Choi  
WRRA-M 0.6-r2 | 1 October 2026  
Independent Researcher Seoul Republic of Korea  
ORCID 0009-0001-4263-9772 | janefather@gmail.com

## Result and computational scope

This work completes a finite constitutive model from common-carrier information states to physical load, twist, local gravity and global expansion. One energy functional supplies state evolution, pressure under volume variation and background dynamics. Individual weighted states therefore connect the carrier calculation to local gravity, while background pressure is computed from the same energy rather than inserted as a separate equation-of-state input.

Completion here is within the declared finite homogeneous model. The volume dependence of energy, load operators and information clock remain disclosed constitutive choices. Pressure and conservation are consequences of those choices. A unique microscopic law of the actual universe and a complete four-dimensional covariant gravity theory are not claimed. Local rotation and lensing are conditional outputs of the inherited calibrated response evaluated with the same clustering load.

WRRA Core 1.0 and Minimal Computation Cosmology MCC 2.3.2 remain the baseline. The B_C premise is preserved: mass may be quantized as a phenotype, whereas fundamental gravity precedes phenotype. Matrix information states are used without introducing an independent gravitational Hilbert space or gravitons. This premise is not classified as a universal theorem excluding gravity quantization.

## Structure inherited from the individual twist papers

The model inherits the quadratic load and calibrated response of twist-stress cosmology, the direct/clustering accounting of the dual-component gravity paper, and the distinction between global gluing and local curvature in the finite boundaryless paper. In particular, the global background and local stress in MCC 2.3.2 Chapters 28–29 are treated as two responses of the same prephenotypic load. No separate dark component is added over that load to count the same effect twice.

The present late-universe calibrations are phenotype 4.93%, entire hidden load 95.07%, clustering sector 26.5% and residual background 68.57%. Each is an energy-weighted fraction of the whole universe. The clustering share is a subset of the hidden total, rather than 26.5% of that total. These are editable inputs, not measured bit-count or particle-channel fractions.

## Weighted states on the common carrier

Sixteen witness channels share one internal lattice. The internal information state ρ is positive semidefinite with unit trace. Its load Js is evaluated by the trace of the state and a positive operator.
'''+E(1)+'''
A periodic cycle Laplacian on N=128 sites is the clustering operator. The background operator starts from the same Laplacian and adds a positive rank-one term only for the noncommuting test. The denominator maintains background load 2 in the uniform state.

Version 0.6 lattice_N controls the common grid for information loads and the transport carrier test. The original 0.5 input is retained as calibration provenance; the shared value is applied only to a private copy for the carrier calculation. The result lattice_contract discloses the configured and effective sizes. Cross-input tests at 64/128 and 128/64 confirm matching grids and unchanged uniform reference outputs.
'''+E(2)+'''
The reference uses ε=0 and the noncommuting test ε=8. The latter is a fixed experiment in exchange between two weighted loads of one state, not a preferred microscopic value for the physical universe. The same operators apply to every witness channel, so this modification does not solve channel-dependent filter selection.

The uniform reference has Jc=Jb=2. A single disclosed calibration of the hidden density supplies the physical density coefficient η.
'''+E(3)+'''
Equal unit-trace states can carry different weighted loads. Information weight here depends on the expectation of the energy operator, rather than the normalized number of states alone. A universal rest mass or fixed energy is not assigned to an arbitrary bit.

## One energy functional and its pressure

For representative volume V₀a³, declare the following energy operator. The exponents nc and nb specify how the information load responds to volume and remain constitutive inputs.
'''+E(4)+E(5)+E(6)+'''
Pressure is the volume derivative at fixed state. Each component's comoving energy is proportional to a raised to its exponent, giving
'''+E(7)+'''
The choice nc=0 gives fixed comoving clustering energy and zero pressure. The choice nb=3 makes background energy proportional to physical volume, with pressure equal to minus its density. This version does not independently input w again. It also does not derive the microscopic origin of exponent 3. Constant density and negative pressure are exact consequences of the chosen volume dependence.

## Information evolution and total conservation

The same energy operator generates a lossless state update. Here ℓ is the lapse, set to 1 for calculation. The positive action scale A* sets the information clock and is not identified with Planck's constant. The present ω*/H₀=0.7 is also a disclosed test input.
'''+E(8)+'''
On the unitary orbit ρ=Uρ₀U†, trace, positivity and the state's eigenvalues are preserved. Cyclicity of the trace makes the state-change contribution to the instantaneous energy vanish. Its change is the work associated with volume variation.
'''+E(9)+'''
This does not make the information state stationary. Individual Jc and Jb may change. Noncommuting operators transfer energy between the internal sectors while their exchange sums to zero. Pure-state phases and mixed-state spectral accounting can therefore be used together with global expansion.

## Classical background action and expansion

Choose an isotropic flat average on a finite T³. Spatial identification and extra local gravity remain distinct. The classical background action is
'''+E(10)+'''
Couple the state-orbit action and phenotype load to the same lapse. The pressureless phenotype has fixed comoving energy Eφ,0.
'''+E(11)+'''
Varying the sum Sg+SI with respect to ℓ gives the Friedmann constraint; variation with respect to a gives the acceleration equation; and variation of U gives equation (8). Homogeneous state, energy, pressure and expansion consequently close in a single finite action.
'''+E(12)+'''
This is a minisuperspace action restricted to homogeneous degrees of freedom. It does not derive local photon transport, anisotropic stress, spatial perturbations or galactic backreaction in a full four-dimensional action. The Friedmann and continuity equations are established external mathematics [5]. The constitutive contribution here is the connection among weighted information load, state evolution, pressure and twist response.

Component continuity includes the state-dependent exchange, with χc=χ and χb=1−χ.
'''+E(13)+E(14)+'''
Expansion and accelerated expansion are distinct. For nc=0 and nb=3, acceleration occurs when the background load satisfies the stated inequality relative to phenotype and clustering load. It is not asserted that every twist or information state accelerates the universe.

## The same load in twist and local gravity

The entire hidden energy density determines the global twist rate. Only its clustering part supplies the local additional-attraction scale.
'''+E(15)+'''
The second relation rewrites the existing 0.5 calibration aT=cH√(fc/8) using the critical density. Changes in state therefore change uc and aT by actual calculation. The global H and instantaneous source fractions are not held inconsistently fixed under changing load.

The local response retains the calibrated function adopted in the earlier galactic-disk paper.
'''+E(16)+'''
The test source is a Plummer mass of 6×10¹⁰ solar masses with scale 3 kpc, and velocities are compared at 8.2 kpc. This is neither an observed galaxy's temporal history nor a new data fit. Under Φ=Ψ, the same acceleration supplies conditional lensing.
'''+E(17)+'''
The patch radius is R=200 kpc and the impact radius b=10 kpc. Exterior geometry and observer-lens-source distance factors are excluded. Microscopic derivation of the local response and verification of gravitational slip remain outside the completion claim.
'''+states('EN')+f'''
The uniform reference reproduces aT={C['aT0_m_s2']:.9e} m/s² and 207.510905 km/s. Its conditional lens deflection is 0.535586511 arcsec. These acceleration, rotation and lensing outputs agree with the recorded 0.5 results. The zero mode has no additional gravity; undefined fractions and uncomputed zero-load lensing are recorded as null.

## Finite boundaryless construction and geometric load

The representative T³ identification of the finite boundaryless paper is retained. Its reference length L₀ is unidentified and L=L₀a. At fixed positive stiffness, the quadratic loop-record aggregate obeys
'''+E(18)+E(19)+'''
For positive nonzero load, positive L₀ and finite a, volume is finite at each calculated instant and T³ has no boundary. This is an exact conditional identity of the chosen identification. It neither selects the actual universe's unique topology nor measures absolute cosmic length. A fixed volume upper bound over an indefinitely expanding future is not established.

For the uniform reference with nc=0 and nb=3, expansion and global twist record magnitude are
'''+E(20)+backgrounds('EN')+'''
Physical twist rate and global twist record magnitude evolve differently. The record magnitude is an aggregate computed from the load density and spatial size at the current state and scale; no independent law of temporal record accumulation has been calculated. Beyond the present, this global record magnitude can grow during expansion while the density-dependent physical twist rate declines. They are not combined into one scalar twist statement. The variable a is geometric scale; it is not automatically replaced by observed redshift before a twist photon-redshift kernel is derived.

![Figure 1 Expansion and twist calculated from one energy functional](results/expansion_twist.png){width=6.4in}

The start calculation attempted to express every background density with one fixed load kernel and failed the state-domain bound at a=0.5. The present version specifies the volume dependence of energy, so the physical load kernel itself depends on geometry.
'''+E(21)+'''
Trace-one normalization and state positivity are retained. The operator spectrum varies with a, and every calculated uniform reference state from a=0.5 to 2 lies within that spectrum. This resolves the start model's restriction by an explicit new constitutive choice.

## Executed noncommuting state evolution

Modes 8, 16 and 24 are superposed with equal weights. For commuting operators, phases evolve while mean loads stay constant. In the noncommuting test, both mean loads actually change.

Jc spans '''+f"{H['Jc_range'][0]:.6f} to {H['Jc_range'][1]:.6f}"+''' and Jb spans '''+f"{H['Jb_range'][0]:.6f} to {H['Jb_range'][1]:.6f}"+'''. These are calculated test results at ε=8 and the declared information clock. They follow from weighted states and geometry-dependent energy, rather than a change in normalized information count.

![Figure 2 Changing loads and cancelling internal stress exchange](results/state_exchange.png){width=6.4in}

The two sectors are not independently supplied by an external source. Equations (9) and (13) preserve their total. Directly calculated exchange sums nearly to zero, and an independent finite difference verifies total continuity.

## Verification and falsification

The state ODE is integrated in both directions with DOP853. An independent midpoint unitary exponential propagator starts from the same state and compares 320 and 640 steps. The noncommuting load error improves by approximately four at both endpoints, as expected for second-order convergence. A separate integration of the acceleration equation also checks endpoint state loads and time against integration using the H constraint.
'''+verifications('EN')+'''
Additional checks cover pressure from finite volume variation, simultaneous basis-change invariance, the combined zero-phenotype/zero-hidden-load boundary, and a zero-residual-background boundary. Negative operator coefficients, zero scale and a nonfinite information clock are rejected. These establish homogeneous numerical consistency; they are not a test of spatial sound speed, perturbation stability or observed lens fits.

Negative kernel eigenvalues or loss of trace/positivity reject the load model. A mismatch between pressure and volume variation, or noncancelling exchanges, invalidates the single-energy construction. An acceleration solution inconsistent with the Friedmann constraint requires revising the background link. Failure of motion and lensing under the same response requires revising the conditional matching or slip assumption.

## Constitutive choices and completion claim

The dependence of expansion on energy homogeneity is evaluated explicitly. For the uniform reference,
'''+E(22)+scans()+'''
Exponent 1 gives a w=−1/3 background associated with a fixed twist record and does not accelerate at the adopted calibration. Exponent 3 gives constant density and w=−1; the reference background has the ΛCDM expansion form. This identity is not presented as an independent observational prediction or microscopic proof of exponent 3. The result is a consistent pressure and dynamical calculation from the declared volume dependence of information energy.

| Claim | Status | Result in this version |
| --- | --- | --- |
| State-dependent information load | Executed within the chosen operators | Matrix trace agrees with mode calculation |
| State evolution pressure and conservation | Finite homogeneous construction and calculation | One energy functional and action |
| Expansion and twist together | Conditional background output | H records and twist rate calculated together |
| Information load to local gravity | Inherited calibrated matching | Rotation lensing and 0.5 reproduction |
| Finite boundaryless universe | Conditional chosen T3 construction | Length relation for load and loop record |
| Unique microscopic weights and exponents | Open | Disclosed constitutive choices |
| Four dimensional completion and spatial perturbations | Subsequent scope | Distinguished from the homogeneous action |

The 0.6 completion boundary is to calculate load from information states, close state evolution, pressure, expansion and twist with one energy functional and homogeneous action, and pass the same clustering load into the inherited local response. This version reaches that finite boundary. Symmetric-carrier selection gaps remain zero. Actual topology and length, lower-order filter origins, covariant local response and observational validation remain recorded physical questions.

## References and reproducibility

1. Choi W. Minimal Computation Cosmology MCC 2.3.2. 2026. Chapters 28–29 on global background and local stress accounting. https://doi.org/10.5281/zenodo.22733000.
2. Choi W. Twist Stress Universe and Dark Matter Mass Phenotypes. v1.0. 11 September 2026. https://doi.org/10.5281/zenodo.22700557.
3. Choi W. Dual Component Model of Mass Gravity and Spatial Twist Stress Gravity. v0.4. 27 September 2026. The individual original is used.
4. Choi W. WRRA Finite Boundaryless Universe. v1.0. 28 September 2026. The individual original is used.
5. Trodden M and Carroll SM. TASI Lectures Introduction to Cosmology. 2004. §2.2. arXiv:astro-ph/0401547. https://vo.ned.ipac.caltech.edu/level5/Sept03/Trodden/Trodden2_2.html.
6. Choi W. WRRA-M 0.5 Information Load and Twist Gravity in a Finite Model. 1 October 2026. Korean and English manuscripts with corrected computation.
7. Choi W. WRRA Spatial Twist Galactic Disk Plane Selection and Dark Mass Phenotypes. v1.0. 27 September 2026. https://doi.org/10.5281/zenodo.23003875.

The computation and both parameter files disclose calibrations, operators and clock. results.json records complete trajectories, summary.json the main outputs, and release_checks.json reproduction and boundary tests. verify.py compares the recorded 0.5 outputs. Both language sources are generated from the same equations and numerical ledger. Calculation needs numpy, scipy and matplotlib; native Word generation additionally needs pandoc and python-docx.

© 2026 Wonsik Choi. Manuscripts and calculations are distributed under CC BY 4.0.
'''

for lang,text in [('KO',ko),('EN',en)]:
    (ROOT/('source_'+lang.lower()+'.md')).write_text(text.replace('A*','A∗').replace('ω*','ω∗'))
print('wrote matched KO/EN sources with',len(EQ),'numbered equations')
