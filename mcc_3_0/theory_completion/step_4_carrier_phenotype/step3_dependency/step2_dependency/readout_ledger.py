"""Step 2 v0.2: explicit frame ledger and calibration response."""
from pathlib import Path
import ast,json,math
import numpy as np
ROOT=Path(__file__).resolve().parent
# Execute only setup and structural replay, before sampled product probes.
path=ROOT/'address_structure.py';tree=ast.parse(path.read_text());prefix=[]
for node in tree.body:
    if isinstance(node,ast.FunctionDef) and node.name=='product':break
    prefix.append(node)
s={'__file__':str(path),'__name__':'structural_setup'}
exec(compile(ast.Module(body=prefix,type_ignores=[]),str(path),'exec'),s)
cfg=s['cfg'];w=s['w'];cost=s['cost'][2:];mask=s['struct_odd'];even=s['struct_even'];prime=s['struct_prime']
sp=cfg['upstream']['spectrum'];up=cfg['upstream']['update'];alpha=cfg['upstream']['state']['alpha'];h=up['sigmoid_threshold_h']
gamma=np.asarray(sp['gamma'])[:,None];coef=np.asarray(sp['coefficients'])[:,None];offset=np.asarray(sp['phase_offsets'])[:,None]
K=up['admission_frames_K']
drives=np.array([(coef*np.cos(gamma*(cost[mask][None,:]+up['phase_step_xi']*k)+offset)).sum(axis=0) for k in range(K)])
# This is an algebraic decomposition of the inherited admission law,
# not newly assumed independent physical detection events.
log_survival_step=-np.logaddexp(0,drives-h)
survival=np.ones(mask.sum());frame_rows=[];ledger=np.zeros(mask.sum())
for k in range(K):
    transfer=survival*(-np.expm1(log_survival_step[k]))
    survival*=np.exp(log_survival_step[k]);ledger+=transfer
    frame_rows.append({'frame':k,'weighted_phenotype_transfer':float(w[mask]@transfer),
                       'eligible_remaining_weight':float(w[mask]@survival)})
admission=-np.expm1(log_survival_step.sum(axis=0))
checks={}
checks['frame_transfers_reconstruct_admission']=bool(np.allclose(ledger,admission,atol=2e-15,rtol=0))
checks['every_eligible_address_conserves_ledger']=bool(np.allclose(ledger+survival,1,atol=2e-15,rtol=0))
checks['all_addresses_have_exactly_one_structural_class']=bool(np.all(prime.astype(int)+even.astype(int)+mask.astype(int)==1))
shares=s['shares'];contributions={'prime_to_return':float(w[prime].sum()),'minimum_atom_composite_to_dark':float(w[even].sum()),'eligible_to_phenotype':float(w[mask]@admission),'eligible_to_return':float(w[mask]@survival)}
reconstructed=np.array([contributions['eligible_to_phenotype'],contributions['minimum_atom_composite_to_dark'],contributions['prime_to_return']+contributions['eligible_to_return']])
checks['sector_ledger_reproduces_frozen_shares']=bool(np.allclose(reconstructed,shares,atol=2e-13,rtol=0))
checks['total_normalized_weight_conserved']=abs(sum(contributions.values())-1)<2e-13
# alpha modifies the common measure; h modifies only the eligible P/R split.
effect=s['effect'];mean_cost=float(w@cost)
dalpha=-(effect*(cost-mean_cost)*w).sum(axis=1)
pstep=np.exp(-np.logaddexp(0,h-drives))
dadmission=-survival*pstep.sum(axis=0)
dh=np.array([float(w[mask]@dadmission),0.,-float(w[mask]@dadmission)])
def evaluate(a,t):
    raw=np.exp(-a*cost);weight=raw/raw.sum()
    admit=-np.expm1((-np.logaddexp(0,drives-t)).sum(axis=0))
    p=float(weight[mask]@admit);d=float(weight[even].sum())
    return np.array([p,d,1-p-d])
eps=1e-5
numa=(evaluate(alpha+eps,h)-evaluate(alpha-eps,h))/(2*eps)
numh=(evaluate(alpha,h+eps)-evaluate(alpha,h-eps))/(2*eps)
checks['alpha_derivative_matches_finite_difference']=bool(np.allclose(dalpha,numa,atol=2e-9,rtol=0))
checks['h_derivative_matches_finite_difference']=bool(np.allclose(dh,numh,atol=2e-9,rtol=0))
checks['h_preserves_dark_share']=dh[1]==0 and dh[0]<0 and dh[2]>0
checks['calibration_derivatives_conserve_total']=abs(dalpha.sum())<2e-13 and abs(dh.sum())<2e-13
jac=np.column_stack([dalpha[:2],dh[:2]])
checks['two_target_local_calibration_has_full_rank']=np.linalg.matrix_rank(jac)==2
# Change the phase reference, transporting the offsets with it.
shift=.37
old=(coef*np.cos(gamma*cost[mask][None,:]+offset)).sum(axis=0)
new=(coef*np.cos(gamma*(cost[mask][None,:]+shift)+(offset-gamma*shift))).sum(axis=0)
phase_error=float(np.max(np.abs(old-new)))
checks['transported_phase_reference_preserves_drive']=phase_error<1e-12
checks={k:bool(v) for k,v in checks.items()}
assert all(checks.values()),checks
r={'status':'PASS','version':'0.2','date':'2026-10-08','fixed_alpha':alpha,'fixed_h':h,'shares':shares.tolist(),'ledger_contributions':contributions,'frame_transfer_ledger':frame_rows,'derivatives':{'dshares_dalpha':dalpha.tolist(),'dshares_dh':dh.tolist(),'finite_difference_alpha':numa.tolist(),'finite_difference_h':numh.tolist(),'two_target_jacobian':jac.tolist(),'determinant':float(np.linalg.det(jac))},'phase_reference_max_drive_error':phase_error,'checks':checks,'interpretation_limits':['frame transfers are an exact algebraic ledger, not a demonstrated stochastic independence law','nonzero calibration Jacobian establishes only local invertibility for the fixed readout family','sector assignments and log prime costs remain declared constitutive choices']}
(ROOT/'readout_ledger_results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
print(json.dumps(r,ensure_ascii=False,indent=2))
