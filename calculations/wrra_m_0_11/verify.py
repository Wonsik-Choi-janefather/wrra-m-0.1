"""Dependency, degeneracy and inherited-physics falsifiers for 0.11."""
from pathlib import Path
import copy
import json
import math
import numpy as np
import compute as m

ROOT=Path(__file__).resolve().parent

def main():
    cfg=json.loads((ROOT/'parameters.json').read_text());before=m.m09.digest(cfg)
    r=m.run(cfg,ROOT/'results');checks=[]
    def check(name,passed,evidence):
        checks.append({'id':len(checks)+1,'check':name,'passed':bool(passed),'evidence':evidence})
        if not passed:raise AssertionError(name+': '+str(evidence))
    close=lambda x,y,t=1e-10:abs(x-y)<=t*max(abs(x),abs(y),1e-300)
    old=cfg['baseline_0_10'];o=r['final_outputs'];cal=r['calibration_0_10_bridge'];ref=r['reference'];u=cfg['SI'];v=cfg['targets']
    baseline=json.loads((ROOT.parent/'wrra_m_0_10/results/results.json').read_text())
    inherited=json.loads((ROOT.parent/'wrra_m_0_10/results/verification.json').read_text())
    check('frozen_0_10_input_and_inherited_checks',m.m09.digest(old)==cfg['provenance']['baseline_0_10_input_sha256'] and inherited['passed'] and inherited['check_count']==32,{'baseline_hash':m.m09.digest(old),'inherited_checks':32})
    check('exact_order_and_partial_input_ownership',all(list(x['supplied_inputs'])==list(m.ORDER[:i+1]) and x['remaining_calibrations']==list(m.ORDER[i+1:]) for i,x in enumerate(r['sequential_calibration'])),{'order':list(m.ORDER)})
    hidden=0
    for i in range(1,6):
        prefix=dict(list(v.items())[:i]);t=copy.deepcopy(cfg)
        for k in m.ORDER[i:]:t['targets'][k]=float('nan')
        if m.prefix_outputs(t,prefix)==m.prefix_outputs(cfg,prefix):hidden+=1
    check('future_targets_are_not_read_by_partial_stages',hidden==5,{'independent_prefixes':hidden})
    counts=[len(x['outputs']) for x in r['sequential_calibration']]
    check('stages_add_outputs_without_retracting_prior_outputs',all(all(x['outputs'].get(k)==value for k,value in prior['outputs'].items()) for prior,x in zip(r['sequential_calibration'],r['sequential_calibration'][1:])),{'available_output_counts':counts})
    check('G_sets_action_and_response_normalization',close(o['Einstein_action_coefficient_J_per_m']*o['Einstein_response_m_J'],.5) and close(o['Planck_length_m']/o['Planck_time_s'],u['c_m_s']),{'action_J_per_m':o['Einstein_action_coefficient_J_per_m'],'response_m_J':o['Einstein_response_m_J']})
    H=v['H0_km_s_Mpc']*1000/(1e6*u['parsec_m']);crit=3*H**2*u['c_m_s']**2/(8*math.pi*v['G_SI'])
    check('H0_conversion_and_critical_density',close(o['H0_s_minus1'],H) and close(o['ucrit_J_m3'],crit) and close(o['Hubble_length_m']/o['Hubble_time_s'],u['c_m_s']),{'H0_s_minus1':H,'ucrit_J_m3':crit})
    check('physical_fractions_close_one_energy_budget',close(v['f_phi']+v['f_c']+o['f_b'],1) and close(o['u_phi_J_m3']+o['u_c_J_m3']+o['u_b_J_m3'],crit) and close(o['f_h'],1-v['f_phi']),{'f_phi':v['f_phi'],'f_c':v['f_c'],'f_b':o['f_b'],'f_h':o['f_h']})
    arithmetic=old['upstream_0_9']['upstream']['targets']
    check('arithmetic_and_physical_targets_remain_distinct',arithmetic=={'phenotype':.05,'resident_nonphenotype':.268,'return':.682} and cal['target_energy_fractions']['phenotype']==.0493 and cal['target_energy_fractions']['resident_nonphenotype']==.265,{'arithmetic':arithmetic,'physical':cal['target_energy_fractions']})
    check('three_once_fitted_SI_coefficients_reproduce_reference',all(close(ref['sector_density_J_m3'][s],crit*cal['target_energy_fractions'][s]) for s in m.SECTORS) and min(cal['eta_J_m3'].values())>0,{'eta_J_m3':cal['eta_J_m3']})
    regression=[]
    for x,y in zip(r['cases'],baseline['cases']):
        assert x['case_name']==y['case_name']
        regression.append(max(abs(x['total_density_J_m3']-y['total_density_J_m3'])/crit,abs(x['total_pressure_Pa']-y['total_pressure_Pa'])/crit,abs(x['deceleration_q']-y['deceleration_q']),abs(x['local_readout']['v_total_km_s']-y['local_readout']['v_total_km_s'])/300))
    check('all_nine_0_10_cases_are_retained',len(regression)==9 and max(regression)<1e-10,{'cases':9,'maximum_scaled_difference':max(regression)})
    check('reference_gravity_expansion_and_conditional_lensing',close(ref['deceleration_q'],o['q0']) and abs(ref['local_readout']['v_total_km_s']-207.51090512661662)<1e-8 and abs(ref['local_readout']['finite_patch_lensing']['alpha_patch_arcsec']-.5355865105583804)<1e-10,{'q':ref['deceleration_q'],'v_km_s':ref['local_readout']['v_total_km_s'],'lens_arcsec':ref['local_readout']['finite_patch_lensing']['alpha_patch_arcsec']})
    N=old['upstream_0_9']['baseline_0_8']['ledger_0_7']['carrier_and_background']['lattice_N'];car=m.m10.m06.Carrier(N,8)
    rho=m.m10.m07.state_from_recipe(car,{'kind':'packet','modes':[8,16,24],'weights':[1/3]*3})
    mu=np.array([cal['reference_address_moments'][s] for s in m.SECTORS]);errors=[]
    for a in (.5,1,2):
        V=old['reference_volume_m3']*a**3;h=V*1e-4
        def energy(volume):return float(np.trace(rho@m.m10.energy_operator(old,cal,mu,car,(volume/old['reference_volume_m3'])**(1/3))).real)
        fd=-(-energy(V+2*h)+8*energy(V+h)-8*energy(V-h)+energy(V-2*h))/(12*h)
        exact=m.m10.ledger(old,cal,mu,car,rho,a,include_local=False)['total_pressure_Pa'];errors.append(abs(fd-exact)/crit)
    check('independent_volume_derivative_at_three_volumes',max(errors)<1e-9,{'maximum_error_over_ucrit':max(errors)})
    Q=16*math.pi*v['G_SI']*o['u_hidden_J_m3']/u['c_m_s']**4
    check('weighted_twist_and_length_coefficient_units',close(Q,o['weighted_twist_hidden_m_minus2']) and close(o['length_coefficient_m']**2*Q,1) and close(o['eta_load_J_m3']*2,o['u_hidden_J_m3']),{'zeta_kappa_squared_m_minus2':Q,'length_coefficient_m':o['length_coefficient_m']})
    zeta=7.;k=math.sqrt(Q/zeta);rescale=11.
    check('stiffness_twist_rescaling_is_unidentifiable',close(zeta*k*k,(zeta*rescale)*(k/math.sqrt(rescale))**2) and 'W0' not in o,{'rescaling_factor':rescale,'W0_assigned':False,'actual_cosmic_length_assigned':False})
    modes={x['mode']:x['rest_energy_eV'] for x in r['mass_modes']}
    check('electron_mode_23_fixes_mass_unit',cfg['mass_construction']['electron_mode']==23 and close(23*o['mass_mode_scale_eV'],v['electron_energy_eV']) and close(modes[23],v['electron_energy_eV']),{'n_e':23,'mu_eV':o['mass_mode_scale_eV']})
    check('mass_modes_have_sign_symmetry_and_zero_intercept',all(close(modes[n],modes[-n]) for n in (1,2,3,23)) and modes[0]==0,{'generic_mass_modes':r['mass_modes'],'particle_label_prediction':False})
    check('electron_SI_mass_energy_conversion',close(o['electron_energy_J'],v['electron_energy_eV']*u['eV_J']) and close(o['electron_mass_kg']*u['c_m_s']**2,o['electron_energy_J']),{'energy_J':o['electron_energy_J'],'mass_kg':o['electron_mass_kg']})
    check('electron_units_do_not_duplicate_cosmic_energy',close(r['energy_operator_in_electron_units']*o['electron_energy_J'],ref['total_energy_J']) and close(ref['total_density_J_m3'],crit),{'total_energy_in_electron_units':r['energy_operator_in_electron_units'],'added_electron_budget_J':0})
    J=np.array(r['dependency_map']['log_sensitivity']);expected=np.array([[-1,0,0,0,0],[-1,2,0,0,0],[-1,2,-v['f_phi']/(1-v['f_phi']),0,0],[-1,2,0,1,0],[0,0,0,0,1]])
    check('five_anchor_dependency_rank_and_analytic_Jacobian',r['dependency_map']['rank']==5 and np.max(abs(J-expected))<1e-8,{'rank':r['dependency_map']['rank'],'maximum_Jacobian_error':float(np.max(abs(J-expected))),'scope':'conditional on fixed constitutive choices'})
    probes=r['input_response_probes']
    ep=[x for x in probes if x['changed_input']=='electron_energy_eV']
    check('electron_anchor_changes_mass_unit_but_not_macro_budget',all(close(x['mu_eV'],o['mass_mode_scale_eV']*x['multiplier']) and close(x['ucrit_J_m3'],crit) and close(x['q0'],o['q0']) and close(x['v_km_s'],ref['local_readout']['v_total_km_s']) for x in ep),{'electron_input_probes':ep})
    gp=[x for x in probes if x['changed_input']=='G_SI'];hp=[x for x in probes if x['changed_input']=='H0_km_s_Mpc']
    check('G_and_H0_scalings_are_executed',all(close(x['ucrit_J_m3'],crit/x['multiplier']) and close(x['aT_m_s2'],o['aT_m_s2']) for x in gp) and all(close(x['ucrit_J_m3'],crit*x['multiplier']**2) and close(x['aT_m_s2'],o['aT_m_s2']*x['multiplier']) for x in hp),{'G_probes':gp,'H0_probes':hp})
    frac=[x for x in probes if x['changed_input'] in ('f_phi','f_c')]
    check('physical_fraction_responses_are_separate_from_address_refit',all(close(x['q0'],o['q0']+1.5*v[x['changed_input']]*(x['multiplier']-1)) and close(x['mu_eV'],o['mass_mode_scale_eV']) for x in frac),{'fraction_probes':frac,'arithmetic_refit':False})
    rc=r['address_reparameterization']
    check('address_alpha_and_beta_are_reexpressed_from_two_legacy_targets',abs(rc['alpha']-rc['frozen_alpha_addr'])<1e-10 and abs(rc['derived_effective_beta']-rc['frozen_beta_scalar'])<1e-10 and rc['independent_beta_required'] is False and rc['electromagnetic_alpha'] is None,rc)
    ap=r['frozen_coefficient_address_probes']
    check('fixed_energy_coefficients_retain_address_rule_response',abs(ap[0]['physical']['deceleration_q']-ap[1]['physical']['deceleration_q'])>1e-4,{'K4_q':ap[0]['physical']['deceleration_q'],'K16_q':ap[1]['physical']['deceleration_q'],'refit':False})
    dg=r['response_shape_degeneracy']
    check('same_five_anchors_allow_different_unfitted_response_shapes',all(close(x['reference_q'],o['q0']) for x in dg) and abs(dg[0]['K4_q']-dg[1]['K4_q'])>1e-5,dg)
    E=ref['total_energy_J'];ex=r['internal_exchange']
    check('inherited_internal_exchange_conserves_energy_and_state',max(abs(x['exchange_sum_J'])/E for x in ex)<1e-10 and all(abs(x['state_trace']-1)<1e-10 and x['minimum_state_eigenvalue']>-1e-12 for x in ex),{'clock_points':len(ex),'maximum_exchange_residual_over_reference':max(abs(x['exchange_sum_J'])/E for x in ex)})
    invalid=[]
    for path,value in [(('targets','G_SI'),0),(('targets','H0_km_s_Mpc'),float('nan')),(('targets','f_phi'),-.1),(('targets','f_c'),1),(('targets','electron_energy_eV'),0),(('mass_construction','mass_intercept_eV'),1),(('SI','h_J_s'),1)]:
        t=copy.deepcopy(cfg);t[path[0]][path[1]]=value;invalid.append(t)
    t=copy.deepcopy(cfg);t['baseline_0_10']['reference_volume_m3']=2;invalid.append(t)
    t=copy.deepcopy(cfg);t['physical_records']=[1];invalid.append(t)
    rejected=0
    for t in invalid:
        try:m.validate(t)
        except ValueError:rejected+=1
    prefixes=[{'H0_km_s_Mpc':67.4},{'G_SI':6.6743e-11,'f_phi':.0493},{'G_SI':float('inf')},{'G_SI':1,'H0_km_s_Mpc':1,'f_phi':1,'f_c':.1}]
    for t in prefixes:
        try:m.prefix_outputs(cfg,t)
        except ValueError:rejected+=1
    check('invalid_units_inputs_records_and_order_are_rejected',rejected==len(invalid)+len(prefixes),{'invalid_cases':len(invalid)+len(prefixes),'rejected':rejected})
    check('execution_preserves_frozen_inputs_and_scope',m.m09.digest(cfg)==before and r['physical_records']==[] and r['address_reparameterization']['electromagnetic_alpha'] is None,{'input_sha256':before,'measurement_records':0})
    report={'version':r['version'],'passed':True,'check_count':len(checks),'inherited_0_10_check_count':32,'input_hash_sha256':before,'checks':checks}
    (ROOT/'results/verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    print(json.dumps({'passed':True,'checks':len(checks),'inherited_checks':32,'q0':o['q0'],'mu_eV':o['mass_mode_scale_eV']}))

if __name__=='__main__':main()
