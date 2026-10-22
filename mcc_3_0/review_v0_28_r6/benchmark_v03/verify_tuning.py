from pathlib import Path
import sys,csv,json,math
import numpy as np
P=Path(__file__).resolve().parent;D=Path(sys.argv[1]) if len(sys.argv)>1 else P/'tuning'
def req(ok,msg):
 if not ok:raise ValueError(msg)
def close(a,b):return math.isclose(float(a),float(b),rel_tol=1e-8,abs_tol=1e-6)
def main():
 raw={}
 for line in (P/'fit/baseline_v01/inputs/MassModels_Lelli2016c.mrt').read_text().splitlines():
  a=line.split()
  try:
   vals=list(map(float,a[1:]));r,v,e,g,d,b=vals[1:7];gas=g*abs(g);stars=.5*d*abs(d)+.7*b*abs(b)
   if min(r,v,e)>0 and gas+stars>0 and all(math.isfinite(x) for x in vals):raw.setdefault(a[0],[]).append((r,v,e,gas,stars))
  except (ValueError,IndexError):continue
 for x in raw.values():x.sort(key=lambda r:r[0])
 clean=[]
 for line in (P/'fit/baseline_v01/inputs/SPARC_Lelli2016c.mrt').read_text().splitlines():
  a=line.split()
  if a and a[0] in raw:
   if int(a[17])==1 and 40<=float(a[5])<=80 and float(a[3])/float(a[2])<=.1 and float(a[6])<=5 and len(raw[a[0]])>=10:clean.append(a[0])
 # Native scale cross-checked against the inherited load, not a fitted value.
 state=next(x for x in json.loads((P/'fit/baseline_v01/wrra_original/inputs/shared_gravity_results.json').read_text())['cases'] if x['carrier_state']=='product' and x['epsilon']==0 and x['a']==1)
 h=67.4*1000/(1e6*3.085677581491367e16);c=299792458.;G=6.67430e-11
 at=c*h*math.sqrt(state['sector_density_J_m3'][1]/(3*h*h*c*c/(8*math.pi*G))/8)
 fits=list(csv.DictReader((D/'fits.csv').open()));points=list(csv.DictReader((D/'points.csv').open()));groups={};seen=set()
 for p in points:
  key=(p['galaxy'],p['model'],p['phase']);uid=key+(p['j'],);req(uid not in seen,'DUPLICATE');seen.add(uid);groups.setdefault(key,[]).append(p)
 models=sorted({f['model'] for f in fits});expected={(name,m,ph) for name in clean for m in models for ph in ['full','interleaved','outer']}
 req(set(groups)==expected,'GROUP_COVERAGE');req(len(fits)==len(expected),'FIT_COUNT');fitkeys=set()
 for f in fits:
  key=(f['galaxy'],f['model'],f['phase']);req(key not in fitkeys,'DUPLICATE_FIT');fitkeys.add(key);pp=sorted(groups[key],key=lambda p:int(p['j']));n=len(raw[key[0]])
  req(len(pp)==n and [int(p['j']) for p in pp]==list(range(n)),'ROW_COVERAGE')
  flags=[False if key[2]=='full' else j%5==4 if key[2]=='interleaved' else j>=n-math.ceil(.2*n) for j in range(n)]
  pivot=float(np.median([x[0] for x,t in zip(raw[key[0]],flags) if not t]));req(close(pivot,f['pivot']),'PIVOT')
  pars=json.loads(f['params']);tr=te=0
  for j,p in enumerate(pp):
   r,v,e,gas,stars=[float(p[k]) for k in ['r','v','e','gas','stars']];req(all(close(x,y) for x,y in zip((r,v,e,gas,stars),raw[key[0]][j])),'CATALOG_MISMATCH');req((p['test']=='True')==flags[j],'SPLIT')
   if key[1]=='NFW_refined':
    vv,cc,s=10**np.array(pars);x=r*.674/vv;halo=vv*vv*(math.log1p(cc*x)-cc*x/(1+cc*x))/(x*(math.log1p(cc)-cc/(1+cc)));pred=math.sqrt(gas+s*stars+halo)
   else:
    A,power,q,s=10**pars[0],pars[1],pars[2],10**pars[3];x=r/pivot
    a=at*A*math.exp(power*math.log(x)+q*math.log(x)**2) if key[1]=='WRRA_curvature_ML' else at*A*x**power*(1+1/10**q)/(1+x/10**q)
    gb=(gas+s*stars)*1e6/(r*3.085677581491367e19);pred=math.sqrt(gb/(-math.expm1(-math.sqrt(gb/a)))*r*3.085677581491367e19)/1000
   req(close(pred,p['pred']),'PREDICTION_MISMATCH');z=((pred-v)/e)**2
   if flags[j]:te+=z
   else:tr+=z
  nt=n-sum(flags);k=3 if key[1]=='NFW_refined' else 4
  req(int(f['k'])==k and int(f['n_fit'])==nt and int(f['n_test'])==sum(flags),'COUNT')
  req(close(tr,f['chi2']) and close(te,f['test_chi2']),'CHI2');req(close(tr+2*k,f['AIC']) and close(tr+k*math.log(nt),f['BIC']),'PENALTY');req(f['success']=='True','OPTIMIZER')
 req(fitkeys==expected,'FIT_COVERAGE');print(json.dumps(dict(status='PASS',fits=len(fits),points=len(points),clean_galaxies=len(clean))))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL:',e);sys.exit(1)
