from pathlib import Path
import subprocess,sys,os
P=Path(__file__).resolve().parent
env=dict(os.environ,OMP_NUM_THREADS='2',OPENBLAS_NUM_THREADS='2')
for name in ['prepare_inputs.py','run_camb.py','thermal_history.py','lensing_likelihood.py','run_checks.py']:
    subprocess.run([sys.executable,str(P/name)],cwd=P,env=env,check=True)
