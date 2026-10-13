"""Fixed-ledger observable adapter. No fitting and no invented spatial bridge.

The executed route adopts standard GR, plasma history and primordial perturbations.
The microscopic-only route refuses to substitute these missing constitutive data.
Run: OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python run.py
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
from pathlib import Path
import argparse, hashlib, json, importlib.util
import numpy as np
import camb
from camb import constants as c, bbn
from scipy.signal import find_peaks
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
INPUT = ROOT/'inputs'
OUT = ROOT/'results'
ETA = np.array([7.5615824991e-10, 7.2857613288e-10, 7.6461028188e-10])
NU = np.array([0., 0., 3.])
# SI quantities are carried only in this declared post-reading completion.
U100 = 3*(100000/c.Mpc)**2*c.c**2/(8*np.pi*c.G)
FIXED = dict(As=2.1e-9, ns=0.9649, tau=0.0544, TCMB=2.7255,
             mnu=0.06, nnu=3.044, pivot_scalar=0.05)
Z_BAO = np.array([0.38, 0.51, 0.61])
MICRO_MISSING = ['physical_3D_embedding_and_k_Mpc',
                 'primordial_curvature_covariance_from_address_state',
                 'physical_density_velocity_and_rest_frame_pressure_closure',
                 'anisotropic_stress_dynamics_and_covariant_conservation']

def require_microscopic_bridge(fields):
    missing = [k for k in MICRO_MISSING if fields.get(k) is None]
    if missing:
        raise ValueError('Microscopic-only evaluation unavailable: '+', '.join(missing))
    return True

def hash_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def inputs_to_loads():
    p6 = json.loads((INPUT/'p6_results.json').read_text())
    with np.load(INPUT/'positive_profile_and_payload.npz') as z:
        for branch in ('weighted', 'unweighted'):
            masses = z[branch+'_sector_residue_slot_payload'].sum(axis=(1,2))
            actual = next(x for x in p6['cases'] if x['branch']==branch)
            # Verify the inherited means directly from residue-resolved payload.
            # Multiples of 3 were prepared uniformly, other addresses in mode 8.
            uniform = np.arange(30)%3==0
            mode8 = 1-np.cos(2*np.pi*8/128)
            response = np.where(uniform,1.,mode8)
            response_P_D_R = np.vstack([np.ones(30),response,response])
            direct = (z[branch+'_sector_residue_slot_payload'].sum(2)*response_P_D_R).sum(1)
            if not np.allclose(direct,actual['mean_P_D_R_load'],atol=2e-12,rtol=0):
                raise ValueError('Residue-resolved loads disagree with inherited P6 mean')
            yield branch+'_uniform', masses
            yield branch+'_correlated', np.array(actual['mean_P_D_R_load'])

def standard_params(H0, wb, wc, accuracy=1.5):
    p = camb.CAMBparams()
    p.set_cosmology(H0=H0, ombh2=wb, omch2=wc, omk=0,
                    mnu=FIXED['mnu'], nnu=FIXED['nnu'], tau=FIXED['tau'],
                    TCMB=FIXED['TCMB'], bbn_predictor='PRIMAT_Yp_DH_ErrorMC_2024.dat')
    p.InitPower.set_params(As=FIXED['As'], ns=FIXED['ns'], pivot_scalar=FIXED['pivot_scalar'])
    p.set_dark_energy(w=-1, wa=0, dark_energy_model='fluid')
    p.set_for_lmax(2500, lens_potential_accuracy=0)
    p.NonLinear = camb.model.NonLinear_none
    p.set_accuracy(AccuracyBoost=accuracy, lAccuracyBoost=accuracy, lSampleBoost=accuracy)
    p.scalar_initial_condition = 'initial_adiabatic'
    return p

def thermal_budget():
    # Disjoint added thermal components: P is baryon, D is cold toy stress,
    # R is vacuum. D is NOT silently reduced by the added neutrino budget.
    p = standard_params(100., .0224, .12)
    r = camb.get_background(p)
    return {k:float(r.get_Omega(k)) for k in ('photon','neutrino','nu')}

def diagnostic(ell, dl):
    out = {}; allres = []
    for name, col, release in [('TT',0,'3.01'),('TE',3,'3.02'),('EE',1,'3.02')]:
        data = np.loadtxt(INPUT/f'COM_PowerSpect_CMB-{name}-binned_R{release}.txt')
        # Bin-centre interpolation only, not proper experimental windows.
        sigma = (data[:,2]+data[:,3])/2
        residual = (np.interp(data[:,0], ell, dl[:,col])-data[:,1])/sigma
        out[name] = {'bin_count':len(data), 'RMS_in_public_bin_sigma':float(np.sqrt(np.mean(residual**2))),
                     'diagonal_Q':float(residual@residual)}
        allres.extend(residual)
    out['all'] = {'bin_count':len(allres), 'RMS_in_public_bin_sigma':float(np.sqrt(np.mean(np.array(allres)**2))),
                  'diagonal_Q':float(np.sum(np.array(allres)**2))}
    return out

def calculate(case, load, thermal, accuracy=1.5, save=True):
    u = ETA*load
    wb, wc, wv = u/U100
    h2 = float(wb+wc+wv+sum(thermal.values()))
    H0 = 100*np.sqrt(h2)
    p = standard_params(H0, wb, wc, accuracy)
    r = camb.get_results(p)
    dl = r.get_total_cls(lmax=2500, CMB_unit='muK', raw_cl=False)
    cl = r.get_total_cls(lmax=2500, CMB_unit='muK', raw_cl=True)
    ell = np.arange(len(dl))
    a = np.geomspace(1e-8, 1, 240)
    expected = u[None,:]*a[:,None]**(NU[None,:]-3)
    p_sector = -NU[None,:]*expected/3
    bg = r.get_background_densities(a, vars=['baryon','cdm','de','photon','neutrino','nu','tot'])
    norm = 3*(100000/c.c)**2  # 3 H100^2/c^2 in Mpc^-2
    actual = np.column_stack([bg[k] for k in ('baryon','cdm','de')])/norm*U100/a[:,None]**4
    thermal_u = sum(bg[k] for k in ('photon','neutrino','nu'))/norm*U100/a**4
    total_u = expected.sum(1)+thermal_u
    H_expected = 100*np.sqrt(total_u/U100)
    H_actual = r.hubble_parameter(1/a-1)
    density_error = float(np.max(np.abs(actual/expected-1)))
    friedmann_error = float(np.max(np.abs(H_actual/H_expected-1)))
    derived = {k:float(v) for k,v in r.get_derived_params().items()}
    # BAO lengths are computed from this same background/recombination result.
    rd = derived['rdrag']
    dm = r.comoving_radial_distance(Z_BAO)
    hz = r.hubble_parameter(Z_BAO)
    dh = c.c/1000/hz
    dv = (Z_BAO*dm**2*dh)**(1/3)
    bao = np.column_stack([Z_BAO,dm/rd,dh/rd,dv/rd,hz,dm])
    pred = bbn.get_predictor('PRIMAT_Yp_DH_ErrorMC_2024.dat')
    dn = FIXED['nnu']-3.044
    if not min(pred.ombh2s)<=wb<=max(pred.ombh2s) or not min(pred.deltans)<=dn<=max(pred.deltans):
        raise ValueError('BBN table extrapolation forbidden')
    bbn_result = {'method':'inherited PRIMAT 2024 interpolation, not a new reaction-network run',
                  'ombh2':float(wb), 'DeltaN':dn, 'Y_He_mass_fraction':float(pred.Y_He(wb,dn)),
                  'Y_p_nucleon_fraction':float(pred.Y_p(wb,dn)), 'D_over_H':float(pred.DH(wb,dn)),
                  'sigma_D_over_H_table':float(pred.get('sig(D/H)',wb,dn)),
                  'sigma_Y_p_table':float(pred.get('sig(Yp^BBN)',wb,dn))}
    peaks, _ = find_peaks(dl[:,0])
    peaks = peaks[(peaks>100)&(peaks<1000)][:3]
    row = {'id':case, 'state_preparation':'I/128' if case.endswith('uniform') else 'existing n mod 3 preparation',
           'readout_operator':'A_P=I, A_D=A_R=Kc/2; inherited commuting epsilon_carrier=0 branch',
           'load_P_D_R':load.tolist(), 'u_P_D_R_today_J_m3':u.tolist(),
           'ombh2':float(wb), 'omch2':float(wc), 'omega_vacuum':float(wv),
           'H0_derived_km_s_Mpc':float(H0), 'age_Gyr':derived['age'],
           'Omega_P_D_R_today':(u/U100/h2).tolist(), 'derived':derived,
           'TT_first_three_peak_ell':peaks.tolist(), 'planck_public_bin_diagnostic':diagnostic(ell,dl),
           'BBN':bbn_result,
           'BAO_rows':bao.tolist(), 'density_relative_error':density_error,
           'friedmann_relative_error':friedmann_error,
           'official_minus2logL':None, 'statistical_rejection':None}
    checks = {case+'_density_ledger_matches_CAMB':density_error<2e-8,
              case+'_friedmann_matches_CAMB':friedmann_error<2e-8,
              case+'_vacuum_density_matches_input':abs(float(r.get_Omega('de'))*h2/wv-1)<2e-8,
              case+'_finite_positive_auto_spectra':bool(np.isfinite(dl).all() and np.all(dl[2:,:3]>=0)),
              case+'_TE_covariance_bound':bool(np.max(np.abs(cl[2:,3])-np.sqrt(cl[2:,0]*cl[2:,1]))<1e-9),
              case+'_Cl_Dl_conversion':bool(np.allclose(dl[2:],cl[2:]*ell[2:,None]*(ell[2:,None]+1)/(2*np.pi),rtol=1e-10)),
              case+'_flat_budget_closure':abs(sum(float(r.get_Omega(k)) for k in ('baryon','cdm','de','photon','neutrino','nu'))-1)<2e-8,
              case+'_BBN_helium_matches_recombination':abs(p.YHe-bbn_result['Y_He_mass_fraction'])<1e-12}
    if save:
        np.savetxt(OUT/f'{case}_Dl.csv',np.column_stack([ell,dl]),delimiter=',',header='ell,TT,EE,BB,TE [microK^2; Dl]',comments='')
        np.savez_compressed(OUT/f'{case}_Cl.npz',ell=ell,tt=cl[:,0],ee=cl[:,1],bb=cl[:,2],te=cl[:,3])
        np.savetxt(OUT/f'{case}_background.csv',np.column_stack([a,expected,p_sector,thermal_u,H_actual]),delimiter=',',header='a,u_P,u_D,u_R [J/m3],p_P,p_D,p_R [Pa],u_thermal [J/m3],H [km/s/Mpc]',comments='')
        np.savetxt(OUT/f'{case}_BAO.csv',bao,delimiter=',',header='z,DM_over_rd,DH_over_rd,DV_over_rd,H_km_s_Mpc,DM_Mpc',comments='')
        (OUT/f'{case}_CAMBparams.txt').write_text(str(p))
    return row,checks,dl

def make_plot(spectra):
    from matplotlib import font_manager
    fonts=font_manager.findSystemFonts()
    korean=next((f for f in fonts if 'NotoSansCJK' in f),None)
    if korean:
        plt.rcParams['font.family']=font_manager.FontProperties(fname=korean).get_name()
        plt.rcParams['axes.unicode_minus']=False
    names={'weighted_uniform':'가중치 적용 · 균일 상태','weighted_correlated':'가중치 적용 · 상관 상태',
           'unweighted_uniform':'가중치 미적용 · 균일 상태','unweighted_correlated':'가중치 미적용 · 상관 상태'}
    if not korean:names={k:k.replace('_',' ') for k in names}
    fig, axs = plt.subplots(3,1,figsize=(10,10),sharex=True)
    colors = ['#3970aa','#e58425','#47764a','#a44384']
    for ax,(spec,col,release) in zip(axs,[('TT',0,'3.01'),('TE',3,'3.02'),('EE',1,'3.02')]):
        data=np.loadtxt(INPUT/f'COM_PowerSpect_CMB-{spec}-binned_R{release}.txt')
        ax.errorbar(data[:,0],data[:,1],yerr=[data[:,2],data[:,3]],fmt='.',ms=2,color='#555555',alpha=.5,label='Planck PR3 공개 구간값' if korean else 'Planck PR3 public bins')
        for (name,dl),color in zip(spectra.items(),colors):
            ax.plot(np.arange(len(dl)),dl[:,col],lw=1.2,color=color,label=names[name])
        ax.set_ylabel(spec+r' $D_\ell$ [$\mu K^2$]');ax.grid(alpha=.2)
        ax.set_xlim(2,2500)
    axs[0].legend(fontsize=8,ncol=2)
    axs[-1].set_xlabel(r'각다중극 $\ell$' if korean else r'Multipole $\ell$')
    fig.suptitle('WRRA 고정 부하 판독 + 명시한 표준 우주론 가정\n추가 피팅 없이 계산한 조건부 토이모델 스펙트럼' if korean else 'Fixed WRRA load readout + declared standard cosmological completion\nNo cosmological fitting; conditional toy-model spectra',fontsize=11)
    fig.tight_layout();fig.savefig(OUT/'conditional_CMB_comparison.png',dpi=180);plt.close(fig)

def main():
    OUT.mkdir(exist_ok=True)
    if camb.__version__!='2.0.4':raise ValueError('Reproducibility requires CAMB 2.0.4')
    if any(k.startswith('WRRA_') for k in os.environ):
        raise ValueError('Clear WRRA patch environment variables before running this standard adapter')
    checks={}; rows=[]; spectra={}
    thermal=thermal_budget()
    for case,load in inputs_to_loads():
        print('Computing '+case,flush=True)
        row,sub,dl=calculate(case,load,thermal)
        rows.append(row);checks.update(sub);spectra[case]=dl
        print(json.dumps({k:row[k] for k in ('id','H0_derived_km_s_Mpc','TT_first_three_peak_ell','density_relative_error','friedmann_relative_error')}),flush=True)
    # Convergence is tested where the geometry changed most, not inferred
    # from unrelated earlier precision controls.
    case='weighted_correlated'
    load=np.array(next(x for x in rows if x['id']==case)['load_P_D_R'])
    high,_,dl_high=calculate(case,load,thermal,accuracy=2.,save=False)
    diffs=[]
    for spec,col,rel in [('TT',0,'3.01'),('TE',3,'3.02'),('EE',1,'3.02')]:
        data=np.loadtxt(INPUT/f'COM_PowerSpect_CMB-{spec}-binned_R{rel}.txt')
        diffs.extend(np.interp(data[:,0],np.arange(len(dl_high)),dl_high[:,col]-spectra[case][:,col])/((data[:,2]+data[:,3])/2))
    conv=float(np.sqrt(np.mean(np.array(diffs)**2)))
    checks['changed_geometry_accuracy_convergence']=conv<0.03
    try:require_microscopic_bridge({})
    except ValueError:checks['incomplete_microscopic_route_refused']=True
    else:checks['incomplete_microscopic_route_refused']=False
    checks['baryon_density_BBN_common_across_states']=np.ptp([x['BBN']['ombh2'] for x in rows])<1e-14
    checks['no_fit_or_rejection_claim']=all(x['statistical_rejection'] is None and x['official_minus2logL'] is None for x in rows)
    checks={k:bool(v) for k,v in checks.items()}
    result={'scope':'executed conditional toy-model observables; microscopic-only route remains open',
            'input':{'address_count':1015000,'slot_count':128,'eta_J_m3':ETA.tolist(),
                     'external_inputs':FIXED,'thermal_omega_at_h1':thermal,'critical_energy_at_h1_J_m3':U100},
            'WRRA_transform':'existing address/slot load -> Tr(Sigma_s A_s) -> eta_s L_s a^(nu_s-3) -> fixed standard completion',
            'completion':{'P':'baryons with standard photon coupling/recombination',
                          'D':'adopted cold perfect fluid: w=0, rest-frame cs2=0, anisotropic stress=0',
                          'R':'constant vacuum, w=-1, no independent vacuum perturbation',
                          'thermal':'photons, massless and massive neutrinos added separately; no double-counted allocation',
                          'geometry':'spatially flat standard GR; H0 from ledger and fixed thermal density',
                          'initial':'standard adiabatic power law, As/ns inherited, not derived from P6 covariance'},
            'microscopic_only':{'status':'missing physical closure','missing':MICRO_MISSING},
            'selection':'not derived; no single-outcome assumption used for ensemble observables',
            'shutter':'existing SI fold spectrum and readout times recorded in inputs; no unsupported identification with cosmic energy/primordial power',
            'new_cosmological_fit':False,'cases':rows,'checks':checks,'checks_passed':sum(checks.values()),
            'accuracy_test':{'case':case,'boost_pair':[1.5,2.0],'RMS_change_in_public_bin_sigma':conv,'diagnostic_tolerance':0.03},
            'official_Planck':{'status':'not evaluated','backend_available':{k:importlib.util.find_spec(k) is not None for k in ('clik','clipy')},
                              'missing':'verified official likelihood data blocks, foreground/calibration settings and null calibration'},
            'refutation_conditions':['negative load or energy','same density budget gives inconsistent Friedmann/CAMB background',
                                    'nonconvergent observable computation','specified fixed completion inconsistent with data under appropriate likelihood'],
            'data_note':'public binned diagnostic uses diagonal errors and bin-centre sampling; Q is not official chi-square or -2lnL; BAO predictions not yet scored against a covariance dataset; BBN table results not a micro-derived nuclear history',
            'provenance':{'CAMB':camb.__version__, 'binary_sha256':hash_file(Path(camb.__file__).parent/'camblib.so'),
                          'BBN_table_sha256':hash_file(Path(camb.__file__).parent/'PRIMAT_Yp_DH_ErrorMC_2024.dat'),
                          'input_sha256':{p.name:hash_file(p) for p in INPUT.iterdir() if p.is_file()}}}
    (OUT/'ledger.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    make_plot(spectra)
    if not all(checks.values()):raise AssertionError({k:v for k,v in checks.items() if not v})
    print('Checks '+str(sum(checks.values()))+'/'+str(len(checks)),flush=True)
    print('Accuracy RMS '+str(conv),flush=True)

if __name__=='__main__':main()
