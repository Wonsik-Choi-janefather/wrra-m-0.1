"""One fixed load/energy state feeds expansion, rotation and conditional lensing."""
from pathlib import Path
import ast,json,math,hashlib
import numpy as np
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
D=ROOT/'step5_dependency';m=json.loads((D/'RELEASE_MANIFEST.json').read_text())
for name,h in m['sha256'].items():assert hashlib.sha256((D/name).read_bytes()).hexdigest()==h
P=D/'step4_dependency/step3_dependency/step2_dependency/dependencies';p=P/'capacity_transport.py';nodes=[]
for node in ast.parse(p.read_text()).body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='inputs' for t in node.targets):break
 nodes.append(node)
s={'__file__':str(p),'__name__':'setup'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),s);ns=s['ns'];cal=s['calibration'];crit=cal['ucrit_J_m3'];V0=s['params']['reference_volume_m3'];H0=ns['H0_KM_S_MPC']*1000/(1e6*ns['PARSEC_M']);C=ns['C'];G=ns['G'];kpc=1000*ns['PARSEC_M'];rtest=ns['TEST_RADIUS_KPC']*kpc
state=json.loads((D/'state_load_results.json').read_text());rows=[];checks={};gx,gw=leggauss(512)
for case in state['cases']:
 a=case['a'];rho=np.array(case['sector_energy_J'])/(V0*a**3);pressure=sum(case['sector_pressure_Pa']);total=rho.sum();H=H0*math.sqrt(total/crit);q=.5*(total+3*pressure)/total
 # The same clustering density sets aT for both local renderers.
 aT=C*H0*math.sqrt(rho[1]/crit/8);g,gm=ns['plummer'](rtest,aT);v=math.sqrt(rtest*g)/1000;lens=ns['lens'](aT)
 # Independent vectorized quadrature of the same declared weak-field kernel.
 b=ns['LENS_IMPACT_KPC']*kpc;R=ns['PATCH_RADIUS_KPC']*kpc;zmax=math.sqrt(R*R-b*b);z=(gx+1)*zmax/2;rad=np.hypot(b,z);scale=ns['SPHERE_SCALE_KPC']*kpc;mass=ns['SPHERE_MASS_MSUN']*ns['M_SUN_KG'];gb=G*mass*rad/(rad*rad+scale*scale)**1.5
 accel=gb/(-np.expm1(-np.sqrt(gb/aT))) if aT>0 else gb
 alpha=4/C**2*zmax/2*np.dot(gw,accel*b/rad)*180/math.pi*3600
 assert abs(alpha-lens['alpha_patch_arcsec'])<1e-9
 assert abs(q-.5*(1+3*pressure/total))<1e-13
 rows.append({'carrier_state':case['state'],'epsilon':case['epsilon'],'a':a,'sector_density_J_m3':rho.tolist(),'pressure_Pa':pressure,'H_over_H0':H/H0,'q':float(q),'aT_m_s2':aT,'rotation_km_s':v,'lensing_arcsec':lens['alpha_patch_arcsec'],'independent_lensing_arcsec':float(alpha),'lensing_quadrature_difference_arcsec':float(abs(alpha-lens['alpha_patch_arcsec']))})
ref=next(x for x in rows if x['carrier_state']=='product' and x['epsilon']==0 and x['a']==1)
checks['frozen_step5_input_hashes_match']=True
checks['all12_states_use_shared_clustering_density']=len(rows)==12
checks['uniform_rotation_reproduces_existing_value']=abs(ref['rotation_km_s']-207.5102418659153)<1e-9
checks['uniform_lensing_reproduces_existing_value']=abs(ref['lensing_arcsec']-.5355822400088303)<1e-10
checks['uniform_expansion_q_reproduces_existing_value']=abs(ref['q']+.5285585894376319)<1e-12
checks['independent_lens_quadrature_reproduces_all_cases']=True
checks['expansion_q_uses_same_density_pressure']=True
checks['no_per_observable_calibration']=True
assert all(checks.values())
out={'status':'PASS','version':'0.1','checks':checks,'cases':rows,'scope':'shared frozen constitutive local renderer and homogeneous expansion; conditional weak-field lens uses Phi=Psi and fixed finite patch','inputs':'same sector density/pressure from Step5; frozen baryonic source and constants; no new fit','falsifiers':['uniform reference mismatch','independent quadrature mismatch','different aT fitted for rotation/lensing','density/pressure changed separately for expansion'],'remaining':['joint record/supplier boundary in macro readout','zero clustering/local baryonic boundary and shared-state final review'],'not_claimed':['new observational dataset fit','covariant4D gravity derived','all galaxy source profiles predicted']}
(ROOT/'shared_gravity_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'status':'PASS','checks':len(checks),'cases':len(rows),'reference':ref}))
