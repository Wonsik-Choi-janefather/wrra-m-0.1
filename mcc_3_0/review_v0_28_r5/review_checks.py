from pathlib import Path
import sys,csv,json,numpy as np
from scipy.linalg import expm
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'sparc_fit_v02'))
import fit
D,meta,clean=fit.getdata();rows=list(csv.DictReader((fit.P/'results/predictions.csv').open()))
for row in rows:
 d=D[row['galaxy']]; j=int(row['point'])
 for a,b in [('r_kpc','r'),('vobs','v'),('error','e'),('gas_v2','gas'),('stars_v2','stars')]:
  assert np.isclose(float(row[a]),d[b][j],rtol=1e-13,atol=1e-13),(row['galaxy'],j,a)
I=np.eye(4);Pi=np.diag([1,0,1,0]);G=.37
K=np.sqrt(G)*Pi;Hold=I-Pi+np.sqrt(1-G)*Pi
select=float(np.max(abs(K.T@K+Hold.T@Hold-I)))
swap=np.array([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]])
unit=float(np.max(abs(expm(-1j*np.pi/2*(I-swap))-swap)))
n=np.arange(2,6);gam=np.array([14.134725,21.02204,25.010858]);C=len(gam)
Ds=[np.diag(np.exp(-1j*g*np.log(n))) for g in gam]
A=[sum(np.exp(-2j*np.pi*m*j/C)*Ds[j] for j in range(C))/C for m in range(C)]
ports=float(np.max(abs(sum(a.conj().T@a for a in A)-I)))
assert max(select,unit,ports)<1e-12
fits=list(csv.DictReader((fit.P/'results/fits.csv').open()));f={}
for r in fits:
 if r['phase']=='full' and r['model'] in ['WRRA_radial_ML','NFW_ML']:f.setdefault(r['galaxy'],{})[r['model']]=float(r['chi2'])
delta={k:v['WRRA_radial_ML']-v['NFW_ML'] for k,v in f.items()}
r={'source_observation_rows_checked':len(rows),'normal_source_match':True,'selection_identity_max_error':select,'swap_unitary_max_error':unit,'ports_completeness_max_error':ports,'wrra_better':sum(v<0 for v in delta.values()),'nfw_better':sum(v>0 for v in delta.values()),'total_delta_chi2':sum(delta.values()),'IC2574_delta':delta['IC2574'],'UGC06787_delta':delta['UGC06787'],'omit_two_contributions_delta':sum(v for k,v in delta.items() if k not in ['IC2574','UGC06787']),'scope':'saved-fit replay and finite operator examples; no full refit, physical experiment or whole-model execution'}
(P/'REVIEW_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
