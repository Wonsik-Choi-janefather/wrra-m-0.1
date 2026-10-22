"""Finite KZF audit implementation. Bounds are computational policy, not physics."""
from fractions import Fraction
from math import lcm,isfinite,isqrt
from bisect import bisect_left
import numpy as np
import mpmath as mp
MAX_ADDRESSES=2_000_000

def integer(x,name,minimum=0):
 if type(x) is not int or x<minimum:raise ValueError(name+'_INVALID_INTEGER')
 return x

def resolution(shares):
 if not shares or any(type(x) is not str for x in shares):raise ValueError('EXACT_DECIMAL_STRINGS_REQUIRED')
 try:f=[Fraction(x) for x in shares]
 except (ValueError,ZeroDivisionError):raise ValueError('INVALID_FRACTION')
 if any(x<0 for x in f) or sum(f)!=1:raise ValueError('SHARES_NOT_NONNEGATIVE_UNIT_SUM')
 L=lcm(*(x.denominator for x in f))
 return L,[int(x*L) for x in f]

def dimensions(L,H,C):
 for x,name in [(L,'L'),(H,'H')]:integer(x,name,1)
 integer(C,'C');N=L*H*C
 if N>MAX_ADDRESSES:raise ValueError('COMPUTE_BUDGET_EXCEEDED')
 return N

def encode(ell,h,z,L,H,C):
 dimensions(L,H,C)
 for x,name in [(ell,'ell'),(h,'h'),(z,'z')]:integer(x,name)
 if not (ell<L and h<H and 1<=z<=C):raise ValueError('COORDINATE_OUT_OF_DOMAIN')
 return 1+ell+L*(h+H*(z-1))

def decode(n,L,H,C):
 N=dimensions(L,H,C);integer(n,'n',1)
 if n>N:raise ValueError('ADDRESS_OUT_OF_DOMAIN')
 q,ell=divmod(n-1,L);z,h=divmod(q,H)
 return ell,h,z+1

def spectral_count(heights,T):
 # Strict < convention. A supplied pool must contain a next (excluded) height.
 if not mp.isfinite(T) or T<0:raise ValueError('INVALID_THRESHOLD')
 if not heights or any(not mp.isfinite(x) or x<=0 for x in heights):raise ValueError('INVALID_ZERO_POOL')
 if any(a>=b for a,b in zip(heights,heights[1:])):raise ValueError('UNORDERED_ZERO_POOL')
 if heights[-1]<T:raise ValueError('UNBRACKETED_WINDOW')
 return bisect_left(heights,T)

def window(H,dps=50):
 integer(H,'H',1);integer(dps,'dps',30)
 if H>40 or dps>120:raise ValueError('SPECTRAL_COMPUTE_BUDGET_EXCEEDED')
 with mp.workdps(dps):
  T=2*mp.pi*H;cnt=int(mp.nzeros(T));last=mp.im(mp.zetazero(cnt)) if cnt else None
  nxt=mp.im(mp.zetazero(cnt+1))
  if last is not None and last==T:cnt-=1;nxt=last;last=mp.im(mp.zetazero(cnt)) if cnt else None
  if not ((last is None or last<T) and T<=nxt):raise ValueError('ZERO_WINDOW_NOT_BRACKETED')
  fmt=lambda x:mp.nstr(x,dps) if x is not None else None
  return {'H':H,'dps':dps,'C':cnt,'T':fmt(T),'gamma_last':fmt(last),'gamma_next':fmt(nxt),'gap_below':fmt(T-last) if last else None,'gap_above':fmt(nxt-T),'boundary':'strict positive height < T'}

def ledger(L,H,C,alpha):
 N=dimensions(L,H,C)
 if not isinstance(alpha,(float,int)) or isinstance(alpha,bool) or not isfinite(alpha) or abs(alpha)>100:raise ValueError('ALPHA_OUT_OF_NUMERICAL_DOMAIN')
 n=np.arange(1,N+1,dtype=np.int64);q=n-1
 ell=q%L;h=q//L%H;z=q//(L*H)+1
 spf=np.zeros(N+1,dtype=np.int64)
 for p in range(2,N+1):
  if spf[p]==0:
   spf[p]=p
   if p*p<=N:
    v=spf[p*p::p];v[v==0]=p
 kind=np.zeros(N,dtype=np.uint8)
 if N>=2:
  prime=spf[2:]==n[1:];kind[1:]=np.where(prime,1,np.where(n[1:]%2==0,2,3))
 weight=np.zeros(N)
 if N>=2:
  logw=-alpha*np.log(n[1:].astype(float));logw-=max(logw);v=np.exp(logw)
  if np.any(v==0) or not np.isfinite(v).all():raise ValueError('WEIGHT_UNDERFLOW_OR_NONFINITE')
  weight[1:]=v/v.sum()
 return dict(n=n,ell=ell,h=h,z=z,kind=kind,weight=weight)

def seam(ell,h,z,L,H,C,inverse=False):
 encode(ell,h,z,L,H,C)
 if inverse:return ((-ell)%L,h,C) if z==1 else (ell,h,z-1)
 return ((-ell)%L,h,1) if z==C else (ell,h,z+1)

def finite_em(s,M):
 integer(M,'M',2)
 s=complex(s)
 if not isfinite(s.real) or not isfinite(s.imag):raise ValueError('NONFINITE_S')
 if s==1:raise ValueError('ZETA_POLE_AT_ONE')
 if s.real<=-5:raise ValueError('REMAINDER_BOUND_DOMAIN_REQUIRES_REAL_S_GT_MINUS5')
 if M>100000:raise ValueError('EM_COMPUTE_BUDGET_EXCEEDED')
 a=np.arange(1,M,dtype=float)
 return np.exp(-s*np.log(a)).sum()+M**(1-s)/(s-1)+.5*M**(-s)+s/12*M**(-s-1)-s*(s+1)*(s+2)/720*M**(-s-3)

def em_analytic_bound(s,M):
 # Exact-arithmetic truncation bound: omitted B6 term + bounded periodic-B6 remainder.
 # Does not bound floating-point rounding or mpmath's evaluation error.
 s=mp.mpc(s);sigma=mp.re(s)
 if sigma<=-5 or M<2:raise ValueError('BOUND_DOMAIN')
 prod5=mp.rf(s,5);prod6=mp.rf(s,6)
 return abs(prod5)/30240*mp.power(M,-sigma-5)+2*mp.zeta(6)/(2*mp.pi)**6*abs(prod6)/(sigma+5)*mp.power(M,-sigma-5)
