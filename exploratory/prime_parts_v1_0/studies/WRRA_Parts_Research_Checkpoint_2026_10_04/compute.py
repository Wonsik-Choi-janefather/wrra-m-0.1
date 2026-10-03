from pathlib import Path
import numpy as np,json,csv,math
B=Path(__file__).resolve().parent
M=1000000;s=np.ones(M+1,bool);s[:2]=False
for p in range(2,1001):
 if s[p]:s[p*p::p]=False
primes=np.flatnonzero(s);rows=[]
for N in [1000,10000,100000,1000000]:
 v=np.arange(2,N+1);n=v[(v%2==1)&~s[2:N+1]]
 w=n.astype(float)**(-1.8996876950554356);w/=w.sum()
 for K in [2,4,8,12,15,16,20]:
  pool=primes[:K]
  for name,parts in [('small',pool),('large',pool[::-1])]:
   cyc=n//parts.sum();c=np.repeat(cyc[:,None],K,axis=1);r=n-cyc*parts.sum()
   # One-each cyclic addition; after full cycles at most pool.sum/2 additions.
   while np.any(r>=2):
    for j,p in enumerate(parts):
     t=r>=p;c[:,j]+=t;r-=p*t
   assert np.all(c@parts+r==n)
   avg=w@c;f=float(avg[np.isin(parts,[5,47])].sum()/avg.sum())
   target_ratio=(1-f)/f if f>0 else None
   rows.append({'N':N,'K':K,'largest_prime':int(pool[-1]),'order':name,'addresses':len(n),'mean_parts':float(avg.sum()),'residue1_weight':float(w[r==1].sum()),'fixed_5_47_neutron_fraction':f,'p_per_n':target_ratio,'target_absolute_error':abs(f-.125),'mapping_status':'fixed prior calibrated candidate; missing labels not replaced'})
with (B/'stability_grid.csv').open('w') as f:
 wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
summary=[]
for K in [2,4,8,12,15,16,20]:
 for name in ['small','large']:
  group=[x for x in rows if x['K']==K and x['order']==name]
  summary.append({'K':K,'order':name,'neutron_fraction_N1k':group[0]['fixed_5_47_neutron_fraction'],'neutron_fraction_N1m':group[-1]['fixed_5_47_neutron_fraction'],'change_N100k_to_1m':group[-1]['fixed_5_47_neutron_fraction']-group[-2]['fixed_5_47_neutron_fraction']})
r={'cases':len(rows),'numerical_conservation':'PASS all cases','assignment':'prime5/47 -> n, other allowed primes -> p+e; fixed from prior calibration no refit','summary':summary,'limits':['arithmetic prime labels not derived quark channels','p/n/e assignment calibrated; not independent prediction','N and K sensitivity are numerical/model checks, not observational uncertainty','physical species energy, capture/decay times and CMB spectrum remain open'],'conclusion':'finite candidate stability evaluated; no automatic preferred K from this fitted species decoder'}
(B/'results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
