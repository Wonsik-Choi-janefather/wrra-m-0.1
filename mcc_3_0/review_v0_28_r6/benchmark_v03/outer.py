"""Frozen outer-radius challenge, no tuning on test velocities."""
from pathlib import Path
import sys,json
import numpy as np
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'fit'))
import fit as f
out=P/'outer_results';out.mkdir(exist_ok=True)
data,meta,clean=f.getdata();rows=[];points=[]
for idx,(name,d) in enumerate(data.items()):
 n=len(d['r'])
 if n<10:continue
 cut=n-int(np.ceil(.2*n));train={k:v[:cut] for k,v in d.items()};pivot=float(np.median(train['r']))
 # Common positivity bound uses baryonic source components only, never heldout velocities.
 low=f.b.star_lower(d)
 for model in ['WRRA_radial_ML','NFW_ML']:
  fit,bound,starts=f.fit(train,model,pivot,low);pred=f.predict(d,model,fit.x,pivot)
  z=((pred-d['v'])/d['e'])**2
  rows.append(dict(galaxy=name,model=model,clean=name in clean,n_train=cut,n_test=n-cut,train_chi2=sum(z[:cut]),test_chi2=sum(z[cut:]),params=json.dumps(fit.x.tolist()),pivot=pivot,success=bool(fit.success),boundary=bound,stellar_lower=low))
  for j in range(n):points.append(dict(galaxy=name,model=model,j=j,partition='train' if j<cut else 'test',r=d['r'][j],v=d['v'][j],e=d['e'][j],gas=d['gas'][j],stars=d['stars'][j],pred=pred[j]))
 if (idx+1)%25==0:print(idx+1,flush=True)
f.b.writecsv(out/'fits.csv',rows);f.b.writecsv(out/'points.csv',points)
(out/'protocol.json').write_text(json.dumps(dict(split='largest ceil(0.2*n) radii held out, n>=10',pivot='median training radius',aT=float(f.b.AT),models=['WRRA_radial_ML','NFW_ML'],k_each=3,scope='same previously studied catalogue; new radial extrapolation diagnostic, not untouched external validation'),indent=2))
print('DONE',len(rows),'fits',len(points),'predictions')
