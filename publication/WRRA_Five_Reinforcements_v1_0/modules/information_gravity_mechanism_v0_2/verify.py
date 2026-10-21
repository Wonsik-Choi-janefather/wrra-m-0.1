"""Independent gate ODE, constrained minimization and photon quadrature checks."""
from pathlib import Path
import numpy as np,json,math
from scipy.integrate import solve_ivp,quad
from scipy.optimize import brentq,minimize_scalar
P=Path(__file__).resolve().parent;r=json.loads((P/'results.json').read_text());checks={}
# An actual ODE integration supplies admission, without evaluating its exponential solution.
yvals=np.geomspace(1e-8,100,41);errors=[]
for y in yvals:
 sigma=math.sqrt(y)
 sol=solve_ivp(lambda s,p:[-p[0],p[0]],(0,sigma),[1.,0.],method='DOP853',rtol=2e-12,atol=1e-22)
 assert sol.success
 g=y/sol.y[1,-1];old=y/(-math.expm1(-math.sqrt(y)))
 errors.append(abs(g/old-1))
checks['independent_ODE_RAR']=max(errors)<1e-10
# Independent adaptive quadrature and convex minimization at known target x.
def psi(y):
 if y==0:return 0.
 s=math.sqrt(y)
 return quad(lambda z:0 if z==0 else 2*z**3/(-math.expm1(-z)),0,s,epsabs=1e-13,epsrel=1e-12)[0]
mins=[]
for y0 in [.01,.1,1.,10.]:
 x=y0/(-math.expm1(-math.sqrt(y0)))
 sol=minimize_scalar(lambda y:psi(y)-x*y,bounds=(y0*.1,y0*3),method='bounded',options={'xatol':1e-13})
 err=abs(sol.x/y0-1);mins.append(err)
checks['independent_convex_minimum']=max(mins)<2e-7
# Direct infinite-precision physics is not claimed: finite quadrature of frozen lens patch.
G=6.6743e-11;c=299792458.;pc=30856775814913670.;mass=6e10*1.98847e30;a=3000*pc;impact=10000*pc;patch=200000*pc;zmax=math.sqrt(patch*patch-impact*impact);aT=r['origin_reference']['aT_m_s2']
def f(z):
 rad=math.hypot(impact,z);gb=G*mass*rad/(rad*rad+a*a)**1.5
 # Direct old formula, separate scalar implementation.
 g=gb/(-math.expm1(-math.sqrt(gb/aT)))
 return g*impact/rad
value,est=quad(f,0,zmax,epsabs=1e-3,epsrel=2e-12)
angle=4*value/c**2*180/math.pi*3600
checks['independent_finite_patch_lensing']=abs(angle-r['origin_reference']['lensing_arcsec'])<1e-10
checks={k:bool(v) for k,v in checks.items()}
assert all(checks.values()),checks
out={'status':'PASS','method':'ODE-derived finite admission, adaptive quadrature, scalar constrained minimum and independent frozen-lens integration','checks':checks,'max_relative_ODE_RAR_error':max(errors),'max_relative_minimizer_error':max(mins),'lensing_arcsec':angle,'scope':'Internal independent calculation, not an independent empirical discovery or external review'}
(P/'independent_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
