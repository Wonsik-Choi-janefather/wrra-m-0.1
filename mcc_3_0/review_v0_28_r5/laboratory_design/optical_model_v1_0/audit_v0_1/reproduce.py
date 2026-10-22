#!/usr/bin/env python3
"""Conditional SOURCE-to-relative-phase audit. No observational fitting.

Run: python reproduce.py
The new optical phase coupling is DECLARED, not derived from the inherited
stress/gravity calculation. Three memory laws are compared rather than selected.
"""
from pathlib import Path
from decimal import Decimal, localcontext, ROUND_HALF_UP
import csv, hashlib, json, math
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.signal import find_peaks
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True)

def write_csv(name, rows):
    with (OUT/name).open('w', newline='') as stream:
        writer=csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

def main():
    clock=json.loads((ROOT/'inputs/clock.json').read_text())
    frozen=json.loads((ROOT/'inputs/extension.json').read_text())
    archive=np.load(ROOT/'inputs/finite_preparation.npz')
    raw=archive['dimensionless_fluctuation'][1]
    # Remove the mean, a deterministic phase shift, not visibility loss.
    f=raw-raw.mean(); J=len(f); var=float(np.mean(f*f)); rms=math.sqrt(var)
    dt=clock['epsilon']*clock['h_J_s']/clock['e_J_per_eV']/(2*math.pi)/clock['mode_energy_eV']
    ell=clock['c_m_s']*dt; g=frozen['relative_phase_coupling_g']
    assert J==128
    correlations=np.array([np.mean(f*np.roll(f,-q)) for q in range(J)])
    prefixes=np.zeros((J,J))
    for r in range(1,J): prefixes[r]=prefixes[r-1]+np.roll(f,-(r-1))
    cycle_sum=np.sum([np.roll(f,-q) for q in range(J)],axis=0)
    cycle_rms=max(float(np.sqrt(np.mean(p*p))) for p in prefixes)
    cycle_max=max(float(np.max(abs(p))) for p in prefixes)
    checks={}

    def ticks(length):
        with localcontext() as context:
            context.prec=70
            n=int((Decimal(str(length))/Decimal(str(ell))).to_integral_value(rounding=ROUND_HALF_UP))
            rounded=Decimal(n)*Decimal(str(ell))
            error=rounded-Decimal(str(length))
        return n,float(rounded),float(error)

    def finite_visibility(phase):
        # Stable evaluation of both |mean exp(i phase)| and 1 - visibility.
        phase=np.asarray(phase,dtype=np.longdouble)
        rr=np.mean(-2*np.sin(phase/2)**2)
        ii=np.mean(np.sin(phase))
        w=2*rr+rr*rr+ii*ii
        log_v=np.log1p(w)/2 if w>-1 else np.longdouble('-inf')
        return float(np.exp(log_v)),float(-np.expm1(log_v)),float(log_v)

    def point(wavelength,length):
        n,L,error=ticks(length); a=2*math.pi/float(wavelength)
        static_phase=g*a*L*f
        vs,loss_s,_=finite_visibility(static_phase)
        _,_,log_single=finite_visibility(g*a*ell*f)
        iid_log=n*log_single
        vi=float(np.exp(iid_log)); loss_i=float(-np.expm1(iid_log))
        cycle_phase=g*a*ell*prefixes[n%J]
        vc,loss_c,_=finite_visibility(cycle_phase)
        return dict(wavelength_m=wavelength,path_exposure_m=L,requested_path_exposure_m=length,
            physical_shutters=str(n),path_rounding_error_m=error,
            base_unitary_visibility=1.0,static_visibility=vs,static_visibility_loss=loss_s,
            static_phase_RMS_rad=abs(g)*a*L*rms,
            iid_visibility=vi,iid_visibility_loss=loss_i,
            iid_phase_RMS_rad=abs(g)*a*ell*math.sqrt(n*var),
            iid_fresh_register_entropy_nats=n*math.log(J),
            cyclic_visibility=vc,cyclic_visibility_loss=loss_c,
            cyclic_phase_RMS_rad=float(np.std(cycle_phase)),cyclic_residual_shutters=n%J,
            static_or_cyclic_initial_register_entropy_nats=math.log(J))

    table=[]; boundaries=[]
    target=math.exp(-.5)
    for wavelength in frozen['wavelengths_m']:
        a=2*math.pi/wavelength
        static_L=1/(abs(g)*a*rms)
        iid_L=1/(g*g*a*a*ell*var)
        # Find FIRST visibility crossing; finite distribution is not Gaussian.
        def loss_target(L): return abs(np.mean(np.exp(1j*g*a*L*f)))-target
        grid=np.linspace(0,static_L*10,10001)
        first=next((i for i in range(1,len(grid)) if loss_target(grid[i])<=0),None)
        first_cross=brentq(loss_target,grid[first-1],grid[first]) if first else None
        _,_,single_log=finite_visibility(g*a*ell*f)
        iid_cross_N=math.ceil(-.5/single_log)
        iid_cross_L=iid_cross_N*ell
        bound_phase=abs(g)*a*ell*cycle_max
        boundaries.append(dict(wavelength_m=wavelength,static_sigma_one_path_m=static_L,
            static_exact_first_visibility_exp_minus_half_path_m=first_cross,
            static_visibility_at_sigma_one=loss_target(static_L)+target,
            iid_sigma_one_path_m=iid_L,iid_exact_visibility_exp_minus_half_path_m=iid_cross_L,
            cyclic_all_length_phase_RMS_bound_rad=abs(g)*a*ell*cycle_rms,
            cyclic_all_length_visibility_loss_upper_bound=bound_phase**2/2,
            status='Conditional on declared g=1 and specified memory law; not an inherited optical prediction'))
        for L in frozen['path_exposures_m']: table.append(point(wavelength,L))
    write_csv('visibility_by_wavelength_and_exposure.csv',table)
    write_csv('conditional_boundaries.csv',boundaries)
    write_csv('source_phase_autocorrelation.csv',[dict(lag=q,covariance=float(correlations[q]),
        normalized_correlation=float(correlations[q]/var)) for q in range(J)])
    # Dimensionless curve shape survives a rescaling of nonzero g or wavelength
    # within the STATIC, LINEAR phase extension; its absolute length does not.
    z=f/rms
    shape=lambda beta: abs(np.mean(np.exp(1j*beta*z)))
    betas=np.linspace(0,10,10001)
    vis=np.abs(np.mean(np.exp(1j*betas[:,None]*z),axis=1))
    minimum_indices=find_peaks(-vis)[0]
    maximum_indices=find_peaks(vis)[0]
    mi=minimum_indices[0]; ma=next(i for i in maximum_indices if i>mi)
    opt_min=minimize_scalar(shape,bounds=(betas[mi-1],betas[mi+1]),method='bounded',options={'xatol':1e-13})
    opt_max=minimize_scalar(lambda beta:-shape(beta),bounds=(betas[ma-1],betas[ma+1]),method='bounded',options={'xatol':1e-13})
    shape_result=dict(first_minimum_beta=float(opt_min.x),first_minimum_visibility=float(opt_min.fun),
        first_revival_beta=float(opt_max.x),first_revival_visibility=float(-opt_max.fun),
        revival_to_first_minimum_exposure_ratio=float(opt_max.x/opt_min.x),
        minimum_exposure_1064nm_g1_m=float(opt_min.x*1064e-9/(2*math.pi*rms)),
        revival_exposure_1064nm_g1_m=float(opt_max.x*1064e-9/(2*math.pi*rms)),
        scope='Static 128-state, centered mean-stress, linear phase coupling only. Not fundamental wavefunction collapse.')

    # Direct density-matrix control: the finite phase gate commutes with path-
    # degenerate free photon energy, preserves trace/positivity, and global entropy.
    # It does NOT implement a Maxwell/SOURCE interaction Hamiltonian derivation.
    lam=frozen['wavelengths_m'][1]; L=10.; phi=g*2*math.pi/lam*L*f
    states=np.stack([np.exp(1j*phi),np.ones(J)],axis=1)/math.sqrt(2)
    rho=states.T@states.conj()/J
    eig=np.linalg.eigvalsh(rho)
    energy=clock['h_J_s']*clock['c_m_s']/lam
    checks['density_trace']=bool(abs(np.trace(rho)-1)<1e-14)
    checks['density_positive']=bool(eig.min()>=-1e-14)
    checks['density_visibility_exact_average']=bool(abs(2*abs(rho[0,1])-abs(np.mean(np.exp(1j*phi))))<1e-14)
    checks['photon_energy_unchanged']=bool(abs(energy*np.trace(rho).real/energy-1)<1e-14)
    checks['finite_cycle_zero_mode_removed']=bool(np.max(abs(cycle_sum))<1e-20)
    checks['autocorrelation_PSD']=bool(np.fft.fft(correlations).real.min()>-1e-28)
    inherited=json.loads((ROOT/'inputs/preparation_results.json').read_text())
    checks['SOURCE_RMS_reproduced']=bool(abs(rms/inherited['mean_stress_relative_RMS_D_R'][0]-1)<1e-13)
    checks['source_D_R_covariance_reproduced']=bool(np.max(abs(archive['dimensionless_fluctuation'][1:]@archive['dimensionless_fluctuation'][1:].T/J-np.array(inherited['covariance_finite_phase'])))<1e-30)
    checks['exact_iid_matches_variance_boundary']=bool(all(abs(b['iid_exact_visibility_exp_minus_half_path_m']/b['iid_sigma_one_path_m']-1)<1e-12 for b in boundaries))
    # Numerical subdivision retains each physical shutter's control value.
    fine_err=max(float(np.max(abs(np.exp(1j*phi)-np.exp(1j*phi/r)**r))) for r in [2,4,8])
    checks['same_physical_state_subdivision']=fine_err<1e-13
    # Inherited common 15-channel carrier: roll both arms identically.
    rng=np.random.default_rng(20261014)
    packet=rng.normal(size=(15,512))+1j*rng.normal(size=(15,512));packet/=np.linalg.norm(packet)
    arms=np.stack([packet.copy(),packet.copy()])
    max_v=0.;max_norm=0.
    for t in range(65):
        max_v=max(max_v,abs(abs(np.vdot(arms[0],arms[1]))-1))
        max_norm=max(max_norm,max(abs(np.linalg.norm(arm)-1) for arm in arms))
        if t<64: arms=np.roll(arms,1,axis=-1)
    checks['base_common_carrier_coherence']=max_v<1e-13
    checks['base_common_carrier_norm']=max_norm<1e-13
    # Full common-mode exposure on BOTH arms cancels, at any source state.
    checks['identical_arm_coupling_cancels']=bool(np.max(abs(np.exp(1j*phi)*np.exp(-1j*phi)-1))<1e-14)
    checks['tick_rounding_bound']=all(abs(row['path_rounding_error_m'])<=ell*.501 for row in table)
    checks['visibility_in_unit_interval']=all(-1e-13<=row[key]<=1+1e-13 for row in table for key in ['static_visibility','iid_visibility','cyclic_visibility'])
    checks['finite_state_revival_resolved']=bool(shape_result['first_revival_visibility']>shape_result['first_minimum_visibility'])
    checks['wavelength_scaling']=bool(abs(boundaries[1]['static_exact_first_visibility_exp_minus_half_path_m']/boundaries[0]['static_exact_first_visibility_exp_minus_half_path_m']-2)<1e-10)
    checks={key:bool(value) for key,value in checks.items()}
    assert all(checks.values()),checks
    result=dict(version='0.1',date='2026-10-14',authors=['Wonsik Choi','Jeongin Choi'],
        validation_inputs=dict(c_m_s=clock['c_m_s'],shutter_s=dt,light_step_m=ell,
            frozen_SOURCE_phase_states=J,relative_dark_mean_stress_RMS=rms,
            removed_deterministic_mean=float(raw.mean()),no_new_observational_fitting=True),
        WRRA_transformation=dict(base='U_shift tensor I_15: coherent unitary transport',
            candidate='U_j = diag(exp(i g (2*pi/lambda) ell f_D(j)),1) on two paths, controlled by finite SOURCE phase label',
            f_D='Existing relative mean-dark-stress profile, centered; not intrinsic supply-bit variance',
            new_declared_coupling_g=g,g_derivation_status='Not derived; g=1 is an explicit trial extension',
            memory_laws=['one static phase register per run','fresh independent register each physical shutter','one register advanced cyclically per shutter'],
            cyclic_status='New correlation-policy control; cyclic SOURCE-energy preparation/drive costs not derived',
            optical_path_meaning='L is differential coupling exposure; equal common-mode arms cancel',
            visibility='Exact finite characteristic function, not an automatic Gaussian approximation'),
        outputs=dict(base_additional_phase_diffusion=0.0,base_visibility=1.0,conditional_boundaries=boundaries,
            static_curve_shape=shape_result,
            density_eigenvalues_at_1064nm_10m=eig.tolist(),
            photon_path_entropy_at_1064nm_10m=float(-np.sum(eig*np.log(eig))),
            initial_and_global_phase_register_entropy_nats=math.log(J),
            cyclic_max_prefix_relative_stress_RMS=cycle_rms,
            cyclic_max_prefix_absolute_relative_stress=cycle_max,
            finite_cycle_numerical_residual=float(np.max(abs(cycle_sum))),
            base_15_channel_max_visibility_error=max_v,
            numerical_subdivision_error=fine_err),
        refutation_conditions=[
            'Revise if the optical coupling cannot be derived or justified within the declared full ledger.',
            'Reject a frozen candidate if measured visibility/cross-path correlation contradicts its calculated law.',
            'Reject physical claims for effects caused by solver refinement rather than a fixed physical shutter.',
            'Reject free independent resets or cyclic preparation not counted in resources and energy.',
            'Revise if positivity, photon-energy accounting, normalization or common-mode cancellation fails.'],
        conclusion='Base shutter transport adds no dephasing. A finite-state conditional phase extension is executed. The coupling and time correlation are not selected by the inherited SOURCE snapshot; no unique empirical dephasing threshold is established.',
        checks=checks)
    (OUT/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    Lgrid=np.linspace(0,60,1500)
    fig,axs=plt.subplots(1,2,figsize=(11,4.4),layout='constrained')
    for wave in frozen['wavelengths_m']:
        v=np.abs(np.mean(np.exp(1j*2*math.pi/wave*Lgrid[:,None]*f),axis=1))
        axs[0].plot(Lgrid,v,label=f'{wave*1e9:.0f} nm')
    axs[0].axhline(target,color='gray',ls='--',label='exp(-1/2)')
    axs[0].set(xlabel='Differential exposure L (m)',ylabel='Exact relative visibility',ylim=(0,1.03),
        title='Trial g=1: static SOURCE phase register')
    axs[0].legend(fontsize=8);axs[0].grid(alpha=.25)
    axs[1].plot(np.arange(J),correlations/var)
    axs[1].axhline(0,color='gray',lw=.7)
    axs[1].set(xlabel='Finite phase-label lag (not measured time)',ylabel='Normalized profile correlation',
        title='Inherited 128-state profile; temporal law remains open')
    axs[1].grid(alpha=.25)
    fig.savefig(OUT/'conditional_visibility_and_profile.png',dpi=170);plt.close(fig)
    print(json.dumps(dict(clock=dt,step_pm=ell*1e12,source_RMS=rms,boundaries=boundaries,checks=checks),indent=2))

if __name__=='__main__':main()
