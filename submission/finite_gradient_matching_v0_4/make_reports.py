from pathlib import Path
import json,subprocess,os,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

P=Path(__file__).resolve().parent;r=json.loads((P/'results/audit.json').read_text())
rows=r['physical_modes'];stress=r['stress_cases'];neg=r['negative_controls'][0]['audit']
fig,ax=plt.subplots(2,2,figsize=(10,7),layout='constrained')
n=np.array([x['mode'] for x in rows]);e=np.array([abs(x['entropy_relative_to_v03']) for x in rows])
ax[0,0].loglog(n,e,'o-',ms=3);ax[0,0].set(xlabel='Original mode n',ylabel='|S(k)/S(v0.3) - 1|',title='All 64 modes actually evolved')
x=np.array([q['k_over_aH'] for q in stress]);eta=np.array([q['eta'] for q in stress]);delta=np.array([q['perfect_fluid_eta_difference'] for q in stress])
ax[0,1].semilogx(x,abs(delta/eta),'o-');ax[0,1].set(xlabel='k/(aH) at matching',ylabel='|eta(perfect fluid)/eta(free stream) - 1|',title='Stress tests of neutrino anisotropic stress')
keys=['Hamiltonian_residual','trace_residual','energy_residual','momentum_residual'];xx=np.arange(4)
ax[1,0].bar(xx-.17,[r['max_physical_constraint_residuals'][s] for s in keys],width=.34,label='Conserving model')
ax[1,0].bar(xx+.17,[neg[s]['normalized'] for s in keys],width=.34,label='Missing recipient momentum')
ax[1,0].set(yscale='log',ylabel='Declared normalized residual',title='Energy alone does not test momentum')
ax[1,0].set_xticks(xx,['00','trace','energy','momentum']);ax[1,0].legend(fontsize=8)
ax[1,1].loglog([z['K'] for z in r['matching']],[z['post_boundary_relative_difference'] for z in r['matching']],'o-',label='Matched vs unmerged continuation')
ax[1,1].loglog([z['K'] for z in r['independent_solver']],[z['normalized_state_difference'] for z in r['independent_solver']],'s-',label='Independent trace evolution')
ax[1,1].set(xlabel='Dimensionless initial K',ylabel='Normalized state difference',title='Matching and independent metric checks');ax[1,1].legend(fontsize=8)
for a in ax.flat:a.grid(alpha=.2)
fig.savefig(P/'finite_gradient_diagnostics.png',dpi=180);plt.close(fig)

last=rows[-1];match=max(z['post_boundary_relative_difference'] for z in r['matching']);ind=max(z['normalized_state_difference'] for z in r['independent_solver'])
state=json.loads((P/'results/matching_states.json').read_text())[-1]

maths=r'''
## Equations and variables

Use $8\pi G_{\rm N}/3=1$, the relative scale factor $a(0)=1$ and $H(0)=1$. Dots below denote dimensionless local proper time; primes denote conformal time. The physical starting scale remains $a_i=10^{-10}$. Radiation budgets are $C=\rho_xa^4$, $G=\rho_\gamma a^4$, $V=\rho_\nu a^4$ and $M=\rho_ma^3$. Initially $C=\beta$, $G=(1-\beta)(1-f_\nu)$, $V=(1-\beta)f_\nu$, $M=0$.

The disclosed transfer prescription is

$$Q_m^\mu=-Q_x^\mu=\Gamma(T)(1+\xi)\rho_xu_x^\mu.$$

Here $T$ is the declared geodesic-reference proper-time clock, with conversion active for $0<T<1$. The synchronous slice sets its perturbation to zero. Under another gauge the clock perturbation must also transform; it is not a universal absolute-time assertion. The scalar modulation $\xi$ is the frozen WRRA seed, conserved to first order. Its unit-amplitude response is evolved and subsequently multiplied by the actual small seed. This constitutive choice is an explicit model input, not a particle reaction derived from a microscopic Hamiltonian.

The inherited background is

$$\dot N=H,\quad\dot C=-\Gamma C,\quad\dot M=\Gamma C/a,$$
$$\dot H=-\tfrac12[4(C+G+V)/a^4+3M/a^3],\qquad\dot W=H(C+G+V)/a.$$

Let $d_i=a^{3(1+w_i)}\delta\rho_i$, $P_i=a^4(\rho_i+p_i)\theta_i/K^2$, $L=\dot h$, and $P=\sum_iP_i$. There is no division by the initially zero matter density during integration. In the unit rate-modulation response,

$$\dot d_x=-K^2P_x/a-2CL/3-\Gamma(d_x+C),$$
$$\dot d_\gamma=-K^2P_\gamma/a-2GL/3,\quad
\dot d_\nu=-K^2P_\nu/a-2VL/3,$$
$$\dot d_m=-K^2P_m/a^2-ML/2+\Gamma(d_x+C)/a.$$

The momentum equations retain the receiver source:

$$\dot P_x=d_x/(3a)-3\Gamma P_x/4,\quad\dot P_m=3\Gamma P_x/4,$$
$$\dot P_\gamma=d_\gamma/(3a),\qquad
\dot P_\nu=d_\nu/(3a)-4VK^2s_\nu/(3a).$$

For a numerically stable $K\to0$ limit, use $s_\nu=\sigma_\nu/K^2$, $f_\ell=F_{\nu\ell}/K^\ell$ and $g=(h'+6\eta')/K^2$:

$$\dot\eta=3P/(2a^3),\quad L=K^2g/a-6\dot\eta,$$
$$\dot g=-2Hg+2\eta/a-12Vs_\nu/a^3,$$
$$\dot s_\nu=[4v_\nu/15+2g/15-3K^2f_3/10]/a,$$
$$\dot f_\ell=[\ell f_{\ell-1}-(\ell+1)K^2f_{\ell+1}]/[(2\ell+1)a],\quad\ell\ge3,$$

where $v_\nu=P_\nu/(4V/3)$ and $f_2=2s_\nu$. The upper hierarchy is set to zero beyond the stated truncation. Convergence is tested at $\ell_{\max}=16,24$ together with halved time steps; no claim is made for arbitrary wavenumber or arbitrarily long propagation.

The Hamiltonian constraint is inspected without resetting a metric variable:

$$K^2\eta-\tfrac12a^2HL+\tfrac32a^2\delta\rho=0.$$

An independent implementation evolves $L$ through the Einstein trace equation,

$$\dot L=-3HL+2K^2\eta/a^2-9\delta p,$$

and unscaled neutrino multipoles. Its trajectory is compared against the shear-based implementation. The energy/momentum residuals also directly inspect cancellation of the transfer terms; they are consistency checks, not independent observational tests.

## Executed matching operation

At $T=10$, retain $(h,\eta,g,M,d_m,P_m)$ and every neutrino moment. Absorb the remaining *perfect* reservoir radiation into the perfect photon-like bath:

$$G^+=G^-+C^-,\quad d_\gamma^+=d_\gamma^-+d_x^-,\quad
P_\gamma^+=P_\gamma^-+P_x^-;\qquad C^+=d_x^+=P_x^+=0.$$

This preserves background/perturbed total energy, pressure, momentum and anisotropic stress on the same proper-time slice, hence the induced metric and its first derivative. The operation is an exact linear stress-energy regrouping of two perfect radiative components. It is not a calculated microscopic thermalization or baryon-production reaction. Both the unmerged and merged systems are actually continued to $T=30$. Their agreement tests this regrouping only, not equality of every possible physical post-transition model.

The export retains separate photon and neutrino densities, velocities and the full computed neutrino hierarchy, rather than projecting it down to the two v0.3 primordial coefficients. Photon-reservoir absorption is a disclosed branch choice. Other destinations require a separately conserving matching rule.
'''

results=fr'''
\newpage

## Numerical outputs

| Quantity | Result |
|---|---:|
| New finite calculation checks | {r['checks_passed']} passed |
| Original finite wavenumbers actually evolved and matched | 64 |
| Zero-gradient entropy response | {r['zero_gradient']['S_mr']:.15g} |
| Zero-gradient radiation curvature response | {r['zero_gradient']['zeta_r']:.15g} |
| Largest physical $k/(aH)$ at matching | {last['k_over_aH']:.12g} |
| Mode-64 entropy-response relative change from v0.3 | {last['entropy_relative_to_v03']:.12g} |
| Mode-64 radiation-curvature relative change | {last['curvature_relative_to_v03']:.12g} |
| Actual 128-cell entropy field relative L2 change | {r['actual_seed']['entropy_L2_change_relative_to_v03']:.12g} |
| Largest matched/unmerged continuation difference, declared norm | {match:.6g} |
| Largest independent-metric state difference, declared norm | {ind:.6g} |

At the largest original mode, per unit rate modulation, $S_{{mr}}={last['S_mr']:.15g}$ and $\zeta_r={last['zeta_r']:.15g}$. The actual seed gives entropy RMS={r['actual_seed']['entropy_RMS']:.12g}. No amplitude was refitted. Printed digits specify reproducible outputs rather than empirical precision.

The merge also produces a branch-specific photon/neutrino entropy $S_{{\nu\gamma}}={state['S_nugamma_after_merge']:.12g}$ per unit modulation at mode 64. It is multiplied by the small actual seed; it is not a measured cosmological isocurvature amplitude. This separate species memory is retained in the export.

| Residual across the original 64 modes | Maximum declared normalized value |
|---|---:|
| Einstein Hamiltonian | {r['max_physical_constraint_residuals']['Hamiltonian_residual']:.6g} |
| Einstein trace | {r['max_physical_constraint_residuals']['trace_residual']:.6g} |
| Perturbed energy conservation | {r['max_physical_constraint_residuals']['energy_residual']:.6g} |
| Perturbed momentum conservation | {r['max_physical_constraint_residuals']['momentum_residual']:.6g} |

Each normalizer is explicit in `sample_audit` and in the negative-control JSON. These are numerical residuals in the declared units, not measurement uncertainties. The momentum constraint is used to evolve $\eta$; its identical re-evaluation is not counted as an independent test. The Hamiltonian and independent trace trajectories provide additional checks.

Stress cases extend to $k/(aH)=4.58257$ at matching. They are diagnostic wavenumbers outside the original finite SOURCE grid, not new universe-wide source modes. The comparison removes neutrino shear to define a separate perfect-fluid model; its metric differs. The combined hierarchy/time-step convergence changes the selected metric/curvature responses by at most {max(x['hierarchy_and_step_error'] for x in stress):.6g} in the declared norm.

## Rejecting controls

1. Delete the recipient momentum source while leaving energy exchange intact: energy residual remains small, but normalized Hamiltonian residual becomes {neg['Hamiltonian_residual']['normalized']:.6g}, trace residual {neg['trace_residual']['normalized']:.6g}, and momentum residual {neg['momentum_residual']['normalized']:.6g}. Energy-only auditing would miss the error.
2. Drop the reservoir density perturbation at matching: the relative total-density jump is {r['negative_controls'][1]['relative_density_jump']:.6g}.
3. Drop its momentum: the relative total-momentum jump is {r['negative_controls'][2]['relative_momentum_jump']:.6g}.

The 643 checks comprise 576 original-mode state/constraint/matching checks; three zero-gradient checks; five finite-gradient/hierarchy response checks; 21 actual-seed field checks; 35 stress-case matching/independent-solver/convergence checks; and three rejecting controls. Previous v0.3 checks are not added to this count.
'''

ending=r'''
## Falsification conditions and scope

Failure to recover the fixed v0.3 zero-gradient outputs, a nonconvergent hierarchy/time integration, failed Einstein constraints, unpaired transfer momentum, or a density/momentum/geometry jump on the declared matching surface rejects or revises this branch. The frozen SOURCE is used without a new observational amplitude fit. A later observational comparison must use the completed state and its declared physical history.

**Implemented:** the effective conversion interval now has finite spatial gradients at linear amplitude, separately moving components, a dynamical synchronous metric, a collisionless massless-neutrino hierarchy, and an explicitly executed conserving matching/continuation. The small-gradient limit is computed rather than imposed as the final state.

**Still open:** injecting this entire state into the production CAMB initial callback and computing new T/E/lensing spectra; a self-consistent nonzero baryon background/production and tight-coupled photon-baryon system in the conversion interval; massive-neutrino momentum dependence, collisional neutrino decoupling, a MeV thermal history, microscopic transfer rates, finite-quantum event timing, nonlinear dynamics and new observational likelihoods. A massless collisionless neutrino bath and a perfect photon-like bath are explicit effective inputs during this experiment, not a derived early-Universe thermal history. This extends Item 6 but does not close all of its physical branches.

The inherited v0.3 full CMB spectra are not relabeled as v0.4 predictions. No new CMB angular spectrum or new observational detection is claimed here. Standard GR/Boltzmann equations are disclosed construction material; their present integration is limited to the equations actually evolved.

## Reproduction and primary sources

Python 3.12, NumPy 2.3.5 and SciPy 1.17.0. Run `python run_checks.py`; it needs only the two frozen files in `inputs/`. `finite_gradient.py` and `independent_metric.py` contain both metric formulations. `results/audit.json` contains every named test, absolute residuals for counterexamples and normalization information. `matching_states.json` provides before/after species states and velocity units; `all_64_transition_responses.npz` stores normalized responses; `actual_128_cell_matched_fields.npz` applies them to the actual seed. `make_reports.py` additionally uses Matplotlib and Pandoc/XeLaTeX to rebuild the reports. A clean numerical rerun requires no CAMB binary or network.

1. Choi, W. and Choi, J. v0.3 predecessor, DOI [10.5281/zenodo.23489547](https://doi.org/10.5281/zenodo.23489547).
2. Ma, C.-P. and Bertschinger, E. *Cosmological Perturbation Theory in the Synchronous and Conformal Newtonian Gauges*, equations (21), (49), [astro-ph/9506072](https://arxiv.org/abs/astro-ph/9506072).
3. Malik, K. A. and Wands, D. *Cosmological perturbations*, interacting-fluid conservation and transfer, [arXiv:0809.4944](https://arxiv.org/abs/0809.4944).

External sources specify the adopted field equations; the reservoir prescription, finite-source response, matching operation and numerical outputs are the declared WRRA construction executed here. Authors: Wonsik Choi and Jeongin Choi, independent researchers. AI assistance: implementation, computational checks and language preparation. Original new material: CC BY 4.0. No new Zenodo/GitHub publication is asserted by this working report.

\newpage

## Diagnostic plots

![Finite-gradient corrections, neutrino-stress comparison, conservation counterexample and matching tests.](finite_gradient_diagnostics.png){width=100%}
'''

en=fr'''# Finite-Gradient Conversion and Conserving Neutrino-Metric Matching in WRRA

**MCC 3.0 Item 6 follow-up, working v0.4**  
Wonsik Choi · Jeongin Choi | Independent researchers | 20 October 2026

## Verified inputs → WRRA transformation → outputs → falsification

**Verified inputs.** Retain v0.3's fixed reservoir fraction $\beta={r['inputs']['beta']:.15g}$, proper pulse, starting scale, background normalization and 128-cell SOURCE seed. Split the spectator radiation using the inherited $N_{{\rm eff}}=3.044$ prescription, giving $f_\nu={r['inputs']['fnu']:.12g}$. The free-streaming/perfect-fluid content and reservoir velocity transfer are new disclosed effective-model choices.

**WRRA transformation.** Evolve the complete finite-k effective transition state rather than only its local zero-gradient entropy. Pair source and recipient energy and momentum, evolve metric and neutrino hierarchy, match by conserving the total stress-energy, then continue the matched state.

**Outputs.** {r['checks_passed']} new finite checks pass; all 64 original modes are evolved and matched. The zero-gradient coefficients reproduce v0.3. New complete species states and their action on the actual seed are exported.

**Falsification.** Failed conservation, Einstein constraints, matching continuity, convergence or zero-gradient recovery require revision. The current result is not a newly fitted CMB angular spectrum.

''' + maths + results + ending

ko=fr'''# 유한 구배 전환과 중성미자·메트릭의 보존적 접합

**WRRA / 최소계산우주론 3.0의 6번 보강 계산 v0.4 작업본**  
최원식 · 최정인 | 독립연구자 | 2026년 10월 20일

## 검증 입력

공개 v0.3의 전환 저장소 비중 $\beta={r['inputs']['beta']:.15g}$, 전환률 $\Gamma=\ln2$, 초기 물리 축척 $a_i=10^{{-10}}$, 고유시간 펄스 $0<T<1$, 기존 128셀 SOURCE 프로파일과 시간 정규화를 고정했다. 원래의 파수 $k_n=0.05n\,\mathrm{{Mpc}}^{{-1}}$, $n=1,\ldots,64$를 모두 다시 진화시켰다. 관측값을 이용한 기존 보정은 정당한 구성 입력으로 유지하며, 새로운 관측 진폭 맞춤은 하지 않았다.

비전환 복사를 완전유체인 광자형 부문과 무질량 자유비행 중성미자 부문으로 분리했다. 기존 $N_{{\rm eff}}=3.044$ 처방에 따라 중성미자 분율은 $f_\nu={r['inputs']['fnu']:.12g}$다. 전환 저장소는 별도의 완전 복사 유체, 생성물은 압력 없는 유효 물질이다. 이것은 실제 입자 반응이나 MeV 열역사를 이미 유도했다는 뜻이 아니라, 이번에 공개한 유효 구성이다.

## WRRA 고유 변환

기존의 국소 전환을 공간적으로 연결하기 위해 밀도만이 아니라 각 부문의 운동량을 함께 진화시켰다. 전환되는 복사에서 빠진 운동량을 생성 물질에 반대 부호로 넣는다. 메트릭과 중성미자는 전환 이후에 임의의 표준 초기값으로 덮어쓰지 않고 같은 구간에서 함께 계산한다.

계산은 **섭동 진폭에는 선형**이지만 공간 구배를 선도항에서 자르지 않는다. 따라서 여기서 '유한 구배'는 비선형 우주 구조까지 계산했다는 뜻과 구별한다. 고차 중성미자 다중극의 유한 절단은 명시하고 절단 차수·시간 간격을 바꾸어 대조했다.

전달 규칙은 $Q_m^\mu=-Q_x^\mu=\Gamma(T)(1+\xi)\rho_xu_x^\mu$다. $T$는 정한 초기면에서 시작하는 기준 측지선의 고유시간이며, 동기 게이지에서 그 섭동을 0으로 두었다. 다른 게이지에서는 이 시계의 섭동도 함께 변환해야 한다. 하나의 우주에 전역 절대 동시성을 추가하는 규칙이 아니다. $\xi$는 고정한 기존 SOURCE이며, 단위 진폭의 선형 응답을 구한 후 실제 작은 진폭에 적용했다.

### 에너지와 운동량을 동시에 연결

$a(0)=H(0)=1$, $8\pi G_{{\rm N}}/3=1$인 정규화에서 $C=\rho_xa^4$, $G=\rho_\gamma a^4$, $V=\rho_\nu a^4$, $M=\rho_ma^3$를 사용한다. 점은 국소 고유시간 미분이다.

$$\dot C=-\Gamma C,\qquad\dot M=\Gamma C/a.$$

섭동 밀도 장부를 $d_i=a^{{3(1+w_i)}}\delta\rho_i$, 운동량 장부를 $P_i=a^4(\rho_i+p_i)\theta_i/K^2$로 두면 전환 부문의 운동량은

$$\dot P_x=d_x/(3a)-3\Gamma P_x/4,\qquad\dot P_m=3\Gamma P_x/4$$

가 된다. 처음 물질 밀도가 0이어도 적분 중에는 $\delta\rho_m/\rho_m$로 나누지 않으므로 특이점 없이 출발한다. 밀도 전환항은 $-\Gamma(d_x+C)$와 $+\Gamma(d_x+C)/a$로 각각 반영했다.

### 메트릭과 자유비행 중성미자

동기 게이지의 $h,\eta$를 진화시키고, 중성미자의 밀도·속도·사중극 비등방 응력과 상위 다중극을 함께 적분했다. 수치적으로 작은 파수의 상쇄를 줄이기 위해 $s_\nu=\sigma_\nu/K^2$, $f_\ell=F_{{\nu\ell}}/K^\ell$, $g=(h'+6\eta')/K^2$를 쓴다. 프라임은 등각시간 미분이다.

$$\dot\eta=3\sum_iP_i/(2a^3),\qquad\dot h=K^2g/a-6\dot\eta,$$
$$\dot g=-2Hg+2\eta/a-12Vs_\nu/a^3.$$

별도 구현은 전혀 다른 메트릭 진화 변수인 $L=\dot h$를 사용하고,

$$\dot L=-3HL+2K^2\eta/a^2-9\delta p$$

를 직접 적분한다. 두 적분 궤적을 대조했다. 해밀토니안 제약은 결과를 맞추기 위해 매번 덮어쓰지 않고 독립적으로 검사한다. 운동량 제약은 $\eta$의 진화에 사용하므로, 같은 식을 다시 평가한 것을 독립 검증이라고 세지 않았다.

### 실제 실행한 접합

$T=10$에서 남아 있는 완전 복사 저장소를 완전유체 광자형 부문에 합쳤다.

$$G^+=G^-+C^-,\quad d_\gamma^+=d_\gamma^-+d_x^-,\quad P_\gamma^+=P_\gamma^-+P_x^-.$$

메트릭·물질 상태와 중성미자 계층은 그대로 운반했다. 같은 고유시간 면에서 총 밀도·압력·운동량·비등방 응력, 메트릭과 그 1차 미분이 이어진다. 합치지 않은 계와 합친 계를 모두 $T=30$까지 실제 진화시켜 대조했다. 이는 두 완전 복사 성분을 합치는 선형 응력-에너지 재분류의 접합이다. 미시적 열평형 반응까지 계산했다는 뜻은 아니다.

광자 부문으로 합친다는 선택 자체는 이번 가지의 공개된 구성이다. 다른 수신처를 택하려면 그 수신처의 밀도·운동량·응력까지 보존하는 별도 규칙이 필요하다. 광자·중성미자의 서로 다른 상태와 속도, 중성미자 다중극은 최종 출력에 남겼으며 두 개의 초기 기저 계수로 강제로 줄이지 않았다.

## 산출값

| 항목 | 이번 계산 결과 |
|---|---:|
| 새 유한 계산 검사 | {r['checks_passed']}개 통과 |
| 실제 진화·접합한 기존 파수 | 64개 |
| 무구배 극한의 엔트로피 계수 | {r['zero_gradient']['S_mr']:.15g} |
| 무구배 극한의 복사 곡률 계수 | {r['zero_gradient']['zeta_r']:.15g} |
| 기존 64번째 모드의 $k/(aH)$ | {last['k_over_aH']:.12g} |
| 64번째 모드 엔트로피 계수의 v0.3 대비 상대 보정 | {last['entropy_relative_to_v03']:.12g} |
| 실제 128셀 엔트로피장의 상대 L2 변화 | {r['actual_seed']['entropy_L2_change_relative_to_v03']:.12g} |
| 접합 전후 계의 후속 진화 차이: 공개한 정규화 기준 | {match:.6g} 이하 |
| 두 메트릭 적분 구현의 상태 차이: 공개한 정규화 기준 | {ind:.6g} 이하 |

$k\to0$에서 v0.3의 두 계수를 재현했다. 큰 파수에서부터 작은 파수로 응답식을 외삽한 것이 아니라, 기존 파수 64개를 각각 적분했다. 실제 SOURCE에 적용한 엔트로피 RMS는 {r['actual_seed']['entropy_RMS']:.12g}다. 계산된 각 자리수는 재현용 수치이며 관측 정밀도를 의미하지 않는다.

64번째 모드의 단위 조절자당 출력은 $S_{{mr}}={last['S_mr']:.15g}$, $\zeta_r={last['zeta_r']:.15g}$다. 광자형 흡수 가지에서는 접합 후 광자-중성미자 상대 엔트로피도 {state['S_nugamma_after_merge']:.12g}만큼 생긴다. 이 수치 역시 실제 작은 SOURCE 진폭을 곱해야 하며 관측된 진폭으로 제시하지 않는다.

| 기존 64모드 전체의 제약·보존 검사 | 최대 정규화 잔차 |
|---|---:|
| 아인슈타인 해밀토니안 제약 | {r['max_physical_constraint_residuals']['Hamiltonian_residual']:.6g} |
| 아인슈타인 trace 방정식 | {r['max_physical_constraint_residuals']['trace_residual']:.6g} |
| 섭동 에너지 보존 | {r['max_physical_constraint_residuals']['energy_residual']:.6g} |
| 섭동 운동량 보존 | {r['max_physical_constraint_residuals']['momentum_residual']:.6g} |

정규화 분모는 코드의 `sample_audit`와 JSON에 공개했다. 이 잔차는 선언한 단위·응답 규모에서의 계산 일관성으로, 물리적 오차의 보편 상한이나 새 관측 검증 횟수가 아니다.

기존 SOURCE 격자 밖의 진단용 파수에서는 접합 시 $k/(aH)=4.58257$까지 시험했다. 지평선 안쪽에서 중성미자 비등방 응력을 지운 완전유체 비교모형과 메트릭이 달라진다. 이 시험 파수를 우주의 새로운 SOURCE 주소나 기존 64모드라고 세지 않았다. 중성미자 절단 차수 16→24와 시간 간격 1/2 대조의 선택한 메트릭·곡률 응답 차이는 최대 {max(x['hierarchy_and_step_error'] for x in stress):.6g}였다.

## 반증조건과 거부 대조

1. 생성 물질의 운동량 수신항만 지우면 에너지 검사는 여전히 작지만, 해밀토니안 정규화 잔차는 {neg['Hamiltonian_residual']['normalized']:.6g}, trace는 {neg['trace_residual']['normalized']:.6g}, 운동량은 {neg['momentum_residual']['normalized']:.6g}로 커진다. 에너지만 맞추어서는 연결을 검증할 수 없다.
2. 접합에서 저장소의 밀도 섭동을 누락하면 총 밀도가 상대 {r['negative_controls'][1]['relative_density_jump']:.6g}만큼 불연속이 된다.
3. 운동량을 누락하면 총 운동량이 상대 {r['negative_controls'][2]['relative_momentum_jump']:.6g}만큼 불연속이 된다.

무구배 극한 재현, 보존·제약식, 접합 연속성, 시간 적분·다중극 수렴 중 어느 하나라도 정한 허용 기준을 넘으면 해당 가지를 수정하거나 기각한다. 검사 643개는 기존 모드 관련 576개, 무구배 3개, 구배·계층 응답 5개, 실제 SOURCE 적용 21개, 진단 파수의 접합·독립 적분·수렴 35개, 거부 대조 3개다. v0.3의 123개를 합산하지 않았다.

## 판정과 남은 범위

**선언한 유효 전환 모형 안에서 유한 공간 구배, 별도 운동량, 메트릭과 자유비행 무질량 중성미자를 함께 계산하고 보존적 접합·후속 진화를 실행했다.** 기존 작은 구배 결과가 유지된다는 것도 수치로 확인했다. 따라서 1번 과제 중 전환 구간의 유효 유체·메트릭·중성미자 연결이 보강됐다.

이번에 출력한 전체 상태를 실제 CAMB 초기 콜백에 주입해 새 T/E/렌징 스펙트럼을 만드는 단계는 아직 실행하지 않았다. 바리온의 비영 배경과 광자-바리온 긴밀 결합, 실제 입자 생성, 유질량 중성미자의 운동량 의존성, 충돌을 포함한 중성미자 탈결합과 MeV 열역사는 별도 보강 대상이다. 유한 양자 방출 시각·기록 비용·비선형 진화·새 관측 우도도 이번 계산 범위에 넣지 않았다. 기존 v0.3 CMB 출력값을 이번 v0.4의 새 계산값으로 바꾸어 부르지 않는다.

## 재현과 출처

Python 3.12, NumPy 2.3.5, SciPy 1.17.0에서 `python run_checks.py`를 실행한다. CAMB 실행본이나 네트워크는 필요 없다. 두 입력 파일, 두 메트릭 구현, 명명된 전체 검사, 64개 모드의 접합 전·후 상태, 실제 128셀 적용 배열을 함께 보존했다. 각도 계층과 초기 섭동 부호는 아래 원전의 동기 게이지 규약을 사용한다.

- 선행 v0.3: [10.5281/zenodo.23489547](https://doi.org/10.5281/zenodo.23489547).
- Ma와 Bertschinger, 동기/뉴턴 게이지 우주론 섭동, 식 (21), (49): [astro-ph/9506072](https://arxiv.org/abs/astro-ph/9506072).
- Malik과 Wands, 상호작용 유체의 공변 에너지·운동량 전달: [arXiv:0809.4944](https://arxiv.org/abs/0809.4944).

기존 장 방정식은 공개된 구성·검증 재료이며, WRRA의 저장소·SOURCE 변환·접합 규칙과 결합해 실제 적분한 범위만 통합으로 판정한다. 새 원고 저자 최원식·최정인. AI는 구현·수치 검수·언어 정리에 참여했다. 새 자료 CC BY 4.0. 이 작업본 자체는 새로운 Zenodo/GitHub 게시 완료를 뜻하지 않는다.

\newpage

## 계산 진단 도해

![기존 64모드 구배 보정, 중성미자 응력 대조, 운동량 누락 대조와 접합 검사.](finite_gradient_diagnostics.png){{width=100%}}
'''

for lang,text in [('EN',en),('KO',ko)]:
    # Normalize only prose dash variants; math/code are preserved.
    name=f'WRRA_Finite_Gradient_Matching_v0_4_{lang}'
    cmd=['pandoc','--from=markdown','--to=latex','--standalone','--pdf-engine=xelatex',
         '-V','mainfont=Noto Sans CJK KR','-V','sansfont=Noto Sans CJK KR','-V','monofont=DejaVu Sans Mono',
         '-V','geometry:margin=20mm','-V','fontsize=10pt','-V','colorlinks=true','-o',name+'.pdf']
    subprocess.run(cmd,input=text,text=True,cwd=P,check=True)
    # Source text retained as a plain-text input for exact report reconstruction.
    (P/(name+'.txt')).write_text(text)

readme='''WRRA Finite-Gradient Matching v0.4 - working calculation, 20 October 2026
Authors: Wonsik Choi and Jeongin Choi, independent researchers.

Run: python run_checks.py
Numerical requirements: Python 3.12, numpy==2.3.5, scipy==1.17.0
Report rebuild: python make_reports.py (also matplotlib, pandoc, xelatex and Noto Sans CJK KR)

Inputs are frozen v0.3 dynamics_results.json and quantized_seed.npz.
No CAMB runtime or network is required for numerical reproduction.
The rate perturbation response is normalized to one; actual small WRRA seed
amplitudes are then applied in Fourier space. This is linear-amplitude finite-k
evolution of a declared effective reservoir, photon-like perfect radiation,
massless collisionless neutrinos and generated pressureless matter.
It does not compute particle reactions, detailed thermal history or new CMB spectra.

finite_gradient.py: scaled-shear metric and rescaled neutrino hierarchy.
independent_metric.py: independently integrated trace metric, raw hierarchy.
run_checks.py: named tests, all 64 physical modes, seven diagnostic comparisons,
actual seed application, matching, convergence, and three rejecting controls.
results/audit.json: all checks and scope; previous v0.3 checks are not recounted.
results/matching_states.json: per-unit response before/after matching.
Unqualified theta fields use dimensionless conformal-time units; fields ending
_Mpc_inverse provide physical inverse-Mpc velocity-divergence responses.
all_64_transition_responses.npz stores the pre-match internal unit-response state.
actual_128_cell_matched_fields.npz stores actual seed-applied post-match fields.
Curvature and entropy diagnostics at matching are post-exchange quantities.

New original material: CC BY 4.0. Source field equations cited in both reports.
No new Zenodo/GitHub release is asserted by this local working package.
'''
(P/'README.txt').write_text(readme)
(P/'requirements.txt').write_text('numpy==2.3.5\nscipy==1.17.0\n')
files=[p for p in P.rglob('*') if p.is_file() and 'source' not in p.relative_to(P).parts and '__pycache__' not in p.parts and p.name!='SHA256SUMS.json' and p.suffix not in ['.zip','.log']]
(P/'SHA256SUMS.json').write_text(json.dumps({str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},indent=2)+'\n')
