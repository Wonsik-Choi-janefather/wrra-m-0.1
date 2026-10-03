"""Recompute the default ledger and independently audit it with pinned threads."""
from pathlib import Path
import hashlib
import os
import subprocess
import sys
import json

ROOT=Path(__file__).resolve().parent
paths=['code/results.json','code/handoff.json','verification/independent_audit.json']
before={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
env={**os.environ,'OPENBLAS_NUM_THREADS':'2','OMP_NUM_THREADS':'2'}
for name in ['code/compute.py','verify_release.py']:
    subprocess.run([sys.executable,str(ROOT/name)],cwd=ROOT,env=env,check=True)
after={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
result={'all_passed':True,'byte_exact_reference_outputs':before==after,
        'total_checks':json.loads((ROOT/paths[-1]).read_text())['total_checks']}
print(json.dumps(result))
if before!=after:
    raise SystemExit('Numerical checks passed but reference bytes differ: inspect platform and dependency versions.')
