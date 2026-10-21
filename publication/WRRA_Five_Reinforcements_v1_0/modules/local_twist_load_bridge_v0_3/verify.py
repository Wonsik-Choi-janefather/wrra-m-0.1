"""Independent finite-volume 3D receiver and mixed-action variation audit."""
from pathlib import Path
import numpy as np,json,math
from numpy.polynomial.legendre import leggauss
P=Path(__file__).resolve().parent
out=json.loads((P/'results.json').read_text());checks={};rows=[]
def source(x,y,z):
 return [.45+.2*np.sin(x)+.02*np.sin(x+y),.2+.12*np.sin(y)+.02*np.sin(x+y),.1+.06*np.sin(z)]
for n in [32,64,128]:
 h=2*np.pi/n;a=np.arange(n)*h;coords=np.meshgrid(a,a,a,indexing='ij',sparse=True);faces=[]
 for j in range(3):
  x=[q.copy() for q in coords];x[j]=x[j]+h/2
  v=np.array(np.broadcast_arrays(*source(*x)));mag=np.sqrt(np.sum(v*v,axis=0));faces.append(v[j]/(-np.expm1(-np.sqrt(mag))))
 rhs=sum((faces[j]-np.roll(faces[j],1,axis=j))/h for j in range(3))
 k=np.fft.fftfreq(n,d=1/n);kk=np.meshgrid(k,k,k,indexing='ij',sparse=True);lam=sum(4*np.sin(q*h/2)**2/h**2 for q in kk)
 f=np.fft.fftn(rhs);phi=np.fft.ifftn(np.divide(-f,lam,out=np.zeros_like(f),where=lam>0)).real
 F=[(np.roll(phi,-1,axis=j)-phi)/h+faces[j].mean() for j in range(3)]
 div=sum((F[j]-np.roll(F[j],1,axis=j))/h for j in range(3))
 resid=float(np.linalg.norm(div-rhs)/np.linalg.norm(rhs));assert resid<1e-11
 centered=[.5*(F[j]+np.roll(F[j],1,axis=j)) for j in range(3)]
 point=np.array([v[n//8,n//4,3*n//8] for v in centered]);ref=next(r for r in out['three_dimensional'] if r['n']==n);target=np.array([ref['probe_x'],ref['probe_y'],ref['probe_z']])
 err=float(np.linalg.norm(point-target));rows.append({'n':n,'finite_volume_flux_residual':resid,'probe_L2_difference_from_spectral':err,'probe':point.tolist()})
checks['independent_volume_flux']=all(r['finite_volume_flux_residual']<1e-11 for r in rows)
orders=[math.log(rows[j-1]['probe_L2_difference_from_spectral']/rows[j]['probe_L2_difference_from_spectral'],2) for j in [1,2]]
checks['independent_second_order_convergence']=all(1.8<p<2.2 for p in orders)
# Mixed two-potential action: Q(Y)=2*Psi(sqrt(Y)) from the v0.2 finite gate cost.
quadx,quadw=leggauss(96)
def Q(Y):
 s=np.asarray(Y)**.25;t=(quadx[:,None,None]+1)*s[None,:,:]/2
 val=4*t**3/(-np.expm1(-t))
 return s/2*np.sum(quadw[:,None,None]*val,axis=0)
n=17;a=np.arange(n)*2*np.pi/n;x,y=np.meshgrid(a,a,indexing='ij');k=np.fft.fftfreq(n,d=1/n);ks=np.meshgrid(k,k,indexing='ij')
def grad(phi):
 f=np.fft.fftn(phi);return np.array([np.fft.ifftn(1j*q*f).real for q in ks])
def div(v):return sum(np.fft.ifftn(1j*ks[j]*np.fft.fftn(v[j])).real for j in range(2))
phi=.03*np.cos(x)*np.sin(y);native=.05*np.cos(x)+.02*np.sin(x+y);external=np.array([.45,.2])[:,None,None]
j=-.05*np.cos(x)-.04*np.sin(x+y)
def E(p,nv):
 v=grad(nv)+external;Y=np.sum(v*v,axis=0)
 return float(np.mean(2*np.sum(grad(p)*v,axis=0)-Q(Y)+2*j*p))
v=grad(native)+external;mag=np.sqrt(np.sum(v*v,axis=0));raw=v/(-np.expm1(-np.sqrt(mag)))
ELp=-2*div(grad(native))+2*j;ELn=-2*div(grad(phi))+2*div(raw)
direction=np.cos(2*x+y)+.3*np.sin(x);h=1e-6
fdp=(E(phi+h*direction,native)-E(phi-h*direction,native))/(2*h)
fdn=(E(phi,native+h*direction)-E(phi,native-h*direction))/(2*h)
ep=abs(fdp-np.mean(ELp*direction));en=abs(fdn-np.mean(ELn*direction))
checks['mixed_action_Phi_variation']=ep<1e-8;checks['mixed_action_PhiN_variation']=en<1e-8
# Traction follows the quadratic covector energy variation at fixed one-form.
norm=np.array([1.,2.,3.]);norm/=np.linalg.norm(norm);H=np.array([[.2,.1,0],[.1,-.3,.02],[0,.02,.1]])
def covector_energy(t):
 metric=np.eye(3)+t*H
 return float(math.sqrt(np.linalg.det(metric))*norm@np.linalg.solve(metric,norm))
fd=(covector_energy(1e-6)-covector_energy(-1e-6))/(2e-6)
analytic=float(.5*np.trace(H)-norm@H@norm)
checks['quadratic_metric_variation']=abs(fd-analytic)<1e-9
checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),checks
result={'status':'PASS','method':'Independent staggered finite-volume Poisson receiver, spectral two-potential action variation and fixed-covector metric derivative','checks':checks,'finite_volume':rows,'convergence_orders':orders,'mixed_action_directional_errors':{'Phi':ep,'Phi_N':en},'metric_variation_error':abs(fd-analytic),'scope':'Internal independent numerical audit; not new observed galaxy data or a complete relativistic action'}
(P/'independent_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
