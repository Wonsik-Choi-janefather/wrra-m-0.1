"""Build the SOURCE patch from the included pristine CAMB 2.0.4 archive."""
from pathlib import Path
import subprocess,sys,tarfile,os,shutil
ROOT=Path(__file__).resolve().parent
build=ROOT/'build';build.mkdir(exist_ok=True)
target=build/'camb-2.0.4'
if target.exists():
    raise SystemExit('Build directory already exists. Use a fresh extraction to prevent duplicate patching.')
with tarfile.open(ROOT/'inputs/camb-2.0.4.tar.gz') as t:
    t.extractall(build,filter='data')
subprocess.run([sys.executable,str(ROOT/'cmb_patch.py'),str(target)],check=True)
subprocess.run([sys.executable,str(ROOT/'apply_pair_sampling.py'),str(target)],check=True)
env=dict(os.environ,CAMB_CLUSTER_SAFE='1')
proc=subprocess.run([sys.executable,'setup.py','make'],cwd=target,env=env,capture_output=True,text=True)
(build/'build.log').write_text(proc.stdout+proc.stderr)
binary=target/'camb/camblib.so'
if proc.returncode or not binary.exists() or 'Error ' in proc.stdout+proc.stderr:
    raise SystemExit('Compilation failed; inspect build/build.log. Requires a working gfortran and make.')
shutil.copytree(target/'camb',ROOT/'runtime/camb',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
print('Built patched CAMB. Run with PYTHONPATH=runtime.')
