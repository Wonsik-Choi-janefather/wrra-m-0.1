"""Expanding two-fluid separate-universe conversion with exact tangent ODEs.
Units: 8 pi G/3=1, initial scale factor relative a=1, H=1.
Conversion acts on a declared sub-reservoir, not all cosmic radiation.
This is the gradient-leading continuum closure, not full Einstein-Boltzmann matching.
"""
import verify_inputs
from pathlib import Path
import json,math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
P=Path(__file__).resolve().parent;OUT=P/'results'
AI=1e-10;GAMMA=math.log(2);TF=10.
checks={}
def check(name,yes):
    checks[name]=bool(yes)
    if not yes:raise AssertionError(name)

def rhs(t,y,beta,active,perturb=0.):
    N,C,M,H,W=y[:5];Ns,Cs,Ms,Hs,Ws=y[5:]
    U=1-beta;R=U+C
    rad=R*math.exp(-4*N);matter=M*math.exp(-3*N)
    drad=(Cs-4*R*Ns)*math.exp(-4*N)
    dmat=(Ms-3*M*Ns)*math.exp(-3*N)
    rate=GAMMA*(1+perturb) if active else 0.
    # derivative with respect to the fractional proper-rate perturbation at zero
    d_rate=GAMMA if active else 0.
    return [H,-rate*C,rate*C*math.exp(-N),-.5*(4*rad+3*matter),H*R*math.exp(-N),
        Hs,-rate*Cs-d_rate*C,math.exp(-N)*(rate*Cs+d_rate*C-rate*C*Ns),
        -.5*(4*drad+3*dmat),math.exp(-N)*(Hs*R+H*Cs-H*R*Ns)]

def evolve(beta,perturb=0.,rtol=3e-12):
    y0=[0,beta,0,1,0,0,0,0,0,0]
    first=solve_ivp(lambda t,y:rhs(t,y,beta,True,perturb),(0,1),y0,method='DOP853',
        rtol=rtol,atol=1e-23,max_step=.025,dense_output=True)
    second=solve_ivp(lambda t,y:rhs(t,y,beta,False,perturb),(1,TF),first.y[:,-1],method='DOP853',
        rtol=rtol,atol=1e-23,max_step=.1,dense_output=True)
    if not(first.success and second.success):raise RuntimeError('integration failed')
    return first,second

def quantities(y,beta):
    N,C,M,H,W=y[:5];Ns,Cs,Ms,Hs,Ws=y[5:];R=1-beta+C
    rr=R*np.exp(-4*N);rm=M*np.exp(-3*N)
    # At the post-conversion boundary C and M are constant comoving budgets.
    zr=Cs/(4*R);zm=Ms/(3*M);S=3*(zm-zr)
    dr=rr*(Cs/R-4*Ns);dm=rm*(Ms/M-3*Ns)
    dt=(dr+dm)/(H*(4*rr+3*rm))
    zeta=Ns+H*dt
    return dict(zeta_radiation=zr,zeta_matter=zm,entropy=S,zeta_uniform_density=zeta,
        zeta_weighted=(4*rr*zr+3*rm*zm)/(4*rr+3*rm),a_relative=np.exp(N),
        radiation=rr,matter=rm,friedmann_error=(H*H-rr-rm)/(rr+rm),
        energy_work_error=R*np.exp(-N)+M+W-1)

def main():
    addr=json.loads((P/'inputs/address_results.json').read_text())
    bg=next(v['background'] for v in addr['cases'] if v['branch']=='dark_weight_only')
    wh2gamma=addr['thermal_wh2']['photon'];neff=3.044
    # Declared effective relativistic-fluid extrapolation; no changing g* history.
    wh2rad=wh2gamma*(1+0.22710731766023898*neff)
    target=bg['omch2']/wh2rad*AI
    def residual(beta):
        _,s=evolve(beta,rtol=2e-10);N,C,M,H,W=s.y[:5,-1]
        return M/(1-beta+C)-target
    beta=brentq(residual,1e-9,1e-4,xtol=1e-21,rtol=1e-13)
    a,b=evolve(beta);y=b.y[:,-1];q=quantities(y,beta)
    sample=np.column_stack([a.sol(np.linspace(0,1,101)),b.sol(np.linspace(1.01,TF,300))])
    N,C,M,H,W=sample[:5];R=1-beta+C
    rr=R*np.exp(-4*N);rm=M*np.exp(-3*N)
    fried=float(np.max(abs(H*H-rr-rm)/(rr+rm)))
    work=float(np.max(abs(R*np.exp(-N)+M+W-1)))
    check('positive_densities',np.all((C>0)&(M>=0)&(rr>0)&(rm>=0)))
    check('expanding_branch',np.all(H>0) and np.all(np.diff(N)>=0))
    check('radiation_comoving_half_conversion',abs(a.y[1,-1]/beta-.5)<1e-11)
    check('friedmann_constraint',fried<2e-10)
    check('energy_plus_pressure_work',work<2e-11)
    check('background_observed_ratio_matched',abs(y[2]/(1-beta+y[1])/target-1)<1e-10)
    check('uniform_density_deltaN_identity',abs(q['zeta_uniform_density']-q['zeta_weighted'])<1e-17)
    check('entropy_from_species_curvatures',abs(q['entropy']-3*(q['zeta_matter']-q['zeta_radiation']))<1e-14)
    # Species curvatures and relative entropy are constant after exchange ends.
    middle=quantities(b.sol(3.),beta)
    for key in ['zeta_radiation','zeta_matter','entropy']:
        check('post_exchange_conserved_'+key,abs(q[key]-middle[key])<1e-12)
    # Finite difference at enlarged perturbation, avoiding cancellation of 1e-8 seeds.
    fd=[]
    for eps in [1e-2,5e-3]:
        _,plus=evolve(beta,eps);_,minus=evolve(beta,-eps)
        yp=plus.y[:,-1];ym=minus.y[:,-1]
        cp=yp[1];cm=ym[1]
        sf=(math.log(yp[2]/ym[2])-.75*math.log((1-beta+cp)/(1-beta+cm)))/(2*eps)
        fd.append(sf)
    check('entropy_tangent_finite_difference',abs(fd[-1]/q['entropy']-1)<2e-5)
    check('finite_difference_refinement',abs(fd[-1]-q['entropy'])<abs(fd[0]-q['entropy']))
    _,tight=evolve(beta,rtol=5e-13);qt=quantities(tight.y[:,-1],beta)
    check('time_integrator_convergence',abs(qt['entropy']/q['entropy']-1)<1e-10)
    seed=np.load(P/'inputs/quantized_seed.npz')['entropy']
    S=q['entropy']*seed;zrad=q['zeta_radiation']*seed
    # H_initial normalized to the adopted present-day radiation budget.
    h=bg['H0']/100;H0_Mpc=bg['H0']/299792.458;Or=wh2rad/h**2
    Hi=H0_Mpc*math.sqrt(Or)/(AI*AI*math.sqrt(1-beta+y[1]))
    aphysical=AI*q['a_relative'];calH=aphysical*Hi*y[3]
    eps_gradient=3.2/calH
    check('all_64_modes_superhorizon_at_matching',eps_gradient<.002)
    out={'version':'0.3','assumptions':{'a_initial':AI,'proper_pulse_duration_Hinitial_units':1.,
        'proper_rate_Hinitial_units':GAMMA,'matter_species':'effective CDM-like component',
        'conversion_reservoir':'subcomponent of an effective perfect relativistic fluid',
        'gradient_order':'leading separate-universe, flat local FLRW',
        'rate_modulation':'Gamma_j=Gamma*(1+S_seed_j); seed from prior exact quantization, no amplitude refit',
        'quantization_scope':'quantized spatial seed; continuum transfer-rate closure; no new finite-q emission-time solver',
        'regular_completion':'species invariants supplied to regular primordial mode basis; finite-gradient metric/velocity/neutrino matching still OPEN'},
        'calibrated_convertible_radiation_fraction':beta,'background_target_M_over_R':target,
        'entropy_response_to_rate_modulation':q['entropy'],'radiation_curvature_response':q['zeta_radiation'],
        'uniform_density_curvature_response_at_matching':q['zeta_uniform_density'],
        'a_matching':aphysical,'kmax_over_aH':eps_gradient,'leading_gradient_order_parameter':eps_gradient**2,
        'pressure_work_error_max':work,'friedmann_constraint_relative_error_max':fried,
        'dynamic_entropy_RMS':float(np.sqrt(np.mean(S*S))),
        'generated_adiabatic_radiation_curvature_RMS':float(np.sqrt(np.mean(zrad*zrad))),
        'time_unit_seconds':1/Hi*3.085677581e22/299792458,
        'checks_passed':sum(checks.values()),'checks':checks}
    np.savez_compressed(OUT/'dynamic_preparation.npz',entropy=S,zeta_radiation=zrad,
        history=sample,time=np.r_[np.linspace(0,1,101),np.linspace(1.01,TF,300)])
    (OUT/'dynamics_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
