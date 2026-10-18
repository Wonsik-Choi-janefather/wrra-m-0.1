"""MIT License. Exact checks of the declared model, not empirical validation."""
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path
import json

def composite(x):
    return x>3 and any(x%d==0 for d in range(2,isqrt(x)+1))

p=F(1,4); mean=F(0); second=F(0); equal=F(0); mass=F(0)
for gates in product((0,1),repeat=6):
    weight=F(1)
    for q in gates: weight*=p if q else 1-p
    d=sum((-1)**k*q for k,q in enumerate(gates,1))
    mass+=weight; mean+=weight*d; second+=weight*d*d
    if d==0:equal+=weight
assert mass==1 and mean==0 and second==6*p*(1-p)
assert equal<1
odd=[x for x in range(9,100,2) if composite(x)]
def placement(n,b):
    return ((n+b)//2,(n-b)//2)
placement_cases=0
for n,m,b,c in product(odd,odd,(-1,1),(-1,1)):
    u,d=placement(n,b);v,w=placement(m,c)
    assert u+d==n and u-d==b
    assert (u+v)-(d+w)==b+c
    assert (u+v==d+w)==(c==-b)
    assert placement(n,-b)==(d,u)
    placement_cases+=1
decomp={str(r):[[n,m] for n in odd for m in odd if n<=m and n+m==r]
        for r in (18,20,24,54)}
assert decomp['18']==[[9,9]] and not decomp['20']
assert decomp['24']==[[9,15]] and [9,45] in decomp['54'] and [27,27] in decomp['54']
# P=3 splits one parent per event; H=2 annihilations return one parent per event.
# Unit-packet bookkeeping is an illustrative admitted channel, not a photon law.
nm,na,parent=10,4,5; P,H=3,2
out=(nm+P-H,na+P-H,parent-P+H)
assert out[0]-out[1]==nm-na
assert out[0]+out[1]+2*out[2]==nm+na+2*parent
# Natural units c=1, electron rest mass m=1.
one_photon_s=2**2-2**2
two_headon_photons_s=(1+1)**2-(1-1)**2
threshold_s=(1+1)**2
assert one_photon_s<threshold_s and two_headon_photons_s==threshold_s
result={
 'status':'exact specification audit passed; not empirical validation',
 'late_slots':6,'permission_probability':str(p),'normalization':str(mass),
 'mean_difference':str(mean),'variance_difference':str(second-mean*mean),
 'probability_exactly_equal_counts':str(equal),
 'decomposition_address_bound':99,'unordered_decompositions':decomp,
 'placement_configurations_audited':placement_cases,
 'placement_up_down_9_15':[12,12],
 'placement_up_up_9_15':[13,11],
 'placement_down_down_9_15':[11,13],
 'conversion_ledger_before':[nm,na,parent], 'conversion_ledger_after':out,
 'one_photon_s':one_photon_s,'massive_pair_minimum_s':threshold_s,
 'two_headon_photons_s':two_headon_photons_s,
 'initial_equal_two_mode_burst_net':1000-1000,
 'initial_single_mode_burst_net':1000,
 'empirical_fit_performed':False,'physical_rates_derived':False}
Path(__file__).with_name('verification_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
