"""Independent selection, response, representation and shared-ledger checks."""
import copy
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import subprocess
import sys
import numpy as np
from scipy.integrate import solve_ivp
import compute as m

ROOT=Path(__file__).resolve().parent


def color_generators(items):
    z=np.zeros((3,3),complex);l=[]
    for a,b in ((0,1),(0,2),(1,2)):
        x=z.copy();x[a,b]=x[b,a]=1;l.append(x/2)
        y=z.copy();y[a,b]=-1j;y[b,a]=1j;l.append(y/2)
    l.extend((np.diag([1,-1,0])/2,np.diag([1,1,-2])/(2*np.sqrt(3))))
    result=[]
    for generator in l:
        block=np.zeros((16,16),complex)
        for origin in ('3_A','3_B','anti3_A','anti3_B'):
            indices=[i for i,r in enumerate(items) if r['origin']==origin]
            block[np.ix_(indices,indices)]=generator if origin.startswith('3') else -generator.conj()
        result.append(block)
    return result


def weak_generators(pairsets):
    matrices=[np.zeros((16,16),complex) for _ in range(3)]
    pauli=[np.array([[0,1],[1,0]])/2,np.array([[0,-1j],[1j,0]])/2,np.diag([1,-1])/2]
    for pair in pairsets:
        for out,value in zip(matrices,pauli):out[np.ix_(pair,pair)]=value
    return matrices


def main():
    cfg=json.loads((ROOT/'parameters.json').read_text());original=m.m07.digest(cfg)
    result=m.run(cfg,ROOT/'results');checks=[]
    def check(name,condition,**metrics):
        if not condition:raise AssertionError(name+': '+str(metrics))
        checks.append({'name':name,'passed':True,**metrics})
    cases=result['cases'];ref=next(c for c in cases if c['case_name']=='uniform_a1.0')
    base=cfg['ledger_0_7'];N=base['carrier_and_background']['lattice_N'];carrier=m.m07.m06.Carrier(N,0)
    rho=np.eye(N)/N
    inherited=[]
    for version in (1,2,3,4):
        path=ROOT.parent/f'verify_wrra_m_0_{version}.py'
        r=subprocess.run([sys.executable,str(path)],capture_output=True,text=True,check=True)
        parsed=json.loads(r.stdout);inherited.append(parsed)
    check('inherited_0_1_to_0_4_exact_checks',all(r['status']=='PASS' for r in inherited),versions=4)
    inv=m.inventory()
    check('fifteen_color_components_and_neutral_extension',len(inv)==16 and
          sum(i['color']=='3' for i in inv)==6 and sum(i['color']=='anti3' for i in inv)==6 and
          sum(i['sector']=='7_A' for i in inv)==7 and sum(i['sector']=='7_B' for i in inv)==7)
    b=base['calibration_and_local_source'];probes=np.asarray(b['carrier_probe_frequency_squared']);gamma=b['carrier_damping']
    spectrum=(2*np.sin(np.pi*np.arange(N)/N))**2
    fft0=np.mean(1/((spectrum[None,:]-probes[:,None])**2+gamma**2))
    fftmax=0.
    for origin,shift in m.shifts(cfg).items():
        expected=np.mean(1/((spectrum[None,:]+shift-probes[:,None])**2+gamma**2))
        fftmax=max(fftmax,abs(expected-ref['response']['raw_intensity'][origin]))
    check('uniform_response_from_independent_periodic_spectrum',fftmax<1e-12 and
          abs(fft0-ref['response']['common_reference_intensity'])<1e-12,maximum_absolute_error=fftmax)
    small=m.m07.m06.Carrier(32,0);rng=np.random.default_rng(808)
    v=rng.normal(size=32)+1j*rng.normal(size=32);v/=np.linalg.norm(v);mixed=np.outer(v,v.conj())
    computed=m.responses(mixed,small,cfg);directerr=0.
    for origin,shift in m.shifts(cfg).items():
        direct=[]
        for probe in probes:
            R=np.linalg.inv(small.Kc+(shift-probe-1j*gamma)*np.eye(32))
            direct.append(float(np.vdot(R@v,R@v).real))
        directerr=max(directerr,abs(np.mean(direct)-computed['raw_intensity'][origin]))
    check('nonuniform_response_from_direct_complex_resolvent',directerr<1e-11,maximum_absolute_error=directerr)
    zero=copy.deepcopy(cfg);zero['filter_calibration']['charge_contrast_to_response']=0.
    tied=m.selection(m.responses(rho,carrier,zero),zero)
    historical=copy.deepcopy(zero);historical['filter_calibration']['central_response_shift']=0.
    h=m.responses(rho,carrier,historical)
    check('zero_calibration_recovers_tie_and_homogeneous_transport',tied['selected_filter'] is None and
          len(tied['maximizers'])==4 and abs(tied['Delta_L'])<1e-14 and
          abs(tied['Delta_R'])<1e-14 and np.max(abs(np.array(h['transport_gram_diagonal'])-1))<1e-14)
    independent=[]
    for name in m.FILTERS:
        left=name in ('F_DX','F_DD');right=name in ('F_DX','F_XX');u=ref['response']['normalized_signatures']
        pairs=[('3_A','1_A' if left else '1_B'),('3_B','1_B' if left else '1_A'),
               ('anti3_A','1_N' if right else '1_0'),('anti3_B','1_0' if right else '1_N')]
        independent.append(-sum((u[a]-u[b])**2 for a,b in pairs))
    error=max(abs(independent[i]-ref['selection']['scores'][name]) for i,name in enumerate(m.FILTERS))
    check('four_filter_costs_and_alignment_identities',error<1e-14 and
          max(c['selection']['gap_identity_max_error'] for c in cases)<1e-12,score_maximum_error=error)
    check('all_nine_cases_select_calibrated_branch',result['closure_passed'] and len(cases)==9 and
          all(c['selection']['Delta_L']>0 and c['selection']['Delta_R']>0 for c in cases),
          minimum_gap=min(c['selection']['minimum_score_gap'] for c in cases),
          maximum_finite_flow_residual=max(c['selection']['finite_flow_residual'] for c in cases))
    check('positive_rank_sixteen_and_transported_neutral_slot',all(c['response']['transport_gram_rank']==16 and
          c['response']['minimum_gram_eigenvalue']>0 and c['response']['neutral_channel_norm_squared']>0 and
          c['response']['principal_channel_difference']<1e-12 for c in cases))
    slots,P=m.placement('F_DX');colors=color_generators(inv);targetcolors=color_generators(slots)
    colorerr=max(np.linalg.norm(P@source-target@P) for source,target in zip(colors,targetcolors))
    check('bijective_filter_preserves_color_action',np.linalg.norm(P.conj().T@P-np.eye(16))==0 and
          len(set(r['source_index'] for r in slots))==16 and colorerr<1e-14,intertwining_error=float(colorerr))
    charges=ref['placement_and_charge']
    check('single_derived_hypercharge_and_exact_anomalies',charges['alpha']=='1' and charges['beta']=='1/2' and
          charges['benchmark_matches'] and all(Q(x)==0 for x in charges['anomalies'].values()) and
          all(n%2==0 for n in charges['SU2_doublets'].values()),field_groups=6)
    replicated=result['family_replication'];allparticles=replicated['particle_inventory']
    check('three_calibrated_generations_and_normalized_energy_budget',replicated['family_count']==3 and
          replicated['SM_component_count']==45 and replicated['conditional_neutral_component_count']==3 and
          replicated['transport_gram_rank']==48 and replicated['family_state_trace']==1 and
          len(set(r['particle_label'] for r in allparticles))==48 and
          all(sum(Q(r['Y']) for r in allparticles if r['generation']==g)==0 for g in (1,2,3)),
          observed_SM_chiral_components=45,conditional_neutral_slots=3,transport_rank=48)
    left=weak_generators([(0,3),(1,4),(2,5),(6,7)])
    # Right generators ordered with +T3 first, matching the selected diagonal signs.
    right=weak_generators([(11,8),(12,9),(13,10),(15,14)])
    weakerr=0.
    for generators in (left,right):
        for a,b1,c in ((0,1,2),(1,2,0),(2,0,1)):
            weakerr=max(weakerr,np.linalg.norm(generators[a]@generators[b1]-generators[b1]@generators[a]-1j*generators[c]))
    bl=np.diag([float(Q(row['B_minus_L'])) for row in charges['channel_table']])
    check('weak_algebra_and_shared_B_minus_L',weakerr<1e-14 and
          all(np.linalg.norm(bl@T-T@bl)<1e-14 for T in left+right) and
          max(np.linalg.norm(a@b1-b1@a) for a in left for b1 in right)<1e-14,
          commutator_error=float(weakerr))
    frozen=json.loads((ROOT.parent/'wrra_m_0_7/results/results.json').read_text())
    check('same_nine_0_7_physical_ledgers',
          all(all(c['ledger_0_7'][key]==f[key] for key in c['ledger_0_7']) for c,f in zip(cases,frozen['cases'])))
    unequal=copy.deepcopy(cfg);weights=np.arange(1,17,dtype=float);weights/=weights.sum()
    unequal['filter_calibration']['channel_state_weights']=weights.tolist()
    bridge=m.channel_energy_bridge(P,unequal,ref['ledger_0_7'])
    check('nonuniform_channel_state_has_no_energy_double_count',bridge['maximum_energy_change_J']<1e-24 and
          np.max(abs(np.array(bridge['channel_state_after'])-weights[[r['source_index'] for r in slots]]))<1e-14)
    joint=rng.normal(size=(16,32))+1j*rng.normal(size=(16,32));joint/=np.linalg.norm(joint)
    after=P@joint;A=m.m07.operators(1.,small,base)
    entangled_err=max(abs(sum(np.vdot(row,op@row) for row in joint)-sum(np.vdot(row,op@row) for row in after)) for op in A)
    check('general_entangled_channel_state_preserves_load',entangled_err<1e-13,maximum_load_error=float(entangled_err))
    grids=[]
    for n in (32,64,128,256):
        changed=copy.deepcopy(cfg);changed['ledger_0_7']['carrier_and_background']['lattice_N']=n
        c=m.m07.m06.Carrier(n,0);state=np.eye(n)/n
        row=m.evaluate(1.,state,c,changed,'grid_'+str(n),{'kind':'uniform'})
        assert row['lattice_N']==row['ledger_0_7']['lattice_N']==n
        grids.append({'N':n,'gap':row['selection']['Delta_L'],'filter':row['selection']['selected_filter'],
                      'rank':row['response']['transport_gram_rank']})
    check('grid_input_controls_load_and_filter_response',all(g['filter']=='F_DX' and g['rank']==16 for g in grids),grid_results=grids)
    contrast=[]
    for k in (0.,.1,.25,.5):
        changed=copy.deepcopy(cfg);changed['filter_calibration']['charge_contrast_to_response']=k
        s=m.selection(m.responses(rho,carrier,changed),changed)
        contrast.append({'coupling':k,'gap':s['Delta_L'],'filter':s['selected_filter']})
    check('declared_contrast_sensitivity',contrast[0]['filter'] is None and
          all(c['filter']=='F_DX' and c['gap']>0 for c in contrast[1:]),contrast_results=contrast)
    orientation=[]
    for swap_left,swap_right,expected in ((True,False,'F_XX'),(False,True,'F_DD'),(True,True,'F_XD')):
        changed=copy.deepcopy(cfg);tags=changed['filter_calibration']['response_tags']
        if swap_left:tags['1_A'],tags['1_B']=tags['1_B'],tags['1_A']
        if swap_right:tags['1_N'],tags['1_0']=tags['1_0'],tags['1_N']
        s=m.selection(m.responses(rho,carrier,changed),changed);assert s['selected_filter']==expected
        rows,_=m.placement(expected);q=m.charges(rows,changed)
        assert all(Q(v)==0 for v in q['anomalies'].values())
        orientation.append({'filter':expected,'field_charge_benchmark_matches':q['benchmark_matches']})
    globally_flipped=copy.deepcopy(cfg);globally_flipped['filter_calibration']['response_tags']={k:-v for k,v in cfg['filter_calibration']['response_tags'].items()}
    same=m.selection(m.responses(rho,carrier,globally_flipped),globally_flipped)
    check('orientation_controls_and_global_convention_covariance',same['selected_filter']=='F_DX' and
          abs(same['Delta_L']-ref['selection']['Delta_L'])<1e-14,controls=orientation,
          equivalence_note='Origin assignment is fixed by calibration; interchangeable origin names do not define a new observed particle spectrum.')
    V,_=np.linalg.qr(rng.normal(size=(16,16))+1j*rng.normal(size=(16,16)))
    G=np.diag(ref['response']['transport_gram_diagonal']);transformed=V@G@V.conj().T
    covariant_error=max(abs(np.vdot(V[:,i],transformed@V[:,i])-G[i,i]) for i in range(16))
    B=np.diag([m.shifts(cfg)[r['origin']] for r in slots])
    background_commutator=float(np.linalg.norm(B@left[0]-left[0]@B))
    check('joint_response_background_and_basis_covariance',covariant_error<1e-13 and background_commutator>0,
          maximum_response_error=float(covariant_error),weak_background_commutator_norm=background_commutator,
          scope='Component-dependent readout is a calibrated background, not an unbroken SU(2)-invariant Hamiltonian.')
    supported=copy.deepcopy(cfg);supported['filter_calibration']['initial_filter_weights']=[0.,1/3,1/3,1/3]
    blocked=m.selection(ref['response'],supported)
    score=np.array(list(ref['selection']['scores'].values()));initial=np.array([.1,.2,.3,.4]);eta=1.3
    ode=solve_ivp(lambda t,p:eta*p*(score-p@score),(0,5),initial,rtol=1e-12,atol=1e-14)
    odeerr=float(np.max(abs(ode.y[:,-1]-m.optimizer_weights(initial,score,eta,5))))
    check('flow_equation_and_zero_support_boundary',blocked['selected_filter'] is None and
          blocked['status']=='winning_filter_has_zero_support' and odeerr<1e-11 and
          np.max(abs(m.optimizer_weights(initial,score,0,5)-initial))<1e-14 and
          m.optimizer_weights(initial,score,-1,100)[3]>.9,ODE_maximum_error=odeerr)
    invalid=[]
    mutations=[('negative_coupling',lambda x:x['filter_calibration'].update(charge_contrast_to_response=-1)),
               ('nonfinite_shift',lambda x:x['filter_calibration'].update(central_response_shift=float('nan'))),
               ('zero_rate',lambda x:x['filter_calibration'].update(selection_rate=0)),
               ('invalid_weight',lambda x:x['filter_calibration'].update(initial_filter_weights=[-.1,.2,.3,.6])),
               ('wrong_channel_count',lambda x:x['filter_calibration'].update(channel_state_weights=[1.])),
               ('invalid_tag',lambda x:x['filter_calibration']['response_tags'].update(**{'3_A':0})),
               ('negative_potential',lambda x:x['filter_calibration'].update(central_response_shift=0)),
               ('zero_damping',lambda x:x['ledger_0_7']['calibration_and_local_source'].update(carrier_damping=0)),
               ('nan_probe',lambda x:x['ledger_0_7']['calibration_and_local_source'].update(carrier_probe_frequency_squared=[float('nan')])),
               ('empty_band',lambda x:x['ledger_0_7']['calibration_and_local_source'].update(carrier_probe_frequency_squared=[])),
               ('fake_record',lambda x:x['ledger_0_7'].update(physical_records=[{'outcome':1}])),
               ('changed_c',lambda x:x['ledger_0_7']['calibration_and_local_source'].update(c_m_s=3e8))]
    for name,mutation in mutations:
        bad=copy.deepcopy(cfg);mutation(bad)
        try:m.validate(bad)
        except (ValueError,TypeError):invalid.append(name)
    check('invalid_calibrations_and_fake_records_rejected',len(invalid)==len(mutations),rejected_cases=invalid)
    recalibrated=copy.deepcopy(cfg);recalibrated['filter_calibration']['right_hypercharge_anchors']['invariant_singlet']='2'
    q=m.charges(slots,recalibrated)
    check('hash_provenance_and_explicit_recalibration',m.m07.digest(cfg)==original and m.m07.digest(recalibrated)!=original and
          q['alpha']=='2' and q['beta']=='1' and not q['benchmark_matches'] and
          result['physical_records']==[] and result['measurement_events']==[],
          recalibrated_alpha=q['alpha'],recalibrated_beta=q['beta'])
    tiny=copy.deepcopy(cfg)
    tiny['filter_calibration']['initial_filter_weights']=[1e-320,1/3,1/3,1/3]
    m.validate(tiny); tiny_selection=m.selection(ref['response'],tiny)
    check('tiny_positive_winner_support_converges_without_overflow',
          tiny_selection['selected_filter']=='F_DX'
          and math.isfinite(tiny_selection['sufficient_construction_time'])
          and tiny_selection['finite_flow_residual']<1.000001e-8,
          initial_winner_weight=1e-320,
          construction_time=tiny_selection['sufficient_construction_time'],
          final_residual=tiny_selection['finite_flow_residual'])
    report={'version':'WRRA-M 0.8','passed':True,'check_count':len(checks),
            'input_hash_sha256':original,'checks':checks,'random_test_seed':808}
    (ROOT/'results/verification.json').write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'results/inherited_exact_checks.json').write_text(json.dumps(inherited,indent=2)+'\n')
    print(json.dumps({'version':report['version'],'passed':True,'check_count':len(checks),
                      'reference_gap':ref['selection']['Delta_L'],'ODE_error':odeerr,'input_hash_sha256':original},indent=2))


if __name__=='__main__':main()
