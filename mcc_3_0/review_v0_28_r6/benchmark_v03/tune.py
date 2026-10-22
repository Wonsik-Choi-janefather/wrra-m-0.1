"""Exploratory, outcome-motivated response extension; same catalog and errors."""
from pathlib import Path
import sys,json,itertools
import numpy as np
from scipy.optimize import least_squares
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'fit'));import fit as f
MODELS={'WRRA_curvature_ML':4,'WRRA_turnover_ML':4}
def predict(d,model,p,pivot):
 x=d['r']/pivot
 if model=='WRRA_curvature_ML':logfactor=np.log(10)*p[0]+p[1]*np.log(x)+p[2]*np.log(x)**2
 else:logfactor=np.log(10)*p[0]+p[1]*np.log(x)-np.log1p(x/(10**p[2]))+np.log1p(1/(10**p[2]))
 return f.b.wrra(d,f.b.AT*np.exp(logfactor),10**p[3])
def fit(d,model,pivot,low):
 lo=np.array([-2,-2,-1 if model=='WRRA_curvature_ML' else -2,np.log10(low)]);hi=np.array([2,2,1 if model=='WRRA_curvature_ML' else 2,np.log10(5)])
 starts=[[*p,0] for p in itertools.product([-1,0,1],[-1,0,1],[-.5,0,.5])];runs=[]
 for p in starts:
  r=least_squares(lambda p:(predict(d,model,p,pivot)-d['v'])/d['e'],np.clip(p,lo+1e-7,hi-1e-7),bounds=(lo,hi),ftol=1e-10,xtol=1e-10,gtol=1e-10,max_nfev=3000);runs.append(r)
 r=min(runs,key=lambda x:sum(x.fun*x.fun));return r,bool(np.any(np.minimum(r.x-lo,hi-r.x)<1e-4))
def main():
 out=P/'tuning';out.mkdir(exist_ok=True);data,meta,clean=f.getdata();rows=[];points=[]
 protocol=dict(status='exploratory adaptation motivated by known clean-sample results; no pristine test-set claim',sample=sorted(clean),models=MODELS,curvature='aT=aT0*A*exp(p*ln(x)+q*ln(x)^2)',turnover='aT=aT0*A*x^p*(1+1/rt)/(1+x/rt)',bounds='A .01..100, p -2..2, q -1..1 or rt .01..100, stellar scale shared .1..5 positivity',selection='choose lowest full-sample clean BIC among two stated candidates; report all candidates and diagnostic holdouts',scope='new phenomenological stress-response closure; original admission response preserved; not yet global integration')
 (out/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2))
 for name in sorted(clean):
  d=data[name];n=len(d['r']);low=f.b.star_lower(d)
  for phase in ['full','interleaved','outer']:
   test=np.zeros(n,dtype=bool) if phase=='full' else (np.arange(n)%5==4 if phase=='interleaved' else np.arange(n)>=n-int(np.ceil(.2*n)))
   train={k:v[~test] for k,v in d.items()};pivot=float(np.median(train['r']))
   for model,k in MODELS.items():
    fitres,bound=fit(train,model,pivot,low);pred=predict(d,model,fitres.x,pivot);chi=((pred-d['v'])/d['e'])**2;nt=len(train['r'])
    rows.append(dict(galaxy=name,model=model,phase=phase,k=k,n_fit=nt,n_test=sum(test),chi2=sum(chi[~test]),test_chi2=sum(chi[test]),AIC=sum(chi[~test])+2*k,BIC=sum(chi[~test])+k*np.log(nt),params=json.dumps(fitres.x.tolist()),pivot=pivot,boundary=bound,success=bool(fitres.success)))
    for j in range(n):points.append(dict(galaxy=name,model=model,phase=phase,j=j,test=bool(test[j]),r=d['r'][j],v=d['v'][j],e=d['e'][j],gas=d['gas'][j],stars=d['stars'][j],pred=pred[j]))
  print(name,'done',flush=True)
 f.b.writecsv(out/'fits.csv',rows);f.b.writecsv(out/'points.csv',points)
 print('DONE',len(rows))
if __name__=='__main__':main()
