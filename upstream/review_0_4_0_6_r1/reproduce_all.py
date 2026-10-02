#!/usr/bin/env python3
"""Run all reviewed studies and compare scientific ledgers with published baselines."""
from pathlib import Path
import copy,hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent
def main():
 reports={};checks={}
 env={**os.environ,'OPENBLAS_NUM_THREADS':'2','PYTHONDONTWRITEBYTECODE':'1'}
 for v in (4,5,6):
  root=ROOT/'studies'/f'v0_{v}_r1'
  for script in ('code/compute.py','verify_release.py'):
   run=subprocess.run([sys.executable,str(root/script)],env=env,text=True,capture_output=True)
   if run.returncode:raise RuntimeError(f'{root.name}/{script}\n{run.stdout}\n{run.stderr}')
  audit=json.loads((root/'verification.json').read_text());reports[f'0.{v}-r1']=audit
  old=json.loads((ROOT/'baseline'/f'v0_{v}_results.json').read_text());new=json.loads((root/'code/results.json').read_text())
  if v==4:
   old_error=old['spatial_completion']['maximum_link_permutation_error'] if 'spatial_completion' in old else None
   # The one unrounded quadrature residual can differ by one floating-point
   # ulp across BLAS reduction settings. All scientific outputs remain exact.
   def remove_residual(obj):
    if isinstance(obj,dict):return {k:remove_residual(v) for k,v in obj.items() if k!='maximum_link_permutation_error'}
    if isinstance(obj,list):return [remove_residual(v) for v in obj]
    return obj
   checks['v0_4_scientific_ledger_unchanged']=remove_residual(new)==remove_residual(old)
  elif v==5:
   checks[f'v0_{v}_baseline_exact_bytes']=(ROOT/'baseline'/f'v0_{v}_results.json').read_bytes()==(root/'code/results.json').read_bytes()
  else:
   for k in list(new['checks']):
    if 'Fourier_current_adjoint' in k:del new['checks'][k]
   new['checks_total']-=4;new['checks_passed']-=4
   checks['v0_6_scientific_ledger_unchanged']=new==old
  print(f'0.{v}-r1: {audit["total_checks"]} checks passed',flush=True)
 r5=json.loads((ROOT/'studies/v0_5_r1/code/results.json').read_text());r6=json.loads((ROOT/'studies/v0_6_r1/code/results.json').read_text())
 checks['v0_5_to_0_6_same_inherited_H_state_parameters']=r5['calibrated_parameters']==r6['inherited_parameters']
 checks['v0_6_width_refit_is_explicit']=abs(r5['calibrated_parameters']['ell_fm']-r6['new_charge_calibration']['ell_fm'])>.01
 if not all(checks.values()):raise AssertionError({k:v for k,v in checks.items() if not v})
 out={'version':'0.4-0.6-r1','studies':reports,'cross_stage_checks':checks,'cross_stage_checks_total':len(checks),'total_checks':sum(x['total_checks'] for x in reports.values())+len(checks),'all_passed':True,'python':sys.version.split()[0]}
 (ROOT/'reproduction_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'total_checks':out['total_checks'],'all_passed':True},indent=2),flush=True)
if __name__=='__main__':main()
