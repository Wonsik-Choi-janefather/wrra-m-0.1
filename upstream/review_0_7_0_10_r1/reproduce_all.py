"""Reviewed finite upstream collection; development endpoint remains 0.10."""
from pathlib import Path
import os,subprocess,sys
ROOT=Path(__file__).resolve().parent;UP=ROOT.parent
env=dict(os.environ,OPENBLAS_NUM_THREADS='2',OMP_NUM_THREADS='2')
for stage in ['source_filter_v0_7','shutter_v0_8','residue_current_v0_9','generator_v0_10']:
 subprocess.run([sys.executable,str(UP/stage/'reproduce_all.py')],check=True,env=env)
subprocess.run([sys.executable,str(ROOT/'verify_review.py')],check=True,env=env)
