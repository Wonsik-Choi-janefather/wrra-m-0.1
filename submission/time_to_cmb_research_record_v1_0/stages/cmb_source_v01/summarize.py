from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from calculate import ROOT,OUT,record,assemble
from plik_lite import NativePlikLite

def main():
    like=NativePlikLite();cases=[];checks={};regression={};conv={};baseline_conv={}
    for b in ['weighted','unweighted']:
        low=assemble(b,1.5);high=assemble(b,2.5)
        std=np.load(OUT/f'{b}_standard_a1.5_f1.npz')['Dl']
        zero=np.load(OUT/f'{b}_zero_a1.5_f1.npz')['Dl']
        archive=np.loadtxt(ROOT/f'inputs/{b}_uniform_g_parity_Dl.csv',delimiter=',',skiprows=1)[:,1:]
        matched=np.load(OUT/f'{b}_standard_a1.5_f1_l2500.npz')['Dl']
        hi=np.load(OUT/f'{b}_standard_a2.5_f1.npz')['Dl']
        plus=np.loadtxt(OUT/f'{b}_baseline_plus_SOURCE_a2.5_Dl.csv',delimiter=',',skiprows=1)[:,1:]
        regression[b]=dict(zero_max_relative_TT_EE=float(np.max(abs(zero[2:,:2]/std[2:,:2]-1))),
            archive_max_relative_TT_EE=float(np.max(abs(archive[2:,:2]/matched[2:,:2]-1))))
        lo_source=np.loadtxt(OUT/f'{b}_SOURCE_a1.5_f1_Dl.csv',delimiter=',',skiprows=1)[:,1:]
        hi_source=np.loadtxt(OUT/f'{b}_SOURCE_a2.5_f1_Dl.csv',delimiter=',',skiprows=1)[:,1:]
        convergence=np.max(abs(hi_source-lo_source),axis=0)/np.maximum(np.max(abs(hi_source),axis=0),1e-30)
        conv[b]=dict(zip(['TT','EE','BB','TE'],convergence.tolist()))
        baseline_conv[b]=dict(low_chi2=like.evaluate(std)['chi2_highell'],high_chi2=like.evaluate(hi)['chi2_highell'],
            high_minus_low_chi2=like.evaluate(hi)['chi2_highell']-like.evaluate(std)['chi2_highell'])
        high['fixed_background_parameters']={k:record(b)[k] for k in ['H0_derived_km_s_Mpc','ombh2','omch2','u_P_D_R_today_J_m3']}
        high['native_plik_lite_baseline']=like.evaluate(hi)
        high['native_plik_lite_plus_SOURCE']=like.evaluate(plus)
        high['SOURCE_delta_chi2']=like.evaluate(plus)['chi2_highell']-like.evaluate(hi)['chi2_highell']
        cases.append(high)
        checks[b+'_SOURCE_zero_restores_baseline']=regression[b]['zero_max_relative_TT_EE']<1e-8
        checks[b+'_archived_baseline_reproduced']=regression[b]['archive_max_relative_TT_EE']<1e-8
        checks[b+'_SOURCE_spectrum_convergence']=bool(max(convergence)<.002)
        checks[b+'_auto_spectra_nonnegative']=bool(np.all(hi_source[:,[0,1]]>=0))
        checks[b+'_TE_covariance']=high['SOURCE_TE_covariance_excess']<=1e-20
    normal=np.load(OUT/'weighted_R_a1.5_f1.npz');early=np.load(OUT/'weighted_R_a1.5_f1_s0.1.npz')
    initial_time={k:float(np.max(abs(normal[k]-early[k]))/max(abs(normal[k]).max(),1e-30)) for k in ['T','E']}
    checks['tenfold_earlier_start_convergence']=max(initial_time.values())<.001
    audit=json.loads((OUT/'evolution_audit.json').read_text())
    for a in audit[:2]:
        b=a['branch']
        checks[b+'_independent_momentum_integral']=a['independent_integrating_factor_relative_error']<1e-6
        checks[b+'_linear_regime']=a['linear_gate_0_1_pass']
        checks[b+'_vacuum_time_independent']=a['vacuum_contrast_drift']==0
    checks['omitted_vacuum_force_negative_control_fails']=audit[2]['independent_integrating_factor_relative_error']>.99
    result=dict(version='CMB SOURCE response 0.1',date='2026-10-14',cases=cases,regression=regression,
        SOURCE_spectrum_relative_convergence=conv,baseline_precision=baseline_conv,
        earlier_start_transfer_convergence=initial_time,evolution_audit=audit,checks=checks,all_numerical_checks_pass=all(checks.values()),
        input='Frozen finite SOURCE/supply harmonic vectors and weighted/unweighted background ledger',
        transformation='Residue kernel -> addressed supply probability -> conserved dark/vacuum stress -> patched CAMB photon/neutrino evolution -> exact seven-k transfer -> phase/orientation averaged TT/TE/EE',
        additional_conditions=[
            'Radiation-era extension: frozen delta_u_D0/u_D0 interpreted as the regular CDM-isocurvature entropy amplitude, not an inverse solution of the old a=.02 initial data.',
            'delta_R=delta_u_R/u_R0 is time independent; regular forced dark velocity; higher-order vacuum initial metric corrections negligible at tested start times.',
            'Uniform global spatial phase and uniform orientation define the angular ensemble; D/R covariance at each harmonic retained.',
            'SOURCE ensemble independent of inherited standard adiabatic perturbations; no cross term.',
            'Existing macro anchor k1=.05 Mpc^-1 and epsilon=1e-8 retained; no new fit.',
            'SOURCE angular spectra are linear and unlensed; adding them to a standard lensed baseline is a stated first-order diagnostic, not a completed new SOURCE lensing model.',
            'Native high-ell Plik-lite Gaussian covariance likelihood with A_planck=1; no low-ell or lensing likelihood and no official clik executable.'],
        scope='Conditional CMB consistency test of a conserved, early-extended SOURCE candidate. Good baseline agreement does not identify the very small extra SOURCE contribution.',
        refutation_conditions=[
            'Same fixed SOURCE map fails energy/momentum conservation or leaves the declared linear regime.',
            'Zero-source limit fails baseline restoration; start-time or resolution tests fail.',
            'A frozen branch disagrees with the data under agreed likelihood and completed modeling assumptions.',
            'A required primordial preparation, phase covariance or lensing completion cannot be realized internally.'],
        no_new_parameter_optimizer=True)
    (OUT/'results.json').write_text(json.dumps(result,indent=2))
    # Full spectrum and SOURCE contribution are shown separately because subtraction loses precision.
    fig,axs=plt.subplots(3,2,figsize=(13,11),sharex=True)
    for row,(label,c,release) in enumerate([('TT',0,'3.01'),('TE',3,'3.02'),('EE',1,'3.02')]):
        data=np.loadtxt(ROOT/f'inputs/COM_PowerSpect_CMB-{label}-binned_R{release}.txt')
        axs[row,0].errorbar(data[:,0],data[:,1],yerr=[data[:,2],data[:,3]],fmt='.',color='#666',alpha=.5,ms=2,label='Planck PR3 public bins')
        for b,color in [('weighted','#1f6aa5'),('unweighted','#d47935')]:
            full=np.loadtxt(OUT/f'{b}_baseline_plus_SOURCE_a2.5_Dl.csv',delimiter=',',skiprows=1)
            source=np.loadtxt(OUT/f'{b}_SOURCE_a2.5_f1_Dl.csv',delimiter=',',skiprows=1)
            axs[row,0].plot(full[:,0],full[:,c+1],lw=1,label=b,color=color)
            axs[row,1].plot(source[:,0],source[:,c+1],lw=1,label=b,color=color)
        for ax in axs[row]:ax.grid(alpha=.2);ax.set_xlim(2,2508)
        axs[row,0].set_ylabel(label+r' $D_\ell$ [$\mu K^2$]')
        if label!='TE':axs[row,1].set_yscale('log');axs[row,1].set_ylim(1e-17,1e-4)
        else:axs[row,1].set_yscale('symlog',linthresh=1e-11)
    axs[0,0].set_title('Conditional baseline + linear SOURCE');axs[0,1].set_title('SOURCE contribution alone (different scale)')
    axs[0,0].legend(fontsize=9);axs[0,1].legend(fontsize=9)
    for ax in axs[-1]:ax.set_xlabel(r'Multipole $\ell$')
    fig.suptitle('Frozen inputs; conserved dark/vacuum force; explicit primordial extension\nSOURCE is unlensed; no new cosmological fit',fontsize=12)
    fig.tight_layout();fig.savefig(OUT/'SOURCE_CMB_comparison.png',dpi=170);plt.close(fig)
    print(json.dumps(dict(checks_passed=sum(checks.values()),checks_total=len(checks),
        native_high_ell_chi2={r['branch']:r['native_plik_lite_plus_SOURCE']['chi2_highell'] for r in cases},
        source_TT_max={r['branch']:r['maximum_SOURCE_TT_Dl_uK2'] for r in cases})),flush=True)

if __name__=='__main__':main()
