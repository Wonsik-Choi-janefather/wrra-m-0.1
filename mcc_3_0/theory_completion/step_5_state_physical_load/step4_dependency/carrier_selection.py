"""Replay carrier responses and select the placement consumed by Step4."""
from pathlib import Path
from types import SimpleNamespace
from fractions import Fraction as Q
import ast,json,math,importlib.util,hashlib
import numpy as np
from scipy.sparse import csr_matrix
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
def funcs(path,names,ns):
 nodes=[x for x in ast.parse(path.read_text()).body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name in names]
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns);return ns
D=ROOT/'step3_dependency/step2_dependency'
# Execute only the dependency setup of the first Step4 interface.
p=ROOT/'phenotype_transform.py';nodes=[]
for n in ast.parse(p.read_text()).body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='e' for t in n.targets):break
 nodes.append(n)
s={'__file__':str(p),'__name__':'setup'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),s)
m03=funcs(ROOT/'score_metric_0.py',{'scores'},{})
m04=funcs(ROOT/'score_metric_1.py',{'sub','dot','norm_sq','compatibility','gap_identity'},{'Fraction':Q,'Vector':tuple})
a=funcs(D/'connection_sources/channel_compute.py',{'inventory','shifts','responses','optimizer_weights','selection','placement','charges'},{'np':np,'Q':Q,'math':math,'ORIGINS':('3_A','3_B','1_A','1_B','anti3_A','anti3_B','1_N','1_0'),'PAIR_ENTRIES':(('3_A','1_A'),('3_B','1_B'),('3_A','1_B'),('3_B','1_A'),('anti3_A','1_N'),('anti3_B','1_0'),('anti3_A','1_0'),('anti3_B','1_N')),'FILTERS':('F_DX','F_XX','F_DD','F_XD'),'m03':SimpleNamespace(**m03),'m04':SimpleNamespace(**m04)})
c=funcs(D/'connection_sources/carrier_compute.py',{'Carrier'},{'np':np,'math':math,'csr_matrix':csr_matrix})
cfg=s['cfg'];N=cfg['ledger_0_7']['carrier_and_background']['lattice_N'];checks={};rows=[]
for eps in (0.,8.):
 carrier=c['Carrier'](N,eps)
 states=[('uniform',np.eye(N)/N)]
 for j in (0,N//16,N//2):
  v=carrier.wave(j);states.append(('mode_'+str(j),np.outer(v,v.conj())))
 v=carrier.packet([8,16,24],[1/3]*3);states.append(('packet',np.outer(v,v.conj())))
 for name,rho in states:
  response=a['responses'](rho,carrier,cfg);selection=a['selection'](response,cfg)
  assert selection['selected_filter']=='F_DX',(name,eps,selection)
  slots,P=a['placement'](selection['selected_filter']);charge=a['charges'](slots,cfg)
  assert charge['benchmark_matches']
  rows.append({'state':name,'epsilon':eps,'response':response,'selection':selection,'charge_benchmark':charge['benchmark_matches']})
checks['all_ten_carrier_conditions_select_F_DX']=True
checks['selected_filters_reproduce_charge_table']=True
checks['response_Gram_positive_rank16']=all(r['response']['minimum_gram_eigenvalue']>0 and r['response']['transport_gram_rank']==16 for r in rows)
checks['principal_carrier_operator_preserved']=all(r['response']['principal_channel_difference']<1e-12 for r in rows)
checks['construction_flow_converges']=all(r['selection']['finite_flow_residual']<=cfg['filter_calibration']['selection_residual_target']*(1+1e-6) for r in rows)
checks['gap_identities_reproduced']=all(r['selection']['gap_identity_max_error']<1e-12 for r in rows)
# Passive carrier-basis transformation must include both Kc and state.
carrier=c['Carrier'](N,0);rho=np.eye(N)/N;perm=np.random.default_rng(4).permutation(N);U=np.eye(N)[perm]
x=a['responses'](rho,carrier,cfg);y=a['responses'](U@rho@U.T,SimpleNamespace(Kc=U@carrier.Kc@U.T,N=N),cfg)
checks['carrier_basis_covariance']=all(abs(x['normalized_signatures'][k]-y['normalized_signatures'][k])<1e-12 for k in x['normalized_signatures'])
# Zero calibrated contrast is a tied control, not silently forced to F_DX.
control=json.loads(json.dumps(cfg));control['filter_calibration']['charge_contrast_to_response']=0
response=a['responses'](rho,carrier,control);tie=a['selection'](response,control)
checks['zero_contrast_control_fails_closed_on_tie']=tie['status']=='tied' and tie['selected_filter'] is None and len(tie['maximizers'])==4
# Zero initial support for the winner cannot be repaired by construction flow.
control=json.loads(json.dumps(cfg));control['filter_calibration']['initial_filter_weights']=[0,1/3,1/3,1/3]
unsupported=a['selection'](a['responses'](rho,carrier,control),control)
checks['unsupported_winner_not_fabricated']=unsupported['status']=='winning_filter_has_zero_support' and unsupported['selected_filter'] is None
assert all(checks.values()),checks
out={'status':'PASS','version':'0.2','cases':rows,'checks':checks,'controls':{'zero_contrast':tie['status'],'unsupported_winner':unsupported['status']},'handoff':{'selected_filter':'F_DX','slot_permutation':a['placement']('F_DX')[1].argmax(axis=1).tolist(),'consumer':'phenotype_transform.py'},'scope':'inherited calibrated resolvent response -> compatibility -> construction selection -> phenotype placement; optimizer weights are not Born probabilities or physical records','source_hashes':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [ROOT/'score_metric_0.py',ROOT/'score_metric_1.py']}}
(ROOT/'carrier_selection_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'status':'PASS','checks':len(checks),'cases':len(rows),'minimum_gap':min(r['selection']['minimum_score_gap'] for r in rows)}))
