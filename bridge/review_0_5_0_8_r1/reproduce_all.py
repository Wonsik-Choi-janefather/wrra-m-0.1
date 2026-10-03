"""Sequential fresh dependency propagation and final bridge contract review."""
from pathlib import Path
import subprocess,sys,shutil,os
R=Path(__file__).resolve().parent;S=R/'studies'
def copy(a,b):shutil.copy2(S/a,S/b)
env=dict(os.environ,OPENBLAS_NUM_THREADS='1');env.pop('WRRA_REPO',None)
for k in range(1,8):
 if k==3:copy('bridge_0_2/results.json','bridge_0_3/source/bridge_0_2_results.json')
 if k==4:copy('bridge_0_3/results.json','bridge_0_4/source/bridge_0_3_results.json')
 if k==5:
  copy('bridge_0_2/results.json','bridge_0_5/source/bridge_0_2_results.json')
  copy('bridge_0_2/internal_and_carrier_basis.npz','bridge_0_5/source/internal_and_carrier_basis.npz')
 if k==6:
  copy('bridge_0_2/results.json','bridge_0_6/source/state_0_2.json')
  copy('bridge_0_2/internal_and_carrier_basis.npz','bridge_0_6/source/internal_and_carrier_basis.npz')
  copy('bridge_0_5/results.json','bridge_0_6/source/clock_0_5.json')
 if k==7:
  copy('bridge_0_2/results.json','bridge_0_7/source/state_0_2.json')
  copy('bridge_0_5/results.json','bridge_0_7/source/clock_0_5.json')
  copy('bridge_0_6/results.json','bridge_0_7/source/measurement_0_6.json')
 p=subprocess.run([sys.executable,str(S/f'bridge_0_{k}'/('audit_0_1.py' if k==1 else f'compute_0_{k}.py'))],env=env,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(f'stage 0.{k}\n'+p.stderr+p.stdout)
 print(f'stage 0.{k} replayed',flush=True)
p=subprocess.run([sys.executable,str(R/'audit_0_8.py')],env=env)
if p.returncode:raise SystemExit(p.returncode)
