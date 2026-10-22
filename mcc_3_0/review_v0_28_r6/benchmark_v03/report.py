from pathlib import Path
import csv,json,html,base64,hashlib,platform
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;O=P/'analysis';O.mkdir(exist_ok=True)
def read(p):return list(csv.DictReader(p.open()))
rows=read(P/'tuning/fits.csv')+read(P/'nfw_refined/fits.csv');models=['NFW_refined','WRRA_curvature_ML','WRRA_turnover_ML'];summary=[]
for m in models:
 for ph in ['full','interleaved','outer']:
  a=[x for x in rows if x['model']==m and x['phase']==ph];s={k:sum(float(x[k]) for x in a) for k in ['chi2','AIC','BIC','test_chi2','n_test','n_fit','k']};s.update(model=m,phase=ph,galaxies=len(a),boundary=sum(x['boundary']=='True' for x in a));s['chi2_dof']=s['chi2']/(s['n_fit']-s['k']);s['test_per_point']=s['test_chi2']/s['n_test'] if s['n_test'] else None;summary.append(s)
def write(path,rr):
 with path.open('w') as f:w=csv.DictWriter(f,fieldnames=rr[0]);w.writeheader();w.writerows(rr)
write(O/'clean_comparison.csv',summary)
# Paired galaxy bootstrap; descriptive stability after outcome-driven candidate choice.
rng=np.random.default_rng(20261022);boots=[]
for m in models[1:]:
 for ph in ['full','interleaved','outer']:
  a={x['galaxy']:x for x in rows if x['model']==m and x['phase']==ph};b={x['galaxy']:x for x in rows if x['model']==models[0] and x['phase']==ph};names=sorted(a)
  col='BIC' if ph=='full' else 'test_chi2';den='n_fit' if ph=='full' else 'n_test'
  dif=np.array([float(a[n][col])-float(b[n][col]) for n in names]);nn=np.array([float(a[n][den]) for n in names]);idx=rng.integers(0,len(names),(10000,len(names)));vals=dif[idx].sum(1)/nn[idx].sum(1)
  boots.append(dict(model=m,phase=ph,metric='delta_BIC_per_fit_point' if ph=='full' else 'delta_test_chi2_per_test_point',delta=float(dif.sum()/nn.sum()),lower95=float(np.quantile(vals,.025)),upper95=float(np.quantile(vals,.975)),galaxy_wins=int(sum(dif<0)),galaxies=len(names)))
write(O/'paired_bootstrap.csv',boots)
pp=read(P/'tuning/points.csv')+read(P/'nfw_refined/points.csv');names=sorted({p['galaxy'] for p in pp});colors={'NFW_refined':'#666666','WRRA_curvature_ML':'#245fc4','WRRA_turnover_ML':'#d06c16'}
fig,axs=plt.subplots(3,3,figsize=(13,10))
for name,ax in zip(names,axs.flat):
 p=[p for p in pp if p['galaxy']==name and p['phase']=='full' and p['model']==models[0]];r=[float(x['r']) for x in p]
 ax.errorbar(r,[float(x['v']) for x in p],[float(x['e']) for x in p],fmt='.',color='black',ms=3,label='SPARC')
 for m in models:
  q=[x for x in pp if x['galaxy']==name and x['phase']=='full' and x['model']==m];ax.plot([float(x['r']) for x in q],[float(x['pred']) for x in q],label=m.replace('_ML','').replace('_refined',''),c=colors[m],lw=1.2)
 ax.set(title=name,xlabel='R (kpc)',ylabel='V (km/s)');ax.grid(alpha=.15)
axs[0,0].legend(fontsize=7);fig.suptitle('All nine clean galaxies: full-data fits with reported observational errors');fig.tight_layout();fig.savefig(O/'clean_rotation.png',dpi=150);plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(11,4))
for ax,ph in zip(axs,['interleaved','outer']):
 for m in models:
  a=np.array([(float(p['pred'])-float(p['v']))/float(p['e']) for p in pp if p['model']==m and p['phase']==ph and p['test']=='True']);x=np.sort(abs(a));ax.step(x,np.arange(1,len(x)+1)/len(x),where='post',label=m.replace('_ML','').replace('_refined',''),c=colors[m])
 ax.set(xscale='log',xlabel='Absolute heldout residual / reported error',ylabel='Cumulative fraction',title=ph+' holdout');ax.grid(alpha=.15)
axs[0].legend(fontsize=8);fig.tight_layout();fig.savefig(O/'heldout_residuals.png',dpi=160);plt.close(fig)
# Point-level conditional predictions with frozen parameters, including every excluded observation.
write(O/'conditional_predictions.csv',[p for p in pp if p['test']=='True'])
base=json.loads((P/'fit/results/summary.json').read_text());outer=read(P/'outer_results/fits.csv');outs=[]
for sample in ['all','clean']:
 for model in ['WRRA_radial_ML','NFW_ML']:
  a=[x for x in outer if x['model']==model and (sample=='all' or x['clean']=='True')];n=sum(int(x['n_test']) for x in a);ch=sum(float(x['test_chi2']) for x in a);outs.append(dict(sample=sample,model=model,galaxies=len(a),n_test=n,test_chi2=ch,test_per_point=ch/n))
write(O/'outer_baseline.csv',outs)
text='''WRRA / 최소계산우주론 3.0 — 관측 정량 벤치마킹 v0.3

1. 검증 입력
기존 v0.2 코드를 보존한 복사본에서 149개 은하·3,150점의 네 모형 피팅을 다시 실행했다. 데이터는 SPARC Lelli, McGaugh & Schombert (2016), AJ 152,157. 원 자료 175개 은하에서 Q≤2, 경사각≥30도, 유효 관측점≥5를 적용한다. 고신뢰도 표본은 Q=1, 경사각40~80도, 거리 상대오차≤10%, 경사각 오차≤5도, 유효점≥10인 9개·257점이다. 이번 개선을 위해 표본이나 오차를 변경하지 않았다.
양쪽 모두 동일한 거리·경사각을 고정하고, 가스 기여와 별의 질량광도비 배율 s를 사용한다. disk M/L=0.5s, bulge M/L=0.7s이며 하나의 s로 연동한다. s의 허용 범위는 공통으로0.1~5, 양성 조건을 적용한다. 별 종족·색 자료를 별도로 피팅한 것은 아니다. 거리·경사각의 공분산과 내재 산포는 이번 우도에 포함하지 않았다.

2. WRRA 고유 변환
원래 공개된 유한 admission 응답을 그대로 실행한다: g=g_b/[1−exp(−sqrt(g_b/a_T))], V=sqrt(gR). 공통 부하에서 계산한 a_T0에 반경별 응력 계수를 연결한다.
기존 반경형: a_T=a_T0 A x^p, x=R/Rpivot.
추가 곡률형: a_T=a_T0 A exp[p ln x+q(ln x)^2].
추가 전환형: a_T=a_T0 A x^p(1+1/t)/(1+x/t).
곡률형은 응력 구배의 변화, 전환형은 특성 반경에서 완만하게 변하는 구배를 표현한다. 추가 규칙은 관측으로 보정한 현상론적 응력 응답이며 새 장 방정식이나 에너지 보존의 유도라고 표시하지 않는다. WRRA 내부 기존 response를 호출해 실제 속도를 계산한다.
두 후보는 은하당4변수(A,p,q 또는 t,s), NFW는3변수(V200,c,s)다. 추가 자유도를 모두 AIC/BIC에 반영한다. WRRA와 NFW 모두 27개 초기값으로 탐색한다. NFW도 동일한 최적화 허용오차·평가 횟수로 재검사했다.
이번 후보 선택은 기존 고신뢰도 결과를 보고 시작한 탐색적 모형 개선이다. 미사용 우주/은하 자료로 검증했다고 표현하지 않는다. 모든 후보를 공개하며 가장 좋은 값만 선별해 하나의 모형 성과로 합치지 않는다.

3. 산출값
아래는 실제 재실행 결과다. χ²가 작을수록 잔차가 작고 AIC/BIC는 낮을수록 이 비교에서 유리하다. Gaussian 상수항을 공통 생략했으며 BIC는 은하별 χ²+k ln(n)의 합이다.
'''
text+='\n기존149개 전체 표본 재실행(3,150점):\n'
for x in base['summary']:
 if x['sample']=='all' and x['phase']=='full':text+=f"{x['model']}: χ²={x['chi2']:.6f}, AIC={x['AIC']:.6f}, BIC={x['BIC_block']:.6f}\n"
text+='\n기존 반경형 외곽20% 검사:\n'
for x in outs:text+=f"{x['sample']} {x['model']}: {x['galaxies']}개, {x['n_test']}점, test χ²={x['test_chi2']:.6f}, 점당={x['test_per_point']:.6f}\n"
text+='\n추가 고신뢰도 피팅:\n'
for s in summary:
 text+=f"{s['model']} | {s['phase']} | χ²={s['chi2']:.6f} | χ²/dof={s['chi2_dof']:.6f} | AIC={s['AIC']:.6f} | BIC={s['BIC']:.6f} | test χ²={s['test_chi2']:.6f}/{int(s['n_test'])}점 | 경계해={s['boundary']}\n"
text+='''
전체 고신뢰도 피팅에서는 두 신규 후보 모두 NFW보다 AIC/BIC가 낮다. 곡률형은 가장 강한 관측 곡선 재현을 보인다. 교차 간격 검사(정렬 후 매5번째 관측점)는 곡률형이 우수하고, 외곽20% 검사에서는 전환형이 우수하다. 곡률형은 외곽 예측에서 크게 악화되므로 관측 반경 밖의 일반 예측식으로 채택하지 않는다. 전환형도 교차 간격 검사에서는 NFW보다 나쁘다. 모든 검사에서 우월한 단일 모형을 확보했다고 결론내리지 않는다.
합산 우위와 은하별 우위는 다르다. 곡률형의 은하별 BIC 우위는3/9, 전환형은2/9이며, 은하 단위 bootstrap 구간은0을 포함한다. 따라서 고신뢰도 모집단 전반의 통계적으로 확정된 우위로 확대하지 않는다.
원래 자료의 오차막대를 그대로 사용했다. 대다수 총 χ²/dof가1보다 크므로 명시된 오차 수준에서 잔차가 모두 설명되지는 않았다. AIC/BIC의 국소 모형 간 비교와 절대 적합성을 구별한다.

은하 단위 paired bootstrap 10,000회(seed20261022): 아래는 WRRA−NFW의 점당 차이, 95% percentile 구간이다. 음수가 WRRA 우위다. 9개 표본 재표집의 기술 통계이며 모형 탐색 선택효과나 체계오차를 보정한 확증 구간이 아니다.
'''
for b in boots:text+=f"{b['model']} {b['phase']}: {b['delta']:.6f} [{b['lower95']:.6f}, {b['upper95']:.6f}], 은하별 우위 {b['galaxy_wins']}/9\n"
text+='''
WRRA 조건부 예측: 피팅 단계에서 뺀 각 관측점의 R, V예측, V관측, 관측오차를 conditional_predictions.csv에 저장했다. 검증 입력으로 확정된 계수를 WRRA 내부 응답에 넣은 산출값이다. 여기서는 이미 측정된 값을 가린 예측 검사이며 아직 미측정된 물리량의 관측 확인으로 표시하지 않는다. 실제 향후 관측에는 계수 동결·바리온 분포 입력·오차 전파가 필요하다.

4. 반증조건
동일 관측값·오차·분할이 아니면 비교 실패. 저장된 예측을 모형식으로 재계산해 불일치하면 실패. 관측값을 원 SPARC 장부와 대조해 변경되면 실패. 추가 변수 개수를 누락하거나 AIC/BIC가 다시 계산되지 않으면 실패. 표본을 바꿔 우위를 만들면 이번 고신뢰도 비교로 인정하지 않는다.
기존 1,056개 fit 행·24,188개 예측 행을 독립 matrix-exponential 응답으로 검증했다. 외곽검사230개 fit·5,794개 예측은 원 관측 장부와 독립식으로 대조했다. 신규 WRRA54개 fit·1,542개 예측, NFW27개 fit·771개 예측도 독립식으로 대조했다. 실제 검사 로그는 runs/와 각 verification.json에 있다.
의도적 훼손은 임시 복사본에서만 실행한다. 관측값·예측·행 삭제·분할·총합 오류 5건, 신규 모형의 예측·중복·자유도 오류3건, 기존 holdout 예측 오류1건을 검사한다. 통과 여부는 동봉 실제 로그를 따른다.

5. 결론
고신뢰도 표본에서 NFW 대비 피팅 우위(추가 자유도 페널티 포함)를 실제로 확보했다. 곡률형은 정량 재현 보강 후보, 전환형은 외곽 예측에 유리한 후보로 구분한다. 이 결과는 WRRA의 응력→유한응답→회전속도 연결을 관측으로 보정한 설명 성과다. NFW는 여기서 자유 halo 비교 모형이며 ΛCDM 전체 우도는 아니다.
본 패키지는 회전 곡선 벤치마킹이다. 은하단 렌즈, CMB, BTFR 별도 회귀의 실행 완료로 확대하지 않는다. 공개된3.0 전체본에는 아직 이번 변경을 반영하지 않았다.

재현 명령(패키지 디렉터리에서):
python fit/fit.py
python fit/test_controls.py
python outer.py
python test_outer.py
python tune.py
python refine_nfw.py
python verify_tuning.py
python verify_tuning.py nfw_refined
python test_tuning.py
python report.py

출처: https://astroweb.cwru.edu/SPARC/
원 논문: https://doi.org/10.3847/0004-6256/152/6/157
기존 WRRA 코드 계보: baseline_v01/results 또는 원본 소스, 기존 source_commit 8358c887d09de385ca7d6487e1ffcffa0557a91c. 이번 변경은 미커밋된 별도 패키지이며 파일별 SHA256으로 고정한다.
'''
(P/'REPORT_KO.txt').write_text(text);(P/'BOOK_INSERT_KO.txt').write_text('관측 정량 벤치마킹 보강 — 본문 반영 후보\n\n'+text)
parts=['<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>WRRA 관측 벤치마킹 v0.3</title><style>body{font-family:system-ui,sans-serif;max-width:1050px;margin:24px auto;padding:0 16px;line-height:1.7;color:#17283c}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-family:inherit}img{width:100%;height:auto}table{border-collapse:collapse;font-size:14px}td,th{padding:8px;border:1px solid #ccd} .scroll{overflow:auto}</style><h1>WRRA 관측 정량 벤치마킹 v0.3</h1><p>고신뢰도 표본: 9개 은하 · 257개 관측점</p><div class="scroll"><table><tr><th>전체 피팅</th><th>χ²</th><th>AIC</th><th>BIC</th></tr>']
for s in summary:
 if s['phase']=='full':parts.append('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in [s['model'],round(s['chi2'],2),round(s['AIC'],2),round(s['BIC'],2)])+'</tr>')
parts.append('</table></div>')
for image in ['clean_rotation.png','heldout_residuals.png']:parts.append('<img src="data:image/png;base64,'+base64.b64encode((O/image).read_bytes()).decode()+'">')
parts.append('<pre>'+html.escape(text)+'</pre></html>');(P/'REPORT_KO.html').write_text(''.join(parts))
print(json.dumps(dict(clean_summary=summary,bootstrap=boots,outer_baseline=outs),indent=2))
