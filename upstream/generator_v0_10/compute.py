"""Single finite pipeline: SOURCE -> filters -> record -> internal state -> currents."""
from pathlib import Path
import importlib.util,json,math
import numpy as np
ROOT=Path(__file__).resolve().parent
UP=ROOT.parent
spec=importlib.util.spec_from_file_location('residue09',UP/'residue_current_v0_9/compute.py')
v9=importlib.util.module_from_spec(spec);spec.loader.exec_module(v9)

def validate(inp):
    if inp.get('physical_time_unit') is not None or inp.get('energy_fraction_map') is not None:raise ValueError('unimplemented physical maps must remain null')
    names=[]
    if not inp['source_cases']:raise ValueError('empty cases')
    for c in inp['source_cases']:
        if not isinstance(c['name'],str) or not c['name'] or c['name'] in names:raise ValueError('case names')
        names.append(c['name'])
    if not inp['record_draws']:raise ValueError('empty records')
    for x in inp['record_draws']:
        if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not 0<=x<1:raise ValueError('record draw')
    for p in inp['protocols']:
        if 'release_fractions' not in p:
            if type(p['event_count']) is not int or not 1<=p['event_count']<=10000:raise ValueError('event count')
    return inp


def run():
    inp=validate(json.loads((ROOT/'inputs.json').read_text()))
    cfg=json.loads((UP/'residue_current_v0_9/inputs.json').read_text());v9.validate(cfg)
    h=json.loads((UP/'shutter_v0_8/handoff.json').read_text());p6=json.loads((v9.P6/'inputs.json').read_text())
    m,p,e,V,g,c=v9.v6.construct(p6);excited=V[:,cfg['excited_mode_index']];ce=v9.state_current_context(c,excited)
    H=p['delta_MeV']*(m['h0']-p['x']*m['bounded']);gap=float(p['delta_MeV']*(e[cfg['excited_mode_index']]-e[0]))
    ops={(q,name):v9.v6.currents.full_charge(c,q,name) for q in cfg['Q2_GeV2'] for name in ['proton','neutron']}
    inherited=json.loads((UP/'residue_current_v0_9/results.json').read_text())
    rows=[];checks={};vectors_hash={}
    for case in inp['source_cases']:
        name=case['name'];n,vec,b=v9.b8.branches(h['N'],h['alpha'],h['beta'],case['controls'])
        f={'phenotype':b['phi'],'dark':b['D'],'return':b['initial_reflection']+b['normal_return']}
        selector=v9.residue_fraction(n,vec['phi'],cfg['selector_prime']);rho,a=v9.prepare(g,excited,selector,cfg['reference_preparation_strength'])
        excitation=float(np.trace(rho@H).real-p['delta_MeV']*e[0]);curves=[]
        checks[name+'_branch_sum']=abs(sum(b.values())-1)<2e-11
        checks[name+'_prepared_trace']=abs(np.trace(rho)-1)<2e-11
        checks[name+'_prepared_positive']=np.linalg.eigvalsh(rho).min()>-2e-11
        checks[name+'_unnormalized_phi_trace']=abs(np.trace(f['phenotype']*rho)-f['phenotype'])<2e-11
        checks[name+'_same_H_energy']=abs(excitation-a*gap)<2e-8
        for q in cfg['Q2_GeV2']:
            ff=v9.mixed_currents(c,ce,a,q)
            for species in ['proton','neutron']:
                checks[name+f'_current_trace_{species}_{q}']=abs(np.trace(rho@ops[q,species]).real-ff[species]['GE'])<2e-10
            checks[name+f'_CVC_{q}']=abs(ff['weak']['GEV']-ff['proton']['GE']+ff['neutron']['GE'])<2e-10
            curves.append({'Q2_GeV2':q,**ff})
        records=[]
        for i,draw in enumerate(inp['record_draws']):
            label,state=v9.b8.record(vec,draw);norm=float(np.vdot(state,state).real)
            checks[name+f'_record_norm_{i}']=abs(norm-1)<2e-11
            # Phi readout uses this selected conditional vector, not unrelated reconstructed weights.
            internal=None
            if label=='phi':
                selected_selector=v9.residue_fraction(n,state,cfg['selector_prime'])
                sigma,selected_a=v9.prepare(g,excited,selected_selector,cfg['reference_preparation_strength'])
                checks[name+f'_selected_phi_matches_ensemble_{i}']=np.linalg.norm(sigma-rho)<2e-11
                internal={'excited_population':selected_a,'current_at_Q2_0_1':v9.mixed_currents(c,ce,selected_a,.1)}
            records.append({'record_index':i,'draw':draw,'branch':label,'conditional_address_norm':norm,'internal_readout':internal})
        protocols={}
        for protocol in inp['protocols']:
            releases=protocol.get('release_fractions')
            if releases is None:releases=[protocol['release_fraction']]*protocol['event_count']
            stock=v9.b8.parent.transport(f,releases,protocol['leakage']);protocols[protocol['name']]=stock
            checks[name+'_'+protocol['name']+'_stock_conservation']=all(abs(t['ledger_sum']-1)<2e-11 for t in stock)
            checks[name+'_'+protocol['name']+'_stock_positive']=all(min(t['SOURCE_stock'],t['phenotype_stock'],t['dark_stock'])>=-2e-11 for t in stock)
        reference=protocols['reference_closed_window'][-1]
        checks[name+'_closed_window_fraction']=max(abs(reference[k]-f[z]) for k,z in [('SOURCE_stock','return'),('phenotype_stock','phenotype'),('dark_stock','dark')])<2e-11
        parent=next((x for x in inherited['rows'] if x['case']==name and x['strength']==cfg['reference_preparation_strength']),None)
        if parent:
            checks[name+'_frozen_0_9_population']=abs(a-parent['excited_population'])<2e-11
            checks[name+'_frozen_0_9_energy']=abs(excitation-parent['conditional_excitation_MeV'])<2e-8
            checks[name+'_frozen_0_9_currents']=max(abs(ff[name2][key]-parent['curves'][-1][name2][key]) for name2 in ['proton','neutron','weak'] for key in ff[name2])<2e-10
        rows.append({'case':name,'branch_probabilities':b,'aggregate_fractions':f,'selector_fraction_in_phi':selector,'excited_population':a,'conditional_excitation_MeV':excitation,'curves':curves,'finite_records':records,'stock_protocols':protocols})
    if not all(checks.values()):raise AssertionError([k for k,v in checks.items() if not v])
    sources={'0_7_source_code':UP/'source_filter_v0_7/code/compute.py','0_8_branch_code':UP/'shutter_v0_8/address_bridge.py',
      '0_8_handoff':UP/'shutter_v0_8/handoff.json','0_9_preparation_code':UP/'residue_current_v0_9/compute.py','0_9_inputs':UP/'residue_current_v0_9/inputs.json',
      '0_9_results':UP/'residue_current_v0_9/results.json','0_6_inputs':v9.P6/'inputs.json','0_6_current_code':v9.P6/'currents.py','0_6_results':v9.P6/'results.json'}
    out={'version':'upstream-0.10','inputs':inp,'frozen_inputs':{'N':h['N'],'alpha':h['alpha'],'beta':h['beta'],'preparation_strength':cfg['reference_preparation_strength'],'selector_prime':cfg['selector_prime'],'excited_mode_index':cfg['excited_mode_index']},
        'parent_sha256':{k:v9.sha(path) for k,path in sources.items()},'internal_dimension':len(g),'excitation_gap_MeV':gap,'rows':rows,
        'checks':{k:bool(v) for k,v in checks.items()},'checks_passed':int(sum(checks.values())),
        'scope':'conditional finite upstream generation pipeline; branch statistics and sampled records remain separate; physical timing/species/energy-origin interfaces are open',
        'inherited_mismatch':inherited['remaining']}
    (ROOT/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    baseline=rows[0]
    handoff={'version':'upstream-0.10','upstream_endpoint':'0.10 integration complete within declared conditional scope; 1.0 is freeze/review edition, not new automatic development stages',
       'baseline_information_fractions':baseline['aggregate_fractions'],'Actual_fraction':baseline['aggregate_fractions']['phenotype']+baseline['aggregate_fractions']['dark'],
       'SOURCE_definition':'finite prime addresses and disclosed multiplicative amplitude state','record_type':'one branch label and normalized address vector per supplied draw; sample counts are not branch probabilities',
       'internal_state':'phi-only trace-preserving conditional density preparation; same-state frozen nucleon currents',
       'physical_time_unit':None,'physical_energy_fraction_map':None,'species_origin':None,'energy_supply':None,'record_medium_stability':None,
       'downstream_contract':'information fractions, finite states and conditional currents are typed outputs; importing them into a downstream energy/gravity simulator requires its explicit energy/state map',
       'results_sha256':v9.sha(ROOT/'results.json')}
    (ROOT/'handoff.json').write_text(json.dumps(handoff,indent=2,allow_nan=False)+'\n')
    print('0.10 integrated checks passed:',out['checks_passed'])
if __name__=='__main__':run()
