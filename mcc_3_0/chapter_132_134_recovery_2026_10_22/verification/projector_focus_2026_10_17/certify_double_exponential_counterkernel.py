"""Exact interval counterexample with xi-compatible entire growth order bound.
This is a separately owned kernel, NOT actual theta or a counterexample to RH.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json

def point(x):return F(x),F(x)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[1],a[1]-b[0]
def mul(a,b):
 v=[x*y for x in a for y in b];return min(v),max(v)
def div(a,b):
 assert b[0]>0
 return mul(a,(1/b[1],1/b[0]))
def R(n):return 8*n**3+68*n*n+622*n+1255

epsilon=F(1,10**12)
# K_epsilon=exp[-2*u^2-epsilon*(cosh(2*u)-1-2*u^2)]*P(u^2).
# Gaussian reference gamma_n(0)=S*8^(-n)*R(n).
# A global integral inequality (not a finite-u approximation) gives the interval below.
g=[(F(R(n))-36*epsilon*2**n*R(n),F(R(n))) for n in range(6)]
assert all(v[0]>0 for v in g)
b=[mul(div(x,g[0]),point(F(1,8**n*factorial(n)))) for n,x in enumerate(g)]
b[0]=point(1)
c=[]
for n in range(5):
 value=mul(point((-1)**n*(n+1)),b[n+1])
 for j in range(1,n+1):value=sub(value,mul(point((-1)**j),mul(b[j],c[n-j])))
 c.append(value)
q=[F(0),-F(1,20),F(1)]
value=point(0)
for i in range(3):
 for j in range(3):value=add(value,mul(point(q[i]*q[j]),c[i+j]))
assert value[1]<-F(1,200000000)
# Exact Gaussian reference qHq, for provenance comparison only.
g0=[point(R(n)) for n in range(6)]
b0=[mul(div(x,g0[0]),point(F(1,8**n*factorial(n)))) for n,x in enumerate(g0)];b0[0]=point(1)
c0=[]
for n in range(5):
 x=(-1)**n*(n+1)*b0[n+1][0]
 for j in range(1,n+1):x-=(-1)**j*b0[j][0]*c0[n-j]
 c0.append(x)
v0=sum(q[i]*q[j]*c0[i+j] for i in range(3) for j in range(3))
assert v0==-F(6974019391,797000501000800000)
out={'owner':'fixed-rate double exponential K_epsilon, NOT actual xi/theta',
 'epsilon':str(epsilon),'kernel':'exp[-2*u^2-epsilon*(cosh(2*u)-1-2*u^2)]*(1+u^2)*(15+u^2+u^4)',
 'global_gamma_error':'0<=R(n)-g_n<=36*epsilon*2^n*R(n)',
 'g_intervals':[[str(x) for x in v] for v in g],
 'b_intervals':[[str(x) for x in v] for v in b],
 'c_intervals':[[str(x) for x in v] for v in c],
 'negative_witness_q':list(map(str,q)),
 'quadratic_interval':[str(x) for x in value],
 'display_only':[float(x) for x in value],
 'strict_upper_bound':'-1/200000000',
 'gaussian_reference_value':str(v0),
 'analytic_properties_proved_in_report':['positive even analytic kernel','all odd derivatives at 0 vanish','fixed exp(2u) double exponential decay','log K(sqrt(y)) strictly decreasing and concave','all scalar Turan inequalities from prior covariance proof','normalized entire G has order exactly 1/2'],
 'exact_theta_modularity':'NOT_ASSERTED',
 'RH_status':'OPEN; this is not actual xi'}
Path(__file__).with_name('DOUBLE_EXPONENTIAL_CERTIFICATE.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'epsilon':str(epsilon),'witness_interval':out['display_only'],'upper':out['strict_upper_bound']},indent=2))
