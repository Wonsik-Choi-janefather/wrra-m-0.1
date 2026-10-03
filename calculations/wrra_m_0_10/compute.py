"""WRRA-M 0.10: explicit positive SI address energy and volume pressure.

The frozen reference fixes three dimensional coefficients once. Changed
addresses or carrier states never trigger a hidden refit. Physical measurement
outcomes are outside this stage; admission rows remain expected transport.
"""
from __future__ import annotations
from pathlib import Path
import copy
import csv
import json
import math
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp
import importlib.util

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('wrra09_energy_bridge', ROOT.parent/'wrra_m_0_9/compute.py')
m09 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m09)
m07 = m09.m08.m07
m06 = m07.m06
SECTORS = m09.SECTORS


def validate(cfg):
    if cfg['model_version'] != 'WRRA-M 0.10':
        raise ValueError('unsupported version')
    m09.validate(cfg['upstream_0_9'])
    if m09.digest(cfg['upstream_0_9']) != cfg['provenance']['baseline_0_9_input_sha256']:
        raise ValueError('baseline input changed without a new provenance declaration')
    v = cfg['reference_volume_m3']
    if not math.isfinite(v) or v <= 0:
        raise ValueError('positive finite reference volume required')
    e = cfg['energy_map']
    if e['rule'] != 'positive_address_response_times_carrier_operator' or e['operator_rule'] != 'phenotype_I_D_Kc_over_2_R_Kb_over_2':
        raise ValueError('unsupported energy map')
    if e['pending_SOURCE_response'] != 'same epsilon as return background response':
        raise ValueError('unsupported SOURCE correspondence')
    for field in ('address_response_lambda', 'energy_volume_exponents', 'reference_energy_fractions', 'alternate_energy_fractions'):
        if set(e[field]) != set(SECTORS):
            raise ValueError('invalid sector keys')
        values = list(e[field].values())
        if any(not math.isfinite(x) or x < 0 for x in values):
            raise ValueError('nonnegative finite sector data required')
    if e['energy_volume_exponents']['phenotype'] != 0 or e['energy_volume_exponents']['resident_nonphenotype'] != 0:
        raise ValueError('pressureless phenotype and clustering required for inherited local renderer')
    if not 0 <= e['energy_volume_exponents']['return'] <= 3:
        raise ValueError('unsupported background exponent')
    for field in ('reference_energy_fractions', 'alternate_energy_fractions'):
        if abs(sum(e[field].values())-1) > 1e-12:
            raise ValueError('energy fractions must sum to one')
    if cfg['scope']['measurement_records']:
        raise ValueError('physical measurement records are outside this stage')
    for a in cfg['probes']['scale_factors']+[cfg['probes']['transition_scale_factor']]:
        if not math.isfinite(a) or a <= 0:
            raise ValueError('positive scale factors required')
    clocks = cfg['probes']['fixed_volume_clock_coordinates']
    if not clocks or any(not math.isfinite(t) or t < 0 for t in clocks):
        raise ValueError('invalid fixed-volume clock coordinates')


def response(cfg, base):
    # N is an address cutoff. This dimensionless response introduces no length.
    x = np.log(base['n'])/math.log(cfg['upstream_0_9']['upstream']['address_cutoff_N'])
    return np.array([1+cfg['energy_map']['address_response_lambda'][s]*x for s in SECTORS])


def address_moments(cfg, base, effect):
    return np.sum(effect*response(cfg, base)*base['w'][None, :], axis=1)


def calibrate(cfg, base, effect, target=None):
    """Explicit once-only SI fit on the frozen reference, not on each probe."""
    target = cfg['energy_map']['reference_energy_fractions'] if target is None else target
    if set(target) != set(SECTORS) or any(not math.isfinite(v) or v < 0 for v in target.values()) or abs(sum(target.values())-1) > 1e-12:
        raise ValueError('invalid SI calibration target')
    mu = address_moments(cfg, base, effect)
    b = cfg['upstream_0_9']['baseline_0_8']['ledger_0_7']['calibration_and_local_source']
    c = m06.calibration(b)
    # Tr[(I/N) A_s]=1 for I, Kc/2 and the normalized Kb/2.
    eta = []
    for i, s in enumerate(SECTORS):
        if mu[i] <= 0 and target[s] > 0:
            raise ValueError('positive calibrated energy has zero reference support')
        eta.append(c['ucrit_J_m3']*target[s]/mu[i] if mu[i] > 0 else 0.)
    return {'ucrit_J_m3':c['ucrit_J_m3'], 'H0_s_minus1':c['H0_s_minus1'],
            'reference_address_moments':dict(zip(SECTORS,map(float,mu))),
            'eta_J_m3':dict(zip(SECTORS,map(float,eta))),
            'target_energy_fractions':copy.deepcopy(target),
            'ownership':'three positive SI response coefficients fit to disclosed sector-energy targets; not equal energy per bit',
            'reference_state':'frozen 0.9 address measure and uniform carrier'}


def operators(carrier):
    return (np.eye(carrier.N), carrier.Kc/2, carrier.Kb/2)


def amplitudes(cfg, calibration, mu, a):
    if not math.isfinite(a) or a <= 0:
        raise ValueError('invalid scale factor')
    if np.shape(mu) != (3,) or not np.isfinite(mu).all() or min(mu) < 0:
        raise ValueError('invalid address moments')
    return np.array([calibration['eta_J_m3'][s]*mu[i]*a**cfg['energy_map']['energy_volume_exponents'][s]
                     for i,s in enumerate(SECTORS)])


def ledger(cfg, calibration, mu, carrier, rho, a, *, include_local=True):
    rho = m07.validate_state(rho, carrier.N)
    op = operators(carrier)
    loads = np.array([float(np.trace(rho@A).real) for A in op])
    if min(loads) < -1e-12:
        raise ValueError('negative physical carrier load')
    loads = np.maximum(loads,0)  # every positive load, however small, is retained
    V0 = cfg['reference_volume_m3']; V = V0*a**3
    energy = V0*amplitudes(cfg, calibration, mu, a)*loads
    density = energy/V
    n = np.array([cfg['energy_map']['energy_volume_exponents'][s] for s in SECTORS])
    pressure = -n*density/3
    total = float(energy.sum()); u = float(density.sum()); P = float(pressure.sum())
    crit = calibration['ucrit_J_m3']
    result = {'scale_factor':float(a),'volume_m3':V,'lattice_N':carrier.N,
              'carrier_epsilon':carrier.epsilon,'state_trace':float(np.trace(rho).real),
              'address_moments':dict(zip(SECTORS,map(float,mu))),
              'operator_loads':dict(zip(SECTORS,map(float,loads))),
              'sector_energy_J':dict(zip(SECTORS,map(float,energy))),
              'sector_density_J_m3':dict(zip(SECTORS,map(float,density))),
              'sector_pressure_Pa':dict(zip(SECTORS,map(float,pressure))),
              'sector_energy_fractions':dict(zip(SECTORS,map(float,energy/total))) if total > 0 else dict.fromkeys(SECTORS),
              'total_energy_J':total,'total_density_J_m3':u,'total_pressure_Pa':P,
              'H_over_H0':math.sqrt(u/crit),'H_s_minus1':calibration['H0_s_minus1']*math.sqrt(u/crit),
              'deceleration_q':.5*(u+3*P)/u if u > 0 else None,
              'arithmetic_share_policy':'arithmetic shares are preserved separately and are not energy fractions',
              'measurement_records':[]}
    if include_local:
        old = cfg['upstream_0_9']['baseline_0_8']['ledger_0_7']
        p,b = old['carrier_and_background'],old['calibration_and_local_source']
        c = m06.calibration(b)
        snapshot = {'aT_over_reference':math.sqrt(density[1]/(crit*c['fc'])),
                    'hidden_density_over_reference':float(density[1:].sum())/(crit*c['fh'])}
        result['local_readout'] = m06.local_readout(snapshot,p,b,c)
    return result


def energy_operator(cfg, calibration, mu, carrier, a):
    # Hamiltonian has J units. Its state trace is the same ledger total energy.
    return cfg['reference_volume_m3']*sum(k*A for k,A in zip(amplitudes(cfg,calibration,mu,a),operators(carrier)))


def fixed_volume_exchange(cfg, calibration, mu, carrier, rho0):
    a = cfg['probes']['transition_scale_factor']; H = energy_operator(cfg,calibration,mu,carrier,a)
    E0 = calibration['ucrit_J_m3']*cfg['reference_volume_m3']
    rows = []; previous = ledger(cfg,calibration,mu,carrier,rho0,a,include_local=False)
    for t in cfg['probes']['fixed_volume_clock_coordinates']:
        U = expm(-1j*t*H/E0)
        rho = U@rho0@U.conj().T
        now = ledger(cfg,calibration,mu,carrier,rho,a,include_local=False)
        delta = {s:now['sector_energy_J'][s]-previous['sector_energy_J'][s] for s in SECTORS}
        rows.append({'clock_coordinate':t,'state_trace':float(np.trace(rho).real),
                     'minimum_state_eigenvalue':float(np.linalg.eigvalsh(rho).min()),
                     'energy_change_J':delta,'exchange_sum_J':sum(delta.values()),
                     'energy_J':now['total_energy_J'],
                     'D_operator_load':now['operator_loads']['resident_nonphenotype'],
                     'R_operator_load':now['operator_loads']['return']})
        previous = now
    return rows


def expansion_history(cfg, calibration, mu, carrier, psi0):
    """Constitutive slow schedule with the energy shape and volume pressure.

    This schedule does not identify omega_info with the SI phase frequency
    E_star/hbar. The mismatch established in 0.12 is retained explicitly.
    """
    E0 = calibration['ucrit_J_m3']*cfg['reference_volume_m3']
    omega = cfg['upstream_0_9']['baseline_0_8']['ledger_0_7']['carrier_and_background']['information_clock_over_H0']
    def rhs(loga, psi):
        a = math.exp(loga)
        A = amplitudes(cfg,calibration,mu,a)/calibration['ucrit_J_m3']
        kc,kb = carrier.apply(psi)
        hpsi = A[0]*psi + A[1]*kc/2 + A[2]*kb/2
        norm = float(np.vdot(psi,psi).real)
        energy = float(np.vdot(psi,hpsi).real)/norm
        density = energy/a**3
        if density <= 0:
            raise ValueError('expanding clock undefined on zero total density')
        return -1j*omega*hpsi/math.sqrt(density)
    rows=[]
    for target in (.5,1.,2.):
        if target == 1: psi=psi0
        else:
            sol=solve_ivp(rhs,(0,math.log(target)),psi0,method='DOP853',rtol=1e-10,atol=1e-12,max_step=.03)
            if not sol.success: raise RuntimeError(sol.message)
            psi=sol.y[:,-1]
        norm=float(np.vdot(psi,psi).real);rho=np.outer(psi,psi.conj())/norm
        item=ledger(cfg,calibration,mu,carrier,rho,target)
        H=energy_operator(cfg,calibration,mu,carrier,target)/E0
        drho=-1j*(H@rho-rho@H)
        coeff=amplitudes(cfg,calibration,mu,target)/calibration['ucrit_J_m3']
        sector_exchange=np.array([k*float(np.trace(drho@A).real) for k,A in zip(coeff,operators(carrier))])
        n=np.array([cfg['energy_map']['energy_volume_exponents'][s] for s in SECTORS])
        u=np.array(list(item['sector_density_J_m3'].values()))/calibration['ucrit_J_m3']
        continuity=float(np.sum((n-3)*u)+3*(u.sum()+item['total_pressure_Pa']/calibration['ucrit_J_m3']))
        hbar = 6.62607015e-34/(2*math.pi)
        omega_info = omega*calibration['H0_s_minus1']
        item.update(raw_state_norm=norm,state_exchange_sum_over_reference=float(sector_exchange.sum()),
                    continuity_residual_over_ucrit=continuity,
                    state_clock_rule='constitutive slow schedule; dxi/dt=omega_info',
                    old_information_frequency_s_minus1=omega_info,
                    SI_energy_phase_frequency_s_minus1=E0/hbar,
                    old_frequency_over_SI_frequency=hbar*omega_info/E0,
                    physical_SI_phase_identification=False)
        rows.append(item)
    return rows


def frame_energy_transport(cfg, calibration, base, carrier, rho):
    """Four address fields with explicit energy-difference exchange on each edge.

    Frames are dimensionless construction order. The signed exchange account
    represents the owner of conversion work, not a fourth cosmic energy sector.
    S and R have identical per-address energy, so the recovery relabel has zero
    energy exchange. Admission S->phi generally requires disclosed conversion work.
    """
    op=operators(carrier);loads=np.array([float(np.trace(rho@A).real) for A in op])
    a=cfg['probes']['transition_scale_factor'];V0=cfg['reference_volume_m3']
    eps=V0*amplitudes(cfg,calibration,np.ones(3),a)[:,None]*response(cfg,base)*loads[:,None]
    w=base['w'];odd=base['odd'];D=w*base['even'];remaining=w.copy();remaining[base['even']]=0
    phi=np.zeros_like(w);R=np.zeros_like(w);work=0.;rows=[]
    def row(k,energy_transfer,work_transfer,phase):
        E_phi=float(phi@eps[0]);E_D=float(D@eps[1]);E_S=float(remaining@eps[2]);E_R=float(R@eps[2])
        rows.append({'frame':k,'phase':phase,'phenotype_weight':float(phi.sum()),
                     'D_weight':float(D.sum()),'S_pending_weight':float(remaining.sum()),'R_weight':float(R.sum()),
                     'phenotype_energy_J':E_phi,'D_energy_J':E_D,'S_pending_energy_J':E_S,'R_energy_J':E_R,
                     'current_energy_J':E_phi+E_D+E_S+E_R,'conversion_work_account_J':work,
                     'edge_energy_change_J':energy_transfer,'edge_conversion_work_J':work_transfer,
                     'accounted_energy_J':E_phi+E_D+E_S+E_R+work})
    row(-1,0.,0.,'before_admission')
    from scipy.special import expit
    drive=m09.phase_drive(cfg['upstream_0_9'],base['n'][odd])
    for k,delta in enumerate(drive):
        birth=remaining[odd]*expit(delta-cfg['upstream_0_9']['upstream']['update']['sigmoid_threshold_h'])
        edge=float(birth@(eps[0,odd]-eps[2,odd]))
        phi[odd]+=birth;remaining[odd]-=birth;work-=edge
        row(k,edge,-edge,'admission')
    K=len(drive);R=remaining.copy();remaining[:]=0
    row(K,0.,0.,'recovery_same_energy_relabel')
    return rows


def csv_write(path, rows):
    if not rows:return
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def run(cfg,out):
    validate(cfg);out.mkdir(parents=True,exist_ok=True);input_hash=m09.digest(cfg)
    base=m09.address_base(cfg['upstream_0_9']);effect=m09.effects(cfg['upstream_0_9'],base)
    baseline=m09.run(cfg['upstream_0_9'],out/'upstream_0_9')
    refcal=calibrate(cfg,base,effect);altcal=calibrate(cfg,base,effect,cfg['energy_map']['alternate_energy_fractions'])
    mu=address_moments(cfg,base,effect)
    old=cfg['upstream_0_9']['baseline_0_8']['ledger_0_7'];p=old['carrier_and_background'];N=p['lattice_N']
    plain=m06.Carrier(N,0.);coupled=m06.Carrier(N,p['noncommuting_test_strength'])
    cases=[]
    baseline08=json.loads((out/'upstream_0_9/baseline_0_8/results.json').read_text())
    for item in baseline08['cases']:
        carrier=coupled if item['carrier_epsilon'] else plain
        rho=m07.state_from_recipe(carrier,item['state_recipe'])
        row=ledger(cfg,refcal,mu,carrier,rho,item['scale_factor'])
        row.update(case_name=item['case_name'],state_recipe=item['state_recipe'])
        cases.append(row)
    rho0=m07.state_from_recipe(coupled,{'kind':'packet','modes':p['noncommuting_test_initial_modes'],'weights':p['noncommuting_test_initial_weights']})
    psi0=coupled.packet(p['noncommuting_test_initial_modes'],p['noncommuting_test_initial_weights'])
    fixed=fixed_volume_exchange(cfg,refcal,mu,coupled,rho0)
    history=expansion_history(cfg,refcal,mu,coupled,psi0)
    frame=frame_energy_transport(cfg,refcal,base,plain,np.eye(N)/N)
    probes=[]
    for name,adjust in [('reference',None),('K4',4),('K16',16),('xi_zero',0)]:
        trial=copy.deepcopy(cfg)
        if name.startswith('K'):trial['upstream_0_9']['upstream']['update']['admission_frames_K']=adjust
        if name=='xi_zero':trial['upstream_0_9']['upstream']['update']['phase_step_xi']=0.
        ef=m09.effects(trial['upstream_0_9'],base);mm=address_moments(trial,base,ef)
        x=ledger(trial,refcal,mm,plain,np.eye(N)/N,1.)
        probes.append({'case':name,'arithmetic_shares':m09.shares(ef,base['w']),'physical':x,
                       'coefficient_policy':'reference eta held unchanged'})
    alt=ledger(cfg,altcal,mu,plain,np.eye(N)/N,1.)
    samples=[]
    response0=response(cfg,base)
    for n in cfg['upstream_0_9']['upstream']['sample_addresses']:
        i=n-2
        samples.append({'address':n,'normalized_address_weight':float(base['w'][i]),
                        **{s+'_effect':float(effect[j,i]) for j,s in enumerate(SECTORS)},
                        **{s+'_epsilon_reference_J':refcal['eta_J_m3'][s]*cfg['reference_volume_m3']*float(response0[j,i]) for j,s in enumerate(SECTORS)}})
    weighted_base=dict(base);weighted_base['w']=base['w']*response0[0]
    ref08=next(v for v in baseline08['cases'] if v['case_name']=='uniform_a1.0')
    channel=m09.channel_join(cfg['upstream_0_9'],weighted_base,effect,ref08)
    for item in channel:item['phenotype_channel_energy_J']=item['arithmetic_phenotype_weight']*refcal['eta_J_m3']['phenotype']*cfg['reference_volume_m3']
    result={'version':'WRRA-M 0.10','date':'2026-10-02','input_hash_sha256':input_hash,'input_ledger':cfg,
            'upstream_0_9_input_hash_sha256':baseline['input_hash_sha256'],
            'common_arithmetic_ledger':baseline['terminal_common_arithmetic_ledger'],
            'calibration':refcal,'alternate_calibration':altcal,'alternate_reference':alt,
            'cases':cases,'frozen_coefficient_address_probes':probes,
            'fixed_volume_exchange':fixed,'expansion_state_history':history,'frame_energy_transport':frame,
            'address_energy_samples':samples,'phenotype_channel_energy':channel,
            'physical_records':[],'measurement_events':[],
            'executed_connection':'0.9 address effects -> positive SI energy operator -> same volume derivative pressure -> inherited gravity and homogeneous expansion',
            'remaining':'sequential calibration 0.11; shutter/physical clock/spectrum 0.12; measurement and physical record generation 0.13',
            'falsifiers':['negative admissible energy or invalid state','fixed calibration fails reference reproduction',
                          'volume derivative disagrees with pressure','unowned conversion work or nonzero internal total exchange',
                          'channel or family energies double counted','documentation disagrees with executed result']}
    if m09.digest(cfg)!=input_hash:raise RuntimeError('input changed during calculation')
    (out/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    csv_write(out/'address_energy_samples.csv',samples);csv_write(out/'frame_energy_transport.csv',frame)
    csv_write(out/'case_table.csv',[{'case':x['case_name'],'a':x['scale_factor'],'u_J_m3':x['total_density_J_m3'],
        'P_Pa':x['total_pressure_Pa'],'q':x['deceleration_q'],'H_over_H0':x['H_over_H0'],
        'v_km_s':x['local_readout']['v_total_km_s']} for x in cases])
    return result


if __name__=='__main__':
    result=run(json.loads((ROOT/'parameters.json').read_text()),ROOT/'results')
    reference=next(c for c in result['cases'] if c['case_name']=='uniform_a1.0')
    print(json.dumps({'version':result['version'],'reference':reference,'alternate_reference':result['alternate_reference']},indent=2))
