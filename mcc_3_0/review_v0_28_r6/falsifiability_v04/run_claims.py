from pathlib import Path
import csv,json,subprocess,sys
P=Path(__file__).resolve().parent;(P/'cases').mkdir(exist_ok=True)
rows=list(csv.DictReader((P/'evidence/clean_comparison.csv').open()));bs=list(csv.DictReader((P/'evidence/paired_bootstrap.csv').open()));out=[]
for model in ['WRRA_curvature_ML','WRRA_turnover_ML']:
 for phase in ['full','interleaved','outer']:
  col='BIC' if phase=='full' else 'test_chi2'
  a=next(x for x in rows if x['model']==model and x['phase']==phase);b=next(x for x in rows if x['model']=='NFW_refined' and x['phase']==phase)
  d=dict(claim_id=model+'_'+phase,version='v0.3',kind='paired_advantage',scope='sample_aggregate',candidate_losses=[float(a[col])],reference_losses=[float(b[col])],same_inputs=True,same_errors=True,same_split=True,metric=col)
  for scope in ['sample_aggregate','population']:
   d=d.copy();d['scope']=scope
   if scope=='population':
    bb=next(x for x in bs if x['model']==model and x['phase']==phase);d['interval']=[float(bb['lower95']),float(bb['upper95'])];d['selection_adjusted']=False
    # Bootstrap interval is in per-point units; rescale delta inputs to match.
    denom=float(a['n_fit'] if phase=='full' else a['n_test']);d['candidate_losses']=[float(a[col])/denom];d['reference_losses']=[float(b[col])/denom]
   path=P/'cases'/(d['claim_id']+'_'+scope+'.json');path.write_text(json.dumps(d,indent=2));r=subprocess.run([sys.executable,str(P/'judge.py'),str(path)],capture_output=True,text=True);out.append(json.loads(r.stdout));assert r.returncode in [0,1,3]
(P/'claim_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
