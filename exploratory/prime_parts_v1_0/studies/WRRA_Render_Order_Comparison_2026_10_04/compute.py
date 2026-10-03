from pathlib import Path
import numpy as np,json,csv,math
B=Path(__file__).resolve().parent;N=1000000
s=np.ones(N+1,bool);s[:2]=False
for p in range(2,1001):
 if s[p]:s[p*p::p]=False
v=np.arange(2,N+1);n=v[(v%2==1)&~s[2:]];primes=np.flatnonzero(s)
a=1.8996876950554356;beta=.8654570124136961
w=v.astype(float)**(-a);w/=w.sum();w=beta*w[(v%2==1)&~s[2:]];w/=w.sum()
# Declared test semantics: repeat each denomination maximally before next.
# Ascending then exhausts 2 and leaves 1 on odd inputs. This is NOT the
# only possible meaning of user 'one at a time'. Compare repair separately.
def split(parts,repair=False):
 rem=n.copy();count=np.zeros((len(n),len(parts)),dtype=np.int64)
 for j,p in enumerate(parts):
  c=rem//p
  if repair:
   # avoid terminal remainder 1; requires 2 and 3 later or available.
   c=np.where((rem-c*p==1)&(c>0),c-1,c)
  count[:,j]=c;rem-=c*p
 assert np.all(count@np.array(parts)+rem==n)
 return count,rem
out=[]
for K in [2,3,4,8,15]:
 pool=primes[:K].tolist()
 for name,parts,repair in [('small_first',pool,False),('large_first',pool[::-1],False),('small_first_avoid_1',pool,True),('large_first_avoid_1',pool[::-1],True)]:
  c,r=split(parts,repair);num=c.sum(axis=1)
  out.append({'K':K,'largest_prime':pool[-1],'rule':name,'exact_addresses':int((r==0).sum()),'residue1_addresses':int((r==1).sum()),'other_residue_addresses':int(((r!=0)&(r!=1)).sum()),'weighted_mean_parts':float(w@num),'weighted_exact_fraction':float(w[r==0].sum()),'active_denominations':int((c.sum(axis=0)>0).sum()),'charge_assignment':'not assigned by arithmetic','energy_map':'not assigned'})
  if K==4:
   with (B/(name+'_K4_samples.csv')).open('w') as f:
    writer=csv.writer(f);writer.writerow(['n']+[str(x) for x in parts]+['residue'])
    for idx in np.r_[np.arange(40),np.linspace(40,len(n)-1,60,dtype=int)]:writer.writerow([int(n[idx])]+c[idx].tolist()+[int(r[idx])])
# Literal one-each interpretation: cyclic walk through pool, add one each.
for K in [2,3,4,8,15]:
 pool=primes[:K].tolist()
 for name,parts in [('small_first_one_each',pool),('large_first_one_each',pool[::-1])]:
  total=sum(parts);cycles=n//total
  c=np.repeat(cycles[:,None],K,axis=1);r=n-cycles*total
  for repeat in range(total//2+1):
   for j,p in enumerate(parts):
    take=r>=p;c[:,j]+=take;r-=p*take
  assert np.all(c@np.array(parts)+r==n)
  out.append({'K':K,'largest_prime':pool[-1],'rule':name,'exact_addresses':int((r==0).sum()),'residue1_addresses':int((r==1).sum()),'other_residue_addresses':int(((r!=0)&(r!=1)).sum()),'weighted_mean_parts':float(w@c.sum(axis=1)),'weighted_exact_fraction':float(w[r==0].sum()),'active_denominations':int((c.sum(axis=0)>0).sum()),'charge_assignment':'not assigned by arithmetic','energy_map':'not assigned'})
with (B/'comparison.csv').open('w') as f:
 wr=csv.DictWriter(f,fieldnames=list(out[0]));wr.writeheader();wr.writerows(out)
res={'N':N,'addresses':len(n),'pool_sizes':[2,3,4,8,15],'candidate_semantics':'repeat smallest/largest currently available maximally; avoid-1 variant reduces one count when remainder would be 1','conservation':'integer address sum verified for every rule and address','results':out,'physical_conclusion':'Order alone does not define rendering; stopping/upgrade constraints required. Arithmetic exactness is not energy/charge/spin proof.'}
(B/'results.json').write_text(json.dumps(res,indent=2)+'\n')
for row in out:
 if row['K'] in [4,15]:print(json.dumps(row))
