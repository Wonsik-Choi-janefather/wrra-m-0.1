"""Conserving CDM-comoving adapter for frozen v0.4 same-content states.

Transforms the whole scalar state, including neutrino monopole/dipole.
It does not invent absent baryons, e+- perturbations or massive-nu f(q).
It never substitutes this smooth-source state for the finite-packet tangent.
"""
from pathlib import Path
import json,math
import numpy as np
P=Path(__file__).resolve().parent

def transform(state,K,a,H,Hdot,alpha=None):
    """Conformal coordinates in original dimensionless normalization.

    theta_new=theta_old-k^2 alpha; delta_new=delta_old+3(1+w)Hc alpha;
    eta_new=eta_old+Hc alpha. Residual synchronous alpha'=-Hc alpha.
    These equations fix the sign convention by invariant zeta and both constraints.
    """
    s=dict(state);s['F_nu']=list(state['F_nu']);calH=a*H
    alpha=state['theta_m']/K**2 if alpha is None else alpha
    s['eta']+=calH*alpha
    for f,w in [('delta_gamma',1/3),('delta_nu',1/3),('delta_m',0.)]:
        s[f]+=3*(1+w)*calH*alpha
    for f in ['theta_gamma','theta_nu','theta_m']:s[f]-=K*K*alpha
    s['F_nu'][0]=s['delta_nu'];s['F_nu'][1]=4*s['theta_nu']/(3*K)
    # h itself needs a spatial-gauge integration constant. CAMB does not evolve h.
    s.pop('h',None);s.pop('shear_scaled',None)
    for f in list(s):
        if f.endswith('_Mpc_inverse'):s.pop(f)
    s['gauge_alpha']=alpha
    return s

def main():
    inputs=json.loads((P/'inputs/v04_audit.json').read_text())
    states=json.loads((P/'inputs/matching_states.json').read_text())
    arrays=np.load(P/'inputs/all_64_transition_responses.npz')['state']
    beta=inputs['inputs']['beta'];fnu=inputs['inputs']['fnu'];kscale=inputs['inputs']['K_per_Mpc_inverse']
    G=(1-beta)*(1-fnu)+beta/2;V=(1-beta)*fnu
    rows=[]
    for entry,y,d in zip(states,arrays,inputs['physical_modes']):
        s=entry['matched_state'];K=entry['K_initial'];k=entry['k_Mpc_inverse']
        a=s['a_relative'];M=y[2];H=y[3];rho=(G+V)/a**4+M/a**3
        Hdot=-.5*(4*(G+V)/a**4+3*M/a**3);calH=a*H
        out=transform(s,K,a,H,Hdot);alpha=out['gauge_alpha']
        etap=a*d['eta_dot']+a*a*Hdot*alpha
        hp=a*d['hdot']+2*K*K*alpha-6*a*a*Hdot*alpha
        dr=(G*out['delta_gamma']+V*out['delta_nu'])/a**4+M*out['delta_m']/a**3
        ham=K*K*out['eta']-.5*calH*hp+1.5*a*a*dr
        dq=4/3*(G*out['theta_gamma']+V*out['theta_nu'])/a**4+M*out['theta_m']/a**3
        mom=etap-1.5*a*a*dq/K**2
        scale=max(abs(K*K*out['eta']),abs(.5*calH*hp),abs(1.5*a*a*dr),1e-100)
        mscale=max(abs(etap),abs(1.5*a*a*dq/K**2),1e-100)
        Sm=s['delta_m']-.75*(G*s['delta_gamma']+V*s['delta_nu'])/(G+V)
        Snew=out['delta_m']-.75*(G*out['delta_gamma']+V*out['delta_nu'])/(G+V)
        # Inverse at the same background tests every retained density/momentum/moment.
        inv=transform(out,K,a,H,Hdot,alpha=-alpha)
        fields=['eta','delta_m','delta_gamma','delta_nu','theta_m','theta_gamma','theta_nu']
        invscale=max(max(abs(s[f]) for f in fields),1e-100)
        inv_error=max(abs(inv[f]-s[f]) for f in fields)/invscale
        # Deleting recipient velocity without gauge transformation violates momentum constraint.
        theta_deleted_dq=4/3*(G*s['theta_gamma']+V*s['theta_nu'])/a**4
        bad=a*d['eta_dot']-1.5*a*a*theta_deleted_dq/K**2
        badscale=max(abs(a*d['eta_dot']),abs(1.5*a*a*theta_deleted_dq/K**2),1e-100)
        # Native CAMB variable convention, checked against equations.f90 2.0.4.
        # Keep the small derivative combination directly: reconstructing it by
        # h_prime + 6*eta_prime loses precision for the lowest k after this
        # large residual gauge shift. A downstream transport must use this
        # stable combination (and test its constraints), not subtract rounded terms.
        metric_alpha=0.5*s['shear_scaled']+alpha
        out.update(eta_prime=etap,h_prime=hp,
            h_plus_6eta_prime=2*K*K*metric_alpha,
            metric_alpha=metric_alpha,
            native_shear_sigma=K*metric_alpha,
            Bardeen_Phi=s['eta']-calH*0.5*s['shear_scaled'],
            derivative_combination_note='Use h_plus_6eta_prime directly; h_prime and eta_prime separately are rounded diagnostics.',
            physical_k_Mpc_inverse=k,physical_a=1e-10*a,
            native_CAMB_partial=dict(etak=k*out['eta'],clxc=out['delta_m'],
                photon_clx=out['delta_gamma'],photon_q=4*out['theta_gamma']/(3*K),
                neutrino_hierarchy=out['F_nu']),
            missing=['baryon density and tight-coupled velocity','finite-mass neutrino momentum distribution',
                     'finite-packet finite-gradient source evolution','electron/positron perturbation history'],
            thermal_mapping_applied=False,full_state_injected=False)
        rows.append(dict(mode=entry['mode'],adapted=out,
            audit=dict(Hamiltonian_normalized=abs(ham)/scale,momentum_normalized=abs(mom)/mscale,
                entropy_invariance_absolute=abs(Snew-Sm),inverse_normalized=inv_error,
                unchanged_high_neutrino_moments=np.array_equal(out['F_nu'][2:],s['F_nu'][2:]),
                deletion_negative_control=abs(bad)/badscale)))
    (P/'results/cdm_comoving_64_states.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps({key:max(x['audit'][key] for x in rows) for key in rows[0]['audit'] if not isinstance(rows[0]['audit'][key],bool)},indent=2))
if __name__=='__main__':main()
