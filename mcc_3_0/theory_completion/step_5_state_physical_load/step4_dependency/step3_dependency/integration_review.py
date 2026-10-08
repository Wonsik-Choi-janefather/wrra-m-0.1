"""Replay the adopted kernel through the unchanged Step2 interfaces."""
from pathlib import Path
import ast,json,hashlib,math
import numpy as np
from phase_kernel import iter_frame_transfers
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
dep=json.loads((ROOT/'dependency_manifest.json').read_text())
for name,digest in dep['files'].items():assert hashlib.sha256((ROOT/'step2_dependency'/name).read_bytes()).hexdigest()==digest
p=ROOT/'step2_dependency/address_structure.py';nodes=[]
for node in ast.parse(p.read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name=='product':break
 nodes.append(node)
s={'__file__':str(p),'__name__':'setup'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),s)
cfg=s['cfg'];sp=cfg['upstream']['spectrum'];up=cfg['upstream']['update'];mask=s['struct_odd'];cost=s['cost'][2:][mask];w=s['w'];g=s['g'];K=up['admission_frames_K']
fingerprint=s['adapter']['fingerprint']({'cfg':cfg,'params':s['params'],'calibration':s['adapter']['calibration']})
checks={};cases=[];reference=json.loads((ROOT/'step2_dependency/connection_results.json').read_text())['measurement_join']
oldref=json.loads((ROOT/'step2_dependency/connection_sources/measurement_expected.json').read_text());gap=oldref['state']['gap_MeV']*1e6*1.602176634e-19;rest=oldref['state']['rest_energy_per_particle_J'];rg=oldref['measurement']['record_gap_J'];n=s['base']['n'];v3=np.zeros(len(n),np.int16);power=3
while power<=s['N']:v3+=n%power==0;power*=3
selector=v3[mask]%2==1
for method in ('direct','rotation'):
 admitted=np.zeros(len(cost));remaining=np.zeros(len(cost));frame_shares=np.zeros(K)
 for lo,hi,k,birth,residue in iter_frame_transfers(cost,sp['gamma'],sp['coefficients'],sp['phase_offsets'],up['phase_step_xi'],up['sigmoid_threshold_h'],K,method=method):
  admitted[lo:hi]+=birth;frame_shares[k]+=float(w[mask][lo:hi]@birth)
  if residue is not None:remaining[lo:hi]=residue
 effect=np.array([np.zeros(len(w)),s['struct_even'].astype(float),1-s['struct_even'].astype(float)]);effect[0,mask]=admitted;effect[2,mask]=remaining
 assert np.allclose(effect,s['effect'],atol=2e-13,rtol=0)
 assert np.allclose(admitted+remaining,1,atol=2e-14,rtol=0)
 shares=effect@w;mu=(effect*g*w).sum(axis=1);macro=s['adapter']['macro'](mu)
 fraction=float((w[mask]*admitted)@selector/shares[0]);population=.2*fraction;EP=macro['E0_sector_J'][0];count=EP/(rest+population*gap);work=count*((.5-population)*gap+rg/2)
 assert abs(fraction-reference['selector_fraction'])<1e-12
 assert math.isclose(work,reference['supplier_work_J'],rel_tol=2e-12,abs_tol=1e-24)
 out=macro['rows'][1];original=s['reference_macro']['rows'][1]
 for key in ('q','rotation_km_s','lensing_arcsec','pressure_Pa','H_over_H0'):assert math.isclose(out[key],original[key],rel_tol=2e-12,abs_tol=1e-24)
 cases.append({'method':method,'shares':shares.tolist(),'address_moments':mu.tolist(),'frame_contributions':frame_shares.tolist(),'selector_fraction':fraction,'prepared_population':population,'single_write_supply_J':work,'present_macro':out})
checks['both_kernels_reproduce_every_original_address_effect']=True
checks['candidate_transfers_and_final_residue_conserve_each_address']=True
checks['internal_preparation_and_record_supply_preserved']=True
checks['same_load_energy_pressure_and_macro_outputs_preserved']=True
checks['both_implementations_preserve_frame_contributions']=bool(np.allclose(cases[0]['frame_contributions'],cases[1]['frame_contributions'],atol=2e-13,rtol=0))
# Same kernel on a different frame reference with transported spectral offsets.
shift=.37;offset=(np.array(sp['phase_offsets'])-np.array(sp['gamma'])*shift).tolist();adm=np.zeros(len(cost))
for lo,hi,k,birth,_ in iter_frame_transfers(cost+shift,sp['gamma'],sp['coefficients'],offset,up['phase_step_xi'],up['sigmoid_threshold_h'],K):adm[lo:hi]+=birth
checks['transported_phase_reference_preserves_adopted_kernel']=bool(np.allclose(adm,s['effect'][0,mask],atol=2e-13,rtol=0))
checks['frozen_model_inputs_not_modified']=fingerprint==s['adapter']['fingerprint']({'cfg':cfg,'params':s['params'],'calibration':s['adapter']['calibration']})
# Only actual rejected malformed calls count as fail-closed evidence.
invalid=[{'chunk':0},{'frames':True},{'method':'unknown'},{'threshold':float('nan')}];rejections=0
for change in invalid:
 args={'cost':cost[:2],'gamma':sp['gamma'],'coefficients':sp['coefficients'],'offsets':sp['phase_offsets'],'phase_step':up['phase_step_xi'],'threshold':up['sigmoid_threshold_h'],'frames':K};args.update(change)
 try:list(iter_frame_transfers(**args))
 except ValueError:rejections+=1
checks['invalid_kernel_inputs_rejected']=rejections==len(invalid)
checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),checks
r={'status':'PASS','version':'0.4','date':'2026-10-08','cases':cases,'checks':checks,'frozen_input_hash':fingerprint,'rejected_input_cases':rejections,'scope':'adopted equivalent implementation through existing conditional Step2 ledger; not new empirical model validation','adoption':{'same_theory_parameters':True,'phase_modes':4,'real_linear_generator_states':8,'admission_frames':K,'selected_kernel':'rotation','chunk':65536,'direct_reference_retained':True}}
(ROOT/'integration_review_results.json').write_text(json.dumps(r,indent=2));print(json.dumps({'status':'PASS','checks':checks,'adoption':r['adoption']},indent=2))
