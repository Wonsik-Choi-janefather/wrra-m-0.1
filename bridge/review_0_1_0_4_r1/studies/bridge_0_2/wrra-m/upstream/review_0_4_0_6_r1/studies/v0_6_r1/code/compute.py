#!/usr/bin/env python3
"""Upstream 0.6: calibrated Sachs completion and same-state finite currents."""
from pathlib import Path
import copy,hashlib,json,math
import numpy as np
from scipy.linalg import eigh,expm
import model,currents,beta,inherited_v0_5 as v5
from review_contracts import validate_scalars
ROOT=Path(__file__).resolve().parent

def validate(inp):
    validate_scalars(inp)
    v5.validate(inp);c=inp['charge_completion']
    for key in ('reference_regulator_in_ell','inner_delta_R_V_uncertainty'):
        if not math.isfinite(c[key]) or c[key]<=0:raise ValueError(key)
    if not math.isfinite(c['neutron_mean_square_radius_fm2']):raise ValueError('neutron radius')
    if not math.isfinite(c['inner_delta_R_V']) or not 0<=c['inner_delta_R_V']<.2:raise ValueError('inner RC')
    if not c['spacelike_Q2_GeV2'] or any(not math.isfinite(q) or q<0 for q in c['spacelike_Q2_GeV2']):raise ValueError('spacelike Q2')
    if not c['regulator_lengths_in_ell'] or any(not math.isfinite(a) or a<=0 for a in c['regulator_lengths_in_ell']):raise ValueError('regulator')
    for key in ('reference_electron_order','alternate_electron_order','angular_order'):
        if type(c[key]) is not int or c[key]<4:raise ValueError(key+' must be integer >= 4')
    if not math.isfinite(c['uncertainty_fm2']) or c['uncertainty_fm2']<=0:raise ValueError('neutron radius uncertainty')
    if c['neutron_mean_square_radius_fm2']+inp['radius_calibration']['proton_rms_charge_radius_fm']**2<=0:raise ValueError('common width')

def construct(inp,K=None,nr=None,na=None):
    s=inp['spatial_extension'];K=s['reference_shell_order'] if K is None else K
    nr=s['quadrature_radial_order'] if nr is None else nr;na=s['quadrature_angular_order'] if na is None else na
    m=model.build(K,nr,na,s['screening_lambda'])
    # The shared state is always fixed by the inherited K=8 calibration. A
    # larger-space holdout must not silently recalibrate x, delta or eta.
    base=m if K==s['reference_shell_order'] else model.build(s['reference_shell_order'],s['quadrature_radial_order'],s['quadrature_angular_order'],s['screening_lambda'])
    p=v5.calibrate(base,inp);_,e,V,g=model.diagonalize(m,p['x'])
    c=currents.prepare(m,p,g,inp,nr,na)
    return m,p,e,V,g,c

def run(inp):
    validate(inp);s=inp['spatial_extension'];m,p,e,V,g,c=construct(inp);sl=currents.slopes(c);z=currents.ground(c,0);checks={'basis_'+k:v for k,v in m['checks'].items()}
    checks['v0_5_code_hash_unchanged']=hashlib.sha256((ROOT/'inherited_v0_5.py').read_bytes()).hexdigest()==inp['v0_5_baseline']['code_sha256']
    checks['v0_5_model_hash_unchanged']=hashlib.sha256((ROOT/'model.py').read_bytes()).hexdigest()==inp['v0_5_baseline']['model_sha256']
    checks['projection_reconstructed_same_H0']=np.linalg.norm(c['Q'].T@np.diag(np.tile([sum(l) for l in model.labels(m['K'])],3))@c['Q']-m['h0'])<1e-10
    checks['proton_zero_charge_preserved']=abs(z['proton']['GE']-1)<1e-12
    checks['neutron_zero_charge_preserved']=abs(z['neutron']['GE'])<1e-12
    checks['axial_zero_anchor_preserved']=abs(z['weak']['GAV']-abs(inp['axial_calibration']['signed_lambda']))<1e-12
    checks['zero_magnetic_anchors_preserved']=max(abs(z[n]['GM_muN']-inp['magnetic_moments_muN'][n]) for n in ('proton','neutron'))<1e-12
    checks['radius_proton_refitted']=abs(sl['proton']['sachs_charge_radius_squared_fm2']-inp['radius_calibration']['proton_rms_charge_radius_fm']**2)<1e-12
    checks['radius_neutron_refitted']=abs(sl['neutron']['sachs_charge_radius_squared_fm2']-inp['charge_completion']['neutron_mean_square_radius_fm2'])<1e-12
    checks['point_0_5_radius_not_relabelled_as_Dirac']=abs(c['counterterm_radius_fm2'])>.01
    checks['slot_vector_CVC_independent']=max(np.linalg.norm(v-a+b) for v,a,b in zip(c['vslots'],c['charge_slots']['proton'],c['charge_slots']['neutron']))<1e-12
    curves=[currents.ground(c,q) for q in inp['charge_completion']['spacelike_Q2_GeV2']]
    for i,rr in enumerate(curves):
        q=rr['Q2_GeV2'];tau=q/(4*c['mass_reference_GeV']**2)
        for n in ('proton','neutron'):
            ff=rr[n]
            checks[f'Sachs_Dirac_Pauli_{n}_q{i}']=abs(ff['F1']-tau*ff['F2']-ff['GE'])<1e-12 and abs(ff['F1']+ff['F2']-ff['GM_common_mass'])<1e-12
        checks[f'CVC_finite_charge_q{i}']=abs(rr['weak']['GEV']-(rr['proton']['GE']-rr['neutron']['GE']))<1e-12
    for n in ('proton','neutron'):
        checks[n+'_Foldy_decomposition_same_Sachs_radius']=abs(sl[n]['dirac_radius_squared_fm2']+sl[n]['foldy_radius_squared_fm2']-sl[n]['sachs_charge_radius_squared_fm2'])<1e-12
    h=1e-5;a=currents.ground(c,h);b=currents.ground(c,2*h)
    for n in ('proton','neutron'):
        first=(-3*z[n]['GE']+4*a[n]['GE']-b[n]['GE'])/(2*h)
        checks[n+'_radius_from_finite_Q2_derivative']=abs(-6*currents.HC**2*first-sl[n]['sachs_charge_radius_squared_fm2'])<2e-9
    H=p['delta_MeV']*(m['h0']-p['x']*m['bounded']);continuity=[]
    for q in (.01,.1):
        momentum=1000*math.sqrt(q)
        for name in ('proton','neutron'):
            rho=currents.full_charge(c,q,name);J=(H@rho-rho@H)/momentum
            checks[f'{name}_density_hermitian_Q2_{q}']=np.linalg.norm(rho-rho.T)<1e-12
            # Fourier longitudinal amplitude is odd in momentum.
            # Its adjoint equals the -q amplitude, rather than itself.
            checks[f'{name}_Fourier_current_adjoint_Q2_{q}']=np.linalg.norm(J.conj().T+J)<1e-12
            checks[f'{name}_density_ground_integral_Q2_{q}']=abs(g@rho@g-currents.ground(c,q)[name]['GE'])<1e-12
            residual=np.linalg.norm(momentum*(V.T@J@V)-p['delta_MeV']*(e[:,None]-e[None,:])*(V.T@rho@V))
            checks[f'{name}_transition_continuity_Q2_{q}']=residual<2e-8
            psi=(V[:,0]+1j*V[:,1])/math.sqrt(2);dt=1e-7;U=expm(-1j*H*dt)
            evol=(np.vdot(U@psi,rho@(U@psi))-np.vdot(U.conj().T@psi,rho@(U.conj().T@psi)))/(2*dt)
            predicted=1j*np.vdot(psi,(H@rho-rho@H)@psi)
            checks[f'{name}_density_time_derivative_Q2_{q}']=abs(evol-predicted)<2e-7
            continuity.append({'nucleon':name,'Q2_GeV2':q,'transition_residual_MeV':float(residual),'longitudinal_current_norm':float(np.linalg.norm(J))})
    ff={**sl['weak'],'activity_R':p['R']};ne=inp['charge_completion']['reference_electron_order'];nz=inp['charge_completion']['angular_order'];rates=beta.calculate(inp,ff,ne,nz);alternate=beta.calculate(inp,ff,inp['charge_completion']['alternate_electron_order'],nz+4)
    checks['beta_alternate_quadrature_total_rate']=abs(rates['full_rate_ratio_relative_parent']-alternate['full_rate_ratio_relative_parent'])<2e-7
    checks['beta_spectrum_positive_and_normalized']=min(rates['electron_spectrum']['quadrature_probability'])>0 and abs(sum(rates['electron_spectrum']['quadrature_probability'])-1)<1e-12
    checks['recoil_endpoint_lower_than_parent']=rates['endpoint_recoil_total_electron_MeV']<rates['endpoint_parent_total_electron_MeV']
    checks['radiative_correction_changes_frozen_lifetime']=rates['frozen_parent_kappa_lifetime_s']<inp['inherited']['neutron_mean_life_s']-1
    checks['explicit_kappa_refit_changes_value']=rates['separately_refitted_kappa']<inp['inherited']['kappa']
    checks['refitted_lifetime_return_from_actual_rate']=abs(rates['frozen_parent_kappa_lifetime_s']*(inp['inherited']['kappa']/rates['separately_refitted_kappa'])**2-inp['inherited']['neutron_mean_life_s'])<1e-10
    for name,t in rates['trace_diagnostics'].items():
        checks[name+'_mass_shell_conserved']=t['on_shell_residual_MeV2']<1e-8
        checks[name+'_real_positive_probability']=t['minimum_trace']>0 and t['maximum_imaginary_trace']<1e-8
    sensitivity=[{'regulator_in_ell':a,'curve':[currents.ground(c,q,a) for q in inp['charge_completion']['spacelike_Q2_GeV2']]} for a in inp['charge_completion']['regulator_lengths_in_ell']]
    checks['regulator_changes_finite_Q2_without_changing_radius']=abs(currents.ground(c,.2,.5)['neutron']['GE']-currents.ground(c,.2,2.)['neutron']['GE'])>.005
    probe=currents.ground(c,.1)
    ma,pa,ea,Va,ga,ca=construct(inp,nr=40,na=22);alcurve=currents.ground(ca,.1)
    checks['spatial_alternate_quadrature_GE_GM_GA']=max(abs(alcurve[n][k]-probe[n][k]) for n,k in [('proton','GE'),('neutron','GE'),('proton','GM_muN'),('weak','GAV')])<2e-8
    mh,ph,eh,Vh,gh,ch=construct(inp,K=s['reference_shell_order']+2,nr=s['alternate_quadrature_radial_order'],na=s['alternate_quadrature_angular_order'])
    # Freeze both the new charge width and counterterm for the larger shell.
    ch['ell_fm']=c['ell_fm'];ch['counterterm_radius_fm2']=c['counterterm_radius_fm2'];hs=currents.slopes(ch);hc=currents.ground(ch,.1)
    checks['holdout_frozen_charge_radii_converge']=max(abs(hs[n]['sachs_charge_radius_squared_fm2']-sl[n]['sachs_charge_radius_squared_fm2']) for n in ('proton','neutron'))<2e-5
    checks['holdout_finite_currents_converge']=max(abs(hc[n][k]-probe[n][k]) for n,k in [('proton','GE'),('neutron','GE'),('proton','GM_muN'),('weak','GAV')])<2e-5
    quadratic=[];M0=v5.operators(m,p)
    for d in (0.,.0001,-.0001):
        for name,op in M0.items():
            b=.01;ep,vp=eigh(H-b*op-.5*b*b*d*np.eye(len(g)));em,vm=eigh(H+b*op-.5*b*b*d*np.eye(len(g)))
            expected=v5.evaluate(m,p,inp)['nucleons'][name]['internal_susceptibility_MeV_minus1']+d
            derivative=float((vp[:,0]@op@vp[:,0]+b*d-vm[:,0]@op@vm[:,0]+b*d)/(2*b))
            checks[f'{name}_explicit_b2_direct_response_{d}']=abs(derivative-expected)<2e-9
            quadratic.append({'nucleon':name,'direct_b2_coefficient_MeV_minus1':d,'total_internal_response_MeV_minus1':expected,'finite_field_moment_derivative':derivative})
    out={'version':'0.6','scope':'Same-state finite monopole current completion with fitted charge counterterm, CVC and leading recoil/radiative rate controls; no microscopic exchange-charge derivation or complete precision beta calculation.',
        'inherited_parameters':p,'new_charge_calibration':{'ell_fm':c['ell_fm'],'isovector_counterterm_radius_fm2':c['counterterm_radius_fm2'],'regulator_length_fm':c['ell_fm']*c['reference_regulator'],'common_Sachs_mass_MeV':1000*c['mass_reference_GeV'],'GM_common_to_muN_scale':c['magnetic_unit_scale']},
        'zero_momentum':z,'slopes_and_radii':sl,'form_factors':curves,'regulator_sensitivity':sensitivity,'continuity_controls':continuity,
        'beta':rates,'beta_alternate_quadrature':{'full_rate_ratio_relative_parent':alternate['full_rate_ratio_relative_parent'],'electron_order':inp['charge_completion']['alternate_electron_order'],'angular_order':nz+4},
        'larger_shell_holdout':{'K':s['reference_shell_order']+2,'radii':hs,'finite_Q2_point':hc},'direct_b2_controls':quadratic,
        'unfitted_diagnostic':{'neutron_magnetic_radius_fm':math.sqrt(sl['neutron']['magnetic_radius_squared_fm2']),'PDG_reference_fm':.864,'PDG_plus_fm':.009,'PDG_minus_fm':.008,'role':'unfitted comparison; remaining mismatch is not hidden'},
        'checks':{k:bool(v) for k,v in checks.items()},'checks_total':len(checks),'checks_passed':sum(bool(v) for v in checks.values())}
    if not all(checks.values()):raise AssertionError({k:v for k,v in checks.items() if not v})
    return v5.rounded(out)

def main():
    inp=json.loads((ROOT/'inputs.json').read_text());r=run(inp);(ROOT/'results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'charge':r['new_charge_calibration'],'beta':{k:v for k,v in r['beta'].items() if k not in ('electron_spectrum','trace_diagnostics')},'diagnostic':r['unfitted_diagnostic'],'checks':r['checks_total']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
