"""Arithmetic limits for the declared WRRA filter proxy, not physical dynamics."""
import json
import math
from pathlib import Path
from scipy.special import zeta

def mobius(k):
    sign, p = 1, 2
    while p*p <= k:
        if k % p == 0:
            k //= p
            sign = -sign
            if k % p == 0:
                return 0
        p += 1
    return -sign if k > 1 else sign

def prime_zeta(a, terms=80):
    # log zeta(a) = sum_{r>=1} P(r*a)/r, then Möbius inversion.
    return sum(mobius(k)*math.log(float(zeta(a*k, 1)))/k
               for k in range(1, terms+1))

def limits(a):
    z = float(zeta(a, 1))
    p = prime_zeta(a)
    odd = ((1-2**(-a))*(z-1)-p)/(z-1)
    return {'alpha': a, 'zeta': z, 'prime_zeta': p,
            'odd_composite_fraction': odd, 'even_composite_fraction': 2**(-a),
            'prime_fraction': p/(z-1)}

if __name__ == '__main__':
    data = {'status': 'declared arithmetic proxy with alpha>1',
            'limits': [limits(2.), limits(1.9)],
            'alpha_for_even_target_in_infinite_limit': -math.log(.268)/math.log(2),
            'checks': {'prime_zeta_40_vs_80': abs(prime_zeta(2.,40)-prime_zeta(2.,80)) < 1e-14,
                       'alpha2_partition': abs(sum(limits(2.)[k] for k in ('odd_composite_fraction','even_composite_fraction','prime_fraction'))-1) < 1e-14},
            'scope': 'No topology, particle constants, zeta-zero dynamics or pressure is calculated.'}
    assert all(data['checks'].values())
    Path(__file__).with_name('analytic_limit.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(json.dumps(data, indent=2))
