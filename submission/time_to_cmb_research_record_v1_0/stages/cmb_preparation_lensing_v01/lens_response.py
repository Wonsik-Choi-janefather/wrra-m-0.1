"""Mean SOURCE lensing response using the adopted covariance remapping kernel."""
import json,numpy as np
from camb.correlations import lensed_cls
from lensing import source,OUT,L_INPUT,L_OUT
from plik_lite import NativePlikLite

def main():
    C,pp=source(2.5);base=np.load(OUT/'standard_lens_a2.5.npz')
    unl=base['unlensed_Dl'][:L_INPUT+1];bp=base['pp_Dl'][:L_INPUT+1]
    kw=dict(lmax=L_INPUT,lmax_lensed=L_OUT,sampling_factor=1.4,theta_max=None)
    b0=lensed_cls(unl,bp,**kw)
    b1=lensed_cls(unl,bp+pp,**kw)
    ss=lensed_cls(C,bp+pp,**kw)
    combined=b1+ss
    L=np.arange(len(pp));good=L>0
    source_var=float(np.sum((2*L[good]+1)*pp[good]/(2*L[good]*(L[good]+1))))
    std_var=float(np.sum((2*L[good]+1)*bp[good]/(2*L[good]*(L[good]+1))))
    lens_shift=b1-b0
    like=NativePlikLite()
    result=dict(date='2026-10-14',input_lmax=L_INPUT,output_lmax=L_OUT,
        SOURCE_deflection_RMS_rad=np.sqrt(source_var),SOURCE_deflection_RMS_arcsec=np.sqrt(source_var)*180/np.pi*3600,
        standard_deflection_RMS_arcsec=np.sqrt(std_var)*180/np.pi*3600,
        source_to_standard_deflection_variance_ratio=source_var/std_var,
        SOURCE_phi_Dl_max=float(pp.max()),SOURCE_phi_Dl_peak_L=int(pp.argmax()),
        SOURCE_phi_tail_L5800_fraction=float(pp[5800:].sum()/pp.sum()),
        SOURCE_lensing_on_baseline_max_abs_Dl_uK2=dict(zip(['TT','EE','BB','TE'],np.max(abs(lens_shift),axis=0).tolist())),
        baseline_remap_high_ell_chi2=like.evaluate(b0)['chi2_highell'],
        baseline_plus_lensed_SOURCE_high_ell_chi2=like.evaluate(combined)['chi2_highell'],
        SOURCE_primary_lensed_max_TT_Dl_uK2=float(ss[:,0].max()),
        covariance_lensing_executed=True,nonGaussian_SOURCE_exact_remapping=False,
        approximation='Adopted standard isotropic covariance lensing kernel. SOURCE deflection contribution included at leading covariance order; finite SOURCE higher connected moments and primary/lens correlations not fully remapped.',
        SOURCE_amplitude_changed=False,likelihood='Native high-ell Plik-lite with fixed A_planck=1')
    (OUT/'lensing_results.json').write_text(json.dumps(result,indent=2))
    np.savez_compressed(OUT/'lensed_combination.npz',ell=np.arange(L_OUT+1),baseline_lensed=b0,
        baseline_with_SOURCE_lens=b1,SOURCE_primary_lensed=ss,combined=combined,SOURCE_lens_change=lens_shift)
    np.savetxt(OUT/'candidate_SOURCE_lensed_Dl.csv',np.c_[np.arange(L_OUT+1),combined],delimiter=',',header='ell,TT,EE,BB,TE [microK^2]',comments='')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
