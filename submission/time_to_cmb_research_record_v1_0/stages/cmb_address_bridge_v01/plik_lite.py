"""Fixed-calibration Gaussian high-ell Plik-lite native data evaluation.
Formula and data convention: Cobaya PlanckPlikLite, Calabrese/Lewis.
Includes TT/TE/EE cross covariance and actual bin weights. No low-ell likelihood.
"""
import numpy as np
from scipy.io import FortranFile
from scipy.linalg import cho_factor,cho_solve
from calculate_reference import ROOT

class NativePlikLite:
    def __init__(self):
        d=ROOT/'inputs/plik_lite_native'
        self.data=np.loadtxt(d/'cl_cmb_plik_v22.dat')[:,1]
        self.blmin=np.loadtxt(d/'blmin.dat').astype(int)+30
        self.blmax=np.loadtxt(d/'blmax.dat').astype(int)+30
        w=np.loadtxt(d/'bweight.dat');ls=np.arange(len(w))+30
        self.weights=np.r_[np.zeros(30),w*2*np.pi/ls/(ls+1)]
        with FortranFile(d/'c_matrix_plik_v22.dat','r') as f:
            cov=f.read_reals(dtype=np.float64).reshape(613,613)
        self.cov=np.tril(cov)+np.tril(cov,-1).T
        self.chol=cho_factor(self.cov,lower=True)
        assert self.data.shape==(613,)
        assert np.max(abs(self.cov-self.cov.T))==0

    def bins(self,dl,A_planck=1):
        values=[]
        for c,n in [(0,215),(3,199),(1,199)]:
            for i in range(n):
                lo,hi=self.blmin[i],self.blmax[i]
                if hi>=len(dl):raise ValueError('Spectrum misses a likelihood bin')
                values.append(np.dot(dl[lo:hi+1,c],self.weights[lo:hi+1]))
        return np.array(values)/A_planck**2

    def evaluate(self,dl,A_planck=1):
        theory=self.bins(dl,A_planck)
        residual=self.data-theory
        value=float(residual@cho_solve(self.chol,residual))
        return dict(chi2_highell=value,logL_up_to_constant=-.5*value,
            A_planck_fixed=A_planck,bin_count=613,TT_bin_count=215,TE_bin_count=199,EE_bin_count=199,
            method='Native Gaussian Plik-lite TTTEEE, full released covariance and bin weights; fixed calibration',
            official_clik_executable_used=False,lowell_or_lensing_likelihood_included=False)
