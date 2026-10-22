from pathlib import Path
import sys,json,csv,hashlib,time,itertools
import numpy as np
from scipy.optimize import least_squares
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'baseline_v01'))
import run as b
MODELS={'WRRA_native_ML':1,'WRRA_amplitude_ML':2,'WRRA_radial_ML':3,'NFW_ML':3}

def predict(d,model,p,pivot):
 if model=='NFW_ML':return b.nfw(d,p,True)
 if model=='WRRA_native_ML':A,power,scale=1.,0.,10**p[0]
 elif model=='WRRA_amplitude_ML':A,power,scale=10**p[0],0.,10**p[1]
 else:A,power,scale=10**p[0],p[1],10**p[2]
 return b.wrra(d,b.AT*A*(d['r']/pivot)**power,scale)

def fit(d,model,pivot,low):
 ls=np.log10(low);hs=np.log10(5.)
 if model=='WRRA_native_ML':lo,hi,starts=[ls],[hs],[[0.]]
 elif model=='WRRA_amplitude_ML':lo,hi,starts=[-2,ls],[2,hs],[[a,0.] for a in [-1,0,1]]
 elif model=='WRRA_radial_ML':lo,hi,starts=[-2,-2,ls],[2,2,hs],[[a,p,0.] for a in [-1,0,1] for p in [-1,0,1]]
 else:lo,hi,starts=np.log10([5,.1,low]),np.log10([1000,100,5]),[np.log10([v,c,1]) for v in [30,100,300] for c in [1,10,50]]
 lo=np.array(lo);hi=np.array(hi);fits=[]
 for x in starts:
  f=least_squares(lambda p:(predict(d,model,p,pivot)-d['v'])/d['e'],np.clip(x,lo+1e-7,hi-1e-7),bounds=(lo,hi),ftol=1e-10,xtol=1e-10,gtol=1e-10,max_nfev=2000)
  fits.append(f)
 f=min(fits,key=lambda f:sum(f.fun*f.fun));return f,bool(np.any(np.minimum(f.x-lo,hi-f.x)<1e-4)),len(starts)

def getdata():
 data,selection=b.load();meta={}
 for l in (P/'baseline_v01/inputs/SPARC_Lelli2016c.mrt').read_text().splitlines():
  a=l.split()
  if a and a[0] in data:meta[a[0]]=dict(D=float(a[2]),eD=float(a[3]),inc=float(a[5]),einc=float(a[6]),Q=int(a[17]))
 clean=set()
 for name,d in data.items():
  order=np.argsort(d['r'],kind='stable');data[name]={k:v[order] for k,v in d.items()};m=meta[name]
  if m['Q']==1 and 40<=m['inc']<=80 and m['eD']/m['D']<=.1 and m['einc']<=5 and len(d['r'])>=10:clean.add(name)
 return data,meta,clean

def main():
 out=P/'results';out.mkdir(exist_ok=True);data,meta,clean=getdata();records=[];points=[];split=[]
 for idx,(name,d) in enumerate(data.items()):
  n=len(d['r']);pivot=float(np.median(d['r']));low=b.star_lower(d)
  test=np.arange(n)%5==4;eligible=n>=10
  for j in range(n):split.append(dict(galaxy=name,point=j,r_kpc=d['r'][j],clean=name in clean,cv_eligible=eligible,partition=('test' if test[j] else 'train') if eligible else 'not_eligible'))
  for phase in ['full']+(['train'] if eligible else []):
   used=d if phase=='full' else {k:v[~test] for k,v in d.items()}
   for model,k in MODELS.items():
    f,bound,starts=fit(used,model,pivot,low);pred=predict(d,model,f.x,pivot)
    chi=float(sum(((predict(used,model,f.x,pivot)-used['v'])/used['e'])**2));nt=len(used['r']);testchi=float(sum(((pred[test]-d['v'][test])/d['e'][test])**2)) if phase=='train' else None
    records.append(dict(galaxy=name,clean=name in clean,phase=phase,model=model,k=k,n_fit=nt,chi2=chi,dof=nt-k,chi2_dof=chi/(nt-k),AIC=chi+2*k,BIC=chi+k*np.log(nt),n_test=int(test.sum()) if phase=='train' else 0,test_chi2=testchi,params=json.dumps(f.x.tolist()),pivot_kpc=pivot,stellar_lower=low,success=bool(f.success),boundary=bound,starts=starts))
    for j in range(n):points.append(dict(galaxy=name,phase=phase,model=model,point=j,r_kpc=d['r'][j],vobs=d['v'][j],error=d['e'][j],pred=pred[j],gas_v2=d['gas'][j],stars_v2=d['stars'][j],test=bool(test[j]) if phase=='train' else False))
  if (idx+1)%25==0:print(f'{idx+1}/{len(data)} galaxies finished',flush=True)
 b.writecsv(out/'fits.csv',records);b.writecsv(out/'predictions.csv',points);b.writecsv(out/'split.csv',split)
 b.writecsv(out/'sample_metadata.csv',[dict(galaxy=n,clean=n in clean,**m) for n,m in meta.items()])
 summaries=[]
 for sample in ['all','clean']:
  for phase in ['full','train']:
   for model in MODELS:
    rr=[r for r in records if r['phase']==phase and r['model']==model and (sample=='all' or r['clean'])]
    if not rr:continue
    chi=sum(r['chi2'] for r in rr);N=sum(r['n_fit'] for r in rr);k=sum(r['k'] for r in rr);tN=sum(r['n_test'] for r in rr);tc=sum(r['test_chi2'] or 0 for r in rr)
    summaries.append(dict(sample=sample,phase=phase,model=model,galaxies=len(rr),N=N,k=k,chi2=chi,chi2_dof=chi/(N-k),AIC=sum(r['AIC'] for r in rr),BIC_block=sum(r['BIC'] for r in rr),median_galaxy_chi2_dof=float(np.median([r['chi2_dof'] for r in rr])),test_N=tN,test_chi2=tc,test_chi2_per_point=tc/tN if tN else None,boundaries=sum(r['boundary'] for r in rr),failed=sum(not r['success'] for r in rr)))
 b.writecsv(out/'comparison.csv',summaries)
 result=dict(protocol_sha256=hashlib.sha256((P/'PROTOCOL.json').read_bytes()).hexdigest(),aT_native=b.AT,clean_galaxies=sorted(clean),summary=summaries,scope='New phenomenological radial-load candidate; original gate unchanged; conditional diagonal-error fits. No new field-law derivation, lensing or Planck likelihood.')
 (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
