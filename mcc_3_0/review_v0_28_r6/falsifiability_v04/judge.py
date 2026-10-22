"""Claim-level decision gate. 0: survives/observed advantage, 1: claim fails,
2: invalid evidence, 3: not identifiable or not established. Never declares universe proven.
"""
from pathlib import Path
import sys,json,math,csv
from scipy.stats import chi2
import numpy as np
P=Path(__file__).resolve().parent
class Invalid(ValueError):pass
def req(x,s):
 if not x:raise Invalid(s)
def decide(d):
 req(d.get('claim_id') and d.get('version'),'MISSING_CLAIM_VERSION')
 kind=d['kind']
 if kind=='paired_advantage':
  a=np.asarray(d['candidate_losses'],float);b=np.asarray(d['reference_losses'],float)
  req(a.shape==b.shape and a.ndim==1 and len(a)>0 and np.isfinite(a).all() and np.isfinite(b).all(),'INVALID_LOSSES')
  req(d['same_inputs'] and d['same_errors'] and d['same_split'],'UNMATCHED_COMPARISON')
  delta=float(a.sum()-b.sum())
  if d['scope']=='sample_aggregate':return (0 if delta<0 else 1),dict(status='OBSERVED_ADVANTAGE' if delta<0 else 'ADVANTAGE_CLAIM_FAILS',delta=delta)
  req(d['scope']=='population','INVALID_SCOPE');lo,hi=map(float,d['interval']);req(math.isfinite(lo) and math.isfinite(hi) and lo<=hi,'INVALID_INTERVAL')
  if not d['selection_adjusted']:return 3,dict(status='POPULATION_ADVANTAGE_UNESTABLISHED',reason='Exploratory model selection not adjusted',delta=delta)
  return (0 if hi<0 else 1 if lo>0 else 3),dict(status='INTERVAL_BELOW_ZERO' if hi<0 else 'INTERVAL_ABOVE_ZERO' if lo>0 else 'INCONCLUSIVE',delta=delta)
 if kind=='fixed_prediction':
  if not d['mapping_confirmed']:return 3,dict(status='OPEN_MAPPING',reason='Preparation / coupling / receiver not independently established')
  req(d['parameters_fitted_on_test']==0,'TEST_REFIT_NOT_ALLOWED')
  req(d['distribution']=='gaussian_known_covariance','UNCALIBRATED_TEST_DISTRIBUTION')
  a=np.asarray(d['observations'],float);mu=np.asarray(d['predictions'],float);C=np.asarray(d['covariance'],float)
  req(a.ndim==1 and len(a)>0 and a.shape==mu.shape and C.shape==(len(a),len(a)),'DIMENSIONS')
  req(np.isfinite(a).all() and np.isfinite(mu).all() and np.isfinite(C).all(),'NONFINITE')
  req(np.allclose(C,C.T,atol=1e-14,rtol=0),'COVARIANCE_ASYMMETRIC')
  try:L=np.linalg.cholesky(C)
  except np.linalg.LinAlgError:raise Invalid('COVARIANCE_NOT_POSITIVE_DEFINITE')
  alpha=float(d['family_alpha']);m=d['family_tests'];req(0<alpha<1 and type(m)==int and m>=1,'INVALID_ALPHA_OR_FAMILY')
  residual=np.linalg.solve(L,a-mu);Q=float(residual@residual);p=float(chi2.sf(Q,len(a)));threshold=alpha/m;reject=p<threshold
  return int(reject),dict(status='REJECT_FIXED_BRANCH' if reject else 'NOT_REJECTED',Q=Q,p=p,alpha_per_test=threshold,synthetic=bool(d['synthetic']))
 raise Invalid('UNKNOWN_KIND')
def main(path):
 try:
  d=json.loads(Path(path).read_text());code,result=decide(d);print(json.dumps(dict(claim_id=d['claim_id'],version=d['version'],exit=code,**result)));return code
 except (ValueError,KeyError,TypeError) as e:print(json.dumps(dict(status='INVALID',error=str(e))));return 2
if __name__=='__main__':sys.exit(main(sys.argv[1]))
