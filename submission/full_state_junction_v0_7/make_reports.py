from pathlib import Path
import json,subprocess,hashlib
P=Path(__file__).resolve().parent
r=json.loads((P/'results/event_tangent.json').read_text());a=json.loads((P/'results/audit.json').read_text())
b=r['base'];c=r['calibration'];ref=json.loads((P/'results/event_tangent_refined.json').read_text())
common=r'''
\newpage

## Equations and conventions

For $y=(N,\ln T_\gamma,M,W)$ and $N=\ln a_{\rm rel}$,
$C$ is constant between events. The background equations are

$$\rho=\rho_{\rm EM}(T)+\rho_{\nu,i}e^{-4N}+Ce^{-4N}+Me^{-3N},$$
$$\dot N=H,\qquad
\dot{\ln T}=-\frac{3H(\rho_{\rm EM}+p_{\rm EM})}{T\partial_T\rho_{\rm EM}},
\qquad \dot M=0.$$

Dots in the implemented ODE use the inherited dimensionless time. The finite
electron mass, thermal Fermi integrals, effective $N_{\rm eff}=3.044$ input,
and instantaneous relativistic neutrino decoupling branch are inherited from
v0.6. This is not a collision-integral calculation or a BBN yield prediction.

At event $j$, with $q=\beta\rho_i/256$ and $\epsilon=0.01$,

$$C^+=C^--q,\quad M^+=M^-+(1-\epsilon)qe^{-N},\quad
\rho_{\rm EM}(T^+)=\rho_{\rm EM}(T^-)+\epsilon qe^{-4N}.$$

The rate modulation is the original seed $\xi$, with no amplitude refit.
In the fixed-count neighborhood $t_j(\xi)=t_j(0)/(1+\xi)$.
For the common-time tangent $z=\partial y/\partial\xi$, the reset is

$$z^+=DR\,z^-+(DR\,f^--f^+)t'_j,\qquad t'_j=-t_j/(1+\xi).$$

Between events $\dot z=(\partial f/\partial y)z$. The last term above is
essential. Merely differentiating the state reset loses the entire response
in this autonomous fixed-packet model. On the final common proper-time slice,

$$S_{m,{\rm EM}}=\frac{z_M}{M}-3z_N-
\frac{\partial_{\ln T}\rho_{\rm EM}}{\rho_{\rm EM}+p_{\rm EM}}z_{\ln T}.$$

This expression is a $k=0$ tangent of local cells. It supplies no new
finite-gradient radiation or momentum source.

For the *separate frozen v0.4 smooth-source states*, a residual synchronous
transformation into the post-exchange CDM frame is

$$\alpha=\theta_m/k^2,\quad \theta_i^{c}=\theta_i-k^2\alpha,\quad
\delta_i^c=\delta_i+3(1+w_i){\cal H}\alpha,\quad
\eta^c=\eta+{\cal H}\alpha.$$

Here $\alpha'=-{\cal H}\alpha$ after exchange. The implementation also
transforms $h'$ and $\eta'$, with
$\eta^{c\prime}=\eta'+({\cal H}'-{\cal H}^2)\alpha$ and
$h^{c\prime}=h'+2k^2\alpha-6({\cal H}'-{\cal H}^2)\alpha$.
The neutrino monopole and dipole change; all retained moments $\ell\ge2$
remain intact. CAMB conventions are $\mathrm{etak}=k\eta$,
$q_\gamma=4\theta_\gamma/(3k)$, and $q_\nu=F_{\nu1}$.
The adapter exports a partial native variable dictionary, not a complete
CAMB evolution array. No metric $h$ is invented from an unspecified spatial
gauge integration constant.

## Release revalidation and numerical correction

Ten supplementary release checks pass in addition to the 472 base checks.
The independent clock coordinate $u=(1+\xi)t$ keeps events fixed and integrates
$w'=Jw-f$, $w^+=DRw^-$; the final derivative is $z=w+t_{\rm end}f$.
It recovers the entropy response within relative $8.39\times10^{-9}$.
A five-point numerical flow Jacobian agrees within $1.78\times10^{-10}$.

Reconstructing $h'+6\eta'$ from its separately rounded transformed terms
causes up to 16.66% error in the small Bardeen potential at the lowest mode.
The r1 adapter therefore retains the combination directly as
$h'+6\eta'=2k^2(g/2+\alpha)$, using the inherited scaled shear $g$.
The Bardeen potential computed from this stable combination is gauge-invariant
within relative $4.35\times10^{-12}$ over all 64 modes. The lossy reconstruction
is kept as a negative control. Separate derivative components are diagnostics;
they must not be used to recover this small difference. A future actual CAMB
transport must also verify stable constraint evaluation; this release does not
claim to have performed that transport.

The original entropy response, target calibration and 472 base checks are
unchanged. An independent SI-unit reconstruction yields
$\omega_c=0.103663511046343$, consistent with the thermal-density calculation.

## Sources and reproducibility

- WRRA v0.4: DOI [10.5281/zenodo.23490141](https://doi.org/10.5281/zenodo.23490141).
- WRRA v0.5: DOI [10.5281/zenodo.23491041](https://doi.org/10.5281/zenodo.23491041).
- WRRA v0.6: DOI [10.5281/zenodo.23491673](https://doi.org/10.5281/zenodo.23491673).
- Ma and Bertschinger (1995), [astro-ph/9506072](https://arxiv.org/abs/astro-ph/9506072): scalar gauge and Einstein-Boltzmann conventions.
- CAMB 2.0.4 pristine local source, `fortran/equations.f90`: native variable conventions; scalar initial-state assignment and constraint equations. This artifact does not modify or run CAMB.
- CODATA constants through SciPy 1.17.0; the same finite-mass electromagnetic EOS code as the frozen v0.6 input.

Run `python run_all.py` with the pinned requirements. The bundle includes
all inputs used here, scripts, machine-readable outputs, checks and hashes.
The original v0.4/v0.5/v0.6 publications remain unchanged.
Release DOI: [10.5281/zenodo.23492328](https://doi.org/10.5281/zenodo.23492328).
No new CMB or lensing result is claimed.
'''
ko=rf'''---
title: "WRRA 전체 상태 접합: 개발 검증 v0.7-dev-r1"
author: "Won sik Choi · Jeongin Choi"
date: "2026-10-20"
lang: ko
---

## 1. 검증 입력

입력은 공개된 v0.4의 실제 64개 모드와 중성미자 13개 모멘트, v0.5의
256분할 유한 방출 시계, v0.6의 유한 질량 전자·양전자 열역사다.
원래 128셀 씨앗을 그대로 사용했다. 후단 목표 밀도는 기존 WRRA
dark-weight-only 배경의 $\omega_c={c['target_omch2']:.14f}$이다.
이 목표 및 알려진 상수는 명시적 캘리브레이션 입력으로 취급한다.

## 2. WRRA 변환

첫째, v0.4의 전체 스칼라 상태를 CDM 정지 동기 게이지로 변환했다.
밀도만 바꾸지 않고 속도, 메트릭 도함수, 중성미자 단극·쌍극 모멘트를
함께 변환했다. 둘째, v0.5의 각 방출 시각이 씨앗에 따라 이동하는 효과를
v0.6 열역사에 넣어 같은 시간면에서의 선형 응답을 적분했다.
r1에서는 작은 메트릭 도함수 조합을 직접 보존하여 수치 상쇄를 보완했다.
이 두 계산은 각각 검증되었으나 서로 다른 전환 모형의 상태이므로
하나의 완성된 유한 파수 경로로 합쳐졌다고 주장하지 않는다.

## 3. 새 산출

| 항목 | 실행 결과 |
|:---|---:|
| 64모드 변환 후 에너지 제약 최대 잔차 | $3.29\\times10^{{-16}}$ |
| 운동량 제약 최대 잔차 | $4.31\\times10^{{-16}}$ |
| 엔트로피 게이지 불변량 오차 | $1.12\\times10^{{-16}}$ 미만 |
| 유한 방출·열역사의 $k=0$ 엔트로피 응답 | {b['S_m_em_response']:.12f} |
| 이전 연속 전환 응답 | {r['smooth_v04_entropy_response']:.12f} |
| 원래 씨앗에 적용한 엔트로피 RMS | $4.80263\\times10^{{-9}}$ |
| 기존 전환량의 열역사 유도 $\omega_c$ | {b['omch2_from_packets']:.12f} |
| 기존 후단 목표 대비 차이 | {c['old_relative_mismatch']*100:.6f}% |
| 목표 밀도에 재보정한 $\beta$ | $8.85389093544\\times10^{{-7}}$ |
| 기존 $\beta$ 대비 변화 | +{c['beta_relative_change']*100:.6f}% |

현재 열역사를 거친 유한 방출량은 기존 후단 밀도보다 약 13.9% 낮다.
이것은 WRRA 구조의 관측 배제 결론이 아니라, 서로 다른 단계의
정규화를 그대로 접합할 수 없음을 보여 주는 결과다. 전환량을 목표에
맞춰 재보정하면 $\omega_c={c['recalibrated_result']['omch2_from_packets']:.12f}$를
얻는다. 재보정은 정당한 배경 보정이며 독립적인 새 밀도 예측으로
표시하지 않는다. 이 새 배경으로 64모드를 다시 진화한 계산은 아직 없다.

## 4. 반증 및 검증

에너지·운동량 제약, 역 게이지 변환, 엔트로피 불변량, 중성미자 고차
모멘트 보존을 각 모드에서 확인했다. 속도를 단순히 삭제하는 대조군은
운동량 제약을 약 1.47% 위반한다. 방출 시각 이동을 누락하는 대조군은
이 모형의 응답을 0으로 잘못 산출한다.

독립적인 비선형 두 경로의 중앙 차분과 새 접선 적분의 차이는
최대 $2.68\\times10^{{-7}}$ 상대오차다. EOS 격자·구적 및 시간 허용오차를
함께 강화한 엔트로피 응답 차이는 $1.39\\times10^{{-12}}$ 상대수준이다.
에너지와 압력 일 장부 잔차는 기본 계산 $3.11\\times10^{{-11}}$,
강화 계산 $2.53\\times10^{{-12}}$ 미만이다. 총 {a['checks_passed']}개 검사를 통과했다.

선형 접선은 방출 횟수가 같은 열린 구간에만 유효하다. 이번 구간은
$-0.00281226035<\xi<0.00845879466$이며 실제 128셀은 모두 그 안에 있다.
이는 관측 우도나 전체 우주론의 검증 통과 수치가 아니다.

## 5. 결론과 남은 접합

**4번은 부분 구현 상태다.** 이번에 실제 완료한 것은 보존적인 64모드
좌표계 변환, 유한 방출 시각을 포함한 국소 열역사 접선 적분,
배경 밀도 재보정이다. 새로운 CMB 스펙트럼·렌징 우도는 계산하지 않았다.

다음 실행에는 유한 파수에서 사건면을 가로지르는 방출 에너지·운동량의
전달 법칙, 바리온·전자와 질량 중성미자 분포 상태, 재보정한 열역사에서의
모든 모드 재적분, 유한 공간 씨앗의 3차원 각도 공분산 완성이 필요하다.
앞의 동역학·입자종 상태는 단순 포맷 변환으로 만들어낼 수 없다.
뒤의 각도 완성은 가정을 명시한 조건부 모형으로 진행할 수 있으나,
이번 결과에는 도입하지 않았다. 현재의 불완전 상태를 전체 CAMB 초기
조건으로 내보내려 하면 코드가 구체적인 미충족 항목과 함께 중단한다.
'''
en=rf'''---
title: "WRRA Full-State Junction: Development Audit v0.7-dev-r1"
author: "Won sik Choi · Jeongin Choi"
date: "2026-10-20"
---

## 1. Verified inputs

The frozen inputs are the 64 evolved v0.4 modes with 13 neutrino moments,
the v0.5 finite-packet clock with 256 reservoir partitions, and the v0.6
massive-electron thermal completion. The original 128-cell seed is used
without amplitude refitting. The inherited WRRA dark-weight-only target is
$\omega_c={c['target_omch2']:.14f}$. This target and known physical constants
are explicitly declared calibration inputs.

## 2. WRRA transformations

The complete available scalar state of each v0.4 mode is transformed into
the post-exchange CDM-comoving synchronous frame. Density, velocity, metric
derivatives and the neutrino monopole/dipole are transformed together.
The r1 adapter also stores the small metric derivative combination directly
to prevent cancellation loss. Separately, the seed-dependent event-time motion of v0.5 is included in the
v0.6 thermal equations through a common-time saltation tangent. These two
validated calculations still describe different source models. They are
not represented as a single completed finite-k integration.

## 3. Computed outputs

| Quantity | Result |
|:---|---:|
| Maximum transformed Hamiltonian constraint residual | $3.29\\times10^{{-16}}$ |
| Maximum momentum constraint residual | $4.31\\times10^{{-16}}$ |
| Maximum absolute entropy gauge-invariance error | $<1.12\\times10^{{-16}}$ |
| Finite-packet thermal $k=0$ entropy response | {b['S_m_em_response']:.12f} |
| Earlier smooth-source response | {r['smooth_v04_entropy_response']:.12f} |
| Original-seed entropy RMS under the new local tangent | $4.80263\\times10^{{-9}}$ |
| Thermally normalized packet $\omega_c$ at old $\beta$ | {b['omch2_from_packets']:.12f} |
| Relative discrepancy against inherited late target | {c['old_relative_mismatch']*100:.6f}% |
| Recalibrated conversion fraction $\beta$ | $8.85389093544\\times10^{{-7}}$ |
| Change in conversion fraction | +{c['beta_relative_change']*100:.6f}% |

The old packet normalization produces about 13.9% less present dark matter
than the inherited downstream input. This is a junction normalization
discrepancy, not an observational exclusion of the WRRA structure.
Recalibration yields $\omega_c={c['recalibrated_result']['omch2_from_packets']:.12f}$.
This is legitimate background calibration, not an independent density
prediction. The 64 finite-k modes have not yet been rerun on that new background.

## 4. Falsification and checks

Both Einstein constraints, inverse transformation, entropy invariance and
retention of high neutrino moments are tested mode by mode. Simply deleting
the CDM velocity violates the momentum constraint by about 1.47%.
Omitting event-time motion incorrectly gives zero response for this model.

Independent central differences of nonlinear histories agree with the
saltation entropy tangent to at most $2.68\\times10^{{-7}}$ relatively.
Simultaneously refined EOS grid, quadrature and time tolerance change the
response by $1.39\\times10^{{-12}}$ relatively. Energy-plus-pressure-work
residuals remain below $3.11\\times10^{{-11}}$ and $2.53\\times10^{{-12}}$
for the base and refined runs. All {a['checks_passed']} acceptance checks pass.

The derivative is valid only on the fixed-count open branch
$-0.00281226035<\xi<0.00845879466$. All original 128 cells lie inside it.
These checks establish the stated numerical transformations, not an
observational validation of a completed cosmology.

## 5. Conclusion and remaining junction

**Step 4 remains partially implemented.** Executed advances are the conserving
64-mode frame transformation, local thermal/event-time tangent and background
recalibration. No new CMB spectrum or lensing likelihood is calculated here.

A genuine next integration must specify the finite-k energy/momentum transfer
across each event hypersurface; complete baryon/electron and massive-neutrino
distribution states; rerun modes on the recalibrated thermal background; and
declare the three-dimensional/angular covariance of the finite seed.
The first two requirements cannot be supplied by rearranging arrays.
An angular completion can be a declared conditional model, but none is
introduced here. Exporting these partial states as complete CAMB initial
conditions raises an explicit error listing the unmet physical requirements.
'''
for lang,body in [('KO',ko),('EN',en)]:
    stem=f'WRRA_Full_State_Development_v0_7_r1_{lang}'
    (P/(stem+'.md')).write_text(body.replace(chr(92)*2,chr(92))+common)
    cmd=['pandoc',str(P/(stem+'.md')),'--pdf-engine=xelatex','-V','mainfont=Noto Sans CJK KR',
        '-V','monofont=DejaVu Sans Mono','-V','geometry:margin=18mm','-V','fontsize=10pt',
        '-V','colorlinks=true','-o',str(P/(stem+'.pdf'))]
    subprocess.run(cmd,check=True)
print('reports generated')
