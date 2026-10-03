from pathlib import Path
import subprocess,sys,os
root=Path(__file__).resolve().parent
env=dict(os.environ,OPENBLAS_NUM_THREADS='2')
for script in ['compute.py','verify_release.py']:
 subprocess.run([sys.executable,str(root/script)],check=True,env=env)
