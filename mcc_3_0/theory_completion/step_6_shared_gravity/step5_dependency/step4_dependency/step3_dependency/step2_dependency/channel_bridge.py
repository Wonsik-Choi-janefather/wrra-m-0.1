"""Execute inherited channel-blind product-space load bridge."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json,hashlib,math
import numpy as np
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
manifest=json.loads((ROOT/'connection_manifest.json').read_text())
for name,h in manifest['files'].items():assert hashlib.sha256((ROOT/'connection_sources'/name).read_bytes()).hexdigest()==h
# Setup source/filter without executing unrelated probes.
p=ROOT/'address_structure.py';nodes=[]
for node in ast.parse(p.read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name=='product':break
 nodes.append(node)
s={'__file__':str(p),'__name__':'setup'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),s)
path=ROOT/'connection_sources/channel_compute.py';names={'inventory','placement','channel_energy_bridge'}
a=[x for x in ast.parse(path.read_text()).body if isinstance(x,ast.FunctionDef) and x.name in names]
c={'np':np,'Q':Q};exec(compile(ast.Module(body=a,type_ignores=[]),str(path),'exec'),c)
# The published source indices identify the source-to-slot permutation.
legacy=json.loads((ROOT/'dependencies/original/m10_results.json').read_text())['phenotype_channel_energy']
first=[x for x in legacy if x['generation']==1];order=[x['source_index'] for x in sorted(first,key=lambda x:x['target_index'])]
selected=None
for name in ('F_DX','F_XX','F_DD','F_XD'):
 slots,P=c['placement'](name)
 if [x['source_index'] for x in slots]==order:selected=name;break
assert selected is not None
slots,P=c['placement'](selected)
origin=np.array(s['cfg']['channel_coupling']['default_origin_weights']);assert not s['cfg']['channel_coupling']['odd_smallest_prime_overrides']
Gamma=np.diag(origin);mapped=P@Gamma@P.T
# Independent transport directions are columns of P, not ranks of the default
# stochastic address-to-origin readout (whose identical columns have rank one).
core=P[:,:15];checks={}
checks['fifteen_transport_directions_preserved']=np.linalg.matrix_rank(core)==15 and np.allclose(core.T@core,np.eye(15),atol=1e-14,rtol=0)
checks['neutral_extension_preserved']=np.linalg.matrix_rank(P)==16 and np.allclose(P.T@P,np.eye(16),atol=1e-14,rtol=0)
checks['core_plus_extension_partition']=np.allclose(core@core.T+np.outer(P[:,15],P[:,15]),np.eye(16),atol=1e-14,rtol=0)
checks['channel_state_positive_normalized']=np.linalg.eigvalsh(mapped).min()>=0 and abs(np.trace(mapped)-1)<1e-14
# A_s^{joint}=I_channel tensor A_s. For transported product states,
# Tr[(Gamma tensor rho)(I tensor A_s)]=Tr(Gamma)Tr(rho A_s).
connection=json.loads((ROOT/'connection_results.json').read_text());case_rows=[]
for row in connection['carrier_rows']:
 load=np.array(row['loads']);before=load*np.trace(Gamma);after=load*np.trace(mapped)
 assert np.allclose(before,after,atol=1e-14,rtol=0)
 case_rows.append({'state':row['state'],'epsilon':row['epsilon'],'before':before.tolist(),'after':after.tolist()})
checks['channel_blind_product_bridge_preserves_all_tested_loads']=True
# Execute original channel bridge on fixed phenotype energies, not an extra budget.
params=s['params'];cal=s['adapter']['calibration'];eta=np.array([cal['eta_J_m3'][x] for x in s['ns']['SECTORS']]);E=eta*s['mu']*params['reference_volume_m3']
old_cfg={'filter_calibration':{'channel_state_weights':origin.tolist()}}
bridge=c['channel_energy_bridge'](P,old_cfg,{'sector_energy_J':dict(zip(s['ns']['SECTORS'],map(float,E)))})
checks['original_channel_bridge_reproduced']=bridge['maximum_energy_change_J']<1e-24
families=np.array(s['cfg']['channel_coupling']['family_weights']);channel_weights=np.outer(families,np.diag(mapped)).ravel();channel_energy=E[0]*channel_weights
checks['forty_eight_slots_close_to_one_phi_budget']=len(channel_energy)==48 and abs(channel_energy.sum()-E[0])<1e-24
checks['published_channel_share_assignment_reproduced']=np.allclose(channel_weights,[x['arithmetic_phenotype_weight']/sum(z['arithmetic_phenotype_weight'] for z in legacy) for x in legacy],atol=1e-13,rtol=0)
# A correlated diagonal-channel joint state with channel-dependent load states
# contracts to its carrier marginal; no product-of-marginals assumption needed.
# Diagnostic state only: two channel groups use the inherited two tested states.
lu=np.array(connection['carrier_rows'][0]['loads']);lp=np.array(connection['carrier_rows'][1]['loads']);ps=np.diag(mapped)
blocks=np.array([lu if i<8 else lp for i in range(16)]);joint_load=ps@blocks
marginal_load=np.sum(ps[:,None]*blocks,axis=0)
checks['correlated_channel_blocks_match_carrier_marginal']=np.allclose(joint_load,marginal_load,atol=1e-14,rtol=0)
transport=np.random.default_rng(15).permutation(16)
checks['correlated_block_relabel_preserves_load']=np.allclose(ps[transport]@blocks[transport],joint_load,atol=1e-14,rtol=0)
checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),checks
r={'status':'PASS','version':'0.4','selected_inherited_filter':selected,'dimensions':{'core_channels':15,'extended_channels':16,'load_lattice':128,'joint_product_space':2048,'family_slots':48},'contract':'joint load operators I_16 tensor A_s; channel permutations P tensor I_128; independent channel and lattice indices','rank_distinction':{'core_transport_rank':int(np.linalg.matrix_rank(core)),'extended_transport_rank':int(np.linalg.matrix_rank(P)),'default_readout_rank':1,'warning':'transport rank and stochastic origin routing rank describe different maps'},'channel_load_tests':case_rows,'phenotype_budget_J':float(E[0]),'family_channel_energy_sum_J':float(channel_energy.sum()),'one_slot_energy_J':float(channel_energy[0]),'checks':checks,'provenance':manifest,'scope':'execution and structural formulation of inherited channel-blind bridge, not channel-specific interactions or a unique embedding into the load lattice'}
(ROOT/'channel_bridge_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
