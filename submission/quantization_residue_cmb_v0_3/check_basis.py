import verify_inputs
from pathlib import Path
import json
import numpy as np
from run_transfers import camb,params,ROOT
out={}
for kind in ['D','A']:
    p=params(kind=kind);r=camb.get_background(p)
    k=np.array([.05,.2,1.,3.2]);times=np.array([1e-4,1e-3,1e-2])
    v=np.array([r.get_time_evolution(float(kk),[min(.001/kk,.1)],['delta_photon','delta_cdm','etak']) for kk in k])
    entropy=v[:,:,1]-.75*v[:,:,0]
    zr=.25*v[:,:,0]-v[:,:,2]/k[:,None]
    out[kind]={'entropy_at_first_time':entropy[:,0].tolist(),
              'radiation_curvature_at_first_time':zr[:,0].tolist()}
print(json.dumps(out,indent=2),flush=True)
assert max(abs(np.array(out['D']['entropy_at_first_time'])-1))<1e-5
assert max(abs(np.array(out['A']['radiation_curvature_at_first_time'])+1))<1e-5
assert max(abs(np.array(out['A']['entropy_at_first_time'])))<1e-9
assert max(abs(np.array(out['D']['radiation_curvature_at_first_time'])))<1e-7
out['mapping']='CAMB initial vector = [-zeta_radiation, S_c, 0, 0, 0]'
(ROOT/'results/basis_normalization.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
