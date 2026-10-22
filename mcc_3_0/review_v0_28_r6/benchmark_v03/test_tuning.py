from pathlib import Path
import sys,json,tempfile,shutil,csv,subprocess
import numpy as np
import tune
P=Path(__file__).resolve().parent
r=np.geomspace(.3,40,40);d=dict(r=r,gas=100*r/(1+r),stars=4000*r/(r+3)**2,e=np.ones(40));pivot=float(np.median(r));recover=[]
for m,p in [('WRRA_curvature_ML',[.3,-.4,-.1,-.1]),('WRRA_turnover_ML',[.3,-.4,0.,-.1])]:
 d['v']=tune.predict(d,m,p,pivot);f,_=tune.fit(d,m,pivot,.1);err=float(np.max(abs(f.x-p)));assert err<1e-5;recover.append(dict(model=m,max_parameter_error=err))
records=[]
for mode in ['prediction','duplicate','penalty']:
 with tempfile.TemporaryDirectory() as t:
  q=Path(t)/'tuning';shutil.copytree(P/'tuning',q);path=q/('fits.csv' if mode=='penalty' else 'points.csv');rr=list(csv.DictReader(path.open()));fields=list(rr[0])
  if mode=='prediction':rr[-1]['pred']=str(float(rr[-1]['pred'])+10)
  elif mode=='duplicate':rr[-1]=rr[-2].copy()
  else:rr[0]['k']='3'
  with path.open('w') as o:w=csv.DictWriter(o,fieldnames=fields);w.writeheader();w.writerows(rr)
  z=subprocess.run([sys.executable,str(P/'verify_tuning.py'),str(q)],capture_output=True,text=True);assert z.returncode!=0;records.append(dict(case=mode,exit=z.returncode,error=z.stdout.strip()))
out=dict(synthetic=recover,corruptions=records);(P/'tuning/verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
