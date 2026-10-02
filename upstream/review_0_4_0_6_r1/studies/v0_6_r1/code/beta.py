"""Exact three-body tree recoil trace plus additive leading Sirlin outer RC.

Massless antineutrino, unpolarized neutron, no induced pseudoscalar/second-
class currents. The EM Coulomb kernel is the frozen point-charge kernel.
The leading outer RC is added to the leading allowed spectrum, so no claim
of a complete radiative-recoil O(alpha E/M) calculation is made.
"""
import math
import numpy as np
from scipy.special import roots_legendre,spence
I2=np.eye(2);Z2=np.zeros((2,2));pauli=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
G=np.array([np.block([[I2,Z2],[Z2,-I2]])]+[np.block([[Z2,s],[-s,Z2]]) for s in pauli],dtype=complex)
G5=1j*G[0]@G[1]@G[2]@G[3];I4=np.eye(4);METRIC=np.array([1.,-1.,-1.,-1.])
SIG=np.array([[.5j*(G[mu]@G[nu]-G[nu]@G[mu]) for nu in range(4)] for mu in range(4)])

def slash(v):return np.einsum('...m,m,mij->...ij',v,METRIC,G)

def coulomb(E,me,alpha):
    p=np.sqrt(E*E-me*me)
    if alpha==0:return np.ones_like(p)
    x=2*math.pi*alpha*E/p
    return x/(-np.expm1(-x))

def sirlin_g(E,E0,me,mp):
    b=np.sqrt(1-me*me/(E*E));a=np.arctanh(b);d=E0-E
    return 3*math.log(mp/me)-.75+4*(a/b-1)*(np.log(2*d/me)+d/(3*E)-1.5)-4/b*spence(1-2*b/(1+b))+a/b*(2+2*b*b+d*d/(6*E*E)-4*a)

def trace_grid(E,z,mp,mn,me,ff,weak_magnetism=True,finite_slopes=True):
    E,z=np.broadcast_arrays(E,z);shape=E.shape;E=E.ravel();z=z.ravel();N=len(E)
    p=np.sqrt(E*E-me*me);D=mn-E+p*z;k=(mn*mn+me*me-mp*mp-2*mn*E)/(2*D)
    pe=np.column_stack((E,np.zeros(N),np.zeros(N),p))
    nu=np.column_stack((k,k*np.sqrt(np.maximum(1-z*z,0)),np.zeros(N),k*z))
    pn=np.tile([mn,0,0,0],(N,1));pp=pn-pe-nu;q=pp-pn
    t=np.sum(q*q*METRIC,axis=1)*1e-6 # timelike invariant GeV2
    f1=np.full(N,ff['F1V0']);f2=np.full(N,ff['F2V0'] if weak_magnetism else 0.);ga=np.full(N,ff['GA0'])
    if finite_slopes:
        f1-=ff['F1V_prime']*t;ga-=ff['GA_prime']*t
        if weak_magnetism:f2-=ff['F2V_prime']*t
    vertex=np.einsum('n,mij->nmij',f1,G)-np.einsum('n,mij->nmij',ga,G@G5)
    vertex+=np.einsum('n,nv,v,mvij->nmij',f2,q,METRIC,1j*SIG)/(mp+mn)
    ps=slash(pp)+mp*I4;ns=slash(pn)+mn*I4;es=slash(pe)+me*I4;vs=slash(nu)
    left=np.array([METRIC[m]*G[m]@(I4-G5) for m in range(4)])
    total=np.zeros(N,dtype=complex)
    for mu in range(4):
        for nv in range(4):
            bar=G[0]@vertex[:,nv].conj().transpose(0,2,1)@G[0]
            ht=.5*np.trace(ps@vertex[:,mu]@ns@bar,axis1=1,axis2=2)
            lt=np.trace(es@left[mu]@vs@left[nv],axis1=1,axis2=2)
            total+=ht*lt
    residual=float(np.max(abs(np.sum(pp*pp*METRIC,axis=1)-mp*mp)))
    return (p*k/D*total.real).reshape(shape),{'on_shell_residual_MeV2':residual,'minimum_trace':float(total.real.min()),'maximum_imaginary_trace':float(np.max(abs(total.imag))),'timelike_t_range_GeV2':[float(t.min()),float(t.max())]}

def calculate(inp,ff,ne=80,nz=12):
    mp,mn,me=(inp['masses'][k] for k in ('proton','neutron','electron'));alpha=inp['weak_constants']['alpha_em'];E0=mn-mp;Em=(mn*mn+me*me-mp*mp)/(2*mn)
    x,w=roots_legendre(ne);u=(x+1)/2;E=me+(Em-me)*u*u;ew=w/2*2*(Em-me)*u
    z,zw=roots_legendre(nz);F=coulomb(E,me,alpha)
    import inherited_v0_3_r1 as old
    Iparent=me**5*old.phase(mn-mp-me,me,alpha)
    norm=64*mn*(1+3*ff['GA0']**2)*Iparent
    rows=[];details={};spectra={}
    for name,wm,slopes in [('recoil_only',False,False),('recoil_weak_magnetism',True,False),('recoil_finite_currents',True,True)]:
        kernel,info=trace_grid(E[:,None],z[None,:],mp,mn,me,ff,wm,slopes)
        raw=(kernel@zw)*F/(64*mn*(1+3*ff['GA0']**2))
        factor=float(ew@raw/Iparent);rows.append({'case':name,'rate_ratio_to_parent_allowed':factor});details[name]=info;spectra[name]=raw
    lead=np.sqrt(E*E-me*me)*E*(Em-E)**2*F
    outer=lead*(alpha/(2*math.pi))*sirlin_g(E,Em,me,mp) if alpha else np.zeros_like(E)
    delta_outer=float(ew@outer/Iparent);tree=rows[-1]['rate_ratio_to_parent_allowed'];inner=inp['charge_completion']['inner_delta_R_V']
    full=(tree+delta_outer)*(1+inner)
    parent_strength=inp['inherited']['kappa']**2*ff['activity_R'];wc=inp['weak_constants']
    allowed_rate=parent_strength*(wc['GF_GeV_minus2']*1e-6)**2*wc['Vud']**2*(1+3*ff['GA0']**2)*Iparent/(2*math.pi**3*wc['hbar_MeV_s'])
    frozen_life=1/(allowed_rate*full);target=inp['inherited']['neutron_mean_life_s']
    kap=inp['inherited']['kappa']*math.sqrt(frozen_life/target)
    refit_life=1/(allowed_rate*full*(kap/inp['inherited']['kappa'])**2)
    corrected=spectra['recoil_finite_currents']+outer;area=float(ew@corrected);prob=ew*corrected/area
    # Photon-inclusive outer RC changes the electron spectrum, not the stored
    # tree event kinematics or a fully exclusive e-nu angular distribution.
    return {'parent_allowed_integral_MeV5':Iparent,'endpoint_parent_total_electron_MeV':E0,'endpoint_recoil_total_electron_MeV':Em,
        'tree_cases':rows,'outer_rate_increment_relative_parent':delta_outer,'inner_delta_R_V':inner,'full_rate_ratio_relative_parent':full,
        'parent_allowed_rate_s_minus1':allowed_rate,'frozen_parent_kappa_lifetime_s':frozen_life,
        'separately_refitted_kappa':kap,'refitted_lifetime_s':refit_life,
        'parent_kappa_squared_R':parent_strength,'refitted_kappa_squared_R':kap*kap*ff['activity_R'],
        'electron_spectrum':{'energy_MeV':E.tolist(),'quadrature_probability':prob.tolist(),'density_per_MeV':(corrected/area).tolist(),'mean_kinetic_energy_MeV':float(prob@(E-me))},
        'trace_diagnostics':details,'finite_slope_scheme':'First-order analytic continuation Q2=-t. No timelike fit or pion-pole completion.',
        'radiative_scope':'Leading outer electron-inclusive Sirlin RC added to tree recoil spectrum, separate fixed-reference inner RC. Mixed radiative recoil, higher QED and induced pseudoscalar omitted.'}
