"""Wonsik Reality-Renderer Architecture: local stiffness-weighted twist witness.
Native quadratic storage -> dimensional sigma -> explicit traction contract.
Includes an ADOPTED/CREDITED QUMOND-type 3D receiver, not derived full GR.
"""
from pathlib import Path
import numpy as np,math,json,csv,hashlib
from numpy.polynomial.legendre import leggauss
P=Path(__file__).resolve().parent
G=6.6743e-11;C=299792458.;PC=30856775814913670.;MSUN=1.98847e30
checks={}
def check(k,v):
 checks[k]=bool(v)
 if not v:raise AssertionError(k)
def writecsv(name,rows):
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def rms(a):return float(np.sqrt(np.mean(abs(a)**2)))
def nu(y):
 y=np.asarray(y);return 1/(-np.expm1(-np.sqrt(y)))
def source_field(x,y,z):
 A=.2;E=[.45,.20,.10]
 return [E[0]+A*(np.sin(x)+.1*np.sin(x+y)),E[1]+A*(.6*np.sin(y)+.1*np.sin(x+y)),E[2]+A*.3*np.sin(z)]
def loop_twist():
 # Dimensionless connection w=sqrt(|gN|) * gN/|gN|, then physical omega=omegaD*w.
 def vector(x,y,z):
  v=np.array(np.broadcast_arrays(*source_field(x,y,z)));mag=np.sqrt(np.sum(v*v,axis=0));return v/np.sqrt(mag)
 z0=np.pi/3;xl=.2*np.pi;xr=.7*np.pi;yl=.1*np.pi;yr=.6*np.pi
 q,w=leggauss(160);xs=(q+1)*(xr-xl)/2+xl;ys=(q+1)*(yr-yl)/2+yl
 line=(xr-xl)/2*np.dot(w,vector(xs,yl,z0)[0]-vector(xs,yr,z0)[0])+(yr-yl)/2*np.dot(w,vector(xr,ys,z0)[1]-vector(xl,ys,z0)[1])
 x=xs[:,None];y=ys[None,:];v=np.array(np.broadcast_arrays(*source_field(x,y,z0)));mag=np.sqrt(np.sum(v*v,axis=0))
 A=.2;cx=A*.1*np.cos(x+y)
 vx=np.array(np.broadcast_arrays(A*np.cos(x)+cx,cx,np.zeros_like(x+y)))
 vy=np.array(np.broadcast_arrays(cx,A*.6*np.cos(y)+cx,np.zeros_like(x+y)))
 curlz=-.5*mag**(-2.5)*(v[1]*np.sum(v*vx,axis=0)-v[0]*np.sum(v*vy,axis=0))
 area=(xr-xl)*(yr-yl)/4*np.einsum('i,ij,j->',w,curlz,w)
 return float(line),float(area)
def main():
 for fn,meta in json.loads((P/'input_manifest.json').read_text()).items():check('hash_'+fn,hashlib.sha256((P/'inputs'/fn).read_bytes()).hexdigest()==meta['sha256'])
 orig=json.loads((P/'inputs/shared_gravity_results.json').read_text());cases=orig['cases'];ref=next(v for v in cases if v['carrier_state']=='product' and v['epsilon']==0 and v['a']==1)
 aT=ref['aT_m_s2'];uD=ref['sector_density_J_m3'][1];L0=C*C/(4*math.sqrt(3)*aT);omegaD=1/L0;column=uD/aT
 check('native_load_scale_identity',abs(uD/(3*aT*aT/(np.pi*G))-1)<2e-15)
 check('weighted_twist_normalization',abs((C**4*omegaD**2/(16*np.pi*G))/uD-1)<2e-15)
 # sigma = L0 sqrt(zeta) |kappa|; absolute stiffness and twist remain degenerate.
 yvalues=np.geomspace(1e-12,1e4,161);sigma=np.sqrt(yvalues);omega=omegaD*sigma;u=C**4*omega**2/(16*np.pi*G)
 check('dimensional_capacity',np.max(abs(u/uD/yvalues-1))<1e-15)
 check('traction_capacity',np.max(abs(u/(column*aT*yvalues)-1))<1e-15)
 # Minimum storage energy with a prescribed normal traction demand; smaller
 # amplitude violates coverage, larger amplitude has strictly higher energy.
 check('minimum_traction_infeasible_below',np.all(C**4*(.99*omega)**2/(16*np.pi*G)<column*aT*yvalues))
 check('minimum_traction_cost_above',np.all(C**4*(1.01*omega)**2/(16*np.pi*G)>u))
 for zeta in [.01,1.,100.]:
  kappa=omega/math.sqrt(zeta)
  check('stiffness_degeneracy_'+str(zeta),np.max(abs(L0*np.sqrt(zeta)*kappa/sigma-1))<1e-15)
 # Countertwist balance preserves squared magnitude and the same normal stress.
 directions=np.eye(3);n=np.array([1.,2.,3.]);n/=np.linalg.norm(n)
 for i,chi in enumerate(np.linspace(-1,1,9)):
  plus=omegaD*math.sqrt((1+chi)/2)*n;minus=-omegaD*math.sqrt((1-chi)/2)*n
  norm=float(plus@plus+minus@minus);S=C**4/(16*np.pi*G)*(2*(np.outer(plus,plus)+np.outer(minus,minus))-norm*np.eye(3))
  check('countertwist_energy_'+str(i),abs(norm/omegaD**2-1)<1e-15)
  check('normal_traction_'+str(i),abs(n@S@n/uD-1)<1e-15)
 # Isotropic average of this SIMPLE fixed-covector stress is -u/3, not dust.
 Smean=sum((2*np.outer(v,v)-np.eye(3)) for v in directions)/3
 check('bare_quadratic_stress_not_dust',np.max(abs(Smean+np.eye(3)/3))<1e-15)
 # Frozen spherical point: do not equate stored field energy/c^2 with effective mass.
 M=6e10*MSUN;scale=3000*PC;r=8200*PC
 gb=G*M*r/(r*r+scale*scale)**1.5;dgb=G*M*(scale*scale-2*r*r)/(r*r+scale*scale)**2.5
 yy=gb/aT;ss=math.sqrt(yy);mu=-math.expm1(-ss);nn=1/mu;dn=-math.exp(-ss)/(2*ss*mu*mu)
 g=gb*nn;dg=dgb*(nn+yy*dn);rhob=3*M*scale*scale/(4*np.pi*(r*r+scale*scale)**2.5)
 rhoeff=(2*g/r+dg)/(4*np.pi*G)-rhob;stored=uD*yy;bare=stored/C**2;ratio=rhoeff/bare
 check('native_rotation_still_matches',abs(math.sqrt(r*g)/1000-ref['rotation_km_s'])<1e-10)
 check('bare_energy_not_effective_mass',ratio>1e4)
 # 3D periodic contrasting density (positive background can be added) with
 # declared harmonic external field. Coordinates are angles, side length 16 kpc.
 rows=[];probevals=[];last=None
 for N in [32,64,128]:
  a=np.arange(N)*2*np.pi/N;x,y,z=np.meshgrid(a,a,a,indexing='ij',sparse=True)
  vs=source_field(x,y,z);v=np.array(np.broadcast_arrays(*vs));mag=np.sqrt(np.sum(v*v,axis=0));raw=v*nu(mag)
  ks=np.fft.fftfreq(N,d=1/N);kk=np.meshgrid(ks,ks,ks,indexing='ij',sparse=True);k2=sum(q*q for q in kk)
  rf=np.fft.fftn(raw,axes=(1,2,3))
  # A real even-N Fourier derivative has ambiguous Nyquist modes. Admit the
  # band excluding Nyquist planes before the Hodge solve and record its loss.
  unfiltered=raw.copy();rf[:,N//2,:,:]=0;rf[:,:,N//2,:]=0;rf[:,:,:,N//2]=0
  raw=np.fft.ifftn(rf,axes=(1,2,3)).real;bandloss=rms(unfiltered-raw)/rms(unfiltered)
  check('3D_admitted_band_'+str(N),bandloss<1e-4)
  dot=sum(kk[j]*rf[j] for j in range(3))
  projected=[]
  for j in range(3):
   f=np.divide(kk[j]*dot,k2,out=np.zeros_like(dot),where=k2>0);f[0,0,0]=rf[j,0,0,0]
   projected.append(np.fft.ifftn(f).real)
  projected=np.array(projected);pf=np.fft.fftn(projected,axes=(1,2,3))
  def divf(ff):return sum(1j*kk[j]*ff[j] for j in range(3))
  def curlf(ff):return np.array([1j*(kk[1]*ff[2]-kk[2]*ff[1]),1j*(kk[2]*ff[0]-kk[0]*ff[2]),1j*(kk[0]*ff[1]-kk[1]*ff[0])])
  curlraw=np.fft.ifftn(curlf(rf),axes=(1,2,3)).real;curlout=np.fft.ifftn(curlf(pf),axes=(1,2,3)).real
  divraw=np.fft.ifftn(divf(rf)).real;divout=np.fft.ifftn(divf(pf)).real
  diverr=rms(divout-divraw)/rms(divraw);curlratio=rms(curlout)/max(rms(curlraw),1e-30)
  correction=rms(projected-raw)/rms(raw)
  # Fourier longitudinal projection conserves the zero/harmonic mode by convention.
  meanerr=float(max(abs(projected.mean((1,2,3))-raw.mean((1,2,3)))))
  orth=float(abs(np.mean(projected*(raw-projected))))/max(float(np.mean(raw*raw)),1e-30)
  check('3D_divergence_'+str(N),diverr<2e-12);check('3D_curl_free_'+str(N),curlratio<2e-11)
  check('3D_correction_needed_'+str(N),correction>1e-4)
  check('3D_harmonic_'+str(N),meanerr<1e-14);check('3D_orthogonal_'+str(N),orth<1e-12)
  # Newtonian source contrast and its positive reference density are explicit.
  contrast=.2*(np.cos(x)+.6*np.cos(y)+.3*np.cos(z)+.2*np.cos(x+y))
  check('3D_positive_reference_density_'+str(N),float(np.min(2+contrast))>0)
  # Signed periodic source is mean-subtracted; not an isolated galactic mass fit.
  density_error=rms(np.fft.ifftn(divf(np.fft.fftn(v,axes=(1,2,3)))).real-contrast)/rms(contrast)
  check('3D_native_Newtonian_source_'+str(N),density_error<1e-12)
  probes=[float(projected[j,N//8,N//4,3*N//8]) for j in range(3)];probevals.append(probes)
  rows.append(dict(n=N,Nyquist_plane_relative_loss=bandloss,min_Newton_field_over_aT=float(mag.min()),raw_curl_RMS=rms(curlraw),curl_free_output_RMS=rms(curlout),divergence_relative_error=diverr,transverse_correction_fraction=correction,orthogonality_residual=orth,Newtonian_density_relative_error=density_error,probe_x=probes[0],probe_y=probes[1],probe_z=probes[2]))
  last=dict(v=v,raw=raw,projected=projected,mag=mag)
 check('3D_resolution_convergence',max(abs(np.array(probevals[-1])-np.array(probevals[-2])))<1e-8)
 # One loop of the weighted connection: Stokes matches nonzero circulation.
 line,area=loop_twist();Lbox=16000*PC;phase=omegaD*Lbox/(2*np.pi)*line
 check('connection_Stokes',abs(line-area)<1e-12)
 check('connection_not_single_global_phase_gradient',abs(line)>1e-5)
 # A literal per-shutter-angle identification fails: sigma is a normalized rate.
 edge=299792458.*1.481301966415863e-21;edgephase=omegaD*ss*edge
 check('sigma_not_microscopic_edge_angle',abs(edgephase/ss)<1e-30)
 # Save one central plane for review and independent Hodge checks.
 n=last['v'].shape[1];plane=n//4
 np.savez_compressed(P/'3D_plane.npz',Newtonian=last['v'][:,:, :,plane],raw=last['raw'][:,:,:,plane],projected=last['projected'][:,:,:,plane],field_magnitude=last['mag'][:,:,plane])
 writecsv('three_dimensional_receiver.csv',rows)
 writecsv('dimensional_twist.csv',[dict(baryon_over_aT=yy,exposure=s,weighted_twist_m_inv=o,stored_twist_J_m3=uu) for yy,s,o,uu in zip(yvalues,sigma,omega,u)])
 result={'framework_name':'Wonsik Reality–Renderer Architecture','version':'local-twist-load v0.3','date':'2026-10-21',
 'assessment':{'inputs':'Native book quadratic twist energy, shared D energy/aT state, frozen v0.2 RAR gate; explicit positive periodic density contrast and harmonic field','WRRA_transformation':'stiffness-weighted twist -> sigma^2=u_twist/uD -> NEW source-traction coverage -> minimum energy -> frozen admission gate; separately adopted QUMOND-type 3D curl-free receiver','outputs':'Dimensionally explicit twist/traction, native rotation, countertwist invariance, 3D receiver projection and nonzero connection circulation','falsification':'Energy/dimensional/traction mismatch, wrong source versus total field, literal micro-angle or mass equivalence, lost div/curl conditions, nonconvergence or source double-counting'},
 'normalization':{'uD_J_m3':uD,'aT_m_s2':aT,'weighted_reference_twist_m_inv':omegaD,'normalization_length_m':L0,'reference_column_kg_m2':column,'definition':'omega=sqrt(zeta)*kappa_total; sigma=L0*omega; L0 is normalization, not universe size or causal communication length'},
 'reference_local':{'baryon_over_aT':yy,'sigma':ss,'weighted_twist_m_inv':omegaD*ss,'stored_twist_J_m3':stored,'bare_energy_mass_density_kg_m3':bare,'effective_residual_density_kg_m3':rhoeff,'effective_to_bare_density_ratio':ratio,'rotation_km_s':math.sqrt(r*g)/1000,'weighted_shutter_edge_angle_rad':edgephase},
 'three_dimensional':rows,'loop':{'dimensionless_line_integral':line,'dimensionless_surface_integral':area,'weighted_holonomy_for_16kpc_box':phase},
 'new_assumptions':['Normal load-bearing sheet/port traction is at least Sigma_star*g_N; g_N is the auxiliary source field, not measured total g','Use the original quadratic storage as local norm; stiffness and absolute kappa are not separately inferred','Use a credited QUMOND-type auxiliary-field receiver as a separate nonrelativistic 3D candidate; not identical to AQUAL outside spherical symmetry','Harmonic field is prescribed; projected output retains the algebraic mean as a stated periodic boundary convention'],
 'scope':'A conditional dimensional/traction and 3D geometry bridge. Not a unique microscopic strain law, physical sheet derivation, bare energy=rho_eff*c^2, dust pressure derivation, full GR/causal metric dynamics, or new isolated-galaxy observational fit.',
 'checks':checks,'passed':sum(checks.values()),'total':len(checks)}
 (P/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['normalization','reference_local','three_dimensional','loop','passed','total']},indent=2))
if __name__=='__main__':main()
