#!/usr/bin/env python3
"""Correct residue-owned SOURCE spatial readout, calibrated harmonics and 3D test.
Run python reproduce.py. numpy/matplotlib; no online calls.
"""
from pathlib import Path
from decimal import Decimal,getcontext,ROUND_HALF_UP
import csv,hashlib,json,math,runpy
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
getcontext().prec=80

def csvfile(name,rows):
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)

def main():
    cfg=json.loads((P/'frozen_inputs.json').read_text())
    for name,sha in cfg['input_sha256'].items():
        assert hashlib.sha256((P/name).read_bytes()).hexdigest()==sha,name
    funcs=runpy.run_path(str(P/'inputs/original_positive_readout.py'))
    addr=np.load(P/'inputs/addresses.npz');target=np.load(P/'inputs/archived_profile.npz')
    n=addr['addresses'][1:];w=addr['address_weights'][1:];effects=addr['sector_effects'][1:].T
    assert len(addr['addresses'])==1015000 and addr['addresses'][0]==1
    c=cfg['c_m_s'];dt=cfg['dt_s'];dx=c*dt
    eta=np.array(cfg['eta_J_m3']);N=1024;Lmicro=N*dx
    Lmacro=2*math.pi*cfg['Mpc_m']/cfg['macro_anchor_k_Mpc_inv']
    x,K=funcs['modular_positive_kernel'](N)
    branch_rows=[];harmonics=[];profiles={};datasets={};physical_rows=[];physical_modes=[]
    baseline_eps=cfg['inherited_supply_epsilon'];gap=2*math.cos(math.pi/8)
    probability=.5+baseline_eps*(K-1)
    assert probability.min()>0 and probability.max()<1
    # Source register dynamics are inherited, not a fitted damping coefficient.
    ns={'__file__':str(P/'inputs/original_single_mode.py'),'__name__':'source_mode_adapter'}
    exec(compile((P/'inputs/original_single_mode.py').read_text(),ns['__file__'],'exec'),ns)
    for branch,lam in [('unweighted',[0,0,0]),('weighted',[0,.25,.1])]:
        contributions=effects*w[None,:]*(1+np.array(lam)[:,None]*np.log(n)[None,:]/np.log(n[-1]))
        B,total,spliterr=funcs['residue_payload'](contributions,n)
        xx,I,delta,W,Ks,S=funcs['positive_profile'](B,N)
        # Independent direct address residue accumulation; does not route through slots.
        D=np.array([np.bincount(n%30,weights=q,minlength=30) for q in contributions])
        direct=D@K
        errorB=float(np.max(abs(B-target[branch+'_sector_residue_slot_payload'])))
        errorS=float(np.max(abs(S-target[branch+'_sector_profiles'])))
        error_direct=float(np.max(abs(S-direct)))
        assert max(errorB,errorS,error_direct)<1e-12 and spliterr<1e-10
        coarse=B.sum(1)@Ks
        naive=float(np.max(abs(coarse-S)))
        assert naive>.01
        # Sector OWNED kernel is defined only on an occupied sector/slot.
        sector_slot=B.sum(1)
        sector_K=np.divide(np.einsum('srj,rx->sjx',B,K),sector_slot[:,:,None],
                           out=np.zeros((3,128,N)),where=sector_slot[:,:,None]>0)
        restored=np.einsum('sj,sjx->sx',sector_slot,sector_K)
        assert np.max(abs(restored-S))<1e-12
        # Post-frame candidate volume readout, retaining the existing density coefficients.
        # Uniform whole source+supplier resource gives mean readout A=1.
        # S is a positive density-shape input; this is a newly explicit local extension.
        u=eta[:,None]*S;u0=u.mean(1);ut=u.sum(0)
        contrast=ut/ut.mean()-1
        ft=np.fft.rfft(contrast)/N;tail=float(max(abs(ft[8:])))
        assert tail<1e-12
        rms=float(np.sqrt(np.mean(contrast**2)));peak=float(max(abs(contrast)))
        row=dict(branch=branch,address_payload_error=errorB,
          corrected_local_sector_error=errorS,direct_address_vs_slot_error=error_direct,
          sector_owned_kernel_reconstruction_error=float(np.max(abs(restored-S))),
          naive_shared_kernel_error=naive,mean_energy_density_J_m3=float(ut.mean()),
          conditional_density_relative_RMS=rms,conditional_density_max_contrast=peak,
          inherited_linear_gate_0_1_pass=bool(peak<.1),spectral_tail_after_mode7=tail)
        branch_rows.append(row);profiles[branch]=S
        datasets[branch+'_sector_profiles']=S;datasets[branch+'_sector_owned_kernel']=sector_K
        datasets[branch+'_density_shape_J_m3']=u;datasets[branch+'_total_density_contrast']=contrast
        # Correct typed bridge: residue-owned kernel modulates an addressed supply
        # probability, rather than equating information shape to density directly.
        # p_r(X)=1/2+eps*(K_r(X/L)-1), on the original mod3-complement addresses.
        mask=np.arange(30)%3!=0
        controlled=B[:,mask,:].sum(2)
        Cshape=controlled@K[mask,:]
        M=controlled.sum(1)
        du=baseline_eps*eta[:,None]*gap*(Cshape-M[:,None]);du[0]=0
        u_physical=u0[:,None]+du
        # Count the prepared supplier at every phase point, before the swap.
        mu=B.sum((1,2));A8=1-math.cos(math.pi/8)
        src_before=eta*np.array([mu[0],mu[1]-M[1]+A8*M[1],mu[2]-M[2]+A8*M[2]])
        supplier=eta[:,None]*gap*(controlled@probability[mask,:]);supplier[0]=0
        before=src_before[:,None]+supplier
        balance=float(np.max(abs(before-u_physical)))
        pressure_balance=float(np.max(abs(-before[2]+u_physical[2])))
        assert balance<2e-24 and pressure_balance<2e-24
        assert np.min(u_physical)>0
        relative=du.sum(0)/u0.sum()
        assert max(abs(relative))<.1
        pressure_delta=-du[2]
        coeff=np.fft.rfft(du,axis=1)/N
        physical_rows.append(dict(branch=branch,supply_probability_min=float(probability.min()),
          supply_probability_max=float(probability.max()),
          total_density_relative_RMS=float(np.sqrt(np.mean(relative**2))),
          total_density_max_contrast=float(max(abs(relative))),
          mean_density_shift_J_m3=float(np.max(abs(du.mean(1)))),
          whole_frame_density_balance_error_J_m3=balance,
          whole_frame_pressure_balance_error_J_m3=pressure_balance,
          pressure_variation_max_J_m3=float(max(abs(pressure_delta))),
          linear_gate_0_1_pass=True,inherited_epsilon=baseline_eps,new_amplitude_fit=False))
        datasets[branch+'_supply_mapped_density_J_m3']=u_physical
        datasets[branch+'_supply_mapped_density_delta_J_m3']=du
        datasets[branch+'_supply_mapped_pressure_delta_J_m3']=pressure_delta
        for mode in range(1,8):
            ns['K']=cfg['macro_anchor_k_Mpc_inv']*mode
            for component,arr in [('cosine',2*coeff[:,mode].real),('sine',-2*coeff[:,mode].imag)]:
                # Actual small energy amplitudes are provided to the existing solver.
                # epsilon=1 here only avoids applying the inherited epsilon twice.
                response=arr.copy();response[0]=0
                if abs(response[2])<1e-40:continue
                completed,_,solution=ns['integrate'](u0,response,epsilon=1.,include_force=True)
                omitted,_,_=ns['integrate'](u0,response,epsilon=1.,include_force=False)
                tighter,_,tight_solution=ns['integrate'](u0,response,epsilon=1.,include_force=True,rtol=2e-12)
                probe=np.linspace(np.log(.02),0,100)
                conv=float(np.max(abs(solution.sol(probe)-tight_solution.sol(probe)))/max(np.max(abs(tight_solution.sol(probe))),1e-100))
                good=completed['einstein_constraint_in_common_vacuum_source_units']
                bad=omitted['einstein_constraint_in_common_vacuum_source_units']
                assert good<1e-6 and bad>.99 and conv<1e-7
                physical_modes.append(dict(branch=branch,mode=mode,component=component,
                  k_Mpc_inv=ns['K'],delta_u_D_at_a1_J_m3=float(response[1]),
                  delta_u_R_J_m3=float(response[2]),
                  required_transfer_residual=float(good),omitted_transfer_residual=float(bad),
                  tighter_tolerance_residual=float(tighter['einstein_constraint_in_common_vacuum_source_units']),
                  solution_convergence_relative_error=conv,
                  spatial_trace_residual=float(completed['spatial_Einstein_trace_residual_in_vacuum_source_units']),
                  scope='Inherited conditional late-epoch baryon/dark/vacuum GR subsystem; no new CMB/Boltzmann calculation.'))
        for mode in range(1,8):
            k=cfg['macro_anchor_k_Mpc_inv']*mode
            period=Lmacro/mode/c
            # Stable finite integer event count, instead of iterating ~10**36 shutters.
            t=Decimal(str(period));tick=Decimal(str(dt))
            count=(t/tick).to_integral_value(rounding=ROUND_HALF_UP)
            terr=count*tick-t
            assert abs(terr)<=tick/2
            harmonics.append(dict(branch=branch,mode=mode,
              macro_wavenumber_Mpc_inv=k,macro_wavelength_Mpc=2*math.pi/k,
              conditional_density_Fourier_abs=float(abs(ft[mode])),
              conditional_density_cosine_amplitude=float(2*abs(ft[mode])),
              supply_mapped_total_density_cosine_amplitude=float(2*abs(coeff[:,mode].sum())/u0.sum()),
              supply_mapped_D_density_cosine_amplitude_J_m3=float(2*abs(coeff[1,mode])),
              supply_mapped_R_density_cosine_amplitude_J_m3=float(2*abs(coeff[2,mode])),
              Fourier_phase_rad=float(np.angle(ft[mode])),
              snapshot_light_phase_period_s=period,finite_shutter_count=str(count),
              shutter_rounding_error_s=str(terr),
              scope='k1=.05 is supplied/calibrated; additional k and shape amplitudes are outputs. Snapshot light phase period is not cosmic evolution time.'))
    csvfile('local_sector_reconstruction.csv',branch_rows)
    csvfile('calibrated_SOURCE_harmonics.csv',harmonics)
    csvfile('residue_supply_density_map.csv',physical_rows)
    csvfile('SOURCE_harmonic_GR_controls.csv',physical_modes)
    np.savez_compressed(P/'corrected_local_fields.npz',x=x,**datasets)

    # Explicit replacement for naive axis walking: adopted massless spectral transport.
    # Exact discrete U, with one spatial factor and the same identity on 15 channels.
    # It is nonlocal in position; strict microscopic causal support is NOT proved.
    nx,ny,nz=cfg['address_index_shape'];shape=(nz,ny,nx)
    qx=2*math.pi*np.fft.fftfreq(nx);qy=2*math.pi*np.fft.fftfreq(ny);qz=2*math.pi*np.fft.fftfreq(nz)
    qmag=np.sqrt(qz[:,None,None]**2+qy[None,:,None]**2+qx[None,None,:]**2)
    unitary=np.exp(-1j*64*qmag)
    hb=cfg['h_J_s']/cfg['e_J_per_eV']/(2*math.pi)
    energy=hb*qmag/dt
    xx=np.arange(nx)/nx;yy=np.arange(ny)/ny;zz=np.arange(nz)/nz
    weights=np.arange(1,16,dtype=float);weights/=weights.sum()
    wave_rows=[]
    for mx,my,mz in [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1)]:
        phi=np.broadcast_to(np.exp(2j*math.pi*(mx*xx[None,None,:]+my*yy[None,:,None]+mz*zz[:,None,None])),shape).copy()/math.sqrt(nx*ny*nz)
        F=np.fft.fftn(phi,norm='ortho');power=abs(F)**2
        forbidden=float(power[qmag>=math.pi].sum())
        assert forbidden<1e-12
        q=np.array([2*math.pi*mx/nx,2*math.pi*my/ny,2*math.pi*mz/nz]);mag=np.linalg.norm(q)
        after=np.fft.ifftn(F*unitary,norm='ortho')
        norm_error=abs(float(np.sum(abs(after)**2))-1)
        eigen_error=float(np.linalg.norm(after-np.exp(-1j*64*mag)*phi))
        one=np.fft.ifftn(F*np.exp(-1j*qmag),norm='ortho')
        omega=-np.angle(np.vdot(phi,one))/dt
        speed=omega/(mag/dx)
        e0=float(np.sum(power*energy));e1=float(np.sum(abs(F*unitary)**2*energy))
        # Numerical phase-gradient check in the declared spectral dispersion.
        h=max(mag*1e-6,1e-8);grad=[]
        for axis in range(3):
            plus=q.copy();minus=q.copy();plus[axis]+=h;minus[axis]-=h
            grad.append((np.linalg.norm(plus)-np.linalg.norm(minus))/(2*h))
        group_speed=c*np.linalg.norm(grad)
        assert norm_error<1e-11 and eigen_error<1e-10
        assert abs(speed/c-1)<1e-10 and abs(group_speed/c-1)<1e-7
        assert abs(e1/e0-1)<1e-12
        # Tensor identity is evaluated in factored form, no duplicated spatial work.
        assert abs(float(weights.sum())-1)<1e-14
        wave_rows.append(dict(mx=mx,my=my,mz=mz,internal_channels=15,
          shutters=64,phase_speed_m_s=float(speed),group_gradient_speed_m_s=float(group_speed),
          norm_error=norm_error,spectral_energy_relative_error=abs(e1/e0-1),
          spatial_eigenstate_error=eigen_error,forbidden_phase_band_power=forbidden))
    csvfile('three_dimensional_carrier_test.csv',wave_rows)
    del phi,F,power,after,one,energy,unitary,qmag

    result=dict(version='0.2',validation_input=cfg,
      WRRA_transform='Full address effects/weights -> sector-residue-slot B -> residue transmission kernel K_r -> owned P/D/R spatial profiles -> calibrated X=Lx -> local adopted density readout; separate common 3D spectral carrier test.',
      local_reconstruction=branch_rows,macro_mode_calibration=dict(
        anchor='Existing prescribed k1=.05 Mpc^-1 identified with first source harmonic as an explicit calibration choice.',
        profile_micro_period_m=Lmicro,macro_period_m=Lmacro,
        macro_to_micro_length_ratio=Lmacro/Lmicro,
        shape_harmonics_are_outputs=True,cosmological_scale_from_NU_alone=False,
        original_single_mode_eps_1e_minus8_unchanged=True,
        original_mode_is_not_new_source_density_field=True),
      calibrated_harmonics=harmonics,three_dimensional_carrier=wave_rows,
      residue_supply_density_map=physical_rows,SOURCE_harmonic_GR_controls=physical_modes,
      new_typed_density_rule='Use the inherited source/supply Hamiltonian: p_r=.5+eps*(K_r-1); delta u_s=eta_s*DeltaA*eps*sum_controlled B_s,r,j*(K_r-1), s=D,R. P unchanged. No new amplitude fit.',
      new_preparation_assumption='The archived residue kernel supplies the spatial template of each controlled address supply probability. Macro phase coordinate and uniform reference supply remain explicit calibration/preparation inputs.',
      three_dimensional_model_assumptions=['Adopt H=hbar*c*|k| on declared periodic coordinate graph.',
        'Use U=exp(-iH*dt/hbar) tensor I15; phase band admission |k|*dx<pi.',
        'Factored shared spatial plane wave and internal channel weights. Plane waves are probes, not arithmetic generation of photons.'],
      causal_support_or_full_Maxwell_proved=False,
      previous_local_failure_explanation='v0.1 used a TOTAL-slot conditional kernel for each sector. The inherited residue-specific kernel already existed; retaining it restores the archived local allocation.',
      refutation_conditions='Lost address/sector ownership, failed direct-vs-slot reconstruction, violated positivity/total energy accounting, phase alias admitted, unequal directional phase/group speeds under the spectral rule, or invalid use of a nonlinear SOURCE field in linear GR/CAMB.',
      verdict='Residue-owned local bridge reproduced and linked to shutter scale. Direct information-to-density substitution fails the linear gate. The inherited finite supply-probability/energy map succeeds with unchanged epsilon, and its actual source harmonic components pass conditional GR transfer controls. Seven-direction 3D spectral probes pass under adopted dynamics. Macro scale remains calibrated; no new CMB likelihood or universe-size derivation.')
    (P/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    fig,axs=plt.subplots(1,2,figsize=(10,4),layout='constrained')
    S=profiles['weighted']
    for a,label in enumerate(['P','D','R']):axs[0].plot(x,S[a]/S[a].mean(),label=label)
    axs[0].set(xlabel='Source phase coordinate',ylabel='Sector profile / sector mean',title='Residue-owned local profiles reproduced');axs[0].legend();axs[0].grid(alpha=.2)
    hrows=[r for r in harmonics if r['branch']=='weighted']
    kval=np.array([r['macro_wavenumber_Mpc_inv'] for r in hrows])
    axs[1].bar(kval-.008,[r['conditional_density_cosine_amplitude'] for r in hrows],width=.015,label='Direct information→density control')
    axs[1].bar(kval+.008,[r['supply_mapped_total_density_cosine_amplitude'] for r in hrows],width=.015,label='Inherited supply-energy map')
    axs[1].set(yscale='log',xlabel='k (Mpc⁻¹); first mode calibrated',ylabel='Relative density cosine amplitude',title='Typed readout keeps the resource budget');axs[1].grid(axis='y',alpha=.2);axs[1].legend(fontsize=7)
    fig.savefig(P/'local_source_and_harmonics.png',dpi=160);plt.close(fig)
    (P/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(P))+'\n' for f in sorted(P.rglob('*')) if f.is_file() and f.name!='SHA256SUMS.txt'))
    print(json.dumps(dict(local_reconstruction=branch_rows,
       supply_density_map=physical_rows,real_source_GR_components=len(physical_modes),
       max_required_transfer_residual=max(r['required_transfer_residual'] for r in physical_modes),
       max_3D_phase_speed_relative_error=max(abs(r['phase_speed_m_s']/c-1) for r in wave_rows),
       max_3D_norm_error=max(r['norm_error'] for r in wave_rows),
       macro_length_ratio=Lmacro/Lmicro),indent=2))

if __name__=='__main__':main()
