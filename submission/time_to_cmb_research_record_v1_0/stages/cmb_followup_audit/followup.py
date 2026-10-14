"""SI unit audit, per-harmonic diagnostics and fixed-ledger counterfactuals."""
from pathlib import Path
import csv,json,sys
import numpy as np
import camb
from camb import constants as c
from scipy.linalg import solve_triangular
from calculate import params,record,ROOT,OUT
from plik_lite import NativePlikLite
PRIOR=ROOT/'prior/results'
U100=3*(100000/c.Mpc)**2*c.c**2/(8*np.pi*c.G)
G_FACTOR=8*np.pi*c.G*c.Mpc**2/c.c**4

def unit_audit():
    records=[]
    for branch in ['weighted','unweighted']:
        r=camb.get_background(params(branch,'R',2.5));u=np.array(record(branch)['u_P_D_R_today_J_m3'])
        a=np.geomspace(1e-8,1,240)
        bg=r.get_background_densities(a,vars=['baryon','cdm','de'])
        expected=np.c_[u[0]*a,u[1]*a,u[2]*a**4]*G_FACTOR
        actual=np.c_[bg['baryon'],bg['cdm'],bg['de']]
        coeff_error=float(np.max(abs(actual/expected-1)))
        # Background output is a^4-weighted; evolution stress uses a^2-weighting.
        vacuum_stress=u[2]*G_FACTOR*a*a
        dark_momentum_coefficient=u[1]*G_FACTOR/a
        stress_error=float(np.max(abs(vacuum_stress/(r.grhov*a*a)-1)))
        momentum_error=float(np.max(abs(dark_momentum_coefficient/(r.grhoc/a)-1)))
        # Force uses the ratio of a^2-weighted vacuum and dust coefficients.
        force_ratio=u[2]/u[1]*a**3
        force_error=float(np.max(abs(force_ratio/((r.grhov*a*a)/(r.grhoc/a))-1)))
        rows=[x for x in csv.DictReader((ROOT/'inputs/SOURCE_harmonic_GR_controls.csv').open()) if x['branch']==branch]
        amplitudes=[dict(mode=int(x['mode']),component=x['component'],
            S_D=float(x['delta_u_D_at_a1_J_m3'])/u[1],delta_R=float(x['delta_u_R_J_m3'])/u[2]) for x in rows]
        records.append(dict(branch=branch,background_SI_conversion_max_relative_error=coeff_error,
            vacuum_stress_coefficient_error=stress_error,dark_momentum_coefficient_error=momentum_error,
            force_ratio_error=force_error,amplitudes=amplitudes,
            passed=max(coeff_error,stress_error,momentum_error,force_error)<2e-8))
    return dict(constants=dict(c_m_s=c.c,G_SI=c.G,Mpc_m=c.Mpc,U100_J_m3=U100,
        SI_to_Mpc_squared_stress_coefficient=G_FACTOR),records=records,
        convention='u is energy density J/m^3; k is Mpc^-1; conformal time is Mpc. Density output is 8piG*a^4*u*Mpc^2/c^4; stress uses a^2. S_D and delta_R are dimensionless. Temperature power conversion is (T_CMB*1e6)^2, not an extra power of c.')

def per_mode_evolution():
    results=[]
    for branch in ['weighted','unweighted']:
        r=camb.get_background(params(branch,'D',2.5))
        saved=np.load(PRIOR/f'{branch}_evolution_audit.npz')
        tau=saved['tau'];k=saved['k'];vR=saved['values']
        names=saved['variables'].tolist()
        vD=r.get_time_evolution(k,tau,names,lAccuracyBoost=3)
        u=np.array(record(branch)['u_P_D_R_today_J_m3'])
        amplitudes=[x for x in csv.DictReader((ROOT/'inputs/SOURCE_harmonic_GR_controls.csv').open()) if x['branch']==branch]
        snapshots=[]; summaries=[]
        for x in amplitudes:
            n=int(x['mode'])-1;sd=float(x['delta_u_D_at_a1_J_m3'])/u[1];sr=float(x['delta_u_R_J_m3'])/u[2]
            a,H=vR[n,:,0],vR[n,:,1]
            y=sd*vD[n]+sr*vR[n]
            delta_D=y[:,2];delta_B=y[:,3];deltaR=y[:,4];vel=y[:,5];delta_dot=y[:,7]
            force=k[n]*u[2]/u[1]*a**3*deltaR
            res=y[:,8]+H*vel+force
            denom=np.maximum(abs(y[:,8])+abs(H*vel)+abs(force),1e-40)
            mask=a>.02
            gate=abs(delta_D)>max(np.max(abs(delta_D))*1e-6,1e-30)
            # Zero crossing makes a logarithmic growth rate undefined, not a runaway.
            growth=np.full(len(a),np.nan)
            growth[gate]=delta_dot[gate]/(H[gate]*delta_D[gate])
            summaries.append(dict(mode=n+1,component=x['component'],k_Mpc_inv=float(k[n]),
                max_abs_delta_D=float(abs(delta_D).max()),max_abs_delta_baryon=float(abs(delta_B).max()),
                max_abs_velocity_D=float(abs(vel).max()),momentum_relative_residual=float(np.max(abs(res[mask])/denom[mask])),
                unguarded_growth_points=int((~gate).sum()),state_finite=bool(np.isfinite(y).all()),
                late_vacuum_contrast_drift=float(abs(deltaR-sr).max()),
                growth_definition='d ln|delta_D|/d ln a; guarded around density zero crossing'))
            for i in np.linspace(0,len(a)-1,100).astype(int):
                snapshots.append([branch,n+1,x['component'],k[n],tau[i],a[i],delta_D[i],delta_B[i],vel[i],deltaR[i],
                    growth[i] if gate[i] else 'OPEN',float(res[i]/denom[i])])
        with (OUT/f'{branch}_seven_mode_evolution.csv').open('w') as f:
            w=csv.writer(f);w.writerow(['branch','mode','component','k_Mpc_inv','tau_Mpc','a','delta_D','delta_baryon','v_D','delta_R','growth_D_or_OPEN','momentum_relative_residual']);w.writerows(snapshots)
        results.append(dict(branch=branch,modes=summaries))
        np.savez_compressed(OUT/f'{branch}_D_basis_evolution.npz',tau=tau,k=k,variables=names,values=vD)
    return results

def spectrum_scaling():
    one=np.load(PRIOR/'weighted_R_a2.5_f1.npz')
    results=[]
    for amp in [.01,2]:
        p=params('weighted','R',2.5);p.DarkEnergy.delta_R_initial=amp
        r=camb.get_transfer_functions(p);t=r.get_cmb_transfer_data();ell=t.L.astype(float)
        T=t.delta_p_l_k[0]/amp
        E=t.delta_p_l_k[1]*np.sqrt((ell-1)*ell*(ell+1)*(ell+2))[:,None]/amp
        checks={key:float(np.max(abs(value-one[key]))/np.max(abs(one[key]))) for key,value in [('T',T),('E',E)]}
        np.savez_compressed(OUT/f'R_scaled_{amp:g}.npz',ell=t.L,k=t.q,normalized_T=T,normalized_E=E)
        results.append(dict(delta_R_basis_input=amp,normalized_transfer_relative_difference=checks,
            passed=max(checks.values())<.002))
    # Solve a mixed D/R vector directly, rather than combining two output arrays.
    x=next(x for x in csv.DictReader((ROOT/'inputs/SOURCE_harmonic_GR_controls.csv').open()) if x['branch']=='weighted' and x['mode']=='1' and x['component']=='cosine')
    u=np.array(record('weighted')['u_P_D_R_today_J_m3']);sd=float(x['delta_u_D_at_a1_J_m3'])/u[1];sr=float(x['delta_u_R_J_m3'])/u[2]
    norm=np.hypot(sd,sr);p=params('weighted','R',2.5);p.DarkEnergy.delta_R_initial=sr/norm;p.InitialConditionVector=[0,sd/norm,0,0,0]
    r=camb.get_transfer_functions(p);t=r.get_cmb_transfer_data();ell=t.L.astype(float)
    d=np.load(PRIOR/'weighted_D_a2.5_f1.npz')
    expectedT=sd*d['T'][:,0]+sr*one['T'][:,0];expectedE=sd*d['E'][:,0]+sr*one['E'][:,0]
    actualT=t.delta_p_l_k[0,:,0]*norm;actualE=t.delta_p_l_k[1,:,0]*np.sqrt((ell-1)*ell*(ell+1)*(ell+2))*norm
    error={k:float(np.max(abs(a-b))/np.max(abs(b))) for k,a,b in [('T',actualT,expectedT),('E',actualE,expectedE)]}
    results.append(dict(case='direct mixed D/R first cosine harmonic',relative_difference=error,passed=max(error.values())<.002))
    return results

def conditional_blocks(like,dl):
    residual=like.data-like.bins(dl)
    L=np.tril(like.chol[0]);w=solve_triangular(L,residual,lower=True)
    result={};start=0
    for name,n in [('TT',215),('TE_given_TT',199),('EE_given_TT_TE',199)]:
        result[name]=float(np.sum(w[start:start+n]**2));start+=n
    assert abs(sum(result.values())-like.evaluate(dl)['chi2_highell'])<1e-7
    return result

def counterfactual(label,Dbranch,Rbranch):
    non=record('unweighted');dark=record(Dbranch);vac=record(Rbranch)
    h2=(non['H0_derived_km_s_Mpc']/100)**2
    thermal=h2-non['ombh2']-non['omch2']-non['u_P_D_R_today_J_m3'][2]/U100
    wc=dark['omch2'];wv=vac['u_P_D_R_today_J_m3'][2]/U100
    H0=100*np.sqrt(non['ombh2']+wc+wv+thermal)
    p=params('unweighted','standard',2.5)
    p.set_cosmology(H0=H0,ombh2=non['ombh2'],omch2=wc,omk=0,mnu=.06,nnu=3.044,tau=.0544,
        TCMB=2.7255,bbn_predictor='PRIMAT_Yp_DH_ErrorMC_2024.dat')
    r=camb.get_results(p);dl=r.get_total_cls(lmax=2508,CMB_unit='muK')
    np.savez_compressed(OUT/(label+'.npz'),ell=np.arange(len(dl)),Dl=dl)
    like=NativePlikLite()
    result=dict(label=label,D_ledger=Dbranch,R_ledger=Rbranch,derived_H0=H0,ombh2=non['ombh2'],omch2=wc,
        chi2_highell=like.evaluate(dl)['chi2_highell'],conditional_blocks=conditional_blocks(like,dl),
        diagnosis_only=True,new_fit=False,standalone_WRRA_branch_derived=False)
    print(json.dumps(result),flush=True);return result

def main():
    OUT.mkdir(exist_ok=True)
    if len(sys.argv)>1 and sys.argv[1]=='mixed':
        result=counterfactual(sys.argv[2],sys.argv[3],sys.argv[4]);(OUT/(sys.argv[2]+'.json')).write_text(json.dumps(result,indent=2));return
    units=unit_audit();modes=per_mode_evolution();scaling=spectrum_scaling()
    like=NativePlikLite();baselines=[]
    for branch in ['weighted','unweighted']:
        dl=np.load(PRIOR/f'{branch}_standard_a2.5_f1.npz')['Dl']
        baselines.append(dict(branch=branch,chi2=like.evaluate(dl)['chi2_highell'],conditional_blocks=conditional_blocks(like,dl)))
    result=dict(date='2026-10-14',units=units,per_mode_evolution=modes,scaling=scaling,original_baselines=baselines,
        initial_universe_condition_already_included=True,SOURCE_lensing_included=False,
        gauge_scope='Bounded trajectories and conserved momentum in the declared geodesic synchronous gauge. Not a completed second-gauge implementation or a proof of full gauge equivalence.')
    (OUT/'followup_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(units=units['records'],scaling=scaling,baselines=baselines)),flush=True)

if __name__=='__main__':main()
