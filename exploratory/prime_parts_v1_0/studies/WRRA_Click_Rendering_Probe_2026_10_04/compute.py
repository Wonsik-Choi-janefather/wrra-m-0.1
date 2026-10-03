from pathlib import Path
from fractions import Fraction as F
import csv,json,hashlib,itertools,math
import numpy as np
BASE=Path(__file__).resolve().parent
source=BASE/'input_channels.csv'
rows=list(csv.DictReader(source.open()))
q=[F(r['Q']) for r in rows]
# Declared candidate motifs, not an inferred dynamical rendering law.
idx={r['source']:i for i,r in enumerate(rows)}
def vector(names):
 v=[0]*16
 for name in names:v[idx[name]]+=1
 return v
motifs={
 'proton_electron':vector(['3_A_r','3_A_g','3_B_b','1_B']),
 'neutron':vector(['3_A_r','3_B_g','3_B_b']),
 'electron_conjugate_pair':vector(['1_B','1_0']),
 'neutral_channel':vector(['1_A'])}
charges={k:str(sum(x*y for x,y in zip(v,q))) for k,v in motifs.items()}
assert all(F(x)==0 for x in charges.values())
assert sum(q[i] for i in [idx['3_A_r'],idx['3_A_g'],idx['3_B_b']])==1
assert q[idx['1_B']]==-1
# Search the DECLARED occupation model: neutral bags of 1..4 Weyl components.
# These bags are charge-compatible, NOT established bound states.
counts={}
for size in range(1,5):
 counts[size]=sum(sum((q[i] for i in bag),F(0))==0
                 for bag in itertools.combinations_with_replacement(range(16),size))
N=1000000
prime=np.ones(N+1,bool);prime[:2]=False
for k in range(2,math.isqrt(N)+1):
 if prime[k]:prime[k*k::k]=False
n=np.arange(2,N+1); addresses=n[(n%2==1)&~prime[2:]]
cfg=json.loads((BASE/'input_filter.json').read_text())
w=n.astype(float)**(-cfg['alpha']);w/=w.sum()
p=cfg['beta']*w[(n%2==1)&~prime[2:]]
# Two conditional output laws with identical input filter weights and neutral charge.
# These are mutually distinct witnesses of underdetermination, not physical predictions.
A=np.tile(motifs['proton_electron'],(len(addresses),1))
B=np.tile(motifs['neutron'],(len(addresses),1))
q3=np.array([int(3*x) for x in q])
assert np.all(A@q3==0) and np.all(B@q3==0)
assert np.all(A[:,idx['1_B']]==1)
assert not np.array_equal(A,B)
assert len(addresses)==421502
result={'status':'conditional_charge_feasibility_pass',
 'input_channel_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'channel_count':16,'preexisting_core_channels':15,'additional_neutral_channel':1,
 'odd_composite_addresses':len(addresses),'phenotype_weight':float(p.sum()),
 'neutral_bag_counts_by_occupation_size':counts,'motif_charges':charges,
 'witness_A':'every admitted address -> one declared uud+electron motif',
 'witness_B':'every admitted address -> one declared udd motif',
 'witness_both_preserve_input_weights':True,'witness_both_zero_charge':True,
 'witness_A_proton_electron_equal_counts':True,
 'rendering_law_unique':False,'mass_energy_conservation_test':'NOT EVALUABLE: no upstream per-address SI load to output energy map',
 'forces_spin_binding_generations':'NOT DERIVED by charge neutrality or channel count',
 'prime_factorization_used_for_rendering':False,'before_click_decomposition':False,
 'interpretation':'Compatibility demonstration only. Motifs and probabilities are declared; no physical particle production or abundance prediction.'}
(BASE/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
with (BASE/'candidate_motifs.csv').open('w') as f:
 writer=csv.writer(f);writer.writerow(['candidate']+[r['source'] for r in rows]+['total_charge'])
 for name,v in motifs.items():writer.writerow([name]+v+[charges[name]])
print(json.dumps(result,ensure_ascii=False,indent=2))
