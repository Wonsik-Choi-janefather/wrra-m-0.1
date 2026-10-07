"""Fairly calibrated spectral reductions of the same finite readout family."""
from pathlib import Path
import ast,json,hashlib,math,itertools
import numpy as np
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
dep=json.loads((ROOT/'dependency_manifest.json').read_text())
for name,digest in dep['files'].items():assert hashlib.sha256((ROOT/'step2_dependency'/name).read_bytes()).hexdigest()==digest
p=ROOT/'step2_dependency/address_structure.py';nodes=[]
for node in ast.parse(p.read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name=='product':break
 nodes.append(node)
s={'__file__':str(p),'__name__':'setup'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),s)
cfg=s['cfg'];sp=cfg['upstream']['spectrum'];up=cfg['upstream']['update'];gamma=np.array(sp['gamma']);co=np.array(sp['coefficients']);offset=np.array(sp['phase_offsets']);xi=up['phase_step_xi'];K=up['admission_frames_K'];h0=up['sigmoid_threshold_h']
mask=s['struct_odd'];even=s['struct_even'];n=s['base']['n'];cost=s['cost'][2:];w=s['w'];g=s['g'];ref=s['effect'][0,mask];target=float(s['shares'][0])
base_drives=np.array([[co[j]*np.cos(gamma[j]*(cost[mask]+xi*k)+offset[j]) for k in range(K)] for j in range(len(gamma))])
v3=np.zeros(len(n),np.int16);power=3
while power<=s['N']:v3+=n%power==0;power*=3
selector=v3[mask]%2==1
origin=json.loads((ROOT/'step2_dependency/connection_sources/measurement_expected.json').read_text());gap=origin['state']['gap_MeV']*1e6*1.602176634e-19;rest=origin['state']['rest_energy_per_particle_J'];rg=origin['measurement']['record_gap_J'];EP=s['adapter']['macro'](s['mu'])['E0_sector_J'][0]
rows=[]
# Every nonempty subset is tested. This is a finite complete ablation family,
# not a search over all possible frequencies or physical models.
for J in range(1,len(gamma)+1):
 for ids in itertools.combinations(range(len(gamma)),J):
  # Fix total spectral coefficient sum by an explicit shared normalization rule.
  scale=float(co.sum()/co[list(ids)].sum());drive=base_drives[list(ids)].sum(axis=0)*scale
  def admitted(h):return -np.expm1((-np.logaddexp(0,drive-h)).sum(axis=0))
  h=brentq(lambda hh:float(w[mask]@admitted(hh))-target,-50,50,xtol=1e-13)
  adm=admitted(h);effect=np.array([np.zeros(len(w)),even.astype(float),1-even.astype(float)]);effect[0,mask]=adm;effect[2,mask]-=adm
  shares=effect@w;mu=(effect*g*w).sum(axis=1)
  assert np.allclose(shares,s['shares'],atol=2e-12,rtol=0)
  fraction=float((w[mask]*adm)@selector/shares[0]);population=.2*fraction;count=EP/(rest+population*gap)
  work=count*((.5-population)*gap+rg/2)
  q=s['adapter']['macro'](mu)['rows'][1]['q']
  rows.append({'mode_indices_one_based':[j+1 for j in ids],'modes':J,'coefficient_rescale_rule':'preserve sum of inherited coefficients','coefficient_scale':scale,'alpha':cfg['upstream']['state']['alpha'],'calibrated_h':h,'shares':shares.tolist(),'address_moments':mu.tolist(),'weighted_address_readout_difference':float(w[mask]@np.abs(adm-ref)),'maximum_address_readout_difference':float(np.max(np.abs(adm-ref))),'selector_fraction':fraction,'prepared_excited_population':population,'conditional_mean_write_work_J':float(work),'present_q':q,'minimum_real_linear_generator_states':2*J,'two_target_calibration_parameters':2,'stored_spectrum_entries':3*J,'trig_calls_direct_per_eligible_address':J*K,'baseline':J==len(gamma)})
checks={'all_fifteen_nonempty_subsets_tested':len(rows)==15,'same_verified_shares_for_every_subset':all(np.allclose(x['shares'],s['shares'],atol=2e-12,rtol=0) for x in rows),'no_SI_or_dark_readout_refit':all(x['alpha']==cfg['upstream']['state']['alpha'] for x in rows),'full_spectrum_reproduces_frozen_address_readout':rows[-1]['maximum_address_readout_difference']<2e-13,'every_proper_subset_changes_address_readout':all(x['weighted_address_readout_difference']>1e-7 for x in rows[:-1]),'full_spectrum_threshold_reproduced':abs(rows[-1]['calibrated_h']-h0)<1e-10}
checks={k:bool(v) for k,v in checks.items()};assert all(checks.values())
# This is comparison output, not an observational loss function.
best_reduced=min(rows[:-1],key=lambda x:x['weighted_address_readout_difference'])
r={'status':'PASS','version':'0.3','date':'2026-10-08','family':'all15 nonempty subsets of the inherited four frequencies, fixed total coefficient sum, fixed8 frames, equal legitimate two-share calibration','rows':rows,'closest_reduced_address_readout':best_reduced,'checks':checks,'selection_scope':'Retain all4 modes for faithful reproduction of the frozen declared phase/address rule; smaller spectra validly explain same aggregate shares but define different conditional response models. No empirical ranking or universal necessity inferred.','conditional_write_scope':'same published two-mode microscopic gap and budget rule as Step2; costs are expected single-write outputs, not newly observed data'}
(ROOT/'mode_comparison_results.json').write_text(json.dumps(r,indent=2));print(json.dumps({'status':'PASS','checks':checks,'closest_reduced':best_reduced,'reference':rows[-1]},indent=2))
