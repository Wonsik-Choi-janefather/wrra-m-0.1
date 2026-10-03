import json
from pathlib import Path
import numpy as np
from compute import shutter,select_record
rng=np.random.default_rng(20261003);checks=0
for _ in range(100):
 x=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));r=x@x.conj().T;r/=np.trace(r)
 e=float(rng.random());out=shutter(r,e)
 assert np.linalg.eigvalsh(out).min()>-1e-12
 assert abs(np.trace(out)-1)<1e-12
 assert np.allclose(np.diag(out),np.diag(r));checks+=3
 j,c=select_record(r,float(rng.random()));assert np.trace(c)==1 and np.count_nonzero(c)==1;checks+=1
for bad in [-1,2,float('nan')]:
 try:shutter(np.eye(3)/3,bad)
 except ValueError:checks+=1
 else:raise AssertionError
Path(__file__).with_name('audit.json').write_text(json.dumps({'random_seed':20261003,'checks_passed':checks,'scope':'100 independent positive density matrices; invalid shutter strengths'},indent=2)+'\n')
print(checks,'shutter audit checks passed')
