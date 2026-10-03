"""Falsifiers for path clocks, finite spectral boundaries and phase branches."""
from pathlib import Path
import copy
import json
import math
import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm
import compute as m

ROOT=Path(__file__).resolve().parent
def main():
    cfg=json.loads((ROOT/'parameters.json').read_text());before=m.m09.digest(cfg);r=m.run(cfg,ROOT/'results');checks=[]
    def check(name,passed,evidence):
        checks.append({'id':len(checks)+1,'check':name,'passed':bool(passed),'evidence':evidence})
        if not passed:raise AssertionError(name+': '+str(evidence))
    close=lambda a,b,t=1e-10:abs(a-b)<=t*max(abs(a),abs(b),1e-300)
    b=cfg['baseline_0_11'];old=b['baseline_0_10'];u=r['units'];unit=b['SI'];N=cfg['spectra']['mode_lattice_N']
    previous=json.loads((ROOT.parent/'wrra_m_0_11/results/results.json').read_text());pv=json.loads((ROOT.parent/'wrra_m_0_11/results/verification.json').read_text());v10=json.loads((ROOT.parent/'wrra_m_0_10/results/verification.json').read_text())
    check('frozen_0_11_and_all_60_inherited_checks',m.m09.digest(b)==cfg['provenance']['baseline_0_11_input_sha256'] and pv['passed'] and pv['check_count']==28 and v10['passed'] and v10['check_count']==32,{'frozen_input_hash':m.m09.digest(b),'inherited_checks':60})
    check('proper_shutter_units_use_the_frozen_mass_scale',close(u['delta_tau_s']*u['mu_E_J']/u['hbar_J_s'],cfg['clock']['phase_step_epsilon']) and close(u['mu_E_eV'],previous['final_outputs']['mass_mode_scale_eV']),{'delta_tau_s':u['delta_tau_s'],'epsilon':cfg['clock']['phase_step_epsilon']})
    check('Planck_time_is_comparison_not_measured_minimum',cfg['clock']['physical_minimum_time_claim'] is False and u['delta_tau_over_Planck']>1e20 and close(u['c_delta_tau_m'],unit['c_m_s']*u['delta_tau_s']),{'delta_over_tP':u['delta_tau_over_Planck'],'minimum_time_claim':False})
    trial=copy.deepcopy(cfg);trial['clock']['phase_step_epsilon']*=2
    check('changing_shutter_granularity_does_not_refit_spectrum',close(m.units(trial)['delta_tau_s'],2*u['delta_tau_s']) and np.max(abs(m.fold_operator(trial)[2]-m.fold_operator(cfg)[2]))==0,{'step_multiplier':2,'mass_refit':False})
    flat=r['flat_clocks'];target=[64,51.2,38.4]
    check('flat_worldline_clock_rates_and_residuals',all(abs(x['tick_coordinate']-v)<1e-10 and abs(x['complete_ticks']+x['residual_tick_fraction']-v)<1e-10 for x,v in zip(flat[:3],target)),{'proper_tick_coordinates':target,'complete_ticks':[x['complete_ticks'] for x in flat[:3]]})
    check('null_paths_have_no_rest_clock_or_frozen_photon_claim',flat[-1]['proper_s']==0 and flat[-1]['complete_ticks'] is None and flat[-1]['coherent_overlap'] is None,flat[-1])
    boost=cfg['clock']['lorentz_boost_beta'];gamma=1/math.sqrt(1-boost**2);errs=[]
    for beta in (0,.2,.6,.8):
        dtp=gamma*(1-boost*beta);dxp=gamma*(beta-boost);errs.append(abs(math.sqrt(dtp*dtp-dxp*dxp)-math.sqrt(1-beta*beta)))
    check('Lorentz_transformed_event_intervals_preserve_proper_time',max(errs)<1e-14,{'maximum_interval_error':max(errs),'boost_beta':boost})
    path=r['accelerated_worldline'];rows=path['refinement'];berr=max(abs(x['proper_over_T']-x['boosted_proper_over_T']) for x in rows)
    check('accelerated_worldline_chords_preserve_proper_time_under_boost',berr<1e-14,{'maximum_boosted_path_error':berr})
    ratios=[a['absolute_ratio_error']/z['absolute_ratio_error'] for a,z in zip(rows,rows[1:])]
    check('halved_worldline_steps_converge_quadratically',min(ratios)>3.99 and max(ratios)<4.01 and rows[-1]['absolute_ratio_error']<1e-6,{'error_improvement_factors':ratios,'last_error':rows[-1]['absolute_ratio_error']})
    b0,b1=path['beta_coefficients'];events=path['events'];event_error=max(abs(quad(lambda s:math.sqrt(1-(b0+b1*s)**2),0,e['coordinate_time_over_T'],epsabs=1e-12,epsrel=1e-12)[0]*cfg['clock']['reference_ticks']-e['proper_frame']) for e in events)
    check('proper_shutter_events_are_monotone_and_match_path_integrals',event_error<1e-10 and all(a['coordinate_time_over_T']<z['coordinate_time_over_T'] for a,z in zip(events,events[1:])),{'event_count':len(events),'maximum_tick_error':event_error})
    local=r['local_clocks'];static=local[:-1]
    check('finite_patch_boundary_clock_and_redshift_order',static[-1]['phi_over_c2']==0 and static[-1]['lapse']==1 and all(a['lapse']<z['lapse'] for a,z in zip(static,static[1:])),{'radii_kpc':[x['radius_kpc'] for x in static],'lapses':[x['lapse'] for x in static]})
    base=m.m09.address_base(old['upstream_0_9']);ef=m.m09.effects(old['upstream_0_9'],base);cal,mu,src,o=m.m11.physical_context(b,base,ef)
    rad=8.2;h=.001;kpc=1000*src['parsec_m'];derivative=(m.potential_ratio(rad+h,src,o['aT_m_s2'])-m.potential_ratio(rad-h,src,o['aT_m_s2']))*unit['c_m_s']**2/(2*h*kpc)
    g=float(m.m10.m06.m05.plummer(np.array([rad*kpc]),src,o['aT_m_s2'])['g'][0])
    check('independent_potential_derivative_matches_inherited_gravity',abs(derivative/g-1)<1e-8,{'relative_gradient_error':derivative/g-1,'finite_boundary_kpc':src['patch_radius_kpc']})
    circle=local[-1]
    check('inherited_rotation_enters_moving_local_clock',abs(circle['beta_local']*unit['c_m_s']/1000-207.51090512661662)<1e-8 and circle['lapse']<static[1]['lapse'],{'local_speed_km_s':circle['beta_local']*unit['c_m_s']/1000,'moving_lapse':circle['lapse']})
    cosmic=r['cosmic_clocks'];comoving=cosmic[::2]
    check('uniform_FRW_time_integral_is_additive',abs(comoving[0]['coordinate_interval_H0_t']+comoving[1]['coordinate_interval_H0_t']-comoving[2]['coordinate_interval_H0_t'])<1e-12,{'intervals':[x['coordinate_interval_H0_t'] for x in comoving]})
    check('peculiar_worldline_proper_time_uses_same_expansion_history',all(close(moving['proper_interval_s'],.8*rest['proper_interval_s']) for rest,moving in zip(cosmic[::2],cosmic[1::2])),{'peculiar_beta':.6,'proper_time_ratio':.8})
    uniform=[x for x in previous['cases'] if x['case_name'].startswith('uniform_a')]
    check('clock_background_keeps_all_uniform_0_11_outputs',all(close(x['H_over_H0']**2,(b['targets']['f_phi']+b['targets']['f_c'])/x['scale_factor']**3+o['f_b']) for x in uniform) and close(previous['reference']['deceleration_q'],-.52855),{'uniform_cases':len(uniform),'q0':previous['reference']['deceleration_q']})
    n,F,e,H=m.fold_operator(cfg);basis_error=float(np.linalg.norm(F.conj().T@F-np.eye(N)))
    check('finite_spectral_basis_and_fold_Hamiltonian_are_unitary_Hermitian',basis_error<1e-11 and np.linalg.norm(H-H.conj().T)/np.linalg.norm(H)<1e-14,{'basis_error':basis_error,'finite_modes':N})
    plain={x['mode']:x['energy_eV'] for x in r['fold_modes'] if x['boundary_phase']==0}
    check('periodic_fold_rest_spectrum_reproduces_electron_mode_23',close(plain[23],u['electron_energy_eV']) and close(plain[-23],plain[23]) and plain[0]==0 and all(close(plain[j],abs(j)*u['mu_E_eV']) for j in plain),{'electron_energy_eV':plain[23],'zero_mode_eV':plain[0]})
    twisted={x['mode']:x['energy_eV'] for x in r['fold_modes'] if x['boundary_phase']==.5}
    boundary_error=float(np.max(abs(np.exp(2j*math.pi*(n+.5))-np.exp(1j*math.pi))))
    nt,Ft,et,Ht=m.fold_operator(cfg,.5);twisted_residual=float(np.linalg.norm(Ht@Ft-Ft*et)/np.linalg.norm(Ht))
    check('antiperiodic_boundary_changes_modes_without_hidden_refit',close(twisted[0],.5*u['mu_E_eV']) and close(twisted[1],twisted[-2]) and abs(twisted[23]-plain[23])>10000 and boundary_error<1e-12 and twisted_residual<1e-11,{'periodic_mode23_eV':plain[23],'antiperiodic_mode23_eV':twisted[23],'physical_boundary_error':boundary_error,'shifted_generator_residual':twisted_residual,'refit':False})
    operator_errors=[];phase_errors=[]
    for kind in ('periodic','dirichlet'):
        nn,ff,ee,hh=m.cavity_operator(cfg,kind);operator_errors.append(float(np.linalg.norm(ff.conj().T@ff-np.eye(N))))
        phase=m.phase_readout(hh,u['delta_tau_s'],cfg);phase_errors.append(float(np.max(abs(np.sort(ee)-phase['principal_energy_eV_sorted']))))
        assert np.linalg.norm(hh-hh.conj().T)==0 and np.linalg.eigvalsh(hh).min()>0
    check('both_spatial_boundaries_have_positive_Hermitian_operators',max(operator_errors)<1e-11,{'maximum_basis_error':max(operator_errors),'boundaries':['periodic','dirichlet']})
    cav=r['cavity_modes'];per=[x for x in cav if x['boundary']=='periodic'];dire=[x for x in cav if x['boundary']=='dirichlet']
    check('periodic_and_Dirichlet_zero_ground_modes_are_distinct',per[0]['kinetic_energy_eV']==0 and dire[0]['mode']==1 and dire[0]['kinetic_energy_eV']>0,{'periodic_ground_kinetic_eV':0,'Dirichlet_ground_kinetic_eV':dire[0]['kinetic_energy_eV']})
    L=dire[0]['length_m'];independent=math.hypot(u['electron_energy_eV'],u['hbar_J_s']*unit['c_m_s']*math.pi/L/unit['eV_J'])
    check('spatial_energy_matches_independent_SI_dispersion',close(independent,dire[0]['energy_eV']) and max(abs(math.sin(math.pi*j)) for j in range(1,N+1))<1e-13,{'SI_ground_energy_eV':independent,'zero_endpoint_wavefunctions':True})
    spacing=r['finite_volume_spacing'];gapratios=[a['first_kinetic_gap_eV']/z['first_kinetic_gap_eV'] for a,z in zip(spacing,spacing[1:])]
    check('finite_length_controls_change_momentum_and_energy_spacing',all(close(a['momentum_step_c_eV'],2*z['momentum_step_c_eV']) for a,z in zip(spacing,spacing[1:])) and all(3.99<x<4.01 for x in gapratios),{'finite_lengths_m':[x['length_m'] for x in spacing],'energy_gap_ratios':gapratios})
    free=r['free_dispersion'];positive=[x for x in free if x['pc_over_mu']>=0]
    check('same_shutter_accepts_continuous_noninteger_free_momenta',any(x['pc_over_mu']==.1 for x in positive) and all(a['energy_eV']<z['energy_eV'] for a,z in zip(positive,positive[1:])) and close(next(x for x in free if x['pc_over_mu']==.1)['energy_eV'],next(x for x in free if x['pc_over_mu']==-.1)['energy_eV']),{'noninteger_momentum_probes':[x['pc_over_mu'] for x in positive],'discrete_time_implies_discrete_momentum':False})
    fd=r['finite_difference_controls'];ratios=[abs(a['relative_mass_error']/z['relative_mass_error']) for a,z in zip(fd,fd[1:])]
    check('finite_difference_mass_error_decreases_without_electron_refit',all(x['relative_mass_error']<0 and x['calibration_refit'] is False for x in fd) and min(ratios)>3.9 and max(ratios)<4.1,{'relative_errors':[x['relative_mass_error'] for x in fd],'refinement_factors':ratios})
    check('independent_update_eigenphases_recover_all_three_spectra',max(phase_errors+[r['phase_recovery']['max_spectral_phase_energy_error_eV']])<1e-6 and r['phase_recovery']['unitarity_error']<1e-11,{'fold_energy_error_eV':r['phase_recovery']['max_spectral_phase_energy_error_eV'],'spatial_energy_errors_eV':phase_errors})
    phase=m.phase_readout(H,u['delta_tau_s'],cfg);shift=u['phase_bandwidth_eV'];shifted=m.phase_readout(H+shift*np.eye(N),u['delta_tau_s'],cfg)
    alias_error=float(np.linalg.norm(phase['U']-shifted['U']))
    check('one_unitary_does_not_identify_integer_energy_branch',alias_error<1e-10,{'energy_shift_eV':shift,'same_unitary_error':alias_error})
    alias=r['alias_control']
    check('owned_branch_restores_aliased_energies_and_naive_branch_fails',alias['nonzero_branch_modes']>0 and alias['max_naive_sorted_energy_error_eV']>1e5 and alias['max_owned_branch_error_eV']<1e-6,alias)
    p=old['upstream_0_9']['baseline_0_8']['ledger_0_7']['carrier_and_background'];car=m.m10.m06.Carrier(p['lattice_N'],p['noncommuting_test_strength']);EH=m.m10.energy_operator(old,cal,mu,car,1);E0=cal['ucrit_J_m3']*old['reference_volume_m3'];xi=4;proper=xi*u['hbar_J_s']/E0
    SI=expm(-1j*(EH/E0)*(E0*proper/u['hbar_J_s']));legacy=expm(-1j*xi*EH/E0)
    check('fixed_volume_SI_phase_exactly_matches_converted_legacy_coordinate',np.linalg.norm(SI-legacy)<1e-11 and close(r['physical_ledger_updates'][1]['legacy_dimensionless_coordinate'],E0*u['delta_tau_s']/u['hbar_J_s']),{'converted_proper_s':proper,'matrix_error':float(np.linalg.norm(SI-legacy))})
    evolution=r['physical_ledger_updates'];Eref=evolution[0]['total_energy_J'];enerr=max(abs(x['total_energy_J']/Eref-1) for x in evolution)
    check('physical_proper_time_updates_conserve_energy_and_state',enerr<1e-10 and all(abs(x['state_trace']-1)<1e-10 and x['minimum_state_eigenvalue']>-1e-12 for x in evolution),{'maximum_energy_relative_error':enerr,'proper_frames':[x['proper_frame'] for x in evolution]})
    change=max(x['D_load'] for x in evolution)-min(x['D_load'] for x in evolution)
    check('same_SI_energy_operator_has_actual_internal_exchange',change>1e-4,{'D_load_range':change,'energy_operator_replaced':False})
    lc=r['legacy_clock_comparison']
    check('old_slow_expansion_clock_is_not_silently_identified_with_SI_phase',lc['old_expansion_clock_is_physical_SI_phase'] is False and close(lc['old_frequency_over_SI_frequency'],u['hbar_J_s']*p['information_clock_over_H0']*o['H0_s_minus1']/E0) and lc['old_frequency_over_SI_frequency']<1e-40,lc)
    errors=[];bounds=[];A=H/u['mu_E_eV'];Anorm=np.linalg.norm(A,2)
    for step in (.001,.0005,.00025):
        difference=1j*(expm(-1j*step*A)-np.eye(N))/step-A
        errors.append(float(np.linalg.norm(difference)/np.linalg.norm(A)))
        bounds.append({'step':step,'operator_norm_error':float(np.linalg.norm(difference,2)),
                       'finite_step_bound':float(step*Anorm**2/2)})
    check('small_step_update_converges_to_the_same_generator',all(1.99<a/z<2.01 for a,z in zip(errors,errors[1:])) and all(x['operator_norm_error']<=x['finite_step_bound']*(1+1e-10) for x in bounds),{'generator_relative_errors':errors,'finite_positive_step_bounds':bounds})
    j22=int(np.flatnonzero(n==22)[0]);j23=int(np.flatnonzero(n==23)[0]);psi=(F[:,j22]+F[:,j23])/math.sqrt(2);overlap_errors=[]
    for x in flat[:3]:
        tau=x['proper_s']
        U=(F*np.exp(-1j*e*unit['eV_J']*tau/u['hbar_J_s']))@F.conj().T
        overlap_errors.append(abs(float(abs(np.vdot(psi,U@psi))**2)-x['coherent_overlap']))
    check('coherent_clock_readout_matches_full_mode_update',max(overlap_errors)<1e-12,{'maximum_overlap_error':max(overlap_errors),'physical_measurement_records':0})
    invalid=[]
    for section,key,value in [('clock','phase_step_epsilon',0),('clock','physical_minimum_time_claim',True),('clock','lorentz_boost_beta',1),('clock','flat_speed_probes',[1.2]),('clock','local_radius_probes_kpc',[201]),('clock','scale_factor_intervals',[[1,0]]),('spectra','cavity_length_over_length_unit',0),('spectra','fold_boundary_phases',[1]),('spectra','report_fold_modes',[128]),('spectra','alias_phase_step_epsilon',float('nan'))]:
        trial=copy.deepcopy(cfg);trial[section][key]=value;invalid.append(trial)
    trial=copy.deepcopy(cfg);trial['physical_records']=[1];invalid.append(trial)
    for section,key,value in [('clock','potential_boundary','Phi(infinity)=0'),('spectra','spatial_boundaries',['infinite']),('spectra','operator_rule','unreported')]:
        trial=copy.deepcopy(cfg);trial[section][key]=value;invalid.append(trial)
    trial=copy.deepcopy(cfg);trial['baseline_0_11']['targets']['H0_km_s_Mpc']=70;invalid.append(trial)
    rejected=0
    for trial in invalid:
        try:m.validate(trial)
        except ValueError:rejected+=1
    check('invalid_clock_boundary_inputs_and_unexecuted_records_are_rejected',rejected==len(invalid),{'invalid_cases':len(invalid),'rejected':rejected})
    check('execution_keeps_inputs_and_scope_frozen',m.m09.digest(cfg)==before and r['physical_records']==[] and lc['old_expansion_clock_is_physical_SI_phase'] is False,{'input_sha256':before,'measurement_records':0})
    report={'version':r['version'],'passed':True,'check_count':len(checks),'inherited_check_count':60,'input_hash_sha256':before,'checks':checks};(ROOT/'results/verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    print(json.dumps({'passed':True,'checks':len(checks),'inherited_checks':60,'delta_tau_s':u['delta_tau_s'],'phase_error_eV':r['phase_recovery']['max_spectral_phase_energy_error_eV']}))

if __name__=='__main__':main()
