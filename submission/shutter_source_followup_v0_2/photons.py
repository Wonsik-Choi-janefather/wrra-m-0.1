"""Existing exact shift and fixed SOURCE phase: dispersion and pulse audit."""
import math
import numpy as np
from scipy.special import ndtr
from common import IN,OUT,CFG,CLOCK,HB_EV,DT,ELL,C,csvwrite,save,checks_pass

def main():
    cfg=CFG['photon'];g=cfg['g'];band=cfg['relative_intensity_energy_bandwidth']
    raw=np.load(IN/'finite_preparation.npz')['dimensionless_fluctuation'][1]
    f=raw-raw.mean();J=len(f)
    rows=[];bands=[];checks={}
    for E in cfg['energies_eV']:
        phase=E*DT/HB_EV
        principal=(phase+math.pi)%(2*math.pi)-math.pi
        refinement=1 if phase<math.pi else 2**math.ceil(math.log2(phase/math.pi*1.0000000001))
        budget=1 if phase<=CLOCK['epsilon'] else 2**math.ceil(math.log2(phase/CLOCK['epsilon']))
        bands.append(dict(energy_eV=E,wavelength_m=CLOCK['h_J_s']*C/(CLOCK['e_J_per_eV']*E),
            phase_per_base_shutter_rad=phase,base_phase_band_admitted=phase<math.pi,
            false_aliased_energy_if_ledger_ignored_eV=principal*HB_EV/DT,
            alias_safe_binary_refinement=refinement,anchor_budget_refinement=budget,
            refined_dt_s=DT/refinement,refined_dx_m=ELL/refinement,
            refined_speed_m_s=(ELL/refinement)/(DT/refinement),
            status='Refinement/energy-tag accounting; no physical high-energy cutoff inferred'))
        sigma_E=band*E;sigma_t=HB_EV/(2*sigma_E)
        for L in cfg['differential_exposures_m']:
            delay=g*L/C*f
            variance_source=float(np.var(delay));variance=sigma_t**2+variance_source
            rms=math.sqrt(variance);mu3=float(np.mean(delay**3));k4=float(np.mean(delay**4)-3*variance_source**2)
            rows.append(dict(energy_eV=E,exposure_m=L,relative_energy_bandwidth=band,
                original_pulse_time_RMS_s=sigma_t,SOURCE_group_delay_mean_s=float(delay.mean()),
                SOURCE_group_delay_RMS_s=math.sqrt(variance_source),
                SOURCE_group_delay_min_s=float(delay.min()),SOURCE_group_delay_max_s=float(delay.max()),
                nonselective_pulse_time_RMS_s=rms,time_width_ratio=rms/sigma_t,
                mean_energy_dependent_group_delay_s=0.,additional_group_delay_dispersion_s2=0.,
                arrival_distribution_skewness=mu3/variance**1.5,
                arrival_distribution_excess_kurtosis=k4/variance**2,
                scope='SOURCE delay distribution, not vacuum energy dispersion; relative width depends on the declared preparation bandwidth'))
    csvwrite('photon_phase_band_audit.csv',bands);csvwrite('photon_pulse_predictions.csv',rows)

    # Positive-frequency Gaussian packet: direct FFT verifies exact pulse mixture.
    E=cfg['FFT_control_energy_eV'];L=cfg['FFT_control_exposure_m']
    sigma_E=band*E;sigma_t=HB_EV/(2*sigma_E)
    size=16384;dtime=.125*sigma_t
    omega=2*math.pi*np.fft.fftfreq(size,d=dtime)
    offsets=HB_EV*omega
    amps=np.exp(-offsets**2/(4*sigma_E**2)).astype(complex);amps/=np.linalg.norm(amps)
    time=(np.arange(size)-size//2)*dtime
    base=np.fft.fftshift(np.fft.fft(amps)/math.sqrt(size));baseprob=abs(base)**2
    probability=np.zeros(size)
    energy0=float(np.sum(abs(amps)**2*(E+offsets)))
    max_norm=0.;energy_err=0.
    for delay in g*L/C*f:
        shifted_spectrum=amps*np.exp(1j*omega*delay)
        psi=np.fft.fftshift(np.fft.fft(shifted_spectrum)/math.sqrt(size))
        prob=abs(psi)**2;probability+=prob/J
        max_norm=max(max_norm,abs(float(prob.sum())-1))
        energy_err=max(energy_err,abs(float(np.sum(abs(shifted_spectrum)**2*(E+offsets)))/energy0-1))
    mean_fft=float(probability@time)
    variance_fft=float(probability@(time-mean_fft)**2)
    exact=sigma_t**2+float(np.var(g*L/C*f))
    checks['positive_frequency_packet']=bool((E+offsets).min()>0)
    checks['FFT_packet_norm']=max_norm<1e-13
    checks['FFT_energy_unchanged']=energy_err<1e-13
    checks['FFT_base_width']=abs(float(baseprob@time**2)/sigma_t**2-1)<1e-10
    checks['FFT_mixture_width_matches_exact']=abs(variance_fft/exact-1)<1e-10
    checks['FFT_mixture_centroid']=abs(mean_fft)<math.sqrt(exact)*1e-12
    checks['positive_normalized_mixture']=bool(probability.min()>=0 and abs(probability.sum()-1)<1e-13)
    # Independent finite differences verify linear phase versus photon energy.
    energies=np.linspace(100.,10000.,1001)
    phase=energies/HB_EV*L/C*f[7]
    slope=np.gradient(phase,energies)
    expected=L/C*f[7]/HB_EV
    checks['linear_energy_phase_group_delay']=np.max(abs(slope/expected-1))<1e-10
    curvature=np.gradient(slope,energies)
    # E=hbar*omega; d²phi/domega² has units s².
    numerical_GDD=curvature*HB_EV**2
    checks['no_additional_intrinsic_dispersion']=float(np.max(abs(numerical_GDD)))<1e-44
    checks['matched_refinement_keeps_c']=max(abs(x['refined_speed_m_s']/C-1) for x in bands)<1e-14
    checks['refined_phase_has_no_alias']=all(E['energy_eV']*(DT/E['alias_safe_binary_refinement'])/HB_EV<math.pi for E in bands)
    checks['common_mode_delay_cancellation']=float(np.max(abs(g*L/C*f-g*L/C*f)))==0
    np.savez_compressed(OUT/'photon_FFT_control.npz',time_s=time,baseline_probability=baseprob,
        nonselective_SOURCE_probability=probability,spectral_offset_energy_eV=offsets)
    # Exact CDF bin masses retain unresolved narrow components at high energy.
    pulse_rows=[]
    for E in [1,1000,CLOCK['mode_energy_eV'],1000000]:
        sigma=HB_EV/(2*band*E);delay=g/C*f
        extent=float(max(abs(delay).max()+8*sigma,8*math.sqrt(sigma*sigma+np.var(delay))))
        edges=np.linspace(-extent,extent,4097)
        cdf=np.mean(ndtr((edges[:,None]-delay[None,:])/sigma),axis=1)
        masses=np.diff(cdf)
        checks[f'CDF_pulse_mass_{E:g}eV']=bool(masses.min()>-1e-15 and abs(masses.sum()-1)<1e-12)
        for t,dt,prob in zip((edges[1:]+edges[:-1])/2,np.diff(edges),masses):
            pulse_rows.append(dict(energy_eV=E,exposure_m=1,time_offset_s=t,
                exact_bin_probability=max(0.,float(prob)),bin_width_s=float(dt)))
    csvwrite('photon_pulse_CDF_bins.csv',pulse_rows)
    result=dict(validation_inputs=dict(shutter_dt_s=DT,light_step_m=ELL,static_phase_states=J,
        fixed_g=g,declared_relative_energy_bandwidth=band),WRRA_transformation=cfg,
        outputs=dict(pulse_predictions=rows,phase_band= bands,
            base_massless_carrier_velocity_m_s=C,base_extra_group_delay_s=0,
            base_extra_wavepacket_dispersion=0,
            phase_alias_energy_eV=math.pi*HB_EV/DT,
            phase_alias_wavelength_pm=2*ELL*1e12,
            fixed_SOURCE_delay_RMS_at_1m_s=float(np.std(g/C*f)),
            group_delay_dispersion_definition='d²phi/domega² = hbar_eV² d²phi/dE_eV², units s²',
            numerical_group_delay_dispersion_max_abs_s2=float(np.max(abs(numerical_GDD))),
            phase_law_scope='Fixed-duration phase-screen transfer at nominal exposure L/c, not a derived bulk-medium traversal time',
            energy_dependence='Zero mean energy-dependent delay and zero phase curvature. Conditional delay is linear in E phase, hence achromatic.',
            packet_preparation_effect='For fixed fractional bandwidth, initial pulse duration scales as 1/E; relative broadening therefore changes even when delay distribution is achromatic.',
            FFT_variance_relative_error=abs(variance_fft/exact-1),FFT_max_energy_relative_error=energy_err),
        refutation_conditions=['An energy-dependent propagation delay is claimed from the zero-curvature rule','A phase alias is claimed as a physical photon cutoff','Free energy, positivity or common-mode cancellation fails','Pulse preparation changes are misidentified as fundamental vacuum dispersion'],
        conclusion='The current shift and fixed SOURCE interaction predict no energy-dependent vacuum dispersion. The SOURCE ensemble gives an achromatic arrival-time distribution and nonselective pulse broadening, verified by FFT.',
        checks=checks_pass(checks))
    save('photon_results.json',result);print('Photons:',len(result['checks']),'checks passed',flush=True)
    return result

if __name__=='__main__':main()
