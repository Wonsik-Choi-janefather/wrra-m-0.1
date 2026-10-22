from pathlib import Path
import json,subprocess,sys,tempfile,shutil,csv
import numpy as np
import run
P=Path(__file__).resolve().parent
# Physical unit and NFW normalization checks, including nontrivial synthetic recovery.
for v,c in [(30,2),(100,10),(300,30)]:
 r200=v/(10*.0674);assert abs(run.nfw_v2(np.array([r200]),v,c)[0]/v**2-1)<1e-12
r=np.geomspace(.1,100,60);d=dict(r=r,gas=np.zeros(60),stars=np.zeros(60),e=np.ones(60));d['v']=np.sqrt(run.nfw_v2(r,130,8));f,b=run.halo_fit(d);assert np.max(abs(10**f.x/np.array([130,8])-1))<1e-6
normal=subprocess.run([sys.executable,str(P/'verify.py')],capture_output=True,text=True);assert normal.returncode==0,normal.stderr
with tempfile.TemporaryDirectory() as td:
 q=Path(td)/'results';shutil.copytree(P/'results',q);p=q/'point_predictions.csv';rows=list(csv.DictReader(p.open()));rows[0]['predicted_km_s']=str(float(rows[0]['predicted_km_s'])+10)
 with p.open('w',newline='') as out:
  w=csv.DictWriter(out,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 bad=subprocess.run([sys.executable,str(P/'verify.py'),str(q)],capture_output=True,text=True);assert bad.returncode!=0 and 'RESIDUAL_MISMATCH' in bad.stderr
 result=dict(normal_exit=normal.returncode,normal=json.loads(normal.stdout),nfw_r200_normalization_cases=3,synthetic_nfw_recovered=(10**f.x).tolist(),isolated_prediction_corruption_exit=bad.returncode,isolated_error='RESIDUAL_MISMATCH',reported_total_unchanged=True)
 (P/'results/verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
