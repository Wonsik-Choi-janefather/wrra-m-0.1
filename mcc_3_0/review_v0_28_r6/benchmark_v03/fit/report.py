from pathlib import Path
import json,csv,base64,hashlib,zipfile,html
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
s=json.loads((P/'results/summary.json').read_text());d=json.loads((P/'results/diagnostics.json').read_text());v=json.loads((P/'results/verification.json').read_text());rr=s['summary']
labels={'WRRA_native_ML':'WRRA 기존 척도 + 은하별 M/L','WRRA_amplitude_ML':'WRRA 은하별 진폭 + M/L','WRRA_radial_ML':'WRRA 시험용 반경 구배 + M/L','NFW_ML':'NFW 헤일로 + M/L'}
def get(sample,phase,model):return next(r for r in rr if r['sample']==sample and r['phase']==phase and r['model']==model)
def table(sample,phase):
 rows=[r for r in rr if r['sample']==sample and r['phase']==phase]
 out='<div class="scroll"><table><tr><th>모형</th><th>은하</th><th>k</th><th>χ²/ν</th><th>AIC</th><th>BIC(은하별 합)</th><th>미사용점 χ²/N</th><th>경계해</th></tr>'
 for r in rows:
  vals=[labels[r['model']],r['galaxies'],r['k'],f"{r['chi2_dof']:.4f}",f"{r['AIC']:.2f}",f"{r['BIC_block']:.2f}",f"{r['test_chi2_per_point']:.4f}" if r['test_N'] else '—',r['boundaries']]
  out+='<tr>'+''.join('<td>'+str(x)+'</td>' for x in vals)+'</tr>'
 return out+'</table></div>'
fig,axs=plt.subplots(1,3,figsize=(12,4))
for ax,sample,phase,col,title in zip(axs,['all','all','clean'],['full','train','full'],['chi2_dof','test_chi2_per_point','chi2_dof'],['All: full fit (149 galaxies)','All: held-out (115 galaxies)','Clean: full fit (9 galaxies)']):
 a=[get(sample,phase,m)[col] for m in ['WRRA_radial_ML','NFW_ML']];ax.bar(['WRRA radial','NFW'],a,color=['#178b82','#d18b38']);ax.set(title=title,ylabel='chi-square / dof' if phase=='full' else 'held-out chi-square / point',ylim=(0,max(a)*1.25))
 for i,x in enumerate(a):ax.text(i,x+.08,f'{x:.3f}',ha='center')
fig.tight_layout();fig.savefig(P/'results/comparison.png',dpi=180);plt.close(fig)
img=base64.b64encode((P/'results/comparison.png').read_bytes()).decode()
fw=get('all','full','WRRA_radial_ML');fn=get('all','full','NFW_ML');tw=get('all','train','WRRA_radial_ML');tn=get('all','train','NFW_ML')
influence=d['sum_delta_chi2_WRRA_minus_NFW']-sum(x[1] for x in d['largest_WRRA_advantages'][:2])
report=f'''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>WRRA SPARC 피팅 v0.2</title><style>body{{max-width:1100px;margin:30px auto;padding:0 20px;font-family:Arial,'Noto Sans KR',sans-serif;line-height:1.8;color:#172e40}}h1,h2{{line-height:1.35}}h2{{margin-top:32px}}table{{border-collapse:collapse;width:100%;font-size:14px}}th,td{{border:1px solid #c7d5dc;padding:8px;text-align:right}}th:first-child,td:first-child{{text-align:left}}.scroll{{overflow-x:auto}}img{{width:100%}}.note{{padding:20px;background:#edf5f5}}code{{overflow-wrap:anywhere}}</style>
<h1>WRRA–SPARC 피팅 v0.2<br>은하별 질량·진폭·반경 구배의 단계적 조정</h1><p>2026-10-22 · 기존 v0.1을 보존한 후속 시험 · 3.0 v0.28-r1의 중력 응답 함수 사용</p>
<h2>1. 검증 입력</h2><p>동일한 공식 SPARC 자료와 v0.1 선택 기준의 149개 은하·3,150개 점을 사용했다. 거리·경사각·기체 기여는 고정하고, 별질량의 공통 배율 s를 은하별로 피팅한다. 원반 M/L=0.5s, 팽대부 M/L=0.7s이다. <b>은하별 M/L 피팅은 v0.1에도 이미 있었다.</b> 이번에 새로 추가한 것은 은하별 응답 진폭 A와 반경 지수 p이다. 원반과 팽대부 M/L을 별도로 푼 것은 아니며, 현재 자료에 없는 색지수·별 종족을 측정한 것으로 간주하지 않는다.</p>
<p>결과를 보기 전에 PROTOCOL.json에 모형·경계·표본·검증 분할을 고정했다. 고신뢰도 표본은 Q=1, 경사각 40–80°, 거리 상대오차 ≤10%, 경사각 오차 ≤5°, 유효 점 ≥10으로 정의해 9개 은하·257개 점이 남았다. Q는 품질 지표로 활용했으며 새로 회전곡선 대칭성을 측정하지 않았다. 선택 은하: {', '.join(s['clean_galaxies'])}.</p>
<p>검증점 분리에는 점이 10개 이상인 115개 은하를 사용했다. 반경순 정렬 후 매 5번째 점을 제외하여 2,358개 점으로 피팅하고 539개 점을 평가했다. 고신뢰도 표본의 경우 209개 훈련점·48개 검증점이다. 이는 같은 은하 내 보간 진단이며, 독립 은하나 새 관측에 대한 외부 검증이 아니다. v0.1에서 전체 자료를 이미 봤으므로 완전히 눈가림된 검증도 아니다.</p>
<h2>2. WRRA 고유 변환과 새 가정</h2><p>기존 D부하에서 구한 aT₀={s['aT_native']:.15g} m/s²와 유한 게이트 함수는 보존했다. 시험용 확장식은 다음과 같다.</p><pre>aT(R) = aT₀ × A × (R/Rpivot)^p
Rpivot = 각 은하의 관측 반경 중앙값 (피팅 변수 아님)
σ = sqrt(gb/aT(R)); μ = 1 − exp(−σ)
g = gb/μ; V = sqrt(Rg)
uD(R)/uD₀ = A² × (R/Rpivot)^(2p)</pre>
<p>A는 유효 국소 부하 진폭, p는 반경 의존성이다. A=1,p=0이면 기존 응답으로 정확히 돌아간다. A만 허용하는 2변수 중간 단계도 실행했다. <b>이 반경식은 이번에 도입한 현상론적 후보</b>이며 기존 SOURCE에서 필연적으로 도출된 응력 법칙이 아니다. 기존 게이트·자원 소유 관계를 유지한 관측 보정 후보로 평가한다. 전역 부하 예산·응력 보존·렌즈 응답은 새 식에 대해 아직 닫히지 않았다. R→0 또는 무한 반경으로 외삽하지 않는다.</p>
<p>시험 경계는 A∈[0.01,100], p∈[−2,2], s∈[0.1,5]이며 바리온 가속도의 양성을 보장하는 하한은 양쪽 모형에 동일하게 적용했다. 이 폭은 탐색을 위한 규약이며 별 종족으로 입증된 허용 범위가 아니다. NFW는 V200∈[5,1000] km/s, c∈[0.1,100], 동일한 s를 사용했다. 반경 확장 WRRA와 NFW는 모두 은하당 3개 변수, 9개 시작점을 사용했다. 모든 최적화가 성공을 반환했지만 전역 최적성의 증명은 아니다.</p>
<h2>3. 산출값</h2><p>전체 피팅에서 WRRA 확장식 χ²={fw['chi2']:.3f}, NFW χ²={fn['chi2']:.3f}. 두 모형 모두 k=447, ν=2,703이다. WRRA의 조건부 χ²는 {(1-fw['chi2']/fn['chi2'])*100:.2f}% 낮았다. 검증점 χ²는 각각 {tw['test_chi2']:.3f}, {tn['test_chi2']:.3f}로 WRRA가 {(1-tw['test_chi2']/tn['test_chi2'])*100:.2f}% 낮았다.</p>
<h3>전체 표본 · 전체 점 피팅</h3>{table('all','full')}<h3>전체 표본 · 분리한 검증점 평가</h3>{table('all','train')}<h3>고신뢰도 표본 · 전체 점 피팅</h3>{table('clean','full')}<h3>고신뢰도 표본 · 분리한 검증점 평가</h3>{table('clean','train')}
<figure><img src="data:image/png;base64,{img}"><figcaption>변수 3개씩인 모형의 직접 비교. 전체에서는 WRRA 확장식이 낮지만 고신뢰도 표본에서는 NFW가 낮다.</figcaption></figure>
<p>AIC=χ²+2k. 은하마다 서로 다른 변수를 갖기 때문에 주 BIC는 Σ[χ²ᵢ+kᵢ ln nᵢ]로 계산했다. v0.1의 전역 N을 쓰는 BIC와 숫자를 혼용하지 않는다. 변수 수가 같은 WRRA 확장식과 NFW 사이에서는 어느 방식이든 페널티가 같아 χ² 차이가 그대로 남는다. 소표본·경계해·은하 내 오차 상관 때문에 정식 베이즈 증거로 해석하지 않는다.</p>
<p>은하별로는 WRRA 확장식이 81개, NFW가 68개에서 χ²가 낮다. 은하별 Δχ²(WRRA−NFW)의 중앙값은 {d['median_galaxy_delta_chi2_WRRA_minus_NFW']:.3f}이다. 전체 Δχ²={d['sum_delta_chi2_WRRA_minus_NFW']:.3f} 중 IC2574와 UGC06787의 기여가 크다. 두 은하의 기여를 빼는 영향도 계산에서는 합이 +{influence:.3f}으로 바뀐다. 이는 원 표본에서 두 은하를 삭제해 재선정한 결과가 아니라, 우세의 집중도를 드러내는 합계 분해다.</p>
<p>확장식 A의 최소/중앙/최대는 {d['A_min_median_max'][0]:.3g}/{d['A_min_median_max'][1]:.3g}/{d['A_min_median_max'][2]:.3g}, p는 {d['p_min_median_max'][0]:.3g}/{d['p_min_median_max'][1]:.3g}/{d['p_min_median_max'][2]:.3g}, s는 {d['stellar_scale_min_median_max'][0]:.3g}/{d['stellar_scale_min_median_max'][1]:.3g}/{d['stellar_scale_min_median_max'][2]:.3g}이다. 넓은 폭과 27개의 경계해는 이 수치를 정밀한 물리량 추정으로 확정하기 어렵게 한다. NFW에도 68개 경계해가 있다.</p>
<h2>4. 반증조건과 실행 검사</h2><p>변수 추가 효과가 페널티나 검증점에서 사라지는지, 표본 선택에 따라 역전되는지, 원래 게이트·양성·단위를 위반하는지 검사한다. 고신뢰도 표본에서는 실제로 NFW 우세가 나타났다. 현재 전체 χ²/ν도 1보다 커서 관측 오차만으로 완전히 설명했다고 판정하지 않는다. 오차가 큰 점은 χ²에서 낮은 가중치를 받으므로 큰 오차의 자료가 자동으로 피팅을 지배한다고 해석하지 않는다.</p>
<p>별도 verify.py는 저장된 {v['normal']['prediction_rows']:,}개 예측 행, {v['normal']['fit_rows']:,}개 피팅 기록, {v['normal']['summary_rows']}개 요약을 읽어 WRRA 게이트를 전이행렬 지수함수로 재계산한다. NFW도 저장 파라미터에서 독립 재계산한다. χ², AIC, BIC, 검증점 분할을 대조했다. A=1,p=0 원모형 복원과 합성 반경식의 파라미터 복원도 통과했다.</p>
<p>격리 복사본의 검증점 예측속도를 10 km/s 바꾸고 보고 총합을 그대로 두자 <code>PREDICTION_REPLAY_MISMATCH</code>와 종료코드 1로 탐지했다. 정상 검증은 종료코드 0이다. 프로토콜 해시: <code>{s['protocol_sha256']}</code>. 실제 명령과 출력은 fit.log 및 verification.log에 보존한다.</p>
<h2>5. 결론</h2><p class="note">피팅을 확장할 필요가 있다는 제안은 이번 계산에서 효과를 보였다. 기존 구조를 유지하며 은하별 진폭과 반경 구배를 조정한 후보는 동일한 변수 수의 NFW보다 전체 표본의 조건부 χ²·AIC·BIC와 검증점 오차가 낮았다. 그러나 고신뢰도 표본에서는 순서가 역전되고 소수 은하의 기여가 크다. 따라서 결론은 ‘유망한 반경 보정 후보 확보’이며 ‘확정된 WRRA가 모든 표본에서 NFW를 능가한다’는 것은 아니다.</p>
<p>다음 물리적 보완은 A,p를 은하의 관측 구조와 공통 부하 규칙에 연결하고, 거리·경사각 및 별 종족에 근거한 M/L 제약을 함께 적용하는 것이다. 관측값을 이용한 보정은 정당한 모형 구성이며, 그 보정 규칙과 적용 범위를 명시한 뒤 평가하면 된다. 3.0 공개 본문과 외부 게시물은 이번 시험에서 변경하지 않았다.</p>
<h2>재현</h2><pre>python fit.py
python verify.py
python test_controls.py
python report.py</pre><p>Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, matplotlib. baseline_v01에 기존 코드·입력·결과를 보존했다. PROTOCOL.json, 결과 CSV, 실행 로그, 검사 코드 및 SHA256SUMS.json을 동봉했다. report.py는 실행한 결과에서 표와 그림을 생성한다.</p>
<p>출처: <a href="https://astroweb.cwru.edu/SPARC/">SPARC 공식 자료</a>; <a href="https://arxiv.org/abs/1803.00022">Li et al. (2018), Fitting the radial acceleration relation to individual SPARC galaxies</a>; <a href="https://arxiv.org/abs/astro-ph/9611107">Navarro, Frenk &amp; White (1997)</a>; <a href="https://zenodo.org/records/23549809">MCC 3.0 v0.28-r1</a>.</p></html>'''
(P/'WRRA_SPARC_Radial_Fit_v0.2_KO.html').write_text(report)
(P/'README.txt').write_text('WRRA SPARC radial-response candidate v0.2\nRun: python fit.py; python verify.py; python test_controls.py; python report.py\nSee PROTOCOL.json for pre-fit choices. This is a new phenomenological candidate, not an established field-law derivation. Original finite gate imported unchanged from baseline_v01/wrra_original/compute.py.\nFull and clean samples and held-out results are all retained. No external publication was performed.\n')
files=[f for f in P.rglob('*') if f.is_file() and '__pycache__' not in str(f) and f.name!='SHA256SUMS.json']
(P/'SHA256SUMS.json').write_text(json.dumps({str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(files)},indent=2)+'\n')
with zipfile.ZipFile(P.parent/'WRRA_SPARC_Radial_Fit_v0.2.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(P.rglob('*')):
  if f.is_file() and '__pycache__' not in str(f):z.write(f,str(f.relative_to(P)))
print('Report, chart and package built')
