"""Minimal real linear realization of the inherited finite spectral generator.
This is a result within linear time-invariant realizations of the fixed phase
sequence, not a universal physical minimum or a derivation of frame count.
"""
from pathlib import Path
import json,math
import numpy as np
ROOT=Path(__file__).resolve().parent
cfg=json.loads((ROOT/'step2_dependency/dependencies/original/parameters.json').read_text());sp=cfg['upstream']['spectrum'];xi=cfg['upstream']['update']['phase_step_xi']
gamma=np.array(sp['gamma']);coef=np.array(sp['coefficients']);off=np.array(sp['phase_offsets']);J=len(gamma);D=2*J
poles=np.concatenate([np.exp(1j*gamma*xi),np.exp(-1j*gamma*xi)])
separation=min(abs(poles[i]-poles[j]) for i in range(D) for j in range(i))
# Construct the real block rotation and shared output operator.
T=np.zeros((D,D));C=np.zeros(D)
for j,delta in enumerate(gamma*xi):
 c,z=math.cos(delta),math.sin(delta);T[2*j:2*j+2,2*j:2*j+2]=[[c,-z],[z,c]];C[2*j]=coef[j]
rows=[]
for n in (9,15,105,1001):
 theta=gamma*math.log(n)+off;state=np.empty(D);state[::2]=np.cos(theta);state[1::2]=np.sin(theta)
 seq=np.array([sum(coef*np.cos(theta+k*gamma*xi)) for k in range(2*D)])
 constructed=[]
 for k in range(2*D):constructed.append(float(C@state));state=T@state
 assert np.allclose(seq,constructed,atol=2e-13,rtol=0)
 H=np.array([[seq[i+j] for j in range(D)] for i in range(D)]);sing=np.linalg.svd(H,compute_uv=False);rank=int(np.linalg.matrix_rank(H))
 # Hankel=V diag(a) V^T for distinct exponential poles.
 amplitudes=np.concatenate([coef/2*np.exp(1j*theta),coef/2*np.exp(-1j*theta)])
 V=np.array([poles**k for k in range(D)])
 factored=V@np.diag(amplitudes)@V.T
 assert np.allclose(H,factored.real,atol=2e-13,rtol=0)
 assert rank==D
 rows.append({'address':n,'hankel_rank':rank,'singular_values':sing.tolist(),'best_rank7_frobenius_residual_lower_bound':float(sing[-1]),'maximum_sequence_replay_error':float(np.max(np.abs(seq-constructed)))})
checks={'all_eight_complex_poles_distinct':separation>1e-8,'all_spectral_amplitudes_nonzero':bool(np.all(coef!=0)),'real_rotation_realizes_inherited_sequence':all(x['maximum_sequence_replay_error']<2e-13 for x in rows),'hankel_rank_lower_bound_matches_eight_real_states':all(x['hankel_rank']==D for x in rows),'rotation_preserves_state_norm':bool(np.allclose(T.T@T,np.eye(D),atol=2e-14,rtol=0))}
checks={k:bool(v) for k,v in checks.items()}
assert all(checks.values())
r={'status':'PASS','version':'0.2','real_state_dimension':D,'minimum_pairwise_pole_separation':float(separation),'probes':rows,'checks':checks,'theorem_scope':'Any real linear time-invariant realization of the same inherited phase sequence has dimension at least its Hankel rank8; the block rotation realizes dimension8. Distinct poles and nonzero amplitudes imply rank8 by Vandermonde factorization.','probe_scope':'16 synthetic continuation samples from the declared phase rule, not16 observed physical frames; the adopted admission boundary remains8','not_derived':['physical necessity of four selected spectral modes','unique frame boundary K8','minimum among nonlinear encodings or all physical structures','number of common-carrier channels']}
(ROOT/'minimum_phase_state_results.json').write_text(json.dumps(r,indent=2));print(json.dumps({'status':'PASS','dimension':D,'checks':checks,'pole_separation':float(separation)},indent=2))
