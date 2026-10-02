#!/usr/bin/env python3
"""Numerical audit, an alternate quadrature and fresh-directory reproduction."""
from pathlib import Path
import copy, hashlib, importlib.util, json, shutil, subprocess, sys, tempfile
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
import compute

def verify():
    inp=json.loads((ROOT/'code/inputs.json').read_text())
    stored=json.loads((ROOT/'code/results.json').read_text())
    sf,blocks=compute.old.finite_states()
    spatial,W=compute.spatial_completion(sf,inp)
    changed=copy.deepcopy(inp);changed['internal_completion']['quadrature_order']=6
    spatial5,W5=compute.spatial_completion(sf,changed)
    ell=copy.deepcopy(inp);ell['internal_completion']['ell_dimensionless']=2.3
    spatialell,Well=compute.spatial_completion(sf,ell)
    pars=compute.calibration(inp,blocks,W)
    a=compute.evaluate(inp,blocks,W,pars)
    checks={
      'all_implementation_checks_pass':all(stored['checks'].values()),
      'alternate_quadrature_same_spatial_gram':np.linalg.norm(np.array(spatial5['spatial_gram'])-np.array(spatial['spatial_gram']))<2e-12,
      'alternate_quadrature_same_projected_link':np.linalg.norm(W5-W)<2e-12,
      'alternate_quadrature_same_discarded_norm':abs(spatial5['discarded_M_norm_squared']-spatial['discarded_M_norm_squared'])<2e-12,
      'changed_ell_same_projected_link':np.linalg.norm(Well-W)<2e-12,
      'changed_ell_same_oscillator_gap':np.linalg.norm(np.array(spatialell['dimensionless_oscillator_block'])-np.diag([3,5,5]))<2e-12,
      'link_operator_is_not_scalar_c1':np.linalg.norm(a['nucleons']['proton']['magnetic_exchange_operator_muN']-pars['c1_target_muN']*np.eye(2))>.1,
    }
    # A nonzero field is checked using independently constructed characteristic roots.
    for name in ('proton','neutron'):
        H0=np.array(a['nucleons'][name]['hamiltonian_zero_MeV']);M=np.array(a['nucleons'][name]['magnetic_operator_muN'])
        for b in (-2.,.4,2.):
            H=H0-b*M
            direct=(np.trace(H)-np.hypot(H[1,1]-H[0,0],2*H[0,1]))/2
            diagonal=compute.evaluate(inp,blocks,W,pars,field=b)['nucleons'][name]['field_energy_MeV']
            checks[f'{name}_characteristic_root_b{b}']=abs(direct-diagonal)<1e-9
    # Changed calibration anchors must actually propagate into the solved Hamiltonian.
    axial=copy.deepcopy(inp);axial['axial_calibration']['signed_lambda']=-1.29
    pp=compute.calibration(axial,blocks,W);aa=compute.evaluate(axial,blocks,W,pp)
    checks['changed_axial_anchor_changes_C_and_shared_state']=abs(pp['C']-pars['C'])>.1 and abs(aa['axial_magnitude']-1.29)<1e-12
    magnetic=copy.deepcopy(inp);magnetic['magnetic_moments_muN']['proton']+=.01
    pp=compute.calibration(magnetic,blocks,W);mm=compute.evaluate(magnetic,blocks,W,pp)
    checks['changed_magnetic_anchor_changes_eta_and_c0']=abs(pp['eta']-pars['eta'])>1e-3 and abs(pp['c0']-pars['c0'])>1e-3 and abs(mm['nucleons']['proton']['ground_moment_muN']-magnetic['magnetic_moments_muN']['proton'])<1e-12
    # Reviewed input contracts: malformed numbers must fail before a solve.
    for name,section,key,value in [
        ('nan_kappa','inherited','kappa',float('nan')),
        ('inf_kappa','inherited','kappa',float('inf')),
        ('nan_lifetime','inherited','neutron_mean_life_s',float('nan')),
        ('nan_proton_moment','magnetic_moments_muN','proton',float('nan')),
        ('inf_neutron_moment','magnetic_moments_muN','neutron',float('inf'))]:
        bad=copy.deepcopy(inp);bad[section][key]=value
        try:compute.check_inputs(bad)
        except ValueError:ok=True
        else:ok=False
        checks['review_reject_'+name]=ok
    for name,kwargs in [('unknown_model',{'model':'typo'}),('nan_field',{'field':float('nan')}),('negative_gap',{'delta':-1.})]:
        try:compute.evaluate(inp,blocks,W,pars,**kwargs)
        except ValueError:ok=True
        else:ok=False
        checks['review_reject_'+name]=ok
    bad=copy.deepcopy(inp);bad['internal_completion']['quadrature_order']=True
    try:compute.check_inputs(bad)
    except ValueError:checks['review_reject_bool_quadrature']=True
    else:checks['review_reject_bool_quadrature']=False
    with tempfile.TemporaryDirectory(prefix='wrra_upstream04_') as tmp:
        dst=Path(tmp)/'code';shutil.copytree(ROOT/'code',dst,ignore=shutil.ignore_patterns('__pycache__','results.json'))
        completed=subprocess.run([sys.executable,str(dst/'compute.py')],capture_output=True,text=True,check=True)
        checks['fresh_directory_exact_results_bytes']=(dst/'results.json').read_bytes()==(ROOT/'code/results.json').read_bytes()
        fresh=json.loads((dst/'results.json').read_text())
        checks['fresh_directory_all_checks_pass']=all(fresh['checks'].values())
    if not all(checks.values()):raise AssertionError({k:v for k,v in checks.items() if not v})
    result={'implementation_checks':stored['checks_total'],'audit_checks':len(checks),'total_checks':stored['checks_total']+len(checks),
       'checks':{k:bool(v) for k,v in checks.items()},'results_sha256':hashlib.sha256((ROOT/'code/results.json').read_bytes()).hexdigest(),
       'runtime':{'python':sys.version.split()[0],'numpy':np.__version__}}
    (ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':verify()
