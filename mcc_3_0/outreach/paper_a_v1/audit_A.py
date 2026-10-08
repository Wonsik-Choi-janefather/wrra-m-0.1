"""Reproducible numerical audit for executive paper A. No network required.
Floating-point winding is a numerical diagnostic, not interval certification.
"""
from pathlib import Path
from fractions import Fraction
from math import lcm
import json, sys, platform
import numpy as np
import mpmath as mp
mp.mp.dps=40
R=Path(__file__).resolve().parent
L= lcm(*(Fraction(x).denominator for x in ('0.05','0.268','0.682')))
H=29; T=2*mp.pi*H; C=int(mp.nzeros(T)); N=L*H*C
q=np.arange(N,dtype=np.int64)
ell=q%L; h=(q//L)%H; z=q//(L*H)
assert np.array_equal(ell+L*(h+H*z),q)
assert (L,H,C,N)==(500,29,70,1015000)
g70=mp.im(mp.zetazero(70));g71=mp.im(mp.zetazero(71))
# Standard finite Euler-Maclaurin approximation, not a new spectral operator.
def em(s,M=256,K=12):
    s=np.asarray(s,dtype=complex); out=np.zeros_like(s)
    ln=np.log(np.arange(1,M,dtype=float))
    flat=s.reshape(-1); vals=[]
    for j in range(0,len(flat),256):
        v=flat[j:j+256]
        a=np.exp(-v[:,None]*ln).sum(axis=1)
        a+=np.exp((1-v)*np.log(M))/(v-1)+.5*np.exp(-v*np.log(M))
        rising=np.ones_like(v)
        for k in range(1,2*K):
            rising*=v+k-1
            if k%2:
                b=float(mp.bernoulli(k+1)/mp.factorial(k+1))
                a+=b*rising*np.exp((-v-k)*np.log(M))
        vals.append(a)
    return np.concatenate(vals).reshape(s.shape)
def contour(nv,nh,Tvalue):
    a=.25; b=.75; c=.1; d=Tvalue
    return np.concatenate([np.linspace(a,b,nh,endpoint=False)+1j*c,
      b+1j*np.linspace(c,d,nv,endpoint=False),
      np.linspace(b,a,nh,endpoint=False)+1j*d,
      a+1j*np.linspace(d,c,nv,endpoint=False)])
rows=[]
for M,K,nv,nh in [(256,12,4096,256),(256,12,8192,512),(512,16,8192,512)]:
    s=contour(nv,nh,float(T)); v=em(s,M,K)
    phases=np.angle(np.roll(v,-1)/v)
    winding=float(phases.sum()/(2*np.pi))
    rows.append(dict(M=M,K=K,vertical_segments=nv,horizontal_segments=nh,
      winding=winding,min_sampled_modulus=float(abs(v).min()),max_phase_step=float(abs(phases).max())))
    assert abs(winding-70)<1e-9 and abs(phases).max()<.5
# Controlled crossing: lowering top edge below gamma70 must remove one zero.
s=contour(8192,512,float(g70-mp.mpf('.01')));v=em(s)
negative=float(np.angle(np.roll(v,-1)/v).sum()/(2*np.pi));assert abs(negative-69)<1e-9
# Compare finite EM at imported locations; no root-location certification inferred.
zeros=np.array([complex(mp.zetazero(i)) for i in range(1,71)])
res=float(abs(em(zeros,14500,4)).max())
# High precision spot checks of the same finite formula against mpmath zeta.
def em_mp(s,M=256,K=12):
    s=mp.mpc(s)
    return mp.fsum(mp.power(n,-s) for n in range(1,M))+mp.power(M,1-s)/(s-1)+mp.power(M,-s)/2+mp.fsum(mp.bernoulli(2*k)/mp.factorial(2*k)*mp.rf(s,2*k-1)*mp.power(M,1-s-2*k) for k in range(1,K+1))
spots=[mp.mpc('.25','.1'),mp.mpc('.75',T),mp.mpc('.5',T),mp.mpc('.25','100')]
spot_error=max(abs(em_mp(s)-mp.zeta(s)) for s in spots)
alpha=1.8996876950554356
ZN=float(np.sum(np.arange(2,N+1,dtype=float)**(-alpha)))
finite_tail=float(np.sum(np.arange(1000001,N+1,dtype=float)**(-alpha)))
result={'runtime':{'python':platform.python_version(),'numpy':np.__version__,'mpmath':mp.__version__},
'L':L,'H':H,'C_nzeros':C,'N':N,'active_count':N-1,'serialization_all_codes_pass':True,
'T':str(T),'gamma70':str(g70),'gamma71':str(g71),'lower_margin':str(T-g70),'upper_margin':str(g71-T),
'relative_downward_margin':str((T-g70)/T),'C_at_T_minus_001':int(mp.nzeros(T-mp.mpf('.01'))),
'winding_checks':rows,'lowered_boundary_winding':negative,
'finite_EM_M14500_K4_imported_zero_max_abs_value':res,
'high_precision_spot_max_error':str(spot_error),
'cutoff_comparison':{'alpha':alpha,'N_old':1000000,'N_new':N,'tail_mass_over_Znew':finite_tail/ZN,'tail_to_infinity_integral_bound_over_Znew':float(N**(1-alpha)/(alpha-1)/ZN)},
'scope':'Numerical diagnostic on rectangle .25<=Re(s)<=.75, .1<=Im(s)<=T. No interval-certified winding or all-strip theorem. nzeros provides separate standard-library count.'}
(R/'evidence/audit_A_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
