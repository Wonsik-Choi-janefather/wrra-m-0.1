"""CMB execution consumes the address-generated ledger and Fourier vectors."""
from pathlib import Path
import json,sys
import numpy as np
import camb
from calculate_reference import params as reference_params
from plik_lite import NativePlikLite
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'results'
L_MAX=2508

def case(branch):
    j=json.loads((OUT/'address_results.json').read_text())
    return next(r for r in j['cases'] if r['branch']==branch)

def make_params(branch,kind,accuracy):
    p=reference_params('unweighted',kind,accuracy)
    q=case(branch)['background']
    p.set_cosmology(H0=q['H0'],ombh2=q['ombh2'],omch2=q['omch2'],omk=0,
        mnu=.06,nnu=3.044,tau=.0544,TCMB=2.7255,bbn_predictor='PRIMAT_Yp_DH_ErrorMC_2024.dat')
    return p

def run(branch,kind,accuracy):
    p=make_params(branch,kind,accuracy)
    r=camb.get_transfer_functions(p)
    tag=f'{branch}_{kind}_a{accuracy:g}'
    if kind in ('D','R'):
        t=r.get_cmb_transfer_data();L=t.L.astype(float)
        assert np.array_equal(t.L,np.arange(2,L_MAX+1))
        assert np.max(abs(t.q-.05*np.arange(1,8)))<1e-14
        np.savez_compressed(OUT/(tag+'.npz'),ell=t.L,k=t.q,T=t.delta_p_l_k[0],
            E=t.delta_p_l_k[1]*np.sqrt((L-1)*L*(L+1)*(L+2))[:,None])
    else:
        r.power_spectra_from_transfer();dl=r.get_total_cls(lmax=L_MAX,CMB_unit='muK')
        np.savez_compressed(OUT/(tag+'.npz'),ell=np.arange(len(dl)),Dl=dl)
        like=NativePlikLite()
        print(json.dumps(dict(branch=branch,kind=kind,accuracy=accuracy,chi2=like.evaluate(dl)['chi2_highell'])),flush=True)
    (OUT/(tag+'_params.txt')).write_text(str(p))
    print('Completed '+tag,flush=True)

def combine(branch,accuracy):
    inp=case(branch);d=np.load(OUT/f'{branch}_D_a{accuracy:g}.npz');r=np.load(OUT/f'{branch}_R_a{accuracy:g}.npz')
    ell=d['ell'];signal=np.zeros((L_MAX+1,4));per=[]
    for row in inp['amplitudes']:
        n=row['mode']-1;T=row['S_D']*d['T'][:,n]+row['delta_R']*r['T'][:,n]
        E=row['S_D']*d['E'][:,n]+row['delta_R']*r['E'][:,n]
        fac=ell*(ell+1)*(2.7255e6)**2
        contribution=np.c_[T*T,E*E,np.zeros(len(T)),T*E]*fac[:,None]
        signal[ell]+=contribution
        per.append(dict(mode=n+1,component=row['component'],max_TT=float(contribution[:,0].max()),max_EE=float(contribution[:,1].max())))
    baseline=np.load(OUT/f'{branch}_standard_a2.5.npz')['Dl'];full=baseline+signal
    np.savetxt(OUT/f'{branch}_SOURCE_a{accuracy:g}_Dl.csv',np.c_[np.arange(L_MAX+1),signal],delimiter=',',header='ell,TT,EE,BB,TE [microK^2]',comments='')
    if accuracy==2.5:
        np.savetxt(OUT/f'{branch}_baseline_plus_SOURCE_Dl.csv',np.c_[np.arange(L_MAX+1),full],delimiter=',',header='ell,TT,EE,BB,TE [microK^2]',comments='')
    like=NativePlikLite()
    return dict(branch=branch,accuracy=accuracy,baseline_high_ell_chi2=like.evaluate(baseline)['chi2_highell'],
        combined_high_ell_chi2=like.evaluate(full)['chi2_highell'],SOURCE_max_TT_Dl_uK2=float(signal[:,0].max()),
        SOURCE_max_EE_Dl_uK2=float(signal[:,1].max()),components=per,
        finite=bool(np.isfinite(full).all()),TE_covariance_excess=float(np.max(abs(signal[:,3])-np.sqrt(signal[:,0]*signal[:,1]))))

if __name__=='__main__':
    run(sys.argv[1],sys.argv[2],float(sys.argv[3]))
