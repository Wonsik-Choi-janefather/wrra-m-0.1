from common import OUT,IN,DT
import json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from supply import averaging_factor

def main():
    supply=json.loads((OUT/'supply_results.json').read_text())
    photons=json.loads((OUT/'photon_results.json').read_text())
    cmb=np.load(OUT/'CMB_higher_moment_arrays.npz')
    standard=np.load(IN/'standard_lens_a2.5.npz')
    fig,axes=plt.subplots(2,2,figsize=(12,9),layout='constrained')
    times=np.logspace(-12,1,500)
    initial=supply['validation_inputs']['relative_intrinsic_RMS_P_D_R'][1]
    target=supply['validation_inputs']['mean_profile_RMS_D_R'][0]
    for r,label in [(0,'Static bit'),(1,'Independent shutters'),(1/128,'Refresh probability 1/128'),(1e-6,'Refresh probability 1e-6')]:
        value=[initial*np.sqrt(averaging_factor(max(1,round(t/DT)),r)) for t in times]
        axes[0,0].loglog(times,value,label=label)
    axes[0,0].axhline(target,color='black',ls='--',label='Mean-profile RMS')
    axes[0,0].set(xlabel='Averaging time (s)',ylabel='Intrinsic dark relative RMS',
        title='1. Correlation-dependent averaging')
    axes[0,0].legend(fontsize=8);axes[0,0].grid(alpha=.2)
    rows=[x for x in photons['outputs']['pulse_predictions'] if x['exposure_m']==1]
    energy=np.array([x['energy_eV'] for x in rows])
    axes[0,1].loglog(energy,[x['original_pulse_time_RMS_s']*1e18 for x in rows],label='Prepared Gaussian pulse')
    axes[0,1].loglog(energy,[x['nonselective_pulse_time_RMS_s']*1e18 for x in rows],label='With static SOURCE mixture')
    axes[0,1].axhline(photons['outputs']['fixed_SOURCE_delay_RMS_at_1m_s']*1e18,color='gray',ls='--',label='Achromatic SOURCE delay RMS')
    axes[0,1].set(xlabel='Photon energy (eV)',ylabel='Pulse width RMS (attoseconds)',
        title='2. Fixed 1% bandwidth; exposure 1 m')
    axes[0,1].legend(fontsize=8);axes[0,1].grid(alpha=.2)
    ell=cmb['ell'];sel=ell<=2508
    dl=ell*(ell+1)/(2*np.pi)*cmb['Cl_T_E_phi'][0]
    axes[1,0].loglog(ell[sel],dl[sel],label='SOURCE TT, actual transfers')
    axes[1,0].loglog(ell[sel],standard['unlensed_Dl'][ell[sel],0],label='Unlensed Gaussian reference TT')
    axes[1,0].set(xlabel='Multipole ell',ylabel='D_ell (microK squared)',title='3. Power normalization control')
    axes[1,0].legend(fontsize=8);axes[1,0].grid(alpha=.2)
    eq=list(csv.DictReader((OUT/'CMB_equilateral_bispectra_ell2_6000.csv').open()))
    eq=[x for x in eq if x['field']=='T' and int(x['ell'])<=256 and int(x['ell'])%2==0]
    axes[1,1].plot([int(x['ell']) for x in eq],[float(x['reduced_b']) for x in eq])
    axes[1,1].set_yscale('symlog',linthresh=1e-17)
    axes[1,1].set(xlabel='Multipole ell',ylabel='Reduced b_ell,ell,ell (microK cubed)',
        title='4. Conditional shared-phase TTT bispectrum')
    axes[1,1].grid(alpha=.2)
    fig.savefig(OUT/'three_tracks_summary.png',dpi=170)
    plt.close(fig)

if __name__=='__main__':main()
