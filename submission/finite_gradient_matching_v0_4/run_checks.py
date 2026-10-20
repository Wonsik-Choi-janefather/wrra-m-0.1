from pathlib import Path
import json,math,hashlib,time
import numpy as np
from finite_gradient import Model,evolve,diagnostics,sample_audit,full_state
import independent_metric

P=Path(__file__).resolve().parent;OUT=P/'results';OUT.mkdir(exist_ok=True)
checks={}
def check(name,value):
    checks[name]=bool(value)
    if not value:raise AssertionError(name)

def summary(r,side='before'):
    return diagnostics(r['tmatch'],r[side],r['model'],r['Gbefore' if side=='before' else 'Gafter'],r['V'])

def aggregate(r,side='before'):
    y=r[side];G=r['Gbefore' if side=='before' else 'Gafter'];V=r['V']
    q=summary(r,side)
    return np.array([y[0],y[1]+G+V,y[2],y[3],y[4],y[5],y[6],y[7],
        y[8]+y[9]+y[10],y[11],sum(y[12:16]),y[16],q['hdot'],q['eta_dot']])

def main():
    start=time.time();dy=json.loads((P/'inputs/dynamics_results.json').read_text())
    beta=dy['calibrated_convertible_radiation_fraction']
    fnu=.22710731766023898*3.044/(1+.22710731766023898*3.044)
    Kscale=299792458.*dy['time_unit_seconds']/(3.085677581491367e22*1e-10)
    ks=.05*np.arange(1,65);Ks=ks*Kscale
    r0=evolve(Model(beta,fnu,0.));z0=summary(r0)
    check('k0_entropy_recovers_v03',abs(z0['S_mr']/dy['entropy_response_to_rate_modulation']-1)<1e-10)
    check('k0_radiation_curvature_recovers_v03',abs(z0['zeta_r']/dy['radiation_curvature_response']-1)<1e-10)
    base=evolve(Model(beta,0.,0.));qbase=summary(base)
    check('radiation_split_does_not_change_zero_gradient_limit',abs(qbase['S_mr']-z0['S_mr'])<2e-12)
    rows=[];states=[];conservation=[];responses=[]
    for n,(k,K) in enumerate(zip(ks,Ks),1):
        m=Model(beta,fnu,float(K));r=evolve(m,merge=True);q=summary(r);audit,_=sample_audit(r)
        conservation.append(audit)
        for label in ['Hamiltonian_residual','trace_residual','energy_residual','momentum_residual']:
            check(f'mode_{n:02d}_{label}',audit[label]['normalized']<2e-8)
        check(f'mode_{n:02d}_friedmann',audit['background_friedmann']<1e-8)
        check(f'mode_{n:02d}_pressure_work',audit['background_energy_work']<1e-10)
        check(f'mode_{n:02d}_finite_state',np.isfinite(r['before']).all())
        qb=summary(r);qa=summary(r,'after')
        match_scale=max(abs(qb['delta_rho']),abs(qb['momentum_scaled']),abs(qb['hdot']),1e-100)
        match_jump=max(abs(qa[s]-qb[s]) for s in ['delta_rho','momentum_scaled','delta_pressure','hdot','eta_dot'])/match_scale
        check(f'mode_{n:02d}_boundary_stress_and_metric',match_jump<1e-12)
        check(f'mode_{n:02d}_boundary_neutrino_hierarchy',np.array_equal(r['before'][16:],r['after'][16:]))
        q.update(mode=n,k_Mpc_inverse=float(k),K_initial=float(K),
            entropy_relative_to_v03=q['S_mr']/dy['entropy_response_to_rate_modulation']-1,
            curvature_relative_to_v03=q['zeta_r']/dy['radiation_curvature_response']-1)
        rows.append(q);responses.append(r['before'])
        state=full_state(r);matched=full_state(r,'after')
        for st in [state,matched]:
            for field in ['theta_C','theta_gamma','theta_nu','theta_m']:
                st[field+'_Mpc_inverse']=st[field]/Kscale
        states.append({'mode':n,'k_Mpc_inverse':float(k),'K_initial':float(K),'state':state,
                       'matched_state':matched,'S_nugamma_after_merge':qa['S_nugamma']})
        if n%16==0:print('physical modes complete',n,flush=True)
    # Finite-k response is not replaced by a quadratic ansatz: all 64 evolved.
    err=np.array([x['S_mr']-z0['S_mr'] for x in rows]);coef=err/(Ks*Ks)
    check('finite_gradient_entropy_is_nonzero',np.max(abs(err))>1e-11)
    check('small_k_entropy_correction_is_quadratic',np.max(abs(coef[8:]/np.median(coef[8:])-1))<.003)
    check('original_maximum_k_over_aH_recovered',abs(rows[-1]['k_over_aH']/dy['kmax_over_aH']-1)<1e-8)
    # Actual free-streaming moments, not a two-moment perfect-fluid substitute.
    check('nonzero_neutrino_quadrupole',abs(rows[-1]['sigma_nu'])>1e-18)
    check('nonzero_neutrino_octupole',abs(states[-1]['state']['F_nu'][3])>1e-20)
    # Apply the full finite-k responses to the original 128-cell SOURCE seed.
    seed=np.load(P/'inputs/quantized_seed.npz')['entropy'];seed=seed-seed.mean()
    hs=np.fft.rfft(seed);fields={}
    transforms={name:np.array([s['matched_state'][name] for s in states])
                for name in ['h','eta','delta_gamma','delta_nu','delta_m','theta_gamma_Mpc_inverse',
                             'theta_nu_Mpc_inverse','theta_m_Mpc_inverse']}
    transforms['S_mr']=np.array([q['S_mr'] for q in rows])
    transforms['sigma_nu']=np.array([q['sigma_nu'] for q in rows])
    for name,transfer in transforms.items():
        spec=np.r_[0j,hs[1:]*transfer]
        fields[name]=np.fft.irfft(spec,n=128)
        check('actual_seed_'+name+'_finite',np.isfinite(fields[name]).all())
        check('actual_seed_'+name+'_zero_mean',abs(fields[name].mean())<max(np.max(abs(fields[name]))*1e-12,1e-100))
    old=dy['entropy_response_to_rate_modulation']*seed
    seed_effect=float(np.linalg.norm(fields['S_mr']-old)/np.linalg.norm(old))
    check('actual_seed_entropy_positive_density',np.min(1+fields['delta_m'])>0)
    np.savez_compressed(OUT/'actual_128_cell_matched_fields.npz',seed=seed,**fields)
    # Matching at 10: merge remaining tagged perfect radiation into photons.
    # All its density and momentum are transported; neutrino hierarchy untouched.
    matching=[];stress=[];negative=[];independent=[]
    for j,K in enumerate([float(Ks[0]),float(Ks[31]),float(Ks[-1]),.03,.1,.3,1.]):
        m=Model(beta,fnu,K,lmax=16);raw=evolve(m);merged=evolve(m,merge=True)
        ab=aggregate(merged,'before');aa=aggregate(merged,'after');scale=max(abs(ab).max(),1.)
        boundary=float(np.max(abs(ab-aa))/scale)
        # Stress/geometry matching judged against their own response scales.
        qb=summary(merged);qa=summary(merged,'after')
        ownscale=max(abs(qb['delta_rho']),abs(qb['momentum_scaled']),abs(qb['hdot']),abs(qb['eta']),1e-100)
        response_jump=max(abs(qa[k]-qb[k]) for k in ['delta_rho','momentum_scaled','delta_pressure','hdot','eta_dot'])/ownscale
        check(f'match_{j}_energy_momentum_metric',response_jump<1e-12 and boundary<1e-14)
        check(f'match_{j}_neutrino_hierarchy_exact',np.array_equal(merged['before'][16:],merged['after'][16:]))
        y1=raw['segments'][-1][0].y[:,-1];y2=merged['segments'][-1][0].y[:,-1]
        # Compare aggregate states after 20 additional proper-time units.
        def endvec(y,G):return np.r_[y[:1],y[1]+G+raw['V'],y[2:8],y[8]+y[9]+y[10],y[11],sum(y[12:16]),y[16:]]
        v1=endvec(y1,raw['Gafter']);v2=endvec(y2,merged['Gafter'])
        response_ix=np.r_[np.arange(5,11),np.arange(11,len(v1))]
        response_scale=max(np.max(abs(v1[response_ix])),1e-100)
        continuation=float(np.max(abs((v1-v2)[response_ix]))/response_scale)
        check(f'match_{j}_post_boundary_continuation',continuation<1e-7)
        matching.append(dict(K=K,stress_response_normalized_boundary_jump=response_jump,
                             post_boundary_relative_difference=continuation))
        # Independent trace equation, no scaled-shear evolution or resets.
        alt=independent_metric.evolve(m);expected=y1.copy()
        qq=diagnostics(30,y1,m,raw['Gafter'],raw['V'])
        expected[7]=qq['hdot'];expected[16]*=K*K
        for ell in range(3,m.lmax+1):expected[17+ell-3]*=K**ell
        inds=np.r_[np.arange(5,17),np.arange(17,len(expected))]
        rel=float(np.max(abs(alt[inds]-expected[inds]))/max(np.max(abs(expected[inds])),1e-100))
        check(f'independent_trace_solver_{j}',rel<2e-7)
        independent.append(dict(K=K,normalized_state_difference=rel))
        # Hierarchy truncation and integration convergence in stress cases.
        hi=evolve(Model(beta,fnu,K,lmax=24),rtol=2e-12,atol=2e-23,max_step=.02)
        q=summary(raw);qh=summary(hi)
        metric_rel=max(abs(q[x]-qh[x]) for x in ['zeta_r','eta','sigma_nu'])/max(abs(q['zeta_r']),abs(q['eta']),1e-100)
        check(f'hierarchy_and_step_convergence_{j}',metric_rel<2e-8)
        fluid=evolve(Model(beta,fnu,K,lmax=16,no_shear=True));qf=summary(fluid)
        stress.append(dict(K=K,k_over_aH=q['k_over_aH'],S=q['S_mr'],zeta_r=q['zeta_r'],eta=q['eta'],
             sigma_nu=q['sigma_nu'],hierarchy_and_step_error=metric_rel,
             perfect_fluid_eta_difference=qf['eta']-q['eta']))
    # Counterexamples make omitted momentum/matching visible in constraints.
    bad=evolve(Model(beta,fnu,1.,lmax=16,wrong_momentum=True));bad_audit,_=sample_audit(bad)
    check('reject_missing_recipient_momentum',bad_audit['Hamiltonian_residual']['normalized']>1e-4)
    negative.append({'case':'remove recipient momentum source','audit':bad_audit})
    m=Model(beta,fnu,1.,lmax=16);good=evolve(m,merge=True)
    broken=good['after'].copy();broken[9]-=good['before'][8]
    b=diagnostics(10,broken,m,good['Gafter'],good['V']);q=summary(good,'after')
    jump=abs(b['delta_rho']-q['delta_rho'])/max(abs(q['delta_rho']),1e-100)
    check('reject_lost_reservoir_density_at_matching',jump>1e-3)
    negative.append({'case':'drop reservoir perturbation at matching','relative_density_jump':jump})
    broken=good['after'].copy();broken[13]-=good['before'][12]
    b=diagnostics(10,broken,m,good['Gafter'],good['V'])
    jump=abs(b['momentum_scaled']-q['momentum_scaled'])/max(abs(q['momentum_scaled']),1e-100)
    check('reject_lost_reservoir_momentum_at_matching',jump>1e-3)
    negative.append({'case':'drop reservoir momentum at matching','relative_momentum_jump':jump})
    out={'version':'0.4','inputs':{'beta':beta,'fnu':fnu,'K_per_Mpc_inverse':Kscale,
       'rate_modulation_amplitude_for_linear_response':1.,'physical_modes':64,'lmax':12,
       'proper_pulse':[0,1],'matching_time':10.,'continuation_time':30.},
       'zero_gradient':z0,'physical_modes':rows,'matching':matching,'independent_solver':independent,
       'actual_seed':{'entropy_RMS':float(np.sqrt(np.mean(fields['S_mr']**2))),
                     'entropy_L2_change_relative_to_v03':seed_effect,
                     'max_abs_matter_contrast':float(np.max(abs(fields['delta_m']))),
                     'max_abs_neutrino_shear':float(np.max(abs(fields['sigma_nu'])))},
       'stress_cases':stress,'negative_controls':negative,
       'max_physical_constraint_residuals':{s:max(x[s]['normalized'] for x in conservation) for s in ['Hamiltonian_residual','trace_residual','energy_residual','momentum_residual']},
       'checks_passed':sum(checks.values()),'checks':checks,'elapsed_seconds':time.time()-start,
       'scope':'Finite spatial gradients at linear perturbation amplitude; covariant effective reservoir-to-dust exchange, synchronous metric, perfect photon-like radiation and massless collisionless neutrinos. Matching to an explicitly continued same-content Einstein--Boltzmann system executed. Full post-transition CAMB state injection, real baryon production, neutrino decoupling/thermal history and nonlinear evolution not executed.'}
    (OUT/'audit.json').write_text(json.dumps(out,indent=2)+'\n')
    (OUT/'matching_states.json').write_text(json.dumps(states,indent=2)+'\n')
    np.savez_compressed(OUT/'all_64_transition_responses.npz',k_Mpc_inverse=ks,K_initial=Ks,state=np.array(responses))
    print(json.dumps({k:v for k,v in out.items() if k not in ['checks','physical_modes','negative_controls']},indent=2))
if __name__=='__main__':main()
