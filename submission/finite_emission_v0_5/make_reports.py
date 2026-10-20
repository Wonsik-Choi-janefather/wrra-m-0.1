from pathlib import Path
import json,subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;r=json.loads((P/'results/audit.json').read_text())
rows=r['convergence'];base=r['baseline'];first=r['first_event'];last=r['last_event']
fig,ax=plt.subplots(2,2,figsize=(9,6),layout='constrained')
import csv
events=list(csv.DictReader((P/'results/events.csv').open()))
t=[0]+[float(e['time']) for e in events]+[1]
C=[1]+[float(e['reservoir_after'])/r['verified_inputs']['beta'] for e in events]+[.5]
ax[0,0].step(t,C,where='post',label='Finite packets N=256')
tt=np.linspace(0,1,300);ax[0,0].plot(tt,2.**(-tt),'--',label='Smooth transfer')
ax[0,0].set(xlabel='Proper time / initial Hubble time',ylabel='Reservoir / beta');ax[0,0].legend(fontsize=8)
for cost in [0.,.01]:
    z=[x for x in rows if x['cost']==cost]
    ax[0,1].loglog([x['N'] for x in z],[x['M_relative_error'] for x in z],'o-',label=f'cost={cost}')
ax[0,1].set(xlabel='Packet resolution N',ylabel='Matter error vs smooth');ax[0,1].legend(fontsize=8)
z=r['seed_amplitude_scan'];ax[1,0].semilogx([x['delta'] for x in z],[x['entropy_slope'] for x in z],'o-')
ax[1,0].axhline(r['smooth_entropy_tangent'],ls='--',color='black',label='Smooth tangent')
ax[1,0].set(xlabel='Seed probe amplitude',ylabel='Entropy response at fixed N=256');ax[1,0].legend(fontsize=8)
z=np.load(P/'results/actual_seed_event_times.npz');shift=(z['event_times'][:,-1]-last['time'])*r['verified_inputs']['time_unit_seconds']*1e9
ax[1,1].plot(np.arange(128),shift,'.',ms=3)
ax[1,1].set(xlabel='Actual SOURCE cell',ylabel='Last-event time shift (ns, calibrated)')
for a in ax.flat:a.grid(alpha=.2)
fig.savefig(P/'emission_diagnostics.png',dpi=180);plt.close(fig)

equations=r'''
For a fixed reference cell use $8\pi G/3=1$, $a(0)=H(0)=1$,
$C=\rho_x a^4$, $J=\rho_{\rm record}a^4$, $M=\rho_m a^3$ and
$R=1-\beta+C+J$. The spectator photon and neutrino backgrounds are
unchanged. No perturbed free-streaming hierarchy is integrated in this study.

$$q=\beta/N_q,\quad C_0=\beta,\quad r_0=J_0=M_0=0,$$
$$\dot r=\Gamma(1+\xi)C\quad (0<T<1,\ Q=1),\qquad 0\le r<q.$$

The credit $r$ measures integrated transfer eligibility; it is not energy in
addition to $C$. The gate $Q=1$ requires an unused record token. When the gate
closes, credit accumulation pauses. A threshold exactly at $T=1$ is included;
subthreshold credit at the end is retained as inactive credit, never flushed.
The pulse remains inherited input, not an emergent prediction.

At the first threshold $r=q$, apply the complete atomic event:

$$C^+=C^--q,\quad r^+=r^--q,\quad
M^+=M^-+(1-\epsilon)q/a_j,\quad J^+=J^-+\epsilon q.$$

One record token is consumed. Thus the physical energy per reference cell is
$q/a_j$, split into matter $(1-\epsilon)q/a_j$ and record heat $\epsilon q/a_j$.
Neither the integer token nor the credit is counted as another energy store.
The chosen heat destination is perfect photon-like radiation; no temperature,
bit count, Landauer saturation or microscopic recording Hamiltonian is derived.

$$\Delta[(C+J)/a+M]=0,\quad
\dot{\ln a}=H,\quad
\dot H=-\tfrac12(4R/a^4+3M/a^3),\quad \dot W=HR/a.$$

$H$ and $a$ are continuous at each event; pressure and $\dot H$ can jump.
The independently evolved $H$ is checked against $H^2=R/a^4+M/a^3$;
$R/a+M+W=1$ is checked through the whole history. Local cell velocities are
zero, so momentum conservation here is trivial; it does not test nonzero-momentum
finite-gradient junctions.

Between events $C$ is constant, giving an exact event clock:

$$T_j=\frac{1}{\Gamma(1+\xi)}\sum_{m=0}^{j-1}\frac{1}{N_q-m}.$$

There are at most $N_q$ events, with positive spacing. Complete exhaustion
occurs at finite $T_{N_q}=H_{N_q}/[\Gamma(1+\xi)]$, if the pulse and gate allow.
This is a deterministic threshold closure, not a stochastic Born-rule derivation.
'''

numbers=f'''
| Quantity | Result |
|---|---:|
| Named automatic checks | {r['checks_passed']} passed |
| Initial reservoir beta | {r['verified_inputs']['beta']:.15g} |
| Baseline N / cost fraction | 256 / 0.01 |
| Events during inherited pulse | {base['count']} |
| First event, normalized proper time | {first['time']:.15g} |
| Last event, normalized proper time | {last['time']:.15g} |
| First / last event, inherited calibrated seconds | {first['time_seconds']:.12g} / {last['time_seconds']:.12g} |
| Maximum normalized event energy residual | {base['max_jump_balance_normalized']:.6g} |
| Maximum relative Friedmann residual | {base['max_Friedmann_relative']:.6g} |
| Maximum absolute energy + work error | {base['max_energy_plus_work_absolute']:.6g} |
| Independent root-clock time error | {r['independent_clock_max_error']:.6g} |
| Matter M, including record cost | {base['M']:.15g} |
| Record heat J | {base['J']:.15g} |
| Actual seed: cells / count in every cell | 128 / 128 |
| Largest actual-seed time shift, normalized time | {r['actual_seed']['max_time_shift']:.12g} |
| Actual-seed nonlinear log entropy RMS | {r['actual_seed']['entropy_log_RMS']:.12g} |

The seconds inherit the previous calibrated unit {r['verified_inputs']['time_unit_seconds']:.15g} s;
they are conditional outputs, not a new absolute-time measurement or a MeV chronology.
The check count includes per-cell repetitions and numerical consistency checks,
not {r['checks_passed']} independent physical confirmations.
'''
conv='| N | Matter relative error, zero cost | Matter relative error, 1% cost |\n|---|---:|---:|\n'
for n in [32,128,512,2048,8192]:
    z=[x for x in rows if x['N']==n];conv+=f"| {n} | {z[0]['M_relative_error']:.9g} | {z[1]['M_relative_error']:.9g} |\n"
amp='| Seed amplitude | Counts + / - | Fixed-N entropy slope |\n|---|---:|---:|\n'
for x in r['seed_amplitude_scan']:amp+=f"| {x['delta']:.6g} | {x['count_plus']} / {x['count_minus']} | {x['entropy_slope']:.12g} |\n"

ko=f'''# WRRA 유한 양자 방출 시각과 기록 비용

후속 계산 v0.5 · 최원식 · 최정인 · 독립연구자 · 2026-10-20

## 검증 입력 → WRRA 고유 변환 → 산출값 → 반증조건

**검증 입력.** v0.3/v0.4의 고정 잔여 예산, $\\Gamma=\\ln2$, 고유시간 펄스,
시간 환산값과 실제 128셀 SOURCE 씨앗을 유지한다. 방출 분해능 $N_q=256$,
기록 비용 비율 1%, 사건당 기록 토큰 한 개는 이번에 명시한 구성값이다.
이 값들을 관측으로 결정한 물리 상수라고 주장하지 않으며, 기존 물질 구성비를
다시 맞추는 보정도 수행하지 않는다. 기존 검증값을 이론 구성에 사용하는 것은
정당하며, 이번 독창성은 잔여-허가-유한 방출-기록 장부의 실행 연결에 있다.

**WRRA 고유 변환.** 저장된 잔여 자체와 중복되지 않는 방출 크레딧을 축적하고,
문턱과 기록 허가가 충족되는 최초 시각에 유한 패킷을 내보낸다. 방출 에너지는
물질과 기록 열로 분배하며, 팽창 중의 적색편이와 압력 일을 함께 계산한다.

**산출값.** 기준 셀에서 128회 방출한다. 실제 씨앗 128개 셀의 사건 시각과
출력 장부를 직접 계산했다. 미리 지정한 것은 방출 법칙과 단위이며 각 사건의
시각은 내부 계산 결과다. 세부 수치는 3쪽에 제시한다.

**반증조건.** 사건 에너지 보존, 양성, 기록 허가, 독립 시계, 시간 적분 정련,
유한 양자 축소에 따른 연속 전이 복원이 실패하면 구현 또는 법칙을 수정한다.
미시 입자종·양자역학적 방출 진폭·관측 우도는 이번 검증 대상에 포함하지 않는다.

## 판정

유한 방출 시점과 기록 에너지 이동을 실제 실행하는 국소 우주론 토이모형을
구현했다. v0.4의 유한 구배 방정식에 사건 점프를 삽입한 결과는 아니다.
이번 단계는 공유된 배경 동역학 위의 독립 셀 계산이며, 유한 구배 메트릭·운동량·
중성미자 상태의 사건 전후 접합은 다음 통합 단계로 남는다.

\\newpage

## 실행 규칙과 보존식

아래는 코드와 동일한 변수·사건 규칙이다. $q$는 기준 셀의 공변 복사 에너지
차감 단위로, 보편적 입자 에너지나 플랑크 양자의 도출을 의미하지 않는다.
영문 수식 설명을 포함해 재현 시 해석이 달라지지 않도록 제시한다.

{equations}

\\newpage

## 수치 결과와 수렴

{numbers}

{conv}

1% 비용 사례에서 물질량은 비용이 없는 같은 유한 양자 사례보다 약 1% 작다.
그 차이는 기록 열에 들어간다. 비용이 시계를 바꾸지 않는 것은 이번의 고정 공변
문턱·비용 분리 규칙에서 나온 결과이며 모든 기록 장치의 보편 법칙이 아니다.
홀수 분해능 및 다른 펄스 길이의 수렴도 별도로 검사했다.

\\newpage

## 작은 씨앗과 유한 양자: 이번에 확인한 구조

{amp}

연속 모형의 작은 씨앗 응답은 {r['smooth_entropy_tangent']:.12g}로 v0.3의
0.7235673850561154를 복원한다. 그러나 고정된 $N_q=256$에서는 작은 씨앗의
방출 개수가 같고 시각만 변하여 약 0.194689의 응답이 나온다. 방출은 빠르거나
늦게 일어나며, 그동안의 팽창 때문에 물질 장부가 달라진다. 실제 씨앗의 최대
방출 시각 이동은 환산하면 약 {r['actual_seed']['max_time_shift']*r['verified_inputs']['time_unit_seconds']*1e9:.4g} ns이다.
이 ns 값 역시 기존 시간 보정에 조건부다.

따라서 작은 씨앗 극한과 작은 양자 극한을 임의로 바꾸어 쓸 수 없다. 연속
응답을 회복하려면 대략 $q/\\beta\\ll|\\xi|$, 즉 씨앗 차이를 분해할 충분한
에너지 해상도가 필요하다. 이 부등식은 분해능 조건이며 자동 수렴 보증은 아니다.
고정 씨앗 0.01에서 $N_q=8192$의 연속 응답 차이는
{r['fixed_amplitude_convergence'][-1]['error_vs_smooth']:.6g}였다. 실제 $10^{{-8}}$ 수준
씨앗을 그 극한까지 분해하는 대규모 사건 계산은 수행하지 않았다.

## 오류 대조와 다음 단계

기록 열을 누락하면 사건당 정규화 에너지 오차가 0.01로 검출된다. 물질 수신의
적색편이 인자 $1/a_j$를 누락하면 최대 오차는
{r['negative_controls']['missing_redshift']['jump_balance']:.6g}다. 기록 용량 7개는
정확히 7회 후 정지하고, 허가 0은 에너지를 이동시키지 않는다. 음수 비용과
잘못된 방출 단위도 거부한다. 아직 다루지 않은 미시 생성률이나 운동량 접합의
성공을 이 검사로 대신 주장하지 않는다.

다음 단계는 (1) 입자종별 방출 단위와 기록 비용의 검증값 연결,
(2) v0.4 유한 구배 상태에 보존되는 사건 접합과 사건시각 섭동 적용,
(3) 씨앗-양자 해상도 조건을 유지하는 효율적인 사건 묶음 계산이다.
완전한 CAMB 주입, 새로운 CMB 스펙트럼, MeV 열역사는 이번 산출에 포함되지 않는다.

기준 문헌: Malik & Wands, Cosmological perturbations (2009), arXiv:0809.4944.
외부 문헌은 다중 유체·보존식의 검증 자료이며 유한 방출 규칙 자체를 대신하지 않는다.
선행 공개본: https://zenodo.org/records/23490141.
'''
en=f'''# Finite-Quantum Emission Timing and Recording Costs in WRRA

Working calculation v0.5 | Wonsik Choi and Jeongin Choi | Independent researchers | 20 October 2026

## Verified inputs → WRRA transformation → outputs → falsification

**Verified inputs.** Preserve the fixed v0.3/v0.4 reservoir beta, rate Gamma=ln2,
proper-time pulse, calibrated time unit and actual 128-cell SOURCE seed. Packet
resolution 256, recording cost 1% and one record token per event are new declared
closure parameters. They are not measured fundamental constants. No output
amplitude or matter ratio is refitted. Reproduction of known values is a valid
consistency achievement; the structural contribution is the executed connection
between residue, permission, finite emission and recording.

**WRRA transformation.** Accumulate transfer credit without double-counting
reservoir energy. Emit at the first eligible threshold, split each finite debit
between matter and record heat, consume a record token, and evolve expansion
and pressure work between events. Event times are computed from the closure,
not supplied as a list of fitted times.

**Outputs.** The baseline emits 128 packets. All actual SOURCE cells are evolved
with their own event clocks and expanding energy ledgers. Detailed values and
the finite-packet/small-seed distinction follow below.

**Falsification.** Reject or revise a closure/implementation failing event energy
balance, positivity, permission, independent event roots, time refinement or
the fixed-amplitude small-packet continuum limit. These are computational
tests, not microscopic particle identification or observational likelihood tests.

## Assessment and scope

An executable local cosmological toy model now computes finite emission times
and recording-energy transfer. It shares the inherited background with v0.4;
it does not insert finite jumps into the v0.4 finite-k metric, momentum and
neutrino hierarchy. Independent local FLRW cells are the executed spatial
approximation. Full finite-gradient event matching remains a subsequent task.
The closure is deterministic; quantum mechanical amplitudes, a universal
particle energy quantum and a microscopic recording Hamiltonian are not derived.

\\newpage

## Executed equations and event clock

{equations}

\\newpage

## Numerical outputs and continuum recovery

{numbers}

{conv}

The 1% branch yields approximately 1% less matter than the zero-cost packet
branch, with the energy retained in record heat. Its event clock is unchanged
because this chosen credit rule depends on C, not the cost destination. That is
a branch-specific result. Odd N and a different pulse length are also checked
to avoid relying on the exact half-inventory special case.

\\newpage

## Finite packets resolve timing before tiny count differences

{amp}

The smooth entropy tangent {r['smooth_entropy_tangent']:.12g} reproduces
v0.3's 0.7235673850561154. At fixed N=256 tiny seeds leave the event count
unchanged, giving a different response near 0.194689 through redshift-sensitive
timing. The maximum actual-seed time shift is approximately
{r['actual_seed']['max_time_shift']*r['verified_inputs']['time_unit_seconds']*1e9:.4g} calibrated ns.
The reported entropy is the nonlinear species contrast
$\\ln(M_j/M_0)-3\\ln(R_j/R_0)/4$, with the local scale-factor terms canceling.
It is a zero-gradient contrast, not a new finite-k spectrum.

The small-seed and small-packet limits cannot be interchanged without a
resolution condition. Roughly $q/\\beta\\ll|\\xi|$ is needed to resolve count
differences; this is not by itself a convergence guarantee. At fixed seed 0.01,
N=8192 gives an entropy-slope error of
{r['fixed_amplitude_convergence'][-1]['error_vs_smooth']:.6g} against the smooth
finite-amplitude comparison. No claim is made that the actual 1e-8 seed has
been resolved to that limit.

## Rejecting controls and next integration

Omitting record heat gives a normalized per-event energy defect 0.01. Omitting
the recipient redshift factor produces a maximum defect
{r['negative_controls']['missing_redshift']['jump_balance']:.6g}. Capacity 7 allows
exactly 7 events; zero permission permits no energy transfer. Invalid cost,
rate and packet parameters are rejected.

Next: connect packet/cost values to verified microscopic inputs; implement
conserving jumps and event-time perturbations in the complete v0.4 finite-k
state; accelerate event bundles while retaining the seed/packet resolution
condition. Complete CAMB injection, new CMB spectra, particle-specific
production and MeV thermal history remain separate work.

Reference: Malik & Wands, Cosmological perturbations (2009), arXiv:0809.4944,
used for conservation and multi-fluid context. The event rule is the present
explicit closure, not imported quantum dynamics. Predecessor:
https://zenodo.org/records/23490141.
'''
equations_ko=r'''
기준 셀에서 $8\pi G/3=1$, $a(0)=H(0)=1$로 두고,
$C=\rho_xa^4$, $J=\rho_{\rm record}a^4$, $M=\rho_ma^3$,
$R=1-\beta+C+J$를 사용한다. 기존 광자·중성미자 배경은 유지하되,
이번에는 섭동된 자유비행 계층을 적분하지 않는다.

$$q=\beta/N_q,\quad C_0=\beta,\quad r_0=J_0=M_0=0,$$
$$\dot r=\Gamma(1+\xi)C\quad (0<T<1,\ Q=1),\qquad 0\le r<q.$$

$r$은 방출 가능량의 누적 크레딧이다. 저장 에너지 $C$에 더하는 별도 에너지가
아니다. 미사용 기록 토큰이 있어야 $Q=1$이다. 허가가 닫히면 크레딧 축적도
정지한다. 펄스 종료 시각에 정확히 문턱에 도달하면 방출하고, 문턱 미만 잔여는
비활성 크레딧으로 보존한다. 펄스 길이 자체는 기존 입력이다.

최초 문턱 $r=q$에서 다음 갱신을 하나의 사건으로 실행한다.

$$C^+=C^--q,\quad r^+=r^--q,\quad
M^+=M^-+(1-\epsilon)q/a_j,\quad J^+=J^-+\epsilon q.$$

기록 토큰 한 개를 소비한다. 기준 셀의 물리적 에너지 $q/a_j$는 물질의
$(1-\epsilon)q/a_j$와 기록 열의 $\epsilon q/a_j$로 나뉜다. 정수 토큰과
크레딧을 에너지에 중복 산입하지 않는다. 열의 수신 성분은 완전유체 광자형
복사로 지정한다. 온도·비트 수·란다우어 한계 포화·미시 기록 해밀토니안은
이번에 도출하지 않았다.

$$\Delta[(C+J)/a+M]=0,\quad
\dot{\ln a}=H,\quad
\dot H=-\tfrac12(4R/a^4+3M/a^3),\quad \dot W=HR/a.$$

사건 전후 $a,H$는 연속이고, 압력과 $\dot H$는 바뀔 수 있다. 독립적으로
적분한 $H$에 대해 $H^2=R/a^4+M/a^3$를 검사하고, 전체 이력에서
$R/a+M+W=1$을 검사한다. 국소 셀의 속도는 0이므로 운동량 보존은 자명한
경우이며, 비영 운동량의 유한 구배 접합 검증을 대신하지 않는다.

사건 사이 $C$가 일정하므로 방출 시각은 정확히 다음과 같다.

$$T_j=\frac{1}{\Gamma(1+\xi)}\sum_{m=0}^{j-1}\frac{1}{N_q-m}.$$

사건 수는 최대 $N_q$이며 간격은 양수다. 펄스와 허가가 충분하면
$T_{N_q}=H_{N_q}/[\Gamma(1+\xi)]$에서 잔여가 소진된다. 여기서
$H_{N_q}$는 조화수다. 이 규칙은 결정론적 문턱 모형이며 양자 확률의 도출은 아니다.
'''
numbers_ko=numbers
labels={'Quantity':'항목','Result':'결과','Named automatic checks':'이름 있는 자동 검사',
'Initial reservoir beta':'초기 잔여 예산 beta','Baseline N / cost fraction':'기준 N / 비용 비율',
'Events during inherited pulse':'기존 펄스 동안 방출 수','First event, normalized proper time':'첫 방출, 정규화 고유시간',
'Last event, normalized proper time':'마지막 방출, 정규화 고유시간',
'First / last event, inherited calibrated seconds':'첫 / 마지막 방출, 기존 보정 초',
'Maximum normalized event energy residual':'최대 정규화 사건 에너지 오차',
'Maximum relative Friedmann residual':'최대 상대 프리드만 오차',
'Maximum absolute energy + work error':'최대 절대 에너지 + 일 오차',
'Independent root-clock time error':'독립 문턱 적분 시각 오차',
'Matter M, including record cost':'기록 비용 포함 물질 M','Record heat J':'기록 열 J',
'Actual seed: cells / count in every cell':'실제 씨앗: 셀 수 / 각 셀 방출 수',
'Largest actual-seed time shift, normalized time':'실제 씨앗의 최대 정규화 시각 이동',
'Actual-seed nonlinear log entropy RMS':'실제 씨앗의 비선형 로그 엔트로피 RMS','passed':'통과'}
for a,b in labels.items():numbers_ko=numbers_ko.replace(a,b)
numbers_ko=numbers_ko[:numbers_ko.index('The seconds')]+f'''초 단위는 기존 보정값 {r['verified_inputs']['time_unit_seconds']:.15g} s를 물려받는다.
독립적인 절대시간 측정이나 MeV 연대기가 아니다. 검사 수에는 셀별 반복과
수치적 정합성 검사가 포함되며, 서로 독립적인 물리 검증 {r['checks_passed']}개를 뜻하지 않는다.
'''
ko=ko.replace(equations,equations_ko).replace(numbers,numbers_ko)
ko=ko.replace('영문 수식 설명을 포함해 재현 시 해석이 달라지지 않도록 제시한다.','재현에 필요한 문턱·수신 성분·시간 경계 조건을 함께 명시한다.')
ko+=r'''
\newpage

## 계산 진단 그림

![잔여의 계단형 방출, 연속 극한 수렴, 씨앗 분해능과 실제 128셀의 방출 시각 이동.](emission_diagnostics.png)

왼쪽 위는 잔여 장부, 오른쪽 위는 양자 분해능 정련이다. 왼쪽 아래는 고정 양자에서
씨앗 크기를 줄일 때 연속 응답과 다른 평탄 구간이 생기는 모습이다. 오른쪽 아래는
실제 씨앗에 따른 마지막 방출 시각 차이이며, 초 환산은 기존 보정값에 조건부다.
'''
en+=r'''
\newpage

## Numerical diagnostics

![Staircase reservoir, smooth-limit refinement, finite-seed resolution and event-time shifts across all 128 actual SOURCE cells.](emission_diagnostics.png)

The lower-left plateau exposes the distinction between the fixed-packet small-seed
response and the smooth tangent. The lower-right ns scale inherits the calibrated
time unit and is a conditional timing output.
'''
for lang,body in [('KO',ko),('EN',en)]:
    name=f'WRRA_Finite_Emission_v0_5_{lang}'
    (P/(name+'.txt')).write_text(body)
    subprocess.run(['pandoc',str(P/(name+'.txt')),'-f','markdown','--resource-path='+str(P),'--pdf-engine=xelatex',
        '-V','mainfont=Noto Sans CJK KR','-V','geometry:margin=19mm',
        '-V','fontsize=10pt','-V','colorlinks=true','-o',str(P/(name+'.pdf'))],check=True)
print('Reports built')
