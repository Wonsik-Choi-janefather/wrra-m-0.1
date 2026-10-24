"""Finite SOURCE/readout information audit; physical cost remains a separate input."""
from collections import Counter
import math


def entropy(counts):
    total=sum(counts)
    return -sum((n/total)*math.log2(n/total) for n in counts if n)


def conditional_discard(states,readout):
    groups=Counter(readout(x) for x in states)
    # Uniform input over distinct SOURCE states; deterministic readout.
    return math.log2(len(states))-entropy(groups.values())


def run():
    states=[(a,b) for a in (0,1) for b in (0,1)]
    only=conditional_discard(states,lambda x:(x[0]&x[1],))
    plus_a=conditional_discard(states,lambda x:(x[0],x[0]&x[1]))
    full=conditional_discard(states,lambda x:(x[0],x[1],x[0]&x[1]))
    # Bijective reversible embedding, tested on all eight states.
    domain=[(a,b,t) for a in (0,1) for b in (0,1) for t in (0,1)]
    transformed=[(a,b,t^(a&b)) for a,b,t in domain]
    recovered=[(a,b,t^(a&b)) for a,b,t in transformed]
    assert len(set(transformed))==8 and recovered==domain
    # Information bound in a declared ideal classical, isothermal, degenerate-bit
    # reset model with retained side information usable by the protocol.
    kB=1.380649e-23;temperature=300.0;unit=kB*temperature*math.log(2)
    rows=[dict(retained='AND output',discarded_bits=only,ideal_reset_lower_bound_J=unit*only),
          dict(retained='input a and AND output',discarded_bits=plus_a,ideal_reset_lower_bound_J=unit*plus_a),
          dict(retained='both inputs and AND output',discarded_bits=full,ideal_reset_lower_bound_J=unit*full)]
    return dict(source_states=states,rows=rows,reversible_states_checked=len(domain),
      temperature_K=temperature,ideal_one_unbiased_bit_J=unit,
      missing_for_device_claim=['measured complete-cycle work and heat','physical memory Hamiltonian and reset protocol','measurement/copy/control costs','side-information reset accounting'],
      scope='Finite exhaustive WRRA information-retention mapping using standard information theory as external input. The lower bound is conditional, not measured heat, nor an executed integration into a cosmological energy ledger.')
