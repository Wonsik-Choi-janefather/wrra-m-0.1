"""Rerun all CMB response, control and likelihood calculations."""
from pathlib import Path
import os,subprocess,sys
ROOT=Path(__file__).resolve().parent
env=dict(os.environ,OMP_NUM_THREADS='1',PYTHONPATH=str(ROOT/'runtime')+os.pathsep+os.environ.get('PYTHONPATH',''))
# numpy/scipy/matplotlib/sympy/mpmath must be installed in this Python environment.
jobs=[(b,k,a,f,s) for b in ['weighted','unweighted'] for k in ['standard','zero','D','R'] for a,f,s in [(1.5,1,1)]]
jobs += [(b,k,2.5,1,1) for b in ['weighted','unweighted'] for k in ['standard','D','R']]
jobs += [('weighted','R',1.5,0,1),('weighted','R',1.5,1,.1)]
for b,k,a,f,s in jobs:
    subprocess.run([sys.executable,str(ROOT/'calculate.py'),'--branch',b,'--kind',k,'--accuracy',str(a),
        '--force',str(f),'--start-factor',str(s)],env=env,check=True)
for script in ['audit_evolution.py','clocks.py','summarize.py']:
    if script=='summarize.py':
        for b in ['weighted','unweighted']:
            subprocess.run([sys.executable,str(ROOT/'calculate.py'),'--branch',b,'--kind','standard','--lmax','2500'],env=env,check=True)
    subprocess.run([sys.executable,str(ROOT/script)],env=env,check=True)
