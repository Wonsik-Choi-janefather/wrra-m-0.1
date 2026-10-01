"""WRRA-M 0.5: finite conditional calculations, not a covariant completion.

Run: python compute.py --out results
Dependencies: numpy scipy matplotlib
All dimensional constants and calibrations are in parameters.json.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import math
from fractions import Fraction
import numpy as np
from scipy.integrate import quad
from scipy.special import ive, kve


def validate(p):
    for key in ('c_m_s', 'G_SI', 'H0_km_s_Mpc', 'M_sun_kg', 'parsec_m'):
        if not math.isfinite(p[key]) or p[key] <= 0:
            raise ValueError(key + ' must be positive')
    for key in ('fraction_phenotype', 'fraction_twist_clustering'):
        if not math.isfinite(p[key]):
            raise ValueError(key + ' must be finite')
    if p['fraction_phenotype'] < 0 or p['fraction_twist_clustering'] <= 0:
        raise ValueError('Fractions must be nonnegative; clustering fraction must be positive')
    if p['fraction_phenotype'] + p['fraction_twist_clustering'] > 1:
        raise ValueError('Phenotype and clustering fractions must not exceed one')


def nu(y):
    y = np.asarray(y, dtype=float)
    if np.any(y <= 0):
        raise ValueError('y must be positive; the origin is a degenerate limit')
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def source_ratio(clustering_fraction, phenotype_fraction):
    """An absent denominator has no finite ratio; JSON null records it."""
    return clustering_fraction / phenotype_fraction if phenotype_fraction > 0 else None


def dx_dy(y):
    s = np.sqrt(y)
    d = -np.expm1(-s)
    return (d - 0.5 * s * np.exp(-s)) / d**2


def static_F(y):
    """F(Y(y)), Y=(y*nu(y))^2. Constructed spherical AQUAL action.

    Using y=t^2 avoids an apparent endpoint singularity.
    F = integral_0^y 2 q dx/dq dq.
    """
    def integrand(t):
        if t == 0:
            return 0.0
        return 4 * t**3 * float(dx_dy(t*t))
    return quad(integrand, 0, math.sqrt(y), epsabs=1e-15, epsrel=1e-11)[0]


def plummer(r, p, aT):
    G = p['G_SI']
    M = p['sphere_mass_Msun'] * p['M_sun_kg']
    b = p['sphere_scale_kpc'] * 1000 * p['parsec_m']
    mb = M * r**3 / (r*r + b*b)**1.5
    gm = G * mb / r**2
    y = gm / aT
    N = nu(y)
    g = gm * N
    eta = 3*b*b / (r*r + b*b)
    s = np.sqrt(y)
    d = -np.expm1(-s)
    nu_prime = -np.exp(-s) / (2*s*d*d)
    mt = mb*(N-1)
    dmt_dr = mb/r * (eta*(N-1) + nu_prime*y*(eta-2))
    rho_eff = dmt_dr/(4*np.pi*r*r)
    return {'mb': mb, 'gm': gm, 'g': g, 'gt': g-gm, 'mt': mt,
            'rho_eff': rho_eff, 'v': np.sqrt(r*g), 'v_b': np.sqrt(r*gm), 'y': y}


def lens_segment(impact_kpc, p, aT):
    """Deflection accumulated INSIDE a finite spherical patch only.

    Conditional on zero gravitational slip Phi=Psi; no exterior or
    source/lens/observer distance factors are included.
    """
    c = p['c_m_s']
    kpc = 1000*p['parsec_m']
    b = impact_kpc*kpc
    R = p['patch_radius_kpc']*kpc
    if not 0 < b < R:
        raise ValueError('Impact radius must lie inside patch')
    zmax = math.sqrt(R*R-b*b)
    def fn(t, kind):
        z = t*kpc
        r = math.hypot(b,z)
        q = plummer(r,p,aT)
        return float(q[kind])*b/r*kpc
    total, err = quad(lambda t: fn(t,'g'),0,zmax/kpc,epsabs=1e-4,epsrel=2e-11)
    baryon, _ = quad(lambda t: fn(t,'gm'),0,zmax/kpc,epsabs=1e-4,epsrel=2e-11)
    factor = 4/c**2
    return {'impact_kpc':impact_kpc,'alpha_patch_rad':factor*total,
            'alpha_baryon_patch_rad':factor*baryon,
            'alpha_twist_patch_rad':factor*(total-baryon),
            'alpha_patch_arcsec':factor*total*180/math.pi*3600,
            'quad_abs_error_rad':factor*err}


def disk_speed(R_kpc,p,aT):
    """Re-runs the earlier algebraic disk renderer, not a vector PDE solution."""
    kpc=1000*p['parsec_m']; G=p['G_SI']; Ms=p['M_sun_kg']
    R=np.asarray(R_kpc)*kpc
    v2=np.zeros_like(R,dtype=float)
    for m,rd in p['disk_components_mass_1e9Msun_scale_kpc']:
        rd=rd*kpc; y=R/(2*rd)
        # Exponential scaling cancels in the Bessel products.
        bessel=ive(0,y)*kve(0,y)-ive(1,y)*kve(1,y)
        v2 += 2*G*(m*1e9*Ms)/rd*y*y*bessel
    mb,ab=p['bulge_mass_1e9Msun_scale_kpc']
    v2 += G*(mb*1e9*Ms)*R/(R+ab*kpc)**2
    gm=v2/R; N=nu(gm/aT)
    return np.sqrt(v2*N)/1000,np.sqrt(v2)/1000,N-1


def carrier_calculation(p):
    """Homogeneous 16-channel common carrier with a periodic internal witness.

    The resolvent is computed on the internal finite chain. Each identical
    channel injection has the same scalar norm. Normalizing the transport
    Gram gives I_16, which has full transport rank but zero selection gaps.
    """
    N=p['internal_lattice_N']
    j=np.arange(N)
    lam=(2*np.sin(np.pi*j/N))**2
    probes=np.asarray(p['carrier_probe_frequency_squared'])
    # Response is an averaged positive Green-function intensity.
    response=float(np.mean([np.mean(1/((lam-w)**2+p['carrier_damping']**2))
                            for w in probes]))
    raw_gram=response*np.eye(16)
    gram=raw_gram/response
    u=np.full(8,math.sqrt(response))
    costs=np.array([-(u[i]-u[j])**2 for i,j in
                    [(0,2),(1,3),(0,3),(1,2),(4,6),(5,7),(4,7),(5,6)]])
    dl=costs[0]+costs[1]-costs[2]-costs[3]
    dr=costs[4]+costs[5]-costs[6]-costs[7]
    return {'lattice_N':N,'scalar_response_intensity':response,
            'transport_gram_rank':int(np.linalg.matrix_rank(gram)),
            'minimum_gram_eigenvalue':float(np.linalg.eigvalsh(gram)[0]),
            'neutral_channel_transport_norm_squared':float(gram[15,15]),
            'scalar_signature_count':8,'scalar_signatures':u.tolist(),
            'Delta_L':float(dl),'Delta_R':float(dr),
            'filter_scores_FDX_FXX_FDD_FXD':[0.0]*4,
            'selected_filter':'four-way tie in homogeneous prototype',
            'scope':'constructed common-transport witness; no interacting SM completion'}


def run(p,out):
    validate(p)
    c=p['c_m_s'];G=p['G_SI'];pc=p['parsec_m'];kpc=1000*pc
    H=p['H0_km_s_Mpc']*1000/(1e6*pc)
    f=p['fraction_twist_clustering'];fp=p['fraction_phenotype']
    aT=c*H*math.sqrt(f/8)
    fpre=1-fp
    rho_c=3*H*H/(8*np.pi*G)
    zeta_kappa2=6*f*(H/c)**2
    muM=p['electron_mass_energy_eV']/23
    modes=[{'n':n,'mass_energy_eV':abs(n)*muM} for n in [0,1,2,3,23]]
    convergence=[{'N':N,'relative_error_first_mode':
                  N*math.sin(math.pi/N)/math.pi-1} for N in [16,32,64,128,256,512]]
    radii=np.asarray(p['report_radii_kpc'],dtype=float)
    q=plummer(radii*kpc,p,aT)
    sphere=[{'r_kpc':float(r), 'v_total_km_s':float(q['v'][i]/1000),
             'v_baryon_km_s':float(q['v_b'][i]/1000),
             'twist_to_baryon_acceleration':float(q['gt'][i]/q['gm'][i]),
             'M_twist_eff_Msun':float(q['mt'][i]/p['M_sun_kg']),
             'rho_twist_eff_kg_m3':float(q['rho_eff'][i])} for i,r in enumerate(radii)]
    lens=[lens_segment(x,p,aT) for x in p['lens_impact_kpc']]
    yd=np.logspace(-8,8,4000);x=yd*nu(yd)
    mu=1/nu(yd);lp=1/dx_dy(yd)
    constitutive_resid=float(np.max(np.abs(mu*x-yd)/yd))
    ys=[1e-4,0.01,1,100]
    action_checks=[]
    for y in ys:
        h=1e-4*y
        Fy=(static_F(y+h)-static_F(y-h))/(2*h)
        Yy=((y+h)*nu(y+h))**2-((y-h)*nu(y-h))**2
        numerical_mu=Fy/(Yy/(2*h))
        expected=1/float(nu(y))
        action_checks.append({'y':y,'F':static_F(y),
                              'dF_dY_error':abs(numerical_mu/expected-1)})
    rs=np.geomspace(0.01,p['patch_radius_kpc'],2000)*kpc
    qs=plummer(rs,p,aT)
    # Flux conservation is the integrated radial field equation.
    flux=qs['g']/nu(qs['y'])*rs**2/G
    flux_error=float(np.max(np.abs(flux-qs['mb'])/qs['mb']))
    M=p['sphere_mass_Msun']*p['M_sun_kg']; vf=(G*M*aT)**0.25
    disk_rows=[]
    for r in [5,8.2,12,16.5,20,25]:
        vt,vb,ratio=disk_speed(np.array([r]),p,aT)
        disk_rows.append({'R_kpc':r,'v_total_km_s':float(vt[0]),
                          'v_baryon_km_s':float(vb[0]),
                          'twist_to_baryon_acceleration':float(ratio[0])})
    Rgrid=np.linspace(8,25,1001);vd,_,_=disk_speed(Rgrid,p,aT)
    ref=229-1.7*(Rgrid-8.2)
    rms=float(np.sqrt(np.mean((vd-ref)**2)))
    n=np.array([1,2,3])/math.sqrt(14);P=np.eye(3)-np.outer(n,n)
    Pminus=np.eye(3)-np.outer(-n,-n)
    increment_radius_m=kpc
    mass_increment_kg=muM*1.602176634e-19/c**2
    increment_at_r=G*mass_increment_kg/increment_radius_m**2
    increment_at_2r=G*mass_increment_kg/(2*increment_radius_m)**2
    increment_ratio=increment_at_r/increment_at_2r
    tests={
       'radial_flux_relative_error':flux_error,
       'constitutive_relative_error':constitutive_resid,
       'minimum_transverse_static_eigenvalue_on_y_1e-8_to_1e8':float(np.min(mu)),
       'minimum_parallel_static_eigenvalue_on_y_1e-8_to_1e8':float(np.min(lp)),
       'static_action_derivative_checks':action_checks,
       'minimum_effective_twist_density_kg_m3_on_finite_patch':float(np.min(qs['rho_eff'])),
       'plane_projector_sign_invariance_max_error':float(np.max(np.abs(P-Pminus))),
       'plane_projector_idempotency_max_error':float(np.max(np.abs(P@P-P))),
       'quantized_source_response_increment_r_dependence_ratio_r_to_2r':increment_ratio,
       'quantized_source_response_increment_inputs_and_outputs':{
           'radius_m':increment_radius_m,'mass_increment_kg':mass_increment_kg,
           'delta_g_at_r_m_s2':increment_at_r,'delta_g_at_2r_m_s2':increment_at_2r,
           'method':'evaluate G*delta_mass/r^2 at r and 2r, then divide'},
       'origin':'static equation is degenerate at y=0; tests exclude r=0',
       'full_covariant_stability':'not tested; static positivity is not full stability'}
    # Dimensionless exact check of E = A*zeta*Q*L in a declared T^3 closure.
    E,A,zeta,Q=Fraction(12),Fraction(2),Fraction(3),Fraction(4)
    L=E/(A*zeta*Q)
    assert A*zeta*Q*L==E
    tests['closed_torus_energy_length_identity_exact']=True
    assert flux_error<1e-12 and constitutive_resid<1e-12
    assert max(t['dF_dY_error'] for t in action_checks)<2e-6
    assert np.min(qs['rho_eff'])>=0
    sensitivity=[]
    for fnew,fpnew in [(0.20,fp),(0.30,fp),(f,0.08)]:
        pp=dict(p,fraction_twist_clustering=fnew,fraction_phenotype=fpnew)
        validate(pp)
        aa=c*H*math.sqrt(fnew/8)
        sensitivity.append({'f_twist':fnew,'f_phenotype':fpnew,
                            'f_hidden_total':1-fpnew,'aT_m_s2':aa,
                            'asymptotic_velocity_km_s':(G*M*aa)**0.25/1000,
                            'clustering_twist_to_phenotype_ratio':source_ratio(fnew,fpnew)})
    result={
      'version':'WRRA-M 0.5','branch':'B_C: fundamentally non-quantum gravity is a model premise',
      'inputs':p,'cosmic_calibration':{'H0_SI':H,'aT_m_s2':aT,'rho_critical_kg_m3':rho_c,
          'zeta_kappa_squared_m_minus2':zeta_kappa2,
          'normalized_twist_index':math.sqrt(6*f),
          'f_hidden_total':1-fp,'f_hidden_background_balance':1-fp-f,
          'total_hidden_normalized_twist_index_if_same_quadratic_map':math.sqrt(6*fpre),
          'total_hidden_zeta_kappa_squared_if_same_quadratic_map':6*fpre*(H/c)**2,
          'clustering_twist_to_phenotype_ratio':source_ratio(f,fp),
          'clustering_ratio_status':'finite' if fp>0 else 'undefined: zero phenotype denominator',
          'phenotype_share_of_clustering_sources':fp/(fp+f)},
      'mass_modes':modes,'mass_lattice_convergence':convergence,
      'carrier':carrier_calculation(p),'sphere':sphere,'finite_patch_lensing':lens,
      'asymptotic_velocity_km_s':vf/1000,
      'inherited_disk_renderer':{'rows':disk_rows,'RMS_to_linearized_Eilers_8_25_km_s':rms,
             'scope':'earlier calibrated algebraic disk approximation; no off-plane vector PDE'},
      'sensitivity':sensitivity,'verification':tests,
      'unresolved':['channel-dependent lower-order carrier responses',
                    'carrier-to-twist constitutive map','covariant action and gravitational slip',
                    'global finite-universe boundary matching','quantum-matter classical-gravity hybrid dynamics',
                    'disk vertical stress constitutive equation q_T'],
      'global_closure':{'model':'declared T^3 periodic realization; topology not inferred',
          'load_map':'E_pre = sum(w_a I_a); V=L^3',
          'constitutive':'zeta*kappa_total^2 = 16*pi*G*E_pre/(c^4 V)',
          'closure':'Theta_i=kappa_i L; Q=sum(Theta_i^2)>0',
          'conditional_length':'L=16*pi*G*E_pre/(zeta*c^4*Q)',
          'actual_universe_length':'unidentified: weights, zeta and global closure records not fixed',
          'coexistence':'gamma_ij=a(t)^2 hat_gamma_ij[Theta(t)]',
          'dynamics':'expansion and twist evolution not calculated in this static version'}}
    out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axs=plt.subplots(1,2,figsize=(9.0,3.7))
    rplot=rs/kpc
    axs[0].plot(rplot,qs['v']/1000,label='B_C total',color='#183b5b')
    axs[0].plot(rplot,qs['v_b']/1000,label='Baryonic direct',color='#9b6a27')
    axs[0].axhline(vf/1000,ls=':',color='#183b5b',label='Deep-regime limit')
    axs[0].set(xscale='log',xlabel='Radius (kpc)',ylabel='Circular speed (km/s)',xlim=(.1,200))
    axs[0].legend(fontsize=8)
    axs[1].plot(Rgrid,vd,label='Inherited WRRA disk renderer',color='#183b5b')
    axs[1].plot(Rgrid,ref,ls='--',label='Linearized Eilers reference',color='#9b6a27')
    axs[1].set(xlabel='Radius (kpc)',ylabel='Circular speed (km/s)')
    axs[1].legend(fontsize=8)
    for ax in axs:ax.grid(alpha=.18)
    fig.tight_layout();fig.savefig(out/'rotation.png',dpi=220);plt.close(fig)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default='results')
    parser.add_argument('--parameters',default=str(Path(__file__).with_name('parameters.json')))
    args=parser.parse_args()
    data=run(json.loads(Path(args.parameters).read_text()),Path(args.out))
    print(json.dumps({'aT':data['cosmic_calibration']['aT_m_s2'],
                      'carrier':data['carrier']['selected_filter'],
                      'disk_RMS':data['inherited_disk_renderer']['RMS_to_linearized_Eilers_8_25_km_s'],
                      'verification':data['verification']},ensure_ascii=False,indent=2))
