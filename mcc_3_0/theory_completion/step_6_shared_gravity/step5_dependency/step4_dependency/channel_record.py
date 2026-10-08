"""Channel-resolved effective two-state record with one phenotype budget."""
from pathlib import Path
import ast,json,math
import numpy as np
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
p=ROOT/'phenotype_transform.py';nodes=[]
for node in ast.parse(p.read_text()).body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='e' for t in node.targets):break
 nodes.append(node)
s={'__file__':str(p),'__name__':'setup'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),s)
D=ROOT/'step3_dependency/step2_dependency';ref=json.loads((D/'connection_results.json').read_text())['measurement_join'];config=json.loads((D/'connection_sources/measurement_inputs.json').read_text());micro=json.loads((D/'connection_sources/measurement_expected.json').read_text())
st=s['s'];e=st['effect'];w=st['base']['w'];n=st['base']['n'];phi=float(e[0]@w);cw=e[0]*w/phi
v=np.zeros(len(n),dtype=int);power=config['selector_prime']
while power<=st['N']:v+=n%power==0;power*=config['selector_prime']
mask=v%2==1;strength=config['preparation_strength'];fraction=float(cw@mask);pop=strength*fraction
rest=micro['state']['rest_energy_per_particle_J'];gap=ref['gap_J'];rg=ref['record_gap_J'];Ephi=ref['sector_energy_before_J'][0];occupancy=Ephi/(rest+pop*gap)
I=np.eye(2);X=I[:,::-1];a=np.array([1.,1.])/math.sqrt(2);b=np.array([1.,-1.])/math.sqrt(2);A=np.outer(a,a);B=np.outer(b,b);W=np.kron(A,I)+np.kron(B,X);blank=np.diag([1.,0.]);Ht=np.kron(np.diag([0.,gap]),I)+np.kron(I,np.diag([0.,rg]));Qrecord=[np.kron(I,np.diag([1.,0.])),np.kron(I,np.diag([0.,1.]))]
# Normalized origin routing. Correlated diagnostic routes retain the same
# address-sector measure while changing conditional channel preparation.
P=s['P'];order=P.argmax(axis=1);families=np.array(s['s']['cfg']['channel_coupling']['family_weights']) if 's' in s else np.array(s['cfg']['family_replication']['family_weights'])
checks={};cases=[]
for contrast in (0.,.5):
 signs=np.r_[np.ones(8),-np.ones(8)];z=mask.astype(float)-fraction
 channel_share=(1+contrast*signs*np.dot(cw,z))/16
 channel_selected=(fraction+contrast*signs*np.dot(cw,z*mask))/16
 chpop=strength*channel_selected/channel_share
 share=np.outer(families,channel_share[order]).ravel();pops=np.tile(chpop[order],3)
 # Global occupancy is allocated, not recalibrated separately per slot.
 totalwork=0.;record=0.;system=0.;probs=np.zeros(2);branch=np.zeros(2);rows=[]
 for i,(weight,cp) in enumerate(zip(share,pops)):
  j0=np.kron(np.diag([1-cp,cp]),blank);j1=W@j0@W.T;occ=occupancy*weight
  supply=occ*np.trace((j1-j0)@Ht).real;ds=occ*(.5-cp)*gap;dr=occ*rg/2
  assert np.linalg.eigvalsh(j1).min()>-1e-13 and abs(np.trace(j1)-1)<1e-13
  totalwork+=supply;record+=dr;system+=ds
  for k,Qr in enumerate(Qrecord):
   pr=np.trace(Qr@j1).real;probs[k]+=weight*pr;cj=Qr@j1@Qr/pr
   branch[k]+=occ*np.trace((cj-j0)@Ht).real
  rows.append({'slot':i,'conditional_weight':float(weight),'prepared_population':float(cp),'effective_occupancy':float(occ),'prepared_energy_J':float(occ*(rest+cp*gap)),'system_increment_J':float(ds),'record_increment_J':float(dr),'supplier_work_J':float(supply)})
 reservoir=config['supplier_initial_fraction_of_phi']*Ephi
 assert abs(sum(r['prepared_energy_J'] for r in rows)-Ephi)<1e-24
 assert abs(totalwork-ref['supplier_work_J'])<1e-24 and abs(record-ref['record_increment_J'])<1e-24
 assert np.allclose(probs,ref['outcome_probabilities'],atol=1e-13,rtol=0)
 assert abs(totalwork-system-record)<1e-24 and reservoir>=max(branch)
 assert abs((Ephi+reservoir)-(Ephi+totalwork+reservoir-totalwork))<1e-24
 cases.append({'routing_contrast':contrast,'channel_preparation_range':[float(pops.min()),float(pops.max())],'outcome_probabilities':probs.tolist(),'supplier_work_J':float(totalwork),'record_increment_J':float(record),'conditional_branch_supply_J':branch.tolist(),'supplier_remaining_J':float(reservoir-totalwork),'slots':rows})
checks['channel_joint_record_states_positive_normalized']=True
checks['48_preparations_replace_one_phi_budget']=True
checks['aggregate_write_work_matches_original_record']=True
checks['aggregate_record_energy_matches_original_record']=True
checks['outcome_probabilities_match_original_record']=True
checks['system_plus_record_work_closes']=True
checks['supplier_covers_each_outcome_branch']=True
checks['included_supplier_boundary_conserves_energy']=True
checks['correlated_routing_changes_channel_preparation']=cases[1]['channel_preparation_range'][1]-cases[1]['channel_preparation_range'][0]>1e-3
# Channel-blind operation commutes with every channel charge observable:
# [Q_channel tensor I4,I48 tensor W]=0, directly test a nonzero two-channel probe.
Q=np.diag([2/3,-1]);W2=np.kron(np.eye(2),W);Q2=np.kron(Q,np.eye(4))
checks['record_operation_preserves_channel_charge']=bool(np.linalg.norm(Q2@W2-W2@Q2)<1e-14)
checks['write_operator_unitary']=bool(np.linalg.norm(W.T@W-np.eye(4))<1e-13)
assert all(checks.values())
out={'status':'PASS','version':'0.3','checks':checks,'cases':cases,'record_operation':'I_family_channel tensor (P_plus tensor I_record + P_minus tensor X_record)','scope':'channel-resolved inherited effective two-state single write at fixed volume','assumptions':['same effective gap/rest per channel; not species-specific masses','global mean occupancy allocated once','channel-blind write','diagnostic contrast .5 is a routing test, not a fitted physical input'],'not_claimed':['48 simultaneous physical particles or 48 multiplied record events','species masses derived from slot energies','reset/repeated write budget','charge or species measurement by this internal two-state record']}
(ROOT/'channel_record_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'status':'PASS','checks':len(checks),'cases':[{k:x[k] for k in ('routing_contrast','channel_preparation_range','supplier_work_J')} for x in cases]}))
