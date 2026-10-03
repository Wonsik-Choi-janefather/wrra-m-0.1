"""Finite periodic two-component Schroedinger-Poisson feedback, dimensionless effective model."""
from pathlib import Path
import json,math,hashlib
import numpy as np
R=Path(__file__).resolve().parent
source=json.loads((R/'source/state_0_2.json').read_text());baseline=next(x for x in source['rows'] if x['case']=='baseline')
pop=baseline['excited_population'];L=20.;coupling=1.;checks=[];runs=[]
def ck(n,b):checks.append({'name':n,'passed':bool(b)})
def build(N):
 x=np.arange(N)*L/N;dx=L/N;k=2*np.pi*np.fft.fftfreq(N,d=dx)
 def bump(center):
  dist=((x-center+L/2)%L)-L/2
  a=np.exp(-dist**2/(2*1.6**2)).astype(complex)
  return a/math.sqrt(float(dx*np.vdot(a,a).real))
 psi=np.column_stack([math.sqrt(1-pop)*bump(L*.35),math.sqrt(pop)*bump(L*.65)*np.exp(2j*np.pi*x/L)])
 return x,dx,k,psi
def field(psi,dx,k,lam):
 rho=np.sum(abs(psi)**2,axis=1);rh=np.fft.fft(rho-rho.mean());ph=np.zeros(len(k),complex)
 mask=k!=0;ph[mask]=-lam*rh[mask]/k[mask]**2
 return rho,np.fft.ifft(ph).real
def step(psi,dx,k,lam,dt):
 _,phi=field(psi,dx,k,lam);v=psi*np.exp(-.5j*dt*phi[:,None])
 v=np.fft.ifft(np.fft.fft(v,axis=0)*np.exp(-.5j*dt*k[:,None]**2),axis=0)
 _,phi=field(v,dx,k,lam);return v*np.exp(-.5j*dt*phi[:,None])
def energy(psi,dx,k,lam):
 rho,phi=field(psi,dx,k,lam)
 grad=np.fft.ifft(1j*k[:,None]*np.fft.fft(psi,axis=0),axis=0)
 return float(.5*dx*np.sum(abs(grad)**2)+.5*dx*np.dot(rho,phi))
finals={}
for N,dt in [(64,.01),(64,.005),(64,.0025),(128,.0025)]:
 x,dx,k,psi=build(N);initial=psi.copy();E0=energy(psi,dx,k,coupling);steps=round(1/dt);Es=[];history=[]
 for it in range(steps):
  psi=step(psi,dx,k,coupling,dt);Es.append(energy(psi,dx,k,coupling))
  if (it+1)%(steps//10)==0:history.append({'s':(it+1)*dt,'dynamic_energy':Es[-1]})
 rho,phi=field(psi,dx,k,coupling);norm=float(dx*np.sum(abs(psi)**2));error=max(abs(np.array(Es)-E0))
 tag=f'N{N}_dt{dt}'
 ck(tag+' norm',abs(norm-1)<2e-11)
 ck(tag+' mode populations',np.max(abs(dx*np.sum(abs(psi)**2,axis=0)-np.array([1-pop,pop])))<2e-11)
 ck(tag+' dynamic energy drift',error<2e-5)
 residual=np.fft.ifft(-k**2*np.fft.fft(phi)).real-coupling*(rho-rho.mean())
 ck(tag+' Poisson feedback residual',np.max(abs(residual))<2e-11)
 ck(tag+' nonuniform field executed',np.ptp(phi)>1e-3 and np.ptp(rho)>1e-3)
 rev=psi.copy()
 for _ in range(steps):rev=step(rev,dx,k,coupling,-dt)
 ck(tag+' reverse evolution',np.linalg.norm(rev-initial)*math.sqrt(dx)<2e-10)
 # Exact lattice current divergence for the spectral Hermitian kinetic operator.
 K=np.fft.ifft(.5*k[:,None]**2*np.fft.fft(np.eye(N),axis=0),axis=0)
 ck(tag+' kinetic Hermitian relative norm',np.linalg.norm(K-K.conj().T)/np.linalg.norm(K)<1e-13)
 kinetic_matrix=float(dx*np.sum(psi.conj()*(K@psi)).real)
 grad=np.fft.ifft(1j*k[:,None]*np.fft.fft(psi,axis=0),axis=0)
 kinetic_gradient=float(.5*dx*np.sum(abs(grad)**2))
 ck(tag+' kinetic matrix-gradient energy equality',abs(kinetic_matrix-kinetic_gradient)<1e-12)
 # drho here is the cell mass derivative d(dx*rho_i)/ds.
 drho=2*dx*np.imag(np.sum(psi.conj()*(K@psi),axis=1))
 J=np.zeros((N,N))
 for z in range(2):J+=-2*dx*np.imag(psi[:,z].conj()[:,None]*K*psi[:,z][None,:])
 ck(tag+' lattice current antisymmetry',np.max(abs(J+J.T))<1e-12)
 ck(tag+' local continuity',np.max(abs(drho+J.sum(axis=1)))<1e-12)
 free=initial.copy()
 for _ in range(steps):free=step(free,dx,k,0.,dt)
 diff=math.sqrt(float(dx*np.sum((rho-np.sum(abs(free)**2,axis=1))**2)))
 ck(tag+' feedback differs from free propagation',diff>1e-4)
 runs.append({'N':N,'dt_dimensionless':dt,'norm':norm,'max_dynamic_energy_drift':float(error),'dynamic_energy_initial':E0,'final_density':rho.tolist(),'potential':phi.tolist(),'density_feedback_minus_free_L2':diff,'history':history})
 finals[(N,dt)]=rho
 e1=math.sqrt(float(dx*np.sum((rho-rho.mean())**2)))
# Time convergence does not hide constant rest/internal energy in the denominator.
dx=L/64
coarse=math.sqrt(float(dx*np.sum((finals[(64,.01)]-finals[(64,.005)])**2)))
fine=math.sqrt(float(dx*np.sum((finals[(64,.005)]-finals[(64,.0025)])**2)))
ck('second order time refinement',fine<coarse/3)
ck('time density convergence quantitative order',3.8<coarse/fine<4.2)
ck('dynamic energy drift coarse-to-medium refinement',3.8<runs[0]['max_dynamic_energy_drift']/runs[1]['max_dynamic_energy_drift']<4.2)
ck('dynamic energy drift medium-to-fine refinement',3.8<runs[1]['max_dynamic_energy_drift']/runs[2]['max_dynamic_energy_drift']<4.2)
grid=math.sqrt(float(dx*np.sum((finals[(64,.0025)]-finals[(128,.0025)][::2])**2)))
ck('grid refinement density agreement',grid<1e-6)
x,dx,k,_=build(64);uniform=np.column_stack([np.full(64,math.sqrt((1-pop)/L)),np.full(64,math.sqrt(pop/L))]).astype(complex)
rho,phi=field(uniform,dx,k,1.)
ck('uniform mean-subtracted potential zero',np.max(abs(phi))<1e-12)
ck('uniform limit stationary',np.linalg.norm(step(uniform,dx,k,1.,.1)-uniform)<1e-12)
clock=json.loads((R/'source/clock_0_5.json').read_text())
out={'version':'bridge-0.7-r1','scope':'dimensionless nonrelativistic periodic effective field/state feedback; not fully covariant gravity','inputs':{'L_dimensionless':L,'coupling_lambda':coupling,'population_from_0_2':pop,'two_component_initial_profiles':'externally chosen periodic gaussians; excited component one momentum winding','source':'transported occupancy density; equal source weight of internal components','zero_mode':'subtract mean density; periodic zero-average potential','energy_rule':'kinetic + half density*potential; constant internal/rest offsets excluded from drift test','continuity_rule':'drho in discrete test denotes cell mass derivative d(dx*rho_i)/ds; J is antisymmetric spectral lattice current'},'runs':runs,'convergence':{'coarse_time_L2':coarse,'fine_time_L2':fine,'ratio':coarse/fine,'grid_L2':grid},'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'clock_interface':'s=omega*tau may be assigned using 0.5 external rate; coefficients and length are dimensionless construction inputs, not derived SI G calibration','open':['covariant stress-energy and metric evolution','SI length/mass/G calibration of feedback','excitation contributions to gravitational source','time-dependent preparation and record/controller coupling','physical reservoir and durable records'],'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'source').glob('*'))}}
(R/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'failed':out['failed'],'convergence':out['convergence'],'energy_drifts':[x['max_dynamic_energy_drift'] for x in runs]},indent=2))
if out['failed']:raise SystemExit(1)
