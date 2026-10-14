"""Positive static information-profile readout from verified slot payloads.
NO time, SI volume, slot-index-as-prime, arbitrary phase, or epsilon denominator.
"""
from pathlib import Path
import json
import numpy as np
ROOT=Path(__file__).resolve().parent
PRIMES=(2,3,5);MODULUS=30;SLOTS=128

def residue_payload(contribution,n):
    mass=contribution.sum(0);total=float(mass.sum());capacity=total/SLOTS
    end=np.cumsum(mass);start=end-mass
    first=np.clip(np.floor(start/capacity).astype(int),0,SLOTS-1)
    last=np.clip(np.floor(np.nextafter(end,start)/capacity).astype(int),0,SLOTS-1)
    r=n%MODULUS
    B=np.array([np.bincount(r*SLOTS+first,weights=x,minlength=MODULUS*SLOTS).reshape(MODULUS,SLOTS) for x in contribution])
    split_error=0.
    for i in np.flatnonzero(last>first):
        B[:,r[i],first[i]]-=contribution[:,i]
        fractions=[]
        for j in range(first[i],last[i]+1):
            fraction=max(0.,min(end[i],(j+1)*capacity)-max(start[i],j*capacity))/mass[i]
            B[:,r[i],j]+=fraction*contribution[:,i];fractions.append(fraction)
        split_error=max(split_error,abs(sum(fractions)-1))
    return B,total,split_error

def modular_positive_kernel(grid):
    # x is a dimensionless phase coordinate on one periodic interval.
    x=np.arange(grid,dtype=float)/grid;r=np.arange(MODULUS)
    K=np.ones((MODULUS,grid))
    for p in PRIMES:
        theta=(r%p)[:,None]/p-x[None,:]
        divisor=np.exp(2j*np.pi*theta[:,:,None]*np.arange(p)[None,None,:]).mean(2)
        K*=abs(1-divisor)**2
    norms=K.mean(1)
    if np.any(norms<=0):raise ValueError('A residue kernel has zero support')
    K/=norms[:,None]
    return x,K

def positive_profile(payload,grid=1024):
    x,K=modular_positive_kernel(grid)
    per_residue_slot=payload.sum(0)
    W_s=per_residue_slot.sum(0)
    if np.any(W_s<=0):raise ValueError('Empty slot requires an explicit handling rule')
    # K_s uses actual residue composition IN the slot, not the integer slot label.
    K_s=(per_residue_slot.T@K)/W_s[:,None]
    info=W_s@K_s
    baseline=float(W_s.sum())
    if baseline<=0:raise ValueError('Positive input total load required')
    delta=(info-baseline)/baseline
    sector_profile=np.einsum('srj,rx->sx',payload,K)
    return x,info,delta,W_s,K_s,sector_profile

def run():
    d=np.load(ROOT/'inputs/addresses.npz');n=d['addresses'][1:];w=d['address_weights'][1:];e=d['sector_effects'][1:].T
    old=np.load(ROOT/'inputs/verified_slot_loads.npz');results=[];checks={};arrays={}
    for branch,lam in [('unweighted',[0,0,0]),('weighted',[0,.25,.1])]:
        contrib=e*w[None,:]*(1+np.array(lam)[:,None]*np.log(n)[None,:]/np.log(n[-1]))
        B,total,spliterr=residue_payload(contrib,n)
        x,I,delta,W,Ks,sector=positive_profile(B,1024)
        _,I2,delta2,*_=positive_profile(B,2048)
        _,I3,delta3,*_=positive_profile(B,4096)
        direct_B=np.array([np.bincount(n%30,weights=c,minlength=30) for c in contrib])
        _,K=modular_positive_kernel(1024);direct=direct_B.sum(0)@K
        # Analytic strict positivity of the TOTAL profile for every real periodic x.
        # CRT factorization: sum_(r mod30) product_p |H_p(r/p-x)|² = product_p(p-1)=8.
        raw=np.ones((30,1024))
        for p in PRIMES:
            theta=(np.arange(30)%p)[:,None]/p-x[None,:]
            D=np.exp(2j*np.pi*theta[:,:,None]*np.arange(p)[None,None,:]).mean(2)
            raw*=abs(1-D)**2
        class_mass=B.sum(axis=(0,2));Z=raw.mean(1)
        continuous_lower_bound=float(8*class_mass.min()/Z.max())
        # Original mod3 group contributions are recoverable from the richer payload.
        group_payload=np.stack([B[:,np.arange(30)%3!=0].sum(1),B[:,np.arange(30)%3==0].sum(1)],axis=1)
        target=old[branch+'_ascending_sector_group_slot_B']
        checks[branch+'_existing_slot_weights']=bool(np.allclose(W,old[branch+'_ascending_static_slot_load'],atol=1e-12,rtol=0))
        checks[branch+'_group_correlation_preserved']=bool(np.allclose(group_payload,target,atol=1e-12,rtol=0))
        checks[branch+'_all_sector_residue_marginals']=bool(np.allclose(B.sum(2),direct_B,atol=1e-12,rtol=0))
        checks[branch+'_positive_payload_kernel_profile']=bool(B.min()>-1e-14 and Ks.min()>=0 and I.min()>=0)
        checks[branch+'_kernel_mean_one']=bool(np.max(abs(Ks.mean(1)-1))<1e-12)
        checks[branch+'_mean_input_total']=abs(I.mean()/total-1)<1e-12
        checks[branch+'_slot_routing_equals_direct_address']=bool(np.max(abs(I-direct))/total<1e-12)
        checks[branch+'_grid_refinement']=bool(max(abs(I2[::2]-I).max(),abs(I3[::4]-I).max())/total<1e-12)
        checks[branch+'_no_epsilon_denominator']=bool(np.all(np.isfinite(delta)))
        checks[branch+'_split_load_preserved']=spliterr<1e-10
        ft=np.fft.rfft(delta)/len(delta)
        checks[branch+'_all_tap_bandwidth_preserved']=bool(abs(ft[8:]).max()<1e-12)
        checks[branch+'_CRT_raw_kernel_partition']=bool(np.max(abs(raw.sum(0)-8))<1e-12)
        checks[branch+'_positive_all_residue_mass']=bool(class_mass.min()>0)
        checks[branch+'_continuous_strict_positivity_bound']=bool(continuous_lower_bound>0 and I.min()>=continuous_lower_bound)
        arrays[branch+'_sector_residue_slot_payload']=B;arrays[branch+'_verified_W_s']=W
        arrays[branch+'_positive_slot_kernels']=Ks;arrays[branch+'_info_profile']=I
        arrays[branch+'_relative_information_variation']=delta;arrays[branch+'_information_mode_fft']=ft
        arrays[branch+'_sector_profiles']=sector
        results.append({'branch':branch,'grid':1024,'input_static_total':total,'profile_mean':float(I.mean()),
          'profile_min':float(I.min()),'profile_max':float(I.max()),'negative_fraction':float(np.mean(I<0)),
          'strict_positive_bound_all_real_x':continuous_lower_bound,
          'max_relative_information_variation':float(abs(delta).max()),
          'rms_relative_information_variation':float(np.sqrt(np.mean(delta*delta))),
          'largest_nonzero_information_mode':float(abs(ft[1:]).max()),
          'refinement_max_relative_error':float(max(abs(I2[::2]-I).max(),abs(I3[::4]-I).max())/total),
          'small_information_variation_diagnostic_0_1':bool(abs(delta).max()<.1)})
    checks={k:bool(v) for k,v in checks.items()}
    assert all(checks.values()),[k for k,v in checks.items() if not v]
    out={'renderer_slots':128,'actual_prime_filter_stages':list(PRIMES),'payload_modulus':30,
      'coordinate':'dimensionless periodic x=i/grid; endpoint excluded',
      'readout':'I(x)=sum_s W_s K_s(x), K_s>=0, mean(K_s)=1',
      'baseline':'sum_s W_s from input; no 1e-12 denominator',
      'kernel_choice':'NEW spatial/phase readout using all original transmission taps; not a uniquely derived physical density',
      'time_used':False,'physical_volume_used':False,'SI_energy_used':False,'posthoc_amplitude_rescaling':False,
      'cases':results,'checks':checks,'checks_passed':sum(checks.values()),
      'physical_density':None,'sound_speed':None,'CAMB_TT_EE':None,'official_minus_2_logL':None}
    (ROOT/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
    np.savez_compressed(ROOT/'positive_profile_and_payload.npz',x=x,**arrays)
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':run()
