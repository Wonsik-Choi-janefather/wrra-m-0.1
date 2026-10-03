"""Reference-matched replacement and signed excitation exchange, not abundance derivation."""
from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parent
read=lambda n:json.loads((R/'source'/n).read_text())
up=read('bridge_0_2_results.json');down=read('downstream_0_11_results.json');inp=read('internal_inputs.json')
base=next(x for x in up['rows'] if x['case']=='baseline')
uc=down['calibration_0_10_bridge']['ucrit_J_m3'];conv=1e6*1.602176634e-19
checks=[];rows=[]
def ck(n,b): checks.append({'name':n,'passed':bool(b)})
def close(a,b):return math.isclose(a,b,rel_tol=2e-12,abs_tol=1e-25)
def exchange(system,environment,delta):
 if not all(math.isfinite(x) for x in [system,environment,delta]) or system<0 or environment<0 or system+delta<0:raise ValueError('invalid energy input')
 if environment-delta < 0:raise ValueError('insufficient reservoir')
 return system+delta,environment-delta
ck('exact MeV SI conversion',close(conv,1.602176634e-13))
for cal,fr in [('inherited',[.0493,.265,.6857]),('alternate',[.05,.268,.682])]:
 Ephi=uc*fr[0];ED=uc*fr[1];ER=uc*fr[2]
 for species in ['proton','neutron']:
  rest=inp['masses'][species]*conv;eb=base['conditional_excitation_MeV']*conv
  # External matching: expected count in V0=1m3, NOT an integer realization or derived abundance.
  Nbar=Ephi/(rest+eb);Erest=Nbar*rest;Eexc=Nbar*eb
  label=cal+'_'+species
  ck(label+' reference replacement',close(Erest+Eexc,Ephi))
  ck(label+' total calibration preserved',close(Erest+Eexc+ED+ER,uc))
  ck(label+' split nonnegative',Nbar>0 and Erest>=0 and Eexc>=0)
  ck(label+' baseline no extra energy',close(Erest+Eexc+ED+ER,uc))
  # Reference reservoir is explicit finite test input; no microscopic reservoir law is claimed.
  reservoir0=.2*Ephi
  for row in up['rows']:
   tag=label+'_'+row['case'];energy=Nbar*row['conditional_excitation_MeV']*conv
   delta=energy-Eexc;old=Ephi+ED+ER
   system,environment=exchange(old,reservoir0,delta)
   ck(tag+' signed balance',close(system+environment,old+reservoir0))
   ck(tag+' replacement energy',close(system,Erest+energy+ED+ER))
   ck(tag+' D R unchanged',ED==uc*fr[1] and ER==uc*fr[2])
   ck(tag+' reservoir nonnegative',environment>=0)
   ck(tag+' reverse exchange',close(exchange(system,environment,-delta)[0],old) and close(exchange(system,environment,-delta)[1],reservoir0))
   # The naive sum adds the same phi allocation a second time at the reference.
   naive=uc+Erest+energy
   ck(tag+' naive duplicate detected',close(naive-system,Ephi))
   rows.append({'calibration':cal,'species':species,'case':row['case'],'V0_m3':1,'expected_population_input':Nbar,'rest_energy_per_particle_J':rest,'reference_phi_allocation_J':Ephi,'rest_total_J':Erest,'excitation_total_J':energy,'system_energy_J':system,'system_change_J':delta,'environment_initial_J':reservoir0,'environment_final_J':environment,'naive_double_count_total_J':naive,'duplicate_J':naive-system,'protocol':'fixed expected population; conditional preparation controls only'})
  # Ground-state reference removal returns stored excitation to environment.
  ground,env=exchange(uc,reservoir0,-Eexc)
  ck(label+' deexcitation balance',close(ground+env,uc+reservoir0))
  rejected=False
  try:exchange(uc,0,Eexc)
  except ValueError:rejected=True
  ck(label+' full excitation exhaustion rejected',rejected)
  # Alternate route at matched ground density: added excitation must come from reservoir,
  # not simultaneously retain the excited-state reference normalization.
  Ng=Ephi/rest;added=Ng*eb
  ck(label+' ground route distinct calibration',Ng>Nbar and added>0)
  ck(label+' ground route exchange conserved',close(sum(exchange(uc,2*added,added)),uc+2*added))
for bad in [(1.,1.,float('nan')),(1.,1.,float('inf')),(-1.,1.,0.),(1.,-1.,0.),(1.,1.,-2.)]:
 try:exchange(*bad)
 except ValueError:ck('invalid exchange '+str(bad),True)
 else:ck('invalid exchange '+str(bad),False)
out={'version':'bridge-0.3','scope':'finite signed energy account for externally matched expected nucleon population; no SI dynamics','unit_conversion_MeV_to_J':conv,'ucrit_J_m3':uc,'rows':rows,'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'policy':'replace existing reference phi allocation by matched rest+excitation; do not add it again','assumptions':['pure proton or pure neutron illustration, not mixed observed abundance','fixed expected population at V0; no particle creation','conditional preparation changes, not full SOURCE mass-transfer prediction','reservoir0=0.2*Ephi is a disclosed diagnostic input','D and R held fixed; address-weighted probes from 0.2 are not physical energy additions'],'open':['particle abundance and creation rest-energy supply','physical preparation apparatus and reservoir dynamics','source-branch changes with joint population transport','volume-dependent coupling and pressure in 0.4','proper time in 0.5','pre-existing downstream admission work is a separate ledger and is not added here'],'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'source').glob('*'))}}
(R/'results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'passed':out['passed'],'failed':out['failed'],'reference':rows[0],'control':rows[1]},indent=2))
if out['failed']:raise SystemExit(1)
