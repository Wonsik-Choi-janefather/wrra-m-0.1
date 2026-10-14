#!/usr/bin/env python3
"""Finite shared-carrier light/shutter bridge. python reproduce.py"""
from pathlib import Path
from decimal import Decimal, getcontext, ROUND_HALF_UP
import json,csv,hashlib,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
getcontext().prec=70
P=Path(__file__).resolve().parent
D=lambda x: Decimal(str(x))

def savecsv(name,rows):
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

def main():
    cfg=json.loads((P/'frozen_inputs.json').read_text())
    c=cfg['c_m_s']; h=cfg['h_J_s']/cfg['e_J_per_eV']; hb=h/(2*math.pi)
    E=cfg['mode_energy_eV']; eps=cfg['epsilon']; dt=eps*hb/E; dx=c*dt
    # Decimal audit uses the stated finite precision of the frozen clock scale.
    dtd=D(dt); dxd=D(c)*dtd
    photons=[]
    for e in cfg['photon_energy_cases_eV']:
        phase=e*dt/hb
        principal=(phase+math.pi)%(2*math.pi)-math.pi
        inferred=principal*hb/dt
        admitted=phase<math.pi
        refine=1 if admitted else 2**max(0,math.ceil(math.log2(phase/math.pi*1.000000001)))
        finephase=e*(dt/refine)/hb
        recovered=((finephase+math.pi)%(2*math.pi)-math.pi)*hb/(dt/refine)
        assert abs(recovered/e-1)<1e-9
        budget_refine=1 if phase<=eps else 2**math.ceil(math.log2(phase/eps))
        photons.append(dict(energy_eV=e,phase_per_shutter_rad=phase,
           wavelength_m=h*c/e,admitted_on_base_tick=admitted,
           aliased_energy_eV_if_gate_ignored=inferred,required_binary_refinement=refine,
           refined_tick_s=dt/refine,refined_step_m=dx/refine,
           recovered_energy_eV_after_refinement=recovered,
           refinement_to_keep_anchor_phase_budget=budget_refine))
    savecsv('photon_band_audit.csv',photons)

    # New conditional external-space carrier renderer, not SOURCE address geometry.
    # Its finite ring is a computational boundary; internal 15 channels stay distinct.
    N=512; channels=15; spectral=[]
    cells=np.arange(N)
    for n in (1,4,16,64,127):
        v=np.exp(2j*math.pi*n*cells/N)/math.sqrt(N)
        shifted=np.roll(v,1)
        eigen=np.vdot(v,shifted)
        k=2*math.pi*n/(N*dx); omega=-np.angle(eigen)/dt
        spectral.append(dict(mode=n,energy_eV=hb*c*k,omega_s_inv=omega,
          k_m_inv=k,phase_speed_m_s=omega/k,
          relative_c_error=omega/(k*c)-1,
          eigenvector_residual=float(np.linalg.norm(shifted-eigen*v))))
    savecsv('finite_carrier_modes.csv',spectral)

    rng=np.random.default_rng(20261014)
    weights=rng.random(channels);weights/=weights.sum()
    mode=np.arange(N);amps=np.exp(-.5*((mode-16)/2)**2).astype(complex)
    amps[(mode<1)|(mode>=N//2)]=0
    amps*=np.exp(-2j*math.pi*mode*128/N)
    packet=np.fft.ifft(amps);packet/=np.linalg.norm(packet)
    psi=np.sqrt(weights)[:,None]*packet[None,:]
    omega_fft=2*math.pi*np.fft.fftfreq(N)/dt
    carrier_energy=lambda x:float(np.sum(abs(np.fft.fft(x,axis=1))**2*(hb*omega_fft)[None,:])/N)
    initial_energy=carrier_energy(psi)
    angles=[];records=[];maxnorm=0;maxchannel=0;maxenergy=0
    for tick in range(65):
        density=np.sum(abs(psi)**2,axis=0)
        angles.append(float(np.angle(np.sum(density*np.exp(2j*math.pi*cells/N)))))
        maxnorm=max(maxnorm,abs(float(density.sum())-1))
        maxchannel=max(maxchannel,float(max(abs(np.sum(abs(psi)**2,axis=1)-weights))))
        maxenergy=max(maxenergy,abs(carrier_energy(psi)-initial_energy)/initial_energy)
        records.append(dict(tick=tick,time_s=tick*dt,total_probability=float(density.sum()),
                            spectral_energy_eV=carrier_energy(psi)))
        if tick<64: psi=np.roll(psi,1,axis=1)
    positions=np.unwrap(angles)*N*dx/(2*math.pi)
    velocities=np.diff(positions)/dt
    for i,row in enumerate(records):row['circular_centroid_unwrapped_m']=float(positions[i])
    savecsv('transport_ledger.csv',records)
    assert maxnorm<1e-12 and maxchannel<1e-12 and maxenergy<1e-12
    assert max(abs(velocities/c-1))<1e-11
    assert max(abs(x['relative_c_error']) for x in spectral)<1e-11

    # Existing cross-domain times are re-expressed, not used as extra clock fits.
    rows=[]
    for case in cfg['time_cases']:
        t=1/D(case['frequency_Hz']) if 'frequency_Hz' in case else D(case['time_s'])
        ticks=(t/dtd).to_integral_value(rounding=ROUND_HALF_UP)
        reconstructed=ticks*dtd; error=reconstructed-t
        assert abs(error)<=dtd/2
        distance=ticks*dxd
        assert abs(distance-D(c)*reconstructed)<=D('1e-50')*max(D(1),abs(distance))
        rows.append(dict(case=case['label'],kind=case['kind'],reference_time_s=str(t),
          tick_count=str(ticks),reconstructed_time_s=str(reconstructed),
          time_rounding_error_s=str(error),light_path_equivalent_m=str(D(c)*t),
          error_scope='Representational rounding only; inherited physical-model residuals remain.'))
    savecsv('cross_domain_clock.csv',rows)

    # One-hop assumption audit: c constrains hop length / cadence, not each separately.
    resolutions=[]
    for r in (1,2,4,8):
        resolutions.append(dict(refinement=r,dt_s=dt/r,dx_m=dx/r,
          matched_speed_m_s=(dx/r)/(dt/r),speed_if_only_time_refined_m_s=dx/(dt/r)))
    result=dict(version='0.1',clock_interval_s=dt,light_step_m=dx,light_step_pm=dx*1e12,
      shutter_phase_at_mode_energy_rad=E*dt/hb,phase_resolution=eps,
      Nyquist_energy_eV=math.pi*hb/dt,clock_rounding_bound_s=dt/2,
      core_rule='One massless carrier shift per shutter; dx=c*dt in a local inertial frame.',
      rule_status='New explicitly adopted conditional spatial renderer, executed here. Not a pre-existing SOURCE-derived metric.',
      source_book=dict(library_file_id='libfile_262e51b78ae08191934144a2944fca88',version=2,
        relevant_pages=[12,13,14,106,107,149,150]),
      spatial_SOURCE_mapping_closed=False,unique_universal_shutter_established=False,
      universal_global_simultaneity_assumed=False,photon_proper_time_used=False,
      scope='Finite 1D, freely propagating massless branch with a common operator on 15 internal channels. No Maxwell polarization/gauge dynamics, interactions, 3D isotropy, gravity or Lorentz-covariant microscopic completion.',
      carrier_audit=dict(cells=N,internal_channels=channels,steps=64,
        norm_error=maxnorm,channel_weight_error=maxchannel,spectral_energy_relative_error=maxenergy,
        maximum_relative_packet_speed_error=float(max(abs(velocities/c-1)))),
      spectral_modes=spectral,photon_band_cases=photons,time_cases=rows,resolution_cases=resolutions,
      inherited_result_status=cfg['inherited_result_status'],
      identifiability='c fixes dx/dt. With hopping length and cadence both free, it cannot identify a unique dt. dt here is fixed by the calibrated mode-energy/phase-resolution bridge.',
      empirical_status='Unitary transport and representational compatibility checked; c and hbar are inputs. No new light-flight observation or independent spacetime calibration is added.',
      falsification='Nonconservation, channel-dependent propagation, velocity different from c under the common rule, unrejected phase aliasing, incompatible SOURCE metric once supplied, or failure of matched refinement.')
    (P/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

    fig,axs=plt.subplots(1,2,figsize=(10,4),layout='constrained')
    axs[0].plot(np.arange(65), (positions-positions[0])/dx,label='Executed carrier centroid')
    axs[0].plot(np.arange(65),np.arange(65),'--',label='One spatial step per shutter')
    axs[0].set(xlabel='Shutter count',ylabel='Travel (carrier steps)',title='One operator across 15 channels')
    axs[0].legend(fontsize=8);axs[0].grid(alpha=.25)
    xx=np.logspace(0,8,300);yy=xx*dt/hb
    axs[1].loglog(xx,yy);axs[1].axhline(math.pi,color='r',ls='--',label='Phase alias boundary π')
    axs[1].axvline(E,color='gray',ls=':',label='Frozen mode scale')
    axs[1].set(xlabel='Photon energy (eV)',ylabel='Phase per base shutter (rad)',title='A fixed shutter has a finite phase band')
    axs[1].legend(fontsize=8);axs[1].grid(alpha=.25)
    fig.savefig(P/'light_shutter_audit.png',dpi=170);plt.close(fig)
    (P/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name+'\n' for f in sorted(P.iterdir()) if f.is_file() and f.name!='SHA256SUMS.txt'))
    print(json.dumps({k:result[k] for k in ('clock_interval_s','light_step_pm','Nyquist_energy_eV','carrier_audit','spatial_SOURCE_mapping_closed')},indent=2))

if __name__=='__main__':main()
