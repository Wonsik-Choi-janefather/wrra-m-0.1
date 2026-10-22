from pathlib import Path
import sys,json,itertools
import numpy as np
from scipy.optimize import least_squares
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'fit'));import fit as f
D,meta,clean=f.getdata();rows=[];points=[]
for name in sorted(clean):
 d=D[name];n=len(d['r']);lo=np.log10([5,.1,f.b.star_lower(d)]);hi=np.log10([1000,100,5])
 for phase in ['full','interleaved','outer']:
  test=np.zeros(n,dtype=bool) if phase=='full' else (np.arange(n)%5==4 if phase=='interleaved' else np.arange(n)>=n-int(np.ceil(.2*n)))
  train={k:v[~test] for k,v in d.items()};runs=[]
  for v,c,s in itertools.product([30,100,300],[1,10,50],[.2,1,3]):
   r=least_squares(lambda p:(f.b.nfw(train,p,True)-train['v'])/train['e'],np.clip(np.log10([v,c,s]),lo+1e-7,hi-1e-7),bounds=(lo,hi),ftol=1e-10,xtol=1e-10,gtol=1e-10,max_nfev=3000);runs.append(r)
  r=min(runs,key=lambda r:sum(r.fun*r.fun));pred=f.b.nfw(d,r.x,True);chi=((pred-d['v'])/d['e'])**2;nt=sum(~test)
  rows.append(dict(galaxy=name,model='NFW_refined',phase=phase,k=3,n_fit=nt,n_test=sum(test),chi2=sum(chi[~test]),test_chi2=sum(chi[test]),AIC=sum(chi[~test])+6,BIC=sum(chi[~test])+3*np.log(nt),params=json.dumps(r.x.tolist()),pivot=float(np.median(train['r'])),boundary=bool(np.any(np.minimum(r.x-lo,hi-r.x)<1e-4)),success=bool(r.success)))
  for j in range(n):points.append(dict(galaxy=name,model='NFW_refined',phase=phase,j=j,test=bool(test[j]),r=d['r'][j],v=d['v'][j],e=d['e'][j],gas=d['gas'][j],stars=d['stars'][j],pred=pred[j]))
(P/'nfw_refined').mkdir(exist_ok=True);f.b.writecsv(P/'nfw_refined/fits.csv',rows);f.b.writecsv(P/'nfw_refined/points.csv',points);print('DONE',len(rows))
