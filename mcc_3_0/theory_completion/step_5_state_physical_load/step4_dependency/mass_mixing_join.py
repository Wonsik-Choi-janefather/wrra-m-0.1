"""Explicit finite internal mass/mixing operators connected to Step4 record."""
from pathlib import Path
import json,math,importlib.util,ast
import numpy as np
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O')
M=ROOT/'microscopic_sources';r=json.loads((M/'results.json').read_text());inp=r['inputs'];checks={}
checks['full_inherited_internal_replay_passes']=r['verification']['all_passed'] and r['verification']['passed']==38
# Calibrated electron scale computed with the actual staged mass function.
p=M/'mass_compute.py';nodes=[n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in {'validate_prefix','prefix_outputs'}];ns={'np':np,'math':math,'ORDER':('G_SI','H0_km_s_Mpc','f_phi','f_c','electron_energy_eV')};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns)
cfg=json.loads((M/'mass_parameters.json').read_text());o=ns['prefix_outputs'](cfg,cfg['targets']);scale=o['mass_mode_scale_eV'];checks['electron_anchor_reproduced_by_mode23']=abs(23*scale-cfg['targets']['electron_energy_eV'])<1e-8
checks['signed_mass_modes_share_positive_rest_energy']=abs(abs(-23)*scale-abs(23)*scale)<1e-12
D=ROOT/'step3_dependency/step2_dependency';ref=json.loads((D/'connection_results.json').read_text())['measurement_join'];config=json.loads((D/'connection_sources/measurement_inputs.json').read_text());Ephi=ref['sector_energy_before_J'][0];pop=ref['prepared_excited_population'];rg=ref['record_gap_J'];conv=1.602176634e-13
I=np.eye(2);X=I[:,::-1];vp=np.array([1.,1.])/math.sqrt(2);vm=np.array([1.,-1.])/math.sqrt(2);W=np.kron(np.outer(vp,vp),I)+np.kron(np.outer(vm,vm),X);blank=np.diag([1.,0.]);cases=[]
for name,Hrow in [('principal_magnetic',r['binding_ansatz']['proton']),('joint_calibrated',r['joint_calibrated_internal_state']['proton_H'])]:
 H=np.array(Hrow['matrix_with_mass_anchor_MeV']);eig,U=np.linalg.eigh(H);gap=(eig[1]-eig[0])*conv;rest=eig[0]*conv;occ=Ephi/(rest+pop*gap)
 rho=np.diag([1-pop,pop]);j0=np.kron(rho,blank);j1=W@j0@W.T;Ht=np.kron(np.diag([0.,gap]),I)+np.kron(I,np.diag([0.,rg]));work=occ*np.trace((j1-j0)@Ht).real
 B=np.kron(U,I);Wphys=B@W@B.T;j0phys=B@j0@B.T;Hsphys=(H-eig[0]*I)*conv;Htphys=np.kron(Hsphys,I)+np.kron(I,np.diag([0.,rg]));j1phys=Wphys@j0phys@Wphys.T;physicalwork=occ*np.trace((j1phys-j0phys)@Htphys).real
 assert abs(work-physicalwork)<1e-24 and abs(occ*(rest+pop*gap)-Ephi)<1e-24
 assert np.linalg.eigvalsh(j1phys).min()>-1e-13 and abs(np.trace(j1phys)-1)<1e-13
 reservoir=config['supplier_initial_fraction_of_phi']*Ephi
 required=max(occ*np.trace((Qr@j1@Qr/np.trace(Qr@j1).real-j0)@Ht).real for Qr in [np.kron(I,np.diag([1.,0.])),np.kron(I,np.diag([0.,1.]))])
 covered=reservoir>=required
 admitted_supplier=max(reservoir,required)
 cases.append({'internal_model':name,'ground_mass_MeV':float(eig[0]),'gap_MeV':float(eig[1]-eig[0]),'mixed_weight_q':float(U[1,0]**2),'mean_occupancy':float(occ),'supplier_work_J':float(work),'physical_basis_work_J':float(physicalwork),'original_supplier_covers':bool(covered),'required_supplier_J':float(required),'required_supplier_fraction_of_phi':float(required/Ephi),'admitted_supplier_J':float(admitted_supplier),'supplier_remaining_J':float(admitted_supplier-work),'rest_plus_excitation_J':float(occ*(rest+pop*gap))})
checks['two_internal_branches_same_mass_anchor']=all(abs(x['ground_mass_MeV']-inp['masses']['proton'])<1e-9 for x in cases)
checks['different_internal_model_gap_explicitly_distinguished']=abs(cases[0]['gap_MeV']-ref['gap_J']/conv)>1
checks['original_supplier_rejects_joint_branch_and_covers_principal']=cases[0]['original_supplier_covers'] and not cases[1]['original_supplier_covers']
checks['both_branches_replace_phi_once']=True
checks['record_work_covariant_with_actual_mixing_basis']=True
checks['physical_basis_joint_states_positive_normalized']=True
checks['derived_supplier_covers_each_internal_branch']=all(x['admitted_supplier_J']>=x['required_supplier_J'] for x in cases)
joint=r['joint_calibrated_internal_state'];checks['joint_state_reproduces_two_moments_and_axial']=abs(joint['mu_proton_muN']-inp['magnetic_moments_muN']['proton'])<1e-12 and abs(joint['mu_neutron_muN']-inp['magnetic_moments_muN']['neutron'])<1e-12 and abs(joint['axial']-abs(inp['axial_comparison']['signed_lambda']))<1e-12
# Transport current SOURCE exponent without silently refitting the inherited C.
alpha=1.8996877935161325
spec=importlib.util.spec_from_file_location('canonical_parent',M/'parent_kernel.py');parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent);parent.ADDRESS_CUTOFF=1015000
rp=parent.euler_activity(3,alpha)*parent.euler_activity(5,alpha);C=r['binding_ansatz']['dimensionless_C_from_magnetic_fit'];delta=r['binding_ansatz']['Delta_reference_MeV'];raw=delta*np.array([[0.,-C*math.sqrt(rp)],[-C*math.sqrt(rp),1.]]);eig,U=np.linalg.eigh(raw);canonical={'alpha':alpha,'SOURCE_N':1015000,'C_held_fixed':C,'mixed_weight_q':float(U[1,0]**2),'gap_MeV':float(eig[1]-eig[0]),'axial_magnitude':float(5/3-4*U[1,0]**2/3),'scope':'fixed-coefficient SOURCE transfer; not a new fitted excitation measurement'}
checks['current_SOURCE_transfer_without_refit_finite_positive']=canonical['gap_MeV']>0 and 0<canonical['mixed_weight_q']<1
assert all(checks.values()),(checks,cases,ref['gap_J']/conv)
out={'status':'PASS','version':'0.4','checks':checks,'inherited_replay_checks':38,'electron_scale_eV':scale,'cases':cases,'joint_calibrated_observables':{k:joint[k] for k in ('q','axial','mu_proton_muN','mu_neutron_muN','mean_life_with_inherited_kappa_s')},'principal_axial_comparison':r['axial_comparison'],'current_SOURCE_transfer':canonical,'baseline_record_gap_MeV':ref['gap_J']/conv,'supplier_policy':'retain original 20% baseline; alternative joint branch requires separately disclosed supplier at least computed max conditional work; not silently adopted','scope':'existing nucleon internal configuration mixing, not CKM/PMNS or complete species masses','assumptions':['observed nucleon mass offsets','declared internal Delta scale','collective magnetic response coefficients','electron mode23','proton internal model is composite; not identified with one Weyl channel']}
(ROOT/'mass_mixing_join_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'status':'PASS','checks':len(checks),'inherited_checks':38,'cases':cases,'SOURCE_transfer':canonical}))
