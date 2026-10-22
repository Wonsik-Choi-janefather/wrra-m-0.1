"""Finite-resolution bridge for Wonsik Reality–Renderer Architecture.

numpy-only scientific calculation; no network, fit, or infinite physical grid.
Run python compute.py. The adopted finite-periodic geometry and weak-field
Poisson receiver are declared witnesses, not a derivation of full GR.
"""
from pathlib import Path
import hashlib,json,csv,math
import numpy as np
P=Path(__file__).resolve().parent
checks={}
def check(name,value):
 checks[name]=bool(value)
 if not value:raise AssertionError(name)
def writecsv(name,rows):
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def kernel(N):
 x=np.arange(N)/N;r=np.arange(30);K=np.ones((30,N))
 for p in (2,3,5):
  theta=(r%p)[:,None]/p-x[None,:]
  D=np.exp(2j*np.pi*theta[:,:,None]*np.arange(p)[None,None,:]).mean(2)
  K*=abs(1-D)**2
 return K/K.mean(1)[:,None]
def avg(a,b):return a.reshape(a.shape[:-1]+(-1,b)).mean(-1)
def rms(a):return float(np.sqrt(np.mean(abs(a)**2)))
def lap(u,h):return sum((np.roll(u,1,a)-2*u+np.roll(u,-1,a))/h**2 for a in range(u.ndim))
def main():
 manifest=json.loads((P/'inputs_manifest.json').read_text())
 for fn,sha in manifest['files'].items():check('input_hash_'+fn,hashlib.sha256((P/fn).read_bytes()).hexdigest()==sha)
 inp=json.loads((P/'payloads.json').read_text());N=1024;K=kernel(N);out=[];source_rows=[];source_receiver=[];spectral_rows=[]
 eta=np.array([7.5615824991e-10,7.2857613288e-10,7.6461028188e-10]);eps=1e-8;gap=2*math.cos(math.pi/8)
 frozen=np.load(P/'reference_profiles.npz')
 for branch in ['weighted','unweighted']:
  B=np.array(inp[branch]);S=np.einsum('srj,rx->sx',B,K);I=S.sum(0)
  check(branch+'_frozen_sector_replay',np.max(abs(S-frozen[branch+'_sector_profiles']))<2e-14)
  controlled=B[:,np.arange(30)%3!=0,:].sum(2)
  du=eps*eta[:,None]*gap*(controlled@K[np.arange(30)%3!=0,:]-controlled.sum(1)[:,None]);du[0]=0
  u0=eta*S.mean(1);u=u0[:,None]+du;pressure=-u[2]
  check(branch+'_positive_energy',u.min()>0)
  coeff=np.fft.fft(du.sum(0))/N
  check(branch+'_seven_mode_support',max(abs(coeff[8:N-7]))<1e-30)
  # Compare original source/supply result, not information shape as mass.
  density_rms=rms(du.sum(0)/u0.sum())
  source_rows.append(dict(branch=branch,density_relative_rms=density_rms,information_relative_rms=rms(I/I.mean()-1),max_density_contrast=float(max(abs(du.sum(0)/u0.sum())))))
  for b in [1,2,4,8,16,32,64,128]:
   Ic=avg(I,b);uc=avg(u,b);pc=avg(pressure,b);Ncoarse=N//b
   # Cell-volume weighted sector integrals are conserved independently.
   balance=float(max(abs(uc.mean(-1)-u.mean(-1))))/float(max(u0))
   check(branch+f'_sector_integrals_b{b}',balance<1e-14)
   check(branch+f'_pressure_ownership_b{b}',np.max(abs(pc+uc[2]))<1e-25)
   check(branch+f'_positive_b{b}',uc.min()>0 and Ic.min()>0)
   # Exact Fourier transfer of point-sample box averaging, before aliasing.
   F=np.fft.fft(I)/N;Fc=np.fft.fft(Ic)/Ncoarse
   err=[]
   for m in range(1,min(8,(Ncoarse+1)//2)):
    H=np.mean(np.exp(2j*np.pi*m*np.arange(b)/N))
    err.append(abs(Fc[m]-H*F[m])/I.mean())
   banderr=max(err,default=0.)
   # For Ncoarse=8, modes above coarse Nyquist alias: use only resolved modes
   # if their aliased partners are absent. Detect, do not silently accept them.
   alias_safe=Ncoarse>14
   if alias_safe:check(branch+f'_box_transfer_b{b}',banderr<1e-13)
   out.append(dict(branch=branch,block=b,coarse_cells=Ncoarse,sector_integral_relative_error=balance,
     info_relative_rms=rms(Ic/Ic.mean()-1),box_transfer_error=banderr,alias_free_for_original_7_modes=alias_safe))
  # Apply a declared 1D weak-field receiver to the ACTUAL frozen supply.
  # Unit period, 4*pi*G*rho0=1: no physical length calibration is inferred.
  contrast=du.sum(0)/u0.sum();fk=np.fft.fft(contrast)
  k=2*np.pi*np.fft.fftfreq(N,d=1/N)
  pref=np.fft.ifft(np.divide(-fk,k*k,out=np.zeros_like(fk),where=k!=0)).real
  for b in [1,2,4,8,16,32,64]:
   nc=N//b;hc=1/nc;rc=avg(contrast,b)
   kc=2*np.pi*np.fft.fftfreq(nc,d=hc)
   lam=4*np.sin(kc*hc/2)**2/hc**2
   pc=np.fft.ifft(np.divide(-np.fft.fft(rc),lam,out=np.zeros(nc,dtype=complex),where=lam>0)).real
   pe=rms(pc-avg(pref,b))/rms(avg(pref,b))
   residual=rms(lap(pc,hc)-rc)/rms(rc)
   check(branch+f'_actual_source_poisson_residual_{nc}',residual<3e-10)
   A=(hc*2*np.pi*7)**2/12
   bound=A/(1-A) if A<1 else None
   if bound is not None:check(branch+f'_actual_source_poisson_bound_{nc}',pe<=bound*(1+1e-9))
   source_receiver.append(dict(branch=branch,coarse_cells=nc,potential_relative_L2=pe,relative_stencil_residual=residual,worst_band_bound=bound))
   # Execute inherited positive-frequency spectral flow and compare block maps.
   # Common unit period and c=1; retained modes 0..7 have no coarse alias.
   t=.137
   psi=I.astype(complex);evolved=np.fft.ifft(np.fft.fft(psi)*np.exp(-1j*abs(k)*t))
   coarse_evolved=np.fft.ifft(np.fft.fft(avg(psi,b))*np.exp(-1j*abs(kc)*t))
   comm=rms(avg(evolved,b)-coarse_evolved)/rms(psi)
   normerr=abs(rms(evolved)/rms(psi)-1)
   check(branch+f'_spectral_coarse_commutation_{nc}',comm<1e-13)
   check(branch+f'_spectral_norm_{nc}',normerr<1e-13)
   spectral_rows.append(dict(branch=branch,coarse_cells=nc,time_unit_period_over_c=t,commutation_relative_L2=comm,norm_relative_error=normerr))
  # Telescoping finite-volume flux balance, for a declared test flux.
  x=np.arange(N)/N;J=np.sin(2*np.pi*x)+.2*np.cos(14*np.pi*x);dI=-(J-np.roll(J,1))*N
  for b in [2,8,32,64]:
   Jc=J[b-1::b];rhs=-(Jc-np.roll(Jc,1))*(N//b)
   check(branch+f'_finite_volume_flux_b{b}',max(abs(avg(dI,b)-rhs))<2e-12)
  # Subcell covariance: deleting it loses a nonlinear stress even with same mean.
  rho=I/I.mean();vel=np.sin(6*np.pi*x)+.3*np.cos(10*np.pi*x)
  tau=avg(rho*vel,32)-avg(rho,32)*avg(vel,32)
  check(branch+'_nonlinear_closure_loss_detected',max(abs(tau))>1e-5)
 # Constant fields are exact zero modes; positivity of -L follows summation by parts.
 rng=np.random.default_rng(20261021);u=rng.normal(size=(16,16,16));h=1/16
 q=-float(np.mean(u*lap(u,h)));edge=sum(float(np.mean(((np.roll(u,-1,a)-u)/h)**2)) for a in range(3))
 check('discrete_energy_identity',abs(q-edge)/edge<2e-15)
 check('laplacian_constant_nullspace',np.max(abs(lap(np.ones_like(u),h)))==0)
 # Numerical refinement of a fixed unit-periodic receiver: geometry is not SOURCE count.
 rows=[];modes=[((1,0,0),.05,'sin'),((1,2,0),.025,'cos'),((1,1,1),.01,'sin')]
 for n in [16,32,64,128]:
  h=1/n;v=np.arange(n)/n;xyz=np.meshgrid(v,v,v,indexing='ij',sparse=True)
  rho=np.zeros((n,n,n));phi_ref=np.zeros_like(rho);gref=[np.zeros_like(rho) for _ in range(3)]
  for m,a,kind in modes:
   phase=2*np.pi*sum(m[i]*xyz[i] for i in range(3));k2=(2*np.pi)**2*sum(j*j for j in m)
   f=np.sin(phase) if kind=='sin' else np.cos(phase);df=np.cos(phase) if kind=='sin' else -np.sin(phase)
   rho+=a*f;phi_ref-=a*f/k2
   for axis in range(3):gref[axis]+=a*2*np.pi*m[axis]*df/k2
  q=2*np.pi*np.fft.fftfreq(n);lambda_h=sum(4*np.sin(q.reshape(tuple(n if j==a else 1 for j in range(3)))/2)**2/h**2 for a in range(3))
  rhok=np.fft.fftn(rho);phik=np.divide(-rhok,lambda_h,out=np.zeros_like(rhok),where=lambda_h>0);phi=np.fft.ifftn(phik).real
  check(f'poisson_stencil_residual_{n}',rms(lap(phi,h)-rho)/rms(rho)<3e-12)
  g=[-(np.roll(phi,-1,a)-np.roll(phi,1,a))/(2*h) for a in range(3)]
  # Face force plus matching divergence checks Gauss law; center force differs.
  edgeg=[-(np.roll(phi,-1,a)-phi)/h for a in range(3)]
  div=sum((edgeg[a]-np.roll(edgeg[a],1,a))/h for a in range(3))
  check(f'discrete_gauss_{n}',rms(div+rho)/rms(rho)<3e-12)
  pe=rms(phi-phi_ref)/rms(phi_ref);ge=math.sqrt(sum(np.mean((g[a]-gref[a])**2) for a in range(3))/sum(np.mean(x*x) for x in gref))
  # Independent, analytical modal wave/Poisson dispersion bounds.
  errors=[];phaseerrors=[];bounds=[];exact_phase=[]
  for m,_,_ in modes:
   k=2*np.pi*np.array(m);lam=float(sum(4*np.sin(k*h/2)**2/h**2));k2=float(k@k);A=h*h*k2/12
   errors.append(1-lam/k2);phaseerrors.append(1-math.sqrt(lam/k2));bounds.append(A)
   check(f'laplacian_bound_{n}_{m}',0<=errors[-1]<=A*(1+1e-12))
   check(f'potential_bound_{n}_{m}',k2/lam-1<=A/(1-A)*(1+1e-12))
   # Finite grid spectral interpolation preserves retained modes exactly.
   exact_phase.append(abs(np.exp(-1j*.1*np.linalg.norm(k))-np.exp(-1j*.1*math.sqrt(k2))))
  rows.append(dict(n=n,h=h,poisson_relative_L2=pe,center_force_relative_L2=ge,max_laplacian_relative_error=max(errors),max_phase_speed_error=max(phaseerrors),max_bound=max(bounds),spectral_reference_phase_error=max(exact_phase)))
 # The observed order is measured, not assumed by a regression imposed in advance.
 for i in range(1,len(rows)):
  for name in ['poisson_relative_L2','center_force_relative_L2']:
   order=math.log(rows[i-1][name]/rows[i][name],2);rows[i]['order_'+name]=order
   check(f'convergence_{name}_{rows[i]["n"]}',1.8<order<2.2)
 for name in ['order_poisson_relative_L2','order_center_force_relative_L2']:rows[0][name]=''
 # Aliasing is explicitly detected: a high mode is identical after raw decimation.
 N=1024;b=32;nc=N//b;x=np.arange(N)/N
 low=np.cos(2*np.pi*3*x);high=np.cos(2*np.pi*(nc+3)*x)
 alias=rms(low[::b]-high[::b]);filtered_distance=rms(avg(low,b)-avg(high,b))
 check('raw_decimation_alias_detected',alias<1e-13 and filtered_distance>.1)
 # A constant contrast does not vanish merely by changing the length unit.
 x_stretched=1e12*x; unchanged=np.cos(2*np.pi*3*x_stretched/1e12)
 check('length_rescaling_not_smoothing',rms(unchanged-low)<1e-13 and source_rows[0]['information_relative_rms']>.1)
 # Unit one-hop CFL cannot be copied into local 3D leapfrog.
 nyquist_A=3.;growth=abs(1-2*nyquist_A-math.sqrt((1-2*nyquist_A)**2-1))
 check('unit_CFL_3D_negative_control',growth>1)
 bounds={'wave_1percent_min_wavelength_cells':2*np.pi/math.sqrt(12*(2*.01-.01**2)),
  'poisson_1percent_min_wavelength_cells':2*np.pi/math.sqrt(12*.01/1.01)}
 summary={'framework_name':'Wonsik Reality–Renderer Architecture','version':'finite-scale-bridge v0.1','date':'2026-10-21',
  'assessment':{'inputs':'Frozen residue-owned payloads, kernel taps, SI coefficients/epsilon; declared periodic receiver and resolution family','transformation':'Typed block averaging, flux balance and Fourier-map audit; finite-difference weak-field Poisson/transport scaling witness','outputs':'Source-preserving averages, modal error bounds and measured convergence','falsification':'Hash/name/ownership/mean/flux/positivity/bound/convergence failure or alias accepted as a resolved mode'},
  'source_profiles':source_rows,'actual_source_receiver':source_receiver,'spectral_coarse_transport':spectral_rows,'refinement':rows,'scale_bounds':bounds,'controls':{'raw_decimation_alias_L2':alias,'block_average_low_high_distance':filtered_distance,'nonlinear_closure_covariance_max':float(max(abs(tau))),'unit_CFL_3D_highmode_growth_per_step':growth},
  'scope':'Finite-domain conditional coarse-graining and weak-field receiver witness. Not a full GR/SM renormalization or derivation of physical macro scale; original spectral transport remains nonlocal.',
  'checks':checks,'passed':sum(checks.values()),'total':len(checks)}
 writecsv('source_coarse_graining.csv',out);writecsv('refinement.csv',rows);writecsv('actual_source_receiver.csv',source_receiver);writecsv('spectral_coarse_transport.csv',spectral_rows)
 (P/'results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:summary[k] for k in ['framework_name','source_profiles','refinement','scale_bounds','controls','passed','total']},indent=2))
if __name__=='__main__':main()
