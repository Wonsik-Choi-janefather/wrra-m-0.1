from pathlib import Path
import numpy as np,json,csv,math
from scipy.spatial import cKDTree
B=Path(__file__).resolve().parent
N=1000000
s=np.ones(N+1,bool);s[:2]=False
for a in range(2,1001):
 if s[a]:s[a*a::a]=False
alln=np.arange(2,N+1);odd=alln[(alln%2==1)&~s[2:]];primes=np.flatnonzero(s);primes=primes[primes>2]
# Finite reproducible diagnostic sample, NOT a full universe decoder.
ix=np.unique(np.r_[np.arange(2048),np.linspace(2048,len(odd)-1,2048,dtype=int)])
n=odd[ix]
g=np.array([14.134725141734695,21.022039638771556,25.01085758014569,30.424876125859512])
def feat(x):
 z=np.exp(-1j*np.log(x)[:,None]*g[None,:])
 return np.c_[z.real,z.imag]
pf=feat(primes);nf=feat(n)
dist,j=cKDTree(pf).query(nf,k=2)
p=primes[j[:,0]];delta=n-p;pairs=np.abs(delta)//2
pos=np.searchsorted(primes,n);lower=primes[pos-1]
assert np.all(n==p+delta) and np.all(delta%2==0)
# Feature distance corresponds to same fixed-phase Hilbert norm up to sqrt(5).
assert np.allclose(np.linalg.norm(nf-pf[j[:,0]],axis=1),dist[:,0])
# Source state has equal amplitudes in 5 modes. Its diagonal H energy
# is the SAME for all n: phase differences do not supply particle rest energy.
mu=510998.95069/23
E=np.r_[0,g*mu];source_energy=float(E.mean())
assert np.allclose((np.ones((len(n),5))/5)@E,source_energy)
# Common frame unitary preserves pairwise state distances.
z=np.exp(-1j*np.log(n)[:,None]*g)
zp=np.exp(-1j*np.log(p)[:,None]*g)
u=np.exp(-1j*g*.1)
frame_error=float(np.max(np.abs(np.linalg.norm(z-zp,axis=1)-np.linalg.norm(z*u-zp*u,axis=1))))
with (B/'response_candidates.csv').open('w') as f:
 out=csv.writer(f);out.writerow(['n','phase_nearest_prime','signed_delta','candidate_pairs','state_norm_distance','second_neighbor_distance','lower_prime'])
 for row in zip(n,p,delta,pairs,dist[:,0]/math.sqrt(5),dist[:,1]/math.sqrt(5),lower):out.writerow(row)
r={'sample_addresses':len(n),'all_odd_addresses':len(odd),'prime_reference_count':len(primes),
 'sample_method':'first 2048 odd composites plus 2048 evenly spaced remaining indices; not random/unbiased',
 'response_input':'existing 0.5 source state psi_n=(1,exp(-i gamma_j log n))/sqrt(5)',
 'new_decoder_choice':'Euclidean fixed-phase source-state nearest prime; diagnostic not derived measurement POVM',
 'different_from_lower_prime':int((p!=lower).sum()),'negative_residual_count':int((delta<0).sum()),
 'candidate_pairs_median':float(np.median(pairs)),'candidate_pairs_max':int(pairs.max()),
 'state_distance_median':float(np.median(dist[:,0]/math.sqrt(5))),
 'common_frame_distance_max_change':frame_error,
 'source_energy_eV_all_addresses':source_energy,'source_energy_difference_n_vs_p_eV':0,
 'pair_energy_from_source_energy_difference':'FAIL for positive-mass pairs: difference is zero',
 'charge_check':'neutral +/- templates pass algebraically, not physical production',
 'conclusion':'Existing phase response gives a conditional reference decoder, with large nonlocal address residuals. Existing diagonal source energy cannot finance residual pair creation without a new load/coupling/reservoir map.'}
chi=(dist[:,0]/math.sqrt(5))**2/4
assert np.all((chi>=0)&(chi<=1))
reference_budget=source_energy*(1-chi);pair_budget=source_energy*chi
assert np.allclose(reference_budget+pair_budget,source_energy)
r['bounded_response_load_rule']='NEW candidate: chi=state_norm_distance^2/4; split E into E*(1-chi) and E*chi'
r['pair_budget_max_eV']=float(pair_budget.max())
r['electron_positron_rest_threshold_eV']=2*510998.95069
r['addresses_with_one_source_packet_budget_for_electron_positron']=int((pair_budget>=2*510998.95069).sum())
r['packet_multiplicity']='not determined; source state is not identified as one physical particle packet'
(B/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
