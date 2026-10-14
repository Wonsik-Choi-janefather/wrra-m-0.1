from pathlib import Path
import os,sys,subprocess
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent
env=dict(os.environ,OMP_NUM_THREADS='1',PYTHONPATH=str(ROOT/'runtime')+os.pathsep+os.environ.get('PYTHONPATH',''))
subprocess.run([sys.executable,str(ROOT/'upstream.py')],env=env,check=True)
jobs=[(b,'standard',2.5) for b in ['weighted','unweighted','dark_weight_only']]
jobs += [('dark_weight_only',k,a) for k in ['D','R'] for a in [1.5,2.5]]
jobs += [('dark_weight_only','zero',2.5)]
def run(j):
    subprocess.run([sys.executable,str(ROOT/'cmb_runner.py'),j[0],j[1],str(j[2])],env=env,check=True)
with ThreadPoolExecutor(max_workers=2) as p:list(p.map(run,jobs))
for script in ['validate.py','figures.py']:
    subprocess.run([sys.executable,str(ROOT/script)],env=env,check=True)
