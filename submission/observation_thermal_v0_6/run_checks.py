from pathlib import Path
import json,math,hashlib
import numpy as np
from scipy.linalg import cho_solve
from lensing_likelihood import LensingLikelihood,spectra
from thermal_history import EOS,hubble,ME
P=Path(__file__).resolve().parent;checks={}
def check(name,condition):
    checks[name]=bool(condition)
    if not condition:raise AssertionError(name)

like=LensingLikelihood();obs=json.loads((P/'results/lensing_likelihood.json').read_text())
thermal=json.loads((P/'results/thermal.json').read_text())
check('covariance_positive_definite',np.linalg.eigvalsh(like.cov).min()>0)
check('covariance_symmetric',np.max(abs(like.cov-like.cov.T))<1e-25)
check('covariance_error_columns_consistent',obs['diagonal_error_consistency']<.001)
check('window_normalizations',np.max(abs(like.W.sum(axis=1)-1))<2e-6)
for m in obs['models']:
    check(m['name']+'_official_likelihood_crosscheck',m['official_reference_difference']<1e-10)
    check(m['name']+'_finite_nonnegative_chi2',np.isfinite(m['chi2']) and m['chi2']>=0)
check('numerical_refinement_below_observational_noise',obs['numerical_refinement_distance_sigma']<.01)
check('zero_lensing_control_rejected',obs['null_lensing']['chi2']>100)
pp,tt=spectra('nonlinear');r,b=like.evaluate(pp,tt)
# Normalization defect is explicitly rejected by its likelihood penalty.
bad,_=like.evaluate(pp*2*np.pi,tt)
check('wrong_phiphi_normalization_rejected',bad['chi2']>r['chi2']+100)
check('profile_not_worse_than_fixed',r['chi2']>=like.amplitude_profile(pp,tt)['chi2_profile'])
delta=(like.W+like.Rpp)@pp[:3001]+like.Rtt@tt[:3001]-like.fid-like.d
check('Cholesky_vs_dense_solve',abs(r['chi2']-delta@np.linalg.solve(like.cov,delta))<1e-11)
try:like.evaluate(np.ones(20),tt);invalid=False
except ValueError:invalid=True
check('incomplete_spectrum_rejected',invalid)
linear=np.load(P/'results/linear.npz');nonlin=np.load(P/'results/nonlinear.npz')
check('nonlinear_lensing_actually_changes_spectrum',np.max(abs(nonlin['clpp'][50:2001]/linear['clpp'][50:2001]-1))>.01)
check('lensing_BB_generated',nonlin['lensed'][1000,2]>0 and np.all(nonlin['unlensed'][:,2]==0))

eos=EOS();check('relativistic_electron_entropy_limit',abs(eos.gs(1000)-5.5)<2e-6)
check('annihilated_electron_entropy_limit',abs(eos.gs(.005)-2)<1e-10)
for T in [.005,.02,.1,.5,1.,5.,30.]:
    re,pe,der=eos(T);exact=eos.exact(T)
    check(f'EOS_positive_{T}',re>0 and pe>0 and der>0)
    check(f'EOS_quadrature_table_{T}',np.max(abs(np.array([re,pe,der])/exact-1))<2e-7)
    h=1e-5;rp=eos.exact(T*(1+h))[0];rm=eos.exact(T*(1-h))[0]
    check(f'EOS_independent_heat_capacity_{T}',abs((rp-rm)/(2*h*T)/der-1)<2e-6)
check('thermal_energy_plus_work',thermal['max_energy_work_residual']<2e-9)
check('thermal_event_energy_finite_precision',thermal['max_event_balance_relative']<2e-6)
check('thermal_event_entropy_positive',thermal['record_entropy_gain']>0)
check('thermal_zero_cost_no_record_entropy',thermal['zero_cost_comparison']['record_entropy_gain']==0.)
check('thermal_time_and_table_refinement',max(thermal['refinement'].values())<2e-8)
check('MeV_milestones_computed',len(thermal['milestones'])==4)
check('positive_thermal_times',all(x['time_from_start_s']>0 for x in thermal['milestones']))
check('old_scale_requires_recalibration',abs(thermal['a_initial_derived']/1e-10-1)>.01)

# A positive foreground/adiabatic completion test cannot masquerade as a test of
# the complete earlier transition state. Preserve all 64 matched states as input.
states=json.loads((P/'inputs/matching_states.json').read_text())
fullstate=dict(modes=len(states),full_state_injected=False,
    nonzero_matter_velocity_modes=sum(x['matched_state']['theta_m_Mpc_inverse']!=0 for x in states),
    neutrino_multipoles_per_mode=len(states[-1]['matched_state']['F_nu']),
    selected_CAMB_initial_condition='initial_adiabatic',
    required_for_complete_injection=['gauge transformation into CAMB variables including CDM frame',
        'baryon/photon tight-coupling and massive-neutrino state completion',
        'consistent thermal background/scale mapping',
        'event-time and finite-gradient conserved jump conditions',
        'angular/statistical completion of the finite spatial seed'],
    gate='BLOCKED: no claim of full-state integration is permitted by these runs')
check('matched_state_all_64_retained',len(states)==64)
check('nonzero_velocity_state_cannot_be_silently_discarded',fullstate['nonzero_matter_velocity_modes']==64)
check('full_state_label_fail_closed',all(not x['full_v04_state_injected'] and not x['finite_v05_events_injected'] for x in json.loads((P/'results/camb_runs.json').read_text())))
(P/'results/full_state_gate.json').write_text(json.dumps(fullstate,indent=2)+'\n')
result=dict(version='0.6',checks_passed=sum(checks.values()),checks=checks,
    verified_inputs='NASA SPT-Planck released bandpowers/covariance/windows/corrections; inherited WRRA background and clock; constants/EOS inputs declared.',
    transformation='Conditional WRRA-background CAMB/HMCode spectra, native Gaussian likelihood; separate finite-packet massive-electron thermal completion.',
    output='Executed conditional observational likelihood and MeV elapsed chronology, with an explicit blocked full-state gate.',
    falsification='Covariance/normalization errors, failed official-code crosscheck, failed refinement or conservation, and mislabeled full-state injection are rejected.',
    scope='Step 3 statistical and thermal modules executed. Complete WRRA perturbation/event integration and joint cosmological posterior are not completed.')
(P/'results/audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('checks passed:',result['checks_passed'])
