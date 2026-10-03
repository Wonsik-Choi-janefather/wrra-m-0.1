from pathlib import Path
import numpy as np,json,csv,math
B=Path(__file__).resolve().parent
cfg=json.loads((B/'input_filter.json').read_text());N=cfg['N']
sieve=np.ones(N+1,bool);sieve[:2]=False
for k in range(2,math.isqrt(N)+1):
 if sieve[k]:sieve[k*k::k]=False
numbers=np.arange(2,N+1);n=numbers[(numbers%2==1)&~sieve[2:]]
primes=np.flatnonzero(sieve);primes=primes[primes>2]
pos=np.searchsorted(primes,n);lo=primes[pos-1];hi=primes[np.minimum(pos,len(primes)-1)]
valid=pos<len(primes)
nearest=np.where(valid & ((hi-n)<(n-lo)),hi,lo) # ties choose lower
weight=numbers.astype(float)**(-cfg['alpha']);weight/=weight.sum()
w=cfg['beta']*weight[(numbers%2==1)&~sieve[2:]]
d=n-lo;k=d//2;dn=n-nearest;kn=np.abs(dn)//2
assert np.all(n==lo+d) and np.all(d>0) and np.all(d%2==0)
assert np.all(n==nearest+dn) and np.all(dn%2==0)
# Pair law: delta/2 neutral +/- pairs, declared count convention only.
# A signed residual can label orientation; pair charge still zero.
assert np.all(k-k==0) and np.all(kn-kn==0)
with (B/'address_candidates.csv').open('w') as f:
 out=csv.writer(f);out.writerow(['n','lower_prime','delta_lower','pair_count_lower','nearest_prime','signed_delta_nearest','pair_count_nearest','phenotype_weight'])
 for row in zip(n,lo,d,k,nearest,dn,kn,w):out.writerow([int(x) for x in row[:-1]]+[float(row[-1])])
res={'N':N,'addresses':int(len(n)),'phenotype_weight':float(w.sum()),
 'matching_status':'NEW DECLARED CANDIDATE; not existing filter confusion decoder',
 'lower_rule_max_pair_count':int(k.max()),'lower_rule_mean_pair_count_unweighted':float(k.mean()),
 'lower_rule_weighted_pair_count_conditional':float(w@k/w.sum()),
 'nearest_rule_max_pair_count':int(kn.max()),'nearest_rule_weighted_pair_count_conditional':float(w@kn/w.sum()),
 'addresses_with_different_reference':int((nearest!=lo).sum()),
 'addresses_with_different_pair_count':int((kn!=k).sum()),
 'lower_rule_weight_fraction_one_pair':float(w[k==1].sum()/w.sum()),
 'arithmetic_and_neutral_pair_checks':'PASS on all addresses',
 'energy_check':'UNDETERMINED: L(n), reference output and pair energy map missing',
 'unit_pair_law':'k=abs(n-p)/2, declared convention, not derived physical multiplicity',
 'particle_assignment':'charge +/- template only; proton/electron assignment needs mass, baryon/lepton and binding ledger',
 'negative_residual':'nearest rule may yield negative delta; never negative energy or negative count',
 'reference_component':'p is a numerical template label; not assumed emitted prime particle',
 'conclusion':'Arithmetic neutral-pair rendering is constructible. Reference and count-law sensitivity prevent unique physical decoder.'}
(B/'results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(res,ensure_ascii=False,indent=2))
