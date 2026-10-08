"""Explicit conditional address/channel instrument, not a physical record engine."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
D=ROOT/'step3_dependency/step2_dependency'
manifest=json.loads((ROOT/'step3_dependency/dependency_manifest.json').read_text())
for name,h in manifest['files'].items():assert hashlib.sha256((D/name).read_bytes()).hexdigest()==h
p=D/'address_structure.py';nodes=[]
for node in ast.parse(p.read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name=='product':break
 nodes.append(node)
s={'__file__':str(p),'__name__':'setup'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),s)
p=D/'connection_sources/channel_compute.py'
names={'inventory','placement','charges'}
c={'np':np,'Q':Q};exec(compile(ast.Module(body=[n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(p),'exec'),c)
cfg=s['params']['upstream_0_9']['baseline_0_8']
selection_path=ROOT/'carrier_selection_results.json'
selected='F_DX' # bootstrap only for carrier setup extraction
if not selection_path.exists() and __name__!='setup':
 raise RuntimeError('Run carrier_selection.py first; selection evidence is required')
if selection_path.exists():
 selection_result=json.loads(selection_path.read_text());assert selection_result['status']=='PASS' and all(selection_result['checks'].values())
 selected=selection_result['handoff']['selected_filter']
slots,P=c['placement'](selected);table=c['charges'](slots,cfg)
if selection_path.exists():assert P.argmax(axis=1).tolist()==selection_result['handoff']['slot_permutation']
# Classical address distribution with quantum channel blocks. An address-sector
# operation has Kraus K_s(n)=sqrt(e_s(n))*P. It preserves channel coherence
# within a block. Reading channel labels is a separate projective operation.
e=s['effect'];w=s['base']['w'];origin=np.array(s['cfg']['channel_coupling']['default_origin_weights']);Gamma=np.diag(origin)
family=np.array(s['cfg']['channel_coupling']['family_weights']);target=P@Gamma@P.T
shares=e@w;checks={}
checks['sector_effects_nonnegative_and_complete']=bool(np.min(e)>=-1e-14 and np.allclose(e.sum(axis=0),1,atol=2e-13,rtol=0))
checks['kraus_completeness_all_addresses']=bool(np.allclose(e.sum(axis=0)[:,None,None]*(P.T@P),np.eye(16),atol=2e-13,rtol=0))
checks['charge_table_reproduces_known_fields']=table['benchmark_matches']
checks['all_exact_charge_anomalies_cancel']=all(Q(v)==0 for v in table['anomalies'].values())
output=np.array([v*target for v in shares]);checks['aggregate_sector_channel_state_normalized']=bool(abs(sum(np.trace(x) for x in output)-1)<2e-13 and min(np.linalg.eigvalsh(x).min() for x in output)>=-1e-14)
legacy=json.loads((D/'dependencies/original/m10_results.json').read_text())['phenotype_channel_energy']
weights=(shares[0]*np.outer(family,np.diag(target))).ravel()
checks['original_48_component_weights_reproduced']=bool(np.allclose(weights,[x['arithmetic_phenotype_weight'] for x in legacy],atol=2e-13,rtol=0))
# A nonuniform diagnostic origin mixture tests the actual permutation, unlike I/16.
rng=np.random.default_rng(4);v=rng.normal(size=16)+1j*rng.normal(size=16);v/=np.linalg.norm(v);coherent=np.outer(v,v.conj());mapped=P@coherent@P.T
checks['coherence_preserved_before_label_readout']=bool(abs(np.trace(mapped@mapped)-1)<1e-13 and np.linalg.norm(mapped-np.diag(np.diag(mapped)))>0.1)
read=np.diag(np.diag(mapped));checks['separate_label_readout_preserves_trace_changes_coherence']=bool(abs(np.trace(read)-1)<1e-13 and np.trace(read@read).real<1)
# Two correlated address-channel groups, not a product-of-marginals assumption.
mask=s['base']['n']%3==0;group=np.array([(e[0]*w)[mask].sum(),(e[0]*w)[~mask].sum()]);G1=coherent;G2=np.diag(origin)
correlated=group[0]*(P@G1@P.T)+group[1]*(P@G2@P.T)
checks['correlated_address_channel_output_positive_and_correct_trace']=bool(np.linalg.eigvalsh(correlated).min()>-1e-13 and abs(np.trace(correlated)-shares[0])<2e-13)
# Relabel transport and observables together; charges themselves are not scrambled.
perm=rng.permutation(16);U=np.eye(16)[perm];obs=np.diag([float(Q(x['Q'])) for x in table['channel_table']]);value=np.trace(correlated@obs).real
checks['charge_expectation_covariant_under_passive_basis_change']=bool(abs(np.trace((U@correlated@U.T)@(U@obs@U.T)).real-value)<1e-13)
cal=s['adapter']['calibration'];Ephi=cal['eta_J_m3']['phenotype']*s['mu'][0]*s['params']['reference_volume_m3'];energy=Ephi*np.outer(family,np.diag(target)).ravel()
checks['channel_energy_partition_stays_inside_one_phenotype_budget']=bool(abs(energy.sum()-Ephi)<1e-24)
assert all(checks.values()),checks
out={'status':'PASS','version':'0.1','dependency_commit':'86894014bf1f056fd99642fb7e791679e17c8471','map':'K_s(n)=sqrt(e_s(n))*P on classical-address quantum-channel blocks','sector_shares':shares.tolist(),'channel_table':table,'family_channel_weights':weights.tolist(),'phenotype_energy_J':Ephi,'channel_energy_sum_J':float(energy.sum()),'correlated_charge_expectation_unnormalized':float(value),'checks':checks,'scope':'explicit conditional phenotype routing and label readout; separate from dynamical filter selection, mass/mixing derivation and physical record production','assumptions':['classical address blocks','inherited F_DX placement','independent Weyl channel convention','conditional neutral extension','three calibrated families','default uniform origin routing'],'remaining':['replay carrier response to filter selection in this interface','connect physical record operation with channel-resolved phenotype','review available mass/mixing computation rather than equating budget slots with particle masses']}
(ROOT/'phenotype_transform_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'status':'PASS','checks':len(checks),'shares':out['sector_shares']}))
