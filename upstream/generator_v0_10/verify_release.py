"""Independent scalar, record selection and scope-contract audit."""
from pathlib import Path
import copy,json,math
from compute import validate
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'results.json').read_text());checks={}
for case in r['rows']:
    name=case['case'];b=case['branch_probabilities'];f=case['aggregate_fractions']
    # Rebuild finite stock recurrence with independent explicit scalar equations.
    for protocol in r['inputs']['protocols']:
        source,phi,dark=1.,0.,0.
        releases=protocol.get('release_fractions',[protocol.get('release_fraction',0.)]*protocol.get('event_count',0));nu=protocol['leakage']
        for j,u in enumerate(releases):
            available=source+nu*(phi+dark);oldp=(1-nu)*phi;oldd=(1-nu)*dark;released=u*available
            source=available-released*(f['phenotype']+f['dark']);phi=oldp+released*f['phenotype'];dark=oldd+released*f['dark']
            saved=case['stock_protocols'][protocol['name']][j]
            checks[f'{name}_{protocol["name"]}_{j}']=max(abs(source-saved['SOURCE_stock']),abs(phi-saved['phenotype_stock']),abs(dark-saved['dark_stock']))<2e-11
        if nu==0 and all(x==releases[0] for x in releases):
            expected=1-(1-releases[0]*(f['phenotype']+f['dark']))**len(releases)
            checks[f'{name}_{protocol["name"]}_finite_closed_form']=abs(phi+dark-expected)<2e-11
    for i,rec in enumerate(case['finite_records']):
        keys=list(b);cum=0.;wanted=None
        for k in keys:
            cum+=b[k]/sum(b.values())
            if rec['draw']<cum:wanted=k;break
        checks[f'{name}_record_branch_{i}']=wanted==rec['branch']
        checks[f'{name}_record_ownership_{i}']=(rec['internal_readout'] is not None)==(rec['branch']=='phi')
    checks[name+'_information_Actual_split']=abs(sum(f.values())-1)<2e-11
base=next(x for x in r['rows'] if x['case']=='baseline');phase=next(x for x in r['rows'] if x['case']=='p3_phase')
checks['phase_only_pipeline_invariant']=abs(base['excited_population']-phase['excited_population'])<2e-11
checks['baseline_current_matches_stage09']=abs(next(x for x in base['curves'] if x['Q2_GeV2']==.1)['proton']['GE']-0.7301767666507732)<2e-10
checks['reference_is_single_window_not_repeated_fixed_point']=abs(base['stock_protocols']['recycling_control'][-1]['Actual_stock']-.318)>.1
for key in ['physical_time_unit','energy_fraction_map']:
    bad=copy.deepcopy(r['inputs']);bad[key]=1
    try:validate(bad)
    except ValueError:checks[key+'_unsupported_map_rejected']=True
    else:checks[key+'_unsupported_map_rejected']=False
for draw in [-1,1,float('nan'),True]:
    bad=copy.deepcopy(r['inputs']);bad['record_draws']=[draw]
    try:validate(bad)
    except ValueError:checks['bad_draw_'+str(draw)]=True
    else:checks['bad_draw_'+str(draw)]=False
if not all(checks.values()):raise AssertionError([k for k,v in checks.items() if not v])
(ROOT/'audit.json').write_text(json.dumps({'checks':checks,'checks_passed':len(checks),'scope':'independent finite scalar ledger and branch selection; physical interfaces stay typed/null'},indent=2)+'\n')
print('0.10 independent checks passed:',len(checks))
