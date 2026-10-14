"""Compare the prepared entropy/regular velocity with actual CAMB initial callbacks."""
import json,numpy as np,camb
from preparation import params,CASE,OUT

def main():
    r=camb.get_background(params('R'));p=r.Params
    nu=sum(r.grhormass[:p.nu_mass_eigenstates])+r.grhornomass
    om=(r.grhob+r.grhoc)/np.sqrt(3*(r.grhog+nu));Rc=p.omch2/(p.omch2+p.ombh2)
    dr=camb.get_background(params('D'));rows=[]
    for n in range(1,8):
        k=.05*n;tau=min(.001/k,.1);a=r.adotrad*tau*(1+om*tau/4);o=om*tau;x=k*tau
        expected_gamma=Rc*o*(-2/3+o/4);expected_D=1+.75*expected_gamma
        yy=dr.get_time_evolution(k,[tau],['delta_cdm','delta_photon','source_v_D'])[0]
        yr=r.get_time_evolution(k,[tau],['source_delta_R','source_v_D'])[0]
        expected_v=-k*r.grhov/r.grhoc*a**3*tau/5
        rows.append(dict(mode=n,tau_Mpc=tau,D_density_relative_error=float(abs(yy[0]/expected_D-1)),
            photon_density_relative_error=float(abs(yy[1]/expected_gamma-1)),
            entropy_identity_error_native_float_output=float(abs(yy[0]-.75*yy[1]-1)),
            vacuum_contrast_error=float(abs(yr[0]-1)),
            regular_velocity_relative_error=float(abs(yr[1]/expected_v-1))))
    result=dict(rows=rows,precision_note='Named density transfer outputs use native float32; extra SOURCE fields are double precision.',
        max_dark_density_relative_error=max(x['D_density_relative_error'] for x in rows),
        max_photon_density_relative_error=max(x['photon_density_relative_error'] for x in rows),
        max_density_relative_error=max(max(x['D_density_relative_error'],x['photon_density_relative_error']) for x in rows),
        max_velocity_relative_error=max(x['regular_velocity_relative_error'] for x in rows),
        passed=bool(max(max(x['D_density_relative_error'],x['photon_density_relative_error']) for x in rows)<2e-7 and max(x['regular_velocity_relative_error'] for x in rows)<1e-12))
    (OUT/'initial_callback_check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
