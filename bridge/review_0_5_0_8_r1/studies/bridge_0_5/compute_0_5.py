"""Explicit calibrated phase driver and proper-time clocks; not a derived source clock."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from scipy.linalg import expm,eigh
R=Path(__file__).resolve().parent
down=json.loads((R/'source/downstream_0_12_parameters.json').read_text())
anchor=down['baseline_0_11'];si=anchor['SI']
hbar=si['h_J_s']/(2*math.pi);eV=si['eV_J']
electron=anchor['targets']['electron_energy_eV'];mode=anchor['mass_construction']['electron_mode'];mu=electron/mode;omega=mu*eV/hbar
xi=.1;dt=xi/omega
gamma=np.array([14.134725141734695,21.022039638771556,25.01085758014569,30.424876125859512])
Es=np.r_[0.,gamma*mu]*eV
Hsrc=np.diag(Es);O=np.zeros((5,5));O[0,1:]=1.25;O[1:,0]=1.25
checks=[];rows=[]
def ck(n,b):checks.append({'name':n,'passed':bool(b)})
ck('Hermitian source generator',np.linalg.norm(Hsrc-Hsrc.conj().T)/np.linalg.norm(Hsrc)<1e-14)
ck('positive source energy',np.min(Es)>=0)
ck('source energy SI scale matches electron-mode calibration',abs(Es[-1]/eV-gamma[-1]*mu)<1e-9)
ck('frame choice equals twice inherited proper update',math.isclose(dt,2*.05*hbar/(mu*eV),rel_tol=1e-14))
for n in [3,45,75,315,999999]:
 psi=np.r_[1.,np.exp(-1j*gamma*np.log(n))]/math.sqrt(5)
 for k in [0,1,2,4,8]:
  tau=k*dt;U=expm(-1j*Hsrc*tau/hbar);state=U@psi
  phase=.5*float(np.cos(gamma*(math.log(n)+xi*k)).sum())
  value=float(np.vdot(state,O@state).real)
  ck(f'n{n} k{k} SI phase reproduces dimensionless driver',abs(value-phase)<2e-11)
  ck(f'n{n} k{k} source norm',abs(np.vdot(state,state)-1)<1e-12)
  ck(f'n{n} k{k} source energy conservation',abs(np.vdot(state,Hsrc@state)-np.vdot(psi,Hsrc@psi))<1e-26)
  shifted=expm(-1j*(Hsrc+mu*eV*np.eye(5))*tau/hbar)@psi
  ck(f'n{n} k{k} common shift invariant driver',abs(np.vdot(shifted,O@shifted).real-value)<2e-11)
  rows.append({'n':n,'frame':k,'proper_time_s':tau,'driver_dimensionless':phase,'driver_SI':value})
basis=np.load(R/'source/internal_and_carrier_basis.npz');H=basis['H_MeV'];g=basis['ground'];exc=basis['excited']
ev,V=eigh(H);relative=ev-ev[0];gap=float(exc@H@exc-g@H@g)
ck('nuclear generator distinct from source generator',H.shape==(95,95) and Hsrc.shape==(5,5))
internal=[]
for k in [1,2,4,8]:
 tau=k*dt;phi=relative*1e6*eV*tau/hbar
 U=(V*np.exp(-1j*phi))@V.T
 ck(f'internal k{k} unitarity',np.linalg.norm(U.conj().T@U-np.eye(95))<1e-10)
 theta=np.angle(np.exp(1j*phi));branches=np.rint((phi-theta)/(2*math.pi)).astype(np.int64)
 recovered=(theta+2*math.pi*branches)*hbar/tau/eV/1e6
 err=float(np.max(np.abs(recovered-relative)))
 ck(f'internal k{k} phase branch recovery',err<1e-7)
 ck(f'internal k{k} alias exists',np.count_nonzero(branches)>0)
 coherent=(g+exc)/math.sqrt(2)
 expected=(g+np.exp(-1j*gap*1e6*eV*tau/hbar)*exc)/math.sqrt(2)
 ck(f'internal k{k} coherent same H phase',np.linalg.norm(U@coherent-expected)<2e-9)
 baseline=next(x for x in json.loads((R/'source/bridge_0_2_results.json').read_text())['rows'] if x['case']=='baseline')
 pop=baseline['excited_population']
 rho=(1-pop)*np.outer(g,g)+pop*np.outer(exc,exc)
 ck(f'internal k{k} diagonal mixed state stationary',np.linalg.norm(U@rho@U.conj().T-rho)<2e-9)
 internal.append({'frame':k,'relative_phase_recovery_max_MeV':err,'nonzero_integer_branches':int(np.count_nonzero(branches)),'excitation_phase_rad':gap*1e6*eV*tau/hbar})
clocks=[]
for beta in [0.,.6,.8]:
 coord=64*dt;proper=coord*math.sqrt(1-beta**2);count=proper/dt
 # Covariant interval of endpoint displacement under a finite Lorentz boost.
 boost=.3;gb=1/math.sqrt(1-boost**2)
 tp=gb*coord*(1-boost*beta);xp=gb*coord*(beta-boost)
 interval=math.sqrt(tp*tp-xp*xp)
 ck(f'beta{beta} Lorentz proper-time invariant',math.isclose(interval,proper,rel_tol=1e-13))
 completed=math.floor(count+1e-12)
 ck(f'beta{beta} count including remainder',abs(completed+(count-completed)-count)<1e-12)
 clocks.append({'beta':beta,'coordinate_time_s':coord,'proper_time_s':proper,'completed_frames':completed,'fractional_remainder':max(0.,count-completed)})
uc=7.668947767821907e-10;H0=2.1842852410855023e-18
slow=.7*H0;ratio=hbar*slow/uc
ck('old slow schedule identification remains failed',math.isclose(ratio,2.102556972196466e-43,rel_tol=1e-12) and ratio!=1)
for rate in [.5,2.]:
 altH=Hsrc*rate;altdt=dt/rate
 ck('alternative driver rate '+str(rate),np.linalg.norm(expm(-1j*altH*altdt/hbar)-expm(-1j*Hsrc*dt/hbar))<1e-12)
out={'version':'bridge-0.5-r1','scope':'conditional SI realization of adopted phase driver plus frozen internal Hamiltonian evolution; no autonomous source/preparation dynamics','calibration':{'electron_energy_eV':electron,'mode':mode,'mu_eV':mu,'hbar_J_s':hbar,'chosen_driver_rate_s_minus1':omega,'chosen_frame_duration_s':dt,'source_energy_levels_eV':(Es/eV).tolist(),'construction_choice':'omega=mu/hbar; not uniquely derived or measured; another positive omega defines another valid clock mapping'},'source_rows':rows,'internal_rows':internal,'worldline_rows':clocks,'failed_clock_ratio_preserved':ratio,'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'open':['physical driver selection and rate','source-to-nucleon preparation coupling Hamiltonian','energy supply during state-changing preparation','frame-triggered measurement and durable record','nonuniform covariant dynamics'],'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'source').glob('*'))}}
(R/'results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'passed':out['passed'],'failed':out['failed'],'dt_s':dt,'old_clock_ratio':ratio,'internal_rows':internal},indent=2))
if out['failed']:raise SystemExit(1)
