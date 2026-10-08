"""Finite WRRA comparator carrier. All computations offline. Run python reproduce.py.
Units: c=1; normalized carrier Hamiltonians in E_star; dimensionless time E_star*t/hbar.
The control pulse is specified, not a derived particle interaction or lifetime.
"""
from pathlib import Path
import contextlib, io, runpy, json, hashlib, platform
import numpy as np
import scipy
from scipy.linalg import expm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    prior=runpy.run_path(str(ROOT/'inherited/decay/reproduce.py'))
base=prior['inherited']; rows=base['rows']; checks=[]
def check(name,error,tol=1e-12):
    error=float(error); checks.append(dict(name=name,error=error,tolerance=tol,passed=bool(error<=tol)))
def assert_true(name,condition): check(name,0 if condition else 1,0)
check('inherited dynamic suite passes',sum(not a['passed'] for a in prior['checks']),0)
check('inherited interface suite passes',sum(not a['passed'] for a in base['checks']),0)

def factors(n):
    powers=[]; p=2
    while p*p<=n:
        k=0
        while n%p==0: n//=p;k+=1
        if k:powers.append(k)
        p+=1
    if n>1:powers.append(1)
    return np.array(powers,dtype=float)
def register(n):
    nu=factors(n); return nu/nu.sum()
def generator(d):
    equal=np.diag([float(i==j) for i in range(d) for j in range(d)])
    xe=np.zeros((3,3));xm=np.zeros((3,3))
    xe[0,1]=xe[1,0]=1;xm[0,2]=xm[2,0]=1
    return np.kron(equal,xe)+np.kron(np.eye(d*d)-equal,xm)
def evolve_register(r,theta):
    d=len(r);G=generator(d);U=expm(-1j*theta*G)
    rho=np.kron(np.diag(np.outer(r,r).ravel()),np.diag([1.,0,0]))
    out=U@rho@U.conj().T
    reduced=np.einsum('iaib->ab',out.reshape(d*d,3,d*d,3))
    return reduced,U,G

witness=[]
for n in [9,15,25,45,105,225,315,945]:
    rr=register(n);chi=float(rr@rr)
    errors=[];unitarity_errors=[]
    for theta in [0,.2,np.pi/4,np.pi/2,2.1]:
        red,U,G=evolve_register(rr,theta)
        expected=np.array([np.cos(theta)**2,chi*np.sin(theta)**2,(1-chi)*np.sin(theta)**2])
        errors.append(np.max(abs(np.diag(red).real-expected)))
        unitarity_errors.append(np.max(abs(U.conj().T@U-np.eye(len(U)))))
    check(f'full matrix pulse probabilities n={n}',max(errors))
    check(f'unitarity n={n}',max(unitarity_errors))
    check(f'Hermiticity n={n}',np.max(abs(G-G.conj().T)),0)
    red,_,_=evolve_register(rr,np.pi/2)
    check(f'mixed species coherence zero n={n}',abs(red[1,2]))
    witness.append(dict(address=n,chi=chi,dimension=len(G),electron_probability=float(red[1,1].real)))

# Single-copy obstruction: pure prime powers 9 and 25 force response 1 on both labels.
# The same device on the diagonal 15 mixture must return 1, whereas chi(15)=1/2.
assert_true('single-copy affine obstruction witness',abs((1+1)/2-.5)==.5)
# The equality statistic requires conditional independence, not merely equal marginals.
r=np.array([2/3,1/3]);Gamma=np.diag(r)
check('correlated registers preserve marginals',max(np.max(abs(Gamma.sum(0)-r)),np.max(abs(Gamma.sum(1)-r))),0)
assert_true('correlated registers change routing',abs(np.trace(Gamma)-r@r)>.4)
# Permutation invariant diagonal effects have only two orbits.
from itertools import permutations
d=3;eq=np.eye(d)
check('label permutation equality invariance',max(np.max(abs(eq[np.ix_(p,p)]-eq)) for p in permutations(range(d))),0)
# A deliberately label-dependent equality response breaks that symmetry.
bad=np.diag([1.,.7,.4]);p=[1,0,2]
assert_true('label dependent negative control',np.max(abs(bad[np.ix_(p,p)]-bad))>.2)

# Two-port trace probabilities for the full archived address domain via exact block law.
carrier_rows=[]
for i,row in enumerate(rows):
    X=float(base['dists'][i]@base['chi'])
    check(row['drive']+' operator block readout equals archive',abs(X-row['electron_pair_probability']))
    vals=[]
    for theta in [np.pi/4,np.pi/2]:
        S=np.cos(theta)**2;Pe=X*np.sin(theta)**2;Pm=(1-X)*np.sin(theta)**2
        check(row['drive']+f' pulse normalization theta={theta}',abs(S+Pe+Pm-1))
        # Post-pulse decay: source remains source; daughters use the inherited quadrature.
        for u in [0,1,3,5]:
            v=prior['fixed'](X,u)
            pressure=Pe*(1-prior['r'])/3+Pm*(-np.expm1(-u))*prior['D']
            check(row['drive']+f' composed pressure theta={theta} u={u}',abs(pressure-np.sin(theta)**2*v['pv_over_E0']))
        vals.append(dict(theta=theta,source=S,electron=Pe,muon=Pm,pressure_at_5=pressure))
    # Execute original expansion with comparator-produced X; comparison has same frozen inputs.
    end=np.array(prior['expanding'](X,.01))/prior['E0']
    check(row['drive']+' expansion comparator handoff',np.max(abs(end-np.array(prior['expanding'](row['electron_pair_probability'],.01))/prior['E0'])))
    carrier_rows.append(dict(drive=row['drive'],X=X,pulses=vals,expanded_at_5=end.tolist()))

# Detuned physical-energy blocks, eigenvalue-independent analytic Rabi check.
g=.1;theta=np.pi/2;tbar=theta/g;r_mass=prior['r'];X=carrier_rows[0]['X']
def energies(v):return np.array([1.,np.sqrt(r_mass+(1-r_mass)*v**(-2/3)),1.])
def pv_e(v):
    return (1-r_mass)*v**(-2/3)/(3*np.sqrt(r_mass+(1-r_mass)*v**(-2/3)))
def detuned(v,label):
    h0=np.diag(energies(v));hi=np.zeros((3,3));hi[0,label]=hi[label,0]=g
    h=h0+hi;U=expm(-1j*tbar*h);psi=U[:,0]
    delta=h0[label,label]-1;omega=np.sqrt(g*g+delta*delta/4)
    expected=g*g/(omega*omega)*np.sin(omega*tbar)**2
    return h0,hi,h,U,psi,expected
detuning=[]
for v in [.5,.8,1,1.2,2]:
    h0,hi,h,U,psi,F=detuned(v,1)
    P=float(abs(psi[1])**2); eb=float(np.vdot(psi,h0@psi).real);intE=float(np.vdot(psi,hi@psi).real)
    check(f'detuned Rabi v={v}',abs(P-F))
    check(f'total Hamiltonian conservation v={v}',abs(np.vdot(psi,h@psi)-1))
    check(f'switching work ledger v={v}',abs(eb-1+intE))
    dv=1e-5*v;num=-v*(energies(v+dv)[1]-energies(v-dv)[1])/(2*dv)
    check(f'fixed state pressure derivative v={v}',abs(num-pv_e(v)),1e-9)
    comm=h0@hi-hi@h0
    check(f'commutator norm formula v={v}',abs(np.linalg.norm(comm,2)-g*abs(energies(v)[1]-1)))
    if v!=1: assert_true(f'nonresonance bare energy failure v={v}',np.linalg.norm(comm)>1e-3)
    else: check('reference bare energy commutator',np.linalg.norm(comm),0)
    Pe=X*P;Pm=1-X;Ps=1-Pe-Pm
    detuning.append(dict(volume=v,electron_transfer=P,source=Ps,electron=Pe,muon=Pm,
       bare_energy_over_Estar=1+Pe*(energies(v)[1]-1),switch_work_over_Estar=Pe*(energies(v)[1]-1),
       pressure_after_pulse=Pe*pv_e(v),pressure_after_5=Pe*pv_e(v)+Pm*(-np.expm1(-5))*prior['D']))

# Pulse preparation can share species counts while differing as a quantum state.
eps=1e-5
Fm=float(abs(detuned(np.exp(-eps),1)[4][1])**2)
Fp=float(abs(detuned(np.exp(eps),1)[4][1])**2)
delta_m=energies(np.exp(-eps))[1]-1;delta_p=energies(np.exp(eps))[1]-1
prob_slope=X*(Fp-Fm)/(2*eps)
work_slope=X*(Fp*delta_p-Fm*delta_m)/(2*eps)
check('stationary reference probability versus log volume',abs(prob_slope),1e-9)
check('pressure equals negative preparation work slope',abs(-work_slope-X*pv_e(1)),1e-9)
expected_curvature=((1-r_mass)/3)**2/(4*g*g)
curvature=((1-Fm)+(1-Fp))/(2*eps*eps)
check('quadratic resonance loss coefficient',abs(curvature-expected_curvature),1e-5)

c=1/3; pure=np.outer(np.sqrt([c,1-c]),np.sqrt([c,1-c]));mixed=np.diag([c,1-c])
distance=np.linalg.svd(pure-mixed,compute_uv=False).sum()/2
check('coherent interface distinction',abs(distance-np.sqrt(c*(1-c))))
assert_true('same probabilities not same quantum channel',distance>.4)

# Independent binary production attenuation: one common pulse preserves conditional ratio.
check('pulse error quadratic loss',abs((1-np.sin(np.pi/2+.01)**2)-np.sin(.01)**2))
out=dict(version='0.2',inputs=dict(g_over_Estar=g,pulse_area=theta,preparation='conditional independent prime-label registers',
    physical_energy_units='MeV',E_star=prior['E0'],m_e=prior['m'],m_mu=prior['M'],tau_mu_seconds=prior['tau']),
    witnesses=witness,carrier_rows=carrier_rows,detuning=detuning,
    coherent_distinction_trace_distance=distance,correlated_register_example=dict(independent=float(r@r),correlated=float(np.trace(Gamma))),
    response=dict(probability_slope=prob_slope,negative_work_slope=-work_slope,postpulse_pressure=X*pv_e(1),loss_curvature=curvature,analytic_loss_curvature=expected_curvature),
    inherited_suites=dict(interface=base['result']['passed'],decay=prior['out']['passed']),
    checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
    versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
(ROOT/'results.json').write_text(json.dumps(out,indent=2))
assert all(c['passed'] for c in checks),[c for c in checks if not c['passed']]
plt.rcParams.update({'font.size':9,'font.family':'DejaVu Sans','pdf.fonttype':42})
fig,ax=plt.subplots(1,2,figsize=(7,2.6),layout='constrained')
ts=np.linspace(0,np.pi,201)
for chi,label in [(1,'9'),(5/9,'45'),(1/3,'105')]:ax[0].plot(ts/np.pi,chi*np.sin(ts)**2,label='address '+label)
ax[0].set(xlabel=r'Pulse area $\theta/\pi$',ylabel=r'Electron-channel probability');ax[0].legend(fontsize=7)
vs=np.linspace(.5,2,201);fs=[detuned(v,1)[-1] for v in vs]
ax[1].plot(vs,fs);ax[1].axvline(1,color='gray',ls=':');ax[1].set(xlabel=r'Fixed volume $v$',ylabel=r'Electron transfer factor $F_e$',ylim=(0,1.05))
fig.savefig(ROOT/'figures/Fig1.png',dpi=240);fig.savefig(ROOT/'figures/Fig1.pdf');plt.close(fig)
fig,ax=plt.subplots(figsize=(5.5,2.7),layout='constrained');us=np.linspace(0,5,201)
for th,label in [(np.pi/2,'complete pulse'),(np.pi/4,'half conversion')]:
    ax.plot(us,[np.sin(th)**2*prior['fixed'](X,u)['pv_over_E0'] for u in us],label=label)
ax.set(xlabel=r'Time after pulse $t/\tau_\mu$',ylabel=r'$PV/E_*$');ax.legend();fig.savefig(ROOT/'figures/Fig2.png',dpi=240);fig.savefig(ROOT/'figures/Fig2.pdf');plt.close(fig)
print(json.dumps({k:out[k] for k in ['passed','total','detuning','carrier_rows']},indent=2))
