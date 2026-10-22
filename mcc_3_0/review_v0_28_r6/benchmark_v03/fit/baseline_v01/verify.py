"""Independent saved-row verifier; exits nonzero on corrupted results."""
import csv,json,sys,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
P=Path(__file__).resolve().parent
D=Path(sys.argv[1]) if len(sys.argv)>1 else P/'results'
def require(ok,msg):
 if not ok:raise AssertionError(msg)
def read(n):return list(csv.DictReader((D/n).open()))
pts=read('point_predictions.csv');fits=read('galaxy_fits.csv');summary=json.loads((D/'summary.json').read_text());sums={};keys=set();groups={};scale={(r['galaxy'],r['model']):float(r['stellar_scale']) for r in fits}
# independent native-scale expression (H0 analytically cancels for fixed SI load)
state=next(x for x in json.loads((P/'wrra_original/inputs/shared_gravity_results.json').read_text())['cases'] if x['carrier_state']=='product' and x['epsilon']==0 and x['a']==1)
fitmap={(r['galaxy'],r['model']):r for r in fits}
a=math.sqrt(math.pi*6.6743e-11*state['sector_density_J_m3'][1]/3)
require(math.isclose(a,summary['aT_native'],rel_tol=1e-13),'NATIVE_LOAD_SCALE')
for r in pts:
 key=(r['galaxy'],r['model']);pk=key+(r['point'],);require(pk not in keys,'DUPLICATE_POINT');keys.add(pk)
 v,e,p=float(r['observed_km_s']),float(r['error_km_s']),float(r['predicted_km_s']);require(e>0 and all(math.isfinite(z) for z in [v,e,p]),'INVALID_ROW')
 z=(p-v)/e;require(math.isclose(z,float(r['residual_sigma']),rel_tol=1e-10,abs_tol=1e-10),'RESIDUAL_MISMATCH')
 sums[key]=sums.get(key,0)+z*z;groups.setdefault(key,[]).append((r['point'],r['r_kpc'],v,e))
 if r['model'].startswith('WRRA'):
  at=summary['aT_calibrated'] if r['model']=='WRRA_global_aT' else a
  radius=float(r['r_kpc'])*3.085677581491367e19
  gb=(float(r['gas_v2'])+scale[key]*float(r['stellar_v2_at_unit_scale']))*1e6/radius
  require(gb>0,'NONPOSITIVE_BARYON_SOURCE')
  mu=1-expm(np.array([[-1.,0.],[1.,0.]])*math.sqrt(gb/at))[0,0]
  pred=math.sqrt(radius*gb/mu)/1000
  require(math.isclose(pred,p,rel_tol=1e-10),'GATE_REPLAY_MISMATCH')
 else:
  f=fitmap[key];vv=float(f['v200_km_s']);c=float(f['concentration']);x=float(r['r_kpc'])*(.674)/vv
  vh2=vv*vv*(math.log1p(c*x)-c*x/(1+c*x))/(x*(math.log1p(c)-c/(1+c)))
  pred=math.sqrt(float(r['gas_v2'])+scale[key]*float(r['stellar_v2_at_unit_scale'])+vh2)
  require(math.isclose(pred,p,rel_tol=1e-10),'NFW_REPLAY_MISMATCH')
for f in fits:
 k=(f['galaxy'],f['model']);require(len(groups[k])==int(f['n']),'POINT_COUNT');require(math.isclose(sums[k],float(f['chi2']),rel_tol=1e-10,abs_tol=1e-9),'GALAXY_CHI2')
 require(groups[k]==groups[(f['galaxy'],'WRRA_fixed')],'UNMATCHED_DATA')
for s in summary['summary']:
 rr=[f for f in fits if f['model']==s['model']];N=sum(int(f['n']) for f in rr);k=sum(int(f['k_local']) for f in rr)+(s['model']=='WRRA_global_aT');chi=sum(sums[(f['galaxy'],f['model'])] for f in rr)
 require(N==s['N'] and k==s['k'],'DEGREES_OF_FREEDOM');require(math.isclose(chi,s['chi2'],rel_tol=1e-11),'TOTAL_CHI2');require(math.isclose(chi/(N-k),s['chi2_per_dof'],rel_tol=1e-11),'REDUCED_CHI2');require(s['fit_failures']==0,'OPTIMIZER_FAILURE')
print(json.dumps({'status':'PASS','saved_prediction_rows':len(pts),'galaxy_model_rows':len(fits),'models':len(summary['summary']),'independent_gate':'matrix exponential','native_scale':'SI load identity','matched_rows':True}))
