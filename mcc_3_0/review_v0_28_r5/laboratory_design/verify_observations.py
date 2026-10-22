"""Recompute fixed predictions; test supplied observations and full covariance.
Exit 0 = not rejected, 1 = rejected at alpha, 2 = invalid input.
Not a claim that the fixed branch describes nature.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from scipy.stats import chi2
from design import ROOT,MODEL,visibility

def run(path):
 cfg=json.loads((ROOT/'design.json').read_text());data=json.loads(Path(path).read_text())
 digest=hashlib.sha256((MODEL/'inputs/finite_preparation.npz').read_bytes()).hexdigest()
 if data['source_profile_sha256']!=digest or cfg['source_profile_sha256']!=digest: raise ValueError('SOURCE_PROFILE_HASH_MISMATCH')
 points=cfg['points']; order=[[p['wavelength_m'],p['L_m']] for p in points]
 if data['point_order']!=order: raise ValueError('POINT_ORDER_MISMATCH')
 y=np.array(data['observations'],float);C=np.array(data['covariance'],float)
 if y.shape!=(len(points),) or C.shape!=(len(points),len(points)) or not np.isfinite(y).all() or not np.isfinite(C).all(): raise ValueError('INVALID_DIMENSIONS_OR_NONFINITE')
 if not np.allclose(C,C.T,atol=1e-14,rtol=0):raise ValueError('COVARIANCE_NOT_SYMMETRIC')
 L=np.linalg.cholesky(C)
 mu=np.array([visibility(p['L_m'],p['wavelength_m']) for p in points])
 r=np.linalg.solve(L,y-mu);Q=float(r@r);p=float(chi2.sf(Q,len(y)));reject=p<cfg['test_alpha']
 print(json.dumps({'data':Path(path).name,'synthetic':data.get('synthetic',False),'Q':Q,'dof':len(y),'p_value':p,'alpha':cfg['test_alpha'],'decision':'REJECT_FIXED_BRANCH' if reject else 'NOT_REJECTED','no_parameters_fitted':True}))
 return int(reject)
if __name__=='__main__':
 try:sys.exit(run(sys.argv[1]))
 except Exception as e:print(json.dumps({'error':str(e)}));sys.exit(2)
