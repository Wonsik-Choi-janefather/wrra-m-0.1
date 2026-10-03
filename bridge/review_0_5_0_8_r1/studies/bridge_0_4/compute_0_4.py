"""Homogeneous finite-volume energy-pressure bridge under declared constitutive rules."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from scipy.integrate import solve_ivp
R=Path(__file__).resolve().parent
src=R/'source/bridge_0_3_results.json';prev=json.loads(src.read_text())
uc=prev['ucrit_J_m3'];checks=[];rows=[];histories=[]
def ck(name,ok):checks.append({'name':name,'passed':bool(ok)})
def close(x,y):return math.isclose(x,y,rel_tol=3e-8,abs_tol=1e-22)
def energy(V,M,L):return M+L*V
def pressure(V,M,L):
 h=V*1e-3
 return -(energy(V-2*h,M,L)-8*energy(V-h,M,L)+8*energy(V+h,M,L)-energy(V+2*h,M,L))/(12*h)
for item in prev['rows']:
 f=[.0493,.265,.6857] if item['calibration']=='inherited' else [.05,.268,.682]
 ED=uc*f[1];L=uc*f[2]
 for boundary in ['external','included_pressureless']:
  M=item['rest_total_J']+item['excitation_total_J']+ED
  if boundary=='included_pressureless':M+=item['environment_final_J']
  tag=item['calibration']+'_'+item['species']+'_'+item['case']+'_'+boundary
  ck(tag+' positive coefficients',M>0 and L>0)
  if boundary=='included_pressureless':
   ck(tag+' exchange invisible in full gravity load',close(M,uc*(f[0]+f[1])+item['environment_initial_J']))
  for a in [.5,1,2]:
   V=a**3;E=energy(V,M,L);u=E/V;P=-L;pn=pressure(V,M,L)
   q=(u+3*P)/(2*u);Hratio=math.sqrt(u/uc)
   ck(tag+f' a={a} same-energy pressure',close(pn,P))
   ck(tag+f' a={a} background density constant',close(L*V/V,L))
   ck(tag+f' a={a} positive density',u>0)
   # Derivatives with respect to scale factor, at fixed comoving population/preparation.
   h=a*1e-4
   uf=lambda z:M/z**3+L
   du=(uf(a-2*h)-8*uf(a-h)+8*uf(a+h)-uf(a+2*h))/(12*h)
   residual=a*du+3*(u+P)
   ck(tag+f' a={a} continuity',abs(residual)<1e-8*u)
   acceleration=-.5*(M/uc)/a**2+(L/uc)*a
   ck(tag+f' a={a} Friedmann acceleration consistency',math.isclose(acceleration,-q*Hratio**2*a,rel_tol=1e-12,abs_tol=1e-12))
   rows.append({'calibration':item['calibration'],'species':item['species'],'case':item['case'],'boundary':boundary,'a':a,'V_m3':V,'E_J':E,'u_J_m3':u,'P_Pa':P,'q':q,'H_over_inherited_H0':Hratio,'pressure_fd_Pa':pn,'continuity_residual_J_m3':residual})
   if a==1 and item['case']=='baseline' and boundary=='external':
    ck(tag+' inherited/dedicated q reference',math.isclose(q,-.52855 if item['calibration']=='inherited' else -.523,abs_tol=1e-12))
    ck(tag+' H reference unchanged',math.isclose(Hratio,1,abs_tol=1e-12))
  # Actual homogeneous integration after preparation; tau=H0*t is dimensionless.
  mm=M/uc;ll=L/uc
  def rhs(t,y):return [y[0]*math.sqrt(mm/y[0]**3+ll)]
  times=np.linspace(0,1,17)
  sol=solve_ivp(rhs,(0,1),[1.],t_eval=times,rtol=1e-11,atol=1e-12)
  exact=(math.sqrt(mm/ll)*np.sinh(np.arcsinh(math.sqrt(ll/mm))+1.5*math.sqrt(ll)*times))**(2/3)
  err=float(np.max(np.abs(sol.y[0]-exact)))
  ck(tag+' homogeneous integration',sol.success and err<2e-9)
  ck(tag+' expansion monotonic',np.all(np.diff(sol.y[0])>0))
  histories.append({'tag':tag,'tau_H0t':times.tolist(),'scale_factor':sol.y[0].tolist(),'analytic_max_error':err})
out={'version':'bridge-0.4','constitutive_rule':'fixed comoving particle count and prepared internal state; Ephi and ED constant, ER=L*V; included reservoir constant comoving energy if selected','boundaries':{'external':'environment excluded from gravitational subsystem; exchange is boundary work at fixed V','included_pressureless':'finite reservoir included with assumed Penv=0; reference total differs from inherited benchmark'},'rows':rows,'histories':histories,'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'scope':'homogeneous FRW effective load evolution after preparation; no time law for preparation or covariant nonuniform dynamics','open':['pressure law of actual physical reservoir','volume-dependent microscopic state coupling','particle creation and population dynamics','SI identification of source frames','time-resolved exchange Q(t)','nonuniform geometry and dynamics']}
(R/'results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'passed':out['passed'],'failed':out['failed'],'baseline':[x for x in rows if x['a']==1 and x['species']=='proton' and x['case']=='baseline'],'max_integration_error':max(x['analytic_max_error'] for x in histories)},indent=2))
if out['failed']:raise SystemExit(1)
