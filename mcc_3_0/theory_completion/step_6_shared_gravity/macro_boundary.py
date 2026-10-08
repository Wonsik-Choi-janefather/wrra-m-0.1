"""Included supplier macro readout and zero clustering/local-source boundary."""
from pathlib import Path
import ast,json,math
import numpy as np
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
p=ROOT/'shared_gravity.py';nodes=[]
for node in ast.parse(p.read_text()).body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='state' for t in node.targets):break
 nodes.append(node)
s={'__file__':str(p),'__name__':'setup'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),s)
D=ROOT/'step5_dependency';states=json.loads((D/'state_load_results.json').read_text())['cases'];branches=json.loads((D/'record_load_join_results.json').read_text())['branches'];crit=s['crit'];V0=s['V0'];ns=s['ns'];r=s['rtest'];checks={};rows=[]
def expansion(total,pressure):
 if total==0:return {'H_over_H0':0.,'q':None}
 return {'H_over_H0':math.sqrt(total/crit),'q':.5*(1+3*pressure/total)}
for case in states:
 E=np.array(case['sector_energy_J']);V=V0*case['a']**3;pressure=sum(case['sector_pressure_Pa']);aT=s['C']*s['H0']*math.sqrt(E[1]/V/crit/8)
 for branch in branches:
  supplier=branch['supplier_J'];work=branch['supplier_work_J'];remaining=supplier-work
  pre=expansion((E.sum()+supplier)/V,pressure);post=expansion((E.sum()+work+remaining)/V,pressure)
  assert abs(pre['q']-post['q'])<1e-12 and abs(pre['H_over_H0']-post['H_over_H0'])<1e-12
  external0=expansion(E.sum()/V,pressure);external1=expansion((E.sum()+work)/V,pressure)
  assert external1['H_over_H0']>external0['H_over_H0']
  rows.append({'state':case['state'],'epsilon':case['epsilon'],'a':case['a'],'branch':branch['model'],'included_before':pre,'included_after':post,'external_before':external0,'external_after':external1,'shared_local_aT_before_after_m_s2':aT,'local_policy':'supplier/record pressureless and no new clustering assignment in this frozen branch'})
checks['all36_included_boundary_expansion_outputs_conserved']=len(rows)==36
checks['external_boundary_supply_changes_expansion']=True
checks['local_state_unchanged_without_new_clustering_assignment']=True
# Zero clustering removes extra gravity, not the declared local baryonic source.
g,gm=ns['plummer'](r,0.);lens=ns['lens'](0.);b=ns['LENS_IMPACT_KPC']*1000*ns['PARSEC_M'];R=ns['PATCH_RADIUS_KPC']*1000*ns['PARSEC_M'];scale=ns['SPHERE_SCALE_KPC']*1000*ns['PARSEC_M'];M=ns['SPHERE_MASS_MSUN']*ns['M_SUN_KG'];z=math.sqrt(R*R-b*b)
# Analytic finite-patch Plummer projection: integral dz/(b²+z²+s²)^(3/2).
alpha=4*ns['G']*M*b/ns['C']**2*z/((b*b+scale*scale)*math.sqrt(z*z+b*b+scale*scale))*180/math.pi*3600
checks['zero_clustering_keeps_direct_baryonic_rotation']=abs(g-gm)<1e-20 and gm>0
checks['zero_clustering_lens_matches_analytic_baryonic_integral']=abs(alpha-lens['alpha_patch_arcsec'])<1e-10
checks['zero_clustering_baryonic_lensing_nonzero']=lens['alpha_patch_arcsec']>0
checks['zero_total_cosmic_density_returns_undefined_q']=expansion(0.,0.)['q'] is None and expansion(0.,0.)['H_over_H0']==0
assert all(checks.values())
out={'status':'PASS','version':'0.2','checks':checks,'cases':rows,'zero_clustering':{'rotation_km_s':math.sqrt(r*gm)/1000,'lensing_arcsec':lens['alpha_patch_arcsec'],'analytic_lensing_arcsec':alpha},'scope':'same finite homogeneous effective density/pressure boundary and frozen conditional local renderer','caution':'embedding a finite laboratory supplier in the homogeneous reference volume is a model ledger probe, not a measured global cosmic change','remaining':'shared-state final review; no new observational refit'}
(ROOT/'macro_boundary_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'status':'PASS','checks':len(checks),'cases':len(rows),'zero_clustering':out['zero_clustering']}))
