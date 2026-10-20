"""Independent release checks beyond the frozen 472 checks.

The clock-rescaled tangent uses u=(1+xi)t, fixed event positions and
w'=Jw-f, w+=DR w-. The final common-time derivative is z=w+t_end*f.
This removes event-time saltation from the integration and cross-checks it.
"""
from pathlib import Path
import json,math,hashlib
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy import constants as sc
from thermal_history import EOS,hubble,NUCOEF,SECONDS
from packet_emission import BETA,schedule,Model
P=Path(__file__).resolve().parent
checks={}
def check(name,ok):
 checks[name]=bool(ok)
 if not ok:raise AssertionError(name)

def rescaled_tangent():
 e=EOS();r=json.loads((P/'results/event_tangent.json').read_text())['base']
 Ti=r['Tinitial_MeV'];Tnu=(2/5.5)**(1/3)*(e.gs(Ti)/2)**(1/3)*Ti
 rhoi=(e(Ti)[0]+NUCOEF*Tnu**4)/(1-BETA);rn0=NUCOEF*Tnu**4/rhoi
 C=BETA;q=BETA/256;eps=.01;t=0.;y=np.array([0.,math.log(Ti),0.]);w=np.zeros(3);jerrs=[]
 def flow(y,CC):
  N,L,m=y;T=np.exp(L);re,pe,der=e(T)/rhoi
  rn=rn0*np.exp(-4*N);rx=CC*np.exp(-4*N);rm=m*np.exp(-3*N);rho=re+rn+rx+rm
  H=hubble(float(rho*rhoi))*SECONDS
  return np.array([H,-3*H*(re+pe)/(T*der),0.])
 def jac(y,CC):
  N,L,m=y;T=np.exp(L);re,pe,der=e(T)/rhoi
  d1=np.array([re,pe,der])*np.array([s(L,1) for s in e.spl])
  rn=rn0*np.exp(-4*N);rx=CC*np.exp(-4*N);rm=m*np.exp(-3*N);rho=re+rn+rx+rm
  H=flow(y,CC)[0];hgrad=H/(2*rho)*np.array([-4*(rn+rx)-3*rm,d1[0],np.exp(-3*N)])
  A=(re+pe)/(T*der);J=np.zeros((3,3));J[0]=hgrad;J[1]=-3*A*hgrad
  J[1,1]-=3*H*A*((d1[0]+d1[1])/(re+pe)-1-d1[2]/der)
  return J
 times=schedule(Model())[0]
 for j,target in enumerate([*times,5000.]):
  if j in [0,64,128]:
   J=jac(y,C);numeric=np.zeros_like(J)
   # Five-point derivative; normalize the mass coordinate to rho_i.
   for k,h in enumerate([1e-4,1e-4,1e-6]):
    v=np.zeros(3);v[k]=h
    numeric[:,k]=(-flow(y+2*v,C)+8*flow(y+v,C)-8*flow(y-v,C)+flow(y-2*v,C))/(12*h)
   jerrs.append(float(np.max(abs(J-numeric))/max(np.max(abs(J)),1e-100)))
  def rhs(tt,v):
   f=flow(v[:3],C);return np.r_[f,jac(v[:3],C)@v[3:]-f]
  s=solve_ivp(rhs,(t,float(target)),np.r_[y,w],method='DOP853',rtol=2e-13,
   atol=np.array([2e-16,2e-16,2e-22]*2),max_step=max(.01,(target-t)/40))
  assert s.success
  y=s.y[:3,-1];w=s.y[3:,-1];t=float(target)
  if j==len(times):break
  N,L,m=y;T=np.exp(L);heat=eps*q*np.exp(-4*N)
  Ta=brentq(lambda u:(e(u)[0]-e(T)[0])/rhoi-heat,T,T*(1+1e-4),xtol=5e-15)
  dm=(1-eps)*q*np.exp(-N);DR=np.eye(3)
  db=e(T)[0]*e.spl[0](L,1)/rhoi;da=e(Ta)[0]*e.spl[0](math.log(Ta),1)/rhoi
  DR[2,0]=-dm;DR[1,0]=-4*heat/da;DR[1,1]=db/da
  y=np.array([N,math.log(Ta),m+dm]);w=DR@w;C=(255-j)*q
 z=w+5000.*flow(y,C);N,L,m=y;re,pe,_=e(math.exp(L));S=z[2]/m-3*z[0]-re*e.spl[0](L,1)*z[1]/(re+pe)
 return dict(S_response=float(S),tangent=z.tolist(),max_independent_jacobian_error=max(jerrs),
  clock_formulation='u=(1+xi)t; fixed events; wprime=Jw-f; final z=w+t*f')

def main():
 r=json.loads((P/'results/event_tangent.json').read_text());b=r['base'];alt=rescaled_tangent()
 check('fixed_clock_independent_entropy_tangent',abs(alt['S_response']/b['S_m_em_response']-1)<1e-8)
 check('flow_jacobian_five_point_crosscheck',alt['max_independent_jacobian_error']<1e-8)
 states=json.loads((P/'inputs/matching_states.json').read_text());rows=json.loads((P/'results/cdm_comoving_64_states.json').read_text())
 audit=json.loads((P/'inputs/v04_audit.json').read_text());Kscale=audit['inputs']['K_per_Mpc_inverse']
 phis=[];naive=[];rv=[];relv=[];f1=[]
 for entry,row,d in zip(states,rows,audit['physical_modes']):
  s=entry['matched_state'];c=row['adapted'];K=entry['K_initial'];a=s['a_relative'];hc=a*d['H']
  an=s['shear_scaled']/2
  bn=c['h_plus_6eta_prime']/(2*K*K)
  oldphi=s['eta']-hc*an;newphi=c['eta']-hc*bn
  naivephi=c['eta']-hc*(c['h_prime']+6*c['eta_prime'])/(2*K*K)
  naive.append(abs(naivephi-oldphi)/max(abs(oldphi),1e-100))
  phis.append(abs(newphi-oldphi)/max(abs(oldphi),1e-100))
  rv.append(abs((c['eta']+hc*c['theta_m']/K**2)-(s['eta']+hc*s['theta_m']/K**2)))
  relv.append(abs((c['theta_nu']-c['theta_gamma'])-(s['theta_nu']-s['theta_gamma'])))
  f1.append(abs(c['F_nu'][1]-4*c['theta_nu']/(3*K)))
 check('Bardeen_Phi_stable_combination_invariant_all64',max(phis)<1e-9)
 check('naive_derivative_reconstruction_error_detected',max(naive)>.01)
 check('comoving_curvature_invariant_all64',max(rv)<1e-16)
 check('relative_species_velocity_invariant_all64',max(relv)<1e-24)
 check('neutrino_dipole_normalization_all64',max(f1)<1e-25)
 # SI reconstruction independent of MeV^4 conversion and the U100 conversion used in run().
 H100=100000/(sc.parsec*1e6);rho_initial_mass=3*(1/SECONDS)**2/(8*math.pi*sc.G)
 rho_critical_h2=3*H100**2/(8*math.pi*sc.G)
 v6=json.loads((P/'inputs/v06_thermal.json').read_text())
 independent=rho_initial_mass*v6['M_over_rhoi']*v6['a_initial_derived']**3/rho_critical_h2
 check('physical_density_independent_SI_conversion',abs(independent/b['omch2_from_packets']-1)<1e-8)
 frozen=json.loads((P/'SHA256SUMS.json').read_text())
 check('all_frozen_files_SHA256_exact',all(hashlib.sha256((P/k).read_bytes()).hexdigest()==v for k,v in frozen.items()))
 gate=json.loads((P/'results/full_state_gate.json').read_text())
 check('publication_keeps_full_state_incomplete',not gate['full_state_injected'] and not gate['new_CMB_spectrum'] and not gate['new_lensing_likelihood'])
 result=dict(additional_checks_passed=sum(checks.values()),checks=checks,independent_rescaled_clock=alt,
  relative_S_difference=abs(alt['S_response']/b['S_m_em_response']-1),Bardeen_Phi_max_relative_difference=max(phis),
  independent_SI_omch2=independent,frozen_files_verified=len(frozen)+1,scientific_correction_required=True,
  correction='Keep the small hprime+6etaprime combination directly; do not reconstruct it from separately rounded derivatives.',
  naive_derivative_Bardeen_Phi_max_relative_error=max(naive),
  release_scope='v0.7-dev partial full-state junction development; no new CMB/lensing result')
 (P/'REVALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
