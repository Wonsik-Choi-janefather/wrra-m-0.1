from pathlib import Path
import shutil,json
ROOT=Path(__file__).resolve().parent
src=ROOT.parent/'nu_scaling_r2/book_v0_28_r2'; dst=ROOT/'book_v0_28_r3'
shutil.copytree(src,dst,dirs_exist_ok=True)
ko=r'''
### 122.1 실험 명세: 차등 위상 결합의 가시도 곡선

**검증 입력.** 122장의 동결 모형 v1.0에서 128개 $f_D(J)$, $g=1$, 혼합 준비 $I/128$, 광자 한 번의 전파 동안 유지하는 하나의 라벨을 사용한다. 이전 광학 자료에 새 피팅을 하지 않는다. 아래 수치는 실험을 설계하기 위한 계산값이며 실제 측정 결과가 아니다. 주파수 콤은 $\nu_n=n f_{rep}+f_{CEO}$ 관계를 이용하는 광주파수 교정 수단이다 [E1]. 콤의 주파수 비교 정밀도를 곧바로 셔터 시간 분해능으로 읽지 않는다.

**WRRA 고유 변환.** SOURCE 평균 응력의 유한 분포를 기존 $H_{int}$에 넣고 두 경로의 차등 위상을 비선택적으로 합산하여 $v=V/V_0$를 계산한다. 먼저 실제 장치가 구현하는 유효 노출량 $L$과 경로별 결합을 교정해야 한다. $L$은 장치의 길이나 통상적인 광로차 $D$와 자동으로 같지 않다. 자연적인 SOURCE와 실험 장치의 차등 결합을 확인하는 물리적 절차는 아직 확정되지 않았다. 이를 확인하지 못한 장치의 무신호 결과를 해당 조건부 곡선의 반증으로 간주하지 않는다. 반대로 이 연결이 검증되면 준비·결합·기억 규칙을 고정하고 아래 수치 비교를 수행할 수 있다.

**산출값: 사전 고정할 측정 범위.** 기존 532/1064/1550 nm 곡선의 문턱·최소·회복 위치를 재계산한다. 1064 nm에서는 $L=0$부터 $40\,\mathrm m$까지 유효 노출량을 스캔하고, 핵심 비교점은 13.578784206 m, 21.780958380 m, 37.278764320 m이다. 다른 두 파장은 같은 $L/\lambda$ 범위를 검사하므로 최대 유효 노출량은 각각 20 m와 약 58.271 m다. 세 파장의 세 핵심점, 총 아홉 점을 일차 통계검정 대상으로 사전 고정한다. 추가 스캔 점은 진단용이며 일차 검정의 점 수를 사후에 늘리지 않는다. 최소와 회복의 정규화 가시도는 각각 0.3586975046과 0.6081539566이다.

다음은 이번 설계에서 선택한 목표 오차 예산이다. 장치의 실측 사양이나 이미 달성한 성능으로 읽지 않는다.

| 항목 | 설계 목표와 적용 조건 |
|---|---|
| 정규화 가시도 | 점별 절대 표준불확도 0.01; 공통 기준 측정의 상관을 공분산에 포함 |
| 계수 통계 | $V_0\ge0.9$에서 신호·기준 블록 각각 최소 98,766개의 독립 검출 시행이면 이상적 통계 항의 표준오차 상계 0.005 |
| 유효 노출량 교정 | 가시도 오차 0.002의 충분조건: 532/1064/1550 nm에서 각각 15.93/31.86/46.41 mm 이내 |
| 잔여 위상 잡음 | 독립 영평균 Gaussian 잡음에 의한 상대 가시도 손실을 0.002 이하로 두려면 RMS 0.06328 rad 이하 |
| 광주파수·광로차 안정도 | $D=40$ m, 1064 nm, 서로 독립인 두 잡음에 위상 분산을 반씩 배분할 때 RMS 약 53.37 kHz 및 7.577 nm 이하 |

계수 통계 상계는 별도 교정으로 정한 두 프린지 극값 위상에서 균등하게 측정하는 이상적 Bernoulli 모형이다. 신호와 기준 각각의 전체 시행 수를 $N_b$라 하면 $\sigma_v\le\sqrt{2/(V_0^2N_b)}$를 사용했다. 사후 최대·최소 선택이나 위상 추정의 불확도, 검출기 비선형성·암계수·손실은 이 상계에 포함되지 않으므로 실제 분석에 추가한다. 검출률과 독립 준비율이 주어지지 않아 필요한 측정 시간은 아직 정하지 않는다.

유효 노출량 허용치는 실제 유한 분포에서 계산한 전역 상계

$$|v(L+\delta L,\lambda)-v(L,\lambda)|\le\frac{2\pi}{\lambda}\langle|f_D|\rangle|\delta L|$$

를 사용한다. $g$나 준비 분포의 불확도는 별도 전달해야 한다. 주파수 잡음과 일반 광로차 잡음에는 $\sigma_\phi^2=(2\pi D\sigma_\nu/c)^2+(2\pi\sigma_D/\lambda)^2$를 사용했다. 이 식은 해당 노출 시간에 대한 비상관 준정적 잡음 예시이며 실제 잡음 스펙트럼·서보 전달함수가 있으면 그 적분으로 대체한다. 두 개의 광학 잡음 목표는 SOURCE 유효 노출량 오차와 다른 장치 항이다. 전체 0.01 예산은 모든 항을 공분산으로 결합하여 다시 확인해야 한다. 높은 주파수 정확도 하나만으로 이 조건을 만족했다고 판정하지 않는다 [E2].

**반증조건.** 파장·노출 순서를 무작위화하고, 동일 노출 대조군, 결합 경로 교환, 단일 라벨 조건부 가시도, 독립적인 광원·검출기 기준 측정을 함께 기록한다. 균형 공통 결합과 단일 라벨에서는 정규화 가시도 1이 대조 예측이다. 진동·온도·편광·모드 겹침·공통 기준 오차를 기록하고, 추가 손실이 곧바로 WRRA 신호라고 판정하지 않는다. 물리적 준비 조건이 확인된 아홉 점에서 $r=y-v_{WRRA}$와 측정 공분산 $C$로

$$Q=r^{\mathsf T}C^{-1}r$$

를 평가한다. 알려진 공분산을 가진 Gaussian 근사, 사후 피팅 없음, 자유도 9의 사전 규칙은 $Q>27.8771648713$이면 유의수준 0.001에서 이 동결 분기를 기각하는 것이다. 공분산이 소표본에서 추정되거나 nuisance 모수가 함께 피팅되면 이 문턱을 그대로 쓰지 않고 실제 절차의 모의 반복으로 분포를 교정한다. 기각되지 않음은 입증이나 신호 발견을 뜻하지 않는다. 실패 후 관측값을 반영하여 모형을 수정하는 것은 정당하며, 변경한 입력·자유도·새 산출값을 새 버전으로 기록한다. 같은 규칙을 비교 모형에도 적용한다.

**결론과 실행 범위.** 원전 29개 파일 해시를 확인한 뒤 기존 광학 계산의 17+11개 검사를 재실행했다. 추가 측정 설계와 검증기의 결과는 부록 H.7에 둔다. 이 절은 실제 계산된 WRRA 곡선을 측정 범위·오차·기각 규칙으로 연결한다. 자연적 차등 결합의 구현 확인과 실제 데이터 수집은 남아 있다. 정해진 위상을 광학 위상변조기 또는 7-qubit 라벨 레지스터와 경로 qubit에 부호화하는 실험은 별도의 모사 구현 검증이며, 성공만으로 자연계 SOURCE 결합이 확인되지는 않는다.

셔터 주기의 역수는 약 $6.7508180\times10^{20}\,\mathrm{Hz}$이나 이 계산은 그 주파수의 검출선이나 콤 측정 신호를 예측하지 않는다. 정적 위상식에서는 $N\ell_{sh}=L$이므로 셔터 간격이 소거된다. 따라서 이 실험으로 셔터 주기 자체를 추정할 수 없다. 뒤틀림 응력의 실제 실험실 주파수 이동·힘·위상에 대한 전달함수가 계산되기 전에는 별도의 숫자형 분해능을 임의로 붙이지 않는다. 이는 기존 거시 응답 계산의 성과와 구분되는 추가 연결 과제다.

[E1] NIST, *Femtosecond-Laser Frequency Combs for Optical Clocks*, https://www.nist.gov/programs-projects/femtosecond-laser-frequency-combs-optical-clocks (확인: 2026-10-22).

[E2] NIST, *Advancing Statistical Methods for Next-Generation Clock Networks*, https://www.nist.gov/programs-projects/advancing-statistical-methods-next-generation-clock-networks (확인: 2026-10-22). 이 자료는 일반 계측·불확도 처리의 근거이며 WRRA 검증 자료가 아니다.

'''
en=r'''
### 122.1 Experimental specification: visibility under differential phase coupling

**Verification inputs.** Retain frozen optical model v1.0: the 128 values $f_D(J)$, $g=1$, preparation $I/128$, and one unchanged label during each photon's propagation. No new fit to optical data is performed. The following numbers are calculated design requirements, not experimental measurements. A frequency comb supplies optical-frequency calibration through $\nu_n=n f_{rep}+f_{CEO}$ [E1]. Frequency-comparison precision is not interpreted as shutter-time resolution.

**WRRA-specific transformation.** The existing $H_{int}$ maps the finite SOURCE mean-stress distribution into differential path phases, whose nonselective sum gives $v=V/V_0$. An apparatus must first calibrate its effective exposure $L$ and path-specific couplings. Neither apparatus length nor ordinary optical path difference $D$ automatically equals $L$. A physical procedure establishing natural SOURCE differential coupling in such an apparatus has not yet been fixed. A null result without that preparation does not test the conditional curve. Once the connection is established, freeze preparation, coupling, and memory rules and perform the numerical comparison below.

**Outputs: preregistered measurement range.** Recalculate the threshold, minimum, and revival for 532, 1064, and 1550 nm. At 1064 nm scan effective exposure $L$ from zero to $40\,\mathrm m$, with primary points at 13.578784206 m, 21.780958380 m, and 37.278764320 m. Matching $L/\lambda$ gives maximum effective exposures of 20 m and approximately 58.271 m at the other wavelengths. Preregister three primary points per wavelength, nine in total. Additional scan points are diagnostic and do not retrospectively enlarge the primary test. Minimum and revival normalized visibilities are 0.3586975046 and 0.6081539566.

The following are selected design targets, not measured apparatus specifications or achieved performance.

| Item | Target and assumptions |
|---|---|
| Normalized visibility | Absolute standard uncertainty 0.01 per point; shared-reference correlations included |
| Counting statistics | At least 98,766 independent detected trials in each signal and reference block gives ideal statistical standard-error bound 0.005 if $V_0\ge0.9$ |
| Effective exposure calibration | Sufficient bounds for visibility error 0.002: 15.93/31.86/46.41 mm at 532/1064/1550 nm |
| Residual phase noise | Independent zero-mean Gaussian RMS at most 0.06328 rad for fractional visibility loss at most 0.002 |
| Optical frequency and path stability | At $D=40$ m and 1064 nm, assigning half the phase variance to each independent contribution gives RMS limits about 53.37 kHz and 7.577 nm |

The counting bound assumes ideal Bernoulli trials split equally between two fringe-extremum phases established by separate calibration. With $N_b$ total trials in each of the signal and reference blocks, use $\sigma_v\le\sqrt{2/(V_0^2N_b)}$. This excludes retrospective selection of extrema, phase-estimation uncertainty, detector nonlinearity, dark counts, and losses; include them in actual analysis. No measurement duration follows without detection and independent-preparation rates.

The exposure requirement uses the global bound calculated from the actual finite profile,

$$|v(L+\delta L,\lambda)-v(L,\lambda)|\le\frac{2\pi}{\lambda}\langle|f_D|\rangle|\delta L|.$$

Propagate uncertainty in $g$ and preparation separately. For ordinary optical frequency and path noise, the design uses $\sigma_\phi^2=(2\pi D\sigma_\nu/c)^2+(2\pi\sigma_D/\lambda)^2$. This is an example of uncorrelated quasistatic noise over the exposure; replace it with integrated measured noise spectra and servo transfer functions where appropriate. These optical-noise limits are distinct from SOURCE effective-exposure uncertainty. Recheck the overall 0.01 budget by combining all terms and their covariance. High frequency accuracy alone does not establish the complete uncertainty budget [E2].

**Falsification conditions.** Randomize wavelength and exposure order. Record balanced common-coupling controls, exchanged coupling paths, single-label conditional visibility, and independent source/detector reference measurements. Balanced common coupling and a single conditioned label predict normalized visibility one. Record vibration, temperature, polarization, mode overlap, and shared-reference errors; additional loss alone is not a WRRA signal. For nine points with established physical preparation, use residuals $r=y-v_{WRRA}$ and measurement covariance $C$:

$$Q=r^{\mathsf T}C^{-1}r.$$

Under a Gaussian approximation with known covariance, no posterior fitting, and nine degrees of freedom, the preregistered rule rejects this frozen branch at significance 0.001 if $Q>27.8771648713$. If covariance is estimated from small samples or nuisance parameters are fitted jointly, calibrate the distribution by simulation of the actual procedure instead of retaining this threshold unchanged. Non-rejection is neither proof nor a signal discovery. Observation-driven model revision remains legitimate; record changed inputs, freedoms, and outputs in a new version. Apply the same standard to comparator models.

**Conclusion and execution scope.** All 29 original file hashes were checked before rerunning the optical model's 17+11 controls. Appendix H.7 records additional design and verifier tests. This section connects an actually computed WRRA curve to ranges, errors, and rejection rules. Establishing natural differential coupling and collecting measurements remain outstanding. Encoding the prescribed phases with an optical phase modulator or a seven-qubit label register and a path qubit would test a separate emulator implementation; success alone would not establish natural SOURCE coupling.

The reciprocal shutter interval is approximately $6.7508180\times10^{20}\,\mathrm{Hz}$, but this calculation predicts no detection line or frequency-comb signal there. Since $N\ell_{sh}=L$, shutter spacing cancels from the static phase law. This experiment cannot estimate the shutter interval itself. Do not assign a separate numerical laboratory resolution to twist stress before computing a transfer function to an actual laboratory frequency shift, force, or phase. This additional connection is distinct from the existing macroscopic response achievements.

[E1] NIST, *Femtosecond-Laser Frequency Combs for Optical Clocks*, https://www.nist.gov/programs-projects/femtosecond-laser-frequency-combs-optical-clocks (accessed 2026-10-22).

[E2] NIST, *Advancing Statistical Methods for Next-Generation Clock Networks*, https://www.nist.gov/programs-projects/advancing-statistical-methods-next-generation-clock-networks (accessed 2026-10-22). These sources support general metrology and uncertainty treatment; they are not WRRA validation evidence.

'''
tests=json.loads((ROOT/'test_results.json').read_text())
for lang,addition in [('KO',ko),('EN',en)]:
 old=src/f'MCC_3_0_Full_Book_{lang}_v0.28-r2.md';s=old.read_text()
 lines=s.splitlines();lines[2]=('## 개정판 v0.28-r3: 유한 주소와 실험 반증 명세 보완' if lang=='KO' else '## Revision v0.28-r3: finite addresses and experimental falsification')
 lines.insert(6,('**v0.28-r3 준비본.** v0.28-r2의 보완을 유지하고 122.1절과 H.7을 추가했다. 별도 DOI 출판은 아직 진행하지 않았다.\n' if lang=='KO' else '**Prepared revision v0.28-r3.** Retains the v0.28-r2 additions and adds Sections 122.1 and H.7. No separate DOI publication has been made.\n'))
 s='\n'.join(lines)+'\n'; marker='## 123' if lang=='KO' else '## Chapter 123'
 if marker not in s:
  import re
  candidates=re.findall(r'^#{1,3} .*123.*$',s,re.M);print(candidates);raise ValueError('marker')
 i=s.index(marker);s=s[:i]+addition+s[i:]
 title='## H.7 v0.28-r3: 실험 설계와 합성 자료 검증' if lang=='KO' else '## H.7 v0.28-r3: experimental design and synthetic-data verification'
 h=title+'\n\n'
 if lang=='KO': h+='검증 입력 → WRRA 고유 변환 → 산출값 → 반증조건 → 결론의 순서로 122.1절을 읽는다. 원전은 DOI 10.5281/zenodo.23380920의 보존 패키지에 있는 optical_model_v1_0이며, 입력 프로파일 SHA-256은 `8c53fb73b332db2805b7d614f166511094b54b3f1b2a291fbfdfe46312408d6b`다. 원전 해시 검사 29개, 기존 계산 17+11개, 새 설계 검사 '+str(tests['passed'])+'/'+str(tests['total'])+'개를 실제 실행했다. 아래 자료는 모두 합성 자료이며 실제 관측 판정이 아니다.\n\n'
 else:h+='Read Section 122.1 as verification inputs → WRRA-specific transformation → outputs → falsification conditions → conclusion. The source is optical_model_v1_0 in the preserved package for DOI 10.5281/zenodo.23380920. Input profile SHA-256: `8c53fb73b332db2805b7d614f166511094b54b3f1b2a291fbfdfe46312408d6b`. This revision executed 29 source-file hash checks, 17+11 inherited computational controls, and '+str(tests['passed'])+'/'+str(tests['total'])+' new design checks. All data below are synthetic; these are not observational verdicts.\n\n'
 h+='| Case | Q / error | Exit |\n|---|---|---:|\n'
 for case in tests['runs']:
  res=case['result'];h+=f"| {case['case']} | {res.get('Q',res.get('error',''))} | {case['exit_code']} |\n"
 h+=('\n종료코드 0은 해당 통계 조건에서 기각되지 않음, 1은 동결 분기 기각, 2는 입력 오류다. 오류 자료는 격리된 복사본에서 검사했다. `design.py`는 측정 설계·합성 자료를 생성하고, `verify_observations.py`는 실제 원천 프로파일로 예측을 다시 계산하여 기록의 공분산으로 검정한다. `test_design.py`가 정상·무신호·회복 누락 및 입력 훼손을 실행한다. 전체 패키지에는 실행 로그와 원전 코드를 보존했다. 이 추가 기능은 실험 분석 절차의 검증이며 전체 우주 모형이나 실험적 검증 완료가 아니다.\n' if lang=='KO' else '\nExit 0 means not rejected under the stated statistical conditions, 1 rejects the frozen branch, and 2 identifies invalid input. Malformed cases were tested in isolated copies. `design.py` produces the design and synthetic data; `verify_observations.py` recomputes predictions from the actual source profile and tests the recorded covariance; `test_design.py` executes nominal, no-signal, missing-revival, and malformed-input cases. The package retains logs and original code. This validates an analysis procedure, not an experimentally confirmed or wholly executed universe model.\n')
 s+='\n'+h
 (dst/f'MCC_3_0_Full_Book_{lang}_v0.28-r3.md').write_text(s)
 (dst/f'MCC_3_0_Full_Book_{lang}_v0.28-r2.md').unlink(missing_ok=True);(dst/f'MCC_3_0_Full_Book_{lang}_v0.28-r2.pdf').unlink(missing_ok=True)
 (ROOT/f'addition_{lang}.md').write_text(addition+h)
(dst/'review/render.sh').write_text((dst/'review/render.sh').read_text().replace('v0.28-r2','v0.28-r3'))
