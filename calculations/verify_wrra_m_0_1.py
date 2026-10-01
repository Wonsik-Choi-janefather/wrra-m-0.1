"""Exact color-character and calibrated anomaly checks for WRRA-M 0.1.

Python 3.10+, standard library only. The G2 branching is an input,
not a derivation of G2 or of physical chirality.
"""
from collections import Counter
from fractions import Fraction as Q
import json


def main():
    # SU(3) maximal torus diag(x,y,(xy)^-1); exponents label characters.
    triplet = Counter({(1, 0): 1, (0, 1): 1, (-1, -1): 1})
    antitriplet = Counter({(-a, -b): n for (a, b), n in triplet.items()})
    singlet = Counter({(0, 0): 1})
    seven_complexified = triplet + antitriplet + singlet
    assert sum(seven_complexified.values()) == 7
    assert seven_complexified == Counter({(-a, -b): n for (a, b), n in seven_complexified.items()})
    candidate = singlet + seven_complexified + seven_complexified
    sm_color = triplet + triplet + antitriplet + antitriplet + singlet + singlet + singlet
    assert candidate == sm_color and sum(candidate.values()) == 15
    # Calibrated one-generation benchmark, excluding a sterile neutrino.
    multiplets = [(6, Q(1, 6)), (3, Q(-2, 3)), (3, Q(1, 3)), (2, Q(-1, 2)), (1, Q(1))]
    anomalies = {
        'gravity_U1': sum(n * y for n, y in multiplets),
        'U1_cubed': sum(n * y**3 for n, y in multiplets),
        'SU3_squared_U1': Q(1, 2) * (2*Q(1, 6)+Q(-2, 3)+Q(1, 3)),
        'SU2_squared_U1': Q(1, 2) * (3*Q(1, 6)+Q(-1, 2)),
        'SU3_cubed': 2-1-1,
    }
    assert all(v == 0 for v in anomalies.values())
    assert (3+1) % 2 == 0
    print(json.dumps({'version':'0.1-r1','status':'PASS','complex_color_dimension':15,
        'color_multiplicities':{'3':2,'anti3':2,'1':3},
        'calibrated_anomalies':{k:str(v) for k,v in anomalies.items()},
        'chirality':'physical assumption; not established by this character check'}, indent=2))


if __name__ == '__main__':
    main()
