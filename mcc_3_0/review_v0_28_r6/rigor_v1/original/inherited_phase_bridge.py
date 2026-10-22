"""Constructive candidate bridge: calibrated rational phase orbit -> finite register.
Not a derivation of cosmological dynamics or a replacement of the prime filter.
"""
from fractions import Fraction as F
from math import lcm,pi
from pathlib import Path
import json
import numpy as np

fractions=tuple(map(F,('0.05','0.268','0.682')))
L=lcm(*(f.denominator for f in fractions))
H,C=29,70
N=L*H*C
orbit=[tuple((j*f)%1 for f in fractions) for j in range(L)]
assert len(set(orbit))==L
assert tuple((L*f)%1 for f in fractions)==(F(0),F(0),F(0))
assert all(any((j*f)%1 for f in fractions) for j in range(1,L))
assert tuple(sum(orbit[j])%1 for j in range(L))==(F(0),)*L

# An optional regular register realization: clock Q and shift S on L basis codes.
# Q S = omega S Q. The regular representation is explicitly an extra choice;
# finite order 500 alone does not imply Hilbert dimension 500.
omega=np.exp(2j*pi/L)
q=omega**np.arange(L)
v=np.arange(1,L+1,dtype=complex)
assert np.allclose(q*np.roll(v,1),omega*np.roll(q*v,1),atol=1e-9)
assert np.allclose(q**L,1,atol=1e-10)
# A 3-dimensional diagonal phase representation also has exact order L.
# Its existence prevents confusing phase return order with carrier dimension.
phase_eigenvalues=np.exp(2j*pi*np.array([float(f) for f in fractions]))
assert np.allclose(phase_eigenvalues**L,1,atol=1e-10)
assert all(not all((j*f).denominator==1 for f in fractions) for j in range(1,L))

def encode(l,h,z):
    return 1+l+L*(h+H*z)

def decode(n):
    q,l=divmod(n-1,L)
    z,h=divmod(q,H)
    return l,h,z

# Full-domain bijection, without altering the published serialization.
for n in range(1,N+1):
    assert encode(*decode(n))==n

# Candidate finite Klein-type seam: z wrap reverses the l coordinate.
def A(x):
    l,h,z=x
    return (l+1)%L,h,z

def B(x):
    l,h,z=x
    return ((-l)%L,h,0) if z==C-1 else (l,h,z+1)

def Binverse(x):
    l,h,z=x
    return ((-l)%L,h,C-1) if z==0 else (l,h,z-1)

def repeat(fn,x,k):
    for _ in range(k):x=fn(x)
    return x

for l in range(L):
    x=(l,0,0)
    assert repeat(B,x,C)==((-l)%L,0,0)
    assert repeat(B,x,2*C)==x
    # Reflection conjugates forward l transport into backward transport.
    assert repeat(B,A(repeat(B,x,C)),C)==((l-1)%L,0,0)
for z in range(C):
    for l in range(L):
        x=(l,H-1,z)
        assert Binverse(B(x))==B(Binverse(x))==x

# Nonuniform weighting is compatible with this finite coordinate register.
# This is normalization of the existing address weighting law, not replay of
# its phenotype/dark/return classifier or any downstream gravity calculation.
alpha=1.8996876950554356
addresses=np.arange(2,N+1,dtype=np.int64)
weights=addresses.astype(float)**(-alpha)
weights/=weights.sum()
phase_marginal=np.bincount((addresses-1)%L,weights=weights,minlength=L)
assert abs(float(weights.sum())-1)<1e-12
assert abs(float(phase_marginal.sum())-1)<1e-12
assert not np.allclose(phase_marginal,1/L)

changed=tuple(map(F,('0.0501','0.2680','0.6819')))
phase_defect=[str((L*f)%1) for f in changed]
out={
 'status':'constructed conditional interface candidate, not adopted physical dynamics',
 'calibrated_inputs':[str(f) for f in fractions],
 'new_rule':'One phase turn j advances sector coordinates by f_s mod 1.',
 'orbit_order':L,'orbit_distinct_points':len(set(orbit)),
 'source_tuple_count':N,'executable_addresses':N-1,
 'excluded_reference_address':1,
 'frozen_factors':{'H':H,'C':C},
 'assumptions':['composition shares are fixed exact calibrated model values',
                'shares are reused as sector phase increments (new candidate interface)',
                'all L,H,C tuples are admissible (existing product rule)'],
 'checks':{'exact_phase_closure':True,'no_shorter_phase_return':True,
           'full_serialization_bijection':True,'Klein_seam_inverse':True,
           'Klein_double_return':True,'orientation_conjugation':True,
           'weighted_address_normalization':True,'regular_register_Weyl_relation':True,
           'low_dimension_same_phase_order_counterexample':True},
 'phase_marginal_nonuniform':{'minimum':float(phase_marginal.min()),
                            'maximum':float(phase_marginal.max())},
 'changed_calibration_closure_defect_mod1':phase_defect,
 'excluded_claims':['physical time period','15-channel carrier Hamiltonian derivation',
                   'new composition prediction','full prime-filter replay',
                   'physical necessity of the phase interface or LHC product'],
 'dependency_change':'No published input or downstream coefficient changed.'}
Path(__file__).with_name('phase_bridge_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False,indent=2))
