"""WRRA_M 0.12: worldline proper clocks, finite mode spectra and SI phases."""
from pathlib import Path
import csv
import importlib.util
import json
import math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('wrra11_clock_baseline',ROOT.parent/'wrra_m_0_11/compute.py')
m11=importlib.util.module_from_spec(spec);spec.loader.exec_module(m11)
m10=m11.m10;m09=m11.m09

def units(cfg):
    b=cfg['baseline_0_11'];u=b['SI'];o=m11.prefix_outputs(b,{k:b['targets'][k] for k in m11.ORDER})
    hb=u['h_J_s']/(2*math.pi);mu=o['mass_mode_scale_eV']*u['eV_J'];delta=cfg['clock']['phase_step_epsilon']*hb/mu
    return {'hbar_J_s':hb,'mu_E_eV':o['mass_mode_scale_eV'],'mu_E_J':mu,'electron_energy_eV':b['targets']['electron_energy_eV'],
            't_mu_s':hb/mu,'length_unit_m':hb*u['c_m_s']/mu,'delta_tau_s':delta,
            'Planck_time_s':o['Planck_time_s'],'delta_tau_over_Planck':delta/o['Planck_time_s'],
            'c_delta_tau_m':u['c_m_s']*delta,'phase_bandwidth_eV':2*math.pi*hb/(delta*u['eV_J'])}

def validate(cfg):
    if cfg['model_version']!='WRRA-M 0.12':raise ValueError('version mismatch')
    b=cfg['baseline_0_11'];m11.validate(b)
    if m09.digest(b)!=cfg['provenance']['baseline_0_11_input_sha256']:raise ValueError('frozen baseline changed')
    clock=cfg['clock'];s=cfg['spectra']
    if clock['rule']!='worldline_proper_time' or clock['physical_minimum_time_claim'] is not False:raise ValueError('unsupported global/minimum clock claim')
    for value in (clock['phase_step_epsilon'],s['cavity_length_over_length_unit']):
        if not math.isfinite(value) or value<=0:raise ValueError('positive clock/length coefficient required')
    for N in [s['mode_lattice_N']]+s['finite_difference_N']:
        if not isinstance(N,int) or isinstance(N,bool) or N<64 or N%2:raise ValueError('even finite mode lattice required')
    if s['mode_lattice_N']//2<=b['mass_construction']['electron_mode']:raise ValueError('electron mode outside band')
    if any(not math.isfinite(x) or not 0<=x<1 for x in s['fold_boundary_phases']):raise ValueError('boundary phase outside [0,1)')
    if any(not math.isfinite(x) or x<=0 for x in s['cavity_length_probes']):raise ValueError('invalid length probe')
    if not math.isfinite(s['alias_phase_step_epsilon']) or s['alias_phase_step_epsilon']<=0:raise ValueError('invalid alias step')
    if any(not math.isfinite(x) for x in s['free_momentum_probes']):raise ValueError('finite free momenta required')
    if any(not isinstance(n,int) or isinstance(n,bool) or not -s['mode_lattice_N']//2<=n<s['mode_lattice_N']//2 for n in s['report_fold_modes']):raise ValueError('reported fold mode outside finite band')
    if not isinstance(clock['reference_ticks'],int) or clock['reference_ticks']<=0:raise ValueError('positive tick count required')
    b0,b1=clock['accelerated_beta_coefficients']
    if not all(math.isfinite(x) for x in (b0,b1)) or not 0<=min(b0,b0+b1)<=max(b0,b0+b1)<1:raise ValueError('accelerated path must be timelike')
    if not math.isfinite(clock['lorentz_boost_beta']) or not abs(clock['lorentz_boost_beta'])<1:raise ValueError('subluminal boost required')
    if any(not math.isfinite(v) or not 0<=v<=1 for v in clock['flat_speed_probes']):raise ValueError('invalid flat path')
    R=b['baseline_0_10']['upstream_0_9']['baseline_0_8']['ledger_0_7']['calibration_and_local_source']['patch_radius_kpc']
    if any(not math.isfinite(v) or not 0<v<=R for v in clock['local_radius_probes_kpc']):raise ValueError('local path outside finite patch')
    if any(not all(math.isfinite(v) for v in pair) or not 0<pair[0]<pair[1] for pair in clock['scale_factor_intervals']):raise ValueError('invalid expansion interval')
    if cfg['physical_records']:raise ValueError('physical measurement belongs to 0.13')
    if s['spatial_boundaries']!=['periodic','dirichlet'] or s['operator_rule']!='finite spectral derivative and relativistic positive energy':raise ValueError('unsupported spatial boundary/operator rule')
    if clock['potential_boundary']!='Phi(R_patch)=0; inherited conditional Phi=Psi weak static metric':raise ValueError('unsupported potential boundary')

def fourier(N):
    n=np.rint(np.fft.fftfreq(N)*N).astype(int);x=np.arange(N)/N
    return n,np.exp(2j*math.pi*x[:,None]*n[None,:])/math.sqrt(N)

def fold_operator(cfg,boundary_phase=0.):
    # Periodic gauge phi(y); the physical twisted field is
    # psi(y)=exp(2*pi*i*eta*y)*phi(y). The derivative shifts n to n+eta.
    n,F=fourier(cfg['spectra']['mode_lattice_N']);e=units(cfg)['mu_E_eV']*abs(n+boundary_phase)
    H=(F*e)@F.conj().T
    return n,F,e,(H+H.conj().T)/2

def cavity_operator(cfg,kind,length_ratio=None):
    N=cfg['spectra']['mode_lattice_N'];u=units(cfg);lam=cfg['spectra']['cavity_length_over_length_unit'] if length_ratio is None else length_ratio
    if not math.isfinite(lam) or lam<=0:raise ValueError('positive cavity length required')
    if kind=='periodic':
        n,F=fourier(N);pc_eV=2*math.pi*u['mu_E_eV']*n/lam
    elif kind=='dirichlet':
        n=np.arange(1,N+1);F=math.sqrt(2/(N+1))*np.sin(math.pi*np.arange(1,N+1)[:,None]*n[None,:]/(N+1));pc_eV=math.pi*u['mu_E_eV']*n/lam
    else:raise ValueError('explicit periodic or dirichlet boundary required')
    e=np.hypot(u['electron_energy_eV'],pc_eV);H=(F*e)@F.conj().T
    return n,F,e,(H+H.conj().T)/2

def phase_readout(H_eV,delta_s,cfg):
    if not math.isfinite(delta_s) or delta_s<=0:raise ValueError('positive phase interval required')
    hb=units(cfg)['hbar_J_s'];eV=cfg['baseline_0_11']['SI']['eV_J'];energy,basis=np.linalg.eigh(H_eV)
    scaled=energy*delta_s*eV/hb;U=(basis*np.exp(-1j*scaled))@basis.conj().T
    theta=np.mod(-np.angle(np.linalg.eigvals(U)),2*math.pi)
    theta[np.isclose(theta,2*math.pi,atol=1e-10,rtol=0)]=0
    theta=np.sort(theta);principal=theta*hb/(delta_s*eV)
    branch=np.floor(np.maximum(scaled,0)/(2*math.pi)).astype(int)
    # Read phases from the update matrix in the declared generator eigenbasis.
    # Branch integers are supplied by the generator, never inferred from U alone.
    owned_theta=np.mod(-np.angle(np.diag(basis.conj().T@U@basis)),2*math.pi)
    owned_theta[np.isclose(owned_theta,2*math.pi,atol=1e-10,rtol=0)]=0
    owned=owned_theta*hb/(delta_s*eV)+branch*2*math.pi*hb/(delta_s*eV)
    return {'energy_eV':energy,'U':U,'theta_sorted':theta,'principal_energy_eV_sorted':principal,
            'branch_indices':branch,'branch_restored_energy_eV':owned}

def lapse(phi_over_c2,beta_local):
    if not math.isfinite(phi_over_c2) or abs(phi_over_c2)>.001:raise ValueError('outside declared weak static patch')
    if not math.isfinite(beta_local) or not 0<=beta_local<=1:raise ValueError('timelike/null speed required')
    return math.sqrt((1+2*phi_over_c2)*(1-beta_local**2))

def clock_row(name,phi_over_c2,beta,coordinate_s,cfg):
    if not math.isfinite(coordinate_s) or coordinate_s<0:raise ValueError('nonnegative interval required')
    L=lapse(phi_over_c2,beta);proper=L*coordinate_s;tick=units(cfg)['delta_tau_s'];ticks=proper/tick
    if beta==1:
        return {'name':name,'beta_local':beta,'phi_over_c2':phi_over_c2,'lapse':0.,'coordinate_s':coordinate_s,'proper_s':0.,'tick_coordinate':None,'complete_ticks':None,'residual_tick_fraction':None,'coherent_overlap':None,'scope':'null path: no rest-clock update; not frozen photon propagation'}
    whole=math.floor(ticks+1e-10);residual=ticks-whole
    if abs(residual)<1e-10:residual=0.
    phase=proper/units(cfg)['t_mu_s']
    return {'name':name,'beta_local':beta,'phi_over_c2':phi_over_c2,'lapse':L,'coordinate_s':coordinate_s,'proper_s':proper,
            'tick_coordinate':ticks,'complete_ticks':whole,'residual_tick_fraction':residual,
            'coherent_overlap':math.cos(phase/2)**2,'scope':'generic equal fold-mode pair with gap mu_E; no physical outcome record'}

def potential_ratio(radius_kpc,src,aT):
    R=src['patch_radius_kpc']
    if not math.isfinite(radius_kpc) or not 0<radius_kpc<=R:raise ValueError('clock radius outside finite patch')
    kpc=1000*src['parsec_m']
    integral=quad(lambda x:float(m10.m06.m05.plummer(np.array([x*kpc]),src,aT)['g'][0])*kpc,radius_kpc,R,epsabs=1e-3,epsrel=2e-11)[0]
    return -integral/src['c_m_s']**2

def path_refinement(cfg):
    # Prescribed flat-space accelerated worldline beta(s)=b0+b1*s, 0<=s<=1.
    b0,b1=cfg['clock']['accelerated_beta_coefficients'];T=cfg['clock']['reference_ticks']*units(cfg)['delta_tau_s']
    exact=quad(lambda s:math.sqrt(1-(b0+b1*s)**2),0,1,epsabs=1e-13,epsrel=1e-13)[0];rows=[]
    for N in (16,32,64,128):
        s=(np.arange(N)+.5)/N;v=b0+b1*s;ratio=float(np.mean(np.sqrt(1-v*v)))
        # Lorentz-transform each finite chord, in units c*T for positions.
        boost=cfg['clock']['lorentz_boost_beta'];gamma=1/math.sqrt(1-boost*boost);dt=np.ones(N)/N;dx=v/N
        dtp=gamma*(dt-boost*dx);dxp=gamma*(dx-boost*dt)
        transformed=float(np.sum(np.sqrt(dtp*dtp-dxp*dxp)))
        rows.append({'segments':N,'proper_over_T':ratio,'exact_proper_over_T':exact,'absolute_ratio_error':abs(ratio-exact),'boosted_proper_over_T':transformed})
    count=math.floor(cfg['clock']['reference_ticks']*exact);events=[]
    for k in range(count+1):
        target=k/cfg['clock']['reference_ticks']
        if k==0:s=0.
        else:s=brentq(lambda z:quad(lambda t:math.sqrt(1-(b0+b1*t)**2),0,z,epsabs=1e-12,epsrel=1e-12)[0]-target,0,1,xtol=1e-13)
        events.append({'proper_frame':k,'coordinate_time_over_T':s,'proper_time_s':k*units(cfg)['delta_tau_s']})
    return {'beta_coefficients':[b0,b1],'coordinate_duration_s':T,'exact_proper_over_T':exact,'complete_frames':count,'residual_tick_fraction':cfg['clock']['reference_ticks']*exact-count,'refinement':rows,'events':events}

def write_csv(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def run(cfg,out):
    validate(cfg);out.mkdir(parents=True,exist_ok=True);b=cfg['baseline_0_11'];old=b['baseline_0_10'];u=units(cfg)
    base=m09.address_base(old['upstream_0_9']);effect=m09.effects(old['upstream_0_9'],base);cal,mu,src,o=m11.physical_context(b,base,effect)
    T=cfg['clock']['reference_ticks']*u['delta_tau_s'];flat=[clock_row(f'flat_beta_{beta}',0,beta,T,cfg) for beta in cfg['clock']['flat_speed_probes']]
    local=[]
    for radius in cfg['clock']['local_radius_probes_kpc']:
        phi=potential_ratio(radius,src,o['aT_m_s2']);x=clock_row(f'static_r{radius}',phi,0,T,cfg);x['radius_kpc']=radius;local.append(x)
    source_p=old['upstream_0_9']['baseline_0_8']['ledger_0_7']['carrier_and_background']
    radius=source_p['test_radius_kpc'];phi=potential_ratio(radius,src,o['aT_m_s2']);v=float(m10.m06.m05.plummer(np.array([radius*1000*src['parsec_m']]),src,o['aT_m_s2'])['v'][0])/src['c_m_s']
    local.append(dict(clock_row('inherited_circular_clock',phi,v,T,cfg),radius_kpc=radius))
    cosmic=[]
    for a0,a1 in cfg['clock']['scale_factor_intervals']:
        dtH=quad(lambda a:1/(a*math.sqrt((b['targets']['f_phi']+b['targets']['f_c'])/a**3+o['f_b'])),a0,a1,epsabs=1e-12,epsrel=1e-12)[0]
        for beta in (0.,.6):
            proper=dtH/o['H0_s_minus1']*math.sqrt(1-beta*beta)
            cosmic.append({'a_start':a0,'a_end':a1,'beta_peculiar':beta,'coordinate_interval_H0_t':dtH,'proper_interval_s':proper,'tick_count_order':proper/u['delta_tau_s'],
                           'scope':'uniform reference FRW clock; tick estimate inherits floating-point and input precision, not an exact giant integer'})
    n,F,e,H=fold_operator(cfg);ph=phase_readout(H,u['delta_tau_s'],cfg);fold=[]
    for eta in cfg['spectra']['fold_boundary_phases']:
        nn,ff,ee,hh=fold_operator(cfg,eta)
        for mode in cfg['spectra']['report_fold_modes']:
            j=int(np.flatnonzero(nn==mode)[0]);fold.append({'boundary_phase':eta,'mode':mode,'energy_eV':float(ee[j]),'theta':float((ee[j]/u['mu_E_eV']*cfg['clock']['phase_step_epsilon'])%(2*math.pi))})
    cavities=[]
    for kind in ('periodic','dirichlet'):
        nn,ff,ee,hh=cavity_operator(cfg,kind)
        report=range(0,5) if kind=='periodic' else range(1,6)
        for mode in report:
            j=int(np.flatnonzero(nn==mode)[0]);cavities.append({'boundary':kind,'mode':mode,'length_m':cfg['spectra']['cavity_length_over_length_unit']*u['length_unit_m'],'energy_eV':float(ee[j]),'kinetic_energy_eV':float(ee[j]-u['electron_energy_eV'])})
    spacing=[]
    for lam in cfg['spectra']['cavity_length_probes']:
        nn,ff,ee,hh=cavity_operator(cfg,'periodic',lam);zero=ee[np.flatnonzero(nn==0)[0]];first=ee[np.flatnonzero(nn==1)[0]]
        spacing.append({'length_over_unit':lam,'length_m':lam*u['length_unit_m'],'momentum_step_c_eV':2*math.pi*u['mu_E_eV']/lam,'first_kinetic_gap_eV':float(first-zero),'scope':'finite-volume spacing control; no physically realized infinite support'})
    free=[{'pc_over_mu':x,'energy_eV':float(u['mu_E_eV']*math.hypot(b['mass_construction']['electron_mode'],x)),
           'theta':float((math.hypot(b['mass_construction']['electron_mode'],x)*cfg['clock']['phase_step_epsilon'])%(2*math.pi)),'scope':'continuous local dispersion evaluated at finite noninteger momentum probes'} for x in cfg['spectra']['free_momentum_probes']]
    fd=[]
    for N in cfg['spectra']['finite_difference_N']:
        mode=b['mass_construction']['electron_mode'];value=u['mu_E_eV']*N*abs(math.sin(math.pi*mode/N))/math.pi
        fd.append({'N':N,'mode':mode,'energy_eV':value,'relative_mass_error':value/u['electron_energy_eV']-1,'calibration_refit':False})
    car=m10.m06.Carrier(source_p['lattice_N'],source_p['noncommuting_test_strength']);EH=m10.energy_operator(old,cal,mu,car,1);E0=cal['ucrit_J_m3']*old['reference_volume_m3']
    psi=m10.m07.state_from_recipe(car,{'kind':'packet','modes':[8,16,24],'weights':[1/3]*3});vals,vec=np.linalg.eigh(EH/E0);evol=[]
    for k in (0,1,2,4,8):
        xi=k*u['delta_tau_s']*E0/u['hbar_J_s'];U=(vec*np.exp(-1j*xi*vals))@vec.conj().T;rho=U@psi@U.conj().T
        x=m11.physical_readout(b,cal,mu,car,rho,1,src)
        evol.append({'proper_frame':k,'proper_s':k*u['delta_tau_s'],'legacy_dimensionless_coordinate':xi,'state_trace':float(np.trace(rho).real),'minimum_state_eigenvalue':float(np.linalg.eigvalsh(rho).min()),'total_energy_J':x['total_energy_J'],'D_load':x['operator_loads']['resident_nonphenotype'],'R_load':x['operator_loads']['return'],'q':x['deceleration_q']})
    omega=source_p['information_clock_over_H0']*o['H0_s_minus1'];ratio=u['hbar_J_s']*omega/E0
    alias=phase_readout(H,cfg['spectra']['alias_phase_step_epsilon']*u['t_mu_s'],cfg)
    r={'version':'WRRA-M 0.12','date':'2026-10-03','input_hash_sha256':m09.digest(cfg),'input_ledger':cfg,'units':u,'flat_clocks':flat,'local_clocks':local,'cosmic_clocks':cosmic,'accelerated_worldline':path_refinement(cfg),
       'fold_modes':fold,'cavity_modes':cavities,'finite_volume_spacing':spacing,'free_dispersion':free,'finite_difference_controls':fd,
       'phase_recovery':{'fold_dimension':len(n),'unwrapped_branch':0,'max_spectral_phase_energy_error_eV':float(np.max(abs(np.sort(e)-ph['principal_energy_eV_sorted']))),'unitarity_error':float(np.linalg.norm(ph['U'].conj().T@ph['U']-np.eye(len(n))))},
       'alias_control':{'phase_step_epsilon':cfg['spectra']['alias_phase_step_epsilon'],'nonzero_branch_modes':int(np.count_nonzero(alias['branch_indices'])),'max_naive_sorted_energy_error_eV':float(np.max(abs(np.sort(e)-alias['principal_energy_eV_sorted']))),'max_owned_branch_error_eV':float(np.max(abs(alias['energy_eV']-alias['branch_restored_energy_eV']))),'claim':'one update unitary alone leaves integer energy branches undetermined'},
       'physical_ledger_updates':evol,'legacy_clock_comparison':{'old_information_frequency_s_minus1':omega,'SI_ledger_frequency_s_minus1':E0/u['hbar_J_s'],'old_frequency_over_SI_frequency':ratio,'fixed_volume_identity':'xi=E_star*tau/hbar gives exactly the same SI-energy update','old_expansion_clock_is_physical_SI_phase':False,'scope':'old slow expansion-state schedule retained as a constitutive record, not identified with the SI Hamiltonian proper-time phase'},
       'physical_records':[],'remaining':['origin and empirical calibration of shutter epsilon','selection of actual microscopic confinement and boundary phases','complete covariant interacting mode/clock dynamics','physical measurements and records 0.13'],
       'falsifiers':['improper clock lapse or Lorentz-frame disagreement','nonunitary or nonconserving static SI update','failed mode/phase reproduction under stated boundaries','discarded integer quasienergy branch','identifying the old slow clock with SI energy phase without the computed conversion','claiming a measured minimum time or actual infinite support']}
    (out/'results.json').write_text(json.dumps(r,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    for name,rows in [('flat_clocks',flat),('local_clocks',local),('cosmic_clocks',cosmic),('fold_modes',fold),('cavity_modes',cavities),('free_dispersion',free),('physical_ledger_updates',evol),('worldline_events',r['accelerated_worldline']['events'])]:write_csv(out/(name+'.csv'),rows)
    return r

if __name__=='__main__':
    r=run(json.loads((ROOT/'parameters.json').read_text()),ROOT/'results');print(json.dumps({'version':r['version'],'delta_tau_s':r['units']['delta_tau_s'],'fold_phase_error_eV':r['phase_recovery']['max_spectral_phase_energy_error_eV']}))
