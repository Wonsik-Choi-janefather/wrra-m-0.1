"""Run each frozen module's main and separate verifier, with bounded concurrency.
All checks are internal calculations; the counters are not independent experiments.
"""
from pathlib import Path
import os,sys,subprocess,json,time,concurrent.futures,platform
P=Path(__file__).resolve().parent
MODS=['finite_scale_bridge_v0_1','source_carrier_action_v0_1','information_gravity_mechanism_v0_2','local_twist_load_bridge_v0_3','zeta_physical_readout_v0_1','zeta_symmetry_drive_v0_2','freedom_falsifiability_v0_1']
def run(name):
 root=P/'modules'/name;start=time.time();stages=[]
 for script in (['registry.py'] if (root/'registry.py').exists() else [])+['compute.py','verify.py']:
  env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='2';env['OMP_NUM_THREADS']='2'
  r=subprocess.run([sys.executable,str(root/script)],cwd=root,env=env,capture_output=True,text=True)
  (root/(script+'.recheck.log')).write_text(r.stdout+'\n'+r.stderr)
  stages.append({'script':script,'exit_code':r.returncode})
  if r.returncode:break
 main=json.loads((root/'results.json').read_text());verify=json.loads((root/'independent_verification.json').read_text())
 result={'module':name,'stages':stages,'all_processes_pass':all(s['exit_code']==0 for s in stages),'main_checks':len(main.get('checks',{})),'main_false_checks':[k for k,v in main.get('checks',{}).items() if not v],'separate_check_count':len(verify.get('checks',{})) or None,'separate_false_checks':[k for k,v in verify.get('checks',{}).items() if not v],'seconds':time.time()-start}
 print(json.dumps(result),flush=True);return result
if __name__=='__main__':
 import numpy,scipy,mpmath
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:rows=list(e.map(run,MODS))
 result={'date':'2026-10-21','environment':{'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,'mpmath':mpmath.__version__},'modules':rows,'all_pass':all(r['all_processes_pass'] and not r['main_false_checks'] and not r['separate_false_checks'] for r in rows),'scope':'Seven internal computational modules across five research tasks; no external review or new observational fit'}
 (P/'RECHECK_RESULTS.json').write_text(json.dumps(result,indent=2));assert result['all_pass']
