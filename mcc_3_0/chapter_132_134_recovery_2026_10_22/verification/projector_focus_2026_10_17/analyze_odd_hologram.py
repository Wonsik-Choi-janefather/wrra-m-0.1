"""Finite WRRA odd-composite carrier diagnostics; no RH proof claimed."""
from fractions import Fraction
import math
import json

def compute():
    cap=1_000_000
    prime=bytearray(b'\x01')*(cap+1)
    prime[0:2]=b'\x00\x00'
    for p in range(2,math.isqrt(cap)+1):
        if prime[p]:
            prime[p*p:cap+1:p]=b'\x00'*(((cap-p*p)//p)+1)
    rows=[]
    for limit in [100,1000,10000,100000,1000000]:
        c=[n for n in range(9,limit+1,2) if not prime[n]]
        rows.append({'N':limit,'odd_composites':len(c),
                     'E_sigma_0.4':math.fsum(n**(-.8) for n in c),
                     'E_sigma_0.5':math.fsum(1/n for n in c),
                     'E_sigma_0.6':math.fsum(n**(-1.2) for n in c)})
    # Exact finite projection at s=2, rather than an analytic continuation claim.
    N=1000
    direct=sum((Fraction(1,n*n) for n in range(9,N+1,2) if not prime[n]),Fraction())
    projected=(sum((Fraction(1,n*n) for n in range(1,N+1,2)),Fraction())-1
               -sum((Fraction(1,p*p) for p in range(3,N+1,2) if prime[p]),Fraction()))
    assert direct==projected
    # Multiplicative Euler construction, truncated by product address <=1000.
    addresses={1:0}
    for p in range(3,N+1,2):
        if not prime[p]:continue
        old=list(addresses.items())
        for n,omega in old:
            product=n*p
            degree=omega+1
            while product<=N:
                assert product not in addresses
                addresses[product]=degree
                product*=p
                degree+=1
    assert set(addresses)==set(range(1,N+1,2))
    composites={n for n,degree in addresses.items() if degree>=2}
    assert composites=={n for n in range(9,N+1,2) if not prime[n]}
    assert addresses[15]==2 and addresses[27]==3
    # Equal beat frequencies in an intensity-only renderer.
    assert Fraction(27,9)==Fraction(45,15)==3
    return {'scope':'Conditional mathematical carrier model, not a physical hologram or RH proof',
            'source_rule':'prime -> label1; even composite -> label2; odd composite -> label3; 1 separate',
            'finite_projection':{'N':N,'s':2,'exact_equality':True,'numerator':str(direct.numerator),'denominator':str(direct.denominator)},
            'finite_euler_factorization':{'N':N,'odd_addresses':len(addresses),'odd_composites':len(composites),'exact_match':True},
            'intensity_ratio_collision':{'pairs':[[27,9],[45,15]],'exact_ratio':'3'},
            'energy_values_display_only':rows,
            'proved_general':'sum odd-composite n^(-2*sigma) converges iff sigma>1/2',
            'boundary_proof':'Upper bound by all-integer p-series; lower bound by odd multiples of 9, a positive-density arithmetic progression',
            'finite_complex_amplitude_recovery':'Vandermonde in distinct log(n), invertible for every real sigma',
            'new_actual_xi_inequality':False,'RH_status':'OPEN'}

if __name__=='__main__':
    print(json.dumps(compute(),ensure_ascii=False,indent=2))
