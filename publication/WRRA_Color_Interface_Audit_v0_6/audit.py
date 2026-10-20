#!/usr/bin/env python3
"""Replay selected original functions without importing unrelated macro modules.
This is a targeted rerun, not a full Stage-3 pipeline rerun.
"""
from pathlib import Path
from fractions import Fraction as F
import ast, csv, hashlib, itertools, json, math, platform
import numpy as np
import scipy
import sympy as sp
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parent
REPO=ROOT/'source'
def extract(path,names,env):
    tree=ast.parse(path.read_text())
    nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in names]
    assert {n.name for n in nodes}==set(names)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),env)
    return env

def run():
    manifest=json.loads((ROOT/'SOURCE_SHA256.json').read_text())
    actual={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(REPO.rglob('*')) if p.is_file()}
    if actual != manifest:
        raise ValueError('Frozen source manifest mismatch; refusing execution')
    env=dict(np=np,math=math,itertools=itertools,csv=csv,F=F,REPO=REPO)
    extract(REPO/'calculations/wrra_m_0_9/compute.py',['address_base','phase_drive','effects'],env)
    extract(REPO/'mcc_3_0/stage_3_particle_component_replay/run_stage3.py',
            ['assemble','color_check','charge_checks','particle_bookkeeping'],env)
    cfg=json.loads((REPO/'calculations/wrra_m_0_9/parameters.json').read_text())
    hand=json.loads((REPO/'mcc_3_0/stage_2_finite_source_insertion/STAGE3_HANDOFF.json').read_text())['source_state']
    cfg['upstream']['address_cutoff_N']=hand['N_U']
    cfg['upstream']['state']['alpha']=hand['alpha']
    cfg['upstream']['update']['sigmoid_threshold_h']=hand['threshold_h']
    base=env['address_base'](cfg);effect=env['effects'](cfg,base)
    raw=base['w']*effect[0];odd=base['odd'];n=base['n'][odd];w=raw[odd]/raw[odd].sum()
    primes=base['n'][base['prime']]
    profiles={f'K{k}_{order}':env['assemble'](n,w,primes,k,order) for k in (15,16) for order in ('small','large')}
    tv=float(np.abs(np.array(profiles['K15_small']['number_share'])-profiles['K15_large']['number_share']).sum()/2)
    charge=env['charge_checks'](len(n),float(raw.sum()))
    original_color=env['color_check']()

    # Independently construct normalized fundamental generators T=lambda/2.
    T=[]
    for i,j in [(0,1),(0,2),(1,2)]:
        a=np.zeros((3,3),complex);a[i,j]=a[j,i]=.5;T.append(a)
        a=np.zeros((3,3),complex);a[i,j]=-.5j;a[j,i]=.5j;T.append(a)
    T.extend([np.diag([.5,-.5,0]),np.diag([1,1,-2])/(2*np.sqrt(3))])
    I=np.eye(3);Q=[np.kron(np.kron(t,I),I)+np.kron(np.kron(I,t),I)+np.kron(np.kron(I,I),t) for t in T]
    psi=np.zeros(27,complex)
    for p in itertools.permutations(range(3)):
        sign=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        psi[np.ravel_multi_index(p,(3,3,3))]=sign/np.sqrt(6)
    gram=np.array([[np.trace(a@b) for b in T] for a in T])
    closure=[]
    for a in T:
        for b in T:
            comm=a@b-b@a
            coeff=np.array([-2j*np.trace(comm@t) for t in T]).real
            closure.append(np.linalg.norm(comm-1j*sum((c*t for c,t in zip(coeff,T)),np.zeros((3,3),complex))))
    stack=np.vstack(Q);sv=np.linalg.svd(stack,compute_uv=False)
    rng=np.random.default_rng(20261020);rot=[]
    for _ in range(32):
        H=sum((x*t for x,t in zip(rng.normal(size=8),T)),np.zeros((3,3),complex));U=expm(1j*H)
        rot.append(float(np.linalg.norm(np.kron(np.kron(U,U),U)@psi-psi)))
    tensor=psi.reshape(3,3,3)
    reduced=np.einsum('ijk,ljk->il',tensor,tensor.conj())
    phase=np.diag([-1,1,1]);broken=np.kron(np.kron(phase,I),I)@psi
    bad=np.zeros(27,complex);bad[np.ravel_multi_index((0,1,2),(3,3,3))]=1
    extended={
      'generator_count':len(T),'hermiticity_error':max(float(np.linalg.norm(t-t.conj().T)) for t in T),
      'tracelessness_error':max(float(abs(np.trace(t))) for t in T),
      'gram_error':float(np.max(np.abs(gram-np.eye(8)/2))),
      'commutator_closure_error':float(max(closure)),
      'common_kernel_rank':int(np.count_nonzero(sv>1e-10)),
      'common_kernel_dimension':int(27-np.count_nonzero(sv>1e-10)),
      'smallest_nonzero_stacked_singular_value':float(sv[-2]),
      'total_generator_residual':max(float(np.linalg.norm(q@psi)) for q in Q),
      'collective_SU3_rotation_max_error_32_cases':max(rot),
      'one_quark_reduced_state_error_to_I_over_3':float(np.linalg.norm(reduced-I/3)),
      'basis_rgb_total_charge_max_norm':max(float(np.linalg.norm(q@bad)) for q in Q),
      'one_site_phase_error_total_charge_max_norm':max(float(np.linalg.norm(q@broken)) for q in Q),
      'one_site_phase_error_singlet_fidelity':float(abs(np.vdot(psi,broken))**2),
      'original_color_function_parameters':list(__import__('inspect').signature(env['color_check']).parameters),
      'dependency_verdict':'color_check takes no arithmetic state input; its SU(3) structure is explicitly constructed'
    }
    # Exact common kernel, with nonzero generator rescalings removing radicals.
    exact=[]
    for i,j in [(0,1),(0,2),(1,2)]:
        a=sp.zeros(3);a[i,j]=a[j,i]=1;exact.append(a)
        a=sp.zeros(3);a[i,j]=-sp.I;a[j,i]=sp.I;exact.append(a)
    exact.extend([sp.diag(1,-1,0),sp.diag(1,1,-2)])
    eye=sp.eye(3)
    EQ=[sp.kronecker_product(t,eye,eye)+sp.kronecker_product(eye,t,eye)+sp.kronecker_product(eye,eye,t) for t in exact]
    kernel=sp.Matrix.vstack(*EQ).nullspace()
    sign_vector=sp.Matrix([int(round(z.real*np.sqrt(6))) for z in psi])
    exact_singlet=all(q*sign_vector==sp.zeros(27,1) for q in EQ)
    # A projected arbitrary joint state must factor because the color kernel has rank one.
    Ps=np.outer(psi,psi.conj());A=rng.normal(size=(162,9))+1j*rng.normal(size=(162,9))
    omega=A@A.conj().T;omega/=np.trace(omega)
    P=np.kron(np.eye(6),Ps); projected=P@omega@P; projected/=np.trace(projected)
    sigma=np.einsum('acbc->ab',projected.reshape(6,27,6,27))
    factor_error=float(np.linalg.norm(projected-np.kron(sigma,Ps)))
    extended.update({'exact_common_kernel_dimension':len(kernel),'exact_integer_sign_vector_annihilated':bool(exact_singlet),
                     'projected_joint_state_factorization_error':factor_error})
    historical=json.loads((REPO/'mcc_3_0/stage_3_particle_component_replay/results/results.json').read_text())
    checks={
      'address_count':len(n)==427892,
      'phenotype_share':abs(float(raw.sum())-.05)<2e-12,
      'integer_conservation':all(p['integer_conservation'] for p in profiles.values()),
      'number_share_normalization':all(abs(sum(p['number_share'])-1)<2e-12 for p in profiles.values()),
      'neutron_K15_small_reproduced':abs(profiles['K15_small']['neutron_fraction_5_47']-.12947198693705966)<2e-12,
      'neutron_K15_large_reproduced':abs(profiles['K15_large']['neutron_fraction_5_47']-.1271594116970887)<2e-12,
      'neutron_K16_small_reproduced':abs(profiles['K16_small']['neutron_fraction_5_47']-.12498278121735387)<2e-12,
      'order_TV_reproduced':abs(tv-.20472100116369316)<2e-12,
      'neutral_charge_motifs':charge['all_motifs_neutral'],
      'original_singlet_normalization':abs(original_color['norm']-1)<1e-12,
      'original_singlet_charge':original_color['maximum_residual']<1e-12,
      'generator_hermiticity':extended['hermiticity_error']<1e-12,
      'generator_tracelessness':extended['tracelessness_error']<1e-12,
      'generator_orthogonality':extended['gram_error']<1e-12,
      'generator_closure':extended['commutator_closure_error']<1e-12,
      'unique_singlet_for_declared_three_fundamentals':extended['common_kernel_dimension']==1,
      'collective_rotations':max(rot)<1e-12,
      'reduced_state':extended['one_quark_reduced_state_error_to_I_over_3']<1e-12,
      'basis_state_negative_control_detected':extended['basis_rgb_total_charge_max_norm']>.1,
      'one_site_phase_negative_control_detected':extended['one_site_phase_error_total_charge_max_norm']>.1,
      'exact_kernel_dimension':len(kernel)==1,
      'exact_singlet_annihilation':exact_singlet,
      'rank_one_color_sector_factorization':factor_error<1e-12,
    }
    checks['frozen_source_hashes_verified']=actual==manifest
    for key,reference in historical['profiles']['candidate_phase'].items():
        checks[key+'_historical_fraction']=abs(profiles[key]['neutron_fraction_5_47']-reference['neutron_fraction'])<2e-12
        checks[key+'_historical_mean_parts']=abs(profiles[key]['mean_parts']-reference['mean_parts'])<2e-10
        checks[key+'_historical_residue1_weight']=abs(profiles[key]['residue1_weight']-reference['residue1_weight'])<2e-12
    result={'date':'2026-10-20','source_commit':'9d9daf21154e46e55b9fd0fd461c7c070156ab94',
      'scope':'Targeted original-function replay plus independent color algebra audit; not a full Stage-3 pipeline rerun',
      'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},
      'thresholds':{'reference_fractions_and_shares_absolute':2e-12,'reference_mean_parts_absolute':2e-10,
                    'matrix_errors_absolute':1e-12,'numerical_kernel_rank_threshold':1e-10,
                    'negative_control_minimum_charge_norm':0.1,'exact_symbolic_checks':'zero tolerance'},
      'candidate_addresses':len(n),'phenotype_share':float(raw.sum()),'profiles':profiles,
      'order_total_variation':tv,'charge':charge,'original_color':original_color,'extended_color':extended,
      'checks':checks,'passed':sum(checks.values()),'total':len(checks),'all_passed':all(checks.values()),
      'claim_verdict':{'implementation_consistency':'PASS' if all(checks.values()) else 'FAIL',
         'arithmetic_derivation_of_three_colors_and_SU3':'NOT ESTABLISHED',
         'full_spin_flavor_confinement_and_covariant_QCD':'OPEN',
         'new_observational_prediction':'NOT CLAIMED'}}
    (ROOT/'audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    assert all(checks.values()),checks
    print(json.dumps({k:result[k] for k in ('passed','total','candidate_addresses','phenotype_share','order_total_variation','extended_color')},indent=2))

if __name__=='__main__':run()
