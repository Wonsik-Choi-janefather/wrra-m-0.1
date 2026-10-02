"""WRRA-M 0.11: staged physical calibration on the frozen 0.10 bridge."""
from pathlib import Path
import copy
import csv
import json
import math
import importlib.util
import numpy as np

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('wrra10_sequential',ROOT.parent/'wrra_m_0_10/compute.py')
m10=importlib.util.module_from_spec(spec);spec.loader.exec_module(m10)
m09=m10.m09;SECTORS=m10.SECTORS
ORDER=('G_SI','H0_km_s_Mpc','f_phi','f_c','electron_energy_eV')


def validate_prefix(values):
    if list(values)!=list(ORDER[:len(values)]):raise ValueError('calibration must be an ordered prefix')
    if any(not math.isfinite(v) for v in values.values()):raise ValueError('finite inputs required')
    for k in ('G_SI','H0_km_s_Mpc','electron_energy_eV'):
        if k in values and values[k]<=0:raise ValueError('positive dimensional input required')
    if 'f_phi' in values and not 0<=values['f_phi']<=1:raise ValueError('invalid phenotype share')
    if 'f_c' in values and (values['f_c']<=0 or values['f_c']+values['f_phi']>1):raise ValueError('invalid clustering share')


def validate(cfg):
    if cfg['model_version']!='WRRA-M 0.11':raise ValueError('version mismatch')
    baseline=cfg['baseline_0_10'];m10.validate(baseline)
    if m09.digest(baseline)!=cfg['provenance']['baseline_0_10_input_sha256']:raise ValueError('frozen input changed')
    if tuple(cfg['calibration_order'])!=ORDER:raise ValueError('order changed')
    validate_prefix({k:cfg['targets'][k] for k in ORDER})
    u=cfg['SI'];b=baseline['upstream_0_9']['baseline_0_8']['ledger_0_7']['calibration_and_local_source']
    if u['c_m_s']!=b['c_m_s'] or u['parsec_m']!=b['parsec_m']:raise ValueError('unit convention mismatch')
    if u['h_J_s']!=6.62607015e-34 or u['eV_J']!=1.602176634e-19:raise ValueError('exact SI references changed')
    for k,v in u.items():
        if not math.isfinite(v) or v<=0:raise ValueError('invalid SI value')
    n=cfg['mass_construction']['electron_mode']
    if not isinstance(n,int) or isinstance(n,bool) or n<=0:raise ValueError('positive electron mode required')
    if cfg['mass_construction']['mass_intercept_eV']!=0:raise ValueError('this release freezes the zero intercept')
    if any(not isinstance(n,int) or isinstance(n,bool) for n in cfg['mass_construction']['report_modes']):raise ValueError('integer report modes required')
    if cfg['physical_records']:raise ValueError('measurement records belong to 0.13')


def prefix_outputs(cfg,values):
    """No future calibration input is read by this staged calculator."""
    validate_prefix(values);u=cfg['SI'];c=u['c_m_s'];out={}
    if 'G_SI' in values:
        G=values['G_SI'];hb=u['h_J_s']/(2*math.pi)
        out.update(Einstein_action_coefficient_J_per_m=c**4/(16*math.pi*G),
                   Einstein_response_m_J=8*math.pi*G/c**4,
                   Planck_length_m=math.sqrt(hb*G/c**3),Planck_time_s=math.sqrt(hb*G/c**5))
    if 'H0_km_s_Mpc' in values:
        H=values['H0_km_s_Mpc']*1000/(1e6*u['parsec_m']);crit=3*H**2*c**2/(8*math.pi*G)
        out.update(H0_s_minus1=H,ucrit_J_m3=crit,Hubble_length_m=c/H,Hubble_time_s=1/H)
    if 'f_phi' in values:
        fh=1-values['f_phi'];uh=fh*crit
        out.update(f_h=fh,u_hidden_J_m3=uh,eta_load_J_m3=uh/2,
                   weighted_twist_hidden_m_minus2=16*math.pi*G*uh/c**4,
                   length_coefficient_m=(c*c/math.sqrt(16*math.pi*G*uh) if uh>0 else None))
    if 'f_c' in values:
        fp=values['f_phi'];fc=values['f_c'];fb=1-fp-fc
        out.update(f_b=fb,chi_c=fc/fh,u_phi_J_m3=fp*crit,u_c_J_m3=fc*crit,u_b_J_m3=fb*crit,
                   weighted_twist_clustering_m_minus2=16*math.pi*G*fc*crit/c**4,
                   aT_m_s2=c*H*math.sqrt(fc/8),pressure_Pa=-fb*crit,q0=(1-3*fb)/2)
    if 'electron_energy_eV' in values:
        Ee=values['electron_energy_eV'];out.update(electron_energy_J=Ee*u['eV_J'],
            electron_mass_kg=Ee*u['eV_J']/c**2,mass_mode_scale_eV=Ee/cfg['mass_construction']['electron_mode'])
    return out


def staged(cfg):
    values={};rows=[]
    for k in ORDER:
        values[k]=cfg['targets'][k]
        rows.append({'step':len(values),'added_input':k,'supplied_inputs':copy.deepcopy(values),
                     'outputs':prefix_outputs(cfg,values),'remaining_calibrations':list(ORDER[len(values):]),
                     'fixed_constitutive_choices_remain':True})
    return rows


def physical_context(cfg,base,effect,values=None,response_cfg=None):
    vals=cfg['targets'] if values is None else values;full={k:vals[k] for k in ORDER}
    o=prefix_outputs(cfg,full);old=cfg['baseline_0_10'];physical=old if response_cfg is None else response_cfg
    mu=m10.address_moments(physical,base,effect)
    f=(full['f_phi'],full['f_c'],1-full['f_phi']-full['f_c'])
    cal={'ucrit_J_m3':o['ucrit_J_m3'],'H0_s_minus1':o['H0_s_minus1'],
         'eta_J_m3':dict(zip(SECTORS,(o['ucrit_J_m3']*f[i]/mu[i] for i in range(3)))),
         'reference_address_moments':dict(zip(SECTORS,map(float,mu))),'target_energy_fractions':dict(zip(SECTORS,f)),
         'policy':'explicit once-fitted coefficients, then fixed across probes'}
    src=copy.deepcopy(old['upstream_0_9']['baseline_0_8']['ledger_0_7']['calibration_and_local_source'])
    src.update(G_SI=full['G_SI'],H0_km_s_Mpc=full['H0_km_s_Mpc'],fraction_phenotype=full['f_phi'],
               fraction_twist_clustering=full['f_c'],electron_mass_energy_eV=full['electron_energy_eV'])
    return cal,mu,src,o


def physical_readout(cfg,cal,mu,carrier,rho,a,src,response_cfg=None):
    physical=cfg['baseline_0_10'] if response_cfg is None else response_cfg
    row=m10.ledger(physical,cal,mu,carrier,rho,a,include_local=False)
    c=m10.m06.calibration(src);dens=row['sector_density_J_m3']
    snap={'aT_over_reference':math.sqrt(dens['resident_nonphenotype']/(c['ucrit_J_m3']*c['fc'])),
          'hidden_density_over_reference':(dens['resident_nonphenotype']+dens['return'])/(c['ucrit_J_m3']*c['fh'])}
    p=physical['upstream_0_9']['baseline_0_8']['ledger_0_7']['carrier_and_background']
    row['local_readout']=m10.m06.local_readout(snap,p,src,c)
    return row


def dependency_map(cfg):
    def features(v):
        o=prefix_outputs(cfg,dict(zip(ORDER,v)))
        return np.array([o[k] for k in ('Einstein_action_coefficient_J_per_m','ucrit_J_m3','u_hidden_J_m3','u_c_J_m3','mass_mode_scale_eV')])
    v=np.array([cfg['targets'][k] for k in ORDER]);h=1e-5
    J=np.column_stack([(np.log(features(v*np.exp(h*np.eye(5)[i])))-np.log(features(v*np.exp(-h*np.eye(5)[i]))))/(2*h) for i in range(5)])
    s=np.linalg.svd(J,compute_uv=False)
    return {'input_columns':list(ORDER),'output_rows':['Einstein_action_coefficient','ucrit','u_hidden','u_c','mass_mode_scale'],
            'log_sensitivity':J.tolist(),'singular_values':s.tolist(),'rank':int(np.linalg.matrix_rank(J,tol=1e-8)),
            'scope':'local identification of the five numerical anchors conditional on frozen model choices'}


def write_csv(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def run(cfg,out):
    validate(cfg);out.mkdir(parents=True,exist_ok=True);old=cfg['baseline_0_10']
    base=m09.address_base(old['upstream_0_9']);effect=m09.effects(old['upstream_0_9'],base)
    cal,mu,src,o=physical_context(cfg,base,effect)
    p=old['upstream_0_9']['baseline_0_8']['ledger_0_7']['carrier_and_background'];N=p['lattice_N']
    carrier=m10.m06.Carrier(N,0);uniform=np.eye(N)/N;coupled=m10.m06.Carrier(N,p['noncommuting_test_strength'])
    cases=[];packet={'kind':'packet','modes':[8,16,24],'weights':[1/3]*3}
    recipes=[(f'uniform_a{a}',carrier,{'kind':'uniform'},a) for a in (.5,1.,2.)]
    recipes += [('low_mode_a1.0',carrier,{'kind':'mode','mode':8},1.),
                ('high_mode_a1.0',carrier,{'kind':'mode','mode':N//2},1.),
                ('zero_mode_a1.0',carrier,{'kind':'mode','mode':0},1.),
                ('coherent_packet_a1.0',carrier,packet,1.),
                ('uniform_noncommuting_a1.0',coupled,{'kind':'uniform'},1.),
                ('coherent_packet_noncommuting_a1.0',coupled,packet,1.)]
    for name,car,recipe,a in recipes:
        rho=m10.m07.state_from_recipe(car,recipe)
        row=physical_readout(cfg,cal,mu,car,rho,a,src);row.update(case_name=name,state_recipe=recipe);cases.append(row)
    ref=next(x for x in cases if x['case_name']=='uniform_a1.0')
    masses=[{'mode':n,'rest_energy_eV':abs(n)*o['mass_mode_scale_eV'],
             'rest_energy_J':abs(n)*o['mass_mode_scale_eV']*cfg['SI']['eV_J']} for n in cfg['mass_construction']['report_modes']]
    reparam=m09.calibrate(old['upstream_0_9'],base)
    reparam.update(frozen_alpha_addr=old['upstream_0_9']['upstream']['state']['alpha'],
                   frozen_beta_scalar=old['upstream_0_9']['upstream']['scalar_comparison']['odd_composite_admission_beta'],
                   calibrated_from='two separately disclosed arithmetic targets, not the physical energy fractions',
                   independent_beta_required=False,electromagnetic_alpha=None)
    probes=[]
    for k in ORDER:
        for ratio in (.99,1.01):
            v=copy.deepcopy(cfg['targets']);v[k]*=ratio
            cc,mm,ss,oo=physical_context(cfg,base,effect,v)
            x=physical_readout(cfg,cc,mm,carrier,uniform,1,ss)
            probes.append({'changed_input':k,'multiplier':ratio,'ucrit_J_m3':oo['ucrit_J_m3'],
                          'q0':oo['q0'],'aT_m_s2':oo['aT_m_s2'],'mu_eV':oo['mass_mode_scale_eV'],
                          'v_km_s':x['local_readout']['v_total_km_s'],'scope':'input response probe; not an observational confidence interval'})
    address_probes=[]
    for name,K in [('K4',4),('K16',16)]:
        t=copy.deepcopy(old);t['upstream_0_9']['upstream']['update']['admission_frames_K']=K
        ef=m09.effects(t['upstream_0_9'],base);mm=m10.address_moments(t,base,ef)
        x=physical_readout(cfg,cal,mm,carrier,uniform,1,src,t)
        address_probes.append({'case':name,'physical':x,'coefficient_policy':'held fixed after calibration'})
    # Same five anchors and altered response profiles: distinguish fit products from unfitted shape.
    degeneracy=[]
    for lam in (0.,1.):
        t=copy.deepcopy(old);t['energy_map']['address_response_lambda']['return']=lam
        cc,mm,ss,_=physical_context(cfg,base,effect,response_cfg=t)
        x=physical_readout(cfg,cc,mm,carrier,uniform,1,ss,t)
        t['upstream_0_9']['upstream']['update']['admission_frames_K']=4
        ef=m09.effects(t['upstream_0_9'],base);probe_mu=m10.address_moments(t,base,ef)
        y=physical_readout(cfg,cc,probe_mu,carrier,uniform,1,ss,t)
        degeneracy.append({'lambda_R':lam,'reference_q':x['deceleration_q'],'K4_q':y['deceleration_q'],
                           'eta_R_J_m3':cc['eta_J_m3']['return']})
    exchange=m10.fixed_volume_exchange(old,cal,mu,coupled,m10.m07.state_from_recipe(coupled,{'kind':'packet','modes':[8,16,24],'weights':[1/3]*3}))
    r={'version':'WRRA-M 0.11','date':'2026-10-02','input_hash_sha256':m09.digest(cfg),'input_ledger':cfg,
       'sequential_calibration':staged(cfg),'final_outputs':o,'calibration_0_10_bridge':cal,'cases':cases,
       'reference':ref,'mass_modes':masses,'address_reparameterization':reparam,'dependency_map':dependency_map(cfg),
       'input_response_probes':probes,'frozen_coefficient_address_probes':address_probes,
       'response_shape_degeneracy':degeneracy,'internal_exchange':exchange,
       'energy_operator_in_electron_units':ref['total_energy_J']/o['electron_energy_J'],
       'physical_records':[],'free_combinations':{'weighted_twist':'zeta*kappa_h^2 fixed; zeta and kappa_h not separately fixed',
           'length':'L0=length_coefficient*sqrt(W0); W0 and cosmic length are not assigned',
           'address':'two legacy arithmetic targets and phase/filter profile are disclosed inputs distinct from physical energy targets',
           'mass':'electron mode 23 and zero intercept are frozen choices; other labels and dressed masses are not fixed',
           'response':'reference energies constrain eta_s*mu_s, not arbitrary address-response shapes'},
       'remaining':['electromagnetic alpha and other gauge strengths','physical update clock and general spectra 0.12',
                    'measurement/records 0.13','mixing and neutrino propagation','global W0 and separate stiffness/twist'],
       'falsifiers':['hidden future input in a partial stage','failed inherited reproduction or pressure derivative',
                     'new anchor changes unrelated outputs','nonconserving energy or duplicated electron budget',
                     'claiming separately unidentified coefficients or mismatched documents']}
    (out/'results.json').write_text(json.dumps(r,indent=2,allow_nan=False,ensure_ascii=False)+'\n')
    write_csv(out/'mass_modes.csv',masses);write_csv(out/'input_response_probes.csv',probes)
    write_csv(out/'sequential_calibration.csv',[{'step':x['step'],'added_input':x['added_input'],
              'remaining_calibrations':' '.join(x['remaining_calibrations']),'available_outputs':' '.join(x['outputs'])} for x in r['sequential_calibration']])
    write_csv(out/'physical_cases.csv',[{'case':x['case_name'],'u_J_m3':x['total_density_J_m3'],'P_Pa':x['total_pressure_Pa'],
            'q':x['deceleration_q'],'H_s_minus1':x['H_s_minus1'],'v_km_s':x['local_readout']['v_total_km_s']} for x in cases])
    return r


if __name__=='__main__':
    r=run(json.loads((ROOT/'parameters.json').read_text()),ROOT/'results')
    print(json.dumps({'version':r['version'],'q0':r['final_outputs']['q0'],'mu_eV':r['final_outputs']['mass_mode_scale_eV']}))
