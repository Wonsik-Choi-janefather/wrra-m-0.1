"""One physical 3D Fourier mode of a declared WRRA dark-sector completion.

Arithmetic coefficients are inherited; k, spatial occupation modulation and
initial velocities are explicit diagnostic inputs, not arithmetic predictions.
GR Newtonian-gauge equations are adopted and checked independently via the
propagation identity of the Einstein energy constraint.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
ETA=np.array([7.5615824991e-10,7.2857613288e-10,7.6461028188e-10])
G=6.67430e-11;C_LIGHT=299792458.;MPC=3.085677581e22
K=.05;EPS=1e-8;AI=.02
DELTA_A=2*np.cos(2*np.pi*8/128)

def integrate(u0,response,epsilon=EPS,include_force=True,rtol=2e-11):
    # Controlled baryon-dust + dark-dust + vacuum system. Radiation and
    # neutrinos are omitted ONLY here, not in the recorded CAMB CMB calculation.
    ucrit100=3*(100000/MPC)**2*C_LIGHT**2/(8*np.pi*G)
    H0=100*np.sqrt(u0.sum()/ucrit100);h0=H0/(C_LIGHT/1000)
    omega=u0/u0.sum()
    duD0=response[1]*epsilon;duR0=response[2]*epsilon
    def background(N):
        a=np.exp(N);rho=u0*np.array([a**-3,a**-3,1.])
        H=h0*a*np.sqrt(rho.sum()/u0.sum())
        grav=1.5*H**2*rho/rho.sum()
        return a,rho,H,grav
    def rhs(N,y):
        db,dd,tb,td,phi=y
        a,rho,H,grav=background(N)
        dphi=-phi+(grav[0]*tb+grav[1]*td)/(K*K*H)
        Sr=duR0/rho[1]
        return np.array([-tb/H+3*dphi,-td/H+3*dphi,
                         -tb+K*K*phi/H,
                         -td+K*K*(phi-Sr*include_force)/H,dphi])
    Ni=np.log(AI);_,rho,H,grav=background(Ni)
    # Density perturbation follows actual dL_D/dp; zero velocities are a
    # declared probe preparation. Initial metric is solved from Einstein 00.
    y0=np.array([0.,duD0/u0[1],0.,0.,-(grav[1]*duD0/u0[1]+grav[2]*duR0/u0[2])/(K*K)])
    sol=solve_ivp(rhs,(Ni,0),y0,method='DOP853',rtol=rtol,
                  atol=np.array([1e-17,1e-17,1e-20,1e-20,1e-23]),dense_output=True)
    if not sol.success:raise RuntimeError(sol.message)
    N=np.linspace(Ni,0,640);Y=sol.sol(N);dY=np.array([rhs(n,y) for n,y in zip(N,Y.T)]).T
    a=np.exp(N);rho=u0[None,:]*np.column_stack([a**-3,a**-3,np.ones_like(a)])
    H=h0*a*np.sqrt(rho.sum(1)/u0.sum())
    grav=1.5*H[:,None]**2*rho/rho.sum(1)[:,None]
    V=grav[:,2]*duR0/u0[2]
    # Einstein 00: k^2 phi+3H(phi_dot+Hphi)=-4piG a^2 delta rho.
    terms=np.column_stack([K*K*Y[4],3*H*(grav[:,0]*Y[2]+grav[:,1]*Y[3])/(K*K),
                           grav[:,0]*Y[0],grav[:,1]*Y[1],V])
    constraint=terms.sum(1)
    scale=np.max(np.sum(abs(terms),axis=1))
    Fexpected=np.zeros_like(a) if include_force else V*(1-(AI/a)**3)
    normalized_error=float(np.max(abs(constraint))/max(scale,1e-100))
    identity_error=float(np.max(abs(constraint-Fexpected))/max(np.max(abs(V)),1e-100))
    common_error=float(np.max(abs(constraint))/max(np.max(abs(V)),1e-100))
    # Independent finite differences test both continuity and Euler equations;
    # these are not residuals produced by reusing rhs as the derivative.
    probeN=N[2:-2];step=2e-4
    diff=(sol.sol(probeN-2*step)-8*sol.sol(probeN-step)+8*sol.sol(probeN+step)-sol.sol(probeN+2*step))/(12*step)
    ref=np.array([rhs(n,y) for n,y in zip(probeN,sol.sol(probeN).T)]).T
    diff_error=float(np.max(abs(diff-ref))/max(np.max(abs(ref)),1e-100))
    # Spatial trace Einstein equation, not used as an evolution equation.
    trace_error=[];trace_terms=[]
    for n,y,dy in zip(N,Y.T,dY.T):
        aa,rr,HH,cc=background(n)
        matter=(rr[0]+rr[1])/rr.sum();vac=rr[2]/rr.sum()
        H_N_over_H=1-1.5*matter
        phi_NN=-dy[4]+sum(cc[j]/(K*K*HH)*(dy[2+j]-(1+H_N_over_H)*y[2+j]) for j in (0,1))
        vacuum_term=cc[2]*duR0/u0[2]/HH**2
        trace_terms.append(abs(vacuum_term))
        trace_error.append(phi_NN+(4-1.5*matter)*dy[4]+3*vac*y[4]+vacuum_term)
    trace_residual=float(np.max(abs(np.array(trace_error)))/max(trace_terms))
    table=np.column_stack([a,Y.T,rho[:,0]*Y[0],rho[:,1]*Y[1],np.full(len(a),duR0),
                          np.full(len(a),-duR0),constraint,Fexpected])
    result={'H0_auxiliary_dust_vacuum':float(H0),'k_vector_Mpc_inv':[K,0.,0.],
            'resource_modulation_amplitude':epsilon,'a_start':AI,'a_end':1.,
            'delta_u_D_at_a1_from_mapping_J_m3':float(duD0),
            'delta_u_R_from_mapping_J_m3':float(duR0),
            'required_vacuum_transfer':'Q_R^nu=-nabla^nu u_R; Q_D^nu=-Q_R^nu; Q_b^nu=0 (explicit recipient choice)',
            'force_term_in_dark_Euler':'-k^2 delta_u_R/(u_D H_conformal) in dtheta_D/dln(a)',
            'include_required_momentum_transfer':include_force,
            'einstein_constraint_normalized_max':normalized_error,
            'einstein_constraint_in_common_vacuum_source_units':common_error,
            'spatial_Einstein_trace_residual_in_vacuum_source_units':trace_residual,
            'constraint_propagation_identity_error':identity_error,
            'independent_ODE_difference_error':diff_error,
            'maximum_dust_density_contrast':float(np.max(abs(Y[:2]))),
            'final_state_delta_b_delta_D_theta_b_theta_D_phi':Y[:,-1].tolist(),
            'solver_evaluations':sol.nfev,'constraint_scale_Mpc_inv_squared':float(scale)}
    result['vacuum_source_constraint_scale_Mpc_inv_squared']=float(np.max(abs(V)))
    return result,table,sol

def main():
    parent=json.loads((ROOT/'inputs/physical_frame_ledger.json').read_text())
    payload=np.load(ROOT/'inputs/positive_profile_and_payload.npz')
    checks={};rows=[]
    fig,axs=plt.subplots(2,2,figsize=(10,7),sharex=True)
    for branch in ('weighted','unweighted'):
        base=next(x for x in parent['cases'] if x['id']==branch+'_uniform_g_parity')
        u0=np.array(base['observables']['u_P_D_R_today_J_m3'])
        B=payload[branch+'_sector_residue_slot_payload'].sum(2)
        MC=B[:,np.arange(30)%3!=0].sum(1)
        response=ETA*DELTA_A*MC;response[0]=0
        # Check actual finite-resource derivative without inserting a local
        # density rule independent of the previous frame construction.
        mu=B.sum(1);MU=mu-MC;A8=1-np.cos(2*np.pi*8/128)
        def energy(p):return ETA*np.array([mu[0],MU[1]+MC[1]*(A8+DELTA_A*p),MU[2]+MC[2]*(A8+DELTA_A*p)])
        derivative=(energy(.5+1e-5)-energy(.5-1e-5))/(2e-5)
        checks[branch+'_occupation_response_matches_frame_energy']=np.max(abs(derivative-response))<1e-19
        checks[branch+'_local_exchange_alone_generates_no_total_mode']=np.max(abs((np.array(base['final_source_loads'])-base['initial_total_loads'])))<1e-12
        withQ,table,sol=integrate(u0,response,include_force=True)
        noQ,wrong,_=integrate(u0,response,include_force=False)
        high,_,hi=integrate(u0,response,include_force=True,rtol=2e-12)
        linear,_,lin=integrate(u0,response,epsilon=EPS/2,include_force=True)
        N=np.linspace(np.log(AI),0,160)
        error=float(np.max(abs(sol.sol(N)-hi.sol(N)))/np.max(abs(hi.sol(N))))
        homogeneity=float(np.max(abs(sol.sol(N)-2*lin.sol(N)))/np.max(abs(sol.sol(N))))
        checks[branch+'_required_Q_keeps_Einstein_constraint']=withQ['einstein_constraint_normalized_max']<1e-8
        checks[branch+'_common_source_constraint_error']=withQ['einstein_constraint_in_common_vacuum_source_units']<1e-6
        checks[branch+'_spatial_Einstein_trace_closed']=withQ['spatial_Einstein_trace_residual_in_vacuum_source_units']<1e-10
        checks[branch+'_omitted_Q_violates_spatial_trace']=noQ['spatial_Einstein_trace_residual_in_vacuum_source_units']>.9
        checks[branch+'_omitted_Q_detected']=noQ['einstein_constraint_normalized_max']>1e-3
        checks[branch+'_omitted_Q_drift_matches_analytic_identity']=noQ['constraint_propagation_identity_error']<1e-7
        checks[branch+'_ODEs_pass_independent_difference']=withQ['independent_ODE_difference_error']<1e-6
        checks[branch+'_numerical_convergence']=error<1e-8
        checks[branch+'_linear_homogeneity']=homogeneity<1e-8
        checks[branch+'_positive_linear_probe_density']=withQ['maximum_dust_density_contrast']<.01
        checks[branch+'_valid_supply_probability']=0<.5-EPS<.5+EPS<1
        withQ['convergence_relative_error']=error;withQ['linearity_relative_error']=homogeneity
        rows.append({'branch':branch,'completed_conditional_mode':withQ,'missing_transfer_negative_control':noQ})
        header='a,delta_b,delta_D,theta_b_Mpc_inv,theta_D_Mpc_inv,phi,delta_u_b_J_m3,delta_u_D_J_m3,delta_u_R_J_m3,delta_p_J_m3,Einstein00_constraint_Mpc_inv2,analytic_constraint_drift_Mpc_inv2'
        np.savetxt(ROOT/'results'/f'{branch}_single_mode_with_transfer.csv',table,delimiter=',',header=header,comments='')
        np.savetxt(ROOT/'results'/f'{branch}_single_mode_without_transfer.csv',wrong,delimiter=',',header=header,comments='')
        color='#3970aa' if branch=='weighted' else '#b46b2c'
        axs[0,0].plot(table[:,0],table[:,2],color=color,label=branch+' / required transfer')
        axs[0,1].plot(table[:,0],table[:,5],color=color,label=branch)
        axs[1,0].plot(table[:,0],table[:,-2]/withQ['vacuum_source_constraint_scale_Mpc_inv_squared'],color=color,label=branch+' / completed')
        axs[1,1].plot(wrong[:,0],wrong[:,-2]/noQ['vacuum_source_constraint_scale_Mpc_inv_squared'],color=color,label=branch+' / transfer omitted')
    for ax in axs.ravel():ax.set_xscale('log');ax.grid(alpha=.2);ax.legend(fontsize=8)
    axs[0,0].set_ylabel('Dark dust density contrast');axs[0,1].set_ylabel('Metric potential phi')
    axs[1,0].set_ylabel('Einstein 00 residual / vacuum source');axs[1,1].set_ylabel('Einstein 00 residual / vacuum source')
    axs[1,0].set_xlabel('Scale factor a');axs[1,1].set_xlabel('Scale factor a')
    fig.suptitle('One externally specified 3D Fourier mode: resource-response coefficients from WRRA\nControlled dust + vacuum GR completion; not new CMB spectra',fontsize=11)
    fig.tight_layout();fig.savefig(ROOT/'results/single_mode_conservation.png',dpi=170);plt.close(fig)
    checks={k:bool(v) for k,v in checks.items()}
    result={'input':'v0.28 arithmetic resource/energy coefficients; physical Fourier k and occupation-field preparation supplied as diagnostics',
      'WRRA_transform':'dp_resource -> delta L_D/R=(A72-A8) M_controlled dp -> delta u,p -> conservation-required vacuum gradient force -> conditional GR density/velocity/metric mode',
      'new_completion_assumptions':['physical spatial occupation field p(x)=1/2+epsilon cos(k.x)',
                                    'standard scalar GR, isotropic baryon and dark dust, vacuum T_R=-u_R g',
                                    'all vacuum momentum transfer assigned to D, not baryons',
                                    'fixed physical vacuum-density modulation, hence zero time component of background-linear transfer',
                                    'radiation/neutrinos omitted in this separate controlled late-epoch subsystem'],
      'not_derived':['address-to-physical-3D placement','primordial amplitude or k spectrum','microscopic action producing this interaction','anisotropic stress from arithmetic states'],
      'CMB_status':'earlier fixed conditional CMB unchanged; this new interacting mode is NOT integrated into CAMB recombination/photons/neutrinos',
      'cases':rows,'checks':checks,'checks_passed':sum(checks.values()),
      'refutation_conditions':['resource derivative wrong','failure of total Einstein constraint with required transfer','initial amplitudes outside linear domain','numerical nonconvergence'],
      'official_Planck_minus2logL':None}
    (ROOT/'results/single_mode_ledger.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    if not all(checks.values()):raise AssertionError({k:v for k,v in checks.items() if not v})
    print('Single-mode checks '+str(sum(checks.values()))+'/'+str(len(checks)))
    for x in rows:print(x['branch'],json.dumps(x['completed_conditional_mode']),json.dumps(x['missing_transfer_negative_control']))

if __name__=='__main__':main()
