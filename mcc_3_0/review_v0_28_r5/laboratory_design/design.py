"""Measurement design for the frozen Chapter 122 branch; synthetic data only."""
from pathlib import Path
import hashlib,json,math
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import chi2
ROOT=Path(__file__).resolve().parent
MODEL=ROOT/'optical_model_v1_0'
def profile():
 a=np.load(MODEL/'inputs/finite_preparation.npz')['dimensionless_fluctuation'][1]
 return a-a.mean()
def visibility(L,wavelength):
 return float(abs(np.exp(2j*np.pi*L*profile()/wavelength).mean()))
def main():
 f=profile(); out=json.loads((MODEL/'results/results.json').read_text()); points=[]
 for row in out['outputs']['fixed_predictions']:
  wave=row['wavelength_nm']*1e-9
  for role,key in [('threshold','first_visibility_threshold_m'),('minimum','first_minimum_exposure_m'),('revival','first_revival_exposure_m')]:
   L=row[key];points.append(dict(wavelength_m=wave,role=role,L_m=L,visibility=visibility(L,wave)))
 # Sufficient global Lipschitz bound |d|mean exp(i a L f)||/dL| <= a mean|f|.
 slopes={str(nm):2*np.pi/(nm*1e-9)*float(abs(f).mean()) for nm in [532,1064,1550]}
 budget=.002; phase=math.sqrt(-2*math.log(1-budget)); D=40.; wave=1064e-9; c=299792458.
 C=.008**2*np.eye(9)+.006**2*np.ones((9,9));mu=np.array([x['visibility'] for x in points])
 cfg={'version':'lab_design_v0.1','source_profile_sha256':hashlib.sha256((MODEL/'inputs/finite_preparation.npz').read_bytes()).hexdigest(),'points':points,'covariance':C.tolist(),'test_alpha':.001,'test_dof':9,'Q_critical':float(chi2.isf(.001,9)),'sigma_visibility_absolute':.01,'lipschitz_per_m':slopes,'exposure_error_m_for_visibility_0_002':{k:budget/v for k,v in slopes.items()},'phase_noise_sigma_rad_max_for_0_002_fractional_loss':phase,'physical_OPD_m_assumed':D,'frequency_rms_Hz_all_phase_budget':phase*c/(2*np.pi*D),'frequency_rms_Hz_half_phase_variance':phase*c/(2*np.pi*D*math.sqrt(2)),'OPD_rms_m_half_phase_variance':phase*wave/(2*np.pi*math.sqrt(2)),'detected_trials_each_signal_or_reference_block':math.ceil(2/(.9**2*.005**2)),'shot_bound_assumptions':'Independent detected trials; calibrated extrema phases; balanced two-phase sampling; reference visibility >=0.9; separate equal-size signal/reference blocks. No detection-rate or duration inferred.','shutter_inverse_Hz':1/out['validation_inputs']['shutter_dt_s'],'scope':'Conditional optical branch and synthetic design; differential natural coupling not established; static visibility cannot measure shutter interval.'}
 (ROOT/'design.json').write_text(json.dumps(cfg,indent=2))
 rng=np.random.default_rng(1222026);nominal=mu+np.linalg.cholesky(C)@rng.standard_normal(9)
 cases={'synthetic_nominal':nominal,'synthetic_no_loss':np.ones(9),'synthetic_missing_revival':mu.copy()}
 cases['synthetic_missing_revival'][2::3]=mu[1::3]
 for name,y in cases.items():
  (ROOT/(name+'.json')).write_text(json.dumps({'synthetic':True,'source_profile_sha256':cfg['source_profile_sha256'],'observations':y.tolist(),'covariance':C.tolist(),'point_order':[[p['wavelength_m'],p['L_m']] for p in points]},indent=2))
 print(json.dumps({k:v for k,v in cfg.items() if k not in ['covariance','points']},indent=2))
if __name__=='__main__':main()
