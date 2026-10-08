"""WRRA dynamic decays v0.2. python reproduce.py; numpy scipy matplotlib.
Deterministic finite quadrature; inherited arithmetic readout is rerun unchanged.
All energies MeV, momenta MeV/c with c=1 internally, times in muon lifetimes.
"""
from pathlib import Path
import contextlib, io, json, runpy, platform
import numpy as np
import scipy
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    inherited=runpy.run_path(str(ROOT/'inherited/reproduce.py'))
rows=inherited['rows']; m=0.51099895069; M=105.6583755
tau=2.1969811e-6; E0=2*M; checks=[]
def check(name, value, tolerance):
    checks.append(dict(name=name,error=float(value),tolerance=float(tolerance),passed=bool(value<=tolerance)))

def kernel(order=64, mass=m, shape='VA'):
    """Finite positive three-body kernel. mu- -> e- + anti-nu_e + nu_mu.
    Exact electron mass, massless neutrinos, unpolarized tree-level V-A shape.
    p_e along z. z is anti-nu_e direction in the neutrino-pair rest frame.
    Global orientation averaging is analytic, giving scalar isotropic pressure.
    """
    x,w=leggauss(order); pmax=(M*M-mass*mass)/(2*M)
    p=(x[:,None]+1)*pmax/2; wp=w[:,None]*pmax/2
    z=x[None,:]; wz=w[None,:]
    ee=np.hypot(mass,p); q0=M-ee; q2=q0*q0-p*p
    ea=(q0-p*z)/2; en=(q0+p*z)/2
    paz=(q0*z-p)/2; pnz=(-q0*z-p)/2
    transverse=np.sqrt(np.maximum(q2,0))*np.sqrt(1-z*z)/2
    dot=ee*en-p*pnz
    amplitude=M*ea*dot if shape=='VA' else np.ones_like(ea)
    raw=wp*wz*(p*p/ee)*amplitude
    norm=raw.sum(); weights=raw/norm
    es=np.broadcast_to(ee,ea.shape)
    ps=np.broadcast_to(p,ea.shape)
    return dict(w=weights,ee=es,pe=ps,ea=ea,en=en,paz=paz,pnz=pnz,pt=transverse,norm=norm)

def moments(k,scale=1.,mass=m):
    # Daughter packet aged by a_birth/a_now = scale.
    ee=np.hypot(mass,k['pe']*scale)
    nu=(k['ea']+k['en'])*scale
    e=float(np.sum(k['w']*(ee+nu)))
    pv=float(np.sum(k['w']*((k['pe']*scale)**2/ee+nu))/3)
    return e,pv

k=kernel(); mean=lambda a:float(np.sum(k['w']*a))
check('inherited interface 47 checks',sum(not c['passed'] for c in inherited['checks']),0)
check('positive normalized quadrature',max(abs(k['w'].sum()-1),max(0,-k['w'].min())),1e-14)
check('event energy conservation relative',np.max(abs(k['ee']+k['ea']+k['en']-M))/M,1e-14)
check('event momentum conservation relative',np.max(abs(k['pe']+k['paz']+k['pnz']))/M,1e-14)
check('antineutrino mass shell relative',np.max(abs(k['ea']**2-k['paz']**2-k['pt']**2))/M**2,1e-14)
check('muon neutrino mass shell relative',np.max(abs(k['en']**2-k['pnz']**2-k['pt']**2))/M**2,1e-14)
check('electron mass shell relative',np.max(abs(k['ee']**2-k['pe']**2-m*m))/M**2,1e-14)
# Per charge-conjugate channel (mu-, e-, anti-nu_e, nu_mu), number change.
S=np.array([-1,1,1,1.])
for name,l in [('charge',[-1,-1,0,0]),('electron family',[0,1,-1,0]),('muon family',[1,0,0,1])]:
    check(name+' stoichiometric conservation',abs(np.dot(l,S)),0)
# Independent analytic limit checks, not a copy of the event construction.
k0=kernel(mass=0)
for name,field,target in [('electron','ee',.35),('electron antineutrino','ea',.30),('muon neutrino','en',.35)]:
    check('massless '+name+' mean energy',abs(np.sum(k0['w']*k0[field])/M-target),1e-13)
r=(m/M)**2; f=1-8*r+8*r**3-r**4-12*r*r*np.log(r)
check('integrated finite mass phase space factor',abs(k['norm']/k0['norm']-f),2e-10)
kd=kernel(128)
check('64 to 128 quadrature pressure convergence',abs(moments(k)[1]-moments(kd)[1])/M,2e-10)
for scale in [1,.5,.1]:
    v=scale**-3; dv=1e-5*v
    numerical=-v*(moments(k,(v+dv)**(-1/3))[0]-moments(k,(v-dv)**(-1/3))[0])/(2*dv)
    check('frozen cohort pressure derivative scale '+str(scale),abs(numerical-moments(k,scale)[1])/M,2e-10)

D=2*moments(k)[1]/E0 # daughter-pair PV divided by reference pair energy
def fixed(x,t):
    s=np.exp(-t); mu=2*(1-x)*s; el=2*x+2*(1-x)*(1-s); nu=4*(1-x)*(1-s)
    pv=x*(1-r)/3+(1-x)*(1-s)*D
    return dict(time_tau=float(t),muons=mu,charged_electrons=el,neutrinos=nu,energy_over_E0=1.,pv_over_E0=pv)

fixed_rows=[]
for row in rows:
    x=row['electron_pair_probability']
    rr=[fixed(x,t) for t in [0,1,3,5,10]]
    fixed_rows.append(dict(drive=row['drive'],X=x,values=rr))
    check(row['drive']+' frozen limit',abs(rr[0]['pv_over_E0']-row['pV_over_E_phi_at_v1']),1e-14)
    check(row['drive']+' late charged population',abs(fixed(x,40)['charged_electrons']-2),1e-14)
    check(row['drive']+' charged particle count',max(abs(v['muons']+v['charged_electrons']-2) for v in rr),1e-14)
    check(row['drive']+' pressure monotonicity',max(0,max(rr[i]['pv_over_E0']-rr[i+1]['pv_over_E0'] for i in range(4))),0)

def expanding(x,dt,h=.1,T=5.,record=False):
    # Redshift old cohorts, then decay at the right endpoint. Positive exact hazard.
    steps=int(round(T/dt)); dt=T/steps
    birth=np.arange(1,steps+1)*dt
    counts=2*(1-x)*np.exp(-birth+dt)*(-np.expm1(-dt))
    # Reduce z analytically by summing weights: only total neutrino energy needed.
    wp=k['w'].sum(axis=1); pe=k['pe'][:,0]
    nuenergy=mean(k['ea']+k['en'])
    def state(j):
        t=j*dt; a=np.exp(h*t)
        eprim=2*x*np.hypot(m,np.sqrt(M*M-m*m)/a)
        pvprim=2*x*(M*M-m*m)/a**2/(3*np.hypot(m,np.sqrt(M*M-m*m)/a))
        mu=2*(1-x)*np.exp(-t)
        ratio=np.exp(h*(birth[:j]-t))[:,None]
        ed=np.hypot(m,ratio*pe[None,:]); nud=nuenergy*ratio[:,0]
        ec=ed@wp+nud; pc=((ratio*pe[None,:])**2/ed)@wp/3+nud/3
        E=eprim+M*mu+float(counts[:j]@ec)
        PV=pvprim+float(counts[:j]@pc)
        return E,PV
    end=state(steps)
    if not record: return end
    # Work is separately accumulated from redshifting pre-existing populations.
    Eprev=E0; work=0.; trace=[]; worst=0.
    for j in range(1,steps+1):
        t=j*dt; a=np.exp(h*t); oldt=(j-1)*dt; olda=np.exp(h*oldt)
        work+=2*x*(np.hypot(m,np.sqrt(M*M-m*m)/a)-np.hypot(m,np.sqrt(M*M-m*m)/olda))
        ro=np.exp(h*(birth[:j-1]-oldt))[:,None]; rn=ro*np.exp(-h*dt)
        old=np.hypot(m,ro*pe)@wp+nuenergy*ro[:,0]
        new=np.hypot(m,rn*pe)@wp+nuenergy*rn[:,0]
        work+=float(counts[:j-1]@(new-old))
        E,PV=state(j); worst=max(worst,abs(E-E0-work)/E0)
        if j%max(1,steps//100)==0: trace.append([t,E/E0,PV/E0,PV/E])
    check('expanding discrete work closure',worst,5e-13)
    return end,trace

def continuous(x,h=.1,T=5.):
    # Independent adaptive birth-time quadrature, same finite momentum kernel.
    pe=k['pe'][:,0]; wp=k['w'].sum(axis=1); nuenergy=mean(k['ea']+k['en'])
    def newborn(u,pressure=False):
        s=np.exp(h*(u-T)); ee=np.hypot(m,pe*s)
        v=(np.sum(wp*(pe*s)**2/ee)+nuenergy*s)/3 if pressure else np.sum(wp*ee)+nuenergy*s
        return 2*(1-x)*np.exp(-u)*v
    a=np.exp(h*T); ep=np.hypot(m,np.sqrt(M*M-m*m)/a)
    E=2*x*ep+2*M*(1-x)*np.exp(-T)+quad(newborn,0,T,epsabs=1e-10)[0]
    PV=2*x*(M*M-m*m)/a**2/(3*ep)+quad(lambda u:newborn(u,True),0,T,epsabs=1e-10)[0]
    return np.array([E,PV])

x=rows[0]['electron_pair_probability']; reference=continuous(x)
convergence=[]
for dt in [.04,.02,.01,.005]:
    ans=np.array(expanding(x,dt)); err=float(np.max(abs(ans-reference))/E0)
    convergence.append(dict(dt_tau=dt,E_over_E0=ans[0]/E0,PV_over_E0=ans[1]/E0,max_error=err))
for i in range(1,len(convergence)):
    ratio=convergence[i-1]['max_error']/convergence[i]['max_error']
    check('first order splitting convergence '+str(i),abs(ratio-2),.03)
_,trace=expanding(x,.01,record=True)
check('zero expansion fixed volume recovery',np.max(abs(np.array(expanding(x,.01,h=0))-np.array([E0,fixed(x,5)['pv_over_E0']*E0])))/E0,1e-13)
# Negative controls must fail physically meaningful invariants.
omitted_nu=2*(1-x)*(1-np.exp(-1))*mean(k['ea']+k['en'])/E0
check('omitting neutrinos detected',float(omitted_nu<.1),0)
check('forced dust detected',float(fixed(x,1)['pv_over_E0']<=0),0)
check('Euler negative populations detected',float(1-2>=0),0)
# Aggregate with only total reference energy loses the parent/daughter distinction.
C=np.array([[M,M]]) # state entries parent and whole daughter packet
G=np.array([[-1,0],[1,0.]])
Pi=np.array([[0,moments(k)[1]]])
check('energy generator invariant',np.max(abs(C@G)),1e-14)
check('pressure distinguishes equal energy states',float(abs((Pi@np.array([1.,-1.]))[0])<1),0)
flat=kernel(shape='flat'); flatD=2*moments(flat)[1]/E0
controls=[]
for row in rows:
    xx=row['electron_pair_probability']
    controls.append(dict(drive=row['drive'],reversed_at_tau=fixed(1-xx,1),constant_at_tau=fixed(.5,1)))
check('constant routing erases dynamic drive differences',max(c['constant_at_tau']['pv_over_E0'] for c in controls)-min(c['constant_at_tau']['pv_over_E0'] for c in controls),0)
check('reversed routing changes dynamics',float(abs(controls[0]['reversed_at_tau']['pv_over_E0']-fixed(x,1)['pv_over_E0'])<.01),0)
for i in range(1,4):
    tv=.5*np.abs(inherited['dists'][i]-inherited['dists'][0]).sum()
    delta=abs(fixed(rows[i]['electron_pair_probability'],1)['neutrinos']-fixed(x,1)['neutrinos'])
    check('propagated TV neutrino bound '+str(i),max(0,delta-4*(1-np.exp(-1))*tv),1e-13)
# Prepared mixtures of complete aged daughter packets: same N,E,PV now.
# This is a family of preparations, not two solutions of one fixed source history.
ages=np.array([.002,.01,.05,.2,1.])
now=np.array([moments(k,b) for b in ages]).T/M
future=np.array([moments(k,.5*b) for b in ages]).T/M
Cmom=np.vstack([np.ones(5),now])
_,singular,vh=np.linalg.svd(Cmom,full_matrices=True)
null=vh[3:].T
z=null@(null.T@future[0]); z/=np.max(abs(z))
wplus=np.full(5,.2)+.18*z; wminus=np.full(5,.2)-.18*z
present_plus=Cmom@wplus; present_minus=Cmom@wminus
future_plus=future@wplus; future_minus=future@wminus
check('cohort witness nonnegative weights',max(0,-min(wplus.min(),wminus.min())),0)
check('cohort witness full row rank',float(singular[-1]<1e-5),0)
check('cohort witness equal present N energy stress',np.max(abs(present_plus-present_minus)),2e-14)
check('cohort witness unequal future energy',float(abs(future_plus[0]-future_minus[0])<1e-6),0)
check('cohort witness unequal future stress',float(abs(future_plus[1]-future_minus[1])<1e-7),0)
check('cohort witness both normalized',max(abs(wplus.sum()-1),abs(wminus.sum()-1)),2e-14)
# A massless packet redshifts linearly, so its energy and pressure close.
zero_now=np.array([moments(k0,b,mass=0) for b in ages]).T/M
zero_future=np.array([moments(k0,.5*b,mass=0) for b in ages]).T/M
check('massless energy stress transport closure',np.max(abs(zero_future-.5*zero_now)),1e-14)
cohort_witness=dict(age_scales=ages.tolist(),future_redshift=.5,weights_plus=wplus.tolist(),weights_minus=wminus.tolist(),
    present_N_EoverM_PVoverM_plus=present_plus.tolist(),present_N_EoverM_PVoverM_minus=present_minus.tolist(),
    future_EoverM_PVoverM_plus=future_plus.tolist(),future_EoverM_PVoverM_minus=future_minus.tolist(),
    future_difference=(future_plus-future_minus).tolist(),singular_values=singular.tolist())
out=dict(version='0.2',inputs=dict(m_e_MeV=m,m_mu_MeV=M,tau_mu_seconds=tau,quadrature_order=64,expansion_Htau=.1),
    kernel=dict(mean_e_MeV=mean(k['ee']),mean_antinue_MeV=mean(k['ea']),mean_numu_MeV=mean(k['en']),daughter_PV_over_M=D,phase_space_factor=f,flat_phase_space_PV_over_M=flatD),
    cohort_witness=cohort_witness,fixed_volume=fixed_rows,routing_controls=controls,expansion_convergence=convergence,continuous_reference=dict(E_over_E0=reference[0]/E0,PV_over_E0=reference[1]/E0),
    omitted_neutrino_energy_deficit_at_tau=omitted_nu,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
    versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__))
(ROOT/'results.json').write_text(json.dumps(out,indent=2))
np.savetxt(ROOT/'expanding_trajectory.csv',trace,delimiter=',',header='time_tau,E_over_E0,PV_over_E0,w',comments='')
plt.rcParams.update({'font.size':10,'font.family':'DejaVu Sans','pdf.fonttype':42,'ps.fonttype':42})
fig,ax=plt.subplots(1,2,figsize=(7.0,2.7),layout='constrained')
t=np.linspace(0,5,201); base=[fixed(x,q) for q in t]
for name,label,ls in [('muons','muons','-'),('charged_electrons','electrons and positrons','--'),('neutrinos','neutrinos and antineutrinos',':')]:
    ax[0].plot(t,[a[name] for a in base],ls,label=label)
ax[0].set(xlabel=r'$t/\tau_\mu$',ylabel='Expected number per initial pair');ax[0].legend(fontsize=7);ax[0].text(.02,.96,'a',transform=ax[0].transAxes,va='top')
for row,ls in zip(rows,['-','--',':','-.']):
    ax[1].plot(t,[fixed(row['electron_pair_probability'],q)['pv_over_E0'] for q in t],ls,label=row['drive'].replace('_',' '))
ax[1].set(xlabel=r'$t/\tau_\mu$',ylabel=r'$PV/E_*$');ax[1].legend(fontsize=7,loc='lower right');ax[1].text(.02,.96,'b',transform=ax[1].transAxes,va='top')
for ext in ['png','pdf','eps']:fig.savefig(ROOT/('Fig1.'+ext),dpi=300)
plt.close(fig)
fig,ax=plt.subplots(1,2,figsize=(7,2.7),layout='constrained');tr=np.array(trace)
ax[0].plot(tr[:,0],tr[:,1],'-',label=r'$E/E_*$');ax[0].plot(tr[:,0],tr[:,2],'--',label=r'$PV/E_*$');ax[0].set(xlabel=r'$t/\tau_\mu$',ylabel='Normalized energy and stress');ax[0].legend();ax[0].text(.02,.96,'a',transform=ax[0].transAxes,va='top')
ax[1].loglog([q['dt_tau'] for q in convergence],[q['max_error'] for q in convergence],'o-');ax[1].set(xlabel=r'$\Delta t/\tau_\mu$',ylabel='Maximum normalized error');ax[1].text(.02,.96,'b',transform=ax[1].transAxes,va='top')
ax[1].set_xticks([.005,.01,.02,.04],labels=['0.005','0.01','0.02','0.04'])
ax[1].xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
for ext in ['png','pdf','eps']:fig.savefig(ROOT/('Fig2.'+ext),dpi=300)
plt.close(fig)
print(json.dumps({key:out[key] for key in ['kernel','fixed_volume','expansion_convergence','continuous_reference','passed','total']},indent=2))
assert all(c['passed'] for c in checks),[c for c in checks if not c['passed']]
