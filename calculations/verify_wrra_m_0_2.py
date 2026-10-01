"""Exact operator, electric-charge and anomaly reproduction for WRRA-M 0.2.

Python 3.10+, standard library only. Independent complex left-handed Weyl
channels and the cross-dimensional pairing are declared physical inputs.
"""
from fractions import Fraction as Q
import json


def main():
    # Solve -alpha/2 + beta = 0, alpha/2 + beta = 1.
    a,b,c,d = Q(-1,2),Q(1),Q(1,2),Q(1)
    determinant = a*d-b*c
    assert determinant != 0
    alpha, beta = (Q(0)*d-b*Q(1))/determinant, (a*Q(1)-Q(0)*c)/determinant
    assert (alpha,beta) == (Q(1),Q(1,2))
    # (color dimension, weak dimension, T3R, B-L, expected Y, T3L eigenvalues)
    fields = {
        'Q_L': (3,2,Q(0),Q(1,3),Q(1,6),(Q(1,2),Q(-1,2))),
        'u_c': (3,1,Q(-1,2),Q(-1,3),Q(-2,3),(Q(0),)),
        'd_c': (3,1,Q(1,2),Q(-1,3),Q(1,3),(Q(0),)),
        'L_L': (1,2,Q(0),Q(-1),Q(-1,2),(Q(1,2),Q(-1,2))),
        'e_c': (1,1,Q(1,2),Q(1),Q(1),(Q(0),)),
        'nu_c': (1,1,Q(-1,2),Q(1),Q(0),(Q(0),)),
    }
    expected_electric = {'Q_L':(Q(2,3),Q(-1,3)),'u_c':(Q(-2,3),),
        'd_c':(Q(1,3),),'L_L':(Q(0),Q(-1)),'e_c':(Q(1),),'nu_c':(Q(0),)}
    rows = {}
    for name,(color,weak,t3r,bl,expected,t3l) in fields.items():
        y = alpha*t3r + beta*bl
        electric = tuple(t+y for t in t3l)
        assert y == expected and electric == expected_electric[name]
        rows[name] = {'multiplicity':color*weak,'Y':str(y),'Q':[str(q) for q in electric]}
    assert sum(row['multiplicity'] for row in rows.values()) == 16
    anomalies = {
        'gravity_U1':sum(c*w*y for c,w,_,_,y,_ in fields.values()),
        'U1_cubed':sum(c*w*y**3 for c,w,_,_,y,_ in fields.values()),
        'SU3_squared_U1':sum(w*Q(1,2)*y for c,w,_,_,y,_ in fields.values() if c == 3),
        'SU2_squared_U1':sum(c*Q(1,2)*y for c,w,_,_,y,_ in fields.values() if w == 2),
        'SU3_cubed':2-1-1,
    }
    assert all(value == 0 for value in anomalies.values())
    su2_doublets = {'left':3+1,'right':3+1}
    assert all(n % 2 == 0 for n in su2_doublets.values())
    # B-L generators on 4 and anti4 are traceless.
    assert 3*Q(1,3)-1 == 0 and 3*Q(-1,3)+1 == 0
    print(json.dumps({'version':'0.2-r1','status':'PASS','alpha':str(alpha),'beta':str(beta),
        'channels':rows,'anomalies':{k:str(v) for k,v in anomalies.items()},
        'SU2_doublets':su2_doublets},indent=2))


if __name__ == '__main__':
    main()
