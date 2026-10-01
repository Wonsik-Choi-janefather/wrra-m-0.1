"""WRRA-M 0.6: a finite homogeneous constitutive completion.

One declared energy operator supplies the information update, pressure,
background expansion and twist loads. Local gravity is an inherited matching
rule, not a derived four-dimensional covariant theory. All numerical choices
and dimensional calibrations are in the two parameter files.
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
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('baseline05',ROOT/'baseline_0_5/compute.py')
m05=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m05)


def validate(p,b):
    m05.validate(b)
    N=p['lattice_N']
    if not isinstance(N,int) or isinstance(N,bool) or N<32 or N%16:
        raise ValueError('lattice_N must be a multiple of 16 and at least 32')
    for k in ['a_min','a_max','information_clock_over_H0','rtol','atol','max_log_a_step']:
        if not math.isfinite(p[k]) or p[k]<=0:raise ValueError(k+' must be finite and positive')
    if not p['a_min']<1<p['a_max']:raise ValueError('a_min < 1 < a_max required')
    for k in ['clustering_energy_exponent','background_energy_exponent','noncommuting_test_strength']:
        if not math.isfinite(p[k]) or p[k]<0:raise ValueError(k+' must be finite and nonnegative')
    if p['clustering_energy_exponent']!=0:
        raise ValueError('the inherited clustering renderer requires pressureless exponent zero')
    if p['background_energy_exponent']>3:raise ValueError('this completion excludes the phantom exponent branch')
    if not isinstance(p['output_grid_points'],int) or p['output_grid_points']<21:
        raise ValueError('output_grid_points must be an integer of at least 21')
    if not 0<p['test_radius_kpc']<b['patch_radius_kpc']:raise ValueError('test radius outside patch')
    if not 0<p['lens_impact_kpc']<b['patch_radius_kpc']:raise ValueError('lens impact outside patch')
    modes=p['noncommuting_test_initial_modes'];weights=p['noncommuting_test_initial_weights']
    if len(modes)!=len(weights) or len(set(modes))!=len(modes):raise ValueError('distinct modes and matching weights required')
    if any(not isinstance(j,int) or not 0<=j<N for j in modes):raise ValueError('invalid initial mode')
    if any(not math.isfinite(w) or w<0 for w in weights) or not math.isclose(sum(weights),1):
        raise ValueError('initial weights must be nonnegative and sum to one')


def calibration(b):
    H0=b['H0_km_s_Mpc']*1000/(1e6*b['parsec_m'])
    ucrit=3*H0**2*b['c_m_s']**2/(8*math.pi*b['G_SI'])
    fp=b['fraction_phenotype'];fc=b['fraction_twist_clustering'];fb=1-fp-fc;fh=1-fp
    return {'H0_s_minus1':H0,'ucrit_J_m3':ucrit,'eta_J_m3':fh*ucrit/2,
            'fp':fp,'fc':fc,'fb':fb,'fh':fh,'chi':fc/fh,
            'aT0_m_s2':b['c_m_s']*H0*math.sqrt(fc/8)}


class Carrier:
    def __init__(self,N,epsilon):
        self.N=N;self.epsilon=epsilon
        I=np.eye(N);self.Kc=2*I-np.roll(I,1,axis=0)-np.roll(I,-1,axis=0)
        D=np.zeros((N,N));D[0,0]=1
        self.normalization=1+epsilon/(2*N)
        self.Kb=(self.Kc+epsilon*D)/self.normalization
        self.sc=csr_matrix(self.Kc);self.sb=csr_matrix(self.Kb)
        self.eig_c=np.linalg.eigvalsh(self.Kc);self.eig_b=np.linalg.eigvalsh(self.Kb)
        if min(self.eig_c.min(),self.eig_b.min())< -1e-12:raise ValueError('load kernel not positive')
        self.commutator_norm=float(np.linalg.norm(self.Kc@self.Kb-self.Kb@self.Kc))
    def apply(self,psi):
        kc=2*psi-np.roll(psi,1)-np.roll(psi,-1)
        kb=kc.copy();kb[0]+=self.epsilon*psi[0];kb/=self.normalization
        return kc,kb
    def wave(self,j):return np.exp(2j*math.pi*j*np.arange(self.N)/self.N)/math.sqrt(self.N)
    def packet(self,modes,weights):return sum(math.sqrt(w)*self.wave(j) for j,w in zip(modes,weights))
    def loads(self,psi):
        norm=float(np.vdot(psi,psi).real)
        kc,kb=self.apply(psi)
        vals=[float(np.vdot(psi,k).real)/norm for k in (kc,kb)]
        return tuple(0. if abs(v)<1e-13 else v for v in vals)
    def generator_apply(self,a,psi,p,c):
        kc,kb=self.apply(psi)
        return c['chi']*a**p['clustering_energy_exponent']*kc+(1-c['chi'])*a**p['background_energy_exponent']*kb


def snapshot(a,jc,jb,p,c):
    nc=p['clustering_energy_exponent'];nb=p['background_energy_exponent']
    dc=c['fc']/2*a**(nc-3)*jc;db=c['fb']/2*a**(nb-3)*jb;dp=c['fp']/a**3
    pressure=-(nc*dc+nb*db)/3
    total=dp+dc+db
    q=.5*(total+3*pressure)/total if total>0 else None
    return {'a':float(a),'Jc':jc,'Jb':jb,'density_phenotype_over_ucrit':dp,
            'density_clustering_over_ucrit':dc,'density_background_over_ucrit':db,
            'density_total_over_ucrit':total,'pressure_over_ucrit':pressure,
            'H_over_H0':math.sqrt(total),'deceleration_q':q,
            'hidden_density_over_reference':(dc+db)/c['fh'],
            'hidden_comoving_energy_over_reference':a**3*(dc+db)/c['fh'],
            'zeta_Q_over_reference':a**2*(dc+db)/c['fh'],
            'twist_record_norm_over_reference':a*math.sqrt((dc+db)/c['fh']),
            'twist_rate_over_reference':math.sqrt((dc+db)/c['fh']),
            'aT_over_reference':math.sqrt(dc/c['fc']),
            'actual_hidden_fraction':(dc+db)/total if total>0 else None}


def local_readout(s,p,b,c):
    aT=c['aT0_m_s2']*s['aT_over_reference'];r=p['test_radius_kpc']*1000*b['parsec_m']
    if aT>0:
        q=m05.plummer(np.array([r]),b,aT)
        v=float(q['v'][0])/1000;direct=float(q['v_b'][0])/1000
        extra=float(q['gt'][0]);lens=m05.lens_segment(p['lens_impact_kpc'],b,aT)
    else:
        scale=b['sphere_scale_kpc']*1000*b['parsec_m']
        mb=b['sphere_mass_Msun']*b['M_sun_kg']*r**3/(r*r+scale*scale)**1.5
        direct=v=math.sqrt(b['G_SI']*mb/r)/1000;extra=0.;lens=None
    hidden=s['hidden_density_over_reference']*c['fh']*c['ucrit_J_m3']
    return {'aT_m_s2':aT,'zeta_kappa_total_squared_m_minus2':16*math.pi*b['G_SI']*hidden/b['c_m_s']**4,
            'test_radius_kpc':p['test_radius_kpc'],'v_total_km_s':v,'v_direct_km_s':direct,
            'g_additional_m_s2':extra,'finite_patch_lensing':lens,
            'scope':'fixed test source; conditional Phi=Psi lensing, not an observed galaxy history'}


def state_history(carrier,psi0,p,c,grid):
    """Integrate both ways from a=1 with the same state and energy generator."""
    omega=p['information_clock_over_H0']
    def rhs(n,y):
        a=math.exp(n);psi=y[:-1];jc,jb=carrier.loads(psi)
        E=snapshot(a,jc,jb,p,c)['H_over_H0']
        if E<=0:raise ValueError('log-a evolution requires a positive expansion rate')
        return np.r_[-1j*omega/E*carrier.generator_apply(a,psi,p,c),1/E]
    init=np.r_[psi0,0j]
    opts={'method':'DOP853','rtol':p['rtol'],'atol':p['atol'],
          'max_step':p['max_log_a_step'],'dense_output':True}
    left=solve_ivp(rhs,(0.,math.log(grid[0])),init,**opts)
    right=solve_ivp(rhs,(0.,math.log(grid[-1])),init,**opts)
    if not left.success or not right.success:raise RuntimeError('state integration failed')
    def sol(n):return (left if n<0 else right).sol(n)
    rows=[];norm_error=continuity_error=accel_error=exchange_error=closure_error=0.
    for a in grid:
        n=math.log(a);y=sol(n);psi=y[:-1];jc,jb=carrier.loads(psi)
        s=snapshot(a,jc,jb,p,c);norm=float(np.vdot(psi,psi).real)
        norm_error=max(norm_error,abs(norm-1))
        s['relative_time_H0_t']=float(y[-1].real)
        s['raw_state_norm']=norm
        overlap=abs(np.vdot(psi0,psi))**2/norm
        s['state_density_distance_from_initial']=math.sqrt(max(0.,2*(1-overlap)))
        # Analytic commutator exchange, checked against finite differences below.
        dpsi=rhs(n,y)[:-1];kc,kb=carrier.apply(psi)
        dc=2*float(np.vdot(kc,dpsi).real)/norm
        db=2*float(np.vdot(kb,dpsi).real)/norm
        sc=c['fc']/2*a**(p['clustering_energy_exponent']-3)*dc
        sb=c['fb']/2*a**(p['background_energy_exponent']-3)*db
        s['exchange_c_over_H_ucrit']=sc;s['exchange_b_over_H_ucrit']=sb
        exchange_error=max(exchange_error,abs(sc+sb)/max(s['density_total_over_ucrit'],1e-30))
        eps=1e-5
        def nearby(t):
            z=sol(t)[:-1];j,k=carrier.loads(z);return snapshot(math.exp(t),j,k,p,c)
        minus=nearby(n-eps);plus=nearby(n+eps)
        dtotal=(plus['density_total_over_ucrit']-minus['density_total_over_ucrit'])/(2*eps)
        residual=dtotal+3*(s['density_total_over_ucrit']+s['pressure_over_ucrit'])
        continuity_error=max(continuity_error,abs(residual)/max(s['density_total_over_ucrit'],1e-30))
        dlogH=(math.log(plus['H_over_H0'])-math.log(minus['H_over_H0']))/(2*eps)
        accel_error=max(accel_error,abs((-1-dlogH)-s['deceleration_q']))
        # Normalized T3 closure: E/E0=(W/W0)*(L/L0).
        closure_error=max(closure_error,abs(s['hidden_comoving_energy_over_reference']-a*s['zeta_Q_over_reference']))
        rows.append(s)
    return {'rows':rows,'verification':{'raw_norm_max_error':norm_error,
            'continuity_finite_difference_max_scaled_residual':continuity_error,
            'acceleration_from_H_max_absolute_error':accel_error,
            'internal_exchange_cancellation_max_scaled_error':exchange_error,
            'finite_T3_closure_max_absolute_error':closure_error}},sol


def midpoint_unitary(carrier,psi0,target,p,c,steps):
    """Independent exponential propagator for the nonlinear state/geometry link."""
    h=math.log(target)/steps;omega=p['information_clock_over_H0'];psi=psi0.copy()
    for j in range(steps):
        n=j*h;a=math.exp(n);jc,jb=carrier.loads(psi)
        E=snapshot(a,jc,jb,p,c)['H_over_H0']
        M=c['chi']*a**p['clustering_energy_exponent']*carrier.sc+(1-c['chi'])*a**p['background_energy_exponent']*carrier.sb
        half=expm_multiply((-1j*omega*h/(2*E))*M,psi)
        am=math.exp(n+h/2);jc,jb=carrier.loads(half)
        Em=snapshot(am,jc,jb,p,c)['H_over_H0']
        Mm=c['chi']*am**p['clustering_energy_exponent']*carrier.sc+(1-c['chi'])*am**p['background_energy_exponent']*carrier.sb
        psi=expm_multiply((-1j*omega*h/Em)*Mm,psi)
    return psi


def acceleration_propagation(carrier,psi0,target,p,c):
    """Independent cosmic-time acceleration equation, rather than H constraint."""
    jc,jb=carrier.loads(psi0);E0=snapshot(1.,jc,jb,p,c)['H_over_H0']
    initial=np.r_[1+0j,E0+0j,psi0]
    def rhs(t,y):
        a=float(y[0].real);psi=y[2:];jc,jb=carrier.loads(psi)
        s=snapshot(a,jc,jb,p,c)
        acc=-.5*a*(s['density_total_over_ucrit']+3*s['pressure_over_ucrit'])
        return np.r_[y[1],acc,-1j*p['information_clock_over_H0']*carrier.generator_apply(a,psi,p,c)]
    def hit(t,y):return float(y[0].real)-target
    hit.terminal=True
    s=solve_ivp(rhs,(0.,10. if target>1 else -10.),initial,events=hit,
                method='DOP853',rtol=p['rtol'],atol=p['atol'],max_step=.02)
    if not s.success or len(s.t_events[0])!=1:raise RuntimeError('acceleration propagation did not reach endpoint')
    errors=[]
    for y in s.y.T:
        a=float(y[0].real);jc,jb=carrier.loads(y[2:]);ss=snapshot(a,jc,jb,p,c)
        errors.append(abs(float(y[1].real)**2/a**2-ss['density_total_over_ucrit'])/ss['density_total_over_ucrit'])
    return s.y_events[0][0][2:],float(s.t_events[0][0]),max(errors)


def pressure_check(carrier,p,c):
    states=[np.eye(carrier.N)/carrier.N,np.outer(carrier.wave(8),carrier.wave(8).conj())]
    error=0.
    for rho in states:
        jc=float(np.trace(rho@carrier.Kc).real);jb=float(np.trace(rho@carrier.Kb).real)
        for a in [.5,1.,2.]:
            V=a**3;eps=1e-5*V
            def energy(volume):
                scale=volume**(1/3)
                return c['fc']/2*scale**p['clustering_energy_exponent']*jc+c['fb']/2*scale**p['background_energy_exponent']*jb
            pfd=-(energy(V+eps)-energy(V-eps))/(2*eps)
            exact=snapshot(a,jc,jb,p,c)['pressure_over_ucrit']
            error=max(error,abs(pfd-exact)/max(abs(exact),1e-20))
    return error


def run(p,b,out,verify=True):
    validate(p,b);c=calibration(b);N=p['lattice_N'];plain=Carrier(N,0.)
    coupled=Carrier(N,p['noncommuting_test_strength'])
    modes=p['noncommuting_test_initial_modes'];weights=p['noncommuting_test_initial_weights']
    psi0=plain.packet(modes,weights)
    grid=np.unique(np.r_[np.geomspace(p['a_min'],p['a_max'],p['output_grid_points']),1.])
    nc=p['clustering_energy_exponent'];nb=p['background_energy_exponent']
    reference=[]
    for a in grid:
        s=snapshot(a,2.,2.,p,c);s['relative_time_H0_t']=None;reference.append(s)
    # Reference time is integrated numerically, while its load is stationary.
    def clock(n,y):return [1/snapshot(math.exp(n),2.,2.,p,c)['H_over_H0']]
    for side in [grid[grid<=1],grid[grid>=1]]:
        endpoint=float(side[0] if side[0]<1 else side[-1])
        ss=solve_ivp(clock,(0.,math.log(endpoint)),[0.],method='DOP853',rtol=p['rtol'],atol=p['atol'],dense_output=True)
        for row in reference:
            if (row['a']<=1)==(endpoint<1):row['relative_time_H0_t']=float(ss.sol(math.log(row['a']))[0])
    histories=[]
    for name,carrier in [('coherent_commuting',plain),('coherent_noncommuting',coupled)]:
        history,sol=state_history(carrier,psi0,p,c,grid)
        history['name']=name;history['operator_commutator_norm']=carrier.commutator_norm
        checks=[]
        if verify:
            for a in [p['a_min'],p['a_max']]:
                exact=sol(math.log(a))[:-1];ej=carrier.loads(exact)
                errors=[]
                for steps in [320,640]:
                    other=midpoint_unitary(carrier,psi0,a,p,c,steps)
                    j=carrier.loads(other)
                    errors.append(max(abs(x-y) for x,y in zip(j,ej)))
                state_acc,time_acc,constraint_error=acceleration_propagation(carrier,psi0,a,p,c)
                ja=carrier.loads(state_acc)
                checks.append({'a':a,'midpoint_steps':[320,640],
                    'midpoint_load_absolute_errors':errors,
                    'midpoint_error_improvement_factor':errors[0]/errors[1] if errors[1]>1e-14 else None,
                    'acceleration_solver_load_max_absolute_error':max(abs(x-y) for x,y in zip(ja,ej)),
                    'acceleration_solver_time_absolute_error':abs(time_acc-sol(math.log(a))[-1].real),
                    'acceleration_solver_constraint_max_relative_error':constraint_error})
            v=history['verification']
            assert v['raw_norm_max_error']<1e-7
            assert v['continuity_finite_difference_max_scaled_residual']<2e-7
            assert v['acceleration_from_H_max_absolute_error']<2e-7
            assert v['internal_exchange_cancellation_max_scaled_error']<1e-10
            for ck in checks:
                assert ck['midpoint_load_absolute_errors'][-1]<2e-4
                assert ck['acceleration_solver_constraint_max_relative_error']<2e-7
                assert ck['acceleration_solver_load_max_absolute_error']<2e-7
        history['independent_propagation_checks']=checks
        history['initial_state_trace']=1.
        history['endpoint_local_outputs']=[dict(a=float(a),**local_readout(next(x for x in history['rows'] if math.isclose(x['a'],a)),p,b,c)) for a in [p['a_min'],1.,p['a_max']]]
        for field in ['Jc','Jb']:
            history[field+'_range']=[min(x[field] for x in history['rows']),max(x[field] for x in history['rows'])]
        history['state_density_distance_from_initial_max']=max(x['state_density_distance_from_initial'] for x in history['rows'])
        histories.append(history)
    states=[]
    for name,rho in [('uniform',np.eye(N)/N),('low_mode',np.outer(plain.wave(N//16),plain.wave(N//16).conj())),
                     ('coherent_packet',np.outer(psi0,psi0.conj())),('high_mode',np.outer(plain.wave(N//2),plain.wave(N//2).conj())),
                     ('zero_mode',np.outer(plain.wave(0),plain.wave(0).conj()))]:
        J=float(np.trace(rho@plain.Kc).real);J=0. if abs(J)<1e-13 else J
        s=snapshot(1.,J,J,p,c)
        states.append(dict(state=name,J=J,trace=float(np.trace(rho).real),snapshot=s,**local_readout(s,p,b,c)))
    pressure_error=pressure_check(coupled,p,c)
    assert pressure_error<1e-7
    ref0=next(x for x in reference if x['a']==1.)
    ref_local=local_readout(ref0,p,b,c)
    assert math.isclose(ref_local['aT_m_s2'],c['aT0_m_s2'],rel_tol=1e-14)
    if nb==3:
        assert math.isclose(ref0['deceleration_q'],.5*(1-3*c['fb']),abs_tol=1e-14)
    scan=[{'background_energy_exponent':n,'derived_w_background':-n/3,
           'q_present_uniform':.5*(1-n*c['fb'])} for n in [0.,1.,1.5,2.,3.]]
    sigma_spectrum_bound=[]
    for a in [p['a_min'],1.,p['a_max']]:
        matrix=c['chi']*a**(nc-3)*plain.Kc+(1-c['chi'])*a**(nb-3)*plain.Kb
        eig=np.linalg.eigvalsh(matrix);Jref=float(np.trace(matrix)/N)
        sigma_spectrum_bound.append({'a':a,'physical_load_kernel_min':float(eig.min()),
              'physical_load_kernel_max':float(eig.max()),'reference_load':Jref,
              'reference_in_state_domain':bool(eig.min()-1e-12<=Jref<=eig.max()+1e-12)})
    result={'version':'WRRA-M 0.6','status':'completed finite homogeneous constitutive model; conditional local matching',
       'author':'Wonsik Choi','date':'2026-10-01','inputs':p,'baseline_inputs':b,'calibration':c,
       'constitutive_choices':{'energy_operator':'h(a)=chi*a^nc*Kc+(1-chi)*a^nb*Kb',
          'physical_load_operator':'K_phys(a)=h(a)/a^3',
          'pressure':'p=-partial E_hidden/partial V at fixed rho',
          'state_update':'rho_dot=-i*omega_star*[h(a),rho]',
          'information_clock':'omega_star/H0 is declared; not identified with Planck constant',
          'action':'classical lapse minisuperspace plus coadjoint matrix information action',
          'local_matching':'aT^2=pi*G*u_clustering/3 and inherited nu',
          'ownership':'operators, homogeneity exponents and clock are model choices, not unique microscopic laws'},
       'carrier':m05.carrier_calculation(b),
       'operators':{'N':N,'Kc_min_eigenvalue':float(plain.eig_c.min()),
          'Kb_noncommuting_min_eigenvalue':float(coupled.eig_b.min()),
          'Kb_noncommuting_max_eigenvalue':float(coupled.eig_b.max()),
          'uniform_Jc':float(np.trace(plain.Kc)/N),'uniform_Jb':float(np.trace(coupled.Kb)/N),
          'noncommuting_commutator_norm':coupled.commutator_norm,
          'geometric_load_bound_checks':sigma_spectrum_bound},
       'present_information_state_outputs':states,
       'reference_background':{'rows':reference,'present_local_output':ref_local},
       'state_histories':histories,'energy_homogeneity_scan':scan,
       'verification':{'pressure_from_finite_volume_variation_max_relative_error':pressure_error,
          'baseline_aT_relative_error':abs(ref_local['aT_m_s2']/c['aT0_m_s2']-1),
          'coherent_dense_vs_spectral_load_error':abs(states[2]['J']-sum(w*4*math.sin(math.pi*j/N)**2 for j,w in zip(modes,weights))),
          'all_reference_loads_in_geometric_kernel_domain':all(x['reference_in_state_domain'] for x in sigma_spectrum_bound)},
       'falsification_conditions':['negative load eigenvalue or nonpositive physical density',
          'loss of trace or positivity under the declared state update',
          'noncancelling internal exchange or total continuity failure',
          'pressure inconsistent with the same energy-volume function',
          'background acceleration inconsistent with the lapse constraint',
          'motion and lensing incompatible with the assumed local matching'],
       'open_physics':['unique microscopic origin of operators, homogeneity exponents, clock and fractions',
          'four-dimensional covariant action and local-source backreaction',
          'spatial perturbations, sound speed, anisotropic stress and gravitational slip',
          'physical carrier filter selection; symmetric gaps remain zero',
          'hybrid measurement law, photon twist-redshift kernel and observed joint fit',
          'actual spatial topology, dimensional holonomy and absolute cosmic size']}
    out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    summary={k:result[k] for k in ['version','status','calibration','operators','present_information_state_outputs','energy_homogeneity_scan','verification','open_physics']}
    summary['reference_background_rows']=[next(x for x in reference if math.isclose(x['a'],a)) for a in [p['a_min'],1.,p['a_max']]]
    summary['state_histories']=[{k:v for k,v in h.items() if k!='rows'} for h in histories]
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False))
    make_figures(result,out)
    return result


def make_figures(result,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    colors=['#183b5b','#9b6a27','#65776d']
    rows=result['reference_background']['rows'];a=np.array([x['a'] for x in rows])
    fig,axs=plt.subplots(1,2,figsize=(9.2,3.8))
    axs[0].plot(a,[x['H_over_H0'] for x in rows],label='Expansion H/H0',color=colors[0])
    axs[0].plot(a,[x['deceleration_q'] for x in rows],label='Deceleration q',color=colors[1])
    axs[0].axhline(0,color='#aaa',lw=.7)
    axs[1].plot(a,[x['twist_record_norm_over_reference'] for x in rows],label='Accumulated twist record',color=colors[0])
    axs[1].plot(a,[x['twist_rate_over_reference'] for x in rows],label='Physical twist rate',color=colors[1])
    axs[0].set(xlabel='Scale factor a',ylabel='Dimensionless background output')
    axs[1].set(xlabel='Scale factor a',ylabel='Ratio to reference at a=1')
    for ax in axs:ax.grid(alpha=.18);ax.legend(fontsize=8)
    fig.suptitle('WRRA-M 0.6 reference: one energy functional, expansion and twist together',fontsize=10)
    fig.tight_layout();fig.savefig(out/'expansion_twist.png',dpi=220);plt.close(fig)
    hist=result['state_histories'][1];rows=hist['rows'];a=np.array([x['a'] for x in rows])
    fig,axs=plt.subplots(1,2,figsize=(9.2,3.7))
    axs[0].plot(a,[x['Jc'] for x in rows],label='Clustering weight Jc',color=colors[0])
    axs[0].plot(a,[x['Jb'] for x in rows],label='Background weight Jb',color=colors[1])
    axs[1].plot(a,[x['exchange_c_over_H_ucrit'] for x in rows],label='Clustering exchange',color=colors[0])
    axs[1].plot(a,[x['exchange_b_over_H_ucrit'] for x in rows],label='Background exchange',color=colors[1],ls='--')
    axs[0].set(xlabel='Scale factor a',ylabel='Information-state weighted load')
    axs[1].set(xlabel='Scale factor a',ylabel='Exchange / (H ucrit,0)')
    for ax in axs:ax.grid(alpha=.18);ax.legend(fontsize=8)
    fig.suptitle('Noncommuting test: changing state loads with cancelling internal exchange',fontsize=10)
    fig.tight_layout();fig.savefig(out/'state_exchange.png',dpi=220);plt.close(fig)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--parameters',default=str(ROOT/'parameters.json'))
    ap.add_argument('--baseline',default=str(ROOT/'baseline_0_5/parameters.json'))
    ap.add_argument('--out',default=str(ROOT/'results'));args=ap.parse_args()
    r=run(json.loads(Path(args.parameters).read_text()),json.loads(Path(args.baseline).read_text()),Path(args.out))
    print(json.dumps({'version':r['version'],'verification':r['verification'],
       'q_present':next(x for x in r['reference_background']['rows'] if x['a']==1)['deceleration_q'],
       'state_histories':[{k:h[k] for k in ['name','Jc_range','Jb_range','verification','independent_propagation_checks']} for h in r['state_histories']]},indent=2))
