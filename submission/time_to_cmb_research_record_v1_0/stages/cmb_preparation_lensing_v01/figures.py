"""Scientific plots of executed lensing and finite-preparation diagnostics."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'results'

def main():
    s=np.load(OUT/'SOURCE_lens_a2.5.npz');b=np.load(OUT/'standard_lens_a2.5.npz')
    fig,ax=plt.subplots(1,2,figsize=(11,4.2),constrained_layout=True)
    l=s['ell'];sel=(l>=2)&(l<=2500)&(s['phi_Dl']>0)
    ax[0].loglog(l[sel],s['phi_Dl'][sel],label='Address-generated SOURCE')
    ax[0].loglog(l[sel],b['pp_Dl'][:len(l)][sel],label='Adopted standard component')
    ax[0].set(xlabel='L',ylabel=r'$[L(L+1)]^2 C_L^{\phi\phi}/(2\pi)$',title='Executed lensing-potential spectra')
    ax[0].legend();ax[0].grid(alpha=.25)
    c=np.load(OUT/'lensed_combination.npz');ell=c['ell'][2:]
    ax[1].plot(ell,c['SOURCE_lens_change'][2:,0]*1e6,label='TT')
    ax[1].plot(ell,c['SOURCE_lens_change'][2:,1]*1e6,label='EE')
    ax[1].set(xlabel=r'$\ell$',ylabel=r'Change in $D_\ell$ [$10^{-6}\,\mu K^2$]',title='SOURCE deflection acting on baseline')
    ax[1].legend();ax[1].grid(alpha=.25)
    fig.savefig(OUT/'lensing_diagnostics.png',dpi=170);plt.close(fig)
    p=json.loads((OUT/'preparation_results.json').read_text())
    fig,ax=plt.subplots(figsize=(7,4.2),constrained_layout=True)
    x=np.arange(2);w=.32
    ax.bar(x-w/2,p['mean_stress_relative_RMS_D_R'],w,label='Phase variation of mean stress')
    ax.bar(x+w/2,p['independent_supplier_intrinsic_relative_RMS_P_D_R'][1:],w,label='Intrinsic supply variance: independent bits')
    ax.set(yscale='log',xticks=x,xticklabels=['Dark D','Vacuum R'],ylabel='Relative RMS',title='Two different variances; no automatic gravity identification')
    ax.legend(fontsize=8);ax.grid(axis='y',alpha=.25)
    fig.savefig(OUT/'preparation_variance_diagnostic.png',dpi=170);plt.close(fig)

if __name__=='__main__':main()
