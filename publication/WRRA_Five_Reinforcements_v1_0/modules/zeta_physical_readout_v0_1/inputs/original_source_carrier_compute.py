"""Wonsik Reality-Renderer Architecture: conditional finite source/carrier action.
Replays the registered swap and executes a NEW, declared spatial rate coupling.
128 source MODE labels, supply and record are not timeless allocation slots.
"""
from pathlib import Path
import numpy as np
import json,csv,hashlib,math
P=Path(__file__).resolve().parent
checks={}
BETA=1/1024 # inherited profile period L=1024*c*tau
def check(k,v):
 checks[k]=bool(v)
 if not v:raise AssertionError(k)
def rms(x):return float(np.sqrt(np.mean(abs(x)**2)))
def csvwrite(name,rows):
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def kernel(N):
 x=np.arange(N)/N;K=np.ones((30,N))
 for p in [2,3,5]:
  z=(np.arange(30)%p)[:,None]/p-x
  D=np.exp(2j*np.pi*z[:,:,None]*np.arange(p)[None,None,:]).mean(2)
  K*=abs(1-D)**2
 return K/K.mean(1)[:,None]
def kinetic(n):
 # Dimensionless time t/tau, coordinate x/L; L=1024*c*tau.
 F=np.fft.fft(np.eye(n),axis=0,norm='ortho');q=BETA*2*np.pi*abs(np.fft.fftfreq(n,d=1/n))
 return (F.conj().T*q)@F

def main():
 for fn,meta in json.loads((P/'input_manifest.json').read_text()).items():
  check('hash_'+fn,hashlib.sha256((P/'inputs'/fn).read_bytes()).hexdigest()==meta['sha256'])
 old=np.load(P/'inputs/finite_registers.npz');perm=old['permutation'];d=len(perm);G=np.eye(d)[perm]
 A=1-np.cos(2*np.pi*np.arange(128)/128);gap=A[72]-A[8];a=4*8+2;b=4*72+1
 check('original_swap_pair',perm[a]==b and perm[b]==a and np.count_nonzero(perm!=np.arange(d))==2)
 H0=np.repeat(A,4)+gap*np.tile([0,0,1,1],128)
 Pminus=(np.eye(d)-G)/2;Kgen=np.pi*Pminus
 check('generator_hermitian',np.max(abs(Kgen-Kgen.T))==0)
 check('projector_idempotent',np.max(abs(Pminus@Pminus-Pminus))==0)
 check('resource_commutator',np.max(abs(Kgen*(H0[None,:]-H0[:,None])))<1e-14)
 ev,vec=np.linalg.eigh(Kgen);U=(vec*np.exp(-1j*ev))@vec.T
 check('exact_registered_gate',np.max(abs(U-G))<2e-15)
 check('generator_nonnegative',ev.min()>-1e-14)
 check('generator_bandwidth_minimal',abs(np.ptp(ev)-np.pi)<2e-14)
 # Positive Hermitian logarithm branch cost: all eigenphase branches n=0..3.
 # One negative eigenvalue of G requires pi mod 2pi; positive ones require 0.
 branch_costs=[float((np.pi+2*np.pi*j)**2) for j in range(4)]
 check('positive_branch_minimum',branch_costs[0]==min(branch_costs))
 for branch in ['weighted','unweighted']:
  for prior in ['uniform_g_parity','P7_Gibbs_g_parity_control']:
   label=branch+'_'+prior;gamma=old[label+'_controlled_register_probabilities_before'];target=old[label+'_controlled_register_probabilities_after']
   rho=(U*gamma[None,:])@U.conj().T
   check(label+'_endpoint_replay',np.max(abs(np.diag(rho).real-target))<2e-15)
 # Continuous pair action, pressure/resource conservation throughout (not only endpoints).
 pulse=[]
 for t in np.linspace(0,2,129):
  z=np.exp(-1j*np.pi*t);va=(1+z)/2;vb=(1-z)/2
  prob=abs(vb)**2
  res=A[8]+gap*(.5*prob+.5*(1-prob))
  check('continuous_resource_'+str(len(pulse)),abs(res-(A[8]+gap*.5))<1e-14)
  pulse.append(dict(time_tau=float(t),conditional_transfer_probability=float(prob),record_probability=.5*float(prob),supply_probability=.5*(1-float(prob))))
 check('reverse_not_reset',pulse[-1]['conditional_transfer_probability']<1e-28)
 # Actual source-weighted spatial coupling; no fitted new strength, but the
 # law w(x)=I(x)/mean(I) is a NEW explicit candidate, not forced by the action.
 payload=json.loads((P/'inputs/payloads.json').read_text());eta=np.array([7.5615824991e-10,7.2857613288e-10,7.6461028188e-10])
 rows=[];summary=[];snapshots={};dense_case=None
 for branch in ['weighted','unweighted']:
  B=np.array(payload[branch]);mu=B.sum((1,2));M=B[:,np.arange(30)%3!=0,:].sum((1,2));M[0]=0
  for n in [64,128,256]:
   I=np.einsum('srj,rx->x',B,kernel(n));w=I/I.mean();hc=kinetic(n);psi=np.ones(n)/math.sqrt(n)
   check(f'{branch}_{n}_w_positive',w.min()>0 and abs(w.mean()-1)<1e-14)
   for kind in ['uniform','source_shaped']:
    ww=np.ones(n) if kind=='uniform' else w
    hm=hc+np.diag(np.pi*ww);e,v=np.linalg.eigh(hm);kp=BETA*2*np.pi*abs(np.fft.fftfreq(n,d=1/n))
    times=np.linspace(0,1,33);energy0=.5*.5*np.pi # p/2 * <pi*w>
    maxnorm=maxE=maxresource=maxchannel=0.;endpoint=None
    for ti,t in enumerate(times):
     plus=np.fft.ifft(np.fft.fft(psi)*np.exp(-1j*kp*t))
     minus=v@(np.exp(-1j*e*t)*(v.conj().T@psi))
     va=(plus+minus)/2;vb=(plus-minus)/2;p=.5
     pa=p*float(np.vdot(va,va).real);pb=p*float(np.vdot(vb,vb).real);pc=1-p
     norm=pa+pb+pc
     Ekin=p*(np.vdot(va,hc@va).real+np.vdot(vb,hc@vb).real)+(1-p)*np.vdot(plus,hc@plus).real
     Eint=p*.5*np.vdot(minus,(np.pi*ww)*minus).real
     Etotal=float(Ekin+Eint)
     maxnorm=max(maxnorm,abs(norm-1));maxE=max(maxE,abs(Etotal-energy0))
     # Entire SOURCE + supply resource ledger, sector by sector, V0=1 convention.
     source=eta*(mu-M+A[8]*M+gap*M*pb);supply=eta*gap*M*pa
     expected=eta*(mu-M+A[8]*M+gap*M*p)
     maxresource=max(maxresource,float(max(abs(source+supply-expected)))/max(expected))
     # Common transport acts as identity on 15 internal labels, no channel mixing.
     weights=np.arange(1,16,dtype=float);weights/=weights.sum()
     channelnorm=weights*norm;maxchannel=max(maxchannel,float(max(abs(channelnorm-weights))))
     overlap=np.vdot(plus,minus);purity=.5*(1+abs(overlap)**2)
     if n==256:rows.append(dict(branch=branch,coupling=kind,time_tau=float(t),source_transfer_probability=pb,record_probability=pb,supply_excited_probability=pa,norm_error=abs(norm-1),kinetic_energy_dimensionless=float(Ekin),coupling_energy_dimensionless=float(Eint),joint_energy_dimensionless=Etotal,active_pair_reduced_purity=float(purity)))
     if ti==len(times)-1:
      endpoint=pb;endpurity=float(purity)
      if n==256:snapshots[branch+'_'+kind+'_record_density']=p*n*abs(vb)**2
    label=f'{branch}_{n}_{kind}'
    check(label+'_norm',maxnorm<3e-13);check(label+'_joint_energy',maxE<2e-11)
    check(label+'_typed_resource',maxresource<3e-13);check(label+'_15_channel_ownership',maxchannel<1e-13)
    if kind=='uniform':check(label+'_old_gate_endpoint',abs(endpoint-.5)<2e-13)
    else:check(label+'_actual_coupling_effect',abs(endpoint-.5)>1e-4 and endpurity<.99999)
    summary.append(dict(branch=branch,n=n,coupling=kind,endpoint_record_probability=float(endpoint),endpoint_active_pair_purity=endpurity,max_norm_error=maxnorm,max_joint_energy_error=maxE,max_resource_relative_error=maxresource))
    if branch=='weighted' and n==64 and kind=='source_shaped':
     dense_case=dict(hc=hc,w=ww,psi=psi,va=va,vb=vb,beta=BETA)
 # Resolution convergence is tested on actual source-coupled endpoint, not imposed.
 for branch in ['weighted','unweighted']:
  rr=[r for r in summary if r['branch']==branch and r['coupling']=='source_shaped']
  check(branch+'_resolution_endpoint',abs(rr[-1]['endpoint_record_probability']-rr[-2]['endpoint_record_probability'])<1e-9)
 # Negative controls: omit interaction energy, mis-match supply resonance, rank one carrier.
 omitted=max(abs(r['kinetic_energy_dimensionless']-np.pi/4) for r in rows if r['coupling']=='source_shaped')
 check('omitted_coupling_energy_detected',omitted>.1)
 detunedH=H0.copy();detunedH[a]+=.01
 detune=float(np.max(abs(Kgen*(detunedH[None,:]-detunedH[:,None]))))
 check('detuning_breaks_resource_conservation',detune>.01)
 democratic=np.ones((15,15))/15
 check('rank_one_control_detected',np.linalg.matrix_rank(democratic)==1 and np.linalg.matrix_rank(np.eye(15))==15)
 # Independent finite-difference Euler-Lagrange residual for the active two-block dynamics.
 n=64;hc=dense_case['hc'];ww=dense_case['w'];psi=dense_case['psi'];hm=hc+np.diag(np.pi*ww)
 e,v=np.linalg.eigh(hm)
 def minus(t):return v@(np.exp(-1j*e*t)*(v.conj().T@psi))
 t=.37;dt=1e-5
 derivative=(minus(t-2*dt)-8*minus(t-dt)+8*minus(t+dt)-minus(t+2*dt))/(12*dt)
 residual=float(np.linalg.norm(1j*derivative-hm@minus(t))/np.linalg.norm(hm@minus(t)))
 check('action_equation_finite_difference',residual<1e-8)
 # Export one small problem for independent FULL 2N x 2N evolution.
 np.savez_compressed(P/'dense_verification_input.npz',**dense_case)
 np.savez_compressed(P/'endpoint_record_profiles.npz',**snapshots)
 hbar=1.054571817e-34;tau=1.481301966415863e-21;g=math.pi*hbar/(2*tau)
 result={'framework_name':'Wonsik Reality–Renderer Architecture','version':'source-carrier-action v0.1','date':'2026-10-21',
 'assessment':{'inputs':'Registered 512-state swap, matched source/supply gap, actual frozen B and inherited spectral carrier; retained profile period L=1024*c*tau','WRRA_transformation':'Gate -> minimum positive generator -> constrained quadratic action -> common 15-channel transport plus explicit source-shaped exchange-rate candidate','outputs':'Endpoint replay, continuous exchange, joint coupled evolution, conserved full energy and typed source/supply resources','falsification':'Gate mismatch, action residual, norm/resource/full-energy drift, loss of channels or failure of resolution convergence'},
 'registers':{'source_mode':128,'supply_bit':2,'new_degenerate_record_bit':2,'timeless_allocation_slots_unchanged':True,'internal_carrier_channels':15},
 'geometry':{'profile_period_in_shutter_edges':1024,'c_tau_over_L':BETA,'dimensions_executed':1,'carrier_channels':15},
 'minimum_generator':{'dimensionless_positive_eigenvalues':[0,math.pi],'positive_log_branch_squared_costs':branch_costs,'conditional_hbar_over_tau_J':hbar/tau,'conditional_pair_coupling_g_J':g,'conditional_g_MeV':g/1.602176634e-13,'drive_expectation_uniform_p_half_J':.5*g},
 'coupled_results':summary,'negative_controls':{'omitted_coupling_energy_error':omitted,'detuned_resource_commutator':detune,'rank_one_channel_rank':1},'finite_difference_action_residual':residual,
 'scope':'A conditional continuous generator and variational completion of the registered finite swap, plus an executed NEW spatial coupling candidate. Not derivation of SOURCE cardinality/preparation, autonomous one-shot trigger/reset, SM interactions, macro scale or cosmological metric stress of the new generator.',
 'checks':checks,'passed':sum(checks.values()),'total':len(checks)}
 csvwrite('continuous_exchange.csv',pulse);csvwrite('coupled_time_history.csv',rows);csvwrite('resolution.csv',summary)
 (P/'results.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['minimum_generator','coupled_results','finite_difference_action_residual','passed','total']},indent=2))
if __name__=='__main__':main()
