"""SOURCE lensing potential and leading covariance lensing response.
The finite SOURCE phase ensemble is not assumed exactly Gaussian.
"""
from pathlib import Path
import sys,json
import numpy as np
import camb
from preparation import params,CASE,ROOT,OUT

L_INPUT=6000;L_OUT=2508

def lens_params(kind,accuracy):
    p=params(kind,accuracy)
    if kind in ['D','R']:
        p.max_l=L_INPUT;p.max_eta_k=8000
        p.Want_CMB_lensing=True;p.DoLensing=False
        p.SourceTerms.limber_windows=True
        p.SourceTerms.limber_phi_lmin=100000 # Exact seven-k projection; no continuum Limber fill.
        p.Accuracy.TimeStepBoost=2
    else:
        p.set_for_lmax(L_INPUT,lens_potential_accuracy=1)
        p.NonLinear=camb.model.NonLinear_none
    return p

def run(kind,accuracy):
    p=lens_params(kind,accuracy);r=camb.get_transfer_functions(p)
    tag=f'{kind}_lens_a{accuracy:g}'
    if kind in ['D','R']:
        t=r.get_cmb_transfer_data();L=t.L.astype(float)
        assert t.delta_p_l_k.shape[0]>=3
        assert np.array_equal(t.L,np.arange(2,L_INPUT+1))
        assert np.max(abs(t.q-.05*np.arange(1,8)))<1e-14
        np.savez_compressed(OUT/(tag+'.npz'),ell=t.L,k=t.q,T=t.delta_p_l_k[0],
            E=t.delta_p_l_k[1]*np.sqrt((L-1)*L*(L+1)*(L+2))[:,None],phi=t.delta_p_l_k[2])
    else:
        r.power_spectra_from_transfer()
        unl=r.get_unlensed_scalar_cls(lmax=r.Params.max_l,CMB_unit='muK')
        pp=r.get_lens_potential_cls(lmax=r.Params.max_l)[:,0]
        lensed=r.get_total_cls(lmax=L_OUT,CMB_unit='muK')
        np.savez_compressed(OUT/(tag+'.npz'),ell=np.arange(len(unl)),unlensed_Dl=unl,pp_Dl=pp,
            lensed_Dl=lensed)
        # Verify third transfer normalization at low L where baseline uses exact projection.
        t=r.get_cmb_transfer_data();ix=np.flatnonzero((t.L>=2)&(t.L<=30));kk=t.q
        power=2.1e-9*(kk/.05)**(.9649-1) # Fixed power-law input, zero running.
        calc=4*np.pi*np.trapezoid(t.delta_p_l_k[2,ix]**2*power[None,:],x=np.log(kk),axis=1)
        raw=r.get_lens_potential_cls(lmax=L_OUT,raw_cl=True)[:,0]
        err=float(np.max(abs(calc/raw[t.L[ix]]-1)))
        (OUT/'phi_transfer_normalization.json').write_text(json.dumps(dict(max_relative_low_L_error=err,
            comparison='Direct 4pi integral of the third CAMB transfer against raw C_phi_phi',passed=err<.02),indent=2))
    (OUT/(tag+'_params.txt')).write_text(str(p))
    print('Completed '+tag,flush=True)

def source(accuracy):
    d=np.load(OUT/f'D_lens_a{accuracy:g}.npz');r=np.load(OUT/f'R_lens_a{accuracy:g}.npz')
    L=d['ell'].astype(np.int64);lf=L.astype(np.float64)
    C=np.zeros((L_INPUT+1,4));pp=np.zeros(L_INPUT+1);cross=np.zeros((L_INPUT+1,2))
    components=[]
    for x in CASE['amplitudes']:
        n=x['mode']-1
        T=x['S_D']*d['T'][:,n]+x['delta_R']*r['T'][:,n]
        E=x['S_D']*d['E'][:,n]+x['delta_R']*r['E'][:,n]
        phi=x['S_D']*d['phi'][:,n]+x['delta_R']*r['phi'][:,n]
        factor=lf*(lf+1)*(2.7255e6)**2
        C[L]+=np.c_[T*T,E*E,np.zeros(len(L)),T*E]*factor[:,None]
        pp[L]+=(lf*(lf+1))**2*phi**2
        cross[L,0]+=2*np.pi*(2.7255e6)*T*phi
        cross[L,1]+=2*np.pi*(2.7255e6)*E*phi
        components.append(np.c_[T,E,phi])
    np.savez_compressed(OUT/f'SOURCE_lens_a{accuracy:g}.npz',ell=np.arange(L_INPUT+1),CMB_Dl=C,phi_Dl=pp,
        Tphi_Ephi_raw=cross,real_components=np.array(components))
    return C,pp

if __name__=='__main__':run(sys.argv[1],float(sys.argv[2]))
