"""Numerical controls for finite mean preparation and covariance lensing."""
import json
import numpy as np
from scipy.linalg import cho_solve
from camb.correlations import lensed_cls
from preparation import OUT
from lensing import source,L_INPUT,L_OUT
from plik_lite import NativePlikLite

def main():
    c1,p1=source(1.5);c2,p2=source(2.5)
    prep=json.loads((OUT/'preparation_results.json').read_text())
    init=json.loads((OUT/'initial_callback_check.json').read_text())
    norm=json.loads((OUT/'phi_transfer_normalization.json').read_text())
    expanded=json.loads((OUT/'expanded_likelihood_results.json').read_text())
    saved=np.load(OUT/'lensed_combination.npz')
    base=np.load(OUT/'standard_lens_a2.5.npz')
    like=NativePlikLite();controls=[]
    reference=saved['baseline_lensed']
    for label,lmax,sampling in [('input_L5000',5000,1.4),('sampling_1.8',L_INPUT,1.8),('CAMB_native_lensed',None,None)]:
        if lmax is None:
            arr=base['lensed_Dl'][:L_OUT+1]
        else:
            arr=lensed_cls(base['unlensed_Dl'][:lmax+1],base['pp_Dl'][:lmax+1],lmax=lmax,
                lmax_lensed=L_OUT,sampling_factor=sampling,theta_max=None)
        delta=like.bins(arr)-like.bins(reference)
        whitened_Q=float(delta@cho_solve(like.chol,delta))
        controls.append(dict(control=label,high_ell_Q=like.evaluate(arr)['chi2_highell'],
            bin_difference_quadratic_form=whitened_Q,bin_difference_whitened_RMS=float(np.sqrt(whitened_Q/613)),
            max_abs_TT_Dl_difference_uK2=float(abs(arr[:,0]-reference[:,0]).max())))
    phi_change=float(abs(p2-p1).max()/p2.max())
    cmb_change=float(abs(c2-c1).max()/abs(c2).max())
    ss=np.load(OUT/'SOURCE_lens_a2.5.npz')
    ell=ss['ell'][2:].astype(np.float64);fac=ell*(ell+1)
    tt=2*np.pi*c2[2:,0]/fac;ee=2*np.pi*c2[2:,1]/fac
    rawphi=2*np.pi*p2[2:]/fac**2
    cross=ss['Tphi_Ephi_raw'][2:]
    excess=float(np.max(np.c_[cross[:,0]**2-tt*rawphi,cross[:,1]**2-ee*rawphi]))
    rows=dict(prep['checks'])
    rows.update(initial_callback_agreement=init['passed'],phi_transfer_normalization=norm['passed'],
        SOURCE_transfer_accuracy_stable=phi_change<.01 and cmb_change<.01,
        SOURCE_phi_positive=bool(p2.min()>=0),SOURCE_CMB_auto_positive=bool(c2[:,0].min()>=0 and c2[:,1].min()>=0),
        SOURCE_primary_lens_covariance_positive=excess<1e-40,
        finite_lensed_outputs=bool(np.isfinite(saved['combined']).all()),
        native_likelihood_blocks_finite=all(x['finite'] for x in expanded['cases']),
        high_ell_remapping_controls=all(x['bin_difference_whitened_RMS']<.01 for x in controls),
        no_SOURCE_amplitude_retuning=not json.loads((OUT/'lensing_results.json').read_text())['SOURCE_amplitude_changed'])
    result=dict(check_count=len(rows),passed_count=sum(rows.values()),checks=rows,
        SOURCE_phi_accuracy_max_relative_change=phi_change,SOURCE_CMB_accuracy_max_relative_change=cmb_change,
        SOURCE_primary_lens_covariance_excess=excess,baseline_remapping_controls=controls,
        meaning='Numerical and covariance checks for the declared mean-stress and leading-covariance model. No proof of dynamical preparation or single-outcome gravity.')
    (OUT/'validation_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result),flush=True)
    if not all(rows.values()):raise SystemExit('A numerical validation condition failed')

if __name__=='__main__':main()
