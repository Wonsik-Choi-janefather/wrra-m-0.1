from pathlib import Path
import subprocess,json,math,sys
B=Path(__file__).resolve().parent
def same(a,b):
 if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 if isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float)):return math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-12)
 return a==b
rows=[]
for p in sorted((B/'studies').glob('*/compute.py')):
 before=json.loads((p.parent/'results.json').read_text())
 run=subprocess.run([sys.executable,str(p)],capture_output=True,text=True)
 after=json.loads((p.parent/'results.json').read_text())
 row={'study':p.parent.name,'exit':run.returncode,'agrees':same(before,after)};rows.append(row);print(row)
p=B/'reference_fold_decay'/'compute.py';run=subprocess.run([sys.executable,str(p)],capture_output=True,text=True)
ref=json.loads((p.parent/'results.json').read_text());ok=run.returncode==0 and ref['verification']['all_passed']
print('reference_fold_decay',ok)
assert all(r['exit']==0 and r['agrees'] for r in rows) and ok
