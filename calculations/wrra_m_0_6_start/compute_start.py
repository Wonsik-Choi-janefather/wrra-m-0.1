"""WRRA-M 0.6 start: carrier load -> twist -> gravity and background tests.

The load kernel and background equations of state are declared model choices.
This program computes them; it does not derive a unique microscopic LAW.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('baseline05',ROOT/'baseline_0_5/compute.py')
m05=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m05)


def kernel_and_states(N):
    if not isinstance(N,int) or N<32 or N%16:
        raise ValueError('lattice_N must be an integer multiple of 16 and at least 32')
    eye=np.eye(N)
    K=2*eye-np.roll(eye,1,axis=0)-np.roll(eye,-1,axis=0)
    sites=np.arange(N)
    wave=lambda j:np.exp(2j*np.pi*j*sites/N)/np.sqrt(N)
    cases=[('reference_uniform',eye/N,None),
           ('low_mode',np.outer(wave(N//16),wave(N//16).conj()),[N//16]),
           ('coherent_packet',None,[N//16,N//8,3*N//16]),
           ('high_mode',np.outer(wave(N//2),wave(N//2).conj()),[N//2]),
           ('zero_mode',np.outer(wave(0),wave(0).conj()),[0])]
    packet=sum(wave(j) for j in cases[2][2])/math.sqrt(3)
    cases[2]=(cases[2][0],np.outer(packet,packet.conj()),cases[2][2])
    return K,cases


def background(name,components,p,grid):
    """Numerically evolve W_s=zeta*Q_s up to a fixed normalization.

    u_s=C W_s/a^2; source-free continuity implies W_s'=(-1-3w_s)W_s.
    The w_s are frozen constitutive inputs, not dynamically inferred by this ODE.
    """
    om=p['fraction_phenotype']
    start,end=math.log(grid[0]),math.log(grid[-1])
    gammas=np.array([-1-3*w for _,_,w in components])
    init=np.array([omega*math.exp(gamma*start)
                   for (_,omega,_),gamma in zip(components,gammas)])
    def rhs(n,y):
        a=math.exp(n)
        e2=om/a**3+float(np.sum(y[:-1]))/a**2
        if e2<=0:raise ValueError('nonpositive Friedmann density')
        return np.r_[gammas*y[:-1],1/math.sqrt(e2)]
    solution=solve_ivp(rhs,(start,end),np.r_[init,0.],method='DOP853',
                       rtol=1e-11,atol=1e-13,dense_output=True,max_step=.04)
    if not solution.success:raise RuntimeError(solution.message)
    rows=[];max_analytic_error=0.;max_closure_error=0.;max_continuity_error=0.
    for a in grid:
        n=math.log(a);y=solution.sol(n);W=y[:-1];dens=W/a**2
        analytic=np.array([omega*a**gamma for (_,omega,_),gamma in zip(components,gammas)])
        max_analytic_error=max(max_analytic_error,float(np.max(np.abs(W-analytic)/analytic)))
        total=om/a**3+float(np.sum(dens));e=math.sqrt(total)
        q=.5*(om/a**3+sum((1+3*w)*u for (_,_,w),u in zip(components,dens)))/total
        hidden=float(np.sum(dens));hidden0=1-om
        if name=='frozen_whole_hidden':
            clustering=p['fraction_twist_clustering']/hidden0*hidden
        else:clustering=float(dens[0])
        # H/H0 * sqrt(f_cl/f_cl0) equals sqrt(u_cl/u_cl0).
        at_ratio=math.sqrt(clustering/p['fraction_twist_clustering'])
        at_via_H=e*math.sqrt((clustering/total)/p['fraction_twist_clustering'])
        max_closure_error=max(max_closure_error,abs(at_ratio-at_via_H))
        # Independent finite-difference continuity residual, not the ODE RHS.
        eps=2e-5
        d_up=(solution.sol(n+eps)[:-1]*math.exp(-2*(n+eps))-
              solution.sol(n-eps)[:-1]*math.exp(-2*(n-eps)))/(2*eps)
        res=d_up+np.array([3*(1+w)*u for (_,_,w),u in zip(components,dens)])
        max_continuity_error=max(max_continuity_error,float(np.max(np.abs(res)/dens)))
        rows.append({'a':float(a),'H_over_H0':e,'deceleration_q':q,
                     'hidden_energy_density_over_present':hidden/hidden0,
                     'zeta_Q_over_present':float(np.sum(W))/hidden0,
                     'twist_record_norm_over_present_if_fixed_zeta':math.sqrt(float(np.sum(W))/hidden0),
                     'twist_rate_over_present_if_fixed_zeta':math.sqrt(hidden/hidden0),
                     'information_energy_in_comoving_volume_over_present':a**3*hidden/hidden0,
                     'aT_over_present':at_ratio,
                     'relative_time_H0_t':float(y[-1]-solution.sol(0)[-1]),
                     'component_density_over_critical_present':dens.tolist()})
    return {'name':name,'components':[{'name':n,'omega_present':o,'w':w} for n,o,w in components],
            'rows':rows,'verification':{'ode_vs_exact_W_max_relative_error':max_analytic_error,
               'continuity_finite_difference_max_scaled_residual':max_continuity_error,
               'H_fraction_vs_energy_aT_max_absolute_error':max_closure_error}}


def run(p,base,out):
    m05.validate(base)
    if not (0<p['a_min']<1<p['a_max']):
        raise ValueError('scale-factor bounds must satisfy 0 < a_min < 1 < a_max')
    if base['fraction_twist_clustering']<=0:
        raise ValueError('the normalized background prototype requires positive clustering fraction')
    if p['test_radius_kpc']<=0 or p['lens_impact_kpc']<=0:
        raise ValueError('test radius and lens impact must be positive')
    N=p['lattice_N'];K,cases=kernel_and_states(N)
    eigen=np.linalg.eigvalsh(K)
    assert eigen.min()>-1e-12
    c=base['c_m_s'];G=base['G_SI'];pc=base['parsec_m']
    H0=base['H0_km_s_Mpc']*1000/(1e6*pc)
    ucrit=3*H0**2*c**2/(8*np.pi*G)
    fp=base['fraction_phenotype'];fc=base['fraction_twist_clustering'];fh=1-fp
    ub0=fh*ucrit;uc0=fc*ucrit
    J0=float(np.trace(cases[0][1]@K).real)
    eta=ub0/J0
    partition=fc/fh
    unit_cases=[]
    for name,rho,modes in cases:
        assert np.max(np.abs(rho-rho.conj().T))<1e-13
        assert abs(np.trace(rho)-1)<1e-13
        assert np.linalg.eigvalsh(rho).min()>-1e-12
        J=float(np.trace(rho@K).real)
        # The Laplacian annihilates the constant state. Remove round-off at zero.
        if abs(J)<1e-13:J=0.
        if modes is not None:
            spectral=float(np.mean([(2*np.sin(np.pi*j/N))**2 for j in modes]))
        else:spectral=float(np.mean((2*np.sin(np.pi*np.arange(N)/N))**2))
        assert abs(J-spectral)<2e-13
        upre=eta*J;ucl=partition*upre
        zk2=16*np.pi*G*upre/c**4
        aT=math.sqrt(np.pi*G*ucl/3)
        total_snapshot=fp*ucrit+upre
        H=math.sqrt(8*np.pi*G*total_snapshot/(3*c**2))
        fcluster=ucl/total_snapshot if total_snapshot>0 else None
        if fcluster is not None:
            assert math.isclose(aT,c*H*math.sqrt(fcluster/8),rel_tol=2e-14,abs_tol=1e-24)
        r=p['test_radius_kpc']*1000*pc
        # In the zero-load limit, the inherited constitutive response is Newtonian.
        if aT>0:
            s=m05.plummer(np.array([r]),base,aT)
            total=float(s['v'][0]/1000);direct=float(s['v_b'][0]/1000)
            additional=float(s['gt'][0]);lens=m05.lens_segment(p['lens_impact_kpc'],base,aT)
        else:
            b=base['sphere_scale_kpc']*1000*pc
            mb=base['sphere_mass_Msun']*base['M_sun_kg']*r**3/(r*r+b*b)**1.5
            direct=total=math.sqrt(G*mb/r)/1000;additional=0.;lens=None
        unit_cases.append({'state':name,'trace':float(np.trace(rho).real),
            'carrier_load_dense':J,'carrier_load_spectral':spectral,'load_over_reference':J/J0,
            'u_hidden_J_m3':upre,'u_clustering_J_m3':ucl,'zeta_kappa_squared_m_minus2':zk2,
            'aT_m_s2':aT,'H_snapshot_over_H0':H/H0,
            'actual_fraction_hidden':upre/total_snapshot if total_snapshot>0 else None,
            'test_radius_kpc':p['test_radius_kpc'],'v_total_km_s':total,'v_direct_km_s':direct,
            'g_additional_m_s2':additional,'finite_patch_lensing':lens})
    at0=c*H0*math.sqrt(fc/8)
    assert math.isclose(unit_cases[0]['aT_m_s2'],at0,rel_tol=2e-14)
    # Phase changes preserving K must preserve the load.
    unitary=np.roll(np.eye(N),7,axis=0)
    packet=cases[2][1]
    invariance=abs(float(np.trace((unitary@packet@unitary.T)@K).real)-float(np.trace(packet@K).real))
    assert invariance<2e-13
    grid=np.unique(np.r_[np.geomspace(p['a_min'],p['a_max'],401),1.])
    bg0=1-fp-fc
    backgrounds=[background('frozen_whole_hidden',[('whole_hidden',fh,-1/3)],base,grid),
                 background('cold_plus_frozen_background',[('clustering',fc,0),('background',bg0,-1/3)],base,grid),
                 background('cold_plus_constant_energy_background',[('clustering',fc,0),('background',bg0,-1)],base,grid)]
    for item in backgrounds:
        assert item['verification']['ode_vs_exact_W_max_relative_error']<1e-8
        assert item['verification']['continuity_finite_difference_max_scaled_residual']<2e-8
        # Necessary state-domain check for the same FIXED kernel and eta.
        # A normalized positive rho cannot have Tr(rho K) above lambda_max(K).
        maximum_load=float(eigen.max())
        violations=0
        for row in item['rows']:
            required=J0*row['hidden_energy_density_over_present']
            reachable=0<=required<=maximum_load+1e-12
            row['required_J_if_same_fixed_kernel_and_eta']=required
            row['within_fixed_kernel_state_domain']=reachable
            # An algebraic load witness, not a derived pressure or update law.
            row['high_mode_weight_in_zero_high_mixture']=min(required/maximum_load,1.) if reachable else None
            violations+=not reachable
        def bound_gap(a):
            hidden=sum(o*a**(-3*(1+w)) for _,o,w in
                       [(d['name'],d['omega_present'],d['w']) for d in item['components']])
            return J0*hidden/fh-maximum_load
        threshold=brentq(bound_gap,p['a_min'],1.) if bound_gap(p['a_min'])>0 else None
        item['fixed_kernel_admissibility']={
            'required_J_bounds':[0.,maximum_load],
            'number_of_grid_rows_outside_domain':violations,
            'minimum_a_within_domain_in_test_interval':threshold if threshold is not None else p['a_min'],
            'meaning':'necessary fixed-kernel state-domain condition; no derived microscopic pressure or state update',
            'outside_domain':'cannot represent that background density with trace-one rho and the same fixed K and eta'}
    result={'version':'WRRA-M 0.6 start calculation','status':'finite prototype; microscopic completion remains open',
       'inputs':p,'baseline_inputs':base,'carrier':m05.carrier_calculation(base),
       'load_kernel':{'operator':'periodic cycle Laplacian L_C; same for all 16 witness channels',
          'state':'I_16/16 tensor rho_internal, trace one; not a bit count',
          'N':N,'minimum_kernel_eigenvalue':float(eigen.min()),'reference_J':J0,
          'energy_density_per_dimensionless_load_J_m3':eta,
          'clustering_partition':partition,'calibration':'u_hidden,0=(1-f_phi,0)*rho_critical,0*c^2',
          'ownership':'L_C load kernel and partition are explicit new constitutive choices; not unique LAW'},
       'information_to_gravity':unit_cases,'backgrounds':backgrounds,
       'verification':{'translation_unitary_load_invariance_error':invariance,
         'baseline_aT_relative_error':abs(unit_cases[0]['aT_m_s2']/at0-1),
         'zero_mode_load':unit_cases[-1]['carrier_load_dense']},
       'unresolved':['physical choice and evolution of carrier information states',
         'microscopic ownership of the energy calibration and clustering partition',
         'covariant action linking the load kernel to both background and local response',
         'sound speed, anisotropic stress, lens slip and perturbation stability',
         'photon transport twist redshift kernel and combined observational fit',
         'actual cosmic topology, dimensional holonomy and absolute finite length']}
    out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axs=plt.subplots(1,2,figsize=(9,3.8))
    for item,color,label in zip(backgrounds,['#7b7b7b','#b17b36','#1c506a'],['Frozen hidden','Cold + frozen background','Cold + constant energy background']):
        a=np.array([r['a'] for r in item['rows']]);q=np.array([r['deceleration_q'] for r in item['rows']])
        valid=np.array([r['within_fixed_kernel_state_domain'] for r in item['rows']])
        axs[0].plot(a,q,color=color,ls=':',alpha=.6)
        axs[0].plot(a[valid],q[valid],color=color,label=label)
    rows=backgrounds[2]['rows'];a=np.array([r['a'] for r in rows])
    valid=np.array([r['within_fixed_kernel_state_domain'] for r in rows])
    for field,label,color in [('twist_record_norm_over_present_if_fixed_zeta','Accumulated record norm','#1c506a'),
                              ('twist_rate_over_present_if_fixed_zeta','Twist rate','#b17b36')]:
        values=np.array([r[field] for r in rows])
        axs[1].plot(a,values,color=color,ls=':',alpha=.6)
        axs[1].plot(a[valid],values[valid],label=label,color=color)
    axs[0].axhline(0,color='#aaa',lw=.8);axs[0].set(xlabel='Scale factor a',ylabel='Deceleration parameter q')
    axs[1].set(xlabel='Scale factor a',ylabel='Ratio to present (a=1)')
    for ax in axs:ax.grid(alpha=.18);ax.legend(fontsize=7.5)
    fig.suptitle('Declared pressure closures; dotted segments exceed the fixed-kernel load bound',fontsize=9)
    fig.tight_layout();fig.savefig(out/'background_start.png',dpi=220);plt.close(fig)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',default=str(ROOT/'results'))
    parser.add_argument('--parameters',default=str(ROOT/'parameters.json'))
    args=parser.parse_args()
    result=run(json.loads(Path(args.parameters).read_text()),
               json.loads((ROOT/'baseline_0_5/parameters.json').read_text()),Path(args.out))
    now=lambda b:next(r for r in b['rows'] if r['a']==1.)
    print(json.dumps({'state_loads':[{k:r[k] for k in ['state','carrier_load_dense','aT_m_s2','v_total_km_s']} for r in result['information_to_gravity']],
           'q_present':{b['name']:now(b)['deceleration_q'] for b in result['backgrounds']},
           'verification':result['verification']},ensure_ascii=False,indent=2))
