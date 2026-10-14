"""Released native Planck high-l, low-T, low-E and CMB-marginalized lensing evaluation."""
from pathlib import Path
import json,numpy as np
from cobaya.likelihoods.planck_2018_lowl.TT import TT
from cobaya.likelihoods.planck_2018_lowl.EE import EE
from cobaya.likelihoods.base_classes import CMBlikes
from plik_lite import NativePlikLite
from preparation import ROOT,OUT

def main():
    packages=ROOT/'inputs/native_packages'
    lowT=TT(packages_path=str(packages));lowE=EE(packages_path=str(packages))
    dataset='smicadx12_Dec5_ftl_mv2_ndclpp_p_teb_consext8_CMBmarged.dataset'
    lens=CMBlikes({'path':str(ROOT/'inputs/lensing_native'),'dataset_file':dataset})
    baseline=np.load(OUT/'standard_lens_a2.5.npz');pp=baseline['pp_Dl']
    source=np.load(OUT/'SOURCE_lens_a2.5.npz')['phi_Dl']
    pp_plus=pp.copy();pp_plus[:len(source)]+=source
    cmb=np.load(OUT/'lensed_combination.npz');high=NativePlikLite();rows=[]
    for name,dl,potential in [('baseline',cmb['baseline_lensed'],pp),('baseline_plus_SOURCE',cmb['combined'],pp_plus)]:
        ht=high.evaluate(dl)['chi2_highell'];lt=float(lowT.log_likelihood(dl[:,0],calib=1))
        le=float(lowE.log_likelihood(dl[:,1],calib=1))
        ll=float(lens.log_likelihood({'pp':potential}))
        rows.append(dict(case=name,high_ell_quadratic_form=ht,low_T_minus2logL=-2*lt,
            low_E_minus2logL=-2*le,lensing_CMBmarged_minus2logL=-2*ll,
            combined_minus2logL_up_to_constants=ht-2*lt-2*le-2*ll,
            finite=bool(np.isfinite([ht,lt,le,ll]).all())))
    result=dict(date='2026-10-14',cases=rows,lensing_bin_count=lens.nbins,
        A_planck_fixed=1,low_T_range=[2,29],low_E_range=[2,29],high_ell_bin_count=613,
        source_deflection_covariance_included=True,official_clik_executable_used=False,
        implementation='Cobaya 3.6.2 native TT/EE and CMBlikes; public Planck CMB-marginalized lensing dataset; native Gaussian Plik-lite',
        likelihood_offsets_not_identical_between_blocks=True,
        scope='Expanded conditional native likelihood evaluation. Report individual blocks and differences; the summed offset-dependent -2logL is not a universal chi-square with a simple degree count.')
    result['SOURCE_change_combined_minus2logL']=rows[1]['combined_minus2logL_up_to_constants']-rows[0]['combined_minus2logL_up_to_constants']
    assert all(x['finite'] for x in rows)
    (OUT/'expanded_likelihood_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
