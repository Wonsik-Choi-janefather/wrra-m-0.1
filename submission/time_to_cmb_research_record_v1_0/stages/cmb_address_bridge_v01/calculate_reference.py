"""Conditional SOURCE CMB response. Patched CAMB 2.0.4 required for new modes.
No parameter optimizer. Native Plik-lite evaluation is performed separately.
"""
from pathlib import Path
import json, argparse, csv, hashlib, time
import numpy as np
import camb
from scipy.interpolate import CubicSpline
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
L_MAX=2508 # Includes the final Plik-lite TT bin.
FIXED=dict(mnu=.06,nnu=3.044,tau=.0544,TCMB=2.7255)
LEDGER=json.loads((ROOT/'inputs/closed_ledger.json').read_text())

def record(branch):
    return next(r['observables'] for r in LEDGER['cases'] if r['id']==branch+'_uniform_g_parity')

def params(branch,kind,accuracy=1.5,force=1,start_factor=1):
    r=record(branch);p=camb.CAMBparams()
    p.set_cosmology(H0=r['H0_derived_km_s_Mpc'],ombh2=r['ombh2'],omch2=r['omch2'],omk=0,
        bbn_predictor='PRIMAT_Yp_DH_ErrorMC_2024.dat',**FIXED)
    p.InitPower.set_params(As=2.1e-9,ns=.9649,pivot_scalar=.05)
    p.set_dark_energy(w=-1,wa=0,dark_energy_model='fluid')
    p.set_for_lmax(L_MAX,lens_potential_accuracy=0)
    p.NonLinear=camb.model.NonLinear_none
    p.set_accuracy(AccuracyBoost=accuracy,lAccuracyBoost=accuracy,lSampleBoost=accuracy)
    if kind!='standard':
        from camb.dark_energy import SourceVacuum
        p.DarkEnergy=SourceVacuum()
        p.DarkEnergy.delta_R_initial=1 if kind=='R' else 0
        p.DarkEnergy.force_multiplier=force
        p.DarkEnergy.start_factor=start_factor
    if kind in ('D','R'):
        p.DarkEnergy.discrete_modes=True
        p.DoLensing=False
        p.Want_CMB_lensing=False
        p.max_l=L_MAX
        p.max_eta_k=7000
        p.Accuracy.lSampleBoost=50 # Every integer ell: line spectra need this.
        p.Accuracy.IntTolBoost=3
        p.DoLateRadTruncation=False # Matter-only RSA omits the spatial vacuum pressure.
        p.scalar_initial_condition='initial_vector'
        p.InitialConditionVector=[0,1 if kind=='D' else 0,0,0,0]
    return p

def run(branch,kind,accuracy,force,start_factor=1):
    start=time.time();p=params(branch,kind,accuracy,force,start_factor)
    r=camb.get_transfer_functions(p)
    tag=f'{branch}_{kind}_a{accuracy:g}_f{force:g}'
    if start_factor!=1:tag+=f'_s{start_factor:g}'
    if L_MAX!=2508:tag+=f'_l{L_MAX}'
    if kind in ('D','R'):
        t=r.get_cmb_transfer_data()
        assert t.q.shape==(7,) and np.max(abs(t.q-.05*np.arange(1,8)))<1e-14
        assert np.array_equal(t.L,np.arange(2,L_MAX+1))
        L=t.L.astype(float)
        T=t.delta_p_l_k[0]
        E=t.delta_p_l_k[1]*np.sqrt((L-1)*L*(L+1)*(L+2))[:,None]
        np.savez_compressed(OUT/(tag+'.npz'),ell=t.L,k=t.q,T=T,E=E)
    else:
        r.power_spectra_from_transfer()
        dl=r.get_total_cls(lmax=L_MAX,CMB_unit='muK')
        np.savez_compressed(OUT/(tag+'.npz'),ell=np.arange(len(dl)),Dl=dl,
            unlensed=r.get_unlensed_scalar_cls(lmax=L_MAX,CMB_unit='muK'))
    (OUT/(tag+'_params.txt')).write_text(str(p))
    print(json.dumps(dict(tag=tag,seconds=time.time()-start,finite=True)),flush=True)

def assemble(branch,accuracy=1.5,force=1):
    d=np.load(OUT/f'{branch}_D_a{accuracy:g}_f1.npz')
    r=np.load(OUT/f'{branch}_R_a{accuracy:g}_f{force:g}.npz')
    ell=d['ell'];k=d['k']
    u=np.array(record(branch)['u_P_D_R_today_J_m3'])
    rows=list(csv.DictReader((ROOT/'inputs/SOURCE_harmonic_GR_controls.csv').open()))
    full=np.zeros((len(ell),4));per=[]
    for row in rows:
        if row['branch']!=branch:continue
        n=int(row['mode'])-1
        sd=float(row['delta_u_D_at_a1_J_m3'])/u[1]
        sr=float(row['delta_u_R_J_m3'])/u[2]
        T=sd*d['T'][:,n]+sr*r['T'][:,n]
        E=sd*d['E'][:,n]+sr*r['E'][:,n]
        # Uniform global phase: component covariance=1/2. Uniform orientation:
        # angular Cl=4pi*(1/2)*sum transfer products. No continuous k integral.
        factor=ell*(ell+1)*(FIXED['TCMB']*1e6)**2
        signal=np.column_stack([T*T,E*E,np.zeros(len(T)),T*E])*factor[:,None]
        full+=signal
        per.append(dict(mode=n+1,component=row['component'],S_D=sd,delta_R=sr,
            max_TT_Dl_uK2=float(signal[:,0].max()),max_EE_Dl_uK2=float(signal[:,1].max())))
    baseline=np.load(OUT/f'{branch}_standard_a{accuracy:g}_f1.npz')['Dl']
    combined=baseline.copy();combined[ell]+=full
    def diag(dl):
        result={};allr=[]
        for name,c,release in [('TT',0,'3.01'),('TE',3,'3.02'),('EE',1,'3.02')]:
            b=np.loadtxt(ROOT/f'inputs/COM_PowerSpect_CMB-{name}-binned_R{release}.txt')
            sig=(b[:,2]+b[:,3])/2
            res=(np.interp(b[:,0],np.arange(len(dl)),dl[:,c])-b[:,1])/sig
            result[name]=dict(RMS_public_bin_sigma=float(np.sqrt(np.mean(res**2))),diagonal_Q=float(res@res),n=len(res))
            allr.extend(res)
        result['all']=dict(RMS_public_bin_sigma=float(np.sqrt(np.mean(np.array(allr)**2))),diagonal_Q=float(np.sum(np.array(allr)**2)),n=len(allr))
        return result
    np.savetxt(OUT/f'{branch}_SOURCE_a{accuracy:g}_f{force:g}_Dl.csv',np.c_[ell,full],delimiter=',',header='ell,TT,EE,BB,TE [microK^2]',comments='')
    if force==1:
        np.savetxt(OUT/f'{branch}_baseline_plus_SOURCE_a{accuracy:g}_Dl.csv',np.c_[np.arange(len(combined)),combined],delimiter=',',header='ell,TT,EE,BB,TE [microK^2]',comments='')
    ratio=full[:,[0,1]]/baseline[ell][:,[0,1]]
    cov=np.abs(full[:,3])-np.sqrt(full[:,0]*full[:,1])
    return dict(branch=branch,accuracy=accuracy,force=force,
        maximum_SOURCE_TT_Dl_uK2=float(full[:,0].max()),maximum_SOURCE_EE_Dl_uK2=float(full[:,1].max()),
        maximum_abs_SOURCE_TE_Dl_uK2=float(abs(full[:,3]).max()),
        maximum_fractional_TT=float(ratio[:,0].max()),maximum_fractional_EE=float(ratio[:,1].max()),
        SOURCE_TE_covariance_excess=float(cov.max()),baseline=diag(baseline),baseline_plus_SOURCE=diag(combined),components=per)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--branch',choices=['weighted','unweighted'],required=True)
    a.add_argument('--kind',choices=['standard','zero','D','R'],required=True)
    a.add_argument('--accuracy',type=float,default=1.5);a.add_argument('--force',type=float,default=1)
    a.add_argument('--start-factor',type=float,default=1)
    a.add_argument('--lmax',type=int,default=2508)
    v=a.parse_args();L_MAX=v.lmax;run(v.branch,v.kind,v.accuracy,v.force,v.start_factor)
