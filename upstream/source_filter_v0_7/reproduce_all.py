"""Recompute the default ledger and independently audit it with pinned threads."""
from pathlib import Path
import hashlib
import os
import subprocess
import sys
import json

ROOT=Path(__file__).resolve().parent
paths=['code/results.json','code/handoff.json','verification/independent_audit.json']
before={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths if (ROOT/p).exists()}
env={**os.environ,'OPENBLAS_NUM_THREADS':'2','OMP_NUM_THREADS':'2'}
for name in ['code/compute.py','verify_release.py']:
    subprocess.run([sys.executable,str(ROOT/name)],cwd=ROOT,env=env,check=True)
after={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
if len(before)!=len(paths):
    # A clean source archive has no saved outputs: verify a deterministic second pass.
    for name in ['code/compute.py','verify_release.py']:
        subprocess.run([sys.executable,str(ROOT/name)],cwd=ROOT,env=env,check=True)
    replay={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    if replay!=after:raise SystemExit('Clean regeneration is not byte deterministic.')
    # Existing partial references still must match; newly created outputs are explicit.
    if any(after[p]!=digest for p,digest in before.items()):raise SystemExit('Existing reference bytes differ.')
    before=after
result={'all_passed':True,'byte_exact_reference_outputs':before==after,
        'total_checks':json.loads((ROOT/paths[-1]).read_text())['total_checks']}
print(json.dumps(result))
if before!=after:
    raise SystemExit('Numerical checks passed but reference bytes differ: inspect platform and dependency versions.')
