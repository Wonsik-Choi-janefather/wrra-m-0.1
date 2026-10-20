"""Finite WRRA upstream exchange candidate, not a unique physical derivation.
Run: python3 exchange.py. NumPy is needed only for the quantum SWAP check.
No upstream seconds, metres, flow or phenotype allocation is introduced.
"""
from dataclasses import dataclass, replace
from pathlib import Path
import json, hashlib, math, platform
import numpy as np

L,H,C=500,29,70
N=L*H*C
P2=[1<<e for e in range(1,L+1)]
P3=[3**e for e in range(1,H+1)]
P5=[5**e for e in range(1,C+1)]

def address(ell,h,z):
    if not (type(ell) is int and type(h) is int and type(z) is int and 0<=ell<L and 0<=h<H and 1<=z<=C):
        raise ValueError('KZF coordinate outside frozen finite domain')
    return 1+ell+L*(h+H*(z-1))

def coords(a):
    if type(a) is not int or not 1<=a<=N: raise ValueError('unknown SOURCE address')
    t=a-1
    return t%L,(t//L)%H,t//(L*H)+1

def encode(ell,h,z):
    address(ell,h,z)
    return P2[ell]*P3[h]*P5[z-1]

def decode(q):
    if type(q) is not int or q<=0: raise ValueError('invalid carrier integer')
    e2=(q&-q).bit_length()-1; q>>=e2
    e3=e5=0
    while q%3==0: q//=3; e3+=1
    while q%5==0: q//=5; e5+=1
    if q!=1: raise ValueError('undeclared factor in carrier')
    v=e2-1,e3-1,e5
    address(*v)
    return v

@dataclass(frozen=True)
class Packet:
    q: int
    payload: int

class Exchange:
    """One packet, exclusive owner. Event labels are not physical time."""
    def __init__(self,p):
        a=address(*decode(p.q))
        if a==1: raise ValueError('inactive reference is not an active message')
        if not 0<=p.payload<2**16: raise ValueError('payload outside declared register')
        self.owners={'top':p,'mid':None}
        self.events=set()
    def move(self,src,dst,event,permit=True):
        if (src,dst) not in [('top','mid'),('mid','top')]: raise ValueError('invalid interface')
        if type(permit) is not bool: raise ValueError('permission must be Boolean')
        if not permit: return False
        if event in self.events: raise ValueError('replayed transfer')
        if self.owners[src] is None or self.owners[dst] is not None: raise ValueError('invalid owner')
        self.owners[dst]=self.owners[src]
        self.owners[src]=None
        self.events.add(event)
        return True
    def feedback(self):
        p=self.owners['mid']
        if p is None: raise ValueError('feedback requires middle ownership')
        a=address(*decode(p.q))
        # A declared reversible information operation, not a physical force.
        self.owners['mid']=replace(p,payload=p.payload^(a&65535))

def build_primes():
    sieve=bytearray(b'\x01')*(N+1);sieve[:2]=b'\x00\x00'
    for p in range(2,math.isqrt(N)+1):
        if sieve[p]: sieve[p*p::p]=b'\x00'*((N-p*p)//p+1)
    return sieve

def to_middle(q,payload):
    if type(payload) is not int or not 0<=payload<2**16: raise ValueError('invalid payload register')
    a=address(*decode(q))
    if a==1: return {'kind':'reference','address':a,'payload':payload}
    if a%2==0: return {'kind':'retained','address':a,'payload':payload}
    return {'kind':'singly_even_candidate','r':2*a,'payload':payload}

def from_middle(m):
    if not isinstance(m,dict) or 'kind' not in m: raise ValueError('missing middle state tag')
    kind=m['kind']
    if kind not in ['singly_even_candidate','reference','retained']: raise ValueError('unknown tagged state')
    keys={'kind','payload','r' if kind=='singly_even_candidate' else 'address'}
    if set(m)!=keys: raise ValueError('undeclared or missing middle register')
    if type(m['payload']) is not int or not 0<=m['payload']<2**16: raise ValueError('invalid payload register')
    if kind=='singly_even_candidate':
        r=m['r']
        if type(r) is not int or r%4!=2: raise ValueError('invalid singly-even parent')
        a=r//2
    else: a=m['address']
    coords(a)
    if kind=='reference' and a!=1: raise ValueError('reference tag does not match address')
    if kind=='retained' and a%2!=0: raise ValueError('retained tag does not match address')
    if kind=='singly_even_candidate' and a==1: raise ValueError('reference cannot become active candidate')
    return Packet(encode(*coords(a)),m['payload'])

def admitted(m,prime,permit):
    if type(permit) is not bool: raise ValueError('permission must be Boolean')
    from_middle(m)
    if m['kind']!='singly_even_candidate' or not permit: return False
    a=m['r']//2
    return a>1 and not prime[a]

def verify():
    primes=build_primes(); counts={'reference':0,'prime':0,'even_composite':0,'odd_composite':0}
    types={'reference':0,'retained':0,'singly_even_candidate':0}
    digest=hashlib.sha256();maxbits=0;transfers=0;allowed=0
    for a in range(1,N+1):
        v=coords(a);q=encode(*v)
        assert decode(q)==v and address(*decode(q))==a
        assert q%30==0
        maxbits=max(maxbits,q.bit_length())
        b=q.to_bytes((q.bit_length()+7)//8,'big');digest.update(len(b).to_bytes(2,'big')+b)
        if a==1: counts['reference']+=1
        elif primes[a]:counts['prime']+=1
        elif a%2==0:counts['even_composite']+=1
        else:counts['odd_composite']+=1
        payload=(37*a+11)&65535
        m=to_middle(q,payload);types[m['kind']]+=1
        assert from_middle(m)==Packet(q,payload)
        allowed+=int(admitted(m,primes,True))
        assert not admitted(m,primes,False)
        if a>1:
            e=Exchange(Packet(q,payload))
            assert not e.move('top','mid','closed',False)
            assert e.move('top','mid','forward')
            assert e.owners['top'] is None
            e.feedback()
            assert e.move('mid','top','reply')
            got=e.owners['top'];assert e.owners['mid'] is None
            assert got.q==q and (got.payload^(a&65535))==payload
            transfers+=2
        if a%200000==0:print(f'checked SOURCE labels {a}/{N}',flush=True)

    negatives={}
    def rejects(name,fn):
        try: fn()
        except ValueError:negatives[name]=True
        else:raise AssertionError(name+' was not rejected')
    rejects('zero_address',lambda:coords(0))
    rejects('address_above_N',lambda:coords(N+1))
    rejects('zero_carrier',lambda:decode(0))
    rejects('undeclared_factor',lambda:decode(encode(8,0,1)*7))
    rejects('exponent_out_of_range',lambda:decode(2**501*3*5))
    rejects('missing_factor',lambda:decode(2*3))
    rejects('inactive_reference_transfer',lambda:Exchange(Packet(30,0)))
    e=Exchange(Packet(encode(*coords(9)),123))
    rejects('reverse_without_middle_owner',lambda:e.move('mid','top','bad'))
    e.move('top','mid','forward');e.move('mid','top','reply')
    rejects('replayed_event_after_return',lambda:e.move('top','mid','forward'))
    rejects('invalid_parent_mod4',lambda:from_middle({'kind':'singly_even_candidate','r':20,'payload':0}))
    rejects('unknown_state_kind',lambda:from_middle({'kind':'unknown'}))
    rejects('nonboolean_permission',lambda:e.move('top','mid','new',1))
    rejects('false_reference_tag',lambda:from_middle({'kind':'reference','address':9,'payload':0}))
    rejects('false_retained_tag',lambda:from_middle({'kind':'retained','address':9,'payload':0}))
    rejects('reference_as_candidate',lambda:from_middle({'kind':'singly_even_candidate','r':2,'payload':0}))
    rejects('extra_unowned_register',lambda:from_middle({'kind':'reference','address':1,'payload':0,'lost':7}))
    rejects('payload_out_of_range',lambda:to_middle(30,65536))
    rejects('candidate_out_of_SOURCE',lambda:from_middle({'kind':'singly_even_candidate','r':2*(N+1),'payload':0}))

    # Quantum payload transfer is SWAP, not copying an unknown state.
    # Basis order: external reference R, top T, middle M.
    SW=np.zeros((8,8),complex)
    for k in range(8):
        r,t,m=(k>>2)&1,(k>>1)&1,k&1
        SW[(r<<2)|(m<<1)|t,k]=1
    rng=np.random.default_rng(1351203);waveerr=reducederr=spectrumerr=0.
    for _ in range(200):
        rt=rng.normal(size=4)+1j*rng.normal(size=4);rt/=np.linalg.norm(rt)
        psi=np.kron(rt,[1,0]);moved=SW@psi;back=SW@moved
        waveerr=max(waveerr,float(np.max(np.abs(back-psi))))
        tensor=moved.reshape(2,2,2)
        rm=np.einsum('rtm,stn->rmsn',tensor,tensor.conj()).reshape(4,4)
        orig=np.outer(rt,rt.conj())
        reducederr=max(reducederr,float(np.max(np.abs(rm-orig))))
        top=np.einsum('rtm,rum->tu',tensor,tensor.conj())
        assert np.max(np.abs(top-np.diag([1,0])))<1e-12
        spectrumerr=max(spectrumerr,float(np.max(np.abs(np.linalg.eigvalsh(rm)-np.linalg.eigvalsh(orig)))))
    assert counts=={'reference':1,'prime':79608,'even_composite':507499,'odd_composite':427892},counts
    assert allowed==counts['odd_composite']
    assert max(waveerr,reducederr,spectrumerr)<1e-12
    out={'version':'0.1','verification_status':'PASS','construction_status':'EXPLICIT_FINITE_CANDIDATE_NOT_UNIQUE_PHYSICAL_DERIVATION',
      'inputs':{'L':L,'H':H,'C':C,'N':N,'coordinate_domain':'ell=0..499,h=0..28,z=1..70',
      'SOURCE_serialization':'a=1+ell+500*(h+29*(z-1))','carrier':'q=2^(ell+1)*3^(h+1)*5^z',
      'terminology':'WRRA quasi-prime = composite atomic transport envelope; no Fermat claim',
      'feedback':'16-bit payload XOR (a mod 65536); illustrative reversible operation',
      'seconds_metres_or_flow_assigned_upstream':False},
      'all_SOURCE_codec_cases':N,'active_bidirectional_sessions':N-1,
      'one_way_ownership_transfers':transfers,'source_classification':counts,
      'middle_tag_counts':types,'odd_composite_structural_admissions':allowed,
      'physical_emissions_in_this_audit':0,
      'carrier_max_bits':maxbits,'carrier_stream_sha256':digest.hexdigest(),
      'rejected_controls':negatives,
      'quantum_transfer':{'cases':200,'swap_unitarity_error':float(np.max(np.abs(SW.conj().T@SW-np.eye(8)))),
        'roundtrip_wavefunction_error':waveerr,'external_reference_joint_state_error':reducederr,
        'joint_spectrum_error':spectrumerr,'top_blank_after_move':True,
        'scope':'three-qubit subsystem ownership SWAP; not full quantum amplitude generator'},
      'environment':{'python':platform.python_version(),'numpy':np.__version__},
      'not_claimed':['standard number-theory pseudoprimality','unique carrier choice',
        'physical density/energy/mass from carrier magnitude','new SOURCE addresses from r=2a',
        'derivation of KZF input sizes','empirical proof of physical topmost and middle layers',
        'full interacting microscopic dynamics','physical time before phenotype']}
    out['examples']={str(a):to_middle(encode(*coords(a)),0) for a in [1,2,5,9,10,105,N-1,N]}
    Path(__file__).with_name('results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__': verify()
