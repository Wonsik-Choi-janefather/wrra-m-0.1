"""All-natural finite projector, exact outward quality intervals.
The source-mode model is separate from actual analytically continued xi.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
BITS=160;S=1<<BITS

def compact(a):
 return F(a[0].numerator*S//a[0].denominator,S),F(-((-a[1].numerator*S)//a[1].denominator),S)
def point(x):return F(x),F(x)
def add(a,b):return compact((a[0]+b[0],a[1]+b[1]))
def mul(a,b):
 p=[x*y for x in a for y in b];return compact((min(p),max(p)))
def div(a,b):
 assert b[0]>0
 return mul(a,(1/b[1],1/b[0]))
def sqrt_bounds(n):
 lo=isqrt(n*S*S);hi=lo if lo*lo==n*S*S else lo+1
 return F(lo,S),F(hi,S)
def js(x):return {'exact':list(map(str,x)),'display_only':list(map(float,x))}

def analyze(N):
 H=point(0);H2=point(0);quarter=point(0)
 for n in range(1,N+1):
  H=add(H,point(F(1,n)));H2=add(H2,point(F(1,n*n)))
  quarter=add(quarter,div(point(1+F(1,n)),sqrt_bounds(n)))
 central=mul(point(2),H);edge=add(point(N),H2)
 E={'0':edge,'1/4':quarter,'1/2':central,'3/4':quarter,'1':edge}
 V={s:div(central,x) for s,x in E.items()};V['1/2']=point(1)
 assert V['0'][1]<1 and V['1/4'][1]<1
 assert E['0'][0]>central[1] and E['1/4'][0]>central[1]
 return {'N':N,'addresses':'every n=1,...,N, including1','pair_energy':{k:js(v) for k,v in E.items()},'aggregate_visibility':{k:js(v) for k,v in V.items()},'signal_2H':js(central),'single_channel_condition_number':{'sigma0':'1','sigma_half':js(sqrt_bounds(N)),'sigma1':str(N)}}

runs=[analyze(n) for n in [16,128,1000]]
out={'owner':'declared two-channel all-natural projector, not a new zeta representation',
 'source_amplitudes':'a_n=n^-sigma, b_n=n^-(1-sigma), same n phase/scene owner',
 'clarity_definition':'mode-resolved or common-reference aggregate interference visibility',
 'readout_precondition':'address-resolved modes, or orthogonal mode readout with calibrated reference phases; raw coherent pixel intensity is not the mode-energy sum',
 'mode_visibility':'1/cosh((2*sigma-1)*log(n))',
 'energy_identity':'a_n^2+b_n^2=2/n*cosh((2*sigma-1)*log(n))',
 'proved_optimum':'For N>=2 and positive mode weights, sigma=1/2 uniquely maximizes visibility and minimizes pair energy at fixed per-mode product.',
 'runs':runs,'full_xi_reflection_control':'xi(s)=xi(1-s); whole-output visibility=1 wherever xi(s)!=0, undefined0/0 at zeros; it does not select a central line',
 'general_center':'pair exponents sigma and2*alpha-sigma yields optimum alpha;1/2 depends on complementary exponent contract',
 'infinite_unweighted_resource':'pair energy at sigma1/2 is2*sum1/n, divergent; implemented finite N only',
 'RH_status':'OPEN','physical_image_quality':'not empirically established'}
Path(__file__).with_name('CLARITY_CERTIFICATE.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'N':1000,'energy':{k:v['display_only'] for k,v in runs[-1]['pair_energy'].items()},'visibility':{k:v['display_only'] for k,v in runs[-1]['aggregate_visibility'].items()}},indent=2))
