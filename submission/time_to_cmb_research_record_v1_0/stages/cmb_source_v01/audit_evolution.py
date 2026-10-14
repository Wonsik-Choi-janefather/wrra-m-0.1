from pathlib import Path
import json,csv
import numpy as np
from scipy.interpolate import CubicSpline
import camb
from calculate import params,record,ROOT,OUT

def audit(branch,force=1):
    p=params(branch,'R',2.5,force)
    r=camb.get_background(p)
    tau=np.geomspace(.1,r.conformal_time(0),6000)
    k=.05*np.arange(1,8)
    names=['a','H','delta_cdm','delta_baryon','source_delta_R','source_v_D','source_z',
        'source_d_delta_D','source_d_v_D','source_d_eta']
    vals=r.get_time_evolution(k,tau,names,lAccuracyBoost=3)
    a,H,dc,db,dR,v,z,dd,dv,deta=np.moveaxis(vals,-1,0)
    u=np.array(record(branch)['u_P_D_R_today_J_m3'])
    force_term=k[:,None]*u[2]/u[1]*a**3*dR
    residual=dv+H*v+force_term
    norm=np.maximum(np.abs(dv)+np.abs(H*v)+np.abs(force_term),1e-40)
    gate=a>.02
    differential=float(np.max(np.abs(residual[gate])/norm[gate]))
    # Integrating factor yields an independent integral test of momentum conservation.
    # (a v)'=-k rho_R0/rho_D0 a^4 delta_R.
    from scipy.integrate import cumulative_simpson
    integ=cumulative_simpson(-k[:,None]*u[2]/u[1]*a**4*dR,x=tau,axis=1,initial=0)
    momentum=a*v-a[:,0,None]*v[:,0,None]
    integral_error=float(np.max(abs(momentum[:,50:]-integ[:,50:]))/np.max(abs(integ[:,50:])))
    dcalc=CubicSpline(tau,dc,axis=1).derivative()(tau)
    difference=float(np.max(abs(dcalc[:,50:-50]-dd[:,50:-50]))/np.max(abs(dd[:,50:-50])))
    result=dict(branch=branch,force_multiplier=force,vacuum_contrast_drift=float(np.max(abs(dR-1))),
        dark_total_momentum_relative_residual=differential,
        independent_integrating_factor_relative_error=integral_error,
        density_spline_derivative_relative_error=difference)
    if force==1:
        # Obtain a separate dust-basis result.
        q=camb.get_background(params(branch,'D',2.5))
        rd=q.get_time_evolution(k,tau,['delta_cdm','delta_baryon'],lAccuracyBoost=3)
        rows=[x for x in csv.DictReader((ROOT/'inputs/SOURCE_harmonic_GR_controls.csv').open()) if x['branch']==branch]
        upper_D=np.zeros(len(tau));upper_B=np.zeros(len(tau))
        for x in rows:
            n=int(x['mode'])-1;sd=float(x['delta_u_D_at_a1_J_m3'])/u[1];sr=float(x['delta_u_R_J_m3'])/u[2]
            upper_D+=abs(sd*rd[n,:,0]+sr*dc[n]);upper_B+=abs(sd*rd[n,:,1]+sr*db[n])
        result['max_all_components_triangle_bound_delta_D']=float(upper_D.max())
        result['max_all_components_triangle_bound_delta_baryon']=float(upper_B.max())
        result['linear_gate_0_1_pass']=bool(max(upper_D.max(),upper_B.max())<.1)
        np.savez_compressed(OUT/f'{branch}_evolution_audit.npz',tau=tau,k=k,variables=names,values=vals,
            delta_D_triangle_bound=upper_D,delta_baryon_triangle_bound=upper_B)
    print(json.dumps(result),flush=True)
    return result

if __name__=='__main__':
    results=[audit('weighted'),audit('unweighted'),audit('weighted',0)]
    (OUT/'evolution_audit.json').write_text(json.dumps(results,indent=2))
