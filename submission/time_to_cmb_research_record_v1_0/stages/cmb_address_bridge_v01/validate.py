from pathlib import Path
import json,csv
import numpy as np
import camb
from camb import constants as c
from scipy.integrate import cumulative_simpson
from cmb_runner import case,make_params,combine,ROOT,OUT
from plik_lite import NativePlikLite

def validate():
    inp=json.loads((OUT/'address_results.json').read_text());checks=dict(inp['checks'])
    high=combine('dark_weight_only',2.5);low=combine('dark_weight_only',1.5)
    h=np.loadtxt(OUT/'dark_weight_only_SOURCE_a2.5_Dl.csv',delimiter=',',skiprows=1)[:,1:]
    l=np.loadtxt(OUT/'dark_weight_only_SOURCE_a1.5_Dl.csv',delimiter=',',skiprows=1)[:,1:]
    conv=np.max(abs(h-l),axis=0)/np.maximum(np.max(abs(h),axis=0),1e-30)
    b=np.load(OUT/'dark_weight_only_standard_a2.5.npz')['Dl'];z=np.load(OUT/'dark_weight_only_zero_a2.5.npz')['Dl']
    zero=float(np.max(abs(z[2:,:2]/b[2:,:2]-1)))
    checks['candidate_zero_SOURCE_restore']=zero<1e-8
    checks['candidate_SOURCE_convergence']=bool(max(conv)<.002)
    checks['candidate_SOURCE_TE_covariance']=high['TE_covariance_excess']<1e-20
    checks['candidate_SOURCE_auto_spectra_nonnegative']=bool(np.all(h[:,[0,1]]>=0))
    cfg=case('dark_weight_only');u=np.array(cfg['u0_P_D_R_J_m3'])
    p=make_params('dark_weight_only','R',2.5);r=camb.get_background(p)
    a_grid=np.geomspace(1e-8,1,240);bg=r.get_background_densities(a_grid,vars=['baryon','cdm','de'])
    gfac=8*np.pi*c.G*c.Mpc**2/c.c**4
    expected=np.c_[u[0]*a_grid,u[1]*a_grid,u[2]*a_grid**4]*gfac
    actual=np.c_[bg['baryon'],bg['cdm'],bg['de']]
    density_error=float(np.max(abs(actual/expected-1)))
    checks['candidate_SI_background_from_address_ledger']=density_error<2e-8
    tau=np.geomspace(.1,r.conformal_time(0),6000);ks=.05*np.arange(1,8)
    names=['a','H','delta_cdm','delta_baryon','source_delta_R','source_v_D','source_z','source_d_delta_D','source_d_v_D']
    yr=r.get_time_evolution(ks,tau,names,lAccuracyBoost=3)
    q=camb.get_background(make_params('dark_weight_only','D',2.5))
    yd=q.get_time_evolution(ks,tau,names,lAccuracyBoost=3)
    a,H=np.moveaxis(yr[:,:,:2],-1,0);v=yr[:,:,5]
    integ=cumulative_simpson(-ks[:,None]*u[2]/u[1]*a**4,x=tau,axis=1,initial=0)
    av=a*v-a[:,0,None]*v[:,0,None]
    momentum_error=float(np.max(abs(av[:,50:]-integ[:,50:]))/np.max(abs(integ[:,50:])))
    checks['candidate_independent_momentum_integral']=momentum_error<1e-6
    upD=np.zeros(len(tau));upB=np.zeros(len(tau));trajectory_rows=[]
    for row in cfg['amplitudes']:
        n=row['mode']-1;dc=row['S_D']*yd[n,:,2]+row['delta_R']*yr[n,:,2]
        bc=row['S_D']*yd[n,:,3]+row['delta_R']*yr[n,:,3]
        vv=row['S_D']*yd[n,:,5]+row['delta_R']*yr[n,:,5]
        upD+=abs(dc);upB+=abs(bc)
        trajectory_rows.append(dict(mode=n+1,component=row['component'],delta_D_max=float(abs(dc).max()),
            delta_baryon_max=float(abs(bc).max()),velocity_D_max=float(abs(vv).max()),state_finite=bool(np.isfinite(dc).all() and np.isfinite(bc).all() and np.isfinite(vv).all())))
    checks['candidate_linear_regime']=bool(max(upD.max(),upB.max())<.1)
    checks['candidate_all_14_real_trajectories_finite']=all(x['state_finite'] for x in trajectory_rows)
    np.savez_compressed(OUT/'candidate_evolution.npz',tau=tau,k=ks,variables=names,R_basis=yr,D_basis=yd,
        delta_D_triangle_bound=upD,delta_baryon_triangle_bound=upB)
    # Compare the repeated complete pipeline to frozen original baselines and exchange diagnostic.
    legacy=[];like=NativePlikLite()
    references={'weighted':591.5703352485414,'unweighted':1217.7512246819865}
    for branch in ['weighted','unweighted']:
        dl=np.load(OUT/f'{branch}_standard_a2.5.npz')['Dl'];score=like.evaluate(dl)['chi2_highell']
        err=abs(score-references[branch]);checks[branch+'_CMB_from_addresses_reproduces_prior']=err<1e-5
        legacy.append(dict(branch=branch,chi2=score,frozen_prior_chi2=references[branch],absolute_difference=err))
    diagnostic=585.9139184472003
    diagnostic_error=abs(high['baseline_high_ell_chi2']-diagnostic)
    checks['candidate_reproduces_exchange_diagnostic']=diagnostic_error<1e-5
    # Reconstructed original Fourier vectors must also match.
    old=list(csv.DictReader((ROOT/'inputs/prior_SOURCE_harmonics.csv').open()))
    new=list(csv.DictReader((OUT/'generated_SOURCE_harmonics.csv').open()))
    coefficient_errors={}
    for branch in ['weighted','unweighted']:
        x=[r for r in old if r['branch']==branch];y=[r for r in new if r['branch']==branch]
        coefficient_errors[branch]=max(abs(float(v[k])-float(w[k])) for v,w in zip(x,y) for k in ['delta_u_D_at_a1_J_m3','delta_u_R_J_m3'])
        checks[branch+'_prior_SOURCE_coefficients']=coefficient_errors[branch]<1e-30
    result=dict(version='address_generated_dark_candidate_0.1',date='2026-10-14',
        validation_input='Frozen address weights/sector effects, eta, source/supply rule, conditional primordial extension, public CMB data',
        WRRA_transform='address -> sector log weights -> rerouted residue payload -> finite source+supplier -> mean energy/pressure and Fourier stress -> full linear CMB execution',
        candidate_rule=inp['candidate_rule_origin'],candidate_background=cfg['background'],
        candidate_mean_load=cfg['mean_load_P_D_R'],candidate_mean_energy_J_m3=cfg['u0_P_D_R_J_m3'],
        legacy_CMB_reproduction=legacy,candidate_CMB=high,
        candidate_SOURCE_convergence=dict(zip(['TT','EE','BB','TE'],conv.tolist())),zero_SOURCE_relative_restore=zero,
        direct_SI_background_relative_error=density_error,independent_momentum_integral_relative_error=momentum_error,
        delta_D_triangle_bound_max=float(upD.max()),delta_baryon_triangle_bound_max=float(upB.max()),
        real_mode_trajectories=trajectory_rows,previous_exchange_baseline_chi2=diagnostic,
        address_generated_vs_exchange_chi2_difference=diagnostic_error,prior_SOURCE_coefficient_errors_J_m3=coefficient_errors,
        checks=checks,all_checks_pass=all(checks.values()),
        conclusion='The previous dark-ledger exchange is realized by an explicit member of the existing address-weight family, with fresh slot allocation and counted supply. It is no longer only a downstream density swap.',
        completed='Address-weight -> conserved mean/source ledger -> internally executed conditional CMB candidate',
        still_open=['Physical interpretation and applicability of the calibrated weight choice','Derivation of primordial preparation from upstream execution','SOURCE-specific lensing and full Planck likelihood'],
        parameter_optimizer=False,post_readout_density_swap=False,
        refutation_conditions=['Address sum differs from routed mean or Fourier stress','Finite source/supply balance fails','Zero-source or resolution tests fail','Declared linear regime fails','Agreed completed observational evaluation disagrees'])
    assert result['all_checks_pass'],[k for k,v in checks.items() if not v]
    (OUT/'bridge_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(dict(candidate=cfg['background'],chi2=high['combined_high_ell_chi2'],source_TT=high['SOURCE_max_TT_Dl_uK2'],
        momentum_error=momentum_error,linear_deltaD=float(upD.max()),checks_passed=sum(checks.values()),checks_total=len(checks))),flush=True)

if __name__=='__main__':validate()
