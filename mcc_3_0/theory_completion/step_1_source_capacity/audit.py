"""Exact arithmetic SOURCE audit. Tolerances are scenarios, not observation errors."""
from fractions import Fraction as F
from math import lcm, ceil, floor
import json
from pathlib import Path

HC = 29 * 70
targets = tuple(map(F, ('0.05','0.268','0.682')))

def denominator(values):
    return lcm(*(x.denominator for x in values))

def witness(L, values, eps):
    bounds = [(max(0,ceil(L*(x-eps))),min(L,floor(L*(x+eps)))) for x in values]
    if any(a>b for a,b in bounds) or sum(a for a,b in bounds)>L or sum(b for a,b in bounds)<L:
        return None
    counts=[a for a,b in bounds]
    remainder=L-sum(counts)
    for i,(a,b) in enumerate(bounds):
        extra=min(remainder,b-a)
        counts[i]+=extra
        remainder-=extra
    return counts

def minimal(values, eps):
    for L in range(1,denominator(values)+1):
        counts=witness(L,values,eps)
        if counts is not None:
            return {'epsilon':str(eps),'L':L,'N':L*HC,'counts':counts,
                    'shares':[str(F(k,L)) for k in counts]}
    raise AssertionError('Exact target denominator must be feasible')

decimal_cases=[('0.05','0.268','0.682'),('0.0500','0.2680','0.6820'),
               ('0.0501','0.2680','0.6819'),('0.05001','0.26800','0.68199')]
cases=[{'inputs':v,'L':denominator(tuple(map(F,v))),
        'N':denominator(tuple(map(F,v)))*HC} for v in decimal_cases]
scenarios=[minimal(targets,F(e)) for e in ('0','0.00005','0.0001','0.0005','0.001','0.005')]
fixed=[]
for v in decimal_cases:
    values=tuple(map(F,v))
    fixed.append({'inputs':v,'fixed_L':500,'epsilon':'0.0001',
                  'counts':witness(500,values,F('0.0001'))})
assert cases[0]['L']==cases[1]['L']==500
assert cases[2]['L']==10000 and cases[3]['L']==100000
assert all(x['counts']==[25,134,341] for x in fixed)
assert witness(500,tuple(map(F,decimal_cases[2])),F(0)) is None
for row in scenarios:
    assert sum(row['counts'])==row['L']
    assert all(abs(F(k,row['L'])-x)<=F(row['epsilon']) for k,x in zip(row['counts'],targets))
    assert all(witness(L,targets,F(row['epsilon'])) is None for L in range(1,row['L']))
result={'scope':'denominator factor only; H=29 and C=70 frozen, not rederived',
        'decimal_cases':cases,'illustrative_tolerance_scenarios':scenarios,
        'fixed_resolution_controls':fixed,
        'warning':'Counts are rational representation units, not actual prime-filter populations.'}
best=None
for L in range(1,500):
    lower,upper=0,500
    while lower<upper:
        mid=(lower+upper)//2
        if witness(L,targets,F(mid,500*L)) is not None:
            upper=mid
        else:
            lower=mid+1
    distance=F(lower,500*L)
    if best is None or distance<best['distance']:
        best={'distance':distance,'L':L,'counts':witness(L,targets,distance)}
assert best['distance']==F(1,9180)
assert best['L']==459
result['nearest_smaller_resolution']={'L':best['L'],'counts':best['counts'],
    'minimax_error':str(best['distance']),'float_error':float(best['distance']),
    'robustness_condition':'delta <= epsilon < 1/9180 - delta (sufficient)',
    'maximum_symmetric_guarantee_delta_strictly_below':str(best['distance']/2)}
Path(__file__).with_name('results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
