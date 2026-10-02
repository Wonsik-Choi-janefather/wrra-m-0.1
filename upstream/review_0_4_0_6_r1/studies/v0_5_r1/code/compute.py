#!/usr/bin/env python3
"""Upstream 0.5: bounded spatial completion, conditional scale calibration.

Run with OPENBLAS_NUM_THREADS=2 for reproducible numerical reductions.
Magnetic, axial and radius operators all act on the same projected state.
The N(1440) real pole centroid is an assignment input, not a predicted width.
"""
from pathlib import Path
import copy, hashlib, json, math
import numpy as np
from scipy.linalg import eigh, expm
import model

from review_contracts import validate_scalars
ROOT=Path(__file__).resolve().parent

def validate(inp):
    validate_scalars(inp)
    model.v4.check_inputs(inp)
    s=inp['spatial_extension'];r=inp['radius_calibration'];p=inp['excitation_calibration']
    for key in ('reference_shell_order','quadrature_radial_order','quadrature_angular_order'):
        if type(s[key]) is not int or s[key]<1:raise ValueError(key)
    orders=s['shell_orders']
    if not orders or any(type(k) is not int or not 1<=k<=s['reference_shell_order'] for k in orders):raise ValueError('shell_orders')
    if any(a>=b for a,b in zip(orders,orders[1:])):raise ValueError('shell_orders must be strictly increasing')
    for key in ('alternate_quadrature_radial_order','alternate_quadrature_angular_order'):
        if type(s[key]) is not int or s[key]<s['reference_shell_order']+3:raise ValueError(key+' must cover holdout shell')
    for key in ('quadrature_radial_order','quadrature_angular_order'):
        if s[key]<s['reference_shell_order']+1:raise ValueError(key+' does not resolve reference shell')
    if not s['screening_sensitivity']:raise ValueError('empty screening controls')
    if not math.isfinite(r['standard_uncertainty_fm']) or not 0<r['standard_uncertainty_fm']<r['proton_rms_charge_radius_fm']:raise ValueError('radius uncertainty')
    limits=p['pole_centroid_range_MeV']
    if len(limits)!=2 or not all(math.isfinite(x) and x>sum(inp['masses'][k] for k in ('proton','neutron'))/2 for x in limits) or limits[0]>limits[1]:raise ValueError('pole range')
    if not math.isfinite(s['screening_lambda']) or s['screening_lambda']<=0 or any(not math.isfinite(x) or x<=0 for x in s['screening_sensitivity']):raise ValueError('screening')
    if not math.isfinite(r['proton_rms_charge_radius_fm']) or r['proton_rms_charge_radius_fm']<=0:raise ValueError('radius')
    if not math.isfinite(p['pole_centroid_MeV']) or p['pole_centroid_MeV']<=sum(inp['masses'][k] for k in ('proton','neutron'))/2:raise ValueError('excitation')

def constants(inp):
    _,blocks=model.v4.old.finite_states()
    _,_,mu_u,mu_d,_,_=model.v4.response_energies(inp,blocks)
    g=abs(inp['axial_calibration']['signed_lambda']);q=(5/3-g)/(4/3)
    ri=inp['inherited'];R=math.prod(model.v4.old.euler_activity(p,ri['alpha'],ri['N']) for p in (3,5))
    c0=(sum(inp['magnetic_moments_muN'].values())-mu_u-mu_d)/2
    c1=(inp['magnetic_moments_muN']['proton']-inp['magnetic_moments_muN']['neutron']-(mu_u-mu_d)*g)/2
    return {'q':q,'R':R,'c0':c0,'c1':c1,'mu_u':mu_u,'mu_d':mu_d}

def calibrate(m,inp):
    c=constants(inp);x=model.solve_x(m,c['q']);_,e,_,g=model.diagonalize(m,x)
    mbar=(inp['masses']['proton']+inp['masses']['neutron'])/2
    gap=inp['excitation_calibration']['pole_centroid_MeV']-mbar
    delta=gap/(e[1]-e[0]);rp2=float(g@m['radius_proton']@g)
    ell=inp['radius_calibration']['proton_rms_charge_radius_fm']/math.sqrt(rp2)
    coherence=float(g@m['bounded']@g)
    return {**c,'x':x,'C':x/math.sqrt(c['R']),'delta_MeV':float(delta),'ell_fm':ell,
            'eta':c['c1']/(x*coherence),'coherence':coherence}

def operators(m,p):
    n=m['retained_dimension'];I=np.eye(n);u,d=p['mu_u'],p['mu_d'];qe=m['Eweight']
    out={}
    for name,sgn,a,b in [('proton',1,u,d),('neutron',-1,d,u)]:
        ds=(4*a-b)/3;de=(2*a+b)/3
        out[name]=ds*I+(de-ds)*qe+p['c0']*I+sgn*p['eta']*p['x']*m['bounded']
    return out

def evaluate(m,p,inp):
    H,e,V,g=model.diagonalize(m,p['x']);M=operators(m,p)
    q=float(g@m['Eweight']@g);ga=float(g@m['axial']@g)
    nres={}
    for name,op in M.items():
        trans=V.T@op@g
        chi=float(2*np.sum(trans[1:]**2/(p['delta_MeV']*(e[1:]-e[0]))))
        nres[name]={'moment_muN':float(g@op@g),'excited_moment_muN':float(V[:,1]@op@V[:,1]),
            'first_transition_abs_muN':float(abs(trans[1])),
            'internal_susceptibility_MeV_minus1':chi,
            'first_state_susceptibility_fraction':float((2*trans[1]**2/(p['delta_MeV']*(e[1]-e[0])))/chi),
            'ground_mass_MeV':inp['masses'][name]}
    wc=inp['weak_constants'];mp,mn,me=(inp['masses'][k] for k in ('proton','neutron','electron'))
    phase=model.v4.old.phase(mn-mp-me,me,wc['alpha_em'])
    pref=(wc['GF_GeV_minus2']*1e-6)**2*wc['Vud']**2*me**5/(2*math.pi**3*wc['hbar_MeV_s'])
    life=1/(inp['inherited']['kappa']**2*p['R']*pref*(1+3*ga*ga)*phase)
    rp=float(g@m['radius_proton']@g)*p['ell_fm']**2;rn=float(g@m['radius_neutron']@g)*p['ell_fm']**2
    old_overlap=float(np.sum((m['reference'].T@g)**2))
    return {'shell_order':m['K'],'spatial_modes':m['spatial_dimension'],'retained_dimension':m['retained_dimension'],
        'ground_energy_over_delta':float(e[0]),'gap_over_delta':float(e[1]-e[0]),
        'gap_MeV':float((e[1]-e[0])*p['delta_MeV']),'q_E':q,'gA':ga,'gV':1.,'mean_life_s':life,
        'proton_radius_fm':math.sqrt(rp),'neutron_charge_mean_square_fm2':rn,
        'old_two_configuration_probability':old_overlap,'higher_configuration_probability':1-old_overlap,
        'shell_probabilities':{str(k):float(np.sum(g[m['column_shells']==k]**2)) for k in range(m['K']+1)},
        'nucleons':nres}

def rounded(obj):
    if isinstance(obj,dict):return {k:rounded(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):return [rounded(v) for v in obj]
    if isinstance(obj,(float,np.floating)):return round(float(obj),11)
    if isinstance(obj,(np.bool_,bool)):return bool(obj)
    if isinstance(obj,np.integer):return int(obj)
    return obj

def run(inp):
    validate(inp);s=inp['spatial_extension'];K=s['reference_shell_order']
    m=model.build(K,s['quadrature_radial_order'],s['quadrature_angular_order'],s['screening_lambda'])
    p=calibrate(m,inp);r=evaluate(m,p,inp);checks={'basis_'+k:v for k,v in m['checks'].items()}
    _,e,V,g=model.diagonalize(m,p['x']);n=m['retained_dimension'];M=operators(m,p)
    refit=[];frozen=[];bare=[]
    for k in s['shell_orders']:
        cut=model.restrict(m,k);pp=calibrate(cut,inp)
        refit.append({'parameters':pp,'observables':evaluate(cut,pp,inp)})
        frozen.append(evaluate(cut,p,inp))
        _,be,_,_=model.diagonalize(cut,inp['v0_4_baseline']['x'],'bare')
        bare.append({'shell_order':k,'ground_energy_over_delta':float(be[0])})
    critical=math.sqrt(6)/4
    checks['bare_old_coupling_exceeds_analytic_stability_threshold']=inp['v0_4_baseline']['x']>critical
    checks['bare_variational_energies_fall_with_shell_extension']=all(bare[i+1]['ground_energy_over_delta']<bare[i]['ground_energy_over_delta'] for i in range(len(bare)-1))
    checks['bounded_frozen_variational_energies_do_not_increase']=all(frozen[i+1]['ground_energy_over_delta']<=frozen[i]['ground_energy_over_delta']+1e-10 for i in range(len(frozen)-1))
    checks['bounded_operator_satisfies_analytic_norm_ceiling']=np.max(abs(eigh(m['bounded'],eigvals_only=True)))<=m['bounded_norm_ceiling']+1e-10
    checks['bounded_ground_satisfies_uniform_lower_bound']=e[0]>=-p['x']*m['bounded_norm_ceiling']-1e-10
    checks['shared_axial_anchor_returned']=abs(r['gA']-abs(inp['axial_calibration']['signed_lambda']))<1e-10
    checks['shared_magnetic_anchors_returned']=max(abs(r['nucleons'][name]['moment_muN']-inp['magnetic_moments_muN'][name]) for name in M)<1e-10
    checks['proton_radius_anchor_returned']=abs(r['proton_radius_fm']-inp['radius_calibration']['proton_rms_charge_radius_fm'])<1e-10
    checks['excitation_centroid_gap_returned']=abs(r['gap_MeV']-(inp['excitation_calibration']['pole_centroid_MeV']-(inp['masses']['proton']+inp['masses']['neutron'])/2))<1e-9
    checks['frozen_parent_lifetime_returned']=abs(r['mean_life_s']-inp['inherited']['neutron_mean_life_s'])<1e-7
    checks['frozen_parent_reference_unchanged']=inp['parent_calibration_reference']==json.loads((ROOT/'frozen_parent_reference.json').read_text())
    checks['old_two_configuration_truncation_is_not_silently_closed']=r['higher_configuration_probability']>.01
    checks['neutron_radius_is_comparison_not_an_anchor']=abs(r['neutron_charge_mean_square_fm2']-(-.1155))>.0017
    rho=np.outer(g,g);U=expm(-.43j*(m['h0']-p['x']*m['bounded']))
    checks['density_positive_trace_one']=abs(np.trace(rho)-1)<1e-12 and eigh(rho,eigvals_only=True).min()>-1e-12
    psi=(V[:,0]+1j*V[:,1])/math.sqrt(2);rh=np.outer(psi,psi.conj());evolved=U@rh@U.conj().T
    checks['unitary_evolution_preserves_superposition_density']=abs(np.trace(evolved)-1)<1e-12 and np.linalg.norm(evolved-evolved.conj().T)<1e-12 and np.linalg.norm(evolved-rh)>.01
    derivative=[]
    for h in (.001,.01):
        for name,op in M.items():
            HH=p['delta_MeV']*(m['h0']-p['x']*m['bounded'])
            ep,vp=eigh(HH-h*op);em,vm=eigh(HH+h*op)
            first=-(ep[0]-em[0])/(2*h)
            second=(vp[:,0]@op@vp[:,0]-vm[:,0]@op@vm[:,0])/(2*h)
            checks[f'{name}_energy_derivative_{h}']=abs(first-r['nucleons'][name]['moment_muN'])<2e-7
            checks[f'{name}_spectral_susceptibility_derivative_{h}']=abs(second-r['nucleons'][name]['internal_susceptibility_MeV_minus1'])<2e-9
            derivative.append({'nucleon':name,'b_step_MeV':h,'minus_energy_derivative':float(first),'moment_derivative':float(second)})
    alt=model.build(K,s['alternate_quadrature_radial_order'],s['alternate_quadrature_angular_order'],s['screening_lambda'])
    ar=evaluate(alt,p,inp)
    checks.update({'alternate_'+k:v for k,v in alt['checks'].items()})
    checks['alternate_quadrature_same_ground_energy']=abs(ar['ground_energy_over_delta']-r['ground_energy_over_delta'])<2e-8
    checks['alternate_quadrature_same_radius']=abs(ar['proton_radius_fm']-r['proton_radius_fm'])<2e-8
    checks['alternate_quadrature_same_currents']=max(abs(ar['nucleons'][name]['moment_muN']-r['nucleons'][name]['moment_muN']) for name in M)<2e-8
    hold=model.build(K+2,s['alternate_quadrature_radial_order'],s['alternate_quadrature_angular_order'],s['screening_lambda'])
    hr=evaluate(hold,p,inp);checks.update({'holdout_'+k:v for k,v in hold['checks'].items()})
    checks['holdout_ground_energy_converges']=abs(hr['ground_energy_over_delta']-r['ground_energy_over_delta'])<2e-5
    checks['holdout_gap_converges_MeV']=abs(hr['gap_MeV']-r['gap_MeV'])<.03
    checks['holdout_axial_converges']=abs(hr['gA']-r['gA'])<1e-4
    checks['holdout_radius_converges_fm']=abs(hr['proton_radius_fm']-r['proton_radius_fm'])<1e-4
    checks['holdout_moments_converge_muN']=max(abs(hr['nucleons'][name]['moment_muN']-r['nucleons'][name]['moment_muN']) for name in M)<1e-4
    sensitivity=[]
    for lam in s['screening_sensitivity']:
        mm=m if lam==s['screening_lambda'] else model.build(K,s['quadrature_radial_order'],s['quadrature_angular_order'],lam)
        pp=calibrate(mm,inp);rr=evaluate(mm,pp,inp)
        checks.update({f'lambda_{lam}_'+k:v for k,v in mm['checks'].items()})
        checks[f'lambda_{lam}_joint_anchors_returned']=abs(rr['gA']-r['gA'])<1e-10 and max(abs(rr['nucleons'][name]['moment_muN']-inp['magnetic_moments_muN'][name]) for name in M)<1e-10
        sensitivity.append({'lambda':lam,'parameters':pp,'observables':rr})
    uncertain=[]
    mbar=(inp['masses']['proton']+inp['masses']['neutron'])/2
    for pole in inp['excitation_calibration']['pole_centroid_range_MeV']:
        uncertain.append({'input':'pole_centroid','value_MeV':pole,'delta_MeV':float((pole-mbar)/(e[1]-e[0]))})
    rp=inp['radius_calibration']['proton_rms_charge_radius_fm'];sig=inp['radius_calibration']['standard_uncertainty_fm']
    for rad in (rp-sig,rp+sig):uncertain.append({'input':'proton_radius','value_fm':rad,'ell_fm':p['ell_fm']*rad/rp})
    uncertain.append({'input':'Breit_Wigner_definition_control','value_MeV':1440.,'delta_MeV':float((1440-mbar)/(e[1]-e[0]))})
    for name in ('proton','neutron'):
        checks[name+'_susceptibility_positive']=r['nucleons'][name]['internal_susceptibility_MeV_minus1']>0
        checks[name+'_higher_excited_states_contribute']=r['nucleons'][name]['first_state_susceptibility_fraction']<.99
    activity_controls=[]
    for label,alpha,N in [('N=100',inp['inherited']['alpha'],100),('alpha+0.05',inp['inherited']['alpha']+.05,inp['inherited']['N'])]:
        pp=dict(p);pp['R']=math.prod(model.v4.old.euler_activity(j,alpha,N) for j in (3,5));pp['x']=p['C']*math.sqrt(pp['R'])
        rr=evaluate(m,pp,inp);activity_controls.append({'case':label,'activity':pp['R'],'x':pp['x'],'observables':rr})
        checks[label+'_changes_shared_state_with_frozen_C']=abs(rr['gA']-r['gA'])>1e-4 and abs(rr['mean_life_s']-r['mean_life_s'])>1e-2
    output={'version':'0.5','scope':'Conditional bounded effective spatial completion; fitted scales and current anchors, no QCD derivation or resonance width prediction.',
       'calibrated_parameters':p,'reference':r,'bare_instability':{'critical_x':critical,'old_x':inp['v0_4_baseline']['x'],'shell_sequence':bare},
       'bounded_norm_ceiling':m['bounded_norm_ceiling'],'screening_normalization_k':m['normalization_k'],
       'frozen_parameter_convergence':frozen,'refitted_shell_convergence':refit,'alternate_quadrature':ar,
       'unfitted_shell_holdout':hr,'screening_sensitivity':sensitivity,'conditional_input_ranges':uncertain,
       'field_derivatives':derivative,'frozen_activity_controls':activity_controls,'neutron_radius_comparison':{'observed_fm2':-.1155,'standard_uncertainty_fm2':.0017,'role':'unfitted diagnostic; mismatch requires charge-operator improvement'},
       'checks':{k:bool(v) for k,v in checks.items()},'checks_total':len(checks),'checks_passed':sum(bool(v) for v in checks.values())}
    if not all(checks.values()):raise AssertionError({k:v for k,v in checks.items() if not v})
    return rounded(output)

def main():
    inp=json.loads((ROOT/'inputs.json').read_text());out=run(inp)
    (ROOT/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'parameters':out['calibrated_parameters'],'reference':out['reference'],'holdout':out['unfitted_shell_holdout'],'checks':out['checks_total']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
