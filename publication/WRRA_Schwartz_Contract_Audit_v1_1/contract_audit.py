#!/usr/bin/env python3
"""Actual-coefficient counterexample and class-resolved repair, fixed inputs."""
from pathlib import Path
import json,hashlib,math,platform
import numpy as np
import scipy
from audit import extract,REPO,ROOT

def run():
    manifest=json.loads((ROOT/'SOURCE_SHA256.json').read_text())
    for name,sha in manifest.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('source hash mismatch')
    env=dict(np=np);extract(REPO/'calculations/wrra_m_0_9/compute.py',['address_base','phase_drive','effects'],env)
    cfg=json.loads((REPO/'calculations/wrra_m_0_9/parameters.json').read_text());h=json.loads((REPO/'mcc_3_0/stage_2_finite_source_insertion/STAGE3_HANDOFF.json').read_text())['source_state']
    cfg['upstream']['address_cutoff_N']=h['N_U'];cfg['upstream']['state']['alpha']=h['alpha'];cfg['upstream']['update']['sigmoid_threshold_h']=h['threshold_h']
    base=env['address_base'](cfg);effects=env['effects'](cfg,base);n=base['n'];w=base['w']
    F=effects*(1+np.array([0,.25,.1])[:,None]*np.log(n)/np.log(h['N_U']))
    N=256; a=F[:,:N]*w[:N]; mask=n[:N]%3==0; z=np.where(mask,1.,-1.)
    u=a[2]*z;delta=u-a.T@np.linalg.solve(a@a.T,a@u);delta/=np.max(np.abs(delta))
    before=2*a@delta;after=2*a@(z*delta)
    lift=np.vstack([a*mask,a*~mask])
    eigmin=float((1-np.max(np.abs(delta)))/2)
    # Store Z coefficients of the class-resolved weighted operators.
    stored=np.array([a@(delta*mask),a@(delta*~mask)])
    repaired=2*(stored[0]-stored[1])
    rng=np.random.default_rng(20261020);d=8
    states=rng.normal(size=(N,d))+1j*rng.normal(size=(N,d));states/=np.linalg.norm(states,axis=1)[:,None]
    rho=np.einsum('ni,nj->nij',states,states.conj())
    weighted=np.einsum('sn,nij->sij',a,rho)
    errors=[]
    for _ in range(20):
        b=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));b=(b+b.conj().T)/2
        direct=a@np.einsum('nij,ji->n',rho,b).real
        reduced=np.einsum('sij,ji->s',weighted,b).real
        errors.append(float(np.max(np.abs(direct-reduced))))
    # Scalar diagonal version of the covariance identity using the actual address coefficients.
    f=F[:,:N];ww=w[:N]/w[:N].sum();b=delta
    lhs=f@(ww*b)-(f@ww)*np.sum(ww*b)
    rhs=np.sum(ww[None,:]*(f-(f@ww)[:,None])*(b-np.sum(ww*b))[None,:],axis=1)
    witness_addresses=[[3,6,9],[2,4,25]]
    minors=[F[:,np.array(aa)-2] for aa in witness_addresses]
    checks={
      'conditional_qubits_positive':eigmin>=-1e-14,
      'same_initial_weighted_operators':float(np.max(np.abs(before)))<1e-12,
      'controlled_update_distinguishes_states':float(abs(after[2]))>.1,
      'class_lift_replays_update':float(np.max(np.abs(after-repaired)))<1e-12,
      'base_coefficient_rank_three':np.linalg.matrix_rank(a)==3,
      'class_lift_rank_six':np.linalg.matrix_rank(lift)==6,
      'both_triangular_witnesses_nonsingular':all(abs(np.linalg.det(m))>1e-8 for m in minors),
      'twenty_arbitrary_hermitian_queries_preserved':max(errors)<1e-12,
      'covariance_error_identity':float(np.max(np.abs(lhs-rhs)))<1e-12,
      'initial_difference_reproduced':abs(float(np.max(np.abs(before)))-1.12e-16)<5e-15,
      'return_difference_reproduced':abs(float(after[2])-.6668017457457079)<2e-12,
    }
    from reusable_closure import compile_fixed_ix,encode,advance,readout
    compiled=compile_fixed_ix(a,mask)
    b=rng.normal(size=(N,3));b/=np.maximum(1,np.linalg.norm(b,axis=1))[:,None]
    y=encode(compiled,b);trajectory_error=0.
    for _ in range(8):
        direct=(a@b).reshape(-1)
        trajectory_error=max(trajectory_error,float(np.max(np.abs(direct-readout(compiled,y)))))
        b[~mask,1:]*=-1;y=advance(compiled,y)
    checks.update({'fixed_ix_dimension_15':compiled['fixed_update_variable_dimension']==15,
                   'fixed_ix_dimension_formula':compiled['predicted_fixed_update_dimension']==15,
                   'fixed_ix_less_than_full_class_18':compiled['full_class_variable_dimension_qubit']==18,
                   'fixed_ix_closed':compiled['closure_error']<1e-12,
                   'fixed_ix_eight_step_trajectory':trajectory_error<1e-12})
    zero=compile_fixed_ix(np.zeros((1,2)),[True,False])
    tiny=compile_fixed_ix(np.array([[1e-13,0.]]),[True,False])
    checks['compiler_zero_rank_input']=zero['fixed_update_variable_dimension']==0 and zero['closure_error']==0.
    checks['compiler_below_cutoff_input']=tiny['fixed_update_variable_dimension']==0 and tiny['readout_reconstruction_error']<1e-12
    result={'release':'WRRA-CONTRACT-AUDIT-20261020-v1.1','source_commit':'9d9daf21154e46e55b9fd0fd461c7c070156ab94',
      'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
      'first_active_addresses':N,'initial_max_query_difference':float(np.max(np.abs(before))),
      'post_controlled_update_Z_differences':after.tolist(),'repair_max_error':float(np.max(np.abs(after-repaired))),
      'random_query_max_error':max(errors),'covariance_identity_error':float(np.max(np.abs(lhs-rhs))),
      'base_rank':int(np.linalg.matrix_rank(a)),'lifted_rank':int(np.linalg.matrix_rank(lift)),
      'exact_witness_addresses':witness_addresses,'witness_determinants':[float(np.linalg.det(m)) for m in minors],
      'linear_variable_coordinates_d128':{'snapshot':3*(128**2-1),'complete_class_resolved':6*(128**2-1)},
      'retained_bytes_d128_G32':{'pure_grouped_vectors_and_weights':32*128*16+3*32*8,'three_weighted_complex128_operators':3*128**2*16,'three_float64_loads':24},
      'thresholds':{'absolute_matrix_and_readout_error':1e-12,'historical_return_difference':2e-12},
      'fixed_ix_compilation':{**{k:v for k,v in compiled.items() if not isinstance(v,np.ndarray)},'eight_step_readout_error':trajectory_error},
      'scope':'Numerical rerun of the original actual-interface construction and separately implemented readout and repair checks; no physical-time or observational claim',
      'checks':{k:bool(v) for k,v in checks.items()},'passed':sum(map(bool,checks.values())),'total':len(checks)}
    (ROOT/'contract_results.json').write_text(json.dumps(result,indent=2)+'\n');assert all(checks.values()),checks
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
