"""Independent time stepping of the full two-component equation (NumPy only)."""
from pathlib import Path
import numpy as np,json
P=Path(__file__).resolve().parent
z=np.load(P/'dense_verification_input.npz');w=z['w'];psi=z['psi'];n=len(w)
q=float(z['beta'])*2*np.pi*abs(np.fft.fftfreq(n,d=1/n));V=np.pi*w/2
state=np.stack([psi,np.zeros(n,dtype=complex)]).astype(complex)
def rhs(y):
 kin=np.fft.ifft(np.fft.fft(y,axis=1)*q,axis=1)
 dif=V*(y[0]-y[1]);kin[0]+=dif;kin[1]-=dif
 return -1j*kin
errors=[]
for steps in [1024,2048,4096]:
 y=state.copy();dt=1/steps
 for j in range(steps):
  k1=rhs(y);k2=rhs(y+dt*k1/2);k3=rhs(y+dt*k2/2);k4=rhs(y+dt*k3)
  y+=dt*(k1+2*k2+2*k3+k4)/6
 err=float(np.linalg.norm(y-np.stack([z['va'],z['vb']])))
 errors.append({'steps':steps,'state_L2_error':err,'norm_error':abs(float(np.sum(abs(y)**2))-1),'record_probability':.5*float(np.sum(abs(y[1])**2))})
assert errors[-1]['state_L2_error']<1e-9,errors
# 4th order should be visible before roundoff saturation; a final error floor is allowed.
assert errors[-1]['state_L2_error']<errors[0]['state_L2_error'],errors
# Full block matrix independently checks the block-diagonal reduction.
hc=z['hc'];h=np.block([[hc+np.diag(V),-np.diag(V)],[-np.diag(V),hc+np.diag(V)]])
e,v=np.linalg.eigh(h);ref=v@(np.exp(-1j*e)*(v.conj().T@state.reshape(-1)))
blockerr=float(np.linalg.norm(ref-np.r_[z['va'],z['vb']]))
assert blockerr<1e-11,blockerr
result={'status':'PASS','method':'Direct RK4 time integration of coupled FFT equations and full 2N-block diagonalization, checked against projector reduction','RK4':errors,'full_block_state_L2_error':blockerr,'scope':'Internal independent numerical check; not external peer review or observation'}
(P/'independent_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
