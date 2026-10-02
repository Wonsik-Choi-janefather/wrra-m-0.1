#!/usr/bin/env python3
"""Independent spinor amplitude, adaptive radiative integral and fresh run."""
from pathlib import Path
import copy,hashlib,json,math,os,shutil,subprocess,sys,tempfile
import numpy as np
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'code'))
import compute,currents,beta

def spinors(p,m,anti=False):
    E=p[0];pm=sum(s*k for s,k in zip(beta.pauli,p[1:]));out=[]
    for v in np.eye(2):
        small=pm@v/(E+m);out.append(math.sqrt(E+m)*np.concatenate((small,v) if anti else (v,small)))
    return out

def amplitude_sum(E,z,mp,mn,me,ff):
    p=math.sqrt(E*E-me*me);D=mn-E+p*z;k=(mn*mn+me*me-mp*mp-2*mn*E)/(2*D)
    pe=np.array([E,0,0,p]);nu=np.array([k,k*math.sqrt(1-z*z),0,k*z]);pn=np.array([mn,0,0,0]);pp=pn-pe-nu;q=pp-pn;t=np.sum(q*q*beta.METRIC)*1e-6
    f1=ff['F1V0']-ff['F1V_prime']*t;f2=ff['F2V0']-ff['F2V_prime']*t;ga=ff['GA0']-ff['GA_prime']*t
    vertex=f1*beta.G-ga*beta.G@beta.G5+np.einsum('v,v,mvij->mij',q,beta.METRIC,1j*beta.SIG)*f2/(mp+mn)
    total=0.
    for un in spinors(pn,mn):
        for up in spinors(pp,mp):
            had=np.array([up.conj()@beta.G[0]@v@un for v in vertex])
            for ue in spinors(pe,me):
                for vn in spinors(nu,0,True):
                    lep=np.array([ue.conj()@beta.G[0]@beta.G[mu]@(beta.I4-beta.G5)@vn for mu in range(4)])
                    total+=abs(np.sum(beta.METRIC*had*lep))**2/2
    return total*p*k/D

def verify():
    inp=json.loads((ROOT/'code/inputs.json').read_text());r=json.loads((ROOT/'code/results.json').read_text());m,p,e,V,g,c=compute.construct(inp)
    sl=currents.slopes(c);ff={**sl['weak'],'activity_R':p['R']};checks={'all_implementation_checks_pass':all(r['checks'].values())}
    cliff=max(np.linalg.norm(beta.G[i]@beta.G[j]+beta.G[j]@beta.G[i]-2*(beta.METRIC[i] if i==j else 0)*np.eye(4)) for i in range(4) for j in range(4))
    checks['Clifford_algebra_exact']=cliff<1e-13
    mp,mn,me=(inp['masses'][k] for k in ('proton','neutron','electron'))
    for E,z in ((.63,-.8),(.9,.2),(1.17,.7)):
        direct=amplitude_sum(E,z,mp,mn,me,ff);trace,_=beta.trace_grid(np.array(E),np.array(z),mp,mn,me,ff)
        checks[f'explicit_spinor_sum_matches_trace_E{E}_z{z}']=abs(direct/float(trace)-1)<1e-12
    # Independent analytic heavy-mass limit checks normalization and angular
    # coefficient. This does not reuse the stored lifetime anchor.
    mass=1e6;M=mass+(mn-mp);E=.83;z=.4;mom=math.sqrt(E*E-me*me);D=M-E+mom*z;k=(M*M+me*me-mass*mass-2*M*E)/(2*D)
    trace,_=beta.trace_grid(np.array(E),np.array(z),mass,M,me,ff,False,False)
    analytic=mom*k/D*32*M*mass*E*k*((1+3*ff['GA0']**2)+(1-ff['GA0']**2)*mom/E*z)
    checks['heavy_mass_allowed_normalization_and_a']=abs(float(trace)/analytic-1)<2e-6
    Em=r['beta']['endpoint_recoil_total_electron_MeV'];alpha=inp['weak_constants']['alpha_em']
    def outer(E):
        return math.sqrt(E*E-me*me)*E*(Em-E)**2*float(beta.coulomb(np.array(E),me,alpha))*alpha/(2*math.pi)*float(beta.sirlin_g(np.array(E),Em,me,mp))
    integral,_=quad(outer,me,Em,epsabs=1e-13,epsrel=2e-11,limit=200)
    expected=integral/r['beta']['parent_allowed_integral_MeV5']
    checks['adaptive_outer_integral_matches_gauss']=abs(expected-r['beta']['outer_rate_increment_relative_parent'])<2e-8
    bad=copy.deepcopy(inp);bad['charge_completion']['inner_delta_R_V']=0.;inneroff=beta.calculate(bad,ff)
    checks['inner_RC_factor_propagates']=abs(r['beta']['full_rate_ratio_relative_parent']/inneroff['full_rate_ratio_relative_parent']-(1+inp['charge_completion']['inner_delta_R_V']))<1e-10
    bad=copy.deepcopy(inp);bad['inherited']['kappa']*=1.02;changed=beta.calculate(bad,ff)
    checks['frozen_kappa_square_lifetime_scaling']=abs(changed['frozen_parent_kappa_lifetime_s']/r['beta']['frozen_parent_kappa_lifetime_s']-1/1.02**2)<1e-10
    checks['explicit_refit_removes_prior_normalization_choice']=abs(changed['separately_refitted_kappa']-r['beta']['separately_refitted_kappa'])<1e-9
    bad=copy.deepcopy(inp);bad['weak_constants']['alpha_em']=0.;bad['charge_completion']['inner_delta_R_V']=0.;emoff=beta.calculate(bad,ff)
    checks['zero_EM_removes_outer_RC']=abs(emoff['outer_rate_increment_relative_parent'])<1e-14
    # Both charge slopes are preserved for every regulator, although the
    # unfitted finite-Q2 curvature changes substantially.
    h=1e-5
    for reg in (.5,2.):
        a=currents.ground(c,h,reg);b=currents.ground(c,2*h,reg);z0=currents.ground(c,0,reg)
        for name in ('proton','neutron'):
            slope=(-3*z0[name]['GE']+4*a[name]['GE']-b[name]['GE'])/(2*h)
            checks[f'{name}_regulator_{reg}_same_radius']=abs(-6*currents.HC**2*slope-sl[name]['sachs_charge_radius_squared_fm2'])<2e-9
    changed=copy.deepcopy(inp);changed['charge_completion']['neutron_mean_square_radius_fm2']+=.001
    cp=currents.prepare(m,p,g,changed,32,18)
    checks['changed_neutron_radius_anchor_changes_width_and_counterterm']=abs(cp['ell_fm']-c['ell_fm'])>1e-4 and abs(cp['counterterm_radius_fm2']-c['counterterm_radius_fm2'])>1e-4
    checks['neutron_magnetic_radius_remains_unfitted_mismatch']=abs(r['unfitted_diagnostic']['neutron_magnetic_radius_fm']-.864)>.008
    for name,key,value in [('negative_Q2','spacelike_Q2_GeV2',[-.1]),('nan_counterterm_input','neutron_mean_square_radius_fm2',float('nan')),('incompatible_width','neutron_mean_square_radius_fm2',-1.),('zero_regulator','reference_regulator_in_ell',0.),('negative_inner_RC','inner_delta_R_V',-.1)]:
        bad=copy.deepcopy(inp);bad['charge_completion'][key]=value
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
    for name,key,value in [('empty_qgrid','spacelike_Q2_GeV2',[]),('empty_regulators','regulator_lengths_in_ell',[]),('bool_electron_order','reference_electron_order',True),('nan_uncertainty','uncertainty_fm2',float('nan'))]:
        bad=copy.deepcopy(inp);bad['charge_completion'][key]=value
        try:compute.validate(bad)
        except ValueError:ok=True
        else:ok=False
        checks['review_reject_'+name]=ok
    # Actual full pipeline regression: a reversed, shorter grid and one
    # regulator must not change the fixed convergence probe or physical rate.
    grid=copy.deepcopy(inp);grid['charge_completion']['spacelike_Q2_GeV2']=[.2,.03,0.]
    grid['charge_completion']['regulator_lengths_in_ell']=[2.]
    rerun=compute.run(grid)
    checks['review_reordered_reduced_grid_full_run_passes']=all(rerun['checks'].values())
    checks['review_grid_does_not_change_rate_or_calibration']=rerun['beta']==r['beta'] and rerun['new_charge_calibration']==r['new_charge_calibration']
    checks['review_grid_returns_requested_order']=[row['Q2_GeV2'] for row in rerun['form_factors']]==[.2,.03,0.]
    for name in ('proton','neutron'):
        first=(-3*z0[name]['F1']+4*currents.ground(c,h)[name]['F1']-currents.ground(c,2*h)[name]['F1'])/(2*h)
        checks['review_'+name+'_Dirac_radius_finite_derivative']=abs(-6*currents.HC**2*first-sl[name]['dirac_radius_squared_fm2'])<3e-9
    for key in ('GF_GeV_minus2','Vud'):
        bad=copy.deepcopy(inp);bad['weak_constants'][key]*=1.02
        changed=beta.calculate(bad,ff)
        checks['review_'+key+'_square_rate_scaling']=abs(changed['frozen_parent_kappa_lifetime_s']/r['beta']['frozen_parent_kappa_lifetime_s']-1/1.02**2)<1e-10
    with tempfile.TemporaryDirectory(prefix='wrra06_fresh_') as tmp:
        code=Path(tmp)/'code';shutil.copytree(ROOT/'code',code,ignore=shutil.ignore_patterns('__pycache__','results.json'))
        subprocess.run([sys.executable,str(code/'compute.py')],capture_output=True,text=True,check=True,env={**os.environ,'OPENBLAS_NUM_THREADS':'2'})
        checks['fresh_directory_exact_results_bytes']=(code/'results.json').read_bytes()==(ROOT/'code/results.json').read_bytes()
        checks['fresh_directory_all_checks_pass']=all(json.loads((code/'results.json').read_text())['checks'].values())
    if not all(checks.values()):raise AssertionError({k:v for k,v in checks.items() if not v})
    out={'implementation_checks':r['checks_total'],'audit_checks':len(checks),'total_checks':r['checks_total']+len(checks),'checks':{k:bool(v) for k,v in checks.items()},'results_sha256':hashlib.sha256((ROOT/'code/results.json').read_bytes()).hexdigest(),'python':sys.version.split()[0],'numpy':np.__version__}
    (ROOT/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':verify()
