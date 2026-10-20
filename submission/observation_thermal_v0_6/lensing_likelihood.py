"""Native correlated Gaussian SPT-Planck likelihood, including response windows.
Input TT = ell(ell+1) C_TT/2pi [microK^2]; PP = [L(L+1)]^2 C_phiphi/2pi.
No diagonal-error approximation and no fitted cosmological parameters.
"""
from pathlib import Path
import json,math,sys
import numpy as np
from scipy.linalg import cho_factor,cho_solve
from scipy.stats import chi2
P=Path(__file__).resolve().parent
DATA=P/'inputs/sptplanck/sptplanck_lenslike/data/sptplanck_lensing/sptplanck_fgrm'

class LensingLikelihood:
    def __init__(self):
        self.band=np.loadtxt(DATA/'bandpowers.dat');self.d=self.band[:,4]
        self.cov=np.loadtxt(DATA/'cov.dat');self.chol=cho_factor(self.cov,lower=True)
        self.logdet=2*np.log(np.diag(self.chol[0])).sum()
        self.fid=np.loadtxt(DATA/'lensing_fiducial_correction.dat')[:,1]
        self.W=np.zeros((18,3001));self.Rtt=self.W.copy();self.Rpp=self.W.copy()
        for j in range(18):
            w=np.loadtxt(DATA/f'windows/window{j+1}.dat');ix=w[:,0].astype(int);self.W[j,ix]=w[:,1]
            w=np.loadtxt(DATA/f'lens_delta_windows/window{j+1}.dat');ix=w[:,0].astype(int)
            self.Rtt[j,ix]=w[:,1];self.Rpp[j,ix]=w[:,2]
    def predict(self,PP,TT):
        PP=np.asarray(PP);TT=np.asarray(TT)
        if min(len(PP),len(TT))<3001 or not np.isfinite(PP).all() or not np.isfinite(TT).all():
            raise ValueError('Require finite spectra over L=0..3000')
        return (self.W+self.Rpp)@PP[:3001]+self.Rtt@TT[:3001]-self.fid
    def evaluate(self,PP,TT):
        b=self.predict(PP,TT);delta=b-self.d;ch=float(delta@cho_solve(self.chol,delta))
        return dict(chi2=ch,minus_loglike=ch/2,
            normalized_loglike=-.5*(ch+self.logdet+18*math.log(2*math.pi)),
            fixed_model_reference_tail_probability=float(chi2.sf(ch,18)),bins=18),b
    def amplitude_profile(self,PP,TT):
        v=(self.W+self.Rpp)@PP[:3001];offset=self.Rtt@TT[:3001]-self.fid
        ci=cho_solve(self.chol,v);sigma=1/math.sqrt(float(v@ci))
        A=float((self.d-offset)@ci)*sigma*sigma
        return dict(A_phi_profile=A,sigma_A=sigma,
            chi2_profile=float((A*v+offset-self.d)@cho_solve(self.chol,A*v+offset-self.d)),
            role='Diagnostic fitted lensing-amplitude multiplier, not a WRRA-derived parameter or a fit of As.')

def spectra(name):
    z=np.load(P/'results'/f'{name}.npz');ell=z['ell']
    return z['clpp']*(ell*(ell+1))**2/(2*np.pi),z['lensed'][:,0]

def reference_chi(PP,TT):
    # Separate official CosmoMC implementation, with syntax-only NumPy 2 aliases.
    sys.path.insert(0,str(P/'runtime'))
    source=(P/'inputs/CMBlikes_reference.py').read_text()
    source=source.replace('np.object','object').replace('np.int','int')
    scope={'__name__':'CMBlikes_reference','__file__':str(P/'inputs/CMBlikes_reference.py')}
    exec(compile(source,scope['__file__'],'exec'),scope)
    ref=scope['DatasetLikelihood'](str(DATA.parent/'sptplanck_fgrm.dataset'))
    array=scope['ClsArray']();array.lmax=len(PP)-1;array.lmin=0
    array.cls_array[3,3]=PP;array.cls_array[0,0]=TT
    return float(ref.chi_squared(array))

def main():
    like=LensingLikelihood();rows=[];predictions=[]
    for name in ['linear','nonlinear','unweighted_nonlinear','nonlinear_refined']:
        pp,tt=spectra(name);r,b=like.evaluate(pp,tt);r['name']=name
        r['amplitude_profile']=like.amplitude_profile(pp,tt)
        r['official_CosmoMC_chi2']=reference_chi(pp,tt)
        r['official_reference_difference']=abs(r['chi2']-r['official_CosmoMC_chi2'])
        rows.append(r);predictions.append(b)
    pp,tt=spectra('nonlinear');zero,_=like.evaluate(np.zeros_like(pp),tt)
    covdiag=np.sqrt(np.diag(like.cov));dataerr=like.band[:,5]
    refined=predictions[-1];base=predictions[1]
    difference=refined-base
    report=dict(models=rows,null_lensing=zero,
        diagonal_error_consistency=float(np.max(abs(covdiag/dataerr-1))),
        max_covariance_correlation=float(np.max(abs(like.cov/np.outer(covdiag,covdiag)-np.eye(18)))),
        numerical_refinement_distance_sigma=float(np.sqrt(difference@cho_solve(like.chol,difference))),
        full_state_WRRA_evaluation=False,
        scope='Conditional lensing test of inherited WRRA background plus declared calibrated adiabatic primordial completion. Neither full v0.4 perturbations nor v0.5 events enter these spectra. Gaussian released-data likelihood includes TT and PP response corrections. Tail probabilities use fixed 18-bin models; no look-elsewhere or full-cosmology posterior claimed.')
    (P/'results/lensing_likelihood.json').write_text(json.dumps(report,indent=2)+'\n')
    np.savez_compressed(P/'results/lensing_band_predictions.npz',L=like.band[:,3],data=like.d,
        covariance=like.cov,names=np.array([x['name'] for x in rows]),predictions=np.array(predictions))
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
