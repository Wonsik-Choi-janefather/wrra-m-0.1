from pathlib import Path
import tempfile,shutil,subprocess,sys,csv,json
import numpy as np
import fit
P=Path(__file__).resolve().parent
data,meta,clean=fit.getdata();d=next(iter(data.values()));pivot=np.median(d['r']);native=fit.b.wrra(d);candidate=fit.predict(d,'WRRA_radial_ML',[0.,0.,0.],pivot);assert np.allclose(native,candidate,rtol=1e-13)
# Synthetic nonconstant radial source; recover generated curve and parameters.
r=np.geomspace(.3,40,40);d={'r':r,'gas':100*r/(1+r),'stars':4000*r/(r+3)**2,'e':np.ones(len(r))};p=np.array([.3,-.4,-.1]);pivot=float(np.median(r));d['v']=fit.predict(d,'WRRA_radial_ML',p,pivot);f,_,_=fit.fit(d,'WRRA_radial_ML',pivot,.1);assert np.max(abs(f.x-p))<1e-5
normal=subprocess.run([sys.executable,str(P/'verify.py')],capture_output=True,text=True);assert normal.returncode==0,normal.stderr
with tempfile.TemporaryDirectory() as td:
 q=Path(td)/'results';shutil.copytree(P/'results',q);csvp=q/'predictions.csv';rows=list(csv.DictReader(csvp.open()));row=next(r for r in rows if r['test']=='True');row['pred']=str(float(row['pred'])+10)
 with csvp.open('w',newline='') as out:
  w=csv.DictWriter(out,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 bad=subprocess.run([sys.executable,str(P/'verify.py'),str(q)],capture_output=True,text=True);assert bad.returncode!=0 and 'PREDICTION_REPLAY_MISMATCH' in bad.stderr
 result={'normal_exit':normal.returncode,'normal':json.loads(normal.stdout),'native_nested_recovery':True,'synthetic_radial_parameter_max_error':float(np.max(abs(f.x-p))),'heldout_corruption_exit':bad.returncode,'heldout_corruption_error':'PREDICTION_REPLAY_MISMATCH','reported_totals_unchanged':True}
 (P/'results/verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
