"""WRRA item 5: scoped freedom audit and executable joint-output constraints.
No observational fit; generated diagnostics are explicitly synthetic.
"""
from pathlib import Path
import numpy as np,json,math,hashlib,csv
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq
P=Path(__file__).resolve().parent;checks={}
G=6.6743e-11;C=299792458.;PC=30856775814913670.;MS=1.98847e30
def ck(n,b):
 checks[n]=bool(b)
 if not b:raise AssertionError(n)
def write(name,rows):
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
def main():
 for fn,m in json.loads((P/'input_manifest.json').read_text()).items():ck('hash_'+fn,hashlib.sha256((P/'inputs'/fn).read_bytes()).hexdigest()==m['sha256'])
 gr=json.loads((P/'inputs/shared_gravity_results.json').read_text());ref=next(r for r in gr['cases'] if r['carrier_state']=='product' and r['epsilon']==0 and r['a']==1)
 a0=ref['aT_m_s2'];uD=ref['sector_density_J_m3'][1];H0=67.4*1000/(1e6*PC);uc=3*H0**2*C**2/(8*np.pi*G);fD=uD/uc;kappa=1/8
 ck('fraction_and_SI_parameterization',abs(C*H0*np.sqrt(kappa*fD)/a0-1)<2e-15)
 ck('H0_cancels_at_fixed_SI_density',abs(np.sqrt(8*np.pi*G*kappa*uD/3)/a0-1)<2e-15)
 # Four candidate log parameters, one effective acceleration combination.
 v=np.array([1.,.5,.5,-2.]);gbar=np.geomspace(1e-14,1e-8,201)
 def ae(q):return a0*np.exp(v@q)
 def logr(q):
  y=gbar/ae(q);return np.log(gbar)-np.log(-np.expm1(-np.sqrt(y)))
 step=1e-5;J=np.column_stack([(logr(np.eye(4)[i]*step)-logr(-np.eye(4)[i]*step))/(2*step) for i in range(4)])
 sval=np.linalg.svd(J,compute_uv=False);rank=int(np.sum(sval>sval[0]*1e-7));ck('RAR_log_sensitivity_rank_one',rank==1)
 nulls=np.array([[-.5,1,0,0],[-.5,0,1,0],[2,0,0,1]])
 for j,n in enumerate(nulls):ck('exact_null_direction_'+str(j),np.max(abs(logr(n*.4)-logr(np.zeros(4))))<2e-14)
 np.savez_compressed(P/'RAR_identifiability.npz',jacobian=J,singular_values=sval,null_vectors=nulls,log_parameter_combination=v)
 # One a_eff must determine BOTH existing rotation and conditional lensing.
 x,w=leggauss(512);mass=6e10*MS;scale=3000*PC;r=8200*PC;b=10000*PC;R=200000*PC
 zmax=np.sqrt(R*R-b*b);z=(x+1)*zmax/2;rr=np.hypot(z,b);gb=G*mass*rr/(rr*rr+scale*scale)**1.5;gb0=G*mass*r/(r*r+scale*scale)**1.5
 def obs(a):
  vel=np.sqrt(r*gb0/(-np.expm1(-np.sqrt(gb0/a))))/1000
  lens=4/C**2*zmax/2*np.dot(w,gb/(-np.expm1(-np.sqrt(gb/a)))*b/rr)*180/np.pi*3600
  return float(vel),float(lens)
 v0,l0=obs(a0);ck('old_rotation',abs(v0-ref['rotation_km_s'])<1e-10);ck('old_lens',abs(l0-ref['lensing_arcsec'])<1e-10)
 curve=[]
 for t in np.linspace(-1,1,81):
  aa=a0*np.exp(t);vv,ll=obs(aa);curve.append({'a_eff_m_s2':aa,'rotation_km_s':vv,'conditional_lens_arcsec':ll})
 write('shared_gravity_curve.csv',curve)
 # An exactly fixed rotation plus a 2% lens-only perturbation cannot share a_eff.
 target_v,target_l=v0,l0*1.02
 invv=brentq(lambda t:obs(a0*np.exp(t))[0]-target_v,-2,2,xtol=1e-13)
 invl=brentq(lambda t:obs(a0*np.exp(t))[1]-target_l,-2,2,xtol=1e-13)
 ck('injected_lens_mismatch_detected',abs(invl-invv)>1e-3)
 # Zeta instrument: common unknown detection efficiency and one dephasing eta.
 zr=json.loads((P/'inputs/zeta_readout_results.json').read_text());zd=json.loads((P/'inputs/zeta_drive_results.json').read_text());unit=zr['constants']['energy_unit_keV']
 rows=[];zsummary={}
 for prep in ['uniform','inherited_alpha']:
  old=next(t for t in zr['rows'] if t['case']=='zeta' and t['preparation']==prep);su=zd['summaries'][prep]
  coherent=np.array([old['pass_probability'],old['band_detect_probability'],old['pass_energy_weighted_keV']/unit])
  incoherent=np.array([1/70,su['fully_dephased_band_pass'],old['all_ports_mean_keV']/70/unit])
  d=coherent-incoherent;normal=np.cross(incoherent,d);normal/=np.linalg.norm(normal)
  if normal[2]<0:normal=-normal
  matrix=np.column_stack([incoherent,d]);sv=np.linalg.svd(matrix,compute_uv=False)
  ck(prep+'_two_effective_dimensions',sv[1]>1e-10)
  A=-normal[0]/normal[2]*unit;B=-normal[1]/normal[2]*unit
  # Econditional_keV = A + B*(band_count/pass_count), independent of efficiency.
  maxerr=0.
  for eta in np.linspace(0,1,101):
   y=incoherent+eta*d;ratio=y[1]/y[0];en=y[2]/y[0]*unit;err=abs(en-A-B*ratio);maxerr=max(maxerr,err)
   rows.append({'preparation':prep,'coherence_eta':eta,'band_fraction_of_selected':ratio,'conditional_energy_keV':en,'linear_constraint_error_keV':err})
  ck(prep+'_joint_output_line',maxerr<1e-9)
  eps=.8;eta=.6;y=eps*(incoherent+eta*d)
  ab=np.linalg.solve(matrix[:2],y[:2]);recover_eps=float(ab[0]);recover_eta=float(ab[1]/ab[0])
  pred=matrix[2]@ab;err=abs(pred-y[2]);ck(prep+'_synthetic_recovery',max(abs(recover_eps-eps),abs(recover_eta-eta))<1e-10)
  damaged=y.copy();damaged[2]*=1.01
  damaged_err=abs(float(normal@damaged));ck(prep+'_injected_energy_mismatch',damaged_err>1e-8)
  vv=incoherent+eta*d
  # Ideal multinomial count information for outcomes band / selected-high / rest.
  probabilities=np.array([eps*vv[1],eps*(vv[0]-vv[1]),1-eps*vv[0]])
  derivatives=np.array([[vv[1],eps*d[1]],[vv[0]-vv[1],eps*(d[0]-d[1])],[-vv[0],-eps*d[0]]])
  fisher=derivatives.T@(derivatives/probabilities[:,None]);cov=np.linalg.inv(fisher)
  trials=float(cov[1,1]/.1**2)
  ck(prep+'_count_Fisher_positive',np.linalg.eigvalsh(fisher)[0]>0)
  zsummary[prep]={'coherent_vector_P_B_Edimensionless':coherent.tolist(),'incoherent_vector':incoherent.tolist(),
   'plane_normal':normal.tolist(),'conditional_energy_intercept_keV':float(A),'conditional_energy_slope_keV':float(B),
   'sensitivity_singular_values':sv.tolist(),'sensitivity_condition_number':float(sv[0]/sv[1]),
   'constraint_max_error_keV':maxerr,'synthetic_eta':eta,'synthetic_efficiency':eps,
   'recovered_eta':recover_eta,'recovered_efficiency':recover_eps,'third_output_prediction_error':err,
   'ideal_count_only_trials_for_eta_std_0p1_at_eta_0p6_eff_0p8':trials,
   'count_Fisher_per_trial':fisher.tolist(),
   'one_percent_energy_perturbation_plane_error':damaged_err}
 write('zeta_joint_constraint.csv',rows)
 # State-space/fit freedoms are distinct. CP^(C-1) has real dimension 2C-2.
 counts={'normalized_address_targets':2,'normalized_energy_targets':2,'H0_reference_anchor':1,
  'reference_chain_anchor_dimension':5,'alpha_h_calibration_coordinates':2,
  'eta_s_derived_components':3,'new_observational_fits_in_this_package':0,
  'general_70_branch_pure_combiner_if_released':138,'general_128_carrier_pure_state_if_released':254,
  'general_128_carrier_density_if_released':16383,'RAR_response_rank_for_four_released_parameters':rank,
  'zeta_efficiency_and_noise_effective_dimension':2}
 ck('simplex_dimension',3-1==2);ck('pure_combiner_dimension',2*70-2==138)
 ck('pure_state_dimension',2*128-2==254);ck('mixed_state_dimension',128**2-1==16383)
 result={'architecture':'Wonsik Reality-Renderer Architecture','counts':counts,
  'gravity':{'reference_a_eff_m_s2':a0,'reference_rotation_km_s':v0,'reference_lens_arcsec':l0,
   'parameter_order':['log_H0','log_kappa','log_fD','log_hazard'],'effective_log_coefficients':v.tolist(),
   'singular_values':sval.tolist(),'rank_threshold_relative':1e-7,
   'synthetic_rotation_inferred_log_a_ratio':invv,'synthetic_lens_inferred_log_a_ratio':invl,
   'injected_lens_change_fraction':.02,'scope':'fixed Plummer source, no gravitational slip, same finite lens patch'},
  'zeta_constraints':zsummary,'checks':checks,'all_checks_pass':all(checks.values()),
  'scope':'Scoped audit of book reference chain, shared gravity and finite zeta instrument; not a full-universe parameter census or matched likelihood ranking against LCDM. All new generated calibration/perturbation examples are synthetic.'}
 (P/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps({'checks':len(checks),'counts':counts,'gravity':result['gravity'],'zeta':zsummary},indent=2))
if __name__=='__main__':main()
