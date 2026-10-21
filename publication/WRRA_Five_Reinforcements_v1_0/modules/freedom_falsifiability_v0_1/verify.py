from pathlib import Path
import json,numpy as np
from scipy.integrate import quad
P=Path(__file__).resolve().parent;r=json.loads((P/'results.json').read_text());checks={};metrics={}
def ck(n,b):
 checks[n]=bool(b)
 if not b:raise AssertionError(n)
# Analytic RAR derivative: d log g / d log a_eff = x/[2(expm1(x))].
a=r['gravity']['reference_a_eff_m_s2'];g=np.geomspace(1e-14,1e-8,201);x=np.sqrt(g/a)
s=x/(2*np.expm1(x));v=np.array([1,.5,.5,-2]);analytic=s[:,None]*v
stored=np.load(P/'RAR_identifiability.npz');err=float(np.max(abs(stored['jacobian']-analytic)))
ck('analytic_sensitivity',err<2e-9);ck('analytic_rank_one',np.linalg.matrix_rank(analytic)==1)
for i,n in enumerate(stored['null_vectors']):ck('analytic_null_'+str(i),np.max(abs(analytic@n))<1e-14)
# Independent adaptive lens quadrature, dimensional constants frozen as before.
G=6.6743e-11;c=299792458.;pc=30856775814913670.;ms=1.98847e30;b=1e4*pc;R=2e5*pc;scale=3e3*pc;M=6e10*ms;zmax=np.sqrt(R*R-b*b)
def integrand(t):
 rr=np.hypot(b,zmax*t);gb=G*M*rr/(rr*rr+scale*scale)**1.5
 return gb/(-np.expm1(-np.sqrt(gb/a)))*b/rr*zmax
lens=4/c**2*quad(integrand,0,1,epsabs=1e-7,epsrel=1e-12)[0]*180/np.pi*3600
ck('adaptive_lens',abs(lens-r['gravity']['reference_lens_arcsec'])<1e-11)
# Count-only information after profiling common efficiency equals conditional-binomial form.
for prep,z in r['zeta_constraints'].items():
 b=np.array(z['incoherent_vector']);d=np.array(z['coherent_vector_P_B_Edimensionless'])-b
 eta=.6;eps=.8;y=b+eta*d;q=y[1]/y[0];dq=(d[1]*y[0]-d[0]*y[1])/y[0]**2
 N=q*(1-q)/(.1**2*dq*dq*eps*y[0]);target=z['ideal_count_only_trials_for_eta_std_0p1_at_eta_0p6_eff_0p8']
 ck(prep+'_profile_information',abs(N/target-1)<1e-9)
 # Direct determinant constraint on 17 noise values and arbitrary common efficiencies.
 for i,t in enumerate(np.linspace(0,1,17)):
  y=(.4+.3*t)*(b+t*d);det=np.linalg.det(np.column_stack([b,d,y]))
  ck(prep+'_det_'+str(i),abs(det)<1e-18)
  q=y[1]/y[0];en=y[2]/y[0]*444.3469133712202
  ck(prep+'_conditional_line_'+str(i),abs(en-z['conditional_energy_intercept_keV']-z['conditional_energy_slope_keV']*q)<1e-9)
reg=json.loads((P/'parameter_registry.json').read_text());names={z['name'] for z in reg['entries']}
for item in reg['entries']:
 for dep in item['depends_on'].split(','):
  if dep:ck('dependency_'+item['name']+'_'+dep,dep in names)
ck('no_global_fit_count_claim',reg['scope'].startswith('Selected'))
metrics={'analytic_J_max_error':err,'adaptive_lens_arcsec':lens,'lens_difference_arcsec':abs(lens-r['gravity']['reference_lens_arcsec'])}
(P/'independent_verification.json').write_text(json.dumps({'checks':checks,'metrics':metrics,'all_checks_pass':all(checks.values())},indent=2));print(json.dumps({'checks':len(checks),'metrics':metrics},indent=2))
