from pathlib import Path
import json,csv,subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
r=json.loads((P/'results/lensing_likelihood.json').read_text());t=json.loads((P/'results/thermal.json').read_text())
a=json.loads((P/'results/audit.json').read_text());z=np.load(P/'results/lensing_band_predictions.npz')
lin=np.load(P/'results/linear.npz');nl=np.load(P/'results/nonlinear.npz')
history=list(csv.DictReader((P/'results/thermal_history.csv').open()))
clock=np.array([float(x['time_from_start_s']) for x in history]);tg=np.array([float(x['Tgamma_MeV']) for x in history]);tn=np.array([float(x['Tnu_MeV']) for x in history]);sel=clock>0
fig,ax=plt.subplots(2,2,figsize=(9.4,6.5),layout='constrained')
ax[0,0].errorbar(z['L'],z['data']*1e7,np.sqrt(np.diag(z['covariance']))*1e7,fmt='o',ms=3,label='Released SPT-Planck data')
ax[0,0].plot(z['L'],z['predictions'][0]*1e7,'--',label='Linear-lensing completion')
ax[0,0].plot(z['L'],z['predictions'][1]*1e7,'-',label='HMCode completion')
ax[0,0].set(xlabel='Lensing multipole L',ylabel='Corrected PP bandpower x 1e7');ax[0,0].legend(fontsize=7)
ell=nl['ell'];ii=(ell>=50)&(ell<=2000)
ax[0,1].plot(ell[ii],100*(nl['clpp'][ii]/lin['clpp'][ii]-1))
ax[0,1].set(xlabel='Lensing multipole L',ylabel='Nonlinear change in C_phi_phi (%)')
ax[1,0].loglog(clock[sel],tg[sel],label='Photon + e+- temperature')
ax[1,0].loglog(clock[sel],tn[sel],'--',label='Free-streaming neutrino temperature')
ax[1,0].set(xlabel='Elapsed seconds from pulse start',ylabel='Temperature (MeV)');ax[1,0].legend(fontsize=7)
ax[1,1].semilogx(tg,[float(x['g_s_em']) for x in history],label='EM entropy degrees g_s')
ax[1,1].semilogx(tg,[float(x['g_rho']) for x in history],label='Thermal energy degrees g_rho')
ax[1,1].set(xlabel='Photon temperature (MeV)',ylabel='Effective thermal degrees');ax[1,1].legend(fontsize=7)
for x in ax.flat:x.grid(alpha=.2)
fig.savefig(P/'observation_diagnostics.png',dpi=180);plt.close(fig)

like_table='| Case | chi-square, 18 bins | Profile A_phi | Profile sigma |\n|---|---:|---:|---:|\n'
for q in r['models']:
 like_table+=f"| {q['name']} | {q['chi2']:.9f} | {q['amplitude_profile']['A_phi_profile']:.9f} | {q['amplitude_profile']['sigma_A']:.9f} |\n"
thermal_table='| Photon T (MeV) | Elapsed seconds | Relative scale factor | Neutrino T (MeV) |\n|---|---:|---:|---:|\n'
for q in t['milestones']:
 thermal_table+=f"| {q['Tgamma_MeV']:.3g} | {q['time_from_start_s']:.9g} | {q['a_relative']:.9g} | {q['Tnu_MeV']:.9g} |\n"
like_eq=r'''
$$D_L^{\phi\phi}=\frac{[L(L+1)]^2}{2\pi}C_L^{\phi\phi},\qquad
D_\ell^{TT}=\frac{\ell(\ell+1)}{2\pi}C_\ell^{TT}\quad[\mu{\rm K}^2],$$
$$b_i=\sum_L(W_{iL}+R^{PP}_{iL})D_L^{\phi\phi}
+\sum_\ell R^{TT}_{i\ell}D_\ell^{TT}-f_i,$$
$$\chi^2=(b-d)^T\Sigma^{-1}(b-d),\qquad
\log\mathcal L=-\frac12[\chi^2+\log|\Sigma|+18\log(2\pi)].$$
'''
thermal_eq=r'''
$$\rho_{e^\pm}=\frac4{2\pi^2}\int_0^{\infty}
\frac{p^2\sqrt{p^2+m_e^2}}{\exp(\sqrt{p^2+m_e^2}/T_\gamma)+1}\,dp,$$
$$p_{e^\pm}=\frac4{6\pi^2}\int_0^{\infty}
\frac{p^4}{\sqrt{p^2+m_e^2}[\exp(\sqrt{p^2+m_e^2}/T_\gamma)+1]}\,dp.$$

$$\rho_\gamma=\pi^2T_\gamma^4/15,\quad
\rho_\nu=(7/8)(2N_{\rm eff})\pi^2T_\nu^4/30,\quad
s_{\rm em}=(\rho_{\rm em}+p_{\rm em})/T_\gamma,$$
$$H=\frac{\sqrt{8\pi\rho_{\rm tot}/3}}{M_{\rm Pl}\hbar},\quad
\dot T_\gamma=-\frac{3H(\rho_{\rm em}+p_{\rm em})}{d\rho_{\rm em}/dT_\gamma},\quad
T_\nu\propto a^{-1}.$$
'''
ko=f'''# WRRA 비선형 렌징 우도와 MeV 열역사 보강

작업 계산 v0.6 · 최원식 · 최정인 · 독립연구자 · 2026-10-20

## 검증 입력 → WRRA 고유 변환 → 산출값 → 반증조건

**검증 입력.** 기존 WRRA 주소-배경 변환의 dark_weight_only 배경값
$H_0=67.2568374662$, $\\omega_b=0.02239580679$, $\\omega_c=0.12037806177$를
유지한다. 초기요동의 $A_s=2.1\\times10^{{-9}}$, $n_s=0.9649$, 광학깊이
$\\tau=0.0544$, $N_{{\\rm eff}}=3.044$, $T_{{\\rm CMB}}=2.7255$ K는 명시한
검증·보정 입력이다. SPT-Planck 공개 렌징 자료 18구간의 공분산·창함수·응답 보정을
사용한다. 열역사는 v0.5의 고정 잔여 예산·256 분해능·128회 방출·1% 기록 비용을
물려받고, 유한 전자 질량의 평형 열역학을 추가한다.

**WRRA 고유 변환.** WRRA에서 산출한 배경을 명시적 초기요동 완성 조건과 함께
CAMB에 넣어 새로운 전송·렌징 계산을 수행한다. 별도의 열역사 모듈에서는 잔여
방출의 물질·기록 열 이동을 온도·팽창·압력 일에 직접 연결한다. 외부 계산법의
차용과 WRRA 내부에서 실제 실행한 연결을 구분한다.

**산출값.** 비선형 보정이 있는 고정 조건의 18구간 $\\chi^2$는
{r['models'][1]['chi2']:.6f}이다. 초기 온도는 {t['Tinitial_MeV']:.9f} MeV,
기존 시간 단위를 유지하며 오늘의 광자 엔트로피에 연결한 초기 축척은
{t['a_initial_derived']:.12g}이다. {a['checks_passed']}개 검사를 통과했고, 별도
폴더 재실행에서 과학적 수치·CSV·배열이 정확히 일치했다.

**반증조건.** 공분산·규격화·응답 보정 오류, 공식 코드와의 불일치, 적분·표 정련
실패, 열역학 보존 위반 또는 미주입 상태를 통합 완료로 표시하는 경우를 거부한다.

## 이번 단계의 판정

관측 우도와 MeV 열역사 계산 모듈은 실행되었다. 이는 WRRA 배경과 명시한 초기요동
완성 조건의 조건부 관측 평가다. v0.4의 전체 메트릭·속도·중성미자 상태 및 v0.5의
방출시각 섭동을 CAMB에 직접 주입한 전체 모형 검증은 아직 수행하지 않았다.
3번의 모든 접합이 완료되었다고 판정하지 않는다. 검증값의 사용은 정당한 이론
구성이며, 이번 계산의 성과는 실제 구조 연결과 재현 가능한 산출에 있다.

\\newpage

## 실제 관측 우도와 비선형 렌징

CAMB 2.0.4로 선형, HMCode 2020 비선형, 기존 비가중 배경의 비선형, 정확도
1.5배 정련 사례를 새로 계산했다. 전송과 초기요동은 이 단계에서 표준 아디아바틱
완성 조건을 사용한다. HMCode는 외부에서 검증된 경험적 비선형 처방으로 차용하며,
WRRA 유한 SOURCE에 대해 독자적으로 도출·검증된 처방으로 부르지 않는다.

{like_eq}

$W,R,f,\\Sigma$는 공개 자료에서 읽는다. 공분산을 대각 오차막대로 대체하지
않았다. TT 응답 보정에는 각 사례의 계산된 렌징 TT를 넣는다. 전체 18구간에서
이 고정 모형들을 평가하며, 우주론 매개변수 MCMC를 수행하지 않는다.

{like_table}

$A_\\phi$는 스펙트럼 모양을 고정한 진단용 렌징 진폭 적합이다. WRRA가 도출한
상수나 새 $A_s$ 보정으로 해석하지 않는다. 표의 고정 모형 $\\chi^2$는 이 진폭을
적합하기 전 값이다. 비가중 사례와의 차이가 작으므로 이 자료만으로 배경 분기를
선별했다고 주장하지 않는다.

공식 CosmoMC의 별도 구현과 최대 차이는
{max(x['official_reference_difference'] for x in r['models']):.6g}이다. 정련에 따른
밴드 예측 변화의 공분산 거리는 {r['numerical_refinement_distance_sigma']:.6g}
표준편차다. 렌징 신호를 0으로 놓는 거부 대조는 $\\chi^2={r['null_lensing']['chi2']:.6f}$다.
이 대조는 해당 관측자료의 렌징 검출을 확인하며, 전체 WRRA 구조의 독립 확증을
뜻하지 않는다. $p$값을 이론이 참일 확률로 바꾸어 읽지 않는다.

\\newpage

## 유한 방출을 연결한 MeV 열역사

전자·양전자 화학퍼텐셜은 0으로 두고 유한 질량 적분을 직접 계산한다. 가우스
구적과 온도 표를 정련하고, 열용량은 독립 유한차분으로 확인한다. 아래 식은
자연단위 MeV를 쓰며, $H$에 $\\hbar$를 복원해 초 단위와 연결한다.

{thermal_eq}

중성미자는 상대론적 순간 탈결합의 엔트로피 분기를 사용한다.
$N_{{\\rm eff}}=3.044$는 이미 검증된 유효 에너지 입력이다. 이 수를 충돌 적분으로
새롭게 도출했다고 주장하지 않는다. 기록 열은 사건 시점에 전자·광자 열탕의
에너지를 올리고 새 온도를 풀어 갱신한다. 비열이 달라지므로 단순히 $J/a^4$를
추가하는 것과 구분된다. 잔여 에너지와 물질 수신은 같은 사건에서 보존한다.

{thermal_table}

표의 시간은 방출 시작 후 경과 시간이다. 우주 시작 이후의 절대 나이가 아니다.
초기 $H={t['Hinitial_s_inverse']:.12g}$ s$^{{-1}}$를 유지하면
$T_{{\\gamma,i}}={t['Tinitial_MeV']:.12g}$ MeV다. 이후 비표준 광자 엔트로피
생성이 없다는 연결 조건에서 $a_i={t['a_initial_derived']:.12g}$가 나온다.
기존 $10^{{-10}}$보다 약 {abs(t['a_initial_relative_change'])*100:.5f}% 작다.
따라서 기존 시간 단위·초기 축척·열입자 내용을 모두 그대로 둔 채 MeV 연대기만
붙일 수는 없다. 이것은 모형의 물리적 단위 보정 과제로 드러난 결과다.

\\newpage

## 보존·재현·통합 경계

열역사 전체의 에너지와 압력 일의 최대 오차는
{t['max_energy_work_residual']:.6g}이며, 개별 사건의 작은 열 변화량을 실제
온도 차이로 재구성한 상대 오차는 {t['max_event_balance_relative']:.6g}다.
두 수치는 정규화가 다르다. 후자는 큰 열탕에 대한 작은 방출량의 부동소수점
차분 영향을 포함하며, v0.5의 대수적 전달 장부 오차와 동일한 양이 아니다.
온도 표·구적·시간 정련 시 주요 결과의 최대 상대 변화는
{max(t['refinement'].values()):.6g}이다. 기록 열에 따른 전자·광자 엔트로피 증가는
양수다. 이는 전체 우주 엔트로피의 완전한 미시적 증명을 의미하지 않는다.

전체 상태 접합 검사에서는 64개 모드 모두 비영 물질 속도를 보유하며, 모드당
13개 중성미자 다중극이 저장되어 있음을 확인했다. 현재 CAMB 실행은 이 상태를
읽지 않고 아디아바틱 초기조건을 사용한다. 따라서 전체 상태 주입 표시는 차단된다.

후속 통합에 필요한 실제 작업은 다음과 같다.

1. CAMB 변수와 CDM 기준계로의 게이지 변환을 명시하고 검사한다.
2. 바리온·광자 강결합과 질량 있는 중성미자 상태를 같은 배경에서 완성한다.
3. 이번 열역사가 요구한 물리적 축척 보정을 유한 파수와 방출시각 접합에 반영한다.
4. 유한 공간 씨앗의 각·통계적 완성 조건을 고정한 뒤 전체 초기상태를 주입한다.
5. 그 결과에 현재 우도를 적용하고 CMB·BAO·BBN 공동 후방분포로 확장한다.

현재는 약한 상호작용 탈결합률·중성미자 맛 수송·핵반응망·BBN 원소비를 계산하지
않았다. 관측 입력에 맞춰 모형을 조정하는 것은 허용되는 구성 작업이지만, 그 조정과
고정 이후의 산출은 별도로 기록해야 한다.

참고·감사: NASA LAMBDA의 SPT-Planck 자료와 연구진; Simard et al.,
arXiv:1712.07541; Omori et al., arXiv:1705.00743; CAMB; Mead et al.,
arXiv:2009.01858; Anthony Lewis의 CosmoMC 우도 형식; PDG 2025 Big-Bang
Cosmology, https://pdg.lbl.gov/2025/reviews/rpp2025-rev-bbang-cosmology.pdf.
정확한 자료 URL·버전·해시는 PROVENANCE.json에 고정했다.

\\newpage

## 계산 진단

![관측 밴드와 조건부 예측, 비선형 렌징 변화, MeV 온도 이력과 열역학 자유도.](observation_diagnostics.png)

렌징 그래프는 WRRA 배경과 명시한 보정 초기요동의 조건부 계산이다. 열역사는
별도의 국소 방출 모듈이다. 두 모듈이 같은 전체 초기상태로 접합되었다는 뜻은 아니다.
'''
en=f'''# Nonlinear Lensing Likelihood and MeV Thermal Completion in WRRA

Working calculation v0.6 | Wonsik Choi and Jeongin Choi | Independent researchers | 20 October 2026

## Verified inputs → WRRA transformation → outputs → falsification

**Verified inputs.** Retain the WRRA address-to-background dark_weight_only branch:
H0=67.2568374662, omega_b=0.02239580679, omega_c=0.12037806177.
Declare calibrated adiabatic As=2.1e-9, ns=0.9649, tau=0.0544, N_eff=3.044 and
T_CMB=2.7255 K. Use the released 18-bin SPT-Planck covariance, windows and
response corrections. The separate thermal module retains the v0.5 packet
budget, N=256, 128 events and 1% record cost, and adds finite-mass equilibrium
electron/positron thermodynamics. Known verified inputs are legitimate model
construction inputs; their adoption does not constitute a new derivation.

**WRRA transformation.** Execute new CAMB transfer/lensing calculations with the
WRRA-derived background and explicit primordial completion. Separately connect
the residue-to-matter and record-heat event ledger directly to temperature,
expansion and pressure work. Adopted external methods are distinguished from
the connections actually executed in this calculation.

**Outputs.** The nonlinear fixed model gives chi-square={r['models'][1]['chi2']:.9f}
over 18 bins. Initial photon temperature is {t['Tinitial_MeV']:.12g} MeV;
the entropy-connected physical initial scale is {t['a_initial_derived']:.12g}
when the old time unit is retained. All {a['checks_passed']} checks pass; a clean
folder repeat reproduces scientific JSON, CSV and arrays exactly.

**Falsification.** Reject covariance/normalization/response errors, failed
official-code crosschecks, failed time/EOS refinement or conservation, and
claims of complete state integration when the initial-state gate is blocked.

## Assessment

The statistical and MeV thermal modules are implemented. Their existence is
not completion of the entire Step 3 integration. The lensing result is conditional
on the declared adiabatic completion. Full v0.4 metric/velocity/neutrino states
and v0.5 event-time perturbations are not injected into these CAMB runs.

\\newpage

## Released-data likelihood and new nonlinear spectra

Four new CAMB 2.0.4 runs compare linear lensing, HMCode 2020 nonlinear lensing,
an inherited unweighted-background nonlinear control, and a 1.5-accuracy
refinement. HMCode is an adopted empirical prescription, not a nonlinear law
derived or validated specifically for the finite WRRA SOURCE.

{like_eq}

Read W, R, f and Sigma from the released package. Use computed lensed TT in
the TT response correction. Do not replace the covariance with plotting errors.
All cosmological parameters in this comparison are fixed; no joint MCMC is run.

{like_table}

The profiled A_phi is a diagnostic lensing-amplitude fit at fixed shape, not
a WRRA-derived constant or a new As calibration. Listed fixed-model chi-square
values are before that fit. The background branches are too similar in this
comparison to claim selection of one branch by these data alone.

The largest difference from the separate official CosmoMC implementation is
{max(x['official_reference_difference'] for x in r['models']):.6g}. Only NumPy
2 type aliases are changed in memory for compatibility. The covariance-norm
distance under accuracy refinement is {r['numerical_refinement_distance_sigma']:.6g}
sigma. A zero-lensing control gives chi-square={r['null_lensing']['chi2']:.9f}.
That control verifies sensitivity to the observed lensing signal; it is not
independent confirmation of the complete WRRA structure. A tail probability
must not be interpreted as the probability that the theory is true.

\\newpage

## Finite-packet thermal completion

At zero electron chemical potential, directly integrate the massive ideal
Fermi gas. Refine quadrature and interpolation and independently differentiate
the energy density to check heat capacity. Energy densities use natural MeV
units; restore hbar to obtain H in inverse seconds.

{thermal_eq}

Use the relativistic instantaneous-decoupling entropy branch for the neutrino
temperature ratio. N_eff=3.044 is an effective energy input, not a collision-
integral result. At each event, add record heat to the electromagnetic energy
density and solve for the new photon/electron temperature. Keep the paired
reservoir debit and matter credit in the same event. This differs from simply
adding an always-radiative J/a^4 term when electrons become nonrelativistic.

{thermal_table}

Times are elapsed from the pulse start, not cosmic age. Keeping initial
H={t['Hinitial_s_inverse']:.12g} /s gives T_initial={t['Tinitial_MeV']:.12g} MeV.
Assuming no later non-standard photon entropy production, today's photon
temperature implies a_initial={t['a_initial_derived']:.12g}, about
{abs(t['a_initial_relative_change'])*100:.5f}% below the old 1e-10. Thus the old
clock, physical scale and particle content cannot all remain fixed while merely
attaching a MeV label. This identifies a physical normalization revision.

\\newpage

## Conservation, reproduction and integration boundary

Maximum total energy-plus-pressure-work error is
{t['max_energy_work_residual']:.6g}. Reconstructing a small event heat increment
from actual rounded temperatures gives a per-packet relative residual of
{t['max_event_balance_relative']:.6g}. These use different normalizations; the
latter includes subtractive roundoff of a tiny injection into a large thermal
bath and is not the v0.5 algebraic ledger residual. The largest refinement
change in the reported key thermal quantities is
{max(t['refinement'].values()):.6g}. Record heat increases electromagnetic
comoving entropy. No complete microscopic total-universe entropy proof is claimed.

All 64 retained matched modes have nonzero matter velocity and 13 saved
neutrino multipoles per mode. The current CAMB runs use adiabatic initial
conditions, not these states. The complete-injection label is therefore blocked.
Necessary subsequent work is concrete:

1. Transform the complete state to CAMB variables and the CDM reference frame.
2. Complete baryon/photon tight coupling and massive-neutrino states on the same background.
3. Propagate the thermal scale revision into finite k and conserved event-time junctions.
4. Fix the angular/statistical completion of the finite spatial seed, then inject all states.
5. Apply this likelihood to that result and extend to joint CMB/BAO/BBN posteriors.

Weak decoupling rates, flavor transport, the nuclear reaction network and BBN
abundances are not computed here. Calibration with verified inputs is valid;
calibration choices and outputs after fixing those choices must remain distinct.

Acknowledgments/references: NASA LAMBDA, SPT and Planck; Simard et al.,
arXiv:1712.07541; Omori et al., arXiv:1705.00743; CAMB; Mead et al.,
arXiv:2009.01858; Anthony Lewis's CosmoMC likelihood format; PDG 2025
Big-Bang Cosmology, https://pdg.lbl.gov/2025/reviews/rpp2025-rev-bbang-cosmology.pdf.
Exact data URLs, code versions and SHA256 values are fixed in PROVENANCE.json.

\\newpage

## Numerical diagnostics

![Released bandpowers and conditional predictions, nonlinear corrections, MeV temperature history and thermal degrees of freedom.](observation_diagnostics.png)

The lensing panel uses the WRRA background plus the calibrated adiabatic
completion. Thermal history is a separate local event module. These figures
do not assert a common full-state injection between the two modules.
'''
for lang,body in [('KO',ko),('EN',en)]:
    name='WRRA_Observation_Thermal_v0_6_'+lang
    (P/(name+'.txt')).write_text(body)
    subprocess.run(['pandoc',str(P/(name+'.txt')),'-f','markdown','--resource-path='+str(P),
        '--pdf-engine=xelatex','-V','mainfont=Noto Sans CJK KR','-V','geometry:margin=19mm',
        '-V','fontsize=10pt','-V','colorlinks=true','-o',str(P/(name+'.pdf'))],check=True)
print('Reports built')
