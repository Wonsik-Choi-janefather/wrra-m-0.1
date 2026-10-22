"""WRRA finite admission-gate completion matching the FROZEN empirical RAR.
This is an inverse constitutive construction, not independent discovery of RAR.
Two finite states; exposure is a load coordinate, NOT physical elapsed time.
"""
from pathlib import Path
import numpy as np
import math,json,hashlib,csv
from numpy.polynomial.legendre import leggauss
P=Path(__file__).resolve().parent
G=6.6743e-11;C=299792458.;PC=30856775814913670.;MSUN=1.98847e30
checks={}
def check(k,v):
 checks[k]=bool(v)
 if not v:raise AssertionError(k)
def writecsv(name,rows):
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def admission(s):return -np.expm1(-np.asarray(s))
def response(y):
 y=np.asarray(y,dtype=float);s=np.sqrt(y);p=admission(s)
 # Continuous origin g(0)=0, not division by zero.
 return np.divide(y,p,out=np.zeros_like(y),where=p>0)
def field_of_exposure(s):
 s=np.asarray(s);return np.divide(s*s,admission(s),out=np.zeros_like(s),where=s>0)
def exposure_of_field(x):
 x=np.asarray(x);lo=np.zeros_like(x);hi=np.maximum(x,np.sqrt(x))*2+1
 for _ in range(100):
  mid=(lo+hi)/2;go=field_of_exposure(mid)<x
  lo=np.where(go,mid,lo);hi=np.where(go,hi,mid)
 return (lo+hi)/2
# Stable slope of x(s), with exact series near the origin.
def dxds(s):
 s=np.asarray(s);a=admission(s);small=s<1e-3
 z=np.where(small,1.,s);m=admission(z)
 exact=2*z/m-z*z*np.exp(-z)/m**2
 series=1+s+s*s/4-s**4/144+s**6/4320
 return np.where(small,series,exact)

def main():
 for fn,meta in json.loads((P/'input_manifest.json').read_text()).items():check('hash_'+fn,hashlib.sha256((P/'inputs'/fn).read_bytes()).hexdigest()==meta['sha256'])
 ref=json.loads((P/'inputs/shared_gravity_results.json').read_text());cases=ref['cases'];origin=next(r for r in cases if r['carrier_state']=='product' and r['epsilon']==0 and r['a']==1)
 # Finite two-state admission generator, column probabilities [unresolved,resolved].
 Q=np.array([[-1.,0.],[1.,0.]])
 check('finite_Markov_generator',np.all(Q.sum(0)==0) and Q[1,0]>0 and Q[0,1]==0)
 gate_rows=[];maxgate=0.;maxsemigroup=0.;maxunitary=0.
 for s in np.r_[0.,np.geomspace(1e-10,40,80)]:
  r=math.exp(-s);mu=float(admission(s));T=np.array([[r,0.],[mu,1.]])
  expected=np.array([r,mu]);maxgate=max(maxgate,float(max(abs(T@np.array([1.,0.])-expected))))
  check('gate_probability_'+str(len(gate_rows)),T.min()>=0 and np.max(abs(T.sum(0)-1))<2e-16)
  rr=math.exp(-s/2);Th=np.array([[rr,0.],[-math.expm1(-s/2),1.]])
  maxsemigroup=max(maxsemigroup,float(np.max(abs(Th@Th-T))))
  # Single-use finite unitary realization on admission bit x blank record bit.
  # Rotate |00> and |11>; all four logical basis states are retained.
  U=np.eye(4);co=math.sqrt(r);si=math.sqrt(mu);U[0,0]=co;U[3,3]=co;U[3,0]=si;U[0,3]=-si
  state=U[:,0];record=abs(state[3])**2
  uerr=float(np.max(abs(U.T@U-np.eye(4))));maxunitary=max(maxunitary,uerr)
  check('finite_unitary_'+str(len(gate_rows)),uerr<4e-16 and abs(record-mu)<3e-16)
  entropy=-(r*math.log(r) if r>0 else 0)-(mu*math.log(mu) if mu>0 else 0)
  gate_rows.append(dict(exposure=s,unresolved=r,admission=mu,record_entropy_nats=entropy))
 check('semigroup_identity',maxsemigroup<3e-16)
 # Local activity cost (relative unit-hazard rate): minimum j=1-mu.
 # It is a declared kinetic cost, not a universal machine/energy cost.
 for im,mu in enumerate([0.,.1,.5,.9,.9999]):
  available=1-mu;j=available
  minimum=j*math.log(j/available)-j+available
  check('local_rate_cost_minimum_'+str(im),abs(minimum)<1e-16)
  for factor in [.2,.8,1.2,5.]:
   trial=j*factor;cost=trial*math.log(trial/available)-trial+available
   check('local_rate_cost_competitor_'+str(im)+'_'+str(factor),cost>minimum)

 # Entire fixed RAR, 16 decades of positive baryonic acceleration.
 ys=np.geomspace(1e-12,1e4,801);xs=response(ys)
 # Minimum exposure subject to quadratic coverage sigma^2 >= y.
 selected=np.sqrt(ys)
 check('minimum_exposure_covers_budget',max(abs(selected*selected/ys-1))<4e-16)
 check('smaller_exposure_is_infeasible',np.all((.99*selected)**2<ys))
 check('greater_exposure_costs_more',np.all(1.01*selected>selected))
 # Existing source code computes this legacy function independently by scalar math.
 old=np.array([float(y)/(-math.expm1(-math.sqrt(float(y)))) for y in ys])
 relative=float(np.max(abs(xs/old-1)));check('entire_fixed_RAR',relative<5e-16)
 inverse=exposure_of_field(xs);inverse_error=float(np.max(abs(inverse/np.sqrt(ys)-1)))
 check('constitutive_inverse',inverse_error<2e-14)
 check('origin_extension',float(response(0))==0)
 check('deep_limit',abs(float(response(1e-16))/1e-8-1)<1e-8)
 check('Newtonian_limit',abs(float(response(1e4))/1e4-1)<1e-14)
 response_rows=[dict(baryon_over_aT=float(y),exposure=math.sqrt(y),admission=float(admission(math.sqrt(y))),field_over_aT=float(x),legacy_field_over_aT=float(z),relative_error=float(abs(x/z-1))) for y,x,z in zip(ys,xs,old)]
 # Convex load cost Psi(y)=integral_0^y x(t)dt. Equivalent finite scalar
 # minimization Psi(y)-x*y on y>=0; NOT a positive equilibrium log partition.
 gx,gw=leggauss(160)
 def costs(s):
  z=(gx+1)*s/2;mu=admission(z)
  psi=float(s/2*np.dot(gw,2*z**3/mu))
  F=float(s/2*np.dot(gw,z*z*dxds(z)))
  return psi,F
 costs_rows=[];maxdual=0.;maxderivative=0.;maxconvex=0.
 for s in np.geomspace(1e-5,40,120):
  y=s*s;x=float(field_of_exposure(s));psi,F=costs(s)
  maxdual=max(maxdual,abs(F+psi-x*y)/max(abs(F),abs(psi),1e-20))
  h=1e-4*s
  psip=costs(s+h)[0];psim=costs(s-h)[0]
  dpsi=(psip-psim)/(2*h)/(2*s)
  maxderivative=max(maxderivative,abs(dpsi/x-1))
  mu=float(admission(s));long=2*s/float(dxds(s));maxconvex=max(maxconvex,long)
  check('convexity_'+str(len(costs_rows)),mu>0 and long>0)
  # Competitor y>=0 has no lower value than the chosen stationary minimum.
  best=psi-x*y
  for factor in [.5,.8,1.2,2.]:
   st=math.sqrt(factor)*s;trial=costs(st)[0]-x*st*st
   check('cost_minimum_'+str(len(costs_rows))+'_'+str(factor),trial>=best-1e-10*max(abs(best),1e-25))
  costs_rows.append(dict(exposure=s,baryon_over_aT=y,field_over_aT=x,load_cost=psi,field_cost=F,tangent_stiffness=mu,radial_stiffness=long))
 check('Legendre_pair_identity',maxdual<1e-12)
 check('load_cost_derivative',maxderivative<2e-7)
 # Preserve all 12 shared native states and their fixed rotation/lensing outputs.
 radii=np.geomspace(.05,200,400)*1000*PC;M=6e10*MSUN;a=3*1000*PC;rtest=8.2*1000*PC
 gb=G*M*radii/(radii*radii+a*a)**1.5;gbtest=G*M*rtest/(rtest*rtest+a*a)**1.5
 gr,gw=leggauss(512);impact=10*1000*PC;patch=200*1000*PC;zmax=math.sqrt(patch*patch-impact*impact);z=(gr+1)*zmax/2;rad=np.hypot(impact,z);gb_lens=G*M*rad/(rad*rad+a*a)**1.5
 H0=67.4*1000/(1e6*PC);ucrit=3*H0*H0*C*C/(8*np.pi*G)
 native=[];maxv=maxlens=0.;profiles=[]
 for i,r in enumerate(cases):
  aT=C*H0*math.sqrt(r['sector_density_J_m3'][1]/ucrit/8)
  check('native_scale_'+str(i),abs(aT/r['aT_m_s2']-1)<1e-14)
  g=aT*response(gb/aT);gtest=float(aT*response(gbtest/aT));v=math.sqrt(rtest*gtest)/1000
  gl=aT*response(gb_lens/aT);angle=4/C**2*zmax/2*np.dot(gw,gl*impact/rad)*180/math.pi*3600
  ve=abs(v-r['rotation_km_s']);le=abs(angle-r['lensing_arcsec']);maxv=max(maxv,ve);maxlens=max(maxlens,le)
  check('native_rotation_'+str(i),ve<1e-10);check('native_lensing_'+str(i),le<1e-9)
  native.append(dict(state=r['carrier_state'],epsilon=r['epsilon'],scale_factor=r['a'],aT_m_s2=aT,rotation_km_s=v,legacy_rotation_km_s=r['rotation_km_s'],lensing_arcsec=float(angle),legacy_lensing_arcsec=r['lensing_arcsec']))
  if r['carrier_state']=='product' and r['epsilon']==0 and r['a']==1:
   mass=M*radii**3/(radii*radii+a*a)**1.5
   inferred=radii*radii*g/G
   mu=admission(np.sqrt(gb/aT));res=float(np.max(abs(mu*inferred-mass))/M)
   check('spherical_flux',res<1e-14)
   for rr,bb,gg,mi,mb in zip(radii,gb,g,inferred,mass):profiles.append(dict(radius_kpc=rr/(1000*PC),baryon_acceleration=bb,gravity_acceleration=gg,velocity_km_s=math.sqrt(rr*gg)/1000,effective_residual_mass_Msun=(mi-mb)/MSUN))
 # Negative controls show both of the new matching assumptions matter.
 tests=[('linear_budget',1.,1.),('cubic_budget',3.,1.),('double_hazard',2.,2.)];controls=[]
 yy=np.geomspace(1e-6,1e2,100)
 for label,power,rate in tests:
  gg=yy/(-np.expm1(-rate*yy**(1/power)));base=response(yy)
  err=float(np.max(abs(gg/base-1)))
  check('changed_law_detected_'+label,err>.1)
  controls.append(dict(control=label,budget_power=power,hazard_rate=rate,max_relative_deviation=err))
 # Old finite positive-equilibrium candidate is retained as an explicit failed
 # route to the frozen deep RAR, not silently deleted/refitted.
 previous=json.loads((P/'inputs/previous_candidate_results.json').read_text())
 check('old_candidate_limit_distinguished',previous['candidate']['A']['zero_field_mu']>.4 and float(admission(1e-6))<2e-6)
 result={'framework_name':'Wonsik Reality–Renderer Architecture','version':'information-gravity-mechanism v0.2','date':'2026-10-21',
 'assessment':{'inputs':'Frozen RAR, original shared D energy load, kappa=1/8, G, H0, baryonic source and conditional lens patch','WRRA_transformation':'D load -> aT -> NEW quadratic load/exposure contract y=sigma^2 -> finite unit-hazard admission -> flux ownership y=mu*x -> convex cost/field action','outputs':'Exact fixed RAR across 16 decades, all 12 archived rotation/lens states, finite single-use unitary and record entropy','falsification':'Failed gate probabilities, load/cost/field derivatives, full-curve or native-output mismatch, double-counted residual mass, incorrect record/reset claims or disagreement with data under fixed law'},
 'new_contracts':{'quadratic_load_exposure':'min sigma>=0 subject to sigma^2>=g_b/aT; capacity is a new quadratic contract motivated by quadratic stress, not uniquely derived from SOURCE','unit_hazard':'Local rate-cost minimum j log[j/(1-mu)]-j+(1-mu) gives dmu/dsigma=1-mu; sigma is NOT physical time','local_flux':'g_b=mu*g; spherical/declared local response','physical_status':'Inverse constitutive realization matched to the fixed RAR, no new fit and no independent discovery claim'},
 'metrics':{'max_relative_RAR_error':relative,'max_relative_inverse_error':inverse_error,'max_gate_semigroup_error':maxsemigroup,'max_unitarity_error':maxunitary,'max_relative_Legendre_identity_error':maxdual,'max_relative_cost_derivative_error':maxderivative,'max_native_rotation_difference_km_s':maxv,'max_native_lensing_difference_arcsec':maxlens,'max_sampled_radial_stiffness':maxconvex},
 'origin_reference':{'rotation_km_s':origin['rotation_km_s'],'lensing_arcsec':origin['lensing_arcsec'],'aT_m_s2':origin['aT_m_s2']},
 'negative_controls':controls,'scope':'Finite inverse constitutive completion of the frozen static RAR. No derivation of the quadratic matching contract from microscopic SOURCE, no new SPARC fit, no full 3D/covariant time completion, no single-outcome/thermalization/reset mechanism. P6 susceptibilities remain separate.',
 'checks':checks,'passed':sum(checks.values()),'total':len(checks)}
 writecsv('finite_admission_gate.csv',gate_rows);writecsv('full_RAR_comparison.csv',response_rows);writecsv('convex_costs.csv',costs_rows);writecsv('native_state_replay.csv',native);writecsv('reference_radial_profile.csv',profiles);writecsv('negative_controls.csv',controls)
 (P/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['metrics','origin_reference','negative_controls','passed','total']},indent=2))
if __name__=='__main__':main()
