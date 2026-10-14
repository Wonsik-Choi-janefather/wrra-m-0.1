"""Finite phase-controlled preparation, entropy covariance and regular initial dressing.
Mean-stress covariance and intrinsic supplier variance are deliberately distinct.
"""
from pathlib import Path
import json,runpy,csv
import numpy as np
import camb
from camb import constants as c
from scipy.integrate import quad
from calculate_reference import params as reference_params
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
J=json.loads((ROOT/'inputs/address_results.json').read_text())
CASE=next(x for x in J['cases'] if x['branch']=='dark_weight_only')
CFG=json.loads((ROOT/'inputs/source_frozen_inputs.json').read_text())

def params(kind,acc=2.5):
    p=reference_params('unweighted',kind,acc)
    p.set_cosmology(**CASE['background'],omk=0,mnu=.06,nnu=3.044,tau=.0544,TCMB=2.7255,
        bbn_predictor='PRIMAT_Yp_DH_ErrorMC_2024.dat')
    return p

def main():
    p=np.load(ROOT/'inputs/address_residue_supply_profiles.npz')['dark_weight_only_payload']
    eta=np.array(CFG['eta_J_m3']);mu=p.sum((1,2));u=eta*mu
    functions=runpy.run_path(str(ROOT/'inputs/original_positive_readout.py'))
    phase,K=functions['modular_positive_kernel'](128)
    eps=CFG['inherited_supply_epsilon'];gap=2*np.cos(np.pi/8);A8=1-np.cos(np.pi/8)
    mask=np.arange(30)%3!=0
    probability=.5+eps*(K-1)
    # A counted additional phase register J=128, distinct from the pure |k=8> source mode.
    # rho_phase=I/128. Supplier probabilities are conditional on this common phase.
    M=p[:,mask].sum((1,2));U=mu-M
    source=eta*np.array([mu[0],U[1]+A8*M[1],U[2]+A8*M[2]])
    supply=eta[:,None]*gap*(p[:,mask].sum(2)@probability[mask]);supply[0]=0
    states=source[:,None]+supply
    fluct=(states-u[:,None])/u[:,None]
    # Fourier amplitudes generated earlier from a finer grid, not retuned here.
    nvec=[];analytic=np.zeros((2,2));rows=[]
    for n in range(1,8):
        cos=next(x for x in CASE['amplitudes'] if x['mode']==n and x['component']=='cosine')
        sin=next(x for x in CASE['amplitudes'] if x['mode']==n and x['component']=='sine')
        vc=np.array([cos['S_D'],cos['delta_R']]);vs=np.array([sin['S_D'],sin['delta_R']])
        v=vc[:,None]*np.cos(2*np.pi*n*phase)+vs[:,None]*np.sin(2*np.pi*n*phase)
        cov=.5*(np.outer(vc,vc)+np.outer(vs,vs));analytic+=cov
        rows.append(dict(mode=n,k_Mpc_inv=.05*n,cov_DD=float(cov[0,0]),cov_DR=float(cov[0,1]),cov_RR=float(cov[1,1]),
            min_eigenvalue=float(np.linalg.eigvalsh(cov).min()),rank=int(np.linalg.matrix_rank(cov,tol=1e-30))))
        nvec.append(v)
    reconstructed=np.sum(nvec,axis=0)
    covariance=fluct[1:]@fluct[1:].T/128
    discrepancy=float(np.max(abs(covariance-analytic))/np.max(abs(analytic)))
    rec_error=float(np.max(abs(reconstructed-fluct[1:]))/np.max(abs(fluct[1:])))
    # Cross-harmonic covariance vanishes for this finite phase register (frequencies <=7).
    cross=max(np.max(abs(nvec[n]@nvec[m].T/128)) for n in range(7) for m in range(7) if n!=m)
    # Intrinsic variance of an independent supply bit preparation, before gravity/averaging.
    archive=np.load(ROOT/'inputs/addresses.npz');addr=archive['addresses'][1:]
    w=archive['address_weights'][1:];e=archive['sector_effects'][1:].T
    contrib=e*w[None,:]*(1+np.array([0,.25,0])[:,None]*np.log(addr)[None,:]/np.log(addr[-1]))
    squared=np.array([np.bincount(addr%30,weights=x*x,minlength=30) for x in contrib])
    intrinsic_var=(eta[:,None]*gap)**2*(squared[:,mask]@(probability[mask]*(1-probability[mask])))
    intrinsic_var[0]=0
    rms=np.sqrt(intrinsic_var.mean(1))/u
    mean_rms=np.sqrt(np.diag(covariance))
    r=camb.get_background(params('R'))
    start_rows=[]
    # Construct CDM entropy + its adopted regular radiation-era gravitational dressing.
    om=(r.grhob+r.grhoc)/np.sqrt(3*(r.grhog+r.grhornomass+sum(r.grhormass[:r.Params.nu_mass_eigenstates])))
    Rc=r.Params.omch2/(r.Params.omch2+r.Params.ombh2)
    for n in range(1,8):
        k=.05*n;tau=min(.001/k,.1);a=r.adotrad*tau*(1+om*tau/4)
        for comp in ['cosine','sine']:
            row=next(x for x in CASE['amplitudes'] if x['mode']==n and x['component']==comp)
            sd,sr=row['S_D'],row['delta_R'];x=k*tau;o=om*tau
            dg=sd*Rc*o*(-2/3+o/4);db=.75*dg;dd=sd+db
            vb=-sd*Rc/12*o*x
            vd_rad=-k*(u[2]/u[1])*a**3*sr*tau/5
            # Retarded velocity in the adopted near-radiation background series, no free v_D.
            def integrand(tt):
                aa=r.adotrad*tt*(1+om*tt/4)
                return aa**4
            integ=quad(integrand,0,tau,epsabs=1e-60,epsrel=1e-11)[0]
            vd=-k*(u[2]/u[1])*sr*integ/a
            start_rows.append(dict(mode=n,component=comp,tau_Mpc=tau,a=a,entropy_seed=sd,
                delta_gamma_regular=dg,delta_baryon_regular=db,delta_dark_regular=dd,v_baryon_regular=vb,
                delta_R=sr,v_dark_radiation_series=vd_rad,v_dark_retarded_background_series=vd,
                relative_velocity_series_correction=abs(vd-vd_rad)/max(abs(vd),1e-40),
                entropy_identity_error=abs(dd-.75*dg-sd)))
    minimum_C=float(np.linalg.eigvalsh(covariance).min())
    result=dict(version='finite_initial_preparation_0.1',date='2026-10-14',candidate_lambda=[0,.25,0],
        counted_new_register=dict(name='phase control',dimension=128,state='I/128',entropy_nats=float(np.log(128)),
            distinct_from_source_mode_register=True,energy='Declared degenerate control memory; no uncounted reset cycle'),
        source_state='|8><8|',supplier_state='(1-p_r,j)|0><0|+p_r,j|1><1|',record_state='|0><0|',
        joint_state='Block diagonal over 128 phase-control values; shared phase, conditional supplier marginals',
        supply_probability_range=[float(probability.min()),float(probability.max())],
        phase_trace=1,all_conditional_states_positive=bool(0<=probability.min() and probability.max()<=1),
        covariance_finite_phase=covariance.tolist(),covariance_Fourier_analytic=analytic.tolist(),
        relative_covariance_agreement=discrepancy,relative_profile_reconstruction_error=rec_error,
        max_cross_harmonic_covariance=float(cross),minimum_covariance_eigenvalue=minimum_C,
        mean_stress_relative_RMS_D_R=mean_rms.tolist(),
        independent_supplier_intrinsic_relative_RMS_P_D_R=rms.tolist(),
        mean_stress_equals_single_outcome=False,
        independent_frame_count_needed_for_noise_below_mean_D_R=[int(np.ceil((rms[s]/mean_rms[s-1])**2)) for s in [1,2]],
        gravity_readout='Existing semiclassical ensemble-mean stress. Intrinsic operator variance is reported separately; it is not silently added as a cosmological random field.',
        initial_dressing='Adopted regular radiation/CDM-isocurvature completion applied to address-generated entropy; retarded v_D sourced by delta_R with no decaying homogeneous velocity mode',
        status='Finite mean-stress preparation and covariance constructed. Dynamical preparation history and stochastic/single-outcome gravity not closed.',
        checks=dict(positive_preparation=bool(0<=probability.min() and probability.max()<=1),
            covariance_PSD=minimum_C>=-1e-30,covariance_Fourier_match=discrepancy<1e-6,
            finite_profile_match=rec_error<1e-6,
            entropy_arithmetic_identity=bool(max(x['entropy_identity_error'] for x in start_rows)<1e-30)))
    (OUT/'preparation_results.json').write_text(json.dumps(result,indent=2))
    for filename,data in [('initial_condition_ledger.csv',start_rows),('mode_covariance.csv',rows)]:
        with (OUT/filename).open('w') as f:
            writer=csv.DictWriter(f,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
    np.savez_compressed(OUT/'finite_preparation.npz',phase=phase,probability=probability,
        source_energy=source,supplier_energy=supply,mean_total_energy=states,
        dimensionless_fluctuation=fluct,intrinsic_supplier_variance=intrinsic_var)
    print(json.dumps(dict(covariance_error=discrepancy,mean_RMS=mean_rms.tolist(),intrinsic_supplier_RMS=rms.tolist(),checks=result['checks'])),flush=True)

if __name__=='__main__':main()
