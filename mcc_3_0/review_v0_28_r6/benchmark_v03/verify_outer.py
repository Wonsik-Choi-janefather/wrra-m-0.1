"""Independent replay: no imports from fitting modules; reads raw catalog too."""
from pathlib import Path
import sys,csv,json,math
import numpy as np
P=Path(__file__).resolve().parent
D=Path(sys.argv[1]) if len(sys.argv)>1 else P/'outer_results'
def require(ok,msg):
 if not ok:raise ValueError(msg)
def read(n):return list(csv.DictReader((D/n).open()))
def close(a,b):return math.isclose(float(a),float(b),rel_tol=1e-9,abs_tol=1e-7)
def main():
 raw={}
 for l in (P/'fit/baseline_v01/inputs/MassModels_Lelli2016c.mrt').read_text().splitlines():
  a=l.split()
  try:
   v=list(map(float,a[1:]));r,vel,e,g,d,b=v[1:7];gas=g*abs(g);stars=.5*d*abs(d)+.7*b*abs(b)
   if r>0 and vel>0 and e>0 and gas+stars>0 and all(math.isfinite(x) for x in v):raw.setdefault(a[0],[]).append((r,vel,e,gas,stars))
  except (ValueError,IndexError):continue
 for v in raw.values():v.sort(key=lambda x:x[0])
 points=read('points.csv');fits=read('fits.csv');groups={};seen=set();protocol=json.loads((D/'protocol.json').read_text());at=protocol['aT']
 for p in points:
  key=(p['galaxy'],p['model']);uid=key+(int(p['j']),);require(uid not in seen,'DUPLICATE_ROW');seen.add(uid);groups.setdefault(key,[]).append(p)
 fitseen=set()
 for f in fits:
  key=(f['galaxy'],f['model']);require(key not in fitseen,'DUPLICATE_FIT');fitseen.add(key)
  pp=groups[key];pp.sort(key=lambda p:int(p['j']));n=len(raw[key[0]]);cut=n-math.ceil(.2*n)
  require(len(pp)==n and [int(p['j']) for p in pp]==list(range(n)),'ROW_COVERAGE')
  require(close(f['pivot'],np.median([r[0] for r in raw[key[0]][:cut]])),'PIVOT')
  train=test=0;pars=json.loads(f['params'])
  for j,p in enumerate(pp):
   r,v,e,gas,stars=[float(p[k]) for k in ['r','v','e','gas','stars']]
   require(all(close(x,y) for x,y in zip((r,v,e,gas,stars),raw[key[0]][j])),'CATALOG_MISMATCH')
   require(p['partition']==('train' if j<cut else 'test'),'SPLIT')
   if key[1]=='WRRA_radial_ML':
    A,power,s=10**pars[0],pars[1],10**pars[2];gb=(gas+s*stars)*1e6/(r*3.085677581491367e19);a=at*A*(r/float(f['pivot']))**power
    expected=math.sqrt(gb/(-math.expm1(-math.sqrt(gb/a)))*r*3.085677581491367e19)/1000
   else:
    vv,c,s=10**np.array(pars);x=r*.674/vv;halo=vv*vv*(math.log1p(c*x)-c*x/(1+c*x))/(x*(math.log1p(c)-c/(1+c)))
    expected=math.sqrt(gas+s*stars+halo)
   require(close(expected,p['pred']),'PREDICTION_MISMATCH');z=((expected-v)/e)**2
   if j<cut:train+=z
   else:test+=z
  require(close(train,f['train_chi2']) and close(test,f['test_chi2']),'SCORE_MISMATCH')
  require(int(f['n_train'])==cut and int(f['n_test'])==n-cut,'COUNT')
  require(f['success']=='True','OPTIMIZER_FAILURE')
 require(len(fitseen)==len(groups),'EXTRA_POINTS')
 names={f['galaxy'] for f in fits}
 require(all((name,m) in fitseen for name in names for m in ['WRRA_radial_ML','NFW_ML']),'MISSING_MODEL')
 print(json.dumps(dict(status='PASS',fits=len(fits),points=len(points),raw_catalog_replay=True)))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL:',e);sys.exit(1)
