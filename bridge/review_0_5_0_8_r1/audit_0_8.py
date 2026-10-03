"""Final review checks, boundary ledger diagnostics and dependency sensitivity probes.
Diagnostics do not supply missing autonomous apparatus or covariant field dynamics.
"""
from pathlib import Path
import json,math,hashlib,tempfile,shutil,subprocess,sys,os,zipfile
import numpy as np
from scipy.linalg import expm
R=Path(__file__).resolve().parent;S=R/'studies';checks=[]
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(name,b,category='cross_contract'):checks.append({'name':name,'category':category,'passed':bool(b)})
def close(a,b):return math.isclose(a,b,rel_tol=2e-11,abs_tol=1e-25)
frozen=read(R/'frozen_stage_results.json');stage=[];result={}
for k in range(1,8):
 d=S/f'bridge_0_{k}';f=d/('audit_results.json' if k==1 else 'results.json');r=read(f);result[k]=r
 ck(f'0.{k} recorded check count',r['passed']==sum(bool(x['passed']) for x in r['checks']) and r['failed']==sum(not x['passed'] for x in r['checks']),'provenance')
 ck(f'0.{k} stage checks pass',r['failed']==0,'provenance')
 ck(f'0.{k} frozen numerical result byte identity',digest(f)==frozen[f'0.{k}'],'provenance')
 stage.append({'stage':f'0.{k}','passed':r['passed'],'failed':r['failed'],'result_sha256':digest(f)})
a,b,c,d,e,f,g=[result[k] for k in range(1,8)]
# Verify current source bytes against every result's declared source hashes.
for k in [1,2,3,4,5,6,7]:
 item=result[k];base=S/f'bridge_0_{k}'
 if k==4:
  ck('0.4 source hash',digest(base/'source/bridge_0_3_results.json')==item['source_sha256'],'provenance');continue
 hashes=item['sources_sha256'] if k==1 else item['source_sha256']
 for name,value in hashes.items():
  p=base/name if k==1 else base/'wrra-m'/name if k==2 else base/'source'/name
  ck(f'0.{k} source hash {name}',digest(p)==value,'provenance')
links=[(2,'results.json',3,'bridge_0_2_results.json'),(3,'results.json',4,'bridge_0_3_results.json'),(2,'results.json',5,'bridge_0_2_results.json'),(2,'internal_and_carrier_basis.npz',5,'internal_and_carrier_basis.npz'),(2,'results.json',6,'state_0_2.json'),(2,'internal_and_carrier_basis.npz',6,'internal_and_carrier_basis.npz'),(5,'results.json',6,'clock_0_5.json'),(2,'results.json',7,'state_0_2.json'),(5,'results.json',7,'clock_0_5.json'),(6,'results.json',7,'measurement_0_6.json')]
for k,n,j,target in links:ck(f'fresh 0.{k} {n} -> 0.{j} {target}',digest(S/f'bridge_0_{k}'/n)==digest(S/f'bridge_0_{j}'/'source'/target),'provenance')
# Retain all 36 prior cross-stage energy/pressure checks.
for row in b['rows']:
 for species in ['proton','neutron']:
  for cal in ['inherited','alternate']:
   energy=next(x for x in c['rows'] if x['case']==row['case'] and x['species']==species and x['calibration']==cal)
   load=next(x for x in d['rows'] if x['a']==1 and x['boundary']=='external' and x['case']==row['case'] and x['species']==species and x['calibration']==cal)
   ck(cal+' '+species+' '+row['case']+' SI propagation',close(energy['excitation_total_J'],energy['expected_population_input']*row['conditional_excitation_MeV']*c['unit_conversion_MeV_to_J']))
   ck(cal+' '+species+' '+row['case']+' gravity propagation',close(load['E_J'],energy['system_energy_J']))
for cal in ['inherited','alternate']:
 for species in ['proton','neutron']:
  vals=[x['E_J'] for x in d['rows'] if x['a']==1 and x['boundary']=='included_pressureless' and x['species']==species and x['calibration']==cal]
  ck(cal+' '+species+' closed preparation total load constant',max(vals)-min(vals)<1e-22)
base=next(x for x in b['rows'] if x['case']=='baseline');p=base['excited_population'];gap=f['system_gap_MeV'];conv=c['unit_conversion_MeV_to_J']
ck('0.2 population times same 0.6 gap gives excitation',close(p*gap,base['conditional_excitation_MeV']))
ck('0.5 clock duration forwarded to 0.6',close(e['calibration']['chosen_frame_duration_s'],f['frame_duration_s']))
ck('0.7 initial population forwarded from 0.2',close(g['inputs']['population_from_0_2'],p))
ck('0.6 relative system initial energy matches 0.2',close(f['initial_system_relative_energy_J'],p*gap*conv))
ck('measurement outcome weights sum to one',close(sum(x['probability'] for x in f['outcomes']),1.))
# Reconstruct the declared finite X instrument rather than trust its energy rows.
I=np.eye(2);X=np.array([[0.,1.],[1.,0.]]);v=np.array([1.,1.])/math.sqrt(2);P=np.outer(v,v);Q=I-P
W=np.kron(P,I)+np.kron(Q,X);Hs=np.diag([0.,gap*conv]);Hr=np.diag([0.,f['record_gap_J']]);rho=np.diag([1-p,p]);blank=np.diag([1.,0.])
joint=W@np.kron(rho,blank)@W.T
post=joint.reshape(2,2,2,2).trace(axis1=1,axis2=3)
record=joint.reshape(2,2,2,2).trace(axis1=0,axis2=2)
ck('nonselective internal state is I/2',np.linalg.norm(post-I/2)<1e-12)
ck('pointer internal state has population .5',close(float(post[1,1]),.5))
ck('pointer marginal is I/2',np.linalg.norm(record-I/2)<1e-12)
ck('after-write reported energy includes system and record once',close(float(np.trace(post@Hs)+np.trace(record@Hr)),f['after_write_system_and_record_energy_J']))
system_delta=(.5-p)*gap*conv;record_delta=.5*f['record_gap_J']
ck('controller work equals excitation change plus record change',close(system_delta+record_delta,f['write_work_J']))
ck('write work positive for adopted baseline',system_delta>0 and record_delta>0)
# Boundary diagnostic: insert this ideal readout energy change into the 0.3/0.4 ledger.
# No actual apparatus distribution or time-resolved exchange is inferred.
ledger=[]
for item in c['rows']:
 if item['case']!='baseline':continue
 N=item['expected_population_input'];dS=N*system_delta;dR=N*record_delta;work=N*f['write_work_J'];env0=item['environment_initial_J'];env1=env0-work
 uc=c['ucrit_J_m3'];fr=[.0493,.265,.6857] if item['calibration']=='inherited' else [.05,.268,.682];L=uc*fr[2]
 q_before=(uc-3*L)/(2*uc);external_energy=uc+dS+dR;included_energy=external_energy+env1
 q_after=(external_energy-3*L)/(2*external_energy);q_included=(included_energy-3*L)/(2*included_energy)
 tag=item['calibration']+' '+item['species']
 ck(tag+' expected-population measurement cost',close(work,dS+dR),'boundary_diagnostic')
 ck(tag+' inherited finite reservoir covers ideal readout',env1>=0,'boundary_diagnostic')
 ck(tag+' included system record controller balance',close(included_energy,uc+env0),'boundary_diagnostic')
 ck(tag+' external load change equals supplied work',close(external_energy-uc,work),'boundary_diagnostic')
 ck(tag+' included pressureless q independent of readout redistribution',close(q_included,(uc+env0-3*L)/(2*(uc+env0))),'boundary_diagnostic')
 ck(tag+' external q responds to ideal readout load',q_after>q_before,'boundary_diagnostic')
 # Pressure after the finite write, under the existing fixed comoving constitutive law.
 M=external_energy-L;h=1e-3;Pfd=-((M+L*(1+h))-(M+L*(1-h)))/(2*h)
 ck(tag+' same energy gives unchanged post-write background pressure',close(Pfd,-L),'boundary_diagnostic')
 ledger.append({'calibration':item['calibration'],'species':item['species'],'expected_population_input':N,'system_excitation_increase_J':dS,'record_energy_increase_J':dR,'controller_supply_J':work,'reservoir_before_J':env0,'reservoir_after_J':env1,'external_q_before':q_before,'external_q_after':q_after,'included_pressureless_q':q_included,'scope':'conditional mean ledger insertion at V=1 m3; post-write pressure law adopted from 0.4; not time-resolved apparatus or covariant evolution'})
for rr in f['repeated_readout']:
 k=rr['frame_separation'];angle=gap*conv*k*f['frame_duration_s']/e['calibration']['hbar_J_s'];prob=math.cos(angle/2)**2
 ck(f'repeated k{k} same-generator clock phase',close(prob,rr['same_probability']))
for rr in f['record_retention']:
 expected=.5*(1-(1-2*rr['flip_probability_per_tick_input'])**rr['ticks'])
 ck('retention '+str(rr['ticks'])+' noise '+str(rr['flip_probability_per_tick_input']),close(expected,rr['record_error_probability']))
# Explicit counterexamples to invalid all-stage claims.
ck('old slow clock equality still fails',not close(e['failed_clock_ratio_preserved'],1.))
ck('SI gravity calibration still explicitly absent','not derived SI G calibration' in g['clock_interface'])
ck('0.7 field source is occupancy not stress energy',g['inputs']['source']=='transported occupancy density; equal source weight of internal components')
ck('0.7 populations remain baseline, not measured .5',not close(g['inputs']['population_from_0_2'],float(post[1,1])))
ck('0.4 fixed prepared-state scope differs from measurement changing populations','fixed comoving particle count and prepared internal state' in d['constitutive_rule'])
# Behavioral probes in isolated copies: detect provenance-only inputs and real dependencies.
probes=[];env=dict(os.environ,OPENBLAS_NUM_THREADS='1');env.pop('WRRA_REPO',None)
for name,k,source,change in [
 ('0.7 clock is provenance-only',7,'clock_0_5.json',lambda x:x['calibration'].__setitem__('chosen_driver_rate_s_minus1',x['calibration']['chosen_driver_rate_s_minus1']*2)),
 ('0.7 measurement is provenance-only',7,'measurement_0_6.json',lambda x:x.__setitem__('write_work_J',x['write_work_J']*2)),
 ('0.7 state population is a numerical dependency',7,'state_0_2.json',lambda x:next(r for r in x['rows'] if r['case']=='baseline').__setitem__('excited_population',.12)),
 ('0.6 frame duration is a numerical dependency',6,'clock_0_5.json',lambda x:x['calibration'].__setitem__('chosen_frame_duration_s',x['calibration']['chosen_frame_duration_s']*2))]:
 with tempfile.TemporaryDirectory() as td:
  target=Path(td)/'study';shutil.copytree(S/f'bridge_0_{k}',target,ignore=shutil.ignore_patterns('__pycache__'))
  sf=target/'source'/source;x=read(sf);change(x);sf.write_text(json.dumps(x,indent=2))
  run=subprocess.run([sys.executable,str(target/f'compute_0_{k}.py')],env=env,capture_output=True,text=True)
  ck(name+' probe run passes',run.returncode==0,'dependency_probe')
  if run.returncode:raise RuntimeError(run.stderr+run.stdout)
  test=read(target/'results.json')
  if k==7:
   delta=float(np.max(abs(np.array(test['runs'][2]['final_density'])-np.array(g['runs'][2]['final_density']))))
   same=test['runs']==g['runs'] and test['convergence']==g['convergence']
   ok=same if 'provenance-only' in name else delta>1e-5
  else:
   delta=float(np.max(abs(np.array(test['repeated_readout'][0]['transition_matrix'])-np.array(f['repeated_readout'][0]['transition_matrix']))));ok=delta>1e-5
  ck(name+' behavior matches declared dependency',ok,'dependency_probe')
  probes.append({'name':name,'numerical_difference':delta,'behavior_confirmed':bool(ok),'scope':'single declared input perturbation; no new physical model coupling'})
contracts=[
 {'edge':'0.2 -> 0.3 -> 0.4','status':'executed','payload':'conditional excitation -> matched SI energy -> homogeneous pressure and FRW','limit':'external expected population, species and volume laws'},
 {'edge':'0.2 + 0.5 -> 0.6','status':'executed','payload':'same internal gap and adopted proper frame -> ideal measurement/repeated phase','limit':'controlled instrument; autonomous apparatus and reset absent'},
 {'edge':'0.2 -> 0.7','status':'executed','payload':'baseline mode population -> constructed nonuniform occupancy field feedback','limit':'dimensionless nonrelativistic effective source'},
 {'edge':'0.5 -> 0.7','status':'provenance_only','payload':'clock snapshot and possible s=omega*tau convention','limit':'SI kinetic/length/G coefficients absent; rate perturbation leaves runs unchanged'},
 {'edge':'0.6 -> 0.7','status':'provenance_only','payload':'measurement snapshot','limit':'state/controller/record update not consumed by field evolution'},
 {'edge':'0.6 -> 0.3/0.4 readout ledger','status':'review_diagnostic','payload':'mean write work and signed reservoir insertion calculated in 0.8','limit':'conditional expected population and pressureless included reservoir; no Q(t) or apparatus geometry'},
 {'edge':'source -> preparation apparatus','status':'open','payload':'actual coupling and finite supply dynamics','limit':'no autonomous joint Hamiltonian execution'},
 {'edge':'homogeneous + nonuniform -> one covariant geometry','status':'open','payload':'energy-momentum tensor, metric and common SI scale','limit':'periodic mean-subtracted Poisson zero mode does not generate FRW background'}]
comparison=read(R/'numerical_comparison.json')
with zipfile.ZipFile(R/'historical/bridge_0_8_original.zip') as original:
 for k in range(1,8):
  name=f'bridge_0_8/studies/bridge_0_{k}/'+('audit_results.json' if k==1 else 'results.json')
  old=json.loads(original.read(name));new=result[k]
  omit={'version','checks','passed','failed','source_sha256','inputs'} if k==7 else {'version','checks','passed','failed','source_sha256'}
  same=all(old[x]==new[x] for x in old if x not in omit)
  if k==7:same=same and all(old['inputs'][x]==new['inputs'][x] for x in old['inputs'])
  recorded=next(x for x in comparison['rows'] if x['stage']==f'0.{k}')
  ck(f'0.{k} original numerical payload preserved',same and recorded['numerical_payload_unchanged'],'revision_review')
issues=read(R/'final_issue_register.json')['issues']
ck('all ten original bridge issues retained',sorted(x['id'] for x in issues)==[f'B{i:02}' for i in range(1,11)],'revision_review')
ck('covariant issue B09 remains open in scope',next(x for x in issues if x['id']=='B09')['status']=='effective_feedback_with_open_covariant_bridge','revision_review')
scientific_failures=[{'claim':'old slow schedule is the physical SI source clock','status':'failed','witness_ratio':e['failed_clock_ratio_preserved']},{'claim':'all stages form a single autonomously coupled covariant simulator','status':'not established','witness':'clock/measurement perturbations leave 0.7 numerical runs identical; 0.7 uses occupancy, not stress-energy'}]
report={'version':'bridge-0.8-r1','authors':['Wonsik Choi','Jeongin Choi'],'stages':stage,'stage_case_checks':sum(x['passed'] for x in stage),'review_checks':checks,'review_passed':sum(x['passed'] for x in checks),'review_failed':sum(not x['passed'] for x in checks),'total_case_checks':sum(x['passed'] for x in stage)+sum(x['passed'] for x in checks),'count_scope':'implementation/mathematical case checks including provenance and expected counterexamples; not independent experiments; prior 36 cross checks retained once','ideal_readout_boundary_diagnostics':ledger,'dependency_probes':probes,'contracts':contracts,'failed_or_unestablished_claims':scientific_failures,'verdict':{'bridge_development':'closed at 0.8 within declared finite conditional implementation scope','full_covariant_bridge':'open, not supplied by this review','reproduction':'known outputs reproduced; legitimate explanatory achievements under declared calibration','prediction':'unmeasured outputs after fixing verified inputs and construction choices are conditional WRRA model predictions; empirical accuracy awaits matching observations','closure':'upstream 0.10; downstream 0.12; bridge 0.8; 1.0 publication consolidation; corrections r1/r2; no automatic additional development stage'},'source_result_sha256':frozen}
(R/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'stage_checks':report['stage_case_checks'],'review_passed':report['review_passed'],'review_failed':report['review_failed'],'total':report['total_case_checks'],'boundary_diagnostics':ledger,'dependency_probes':probes},ensure_ascii=False,indent=2))
if report['review_failed']:raise SystemExit(1)
