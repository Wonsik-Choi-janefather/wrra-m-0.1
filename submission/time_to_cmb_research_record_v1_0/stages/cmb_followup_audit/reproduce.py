from pathlib import Path
import subprocess,sys,os,json
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent
env=dict(os.environ,OMP_NUM_THREADS='1',PYTHONPATH=str(ROOT/'runtime')+os.pathsep+os.environ.get('PYTHONPATH',''))
subprocess.run([sys.executable,str(ROOT/'followup.py')],env=env,check=True)
def run(args):subprocess.run([sys.executable,str(ROOT/'followup.py'),'mixed',*args],env=env,check=True)
with ThreadPoolExecutor(max_workers=2) as p:
    list(p.map(run,[['weighted_D_only','weighted','unweighted'],['weighted_R_only','unweighted','weighted']]))
f=ROOT/'results/followup_results.json';j=json.loads(f.read_text())
j['counterfactuals']=[json.loads((ROOT/'results'/n).read_text()) for n in ['weighted_D_only.json','weighted_R_only.json']]
f.write_text(json.dumps(j,indent=2))
