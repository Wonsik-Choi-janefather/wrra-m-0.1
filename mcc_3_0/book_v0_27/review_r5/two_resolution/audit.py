"""WRRA two-resolution compatibility audit; python3 audit.py.

Quantum Born/projector rules are explicit reverse-engineering inputs.
This is a finite compatibility construction, not a derivation of quantum theory,
a Planck-scale experiment, relativistic QFT or a solution of quantum gravity.
"""
import json, math
from pathlib import Path
import numpy as np

rng = np.random.default_rng(20261020)
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1., -1.]).astype(complex)
H = (X+Z)/math.sqrt(2)
def dm(v): return np.outer(v, v.conj())
def obs(t): return math.cos(t)*Z+math.sin(t)*X
def project(t, s): return (I+s*obs(t))/2
def red_b(rho): return np.trace(rho.reshape(2,2,2,2),axis1=0,axis2=2)
def err(a,b): return float(np.max(np.abs(np.asarray(a)-np.asarray(b))))

c=299792458.; h=6.62607015e-34; G=6.67430e-11
hbar=h/(2*math.pi); tp=math.sqrt(hbar*G/c**5); lp=c*tp
sh=1.4813019664158633e-21; length=c*sh
out={'scope':'finite adopted-quantum-instrument compatibility; no empirical Planck test',
 'inputs':{'c_m_s':c,'h_J_s':h,'G_m3_kg_s2':G,'shutter_proper_s':sh,
 'quantum_rule':'complex density matrices, Born probabilities and projective instruments adopted',
 'source_constants':'https://physics.nist.gov/cuu/Constants/Table/allascii.txt',
 'seed':20261020},
 'scales':{'planck_time_s':tp,'planck_length_m':lp,'shutter_length_m':length,
 'shutter_over_planck':sh/tp,'integer_ratio_required':False,
 'hard_grid_nyquist_photon_energy_MeV':math.pi*hbar*c/length/1.602176634e-13}}

# Coherent phase is preserved between readouts; premature dephasing is a control.
fringe=[]; erased=[]
for phi in np.linspace(0,2*math.pi,361):
    v=H@np.array([1.,0.]); v=np.diag([1,np.exp(1j*phi)])@v
    r=dm(v); fringe.append(float((H@r@H)[0,0].real))
    erased.append(float((H@np.diag(np.diag(r))@H)[0,0].real))
out['interference']={'phases':361,'max_born_curve_error':err(fringe,[(1+math.cos(p))/2 for p in np.linspace(0,2*math.pi,361)]),
 'visibility':(max(fringe)-min(fringe))/(max(fringe)+min(fringe)),
 'premature_dephasing_visibility':(max(erased)-min(erased))/(max(erased)+min(erased))}

# Singlet joint state is not replaced by two independent local records.
v=np.array([0,1,-1,0],complex)/math.sqrt(2); singlet=dm(v)
def corr(a,b): return float(np.trace(singlet@np.kron(obs(a),obs(b))).real)
a0=0.; a1=math.pi/2; b0=math.pi/4; b1=-math.pi/4
S=abs(corr(a0,b0)+corr(a0,b1)+corr(a1,b0)-corr(a1,b1))
local=[]
for bits in range(16):
    a,b,d,e=[1 if bits>>i&1 else -1 for i in range(4)]
    local.append(abs(a*d+a*e+b*d-b*e))
out['bell']={'CHSH_S':S,'target':2*math.sqrt(2),
 'deterministic_local_assignments':16,'local_bound':max(local),
 'joint_state_rule_is_input':True}

sig=order=norm=repeat=uncertainty=0.
joint_cases=0
for case in range(200):
    A=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
    rho=A@A.conj().T; rho/=np.trace(rho)
    for theta in np.linspace(0,math.pi,5):
        nonselect=np.zeros((4,4),complex); probs=[]
        B=I; phi=float(rng.uniform(0,2*math.pi))
        for s in [-1,1]:
            M=np.kron(project(theta,s),I)
            nonselect+=M@rho@M.conj().T
            probs.append(float(np.trace(M@rho@M.conj().T).real))
            for t in [-1,1]:
                N=np.kron(I,project(phi,t))
                ab=N@M@rho@M.conj().T@N.conj().T
                ba=M@N@rho@N.conj().T@M.conj().T
                order=max(order,err(ab,ba)); joint_cases+=1
        sig=max(sig,err(red_b(nonselect),red_b(rho)))
        norm=max(norm,abs(sum(probs)-1),max(0,-min(probs)))
    # One instrument event need not assign all incompatible observables.
    q=red_b(rho); x=float(np.trace(q@X).real); y=float(np.trace(q@Y).real); z=float(np.trace(q@Z).real)
    uncertainty=max(uncertainty,max(0,z*z-(1-x*x)*(1-y*y)))
    for s in [-1,1]:
        P=project(.37,s); q1=P@q@P; p=np.trace(q1).real
        if p>1e-14:
            q1/=p; repeat=max(repeat,abs(1-np.trace(P@q1).real))
out['instruments']={'random_mixed_joint_states':200,'nonselective_channels':1000,
 'spacelike_tensor_factor_branch_order_cases':joint_cases,
 'no_signalling_reduced_density_max_error':sig,'commuting_branch_order_max_error':order,
 'probability_error':norm,'same_observable_repeat_error':repeat,
 'pauli_uncertainty_violation_max':uncertainty,
 'caveat':'tensor-factor commutativity is supplied locality structure, not derived field microcausality'}

# Proper-time thresholds stay local; unrelated spacelike events have no order.
clockerr=0.; reversals=0
for beta in np.linspace(-.99,.99,101):
    gam=1/math.sqrt(1-beta*beta)
    for scale in [sh,tp]:
        dt=gam*scale; dx=-gam*beta*scale  # x/c in seconds
        clockerr=max(clockerr,abs((dt*dt-dx*dx)/(scale*scale)-1))
    # Events (ct,x)=(0,0),(0,1): t'=-gamma beta/c.
    if beta>.01 and -gam*beta<0: reversals+=1
out['relativity']={'boosts':101,'proper_interval_checks':202,
 'max_relative_interval_error':clockerr,'positive_boost_spacelike_order_reversals':reversals,
 'global_synchronization':False,'scope':'special-relativistic event kinematics only'}

# Total-energy preserving finite measurement realization, degenerate pointer.
P0=project(0,1); P1=project(0,-1)
U=np.kron(P0,I)+np.kron(P1,X); Etotal=np.kron(Z,I)
out['conservation_example']={'unitarity_error':err(U.conj().T@U,np.eye(4)),
 'total_energy_commutator_error':err(U@Etotal,Etotal@U),
 'scope':'Z-QND measurement with degenerate pointer; no general apparatus dynamics'}

# Scheduler preserves adopted shutter; measurement never flips conjugate phase.
def schedule(tau, minimum):
    if tau<minimum: raise ValueError('local interval below adopted threshold')
    return True
negative={}
try: schedule(tp/2,tp)
except ValueError: negative['sub_planck_interval_rejected_by_assumption']=True
negative['premature_dephasing_fails_fringe']=out['interference']['premature_dephasing_visibility']<.01
negative['factorized_local_assignments_fail_CHSH']=out['bell']['local_bound']<S
negative['absolute_spacelike_order_not_invariant']=reversals>0
out['negative_controls']=negative
# Independent schedules on one apparatus worldline. A measurement does not
# advance the matter/antimatter shutter phase. Not an integer Planck lattice.
def phase(tau): return 1 if math.floor(tau/sh)%2==0 else -1
event_times=[.13*sh,.22*sh,.91*sh,1.31*sh]
last=0.; emitted=[]
for tau in event_times:
    schedule(tau-last,tp)
    emitted.append({'tau_s':tau,'shutter_sector':phase(tau)})
    last=tau
out['scheduler']={'measurement_events':emitted,
 'shutter_sector_at_ticks':[phase(k*sh) for k in range(4)],
 'shutter_interval_unchanged':True,
 'measurement_trigger_does_not_advance_shutter':True,
 'scope':'a local trigger ledger, not microscopic transition dynamics'}
assert out['scheduler']['shutter_sector_at_ticks']==[1,-1,1,-1]
out['unverified']=['Planck floor is not tested by finite qubit algebra',
 'G enters as an observed input, not a new WRRA gravity derivation',
 'No continuous field, interacting relativistic QFT, dynamical metric, Einstein equation or quantum gravity derived',
 'Born rule and complex joint states are adopted, not generated from integer codes',
 'No theorem that all known physics is compatible with the two scales',
 'Both scales are proper local specifications, not a coordinate-invariant Cartesian lattice',
 'No 10^22 internal steps were simulated; threshold represented analytically']
assert out['interference']['max_born_curve_error']<1e-12
assert abs(S-2*math.sqrt(2))<1e-12
assert max(sig,order,norm,repeat,uncertainty,clockerr)<1e-12
assert all(negative.values())
out['status']='PASS_WITH_EXPLICIT_SCOPE_AND_ADOPTED_INPUTS'
p=Path(__file__).with_name('results.json'); p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
