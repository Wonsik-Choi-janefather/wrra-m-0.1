"""Exact finite score and flow checks for WRRA-M 0.3.

Enumerates all 3^8=6561 compatibility tables with entries in {-1,0,1}.
Closed-flow samples use exp(eta*t)=2^k with integer scores and rational
probabilities, so those samples too are exact. Finite checks complement,
and do not replace, the algebraic theorem in the manuscript.
"""
from fractions import Fraction as Q
from itertools import product
import json

COEFFICIENTS = ((1,0,0,1,1,0,0,1),(0,1,1,0,1,0,0,1),
                (1,0,0,1,0,1,1,0),(0,1,1,0,0,1,1,0))
DELTA_L = (1,-1,-1,1,0,0,0,0)
DELTA_R = (0,0,0,0,1,-1,-1,1)


def scores(entries):
    lAA,lAB,lBA,lBB,rAN,rA0,rBN,rB0 = entries
    return (lAA+lBB+rAN+rB0,lAB+lBA+rAN+rB0,
            lAA+lBB+rA0+rBN,lAB+lBA+rA0+rBN)


def probabilities(initial, score, k):
    # Rational samples of exp(eta*t)=2^k, including eta=0 and eta<0.
    raw = [p*Q(2)**(k*c) for p,c in zip(initial,score)]
    return tuple(p/sum(raw) for p in raw)


def main():
    sub = lambda a,b: tuple(x-y for x,y in zip(a,b))
    assert sub(COEFFICIENTS[0],COEFFICIENTS[1]) == DELTA_L
    assert sub(COEFFICIENTS[0],COEFFICIENTS[2]) == DELTA_R
    assert sub(COEFFICIENTS[0],COEFFICIENTS[3]) == tuple(x+y for x,y in zip(DELTA_L,DELTA_R))
    count,unique,tied = 0,0,0
    for entries in product((-1,0,1),repeat=8):
        c = scores(entries)
        dl = entries[0]+entries[3]-entries[1]-entries[2]
        dr = entries[4]+entries[7]-entries[5]-entries[6]
        assert (c[0]-c[1],c[0]-c[2],c[0]-c[3]) == (dl,dr,dl+dr)
        target_unique = c[0] > max(c[1:])
        assert target_unique == (dl>0 and dr>0)
        unique += target_unique
        tied += c.count(max(c)) > 1
        count += 1
    assert count == 6561
    initial = (Q(2,17),Q(3,17),Q(5,17),Q(7,17))
    c = (0,-8,-8,-16)
    assert probabilities(initial,c,0) == initial
    positive,negative = probabilities(initial,c,1),probabilities(initial,c,-1)
    assert positive[0] > initial[0] and negative[3] > initial[3]
    for k in (1,2,10):
        p = probabilities(initial,c,k)
        assert sum(p) == 1 and all(q > 0 for q in p)
        assert 1-p[0] <= ((1-initial[0])/initial[0])*Q(2)**(-8*k)
        for j in range(1,4):
            assert p[j]/p[0] == (initial[j]/initial[0])*Q(2)**(k*(c[j]-c[0]))
    boundary = (Q(0),Q(1,3),Q(1,3),Q(1,3))
    assert probabilities(boundary,c,10)[0] == 0
    # All independent extreme entry perturbations in the stated box.
    witness = (Q(0),Q(-4),Q(-4),Q(0),Q(0),Q(-4),Q(-4),Q(0))
    for signs in product((-1,1),repeat=8):
        perturbed = tuple(v+s*Q(1) for v,s in zip(witness,signs))
        c1 = scores(perturbed)
        assert c1[0] > max(c1[1:])  # delta=8 > 4*rho=4
    sharp = (Q(-2),Q(-2),Q(-2),Q(-2),Q(0),Q(-4),Q(-4),Q(0))
    assert scores(sharp)[0] == scores(sharp)[1]  # rho=2 saturates delta/4
    print(json.dumps({'version':'0.3-r1','status':'PASS','finite_tables':count,
        'target_unique_tables':unique,'tables_with_tied_maxima':tied,
        'flow_eta_positive':'target increases and exponential bound holds',
        'flow_eta_zero':'weights unchanged','flow_eta_negative':'minimum-score weight increases',
        'zero_initial_target':'remains zero','perturbation_vertices':256,
        'sharp_margin':'tie at delta=4*rho'},indent=2))


if __name__ == '__main__':
    main()
