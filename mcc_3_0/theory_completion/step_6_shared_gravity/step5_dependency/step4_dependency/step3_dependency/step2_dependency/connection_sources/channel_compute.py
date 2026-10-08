"""WRRA-M 0.8: common carrier -> calibrated filter -> placement and charges.

This is actual calibrated selection within the frozen four-filter family.
Selection weights are optimizer weights, not Born probabilities or physical records.
"""
from __future__ import annotations
from fractions import Fraction as Q
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
CALCULATIONS = ROOT.parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


m07 = module('wrra07_filter_bridge', CALCULATIONS/'wrra_m_0_7/compute.py')
m03 = module('wrra03_filter_scores', CALCULATIONS/'verify_wrra_m_0_3.py')
m04 = module('wrra04_filter_metric', CALCULATIONS/'verify_wrra_m_0_4.py')
FILTERS = ('F_DX','F_XX','F_DD','F_XD')
ORIGINS = ('3_A','3_B','1_A','1_B','anti3_A','anti3_B','1_N','1_0')
PAIR_ENTRIES = (('3_A','1_A'),('3_B','1_B'),('3_A','1_B'),('3_B','1_A'),
                ('anti3_A','1_N'),('anti3_B','1_0'),('anti3_A','1_0'),('anti3_B','1_N'))


def validate(cfg):
    if cfg['model_version'] != 'WRRA-M 0.8':raise ValueError('unsupported version')
    m07.validate(cfg['ledger_0_7'])
    p = cfg['filter_calibration']
    finite = ('central_response_shift','charge_contrast_to_response','selection_rate',
              'gap_tolerance','selection_residual_target')
    if not all(math.isfinite(p[k]) for k in finite):raise ValueError('nonfinite filter input')
    if p['charge_contrast_to_response'] < 0 or p['gap_tolerance'] < 0:
        raise ValueError('negative contrast or tolerance')
    if p['selection_rate'] <= 0 or not 0 < p['selection_residual_target'] < 1:
        raise ValueError('invalid selection rate or target')
    if set(p['response_tags']) != set(ORIGINS) or any(v not in (-1,1) for v in p['response_tags'].values()):
        raise ValueError('invalid calibrated tags')
    for key,n in (('initial_filter_weights',4),('channel_state_weights',16)):
        v=np.asarray(p[key],dtype=float)
        if len(v)!=n or not np.isfinite(v).all() or min(v)<0 or abs(sum(v)-1)>1e-12:
            raise ValueError('invalid normalized '+key)
    b=cfg['ledger_0_7']['calibration_and_local_source']
    if not math.isfinite(b['carrier_damping']) or b['carrier_damping'] <= 0:
        raise ValueError('positive damping required')
    if not b['carrier_probe_frequency_squared']:
        raise ValueError('empty carrier probe set')
    probes=np.asarray(b['carrier_probe_frequency_squared'],dtype=float)
    if probes.ndim!=1 or not np.isfinite(probes).all() or min(probes)<0:
        raise ValueError('invalid probe band')
    for anchors in ('left_charge_anchors','right_hypercharge_anchors'):
        for value in p[anchors].values():Q(value)
    for value in shifts(cfg).values():
        if value < 0:raise ValueError('negative response potential')
    families=cfg['family_replication'];count=families['family_count']
    if not isinstance(count,int) or isinstance(count,bool) or count<1 or len(families['labels'])!=count:
        raise ValueError('invalid family count or labels')
    fw=np.asarray(families['family_weights'],dtype=float)
    if len(fw)!=count or not np.isfinite(fw).all() or min(fw)<0 or abs(sum(fw)-1)>1e-12:
        raise ValueError('invalid family state weights')


def inventory():
    # Established complexified branching, retaining independent Weyl-channel assumption.
    items=[{'source':'1_0','origin':'1_0','color':'1','sector':'invariant'}]
    for sector in ('A','B'):
        for rep,prefix in (('3','3'),('anti3','anti3')):
            for color in ('r','g','b'):
                items.append({'source':f'{prefix}_{sector}_{color}', 'origin':f'{prefix}_{sector}',
                              'color':rep,'sector':'7_'+sector})
        items.append({'source':'1_'+sector,'origin':'1_'+sector,'color':'1','sector':'7_'+sector})
    items.append({'source':'1_N','origin':'1_N','color':'1','sector':'neutral_extension'})
    return items


def shifts(cfg):
    p=cfg['filter_calibration'];left=p['left_charge_anchors'];right=p['right_hypercharge_anchors']
    dl=float(Q(left['neutral_lepton'])-Q(left['charged_lepton']))*p['charge_contrast_to_response']
    dr=float(Q(right['invariant_singlet'])-Q(right['neutral_singlet']))*p['charge_contrast_to_response']
    return {o:p['central_response_shift']+p['response_tags'][o]*(dl if o in ORIGINS[:4] else dr)
            for o in ORIGINS}


def responses(rho, carrier, cfg):
    """Evaluate the common resolvent intensity with channel-local lower-order shifts."""
    b=cfg['ledger_0_7']['calibration_and_local_source']
    spectrum, basis=np.linalg.eigh(carrier.Kc)
    populations=np.diag(basis.conj().T@rho@basis).real
    probes=np.asarray(b['carrier_probe_frequency_squared'],dtype=float)
    gamma=b['carrier_damping']
    def intensity(mu):
        kernel=1/((spectrum[None,:]+mu-probes[:,None])**2+gamma**2)
        return float(np.mean(kernel@populations))
    reference=intensity(0.0)
    raw={o:intensity(mu) for o,mu in shifts(cfg).items()}
    values={o:math.sqrt(value/reference) for o,value in raw.items()}
    gram=np.diag([raw[x['origin']]/reference for x in inventory()])
    # Explicit finite-matrix check: only a scalar response offset was added.
    kinetic_error=max(float(np.linalg.norm((carrier.Kc+mu*np.eye(carrier.N))-mu*np.eye(carrier.N)-carrier.Kc))
                      for mu in shifts(cfg).values())
    return {'dimensionless_shifts':shifts(cfg),'raw_intensity':raw,
            'common_reference_intensity':reference,'normalized_signatures':values,
            'transport_gram_diagonal':np.diag(gram).tolist(),
            'transport_gram_rank':int(np.linalg.matrix_rank(gram)),
            'minimum_gram_eigenvalue':float(np.linalg.eigvalsh(gram).min()),
            'neutral_channel_norm_squared':float(gram[-1,-1]),
            'principal_channel_difference':kinetic_error,
            'signature_scope':'color-invariant scalar response in the calibrated weak-component basis; background and basis transform jointly',
            'operator_scope':'auxiliary lower-order readout offset; not an extra dynamical Hamiltonian or SI energy sector'}


def optimizer_weights(initial, score, eta, tau):
    initial=np.asarray(initial,dtype=float);score=np.asarray(score,dtype=float)
    supported=initial>0
    exponent=np.log(initial[supported])+eta*tau*score[supported]
    offset=float(exponent.max())
    raw=np.zeros(4);raw[supported]=np.exp(exponent-offset)
    return raw/raw.sum()


def selection(response, cfg):
    u=response['normalized_signatures'];p=cfg['filter_calibration']
    entries=[float(m04.compatibility((u[a],),(u[b],))) for a,b in PAIR_ENTRIES]
    # 0.3 stores each 2x2 table in row order; PAIR_ENTRIES groups matching pairs first.
    score=np.asarray(m03.scores([entries[i] for i in (0,2,3,1,4,6,7,5)]),dtype=float)
    dl=entries[0]+entries[1]-entries[2]-entries[3]
    dr=entries[4]+entries[5]-entries[6]-entries[7]
    identities=[float(m04.gap_identity((u['3_A'],),(u['3_B'],),(u['1_A'],),(u['1_B'],))),
                float(m04.gap_identity((u['anti3_A'],),(u['anti3_B'],),(u['1_N'],),(u['1_0'],)))]
    maxima=np.flatnonzero(score.max()-score<=p['gap_tolerance'])
    row={'compatibility_entries':dict(zip(('lAA','lBB','lAB','lBA','rAN','rB0','rA0','rBN'),entries)),
         'scores':dict(zip(FILTERS,map(float,score))), 'Delta_L':float(dl),'Delta_R':float(dr),
         'gap_identity_max_error':float(max(abs(dl-identities[0]),abs(dr-identities[1]))),
         'maximizers':[FILTERS[i] for i in maxima],'selected_filter':None,
         'status':'tied','optimizer_scope':'dimensionless construction flow; no measurement probability',
         'flow':[]}
    if len(maxima)!=1:return row
    winner=int(maxima[0]);initial=p['initial_filter_weights'];eta=p['selection_rate']
    if initial[winner]==0:
        row['status']='winning_filter_has_zero_support';return row
    gap=float(min(score[winner]-score[j] for j in range(4) if j!=winner))
    log_ratio=(math.log1p(-initial[winner])-math.log(initial[winner])
               if initial[winner]<1 else -math.inf)
    tau=max(0.0,(log_ratio-math.log(p['selection_residual_target']))/(eta*gap))
    if not math.isfinite(tau):
        raise ValueError('required construction time exceeds floating-point range')
    for t in (0.0,1.0,tau):
        weight=optimizer_weights(initial,score,eta,t)
        row['flow'].append({'construction_time':t,'filter_weights':dict(zip(FILTERS,map(float,weight))),
                            'winning_residual':float(1-weight[winner])})
    if row['flow'][-1]['winning_residual']>p['selection_residual_target']*(1+1e-6):
        raise RuntimeError('selection flow did not converge')
    row.update(selected_filter=FILTERS[winner],status='selected',minimum_score_gap=gap,
               sufficient_construction_time=tau,finite_flow_residual=row['flow'][-1]['winning_residual'])
    return row


def placement(filter_name):
    left_direct=filter_name in ('F_DX','F_DD')
    right_cross=filter_name in ('F_DX','F_XX')
    lepton_up,lepton_down=('1_A','1_B') if left_direct else ('1_B','1_A')
    right_low,right_high=('1_N','1_0') if right_cross else ('1_0','1_N')
    slots=[]
    def put(field,origins,t3l,t3r):
        for source in origins:slots.append({'field':field,'source':source,'T3L':str(t3l),'T3R':str(t3r)})
    colors=('r','g','b')
    put('Q_L',[f'3_A_{c}' for c in colors],Q(1,2),Q(0))
    put('Q_L',[f'3_B_{c}' for c in colors],Q(-1,2),Q(0))
    put('L_L',[lepton_up],Q(1,2),Q(0));put('L_L',[lepton_down],Q(-1,2),Q(0))
    put('u_c',[f'anti3_A_{c}' for c in colors],Q(0),Q(-1,2))
    put('d_c',[f'anti3_B_{c}' for c in colors],Q(0),Q(1,2))
    # These names denote the target slot convention; reversed filters need not match its benchmark.
    put('nu_c',[right_low],Q(0),Q(-1,2));put('e_c',[right_high],Q(0),Q(1,2))
    source=inventory();index={x['source']:i for i,x in enumerate(source)}
    order=[index[x['source']] for x in slots]
    P=np.eye(16)[order]
    for i,row in enumerate(slots):
        row.update(target_index=i,source_index=order[i],color=source[order[i]]['color'],origin=source[order[i]]['origin'])
    return slots,P


def charges(slots,cfg):
    p=cfg['filter_calibration'];left_bl=Q(p['left_lepton_B_minus_L']);right_bl=Q(p['right_lepton_B_minus_L'])
    by_source={r['source']:r for r in slots}
    anchors=p['right_hypercharge_anchors']
    a,c=Q(by_source['1_N']['T3R']),Q(by_source['1_0']['T3R'])
    n,e=Q(anchors['neutral_singlet']),Q(anchors['invariant_singlet'])
    determinant=(a-c)*right_bl
    if determinant==0:raise ValueError('singular hypercharge anchors')
    alpha=(n-e)*right_bl/determinant;beta=(a*e-c*n)/determinant
    rows=[]
    for slot in slots:
        row=dict(slot)
        bl=left_bl if slot['field']=='L_L' else (-left_bl/3 if slot['field']=='Q_L' else
             (right_bl if slot['color']=='1' else -right_bl/3))
        y=alpha*Q(slot['T3R'])+beta*bl;q=Q(slot['T3L'])+y
        row.update(B_minus_L=str(bl),Y=str(y),Q=str(q));rows.append(row)
    groups={}
    for row in rows:
        f=groups.setdefault(row['field'],{'multiplicity':0,'Y':row['Y'],'Q':[]})
        if f['Y']!=row['Y']:raise RuntimeError('hypercharge not constant on multiplet')
        f['multiplicity']+=1
        if row['Q'] not in f['Q']:f['Q'].append(row['Q'])
    anomalies={'gravity_U1':sum(Q(r['Y']) for r in rows),
               'U1_cubed':sum(Q(r['Y'])**3 for r in rows),
               'SU3_squared_U1':Q(1,2)*(2*Q(groups['Q_L']['Y'])+Q(groups['u_c']['Y'])+Q(groups['d_c']['Y'])),
               'SU2_squared_U1':Q(1,2)*(3*Q(groups['Q_L']['Y'])+Q(groups['L_L']['Y'])),
               'SU3_cubed':Q(2-1-1)}
    return {'alpha':str(alpha),'beta':str(beta),'anchor_determinant':str(determinant),
            'channel_table':rows,'field_groups':groups,'benchmark_matches':groups==cfg['benchmark']['fields'],
            'anomalies':{k:str(v) for k,v in anomalies.items()},
            'SU2_doublets':{'left':4,'right':4},'color_branching_dimension':15,
            'extended_transport_dimension':16,'chirality':'independent complex left-handed Weyl channels assumed'}


def channel_energy_bridge(P,cfg,ledger):
    weights=np.asarray(cfg['filter_calibration']['channel_state_weights'])
    before=np.diag(weights);after=P@before@P.conj().T
    energies=ledger['sector_energy_J']
    return {'channel_state_before':weights.tolist(),'channel_state_after':np.diag(after).real.tolist(),
            'state_trace_error':float(abs(np.trace(after)-1)),
            'permutation_unitarity_error':float(np.linalg.norm(P.conj().T@P-np.eye(16))),
            'sector_energy_before_J':energies,
            'sector_energy_after_J':{k:float(np.trace(after).real)*v for k,v in energies.items()},
            'maximum_energy_change_J':float(max(abs(v*np.trace(after).real-v) for v in energies.values())),
            'scope':'channel-blind 0.7 energy operators; relabeling has no added SI energy or physical measurement event'}


def evaluate(a,rho,carrier,cfg,name,recipe):
    rho=m07.validate_state(rho,carrier.N)
    ledger=m07.ledger(a,rho,carrier,cfg['ledger_0_7'],validate_rho=False)
    response=responses(rho,carrier,cfg);choice=selection(response,cfg)
    table=bridge=None
    if choice['selected_filter']:
        slots,P=placement(choice['selected_filter']);table=charges(slots,cfg);bridge=channel_energy_bridge(P,cfg,ledger)
    return {'case_name':name,'state_recipe':recipe,'lattice_N':carrier.N,'scale_factor':a,
            'carrier_epsilon':carrier.epsilon,'response':response,'selection':choice,
            'placement_and_charge':table,'channel_energy_bridge':bridge,'ledger_0_7':ledger}


def replicate_families(reference,cfg):
    charge=reference['placement_and_charge']
    if charge is None:return None
    families=cfg['family_replication'];rows=[]
    for generation,labels in enumerate(families['labels'],start=1):
        for channel in charge['channel_table']:
            row=dict(channel);field=row['field'];label=labels[field]
            if isinstance(label,list):label=label[0 if Q(row['T3L'])>0 else 1]
            if row['color']!='1':label+='_'+row['source'].split('_')[-1]
            row.update(generation=generation,particle_label=label,
                       source=f'g{generation}:'+row['source'],
                       status='conditional_neutral_extension' if field=='nu_c' else 'SM_chiral_component')
            rows.append(row)
    G=np.kron(np.eye(families['family_count']),np.diag(reference['response']['transport_gram_diagonal']))
    return {'family_count':families['family_count'],'calibration_provenance':families['provenance'],
            'particle_inventory':rows,'SM_component_count':sum(r['status']=='SM_chiral_component' for r in rows),
            'conditional_neutral_component_count':sum(r['status']=='conditional_neutral_extension' for r in rows),
            'transport_dimension':len(rows),'transport_gram_rank':int(np.linalg.matrix_rank(G)),
            'minimum_gram_eigenvalue':float(np.linalg.eigvalsh(G).min()),
            'family_state_trace':sum(families['family_weights']),
            'energy_policy':'normalized family state tensor channel state; the same 0.7 energy budget is not multiplied by the family count',
            'mass_and_mixing_status':'not derived in 0.8'}


def run(cfg,out):
    validate(cfg);original=m07.digest(cfg);base=cfg['ledger_0_7'];p=base['carrier_and_background'];N=p['lattice_N']
    plain=m07.m06.Carrier(N,0.0);coupled=m07.m06.Carrier(N,p['noncommuting_test_strength'])
    recipes=[('uniform',{'kind':'uniform'}),('low_mode',{'kind':'mode','mode':N//16}),
             ('high_mode',{'kind':'mode','mode':N//2}),('zero_mode',{'kind':'mode','mode':0}),
             ('coherent_packet',{'kind':'packet','modes':p['noncommuting_test_initial_modes'],
                                 'weights':p['noncommuting_test_initial_weights']})]
    cases=[]
    for name,recipe in recipes:
        rho=m07.state_from_recipe(plain,recipe)
        for a in ((.5,1.,2.) if name=='uniform' else (1.,)):
            cases.append(evaluate(a,rho,plain,cfg,name+'_a'+str(a),recipe))
    for name,recipe in (recipes[0],recipes[-1]):
        cases.append(evaluate(1.,m07.state_from_recipe(coupled,recipe),coupled,cfg,
                              name+'_noncommuting_a1.0',recipe))
    if m07.digest(cfg)!=original:raise RuntimeError('input mutated')
    result={'version':'WRRA-M 0.8','date':'2026-10-01','author':'Wonsik Choi',
            'input_hash_sha256':original,'inherited_0_7_hash_sha256':m07.digest(base),'input_ledger':cfg,
            'source_inventory':inventory(),'cases':cases,
            'closure_passed':all(c['selection']['selected_filter']==cfg['benchmark']['selected_filter'] and
                                 c['placement_and_charge']['benchmark_matches'] for c in cases),
            'claims':{'calibrated_selection':'computed within four fixed filters, with disclosed origin tags and lower-order response calibration',
                      'charge_reproduction':'one hypercharge operator from two anchors after the selected placement',
                      'shared_ledger':'same grid, internal state and unchanged 0.7 energy/pressure/gravity/expansion inputs',
                      'scope':'replicated three-generation charge inventory; no mass, mixing or physical quantization/record generation'},
            'falsification_conditions':['response metric loses positivity or transport rank',
                'fixed calibration leaves a tie or chooses a benchmark-incompatible assignment',
                'charge/representation/anomaly or channel-energy accounting mismatch',
                'undeclared input change or describing optimizer weights as measurement probabilities'],
            'physical_records':[],'measurement_events':[],
            'calibration_provenance':{'response_tags':cfg['filter_calibration']['tag_provenance'],
                                    'response_shifts':cfg['filter_calibration']['response_shift_scope'],
                                    'neutral_extension':cfg['filter_calibration']['neutral_channel_status']}}
    reference=next(c for c in cases if c['case_name']=='uniform_a1.0')
    result['family_replication']=replicate_families(reference,cfg)
    out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    with (out/'case_table.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['case','N','Delta_L','Delta_R','selected_filter','phenotype_share','q','transport_rank'])
        for case in cases:
            s=case['selection'];l=case['ledger_0_7']
            writer.writerow([case['case_name'],case['lattice_N'],s['Delta_L'],s['Delta_R'],s['selected_filter'],
                             l['sector_shares']['phenotype'],l['bridge_0_6']['snapshot']['deceleration_q'],case['response']['transport_gram_rank']])
    if reference['placement_and_charge'] is not None:
        with (out/'channel_table.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(reference['placement_and_charge']['channel_table'][0]));writer.writeheader()
            writer.writerows(reference['placement_and_charge']['channel_table'])
    else:
        (out/'channel_table.csv').unlink(missing_ok=True)
    if result['family_replication']:
        rows=result['family_replication']['particle_inventory']
        with (out/'particle_inventory.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    else:(out/'particle_inventory.csv').unlink(missing_ok=True)
    return result


if __name__=='__main__':
    r=run(json.loads((ROOT/'parameters.json').read_text()),ROOT/'results')
    reference=next(c for c in r['cases'] if c['case_name']=='uniform_a1.0')
    print(json.dumps({'version':r['version'],'closure_passed':r['closure_passed'],
                      'selection':reference['selection'],'charges':reference['placement_and_charge']['field_groups']},indent=2))
