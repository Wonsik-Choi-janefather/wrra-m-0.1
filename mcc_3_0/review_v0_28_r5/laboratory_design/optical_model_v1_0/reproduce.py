#!/usr/bin/env python3
"""Fixed static finite-SOURCE optical phase model, version 1.0.
Rules are adopted constitutive choices; this is not observational confirmation.
"""
from pathlib import Path
import csv, hashlib, json, math, runpy
import numpy as np
from scipy.optimize import brentq, minimize_scalar
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)

def main():
    cfg=json.loads((ROOT/'inputs/frozen_model.json').read_text())
    assert cfg['version']=='1.0' and cfg['coupling_g']==1
    for name,digest in cfg['input_sha256'].items():
        assert hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()==digest,name
    # Retain and reproduce the original rejected/alternative policy controls.
    runpy.run_path(str(ROOT/'audit_v0_1/reproduce.py'))['main']()
    prior=json.loads((ROOT/'audit_v0_1/results/results.json').read_text())
    a=np.load(ROOT/'inputs/finite_preparation.npz')
    raw=a['dimensionless_fluctuation'][1];f=raw-raw.mean();J=len(f)
    clock=json.loads((ROOT/'inputs/clock.json').read_text())
    hb=clock['h_J_s']/(2*math.pi)
    dt=clock['epsilon']*hb/clock['e_J_per_eV']/clock['mode_energy_eV']
    ell=clock['c_m_s']*dt;rms=float(np.std(f))
    g=cfg['coupling_g']
    shape=prior['outputs']['static_curve_shape']
    rows=[]
    for wavelength in cfg['wavelengths_m']:
        v=lambda L: float(abs(np.mean(np.exp(1j*g*2*math.pi/wavelength*L*f))))
        scale=wavelength/(2*math.pi*abs(g)*rms)
        threshold=brentq(lambda L:v(L)-cfg['visibility_threshold'],0,scale*1.2)
        minimum_L=shape['first_minimum_beta']*scale
        revival_L=shape['first_revival_beta']*scale
        rows.append(dict(wavelength_nm=wavelength*1e9,
            first_visibility_threshold_m=threshold,
            first_minimum_exposure_m=minimum_L,first_minimum_visibility=v(minimum_L),
            first_revival_exposure_m=revival_L,first_revival_visibility=v(revival_L),
            revival_to_minimum_exposure_ratio=revival_L/minimum_L))
    with (OUT/'fixed_predictions.csv').open('w',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

    # Build the actual finite 128 x 2 Hamiltonian witness for one photon band.
    # Path B is the reference; FREE energy is path degenerate. Source energy
    # diagonal in J commutes for any declared volume; no volume is inferred here.
    wave=1064e-9;L=10.;E=clock['h_J_s']*clock['c_m_s']/wave
    I=np.eye(J*2)
    free=E*I
    interaction=np.diag(np.ravel(np.column_stack([-g*E*f,np.zeros(J)])))
    generator=interaction*L/clock['c_m_s']/hb
    phases=np.exp(-1j*np.diag(generator)).reshape(J,2)
    pure=phases/math.sqrt(2)
    reduced=pure.T@pure.conj()/J
    expected=abs(np.mean(np.exp(1j*g*2*math.pi/wave*L*f)))
    # On/off switching has conditional work, despite zero ensemble-mean work.
    # No erasure or degenerate-source energy generation is inferred from that.
    work_on=-g*E*f/2
    work_off=g*E*f/2
    readout_v=float(2*abs(reduced[0,1]))
    checks={
        'frozen_input_hashes':True,
        'fixed_register_dimension':J==cfg['phase_register_dimension'],
        'positive_interacting_photon_energy':float(np.diag(free+interaction).min())>0,
        'interaction_commutes_with_free_energy':float(np.max(abs(free@interaction-interaction@free)))<1e-60,
        'Hamiltonian_matches_phase_gate':abs(readout_v-expected)<1e-13,
        'switch_on_off_work_balance':float(np.max(abs(work_on+work_off)))<1e-40,
        'single_label_visibility_is_one':bool(np.max(abs(abs(phases[:,0]*phases[:,1].conj())-1))<1e-14),
        'subdivision_preserves_fixed_physical_shutter':prior['checks']['same_physical_state_subdivision'],
        'threshold_monotonic_wavelength_scaling':abs(rows[1]['first_visibility_threshold_m']/rows[0]['first_visibility_threshold_m']-2)<1e-10,
        'curve_shape_is_wavelength_invariant':max(abs(r['first_minimum_visibility']-rows[0]['first_minimum_visibility']) for r in rows)<1e-13,
        'prior_17_controls':all(prior['checks'].values()),
    }
    checks={key:bool(value) for key,value in checks.items()}
    assert all(checks.values()),checks
    work_table=[dict(label=j,relative_dark_mean_stress=float(f[j]),
        interaction_energy_path_A_J=float(-g*E*f[j]),
        interaction_energy_path_B_J=0.,switch_on_expected_work_J=float(work_on[j]),
        switch_off_expected_work_J=float(work_off[j]),balanced_cycle_work_J=float(work_on[j]+work_off[j])) for j in range(J)]
    with (OUT/'interaction_and_switching_ledger.csv').open('w',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=list(work_table[0]));w.writeheader();w.writerows(work_table)
    results=dict(version='1.0',status=cfg['status'],date=cfg['date'],authors=cfg['authors'],
        validation_inputs=dict(shutter_dt_s=dt,light_step_pm=ell*1e12,phase_states=J,
            SOURCE_relative_dark_mean_stress_RMS=rms,no_new_observational_fit=True),
        WRRA_transformation=dict(frozen_memory_law=cfg['memory_law'],frozen_g=g,
            interaction_Hamiltonian=cfg['Hamiltonian'],
            exact_visibility='abs(mean_J exp(i 2*pi*g*L*f_D(J)/lambda))',
            count='One register per independently prepared realization; zero per-shutter resets',
            g_and_memory_status='Explicitly adopted and now fixed constitutive rules, not a unique derivation',
            statistical_scope='Nonselective ensemble visibility. Conditioning on a single retained label restores full visibility.'),
        outputs=dict(fixed_predictions=rows,curve_shape=shape,
            unperturbed_common_carrier_visibility=1.,
            photon_free_energy_J=E,Hamiltonian_visibility_1064nm_10m=readout_v,
            switching_work_RMS_per_edge_J=float(np.sqrt(np.mean(work_on**2))),
            switching_work_mean_per_edge_J=float(work_on.mean()),
            switching_work_counted_per_conditional_label=True,
            initial_register_entropy_nats=math.log(J),
            leading_static_visibility_independent_of_shutter_spacing=True),
        refutation_conditions=[
            'Measured nonselective visibility under the specified preparation/differential coupling contradicts the fixed curve.',
            'Wavelength scaling, minimum/revival visibility or exposure ratio contradicts fixed predictions.',
            'Free-energy, SOURCE-label conservation or preparation/switching accounting fails.',
            'A numerical-subdivision artifact is mistaken for physical-shutter noise.'],
        conclusion='Fixed finite-SOURCE coherence prediction model 1.0. Optical interaction and static memory are constitutive model choices; observational validation and Maxwell/locality completion remain separate.',
        scope_notes=[
            'The leading static phase is N*ell*f_D = L*f_D: shutter spacing cancels. This does not independently measure a fundamental spatial tick.',
            'Differential SOURCE phase coupling must be present. Bare vacuum propagation and identical common-mode arms preserve visibility.',
            'A static unknown label does not cause within-label irreversible collapse; the curve is a nonselective ensemble statistic.',
            'This witness executes a finite Hamiltonian and switching ledger; it does not derive a universal optical interaction from cosmological mean stress.'],
        checks=checks,prior_checks=prior['checks'])
    (OUT/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(version=results['version'],predictions=rows,new_controls=len(checks),
        prior_controls=len(prior['checks']),all_passed=all(checks.values()),
        work_RMS_J=results['outputs']['switching_work_RMS_per_edge_J']),indent=2))

if __name__=='__main__':main()
