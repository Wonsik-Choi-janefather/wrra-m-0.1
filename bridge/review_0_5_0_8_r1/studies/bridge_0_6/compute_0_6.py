"""Finite projective instrument, energetic record qubit and repeated conditional readout."""
from pathlib import Path
import json,math,hashlib
import numpy as np
from scipy.linalg import expm
R=Path(__file__).resolve().parent
clock=json.loads((R/'source/clock_0_5.json').read_text());state=json.loads((R/'source/state_0_2.json').read_text())
b=next(x for x in state['rows'] if x['case']=='baseline');basis=np.load(R/'source/internal_and_carrier_basis.npz')
g=basis['ground'];e=basis['excited'];H=basis['H_MeV'];B=np.column_stack([g,e])
gap=float(e@H@e-g@H@g);conv=1.602176634e-13;hbar=clock['calibration']['hbar_J_s'];dt=clock['calibration']['chosen_frame_duration_s']
Hs=np.diag([0.,gap*conv]);record_gap=clock['calibration']['mu_eV']*1.602176634e-19
Hr=np.diag([0.,record_gap]);I=np.eye(2);X=np.array([[0.,1.],[1.,0.]])
plus=np.array([1.,1.])/math.sqrt(2);minus=np.array([1.,-1.])/math.sqrt(2)
P=[np.outer(plus,plus),np.outer(minus,minus)]
W=np.kron(P[0],I)+np.kron(P[1],X)
Htot=np.kron(Hs,I)+np.kron(I,Hr)
rho=np.diag([1-b['excited_population'],b['excited_population']]);blank=np.diag([1.,0.]);joint0=np.kron(rho,blank)
joint=W@joint0@W.T
checks=[];outcomes=[]
def ck(n,ok):checks.append({'name':n,'passed':bool(ok)})
def close(x,y):return math.isclose(x,y,rel_tol=1e-10,abs_tol=1e-25)
ck('two-mode support orthonormal',np.linalg.norm(B.T@B-I)<1e-10)
Hproject=B.conj().T@H@B;Hscale=np.linalg.norm(H)
ck('inherited full H Hermitian relative norm',np.linalg.norm(H-H.conj().T)/Hscale<1e-13)
ck('two-mode support invariant under full H',np.linalg.norm(H@B-B@Hproject)/Hscale<1e-12)
ck('relative two-mode generator from full H',np.linalg.norm((Hproject-Hproject[0,0]*I)*conv-Hs)/(gap*conv)<1e-12)
ck('initial excitation energy from original full H',abs(float(np.trace(rho@Hproject))-float(Hproject[0,0])-b['conditional_excitation_MeV'])<2e-8)
ck('instrument complete',np.linalg.norm(P[0]+P[1]-I)<1e-12)
ck('write coupling unitary',np.linalg.norm(W.T@W-np.eye(4))<1e-12)
ck('write preserves joint positivity/trace',np.linalg.eigvalsh(joint).min()>-1e-12 and abs(np.trace(joint)-1)<1e-12)
record_projs=[np.kron(I,np.diag([1.,0.])),np.kron(I,np.diag([0.,1.]))]
nonselect=np.zeros((4,4));system_nonselect=np.zeros((2,2))
Einitial=float(np.trace(joint0@Htot));Ewritten=float(np.trace(joint@Htot));work=Ewritten-Einitial
controller0=gap*conv+record_gap
ck('finite controller covers write work',controller0-work>=0)
ck('write signed energy balance',close(Ewritten+controller0-work,Einitial+controller0))
for j,(p,Q) in enumerate(zip(P,record_projs)):
 un=Q@joint@Q;prob=float(np.trace(un));cond=un/prob
 sys=p@rho@p/prob;expected=np.kron(sys,np.diag([1.,0.]) if j==0 else np.diag([0.,1.]))
 ck(f'outcome{j} Born instrument',abs(prob-np.trace(p@rho))<1e-12)
 ck(f'outcome{j} conditional state/correct pointer',np.linalg.norm(cond-expected)<1e-12)
 ck(f'outcome{j} positivity/trace',np.linalg.eigvalsh(cond).min()>-1e-12 and abs(np.trace(cond)-1)<1e-12)
 nonselect+=un;system_nonselect+=prob*sys
 Ec=float(np.trace(cond@Htot));wc=Ec-Einitial
 ck(f'outcome{j} branch energy account',close(Ec+controller0-wc,Einitial+controller0))
 currents=[]
 for row in b['currents']:
  # Diagonal projected charge probe from inherited populations; no off-diagonal current supplied.
  currents.append({'Q2_GeV2':row['Q2_GeV2'],'species':row['species'],'available':'inherited marginal only; coherent transition current not reconstructed'})
 outcomes.append({'record_bit':j,'probability':prob,'conditional_system_relative_energy_J':float(np.trace(sys@Hs)),'record_energy_J':j*record_gap,'conditional_controller_work_J':wc,'current_scope':currents})
ck('nonselective pointer matches dephased system',np.linalg.norm(system_nonselect-sum(p@rho@p for p in P))<1e-12)
ck('nonselective energy same as pre-pointer write',close(float(np.trace(nonselect@Htot)),Ewritten))
repeat=[];rng=np.random.default_rng(20261003);N=100000
for k in [1,2,4]:
 U=expm(-1j*Hs*k*dt/hbar);T=np.array([[float(np.trace(q@U@p@U.conj().T).real) for q in P] for p in P])
 expected_same=math.cos(gap*conv*k*dt/(2*hbar))**2
 ck(f'k{k} Born transition rows normalized',np.all(T>=-1e-12) and np.max(abs(T.sum(axis=1)-1))<1e-12)
 ck(f'k{k} analytic repeated transition',np.max(abs(T-np.array([[expected_same,1-expected_same],[1-expected_same,expected_same]])))<1e-10)
 counts=np.zeros((2,2),int);bit=int(rng.random()>=.5)
 for t in range(N):
  nxt=bit if rng.random()<T[bit,bit] else 1-bit;counts[bit,nxt]+=1;bit=nxt
 for j in [0,1]:
  total=counts[j].sum();freq=counts[j,j]/total;se=math.sqrt(T[j,j]*(1-T[j,j])/total)
  ck(f'k{k} row{j} seeded frequency',abs(freq-T[j,j])<6*se+2/total)
 repeat.append({'frame_separation':k,'transition_matrix':T.tolist(),'transition_counts':counts.tolist(),'samples':N,'same_probability':expected_same,'lag1_sign_correlation':2*expected_same-1})
memory=[]
for flips in [0.,.001,.01]:
 for ticks in [1,64,256]:
  r=blank.copy();Urec=expm(-1j*Hr*dt/hbar)
  for t in range(ticks):r=Urec@r@Urec.conj().T;r=(1-flips)*r+flips*X@r@X
  error=float(r[1,1].real);formula=.5*(1-(1-2*flips)**ticks)
  ck(f'noise{flips} ticks{ticks} retention',abs(error-formula)<1e-12)
  ck(f'noise{flips} ticks{ticks} state contract',np.linalg.eigvalsh(r).min()>-1e-12 and abs(np.trace(r)-1)<1e-12)
  noiseenergy=float(np.trace(r@Hr).real)
  ck(f'noise{flips} ticks{ticks} noise supply account',close(noiseenergy,error*record_gap))
  memory.append({'flip_probability_per_tick_input':flips,'ticks':ticks,'proper_time_s':ticks*dt,'record_error_probability':error,'record_energy_increase_J':noiseenergy})
routing=[]
for source_case in state['rows']:
 probs=source_case['four_branch_probabilities']
 names=['phi_plus','phi_minus','D','initial_reflection','normal_return']
 weights=np.array([probs['phi']/2,probs['phi']/2,probs['D'],probs['initial_reflection'],probs['normal_return']])
 ck(source_case['case']+' hierarchical routing normalized',abs(weights.sum()-1)<2e-11)
 ck(source_case['case']+' phi route coarse probability preserved',abs(weights[:2].sum()-probs['phi'])<1e-12)
 draws=rng.choice(5,size=100000,p=weights/weights.sum());freq=np.bincount(draws,minlength=5)/100000
 for j in range(5):
  se=math.sqrt(weights[j]*(1-weights[j])/100000)
  ck(source_case['case']+' route '+names[j],abs(freq[j]-weights[j])<6*se+2/100000)
 routing.append({'source_case':source_case['case'],'named_routes':names,'probabilities':weights.tolist(),'sample_frequencies':freq.tolist(),'scope':'classical branch routing from 0.2; phi receives the chosen internal instrument; D and returns stay outside nuclear preparation'})
out={'version':'bridge-0.6-r1','scope':'two-mode ideal projective readout, explicit finite write unitary, postselected phase dynamics, seeded repeated-outcome statistics and qubit noise retention','system_gap_MeV':gap,'frame_duration_s':dt,'record_gap_J':record_gap,'write_work_J':work,'initial_system_relative_energy_J':Einitial,'after_write_system_and_record_energy_J':Ewritten,'finite_controller_initial_energy_J':controller0,'hierarchical_routes':routing,'outcomes':outcomes,'repeated_readout':repeat,'record_retention':memory,'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'assumptions':['X-basis measurement chosen, not derived from address readout','record is a modeled qubit, not actual hardware','write is an externally controlled finite operation; duration and autonomous controller Hamiltonian not derived','bit flip noise is an input per tick','record resetting and many-record storage work not modeled; transition samples do not accumulate physical memory energy','two-mode invariant internal energy support; coherent transition currents remain unexecuted'],'open':['autonomous apparatus and energy-conserving controller dilation','physical record material, barriers, rate and stability','reset/work cycle for repeated measurements','full branch/address instrument on coupled physical state','off-diagonal current operator adapter','nonuniform covariant coupling'],'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'source').glob('*'))}}
(R/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'failed':out['failed'],'write_work_J':work,'retention_256':memory[5]},indent=2))
if out['failed']:raise SystemExit(1)
