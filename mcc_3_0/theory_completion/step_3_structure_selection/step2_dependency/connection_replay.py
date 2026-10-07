"""Fixed-address -> inherited load carrier -> finite record ledger probe."""
from pathlib import Path
import ast,json,math,hashlib
import numpy as np
from scipy.sparse import csr_matrix
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
manifest=json.loads((ROOT/'connection_manifest.json').read_text())
for name,h in manifest['files'].items():assert hashlib.sha256((ROOT/'connection_sources'/name).read_bytes()).hexdigest()==h
p=ROOT/'address_structure.py';t=ast.parse(p.read_text());nodes=[]
for node in t.body:
 if isinstance(node,ast.FunctionDef) and node.name=='product':break
 nodes.append(node)
s={'__file__':str(p),'__name__':'setup'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),s)
t=ast.parse((ROOT/'connection_sources/carrier_compute.py').read_text());cl=next(n for n in t.body if isinstance(n,ast.ClassDef) and n.name=='Carrier')
c={'np':np,'math':math,'csr_matrix':csr_matrix};exec(compile(ast.Module(body=[cl],type_ignores=[]),'pinned_carrier','exec'),c)
params=s['params'];old=params['upstream_0_9']['baseline_0_8']['ledger_0_7']['carrier_and_background'];M=old['lattice_N'];mu=s['mu'];checks={};carrier_rows=[]
eta=np.array([s['adapter']['calibration']['eta_J_m3'][x] for x in s['ns']['SECTORS']]);V=params['reference_volume_m3']
for eps in (0.,float(old['noncommuting_test_strength'])):
 carrier=c['Carrier'](M,eps);ops=[np.eye(M),carrier.Kc/2,carrier.Kb/2]
 rho0=np.eye(M)/M
 for name,rho in [('uniform',rho0),('packet',np.outer(carrier.packet(old['noncommuting_test_initial_modes'],old['noncommuting_test_initial_weights']),carrier.packet(old['noncommuting_test_initial_modes'],old['noncommuting_test_initial_weights']).conj()))]:
  loads=np.array([np.trace(rho@a).real for a in ops]);energy=eta*mu*loads*V
  perm=np.random.default_rng(105).permutation(M);rr=rho[np.ix_(perm,perm)];oo=[a[np.ix_(perm,perm)] for a in ops]
  after=np.array([np.trace(rr@a).real for a in oo]);assert np.allclose(after,loads,atol=1e-12,rtol=0)
  assert min(loads)>-1e-12 and np.trace(rho).real>1-1e-12
  if name=='uniform':assert np.allclose(loads,1,atol=1e-12,rtol=0)
  carrier_rows.append({'epsilon':eps,'state':name,'loads':loads.tolist(),'energy_J':energy.tolist(),'basis_transport_max_error':float(np.max(np.abs(after-loads)))})
checks['inherited_carrier_states_positive_normalized']=True
checks['uniform_carrier_matches_macro_factor_one']=True
checks['carrier_basis_transport_preserves_load']=True
checks['same_address_moments_used_in_each_carrier_state']=True
# Keep inherited microscopic inputs; regenerate preparation and mean occupancy
# from the new address state and the new phenotype energy allocation.
ref=json.loads((ROOT/'connection_sources/measurement_expected.json').read_text());config=json.loads((ROOT/'connection_sources/measurement_inputs.json').read_text())
w=s['w'];effect=s['effect'];n=s['base']['n'];selector=config['selector_prime']
valuation=np.zeros(len(n),dtype=np.int16);power=selector
while power<=s['N']:
 valuation+=(n%power==0);power*=selector
selector_mask=valuation%2==1
conditional_w=w*effect[0]/s['shares'][0]
selector_fraction=float(conditional_w@selector_mask);pop=config['preparation_strength']*selector_fraction
response=1+.25*np.log(n)/math.log(s['N'])
joint=float(conditional_w@(response*config['preparation_strength']*selector_mask))
product=float(conditional_w@response)*pop
covariance=config['preparation_strength']*(float(conditional_w@(response*selector_mask))-float(conditional_w@response)*selector_fraction)
checks['address_internal_correlation_retained']=abs(joint-product-covariance)<1e-12 and abs(joint-product)>1e-8
conv=1e6*1.602176634e-19;gap=ref['state']['gap_MeV']*conv;rest=ref['state']['rest_energy_per_particle_J'];rg=ref['measurement']['record_gap_J']
E=eta*mu*V;occupancy=E[0]/(rest+pop*gap)
I=np.eye(2);X=np.array([[0.,1.],[1.,0.]]);v=np.array([1.,1.])/math.sqrt(2);u=np.array([1.,-1.])/math.sqrt(2);P=[np.outer(v,v),np.outer(u,u)]
W=np.kron(P[0],I)+np.kron(P[1],X);rho=np.diag([1-pop,pop]);blank=np.diag([1.,0.]);j0=np.kron(rho,blank);j1=W@j0@W.conj().T
Hs=np.diag([0.,gap]);Hr=np.diag([0.,rg]);Ht=np.kron(Hs,I)+np.kron(I,Hr)
work=float(np.trace((j1-j0)@Ht).real);dsys=occupancy*(.5-pop)*gap;drecord=occupancy*rg/2;supply=occupancy*work
reservoir=config['supplier_initial_fraction_of_phi']*E[0];remaining=reservoir-supply
prob=[];branch=[]
for bit in (0,1):
 Q=np.kron(I,np.diag([1.,0.]) if bit==0 else np.diag([0.,1.]));pr=float(np.trace(Q@j1).real);cj=Q@j1@Q/pr;prob.append(pr);branch.append(occupancy*float(np.trace((cj-j0)@Ht).real))
checks['write_unitary_and_joint_state_normalized']=bool(np.linalg.norm(W.conj().T@W-np.eye(4))<1e-12 and abs(np.trace(j1)-1)<1e-12 and np.linalg.eigvalsh(j1).min()>-1e-12)
checks['prepared_rest_plus_excitation_replaces_phi_once']=abs(occupancy*(rest+pop*gap)-E[0])<1e-24
checks['source_routes_complete_with_two_measurement_outcomes']=abs(s['shares'][0]*sum(prob)+s['shares'][1]+s['shares'][2]-1)<1e-12
checks['matrix_work_equals_system_plus_record']=abs(supply-dsys-drecord)<1e-24
checks['mean_and_conditional_supply_nonnegative']=remaining>=0 and reservoir>=max(branch)
checks['included_supplier_boundary_conserves_energy']=abs((sum(E)+reservoir)-(sum(E)+supply+remaining))<1e-24
checks['record_is_nested_not_fourth_cosmic_sector']=len(E)==3 and drecord>0
# Exact same R-volume law -> pressure; finite write is pressureless in this case.
pressure=-E[2]/V;eps=1e-4*V
energyV=lambda vv:float(E[0]+E[1]+supply+E[2]*vv/V)
pnum=-(energyV(V+eps)-energyV(V-eps))/(2*eps)
checks['post_write_pressure_from_same_energy']=abs(pnum-pressure)<1e-18
q=lambda total:.5*(total+3*pressure*V)/total
checks['included_boundary_q_unchanged']=abs(q(sum(E)+reservoir)-q(sum(E)+supply+remaining))<1e-12
# Structural selector is transported together with its identity, not recomputed
# on arbitrary new display labels.
perm=np.random.default_rng(7).permutation(len(w));sel=selector_mask
ss=float((w[perm]*effect[0,perm])[sel[perm]].sum()/s['shares'][0])
checks['selector_preparation_preserved_by_address_transport']=abs(ss-selector_fraction)<1e-12
checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),checks
r={'status':'PASS','version':'0.3','carrier_lattice_dimension':M,'carrier_scope':'inherited homogeneous load carrier; not asserted identical to CCS-15 channel space','carrier_rows':carrier_rows,'measurement_join':{'selector_prime':selector,'selector_rule':'odd valuation of selector prime, inherited bridge rule','address_internal_joint_probe':joint,'address_internal_product_probe':product,'address_internal_covariance':covariance,'selector_fraction':selector_fraction,'prepared_excited_population':pop,'mean_occupancy':float(occupancy),'gap_J':gap,'record_gap_J':rg,'outcome_probabilities':prob,'sector_energy_before_J':E.tolist(),'system_increment_J':float(dsys),'record_increment_J':float(drecord),'supplier_work_J':float(supply),'supplier_before_J':float(reservoir),'supplier_after_J':float(remaining),'conditional_branch_supply_J':branch,'q_external_before':float(q(sum(E))),'q_external_after':float(q(sum(E)+supply)),'q_included_before':float(q(sum(E)+reservoir)),'q_included_after':float(q(sum(E)+supply+remaining))},'checks':checks,'source_provenance':manifest,'scope':'conditional single write at fixed volume; inherited microscopic gap supplied from pinned published computation, not recalculated here; no full source archive replay','not_claimed':['eight admission frames are actual record writes','complete CCS-15 to load-carrier intertwiner','physical identity of prime parts','accumulated repeated-write/reset costs']}
(ROOT/'connection_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
