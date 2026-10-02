#!/usr/bin/env python3
"""Separate numerical audits and fresh-directory exact result reproduction."""
from pathlib import Path
import copy, hashlib, json, os, shutil, subprocess, sys, tempfile
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
import compute, model

def verify():
    inp=json.loads((ROOT/'code/inputs.json').read_text());r=json.loads((ROOT/'code/results.json').read_text())
    s=inp['spatial_extension'];m=model.build(s['reference_shell_order'],s['quadrature_radial_order'],s['quadrature_angular_order'],s['screening_lambda'])
    p=compute.calibrate(m,inp);_,e,V,g=model.diagonalize(m,p['x'])
    checks={'all_implementation_checks_pass':all(r['checks'].values()),
        'old_v0_4_code_matches_published_hash':hashlib.sha256((ROOT/'code/inherited_v0_4.py').read_bytes()).hexdigest()==inp['v0_4_baseline']['code_sha256'],
        'parent_kernel_matches_frozen_hash':hashlib.sha256((ROOT/'code/parent_kernel.py').read_bytes()).hexdigest()==inp['provenance']['parent_kernel_sha256'],
        'proton_S_gaussian_radius_one':abs(m['reference'][:,0]@m['radius_proton']@m['reference'][:,0]-1)<1e-11,
        'neutron_S_gaussian_radius_zero':abs(m['reference'][:,0]@m['radius_neutron']@m['reference'][:,0])<1e-11,
        'finite_spectral_ground_residual':np.linalg.norm((m['h0']-p['x']*m['bounded'])@g-e[0]*g)<1e-11,
        'all_higher_shell_holdout_parameters_frozen':abs(r['unfitted_shell_holdout']['gA']-r['reference']['gA'])>1e-9,
        'unfitted_neutron_mismatch_recorded':abs(r['reference']['neutron_charge_mean_square_fm2']+.1155)>.05}
    # Inhomogeneous-source response solves the reduced resolvent independently
    # from the stored all-state sum used by compute.evaluate.
    for name,M in compute.operators(m,p).items():
        E=V[:,1:];a=E.T@(M@g);A=E.T@(p['delta_MeV']*(m['h0']-p['x']*m['bounded']-e[0]*np.eye(len(g))))@E
        response=2*float(a@np.linalg.solve(A,a))
        checks[name+'_reduced_resolvent_matches_spectral_susceptibility']=abs(response-r['reference']['nucleons'][name]['internal_susceptibility_MeV_minus1'])<1e-10
    changed=copy.deepcopy(inp);changed['axial_calibration']['signed_lambda']=-1.29
    pp=compute.calibrate(m,changed);rr=compute.evaluate(m,pp,changed)
    checks['changed_axial_anchor_propagates_to_state_and_C']=abs(rr['gA']-1.29)<1e-10 and abs(pp['C']-p['C'])>.1
    changed=copy.deepcopy(inp);changed['magnetic_moments_muN']['proton']+=.01
    pp=compute.calibrate(m,changed);rr=compute.evaluate(m,pp,changed)
    checks['changed_magnetic_anchor_changes_eta_and_c0']=abs(pp['eta']-p['eta'])>1e-3 and abs(pp['c0']-p['c0'])>1e-3 and abs(rr['nucleons']['proton']['moment_muN']-changed['magnetic_moments_muN']['proton'])<1e-10
    changed=copy.deepcopy(inp);changed['radius_calibration']['proton_rms_charge_radius_fm']*=1.01
    pp=compute.calibrate(m,changed)
    checks['radius_anchor_scales_ell_without_refitting_state']=abs(pp['ell_fm']/p['ell_fm']-1.01)<1e-12 and abs(pp['x']-p['x'])<1e-12
    changed=copy.deepcopy(inp);changed['excitation_calibration']['pole_centroid_MeV']+=10
    pp=compute.calibrate(m,changed)
    checks['excitation_anchor_changes_delta_without_refitting_state']=abs(pp['delta_MeV']-p['delta_MeV'])>10 and abs(pp['x']-p['x'])<1e-12
    changed=copy.deepcopy(inp);changed['inherited']['kappa']*=1.02
    rr=compute.evaluate(m,p,changed)
    checks['weak_parent_kappa_square_rate_scaling']=abs(rr['mean_life_s']/r['reference']['mean_life_s']-1/1.02**2)<1e-10
    for name,section,key,value in [('zero_screen','spatial_extension','screening_lambda',0),('nan_screen','spatial_extension','screening_lambda',float('nan')),('negative_radius','radius_calibration','proton_rms_charge_radius_fm',-1),('closed_excitation','excitation_calibration','pole_centroid_MeV',900),('bool_shell','spatial_extension','reference_shell_order',True)]:
        bad=copy.deepcopy(inp);bad[section][key]=value
        try:compute.validate(bad)
        except ValueError:ok=True
        else:ok=False
        checks['reject_'+name]=ok
    # Reviewed input contracts: malformed numbers must fail before a solve.
    for name,section,key,value in [
        ('nan_kappa','inherited','kappa',float('nan')),
        ('inf_kappa','inherited','kappa',float('inf')),
        ('nan_lifetime','inherited','neutron_mean_life_s',float('nan')),
        ('nan_proton_moment','magnetic_moments_muN','proton',float('nan')),
        ('inf_neutron_moment','magnetic_moments_muN','neutron',float('inf'))]:
        bad=copy.deepcopy(inp);bad[section][key]=value
        try:compute.validate(bad)
        except ValueError:ok=True
        else:ok=False
        checks['review_reject_'+name]=ok
    for name,key,value in [('empty_shells','shell_orders',[]),('reversed_shells','shell_orders',[8,2]),('duplicate_shells','shell_orders',[2,2,8]),('unresolved_holdout','alternate_quadrature_radial_order',8),('empty_screen_controls','screening_sensitivity',[])]:
        bad=copy.deepcopy(inp);bad['spatial_extension'][key]=value
        try:compute.validate(bad)
        except ValueError:ok=True
        else:ok=False
        checks['review_reject_'+name]=ok
    with tempfile.TemporaryDirectory(prefix='wrra_upstream05_') as tmp:
        code=Path(tmp)/'code';shutil.copytree(ROOT/'code',code,ignore=shutil.ignore_patterns('__pycache__','results.json'))
        subprocess.run([sys.executable,str(code/'compute.py')],capture_output=True,text=True,check=True,env={**os.environ,'OPENBLAS_NUM_THREADS':'2'})
        checks['fresh_directory_exact_results_bytes']=(code/'results.json').read_bytes()==(ROOT/'code/results.json').read_bytes()
        checks['fresh_directory_checks_pass']=all(json.loads((code/'results.json').read_text())['checks'].values())
    if not all(checks.values()):raise AssertionError({k:v for k,v in checks.items() if not v})
    out={'implementation_checks':r['checks_total'],'audit_checks':len(checks),'total_checks':r['checks_total']+len(checks),'checks':{k:bool(v) for k,v in checks.items()},'results_sha256':hashlib.sha256((ROOT/'code/results.json').read_bytes()).hexdigest(),'python':sys.version.split()[0],'numpy':np.__version__}
    (ROOT/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));return out
if __name__=='__main__':verify()
