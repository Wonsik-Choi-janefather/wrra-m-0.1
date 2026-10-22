"""Exact tests of a declared projector stability contract, not RH."""
from fractions import Fraction as Q
import json

def compute():
    # L=4 log 2. A mode's worst gain on |u|<=L is 2^(4|beta-c|).
    # All exponents below are integers, allowing exact arithmetic.
    spectra={'centered':[Q(1,2)],'symmetric_offline_diagnostic':[Q(1,4),Q(3,4)]}
    result={}
    for label,betas in spectra.items():
        rows=[]
        for c in [Q(1,4),Q(1,2),Q(3,4)]:
            radius=max(abs(b-c) for b in betas)
            exponent=4*radius
            assert exponent.denominator==1
            gain=2**exponent.numerator
            rows.append({'c':str(c),'radius':str(radius),'worst_gain':gain})
        result[label]=rows
    assert result['symmetric_offline_diagnostic'][1]['worst_gain']==2
    assert result['centered'][1]['worst_gain']==1
    assert all(result['symmetric_offline_diagnostic'][i]['worst_gain']==4 for i in [0,2])
    # At c=1/2, u=L: beta=3/4 has gain2, beta=1/4 has gain1/2.
    gain_pair=[Q(2),Q(1,2)]
    assert gain_pair[0]*gain_pair[1]==1
    assert sum(gain_pair)/2==Q(5,4)
    # Self-adjoint metric positivity: (A*W+WA)_jj=2*(beta_j-c)*W_jj.
    # A positive diagonal entry W_jj cannot eliminate nonzero beta_j-c.
    return {'scope':'exact conditional carrier diagnostics; synthetic beta values are not actual zeta zeros',
            'window':'L=4*log(2)', 'minimax_rows':result,
            'offline_mode_gains_at_L':['2','1/2'],
            'gain_product':'1','arithmetic_mean_gain':'5/4',
            'proved_contract':'norm preservation for all coefficient vectors and shifts iff each beta=c',
            'remaining_obligation':'derive norm-preserving contract from actual xi/theta, without assuming RH',
            'actual_xi_new_inequality':False,'RH_status':'OPEN'}

if __name__=='__main__':print(json.dumps(compute(),ensure_ascii=False,indent=2))
