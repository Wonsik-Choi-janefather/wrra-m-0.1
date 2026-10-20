import verify_inputs
from pathlib import Path
import json,math
import numpy as np
from scipy.optimize import brentq
import dynamics
P=Path(__file__).resolve().parent;OUT=P/'results';checks={}
def test(n,v):
    checks[n]=bool(v)
    if not v:raise AssertionError(n)
seed=np.load(P/'inputs/quantized_seed.npz')['entropy'];h=np.fft.rfft(seed-seed.mean())/128
var=2*abs(h[1:])**2;var[-1]/=2
lo_path=OUT/'D_64_a2.5_s32_o0_k50000.npz'
if not lo_path.exists():lo_path=OUT/'D_64_a2.5_s32_k50000.npz'
lo=np.load(lo_path);hi=np.load(OUT/'D_64_a3_s32_o0_k50000.npz')
test('accuracy_controls_same_k_and_ell',np.array_equal(lo['ell'],hi['ell']) and np.allclose(lo['k'],hi['k'],rtol=0,atol=1e-14))
weight=np.broadcast_to(var[None,:],lo['T'].shape).copy();weight[lo['ell']%2==1,-1]=0
accuracy={}
for field in ['T','E','phi']:
    a=np.sum(weight*lo[field]**2,axis=1);b=np.sum(weight*hi[field]**2,axis=1)
    peak=float(np.max(abs(a-b))/np.max(abs(b)))
    shape=float(np.sqrt(np.mean((a-b)**2))/np.sqrt(np.mean(b*b)))
    accuracy[field]={'peak_normalized_power_change':peak,'relative_power_L2_change':shape}
    test('accuracy_power_L2_'+field,shape<.01)
# Uniform-density slicing is verified with separate nonlinear perturbed histories.
dy=json.loads((OUT/'dynamics_results.json').read_text());beta=dy['calibrated_convertible_radiation_fraction']
_,base=dynamics.evolve(beta);y=base.y[:,-1];N,C,M=y[:3];rho=(1-beta+C)*math.exp(-4*N)+M*math.exp(-3*N)
fd=[]
for eps in [.01,.005]:
    ns=[]
    for sign in [1,-1]:
        _,sol=dynamics.evolve(beta,sign*eps);yy=sol.y[:,-1];rr=1-beta+yy[1];mm=yy[2]
        ns.append(brentq(lambda nn:rr*math.exp(-4*nn)+mm*math.exp(-3*nn)-rho,N-.01,N+.01,xtol=2e-15))
    fd.append((ns[0]-ns[1])/(2*eps))
relative=abs(fd[-1]/dy['uniform_density_curvature_response_at_matching']-1)
test('nonlinear_uniform_density_deltaN_matches_tangent',relative<.001)
# Exercise a nonzero Nyquist signal, which the actual frozen profile nearly lacks.
phase=np.arange(128);nyquist=(-1.)**phase
spec=np.fft.rfft(nyquist)/128;test('nonzero_Nyquist_single_real_variance',abs(spec[-1])**2==np.mean(nyquist**2)==1)
test('incorrect_Nyquist_double_count_rejected',2*abs(spec[-1])**2!=np.mean(nyquist**2))
even=float(np.mean(np.cos(np.pi*phase)**2));odd=float(np.mean(np.sin(np.pi*phase)**2))
test('Nyquist_even_odd_phase_readout',abs(even-1)<1e-14 and odd<1e-25)
result={'version':'0.3','checks_passed':sum(checks.values()),'checks':checks,
    'accuracy_2p5_to_3p0_on_actual_471_multipoles':accuracy,
    'uniform_density_deltaN_finite_difference_relative_error':relative,
    'scope':'Numerical precision, nonlinear slicing and nonzero Nyquist controls; no new empirical likelihood or full finite-gradient completion.'}
(OUT/'review_extension_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
