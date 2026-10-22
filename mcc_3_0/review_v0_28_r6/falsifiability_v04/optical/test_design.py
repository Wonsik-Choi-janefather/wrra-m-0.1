from pathlib import Path
import json,subprocess,sys,tempfile
import numpy as np
from design import ROOT,profile,visibility
cfg=json.loads((ROOT/'design.json').read_text());checks={};runs=[]
def check(name,value):
 checks[name]=bool(value)
 if not value:raise AssertionError(name)
f=profile();check('128_centered_source_states',len(f)==128 and abs(f.mean())<1e-22)
for nm in [532,1064,1550]:
 wave=nm*1e-9; check(f'wavelength_scaling_{nm}',abs(visibility(20*wave/1064e-9,wave)-visibility(20,1064e-9))<1e-12)
check('zero_exposure_unit_visibility',visibility(0,1064e-9)==1)
for p in cfg['points']:
 wave=p['wavelength_m']; nm=str(round(wave*1e9));d=cfg['exposure_error_m_for_visibility_0_002'][nm]
 check(f"exposure_budget_{nm}_{p['role']}",abs(visibility(p['L_m']+d,wave)-visibility(p['L_m'],wave))<=.002+1e-12)
check('phase_budget',abs(np.exp(-cfg['phase_noise_sigma_rad_max_for_0_002_fractional_loss']**2/2)-.998)<1e-14)
check('shot_noise_bound',np.sqrt(2/(.9**2*cfg['detected_trials_each_signal_or_reference_block']))<=.005)
for name,expected in [('synthetic_nominal',0),('synthetic_no_loss',1),('synthetic_missing_revival',1)]:
 r=subprocess.run([sys.executable,str(ROOT/'verify_observations.py'),str(ROOT/(name+'.json'))],capture_output=True,text=True)
 runs.append({'case':name,'exit_code':r.returncode,'result':json.loads(r.stdout)})
 check(name+'_expected_exit',r.returncode==expected)
with tempfile.TemporaryDirectory() as tmp:
 original=json.loads((ROOT/'synthetic_nominal.json').read_text())
 for name in ['hash_change','order_change','covariance_invalid']:
  data=json.loads(json.dumps(original))
  if name=='hash_change':data['source_profile_sha256']='0'*64
  if name=='order_change':data['point_order'].reverse()
  if name=='covariance_invalid':data['covariance'][0][0]=-1
  p=Path(tmp)/(name+'.json');p.write_text(json.dumps(data))
  r=subprocess.run([sys.executable,str(ROOT/'verify_observations.py'),str(p)],capture_output=True,text=True)
  runs.append({'case':name,'exit_code':r.returncode,'result':json.loads(r.stdout)})
  check(name+'_invalid_input_exit',r.returncode==2)
result={'passed':sum(checks.values()),'total':len(checks),'checks':checks,'runs':runs,'observed_experimental_data_used':False}
(ROOT/'test_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
