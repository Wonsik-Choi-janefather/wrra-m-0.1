"""Numerical falsifiers for the explicit 0.10 bridge and inherited reference."""
from pathlib import Path
import copy
import json
import math
import numpy as np
from scipy.linalg import expm
import compute as m

ROOT=Path(__file__).resolve().parent


def main():
    cfg=json.loads((ROOT/'parameters.json').read_text());out=ROOT/'results'
    r=m.run(cfg,out);checks=[]
    def check(name,passed,evidence):
        checks.append({'id':len(checks)+1,'check':name,'passed':bool(passed),'evidence':evidence})
        if not passed:raise AssertionError(name+': '+str(evidence))
    ucfg=cfg['upstream_0_9'];base=m.m09.address_base(ucfg);effect=m.m09.effects(ucfg,base)
    cal=r['calibration'];mu=m.address_moments(cfg,base,effect)
    old=ucfg['baseline_0_8']['ledger_0_7'];p=old['carrier_and_background'];N=p['lattice_N']
    plain=m.m06.Carrier(N,0);coupled=m.m06.Carrier(N,p['noncommuting_test_strength'])
    uniform=np.eye(N)/N;E0=cal['ucrit_J_m3']*cfg['reference_volume_m3']
    ref=next(c for c in r['cases'] if c['case_name']=='uniform_a1.0')
    close=lambda a,b,tol=1e-10:abs(a-b)<=tol*max(abs(a),abs(b),1e-300)
    check('frozen_0_9_input_and_arithmetic_reference',r['upstream_0_9_input_hash_sha256']==cfg['provenance']['baseline_0_9_input_sha256'] and
          all(abs(r['common_arithmetic_ledger'][s]-ucfg['upstream']['targets'][s])<1e-12 for s in m.SECTORS),
          {'input_sha256':r['upstream_0_9_input_hash_sha256'],'shares':r['common_arithmetic_ledger']})
    check('positive_once_fitted_dimensional_coefficients',min(cal['eta_J_m3'].values())>0,cal['eta_J_m3'])
    g=m.response(cfg,base)
    check('every_address_positive_energy_response',np.min(g)>=1,{'address_count':len(base['n']),'minimum_response':float(np.min(g))})
    direct=np.array([math.fsum(float(x) for x in base['w']*effect[i]*g[i]) for i in range(3)])
    err=float(np.max(abs(direct-mu)))
    check('independent_address_energy_sum',err<1e-14,{'maximum_absolute_moment_error':err})
    target=cfg['energy_map']['reference_energy_fractions']
    check('three_reference_SI_energies_and_one_total',all(close(ref['sector_energy_fractions'][s],target[s]) for s in m.SECTORS) and close(ref['total_density_J_m3'],cal['ucrit_J_m3']),
          {'fractions':ref['sector_energy_fractions'],'ucrit_J_m3':cal['ucrit_J_m3']})
    b08=json.loads((out/'upstream_0_9/baseline_0_8/results.json').read_text())
    regression=[]
    for new,prior in zip(r['cases'],b08['cases']):
        x=prior['ledger_0_7'];regression.append(max(abs(new['total_density_J_m3']-x['total_density_J_m3'])/cal['ucrit_J_m3'],
            abs(new['total_pressure_Pa']-x['total_pressure_Pa'])/cal['ucrit_J_m3'],abs(new['H_over_H0']-x['bridge_0_6']['snapshot']['H_over_H0']),
            abs(new['deceleration_q']-x['bridge_0_6']['snapshot']['deceleration_q']),
            abs(new['local_readout']['v_total_km_s']-x['bridge_0_6']['local_readout']['v_total_km_s'])/300))
    check('all_nine_inherited_state_and_physical_cases',max(regression)<1e-10,{'case_count':len(regression),'maximum_scaled_difference':max(regression)})
    arc=ref['local_readout']['finite_patch_lensing']['alpha_patch_arcsec']
    check('inherited_q_rotation_and_conditional_lensing',abs(ref['deceleration_q']+.52855)<1e-12 and
          abs(ref['local_readout']['v_total_km_s']-207.510905)<1e-6 and abs(arc-.535586511)<1e-9,
          {'q':ref['deceleration_q'],'v_km_s':ref['local_readout']['v_total_km_s'],'deflection_arcsec':arc})
    alt=r['alternate_reference'];alt_target=cfg['energy_map']['alternate_energy_fractions']
    check('explicit_alternate_three_sector_calibration',all(close(alt['sector_energy_fractions'][s],alt_target[s]) for s in m.SECTORS) and abs(alt['deceleration_q']+.523)<1e-12,
          {'fractions':alt['sector_energy_fractions'],'q':alt['deceleration_q']})
    eig=np.linalg.eigvalsh(m.energy_operator(cfg,cal,mu,coupled,1)/E0)
    check('positive_total_energy_operator',min(eig)>=-1e-12,{'minimum_eigenvalue_over_reference':float(min(eig))})
    pressure_errors=[]
    for carrier in (plain,coupled):
        psi=carrier.packet([8,16,24],[1/3]*3);rho=np.outer(psi,psi.conj())
        for a in (.5,1,2):
            V=cfg['reference_volume_m3']*a**3;h=V*1e-4
            def energy(v):return float(np.trace(rho@m.energy_operator(cfg,cal,mu,carrier,(v/cfg['reference_volume_m3'])**(1/3))).real)
            fd=-(-energy(V+2*h)+8*energy(V+h)-8*energy(V-h)+energy(V-2*h))/(12*h)
            exact=m.ledger(cfg,cal,mu,carrier,rho,a,include_local=False)['total_pressure_Pa']
            pressure_errors.append(abs(fd-exact)/cal['ucrit_J_m3'])
    check('independent_five_point_volume_pressure',max(pressure_errors)<1e-9,{'maximum_pressure_error_over_ucrit':max(pressure_errors),'states_and_volumes':6})
    scan=[]
    for exponent in (0,1.5,3):
        trial=copy.deepcopy(cfg);trial['energy_map']['energy_volume_exponents']['return']=exponent
        x=m.ledger(trial,cal,mu,plain,uniform,1,include_local=False)
        w=x['sector_pressure_Pa']['return']/x['sector_density_J_m3']['return'];scan.append(w)
    check('background_equation_of_state_from_energy_homogeneity',np.max(abs(np.array(scan)-np.array([0,-.5,-1])))<1e-13,{'exponents':[0,1.5,3],'derived_w':scan})
    check('pressureless_expressed_and_clustering_components',all(x['sector_pressure_Pa']['phenotype']==0 and x['sector_pressure_Pa']['resident_nonphenotype']==0 for x in r['cases']),{'checked_cases':len(r['cases'])})
    trial=copy.deepcopy(cfg);trial['reference_volume_m3']=13.7
    x=m.ledger(trial,cal,mu,plain,uniform,1,include_local=False)
    check('reference_volume_is_representative_not_universe_size',close(x['total_energy_J'],13.7*ref['total_energy_J']) and close(x['total_density_J_m3'],ref['total_density_J_m3']) and close(x['H_over_H0'],ref['H_over_H0']),{'volume_multiplier':13.7,'density_unchanged':True})
    probes=r['frozen_coefficient_address_probes'];K4=next(x for x in probes if x['case']=='K4');K16=next(x for x in probes if x['case']=='K16')
    check('frozen_SI_coefficients_respond_to_address_rule_changes',abs(K4['physical']['total_density_J_m3']-K16['physical']['total_density_J_m3'])/cal['ucrit_J_m3']>1e-4,
          {'K4_q':K4['physical']['deceleration_q'],'K16_q':K16['physical']['deceleration_q'],'coefficient_refit':False})
    trial=copy.deepcopy(cfg);trial['upstream_0_9']['upstream']['address_cutoff_N']=300
    bb=m.m09.address_base(trial['upstream_0_9']);ef=m.m09.effects(trial['upstream_0_9'],bb);mm=m.address_moments(trial,bb,ef)
    x=m.ledger(trial,cal,mm,plain,uniform,1,include_local=False)
    check('separate_address_and_carrier_cutoff_probe',len(bb['n'])==299 and x['lattice_N']==N and abs(x['total_density_J_m3']-ref['total_density_J_m3'])>1e-15,
          {'address_N':300,'carrier_N':N,'q':x['deceleration_q'],'SI_coefficients_held':True})
    normalized_w=base['w'][::-1].copy();bb=dict(base);bb['w']=normalized_w
    mm=m.address_moments(cfg,bb,effect);x=m.ledger(cfg,cal,mm,plain,uniform,1,include_local=False)
    check('arbitrary_normalized_address_state_changes_SI_energy',x['total_density_J_m3']>=0 and abs(x['total_density_J_m3']-ref['total_density_J_m3'])/cal['ucrit_J_m3']>1e-4,{'reversed_state_density_J_m3':x['total_density_J_m3']})
    check('zero_hidden_carrier_mode_retains_phenotype_energy',next(c for c in r['cases'] if c['case_name']=='zero_mode_a1.0')['total_energy_J']>0,{'zero_hidden_does_not_delete_phi':True})
    zero=m.ledger(cfg,cal,np.zeros(3),plain,uniform,1,include_local=False)
    check('zero_total_energy_has_explicit_undefined_ratios',zero['deceleration_q'] is None and zero['H_over_H0']==0 and all(v is None for v in zero['sector_energy_fractions'].values()),{'zero_domain':zero})
    ground=plain.wave(0);mode=plain.wave(16);rho=(1-1e-8)*np.outer(ground,ground.conj())+1e-8*np.outer(mode,mode.conj())
    tiny=m.ledger(cfg,cal,mu,plain,rho,1,include_local=False)['sector_energy_J']['resident_nonphenotype']
    check('small_positive_hidden_load_is_retained',tiny>0,{'small_clustering_energy_J':tiny})
    channel_total=sum(x['phenotype_channel_energy_J'] for x in r['phenotype_channel_energy'])
    check('48_channel_energies_preserve_one_phenotype_budget',close(channel_total,ref['sector_energy_J']['phenotype']) and len(r['phenotype_channel_energy'])==48,{'channel_count':48,'energy_J':channel_total,'no_generation_multiplier':True})
    prior_channels=json.loads((out/'upstream_0_9/results.json').read_text())['channel_inventory']
    check('inherited_filter_charge_and_channel_labels_preserved',all(all(x[k]==y[k] for k in ('source','field','Y','Q','particle_label')) for x,y in zip(r['phenotype_channel_energy'],prior_channels)),{'selected_filter':'F_DX'})
    rows=r['fixed_volume_exchange'];maxexchange=max(abs(x['exchange_sum_J'])/E0 for x in rows)
    check('same_energy_operator_internal_exchange_cancels',maxexchange<1e-11,{'maximum_exchange_error_over_reference':maxexchange})
    change=max(x['D_operator_load'] for x in rows)-min(x['D_operator_load'] for x in rows)
    check('noncommuting_carrier_has_actual_sector_exchange',coupled.commutator_norm>0 and change>1e-5,{'commutator_norm':coupled.commutator_norm,'D_load_range':change})
    check('unitary_state_trace_and_positivity_preserved',all(abs(x['state_trace']-1)<1e-10 and x['minimum_state_eigenvalue']>-1e-12 for x in rows),{'clock_points':len(rows)})
    hist=r['expansion_state_history'];norm_error=max(abs(x['raw_state_norm']-1) for x in hist)
    check('same_energy_generator_during_expansion',norm_error<1e-8 and max(abs(x['state_exchange_sum_over_reference']) for x in hist)<1e-10,{'norm_error':norm_error,'scale_factors':[x['scale_factor'] for x in hist]})
    cont=max(abs(x['continuity_residual_over_ucrit']) for x in hist)
    check('homogeneous_energy_pressure_continuity',cont<1e-10,{'maximum_continuity_error_over_ucrit':cont})
    frames=r['frame_energy_transport'];sums=[x['phenotype_weight']+x['D_weight']+x['S_pending_weight']+x['R_weight'] for x in frames]
    check('four_field_transition_weight_conservation',max(abs(x-1) for x in sums)<1e-12,{'frames':len(frames)})
    ferr=max(abs(x['accounted_energy_J']-frames[0]['accounted_energy_J'])/E0 for x in frames)
    check('conversion_work_owns_admission_energy_changes',ferr<1e-11 and abs(frames[-1]['conversion_work_account_J'])/E0>1e-5,{'maximum_accounted_energy_error_over_reference':ferr,'terminal_conversion_work_J':frames[-1]['conversion_work_account_J']})
    check('SOURCE_return_relabel_does_not_duplicate_energy',frames[-1]['S_pending_energy_J']==0 and frames[-1]['edge_energy_change_J']==0 and close(frames[-1]['current_energy_J'],ref['total_energy_J']),{'recovery_frame':frames[-1]['frame'],'return_energy_J':frames[-1]['R_energy_J']})
    # Omit the work account deliberately. The rejection proves the check is not vacuous.
    unowned=abs(frames[-1]['current_energy_J']-frames[0]['current_energy_J'])/E0
    check('missing_conversion_owner_is_detectable',unowned>1e-5,{'energy_error_without_work_account_over_reference':unowned})
    errors=[]
    for key,value in [('reference_volume_m3',0),('reference_volume_m3',float('nan'))]:
        trial=copy.deepcopy(cfg);trial[key]=value;errors.append(trial)
    for field,s,value in [('address_response_lambda','return',-1),('energy_volume_exponents','return',4),('energy_volume_exponents','phenotype',1),('reference_energy_fractions','return',-.1),('alternate_energy_fractions','return',.2)]:
        trial=copy.deepcopy(cfg);trial['energy_map'][field][s]=value;errors.append(trial)
    trial=copy.deepcopy(cfg);trial['scope']['measurement_records']=[{'result':1}];errors.append(trial)
    trial=copy.deepcopy(cfg);trial['provenance']['baseline_0_9_input_sha256']='0'*64;errors.append(trial)
    rejected=0
    for trial in errors:
        try:m.validate(trial)
        except ValueError:rejected+=1
    for rho in (2*uniform,uniform+1j*np.eye(N),np.diag([-1.]+[2/(N-1)]*(N-1))):
        try:m.ledger(cfg,cal,mu,plain,rho,1,include_local=False)
        except ValueError:rejected+=1
    check('invalid_maps_states_and_unexecuted_records_rejected',rejected==len(errors)+3,{'invalid_cases':len(errors)+3,'rejected':rejected})
    before=m.m09.digest(cfg);m.run(cfg,out)
    check('execution_does_not_mutate_inputs_or_silently_refit',m.m09.digest(cfg)==before,{'input_sha256':before})
    report={'version':'WRRA-M 0.10','passed':all(x['passed'] for x in checks),'check_count':len(checks),'input_hash_sha256':before,'checks':checks}
    (out/'verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    print(json.dumps({'passed':report['passed'],'check_count':len(checks),'reference_q':ref['deceleration_q'],'reference_v_km_s':ref['local_readout']['v_total_km_s'],'reference_lens_arcsec':arc,'alternate_q':alt['deceleration_q']},indent=2))


if __name__=='__main__':main()
