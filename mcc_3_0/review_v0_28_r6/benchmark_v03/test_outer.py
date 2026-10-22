from pathlib import Path
import csv,subprocess,sys,tempfile,shutil,json
P=Path(__file__).resolve().parent
r=subprocess.run([sys.executable,str(P/'verify_outer.py')],capture_output=True,text=True);assert r.returncode==0,r.stdout+r.stderr
out={'normal':json.loads(r.stdout),'corruptions':[]}
for mode in ['prediction','observed_value','delete_row','split','summary']:
 with tempfile.TemporaryDirectory() as t:
  q=Path(t)/'data';shutil.copytree(P/'outer_results',q)
  path=q/('fits.csv' if mode=='summary' else 'points.csv');rows=list(csv.DictReader(path.open()));fields=list(rows[0])
  if mode=='prediction':rows[-1]['pred']=str(float(rows[-1]['pred'])+1)
  elif mode=='observed_value':rows[-1]['v']=str(float(rows[-1]['v'])+1)
  elif mode=='delete_row':rows.pop()
  elif mode=='split':rows[-1]['partition']='train'
  else:rows[0]['test_chi2']=str(float(rows[0]['test_chi2'])+1)
  with path.open('w') as o:w=csv.DictWriter(o,fieldnames=fields);w.writeheader();w.writerows(rows)
  r=subprocess.run([sys.executable,str(P/'verify_outer.py'),str(q)],capture_output=True,text=True)
  assert r.returncode!=0,(mode,r.stdout)
  out['corruptions'].append(dict(case=mode,exit=r.returncode,error=r.stdout.strip()))
(P/'outer_results/verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
