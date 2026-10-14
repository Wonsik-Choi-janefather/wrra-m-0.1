"""Stable observables, excluding wall time and archive metadata."""
from pathlib import Path
import json,math
def collect(root):
    root=Path(root);out={}
    s=json.loads((root/'supply_results.json').read_text())
    out['supply']=[{k:r[k] for k in ['sector','refresh_probability','one_frame_relative_RMS','target_mean_profile_relative_RMS','averaging_time_s','averaged_intrinsic_relative_RMS']} for r in s['outputs']['averaging_boundaries']]
    p=json.loads((root/'photon_results.json').read_text())
    out['photon_delay_RMS_1m']=p['outputs']['fixed_SOURCE_delay_RMS_at_1m_s']
    out['photon_alias_energy_eV']=p['outputs']['phase_alias_energy_eV']
    out['pulses']=[{k:r[k] for k in ['energy_eV','exposure_m','original_pulse_time_RMS_s','SOURCE_group_delay_RMS_s','nonselective_pulse_time_RMS_s','arrival_distribution_skewness','arrival_distribution_excess_kurtosis']} for r in p['outputs']['pulse_predictions']]
    c=json.loads((root/'CMB_higher_results.json').read_text())
    keys=['field','lmax','SOURCE_RMS','SOURCE_third_moment','SOURCE_connected_fourth_moment','SOURCE_skewness','SOURCE_excess_kurtosis','Gaussian_baseline_plus_SOURCE_skewness','Gaussian_baseline_plus_SOURCE_excess_kurtosis']
    out['sky']=[{k:r[k] for k in keys} for r in c['outputs']['bandlimited_sky_cumulants']]
    out['SOURCE_deflection_arcsec']=c['outputs']['SOURCE_deflection_RMS_arcsec'];out['equilateral_T_peak']=c['outputs']['equilateral_T_peak']
    return out
def compare(actual,expected,path='root'):
    if isinstance(expected,dict):
        for key,value in expected.items():compare(actual[key],value,path+'/'+key)
    elif isinstance(expected,list):
        assert len(actual)==len(expected),path
        for i,(a,b) in enumerate(zip(actual,expected)):compare(a,b,path+'/'+str(i))
    elif isinstance(expected,(int,float)) and not isinstance(expected,bool):
        assert math.isfinite(float(actual)) and math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-60),(path,actual,expected)
    else:assert actual==expected,(path,actual,expected)
