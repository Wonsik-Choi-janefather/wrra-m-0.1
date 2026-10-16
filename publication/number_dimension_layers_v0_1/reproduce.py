#!/usr/bin/env python3
"""Finite address calculation; arithmetic topology is a declared construction.
Run: python3 reproduce.py --output results.json
Requires Python 3, numpy, scipy. All targets and inherited parameters explicit.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import brentq
from scipy.special import expit

N = 1_015_000
TARGET_P, TARGET_D = .05, .268
ALPHA_FROZEN = 1.8996877935161325
H_FROZEN = 1.4476744689338703
GAMMA = np.array([14.134725141734695, 21.022039638771556,
                  25.01085758014569, 30.424876125859512])
XI, FRAMES, COEFFICIENT = .1, 8, .5

def masks_for(limit):
    prime = np.ones(limit + 1, dtype=bool)
    prime[:2] = False
    for p in range(2, int(limit ** .5) + 1):
        if prime[p]:
            prime[p*p::p] = False
    n = np.arange(2, limit + 1)
    p = prime[2:]
    even = (n % 2 == 0) & ~p
    odd = (n % 2 == 1) & ~p
    assert np.all(p.astype(int) + even.astype(int) + odd.astype(int) == 1)
    return n, p, even, odd

def calculate(limit, refit=False):
    n, prime, even, odd = masks_for(limit)
    logs = np.log(n.astype(float))

    def weights(alpha):
        w = np.exp(-alpha * logs)
        return w / w.sum()

    def branch(alpha):
        w = weights(alpha)
        return dict(prime=float(w[prime].sum()),
                    even_composite=float(w[even].sum()),
                    odd_composite=float(w[odd].sum()))

    # Re-execute the actual four-mode/eight-frame source admission formula.
    log_odd = logs[odd]
    d = np.zeros((FRAMES, len(log_odd)))
    for k in range(FRAMES):
        for gamma in GAMMA:
            d[k] += COEFFICIENT * np.cos(gamma * (log_odd + XI * k))

    def admission(h):
        return 1. - np.prod(expit(h - d), axis=0)

    def ledger(alpha, h):
        w = weights(alpha)
        ep = admission(h)
        ordinary = float(np.dot(w[odd], ep))
        dark = float(w[even].sum())
        prime_return = float(w[prime].sum())
        odd_return = float(np.dot(w[odd], 1. - ep))
        returned = prime_return + odd_return
        return dict(ordinary=ordinary, dark=dark, returned=returned,
                    total=ordinary + dark + returned,
                    prime_return=prime_return, odd_return=odd_return,
                    odd_weight=float(w[odd].sum()),
                    beta_effective=ordinary / float(w[odd].sum()),
                    admission_min=float(ep.min()), admission_max=float(ep.max()))

    dimension = np.where(prime, 1, np.where(n % 2 == 0, 2, 3))
    assert np.array_equal(dimension == 1, prime)
    assert np.array_equal(dimension == 2, even)
    assert np.array_equal(dimension == 3, odd)
    assert dimension[0] == 1  # prime-first: address 2 is 1D
    result = dict(N=limit, active_count=int(len(n)),
                  dimension_counts={str(d): int((dimension == d).sum()) for d in (1,2,3)},
                  counts=dict(prime=int(prime.sum()), even_composite=int(even.sum()),
                              odd_composite=int(odd.sum())),
                  uniform=branch(0.), inverse_square=branch(2.),
                  fixed_alpha_raw=branch(ALPHA_FROZEN),
                  inherited_frozen=ledger(ALPHA_FROZEN, H_FROZEN))
    assert abs(result['inherited_frozen']['total'] - 1.) < 2e-14
    assert 0. <= result['inherited_frozen']['admission_min']
    assert result['inherited_frozen']['admission_max'] <= 1.
    if refit:
        alpha = brentq(lambda a: branch(a)['even_composite'] - TARGET_D,
                       1.5, 2.5, xtol=5e-15)
        w_odd = weights(alpha)[odd]
        h = brentq(lambda h: float(np.dot(w_odd, admission(h))) - TARGET_P,
                   -10., 20., xtol=5e-15)
        result['refit'] = dict(alpha=alpha, h=h, ledger=ledger(alpha, h))
        assert abs(result['refit']['ledger']['ordinary'] - TARGET_P) < 1e-12
        assert abs(result['refit']['ledger']['dark'] - TARGET_D) < 1e-12
        # This is joint calibration, not an additional empirical prediction.
    return result

def topology_example(a, b, flipped):
    """Triangulated quotient band: infer orientability/boundary from incidences.
    Both a,b >= 2; no metric/isometry or 3-D matter volume is assumed.
    """
    def vertex(x, y):
        if x == b:
            x, y = 0, a-y if flipped else y
        return x*(a+1)+y
    faces=[]
    for x in range(b):
        for y in range(a):
            u,v,w,z=vertex(x,y),vertex(x+1,y),vertex(x+1,y+1),vertex(x,y+1)
            faces.extend([(u,v,w),(u,w,z)])
    edges={}
    for i, tri in enumerate(faces):
        for u,v in zip(tri, tri[1:]+tri[:1]):
            key=tuple(sorted((u,v)))
            edges.setdefault(key,[]).append((i,1 if u<v else -1))
    adj=[[] for _ in faces]
    boundary={}
    for (u,v), incidence in edges.items():
        assert len(incidence) in (1,2)
        if len(incidence)==1:
            boundary.setdefault(u,set()).add(v)
            boundary.setdefault(v,set()).add(u)
        else:
            (i,s),(j,t)=incidence
            relation=-s*t
            adj[i].append((j,relation)); adj[j].append((i,relation))
    orientable=True; sign={}
    for start in range(len(faces)):
        if start in sign: continue
        sign[start]=1; stack=[start]
        while stack:
            i=stack.pop()
            for j,relation in adj[i]:
                expected=sign[i]*relation
                if j in sign:
                    if sign[j]!=expected: orientable=False
                else:
                    sign[j]=expected; stack.append(j)
    assert all(len(neighbors)==2 for neighbors in boundary.values())
    seen=set(); components=0
    for start in boundary:
        if start in seen: continue
        components+=1; seen.add(start); stack=[start]
        while stack:
            for j in boundary[stack.pop()]:
                if j not in seen: seen.add(j); stack.append(j)
    vertices={v for tri in faces for v in tri}
    return dict(rectangle=[a,b], flip=flipped, orientable=orientable,
                boundary_components=components, euler=len(vertices)-len(edges)+len(faces))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='results.json')
    args=parser.parse_args()
    topology=[topology_example(2,4,False),topology_example(3,3,True),
              topology_example(3,5,True),topology_example(5,5,True)]
    for item in topology:
        assert item['euler']==0
        assert item['orientable'] == (not item['flip'])
        assert item['boundary_components']==(1 if item['flip'] else 2)
    result=dict(version='0.1', date='2026-10-16',
                status='new declared geometric interpretation; inherited calibrated address ledger replay',
                target=dict(ordinary=TARGET_P,dark=TARGET_D,returned=1-TARGET_P-TARGET_D),
                inputs=dict(alpha=ALPHA_FROZEN,h=H_FROZEN,gamma=GAMMA.tolist(),
                            xi=XI,frames=FRAMES,coefficient=COEFFICIENT),
                reference=calculate(N,True),
                cutoff_sensitivity=[calculate(15000),calculate(507500),calculate(2030000)],
                topology_incidence_checks=topology,
                environment=dict(numpy=np.__version__,scipy=scipy.__version__),
                interpretation_limits=[
                    'Dimension means minimum topological ambient embedding dimension of the declared object.',
                    'Parity-dependent seam is a new modeling postulate, not a theorem of arithmetic.',
                    'Mobius band has intrinsic dimension two and a boundary; no boundaryless universe inference.',
                    'Numbers are address weights, not automatically SI mass-energy density fractions.',
                    'The fraction targets and N construction inherit observational calibration.',
                    'No new alpha/h needed to replay the old ledger; numerical refit is a verification only.',
                    'Geometric folding energy, particle mass, pressure, and dynamics are not computed here.'])
    output=Path(args.output)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
