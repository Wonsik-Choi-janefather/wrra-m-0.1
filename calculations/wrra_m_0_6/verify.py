"""Independent release checks, including degenerate physical inputs."""
import json
import math
import tempfile
from pathlib import Path
import numpy as np
import compute as m

ROOT=Path(__file__).resolve().parent

def main():
    p=json.loads((ROOT/'parameters.json').read_text())
    b=json.loads((ROOT/'baseline_0_5/parameters.json').read_text())
    result=json.loads((ROOT/'results/results.json').read_text())
    old=json.loads((ROOT/'baseline_0_5/results.json').read_text())
    local=result['reference_background']['present_local_output']
    old_sphere=next(x for x in old['sphere'] if x['r_kpc']==p['test_radius_kpc'])
    old_lens=next(x for x in old['finite_patch_lensing'] if x['impact_kpc']==p['lens_impact_kpc'])
    assert local['aT_m_s2']==old['cosmic_calibration']['aT_m_s2']
    assert local['v_total_km_s']==old_sphere['v_total_km_s']
    assert math.isclose(local['finite_patch_lensing']['alpha_patch_rad'],old_lens['alpha_patch_rad'],rel_tol=1e-14)
    assert result['carrier']['filter_gap_left']==old['carrier']['filter_gap_left'] if 'filter_gap_left' in old['carrier'] else result['carrier']==old['carrier']
    assert result['operators']['N']==result['carrier']['lattice_N']==p['lattice_N']
    assert result['lattice_contract']['effective_transport_lattice_N']==p['lattice_N']
    carrier=m.Carrier(p['lattice_N'],p['noncommuting_test_strength'])
    psi=carrier.packet(p['noncommuting_test_initial_modes'],p['noncommuting_test_initial_weights'])
    rho=np.outer(psi,psi.conj());shift=np.roll(np.eye(carrier.N),7,axis=0)
    errors=[]
    for K in [carrier.Kc,carrier.Kb]:
        lhs=np.trace(rho@K)
        rhs=np.trace((shift@rho@shift.T)@(shift@K@shift.T))
        errors.append(float(abs(lhs-rhs)))
    assert max(errors)<1e-12
    assert np.linalg.eigvalsh(rho).min()>-1e-12
    c=m.calibration(b)
    # The zero-load limit at zero phenotype density must have no 0/0 ratio.
    cz=m.calibration(dict(b,fraction_phenotype=0.))
    z=m.snapshot(1.,0.,0.,p,cz);zl=m.local_readout(z,p,b,cz)
    assert z['H_over_H0']==0 and z['deceleration_q'] is None
    assert z['actual_hidden_fraction'] is None and zl['aT_m_s2']==0
    assert zl['finite_patch_lensing'] is None
    # E proportional a gives p=-u/3, independently of the preferred exponent.
    pp=dict(p,background_energy_exponent=1.)
    ss=m.snapshot(.7,2.,2.,pp,c)
    assert math.isclose(ss['pressure_over_ucrit'],-ss['density_background_over_ucrit']/3,rel_tol=1e-14)
    boundary_passes=[]
    for name,bb in [('zero_phenotype',dict(b,fraction_phenotype=0.)),
                    ('zero_background',dict(b,fraction_phenotype=1-b['fraction_twist_clustering']))]:
        with tempfile.TemporaryDirectory() as out:
            rr=m.run(p,bb,Path(out),verify=False)
        assert math.isfinite(rr['calibration']['eta_J_m3'])
        boundary_passes.append(name)
    for key,value in [('a_min',0.),('noncommuting_test_strength',-1.),('information_clock_over_H0',float('nan'))]:
        bad=dict(p);bad[key]=value
        try:m.validate(bad,b)
        except ValueError:pass
        else:raise AssertionError('invalid input accepted: '+key)
    # Exercise the reported 64/128 mismatch and the reverse mismatch end to end.
    # The baseline dict must remain unchanged while both active grids follow 0.6.
    grid_checks=[]
    for state_N,baseline_N in [(64,128),(128,64)]:
        pp=dict(p,lattice_N=state_N);bb=dict(b,internal_lattice_N=baseline_N)
        original_bb=bb.copy()
        with tempfile.TemporaryDirectory() as out:
            rr=m.run(pp,bb,Path(out),verify=False)
        assert bb==original_bb and rr['baseline_inputs']==original_bb
        assert rr['operators']['N']==rr['carrier']['lattice_N']==state_N
        assert rr['lattice_contract']['baseline_configured_internal_lattice_N']==baseline_N
        assert rr['lattice_contract']['effective_transport_lattice_N']==state_N
        reference=next(x for x in rr['reference_background']['rows'] if x['a']==1.)
        ll=rr['reference_background']['present_local_output']
        assert reference['deceleration_q']==next(x for x in result['reference_background']['rows'] if x['a']==1.)['deceleration_q']
        assert ll['v_total_km_s']==local['v_total_km_s']
        assert ll['finite_patch_lensing']['alpha_patch_rad']==local['finite_patch_lensing']['alpha_patch_rad']
        grid_checks.append({'state_lattice_N':state_N,'baseline_configured_N':baseline_N,
            'effective_transport_N':rr['carrier']['lattice_N'],'baseline_input_preserved':True,
            'uniform_reference_outputs_unchanged':True})
    report={'baseline_aT_rotation_and_lensing_reproduced':True,
            'symmetric_carrier_result_unchanged':True,
            'simultaneous_basis_change_load_max_error':max(errors),
            'zero_load_zero_phenotype_ratios_are_null':True,
            'energy_exponent_one_pressure_verified':True,
            'boundary_histories_passed':boundary_passes,
            'invalid_inputs_rejected':True,
            'shared_lattice_regressions':grid_checks}
    (ROOT/'results/release_checks.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
