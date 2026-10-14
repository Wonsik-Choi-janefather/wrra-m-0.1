"""Write provenance and bilingual reports from the executed result files."""
from pathlib import Path
import hashlib,json,platform,importlib.metadata as md
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'results'
def read(name):return json.loads((OUT/name).read_text())

def main():
    p=read('preparation_results.json');v=read('validation_results.json');lens=read('lensing_results.json')
    ex=read('expanded_likelihood_results.json');up=read('upstream_reproduction_check.json');ic=read('initial_callback_check.json')
    row=ex['cases'][1]
    ko=f'''최소계산우주론: 유한 초기 평균 준비 · SOURCE 렌즈 · 확장 CMB 평가 v0.1
최원식 · 최정인 / 2026-10-14

검증 입력
실제 1,015,000 주소 배열(주소 1 제외는 원래 규칙 유지), 기존 슬롯·잔여·공급 장부,
고정 eta=(7.5615824991e-10,7.2857613288e-10,7.6461028188e-10) J/m^3,
lambda=(0,0.25,0), 공급 변조 epsilon=1e-8, k_n=0.05 n Mpc^-1 (n=1..7).
lambda는 이전 관측 진단으로 선택한 보정 후보를 그대로 유지했다. 광속은 고정 입력이며
관측값과 알려진 상수의 보정 활용을 허용한다. 새 진폭 최적화나 판독 후 밀도 교환은 없다.
Planck 공개 고다중극 Plik-lite 613구간, 저다중극 TT/EE (ell=2..29),
CMB 주변화 렌즈 9구간을 실제로 평가했다. 원본 입력의 SHA256을 함께 제공한다.

고유 변환
1. 주소별 e_s(n) w_n [1+lambda_s ln(n)/ln(N_U)]를 기존 128 슬롯/30 잔여에 다시 배치.
   reconstruct_upstream.py 실행으로 이전의 평균 장부·모드 벡터를 재현했다.
2. SOURCE |8>, 공급 Bernoulli 혼합상태, 기록 |0>에 추가 제어 레지스터
   rho_phase=I/128을 명시했다. 이는 원래 SOURCE 모드와 다른 추가 자유도다.
   제어 메모리는 퇴화 에너지로 선언하고 초기 혼합 엔트로피 ln(128)을 장부에 기록했다.
   메모리 준비·재설정의 동역학이나 무비용 반복을 증명한 것은 아니다.
   각 위상 j에서 p_r,j=1/2+epsilon[K_r(j)-1]을 적용해 평균 에너지 프로파일을 구성했다.
   각 모드 공분산 C_n=(v_cos v_cos^T+v_sin v_sin^T)/2와 유한 위상 평균을 비교했다.
   기존 등방 방향 평균과 보정된 거시 파수 연결은 그대로 채택했다.
3. 이 평균 프로파일의 S_D와 delta_R를 채택한 정규 복사시대/CDM 등곡률 초기조건에
   연결하고, 실제 패치 CAMB 초기 콜백의 밀도·속도와 비교했다.
   v_D의 정규 지연해는 v_D=-k(u_R/u_D)delta_R a^-1 integral(a^4 d tau)이며,
   초기 콜백은 선도 복사시대 항 -k(u_R/u_D)delta_R a^3 tau/5를 사용한다.
   별도 장부의 적분은 근복사시대 배경 급수에서 수행했다. 전체 역사 적분이 아니다.
4. 같은 7개 실제 SOURCE 모드를 ell=2..6000까지 진화시켜 T,E,phi를 추출했다.
   SOURCE에는 연속 파수 Limber 대체를 쓰지 않았다. 제3 전달함수의 phi 정규화를
   직접 원시 스펙트럼 적분과 비교했다. 이후 실제 CAMB 공분산 렌즈 커널로
   L(C_std,Cphi_std+Cphi_SOURCE)+L(C_SOURCE,Cphi_std+Cphi_SOURCE)를 계산했다.
   표준 성분과 SOURCE의 원시장은 독립으로 채택했다. 유한 SOURCE의 고차 연결 모멘트,
   일차 CMB/phi 상관을 모두 포함하는 정확 비가우시안 재매핑은 아직 실행하지 않았다.
5. 계산한 스펙트럼을 공개 Planck 자료와 네이티브 likelihood 구현에 넣었다.
   저다중극은 Cobaya TT/EE, 렌즈는 CMBmarged 자료를 읽는 CMBlikes,
   고다중극은 공개 전체 공분산·bin 가중치의 Gaussian Plik-lite 구현을 실행했다.
   공식 clik 실행과 비주변화 전체 전경 모형 분석은 수행하지 않았다.

산출값
- 평균 암흑 부하 0.278925610976744; H0=67.2568374662005 km/s/Mpc.
- 유한 위상 공분산/기존 Fourier 공분산 상대 차이 {p['relative_covariance_agreement']:.9g}.
- 초기 밀도 콜백 최대 상대 차이 {ic['max_density_relative_error']:.12g} (밀도 진단은 float32 출력),
  초기 정규 속도 최대 상대 차이 {ic['max_velocity_relative_error']:.12g}.
- SOURCE 렌즈 편향 RMS {lens['SOURCE_deflection_RMS_arcsec']:.12g} 초각.
  표준 성분 편향 RMS {lens['standard_deflection_RMS_arcsec']:.12g} 초각.
  편향 분산 비 {lens['source_to_standard_deflection_variance_ratio']:.12g}.
- 고다중극 quadratic form / chi^2 = {row['high_ell_quadratic_form']:.12f}.
- 저다중극 TT -2lnL = {row['low_T_minus2logL']:.12f}.
- 저다중극 EE -2lnL = {row['low_E_minus2logL']:.12f}.
- 렌즈 CMBmarged -2lnL = {row['lensing_CMBmarged_minus2logL']:.12f}.
- SOURCE 추가에 따른 합산 -2lnL 차이 = {ex['SOURCE_change_combined_minus2logL']:.12g}.
  각 블록은 정규화 상수가 다르므로 합계 약 1014.36을 단순 자유도 chi^2로 해석하지 않는다.
  SOURCE로 인한 차이는 관측상 구별 가능한 개선으로 해석하지 않는다.
  이전 고다중극 585.9139에서 585.7475로의 변화는 주로 기준 렌즈 계산 확장에 따른 것이다.

반증조건과 검사
준비 상태가 양수가 아니거나, 공분산이 양의 준정부호가 아니거나, 초기 콜백이 준비한
정규 조건과 불일치하거나, phi 단위/정규화·해상도·적분 수렴에 실패하면 연결을 수정한다.
이번 새 검사 {v['passed_count']}/{v['check_count']}, upstream 재현 검사 {sum(up['checks'].values())}/{len(up['checks'])} 통과.
검사는 구현/수치 조건을 검증하며 모형 전체의 관측적 확증을 뜻하지 않는다.
정밀도 1.5 -> 2.5에서 SOURCE phi의 최대 정규화 차이는 {100*v['SOURCE_phi_accuracy_max_relative_change']:.5f}%,
CMB는 {100*v['SOURCE_CMB_accuracy_max_relative_change']:.5f}%였다.
입력 lmax 5000/6000 및 Python/Fortran 기준 렌즈 비교의 bin 차이는 각각
공분산으로 표준화한 RMS 약 0.000305/0.000288로 작았다.
높은 ell 정규화 인자를 int32로 제곱하던 오버플로는 검사 중 발견해 float64로 수정했다.
수정 후 SOURCE phi 전 구간 양수성 및 일차장/phi 공분산 검사를 통과했다.

판정과 다음 연결
유한 평균 준비 -> 채택한 물리 초기조건 -> 실제 SOURCE 전달/공분산 렌즈 ->
고·저다중극/렌즈 관측 평가까지 실행된 조건부 통합이다. 알려진 물리 모듈도 실제
실행 경로로 연결했다. 새로운 독립 예측을 필수 판정 기준으로 삼지 않는다.
남은 핵심은 평균 상태와 개별 실행의 관계다. 독립 주소 공급 비트라는 한 준비 예에서는
공급 고유 요동의 상대 RMS가 D=0.34514, R=0.49415로, 평균 위상 신호의
D=1.21074e-8, R=9.48940e-9보다 크다. 현재 중력 판독은 앙상블 평균 응력이다.
이 고유 분산을 그대로 우주론적 확률장으로 대입하지 않았다. 상관 준비를 달리하면
분산이 달라질 수 있으므로 모든 준비의 불가능성으로 해석하지 않는다.
독립 프레임 평균화만 가정하면 필요한 표본수는 약 8.13e14/2.71e15이나,
그 독립성·새 공급·기록·재설정 비용을 포함한 실제 평균화 과정은 아직 구현하지 않았다.
다음은 공급 상관 구조 또는 유한 평균화의 자원 장부를 구성해 개별 실행과 평균을
연결하는 일이다. 또한 초기 준비의 동역학적 생성과 SOURCE의 정확 비가우시안 렌즈
재매핑이 남아 있다.

재현
Python 3.12, NumPy/SciPy, Cobaya 3.6.2, getdist 1.7.7 및 패치 CAMB 2.0.4.
pip install -r requirements.txt
python reproduce.py                 # 주소 재현 및 CAMB까지 모두 실행; 무거운 작업은 직렬
python reproduce.py --skip-camb     # 저장된 전달함수로 준비·관측 평가 재실행
python reproduce.py --verify-only   # 저장된 결과의 수치 검사와 그림 생성
Linux용 패치 런타임과 원본 CAMB 압축 소스/패치/라이선스가 포함되어 있다.
호환되지 않는 환경에서는 gfortran와 make 설치 후 python build.py로 다시 빌드한다.
결과 JSON/CSV/NPZ, 실제 공개 자료, 그림, SHA256SUMS 및 provenance.json을 포함한다.
'''
    (ROOT/'README_KO.txt').write_text(ko)
    en=f'''Minimum-Computation Cosmology: Finite Mean Preparation, SOURCE Lensing, and Expanded CMB Evaluation v0.1
Wonsik Choi and Jeongin Choi / 2026-10-14

INPUTS
Actual 1,015,000-address archive; inherited residue/128-slot/supplier ledgers;
fixed eta, lambda=(0,0.25,0), epsilon=1e-8, k_n=0.05 n Mpc^-1 for n=1..7.
The prior observationally informed calibration is retained, with no amplitude optimizer
or post-readout density swap. c is a declared fixed input. Calibration by known data
is permitted; an independent prediction is not a mandatory criterion of the architecture.
Public Planck high-l Plik-lite (613 bins), low-T/low-E (l=2..29), and nine
CMB-marginalized lensing bins are executed, not merely referenced.

ARCHITECTURAL TRANSFORMATION
Reconstruct e_s(n)w_n[1+lambda_s ln(n)/ln(N_U)] -> residue/slot/supply payload.
Add a counted 128-state phase-control register rho=I/128, distinct from the pure |8>
SOURCE register. Conditional supplier states have p_r,j=1/2+epsilon(K_r,j-1).
The initial control entropy is ln(128); energy-degenerate memory is declared.
No free repeated reset or dynamical preparation process is claimed.
Construct the finite mean-energy profile and compare its covariance with
sum_n(v_cos v_cos^T+v_sin v_sin^T)/2. Retain the adopted macro-scale anchor
and isotropic orientation average. Feed the resulting S_D and delta_R into the
adopted regular radiation/CDM-isocurvature extension; inspect actual CAMB
initial-condition callbacks. The retarded dark velocity ledger uses the near-radiation
background series; the solver callback uses its regular leading term.
Run patched CAMB for all seven SOURCE wavenumbers and every l=2..6000,
including the third (phi) transfer. Disable continuum Limber substitution for SOURCE.
Check phi normalization against direct primordial quadrature at low L.
Execute CAMB covariance remapping as
L(C_std,Cphi_std+Cphi_SOURCE)+L(C_SOURCE,Cphi_std+Cphi_SOURCE).
The adopted standard primary field and SOURCE primary field are independent.
This is a covariance-kernel extension. SOURCE higher connected moments and primary/lens
correlations are not fully remapped; it is not exact finite-ensemble non-Gaussian lensing.
Execute native Cobaya TT/EE and CMBlikes with released CMBmarged data,
and native Gaussian Plik-lite with the full released bin covariance and weights.
Official clik and an unmarginalized full foreground analysis are not executed.

OUTPUTS
Finite-phase/Fourier covariance relative discrepancy: {p['relative_covariance_agreement']:.9g}.
Initial density callback maximum relative discrepancy: {ic['max_density_relative_error']:.12g}
(native named density outputs are float32); velocity: {ic['max_velocity_relative_error']:.12g}.
SOURCE deflection RMS: {lens['SOURCE_deflection_RMS_arcsec']:.12g} arcsec.
Standard deflection RMS: {lens['standard_deflection_RMS_arcsec']:.12g} arcsec.
SOURCE/standard deflection variance: {lens['source_to_standard_deflection_variance_ratio']:.12g}.
High-l quadratic form: {row['high_ell_quadratic_form']:.12f}.
Low-T -2logL: {row['low_T_minus2logL']:.12f}.
Low-E -2logL: {row['low_E_minus2logL']:.12f}.
CMBmarged lensing -2logL: {row['lensing_CMBmarged_minus2logL']:.12f}.
SOURCE change in the summed offset-dependent -2logL: {ex['SOURCE_change_combined_minus2logL']:.12g}.
The sum near 1014.36 is not a universal chi-square with a simple degree count;
blocks have different likelihood normalization constants. The SOURCE change is tiny.
The earlier high-l result 585.9139 versus 585.7475 is primarily a change of the
baseline lensing calculation, not evidence for a SOURCE-driven fit improvement.

REFUTATION AND NUMERICAL CONTROLS
Revise the connection if preparation positivity, covariance positivity, initial
callback agreement, phi units/normalization, or resolution/remapping checks fail.
New checks: {v['passed_count']}/{v['check_count']} passed. Upstream reconstruction: {sum(up['checks'].values())}/{len(up['checks'])} passed.
Accuracy 1.5 -> 2.5 changes the peak-normalized phi spectrum by
{100*v['SOURCE_phi_accuracy_max_relative_change']:.5f}% and the CMB spectrum by {100*v['SOURCE_CMB_accuracy_max_relative_change']:.5f}%.
Lmax 5000/6000 and Python/native Fortran baseline remapping controls have
covariance-whitened bin RMS differences approximately 0.000305 and 0.000288.
An int32 overflow in the squared lensing normalization was caught by the positivity
check, corrected using float64, and all affected outputs recomputed before packaging.
These are numerical/structural checks of the declared conditional model.

CONCLUSION AND OPEN CONNECTION
The finite mean preparation, adopted physical initial dressing, executed SOURCE
covariance lensing, and expanded native observational evaluation are connected.
The mean/single-outcome bridge remains open. In an explicitly independent-address
supplier-bit preparation, intrinsic relative RMS is D=0.34514 and R=0.49415,
versus mean phase modulation RMS 1.21074e-8 and 9.48940e-9.
Current gravity reads ensemble-mean stress; this intrinsic variance is not silently
identified with a cosmological stochastic field. Correlated preparations can alter it.
Pure independent-frame averaging would require roughly 8.13e14/2.71e15 samples;
fresh resources, independence, record/reset costs, and actual averaging dynamics
have not been implemented. The next task is a counted correlated preparation or
finite averaging model linking individual execution to mean stress. Dynamical
generation of the primordial preparation and exact SOURCE non-Gaussian remapping
also remain open.

REPRODUCTION
pip install -r requirements.txt
python reproduce.py                 # serial upstream, CAMB, likelihood, controls
python reproduce.py --skip-camb     # re-use saved transfers
python reproduce.py --verify-only   # numerical controls and plots
Bundled patched Linux runtime; pristine CAMB source tarball, patch, build script,
licenses, actual public datasets, JSON/CSV/NPZ outputs, figures and SHA256 checksums.
If the binary is incompatible, install gfortran/make and run python build.py.
'''
    (ROOT/'README_EN.txt').write_text(en)
    sources=dict(CAMB_correlations='https://camb.readthedocs.io/en/stable/correlations.html',
        Cobaya_Planck='https://cobaya.readthedocs.io/en/latest/likelihood_planck.html',
        lowT='https://github.com/CobayaSampler/planck_native_data/releases/download/v1/planck_2018_lowT.zip',
        lowE='https://github.com/CobayaSampler/planck_native_data/releases/download/v1/planck_2018_lowE.zip',
        lensing='https://github.com/CobayaSampler/planck_supp_data_and_covmats/tree/master/lensing/2018',
        primordial_and_likelihood_paper='https://arxiv.org/abs/1907.12875',
        Planck_lensing_paper='https://arxiv.org/abs/1807.06210')
    meta=dict(date='2026-10-14',researchers=['Wonsik Choi','Jeongin Choi'],sources=sources,
        prior_bridge_library_id='libfile_6a5905d2952881919bc8a3b1d153147b',
        upstream_DOI='10.5281/zenodo.23329214',python=platform.python_version(),
        package_versions={n:md.version(n) for n in ['numpy','scipy','matplotlib','sympy','mpmath','cobaya','getdist']},
        CAMB_version='2.0.4 with included SOURCE patch',
        binary_sha256=hashlib.sha256((ROOT/'runtime/camb/camblib.so').read_bytes()).hexdigest(),
        inputs={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((ROOT/'inputs').rglob('*')) if f.is_file()},
        new_checks=v['checks'],dynamical_preparation_closed=False,single_outcome_gravity_closed=False,
        covariance_SOURCE_lensing_executed=True,exact_nonGaussian_SOURCE_lensing=False,official_clik_used=False,
        calibration_retained=True,independent_prediction_required=False,
        joint_block_covariance='Adopted block combination with CMB-marginalized lensing; not a full unmarginalized joint foreground fit')
    (ROOT/'provenance.json').write_text(json.dumps(meta,indent=2))

if __name__=='__main__':main()
