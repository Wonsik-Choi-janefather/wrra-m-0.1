"""Common partial-trace readout for differently prepared drive states."""
from pathlib import Path
import json
import numpy as np
from scipy.special import expit
from scipy.optimize import brentq
odd_total=.057772944563190744;d=.268;target=.05
w=np.array([.2,.1,.3,.4])*odd_total
z=np.array([[-.7,.4,.9],[.1,-.3,.6],[1.,.2,-.8],[.2,.8,-.5]])
drives=[z,z+np.array([[.7],[-.4],[.3],[-.6]])]
T=lambda h,z:1-np.prod(1-expit(z-h),axis=1)
states=[];checks=[]
for x,drive in enumerate(drives):
 h=brentq(lambda h:w@T(h,drive)-target,-40,40)
 # Diagonal of the density operator on 3 outcome labels x 6 addresses.
 # Four odd-composite addresses, one even-composite address, one prime address.
 omega=np.zeros((3,6));omega[0,:4]=w*T(h,drive);omega[2,:4]=w-omega[0,:4]
 omega[1,4]=d;omega[2,5]=1-d-odd_total;states.append(omega)
 checks.append({'name':f'drive {x} flagged state positive and trace one','passed':bool(np.all(omega>=0) and abs(omega.sum()-1)<1e-12)})
 checks.append({'name':f'drive {x} conditional distribution normalized','passed':bool(abs((omega[0]/omega[0].sum()).sum()-1)<1e-12)})
a,b=states;ca=a.sum(axis=1);cb=b.sum(axis=1)
checks += [{'name':'fine states are distinguishable','passed':bool(np.abs(a-b).sum()>1e-5)}, {'name':'same partial trace erases their difference','passed':bool(np.allclose(ca,cb,atol=1e-12,rtol=0))}, {'name':'calibrated coarse output','passed':bool(np.allclose(ca,[.05,.268,.682],atol=1e-12,rtol=0))}, {'name':'same energy for several positive volumes','passed':bool(all(abs(ca@np.array([1.7,1.7,V])-cb@np.array([1.7,1.7,V]))<1e-12 for V in [.1,1.7,4]))}]
r={'passed':sum(x['passed'] for x in checks),'total':len(checks),'fine_state_l1_distance':float(np.abs(a-b).sum()),'coarse_outputs':[ca.tolist(),cb.tolist()],'checks':checks}
Path(__file__).with_name('common_readout_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));assert all(x['passed'] for x in checks)
