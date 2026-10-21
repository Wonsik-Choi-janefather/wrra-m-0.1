"""Independent finite Schrödinger integration and exact phase-noise enumeration."""
from pathlib import Path
import numpy as np,json,itertools
from scipy.integrate import solve_ivp
P=Path(__file__).resolve().parent;checks={};metrics={}
def ck(n,v):
 checks[n]=bool(v)
 if not v:raise AssertionError(n)
gamma=np.loadtxt(P/'inputs/zero_heights.csv',skiprows=1)
# Positive drive versus autonomous-clock completion are separate questions.
L=11;C=3;n=np.arange(1,L+1);logn=np.log(n);g=gamma[:C]
F=np.fft.fft(np.eye(L),axis=0,norm='ortho');k=abs(2*np.pi*np.fft.fftfreq(L))
H0=F.conj().T@np.diag(k)@F;Lam=np.diag(logn)
seed=n.astype(float)**(-.6);seed/=np.linalg.norm(seed)
y0=np.tile(seed,(C,1)).ravel()/np.sqrt(C);bigH=np.kron(np.eye(C),H0)
def matrices(t):
 U=F.conj().T@np.diag(np.exp(-1j*k*t))@F
 A=U@Lam@U.conj().T;V=np.kron(np.diag(g),A)
 deriv=-1j*(bigH@V-V@bigH)
 return U,V,deriv
def rhs(t,z):
 U,V,dV=matrices(t);psi=z[:-1];power=np.vdot(psi,dV@psi).real
 return np.r_[-1j*(bigH+V)@psi,power]
sol=solve_ivp(rhs,(0,1),np.r_[y0,0j],method='DOP853',rtol=2e-12,atol=2e-14,dense_output=True)
ck('ODE_completed',sol.success)
U,V,dV=matrices(1);analytic=np.array([U@(seed*np.exp(-1j*gg*logn)) for gg in g]).ravel()/np.sqrt(C)
stateerr=float(np.max(abs(sol.y[:-1,-1]-analytic)));ck('ODE_exact_product_solution',stateerr<2e-10)
Ein=float(np.vdot(y0,bigH@y0).real);Eout=float(np.vdot(analytic,bigH@analytic).real)
work=float(sol.y[-1,-1].real);ck('ODE_work_integral',abs(work-(Eout-Ein))<2e-10)
Bmean=float(g.mean()*np.sum(seed**2*logn));consterr=0.
for i,t in enumerate(np.linspace(0,1,9)):
 U,V,dV=matrices(t);psi=sol.sol(t)[:-1]
 ck('positive_total_H_'+str(i),np.linalg.eigvalsh(bigH+V)[0]>-2e-12)
 consterr=max(consterr,abs(float(np.vdot(psi,V@psi).real)-Bmean))
ck('constant_control_expectation',consterr<2e-9)
# Wrapped phases implement the same endpoint but generally lose rank-one form.
addr=np.array([6,10,12,14,15,18,20,21,22,24,26,28])
raw=gamma[:,None]*np.log(addr);wrapped=np.mod(raw,2*np.pi)
ck('wrapped_endpoint_equivalence',np.max(abs(np.exp(-1j*raw)-np.exp(-1j*wrapped)))<2e-13)
rawrank=np.linalg.matrix_rank(raw);wrappedrank=np.linalg.matrix_rank(wrapped)
ck('unwrapped_rank_one',rawrank==1);ck('wrapped_rank_lower_bound',wrappedrank==len(addr))
# Independent ±theta errors: enumerate all 2^3 phase states, exactly.
theta=.7;eta=float(np.cos(theta)**2);phi=np.array([U@(seed*np.exp(-1j*gg*logn)) for gg in g])
a=phi.mean(0);rho_coh=np.outer(a,a.conj());rho_mix=sum(np.outer(v,v.conj()) for v in phi)/C
rho=np.zeros((L,L),complex)
for signs in itertools.product([-1,1],repeat=C):
 out=(np.exp(1j*theta*np.array(signs))[:,None]*phi).mean(0)
 rho+=np.outer(out,out.conj())/2**C
ck('exact_noise_density',np.max(abs(rho-eta*rho_coh-(1-eta)*rho_mix/C))<2e-14)
ck('noise_density_positive',np.linalg.eigvalsh(rho)[0]>-2e-14)
# Full C=70 Gram, independent dephasing contraction.
C=70;u=np.ones(C)/np.sqrt(C)
for prep in ['uniform','inherited_alpha']:
 G=np.load(P/'inputs'/(prep+'_combiner.npz'))['gram']
 for i,eta in enumerate([0.,.3,.8,1.]):
  noisy=eta*G+(1-eta)*np.eye(C)
  p=float((u@noisy@u).real/C)
  expected=eta*float((u@G@u).real/C)+(1-eta)/C
  ck(prep+'_noisy_Gram_'+str(i),abs(p-expected)<2e-14)
metrics={'ODE_state_max_error':stateerr,'ODE_work_error':abs(work-Eout+Ein),'control_expectation_max_error':consterr,
 'unwrapped_control_rank':int(rawrank),'wrapped_control_rank_on_12_addresses':int(wrappedrank),'wrapped_max_dimensionless':float(wrapped.max()),
 'ODE_evaluations':sol.nfev}
(P/'independent_verification.json').write_text(json.dumps({'checks':checks,'metrics':metrics,'all_checks_pass':all(checks.values())},indent=2));print(json.dumps({'count':len(checks),'metrics':metrics},indent=2))
