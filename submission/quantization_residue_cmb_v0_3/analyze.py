import verify_inputs
from pathlib import Path
import json,math,hashlib
import numpy as np
P=Path(__file__).resolve().parent;OUT=P/'results';checks={}
def check(name,ok):
    checks[name]=bool(ok)
    if not ok:raise AssertionError(name)

def assemble(kind):
    arrays={f:np.full((5999,64),np.nan) for f in ['T','E','phi']};seen=np.zeros(5999,int)
    overlap={f:0. for f in arrays}
    for offset in range(8):
        f=OUT/f'{kind}_64_a2.5_s16_o{offset}_k50000.npz';d=np.load(f);ix=d['ell'].astype(int)-2
        expected=set(range(2,101))
        for lo in range(101+2*offset,6001,16):
            expected.add(lo)
            if lo+1<=6000:expected.add(lo+1)
        expected.update([5999,6000])
        check(kind+'_shard_grid_'+str(offset),set(d['ell'])==expected)
        check(kind+'_k_grid_'+str(offset),np.max(abs(d['k']-.05*np.arange(1,65)))<2e-14)
        dup=seen[ix]>0
        for key in arrays:
            if np.any(dup):
                scale=max(float(np.max(abs(d[key]))),1e-100)
                err=float(np.max(abs(arrays[key][ix[dup]]-d[key][dup]))/scale)
                overlap[key]=max(overlap[key],err)
                check(kind+'_overlap_'+key+'_'+str(offset),err<1e-10)
            arrays[key][ix]=d[key]
        seen[ix]+=1
    check(kind+'_all_integer_multipoles_filled',np.all(seen>0))
    check(kind+'_finite_transfer_arrays',all(np.isfinite(a).all() for a in arrays.values()))
    np.savez_compressed(OUT/f'{kind}_64_full.npz',ell=np.arange(2,6001),k=.05*np.arange(1,65),**arrays)
    return arrays,overlap

def spectrum(transfer,variance,start=0,stop=64):
    names=['T','E','phi'];units=[2.7255e6,2.7255e6,1.]
    ell=np.arange(2,6001);weight=np.broadcast_to(variance[None,:],(5999,64)).copy()
    # For the adopted real Nyquist cosine and the original discrete translations,
    # its odd-ell body amplitude vanishes; no extra sine state is introduced.
    weight[ell%2==1,63]=0.
    weight[:,:start]=0;weight[:,stop:]=0
    out=np.empty((5999,3,3))
    for i,x in enumerate(names):
        for j,y in enumerate(names):out[:,i,j]=4*np.pi*units[i]*units[j]*np.sum(weight*transfer[x]*transfer[y],axis=1)
    return out

def metrics(c):
    ell=np.arange(2,6001);w=(2*ell+1)/(4*np.pi)
    return dict(T_RMS_microK=math.sqrt(float(w@c[:,0,0])),E_RMS_microK=math.sqrt(float(w@c[:,1,1])),
        deflection_RMS_arcsec=math.sqrt(float((w*ell*(ell+1))@c[:,2,2]))*180/math.pi*3600)

def main():
    d,do=assemble('D');a,ao=assemble('A')
    ell=np.arange(2,6001);seed=np.load(P/'inputs/quantized_seed.npz')['entropy'];seed-=seed.mean()
    h=np.fft.rfft(seed)/len(seed);variance=2*abs(h[1:])**2;variance[-1]/=2
    var=float(np.mean(seed**2));check('full_finite_Parseval',abs(variance.sum()/var-1)<1e-12)
    check('tail_is_original_10_897_percent',abs(variance[7:].sum()/var-.1089718520284253)<1e-12)
    static=spectrum(d,variance);seven=spectrum(d,variance,0,7);tail=spectrum(d,variance,7,64)
    check('complete_spectral_budget',np.max(abs(static-seven-tail))/np.max(static)<1e-12)
    dy=json.loads((OUT/'dynamics_results.json').read_text());rs=dy['entropy_response_to_rate_modulation'];rz=dy['radiation_curvature_response']
    # Basis sign was checked with CAMB's actual initial callback: vector A=1 -> zeta_r=-1.
    combined={key:rs*d[key]-rz*a[key] for key in d}
    dyn=spectrum(combined,variance);dynD=spectrum({key:rs*d[key] for key in d},variance)
    correlation_min={}
    for name,c in [('static',static),('dynamic',dyn)]:
        diag=np.diagonal(c,axis1=1,axis2=2)
        den=np.sqrt(diag[:,:,None]*diag[:,None,:]);corr=np.divide(c,den,out=np.zeros_like(c),where=den>0)
        eig=float(np.linalg.eigvalsh(corr).min());correlation_min[name]=eig
        check(name+'_full_covariance_PSD',eig>-1e-10)
        check(name+'_positive_auto_power',np.all(diag>=0))
    # Exact phase sum independently validates the Nyquist normalization and parity.
    co=2*h[1:].real;si=-2*h[1:].imag;co[-1]/=2;si[-1]=0
    theta=2*np.pi*np.arange(128)/128;n=np.arange(1,65)
    cs=np.cos(n[:,None]*theta);sn=np.sin(n[:,None]*theta);sn[-1]=0;cs[-1]=(-1.)**np.arange(128)
    phase_err=0.
    for ix in [0,1,98,99,498,999,1998,5998]:
        l=ell[ix];rows=[]
        for key,unit in [('T',2.7255e6),('E',2.7255e6),('phi',1.)]:
            t=combined[key][ix]
            body=(t*co)@cs+(t*si)@sn if l%2==0 else (t*co)@sn-(t*si)@cs
            rows.append(body*unit*np.sqrt(4*np.pi*(2*l+1)))
        direct=np.array(rows)@np.array(rows).T/(128*(2*l+1))
        ref=dyn[ix];norm=np.sqrt(np.outer(np.diag(ref),np.diag(ref)))
        err=float(np.max(np.divide(abs(direct-ref),norm,out=np.zeros_like(norm),where=norm>0)))
        phase_err=max(phase_err,err);check('direct_phase_covariance_ell_'+str(l),err<1e-11)
    # Actual re-evolution of old seven k values at identical observed multipoles.
    old=np.load(P/'inputs/D_lens_a2.5.npz');recheck={}
    for key in ['T','E','phi']:
        recheck[key]=float(np.max(abs(d[key][:,:7]-old[key]))/np.max(abs(old[key])))
        check('old_seven_transfer_recovery_'+key,recheck[key]<.005)
    oldres=json.loads((P/'inputs/previous_results.json').read_text())['outputs']
    mseven=metrics(seven);mst=metrics(static);mdyn=metrics(dyn);mtail=metrics(tail)
    ratio={k:mtail[k]**2/mst[k]**2 for k in mst}
    scope='64 exact k values and every integer ell=2..6000 assembled from actual paired-grid evolutions; no missing-multipole interpolation or k extrapolation. Dynamics is a calibrated gradient-leading expanding two-fluid closure with a quantized spatial seed; full finite-gradient and microphysical matching remains OPEN.'
    result={'version':'0.3','new_mode_count':57,'total_mode_count':64,'integer_multipoles':5999,
        'input_entropy_variance':var,'all_64_entropy_variance':float(variance.sum()),'untransferred_initial_entropy_variance_fraction':0.,
        'new_tail_initial_entropy_variance_fraction':float(variance[7:].sum()/var),
        'Nyquist_initial_variance_fraction':float(variance[-1]/var),'Nyquist_rule':'real cosine, original 128 discrete translations, no added sine; zero odd-ell contribution',
        'static_seven_recomputed':mseven,'static_all_64':mst,'static_new_57_only':mtail,
        'tail_fraction_of_projected_variance':ratio,'dynamic_all_64':mdyn,
        'dynamic_with_adiabatic_vs_D_only_relative_RMS':{k:mdyn[k]/metrics(dynD)[k]-1 for k in mdyn},
        'old_seven_transfer_normalized_max_errors':recheck,
        'old_seven_RMS_relative_changes':{'T':mseven['T_RMS_microK']/oldres['projected_CMB_T_RMS_microK']-1,'E':mseven['E_RMS_microK']/oldres['projected_CMB_E_RMS_microK']-1,'deflection':mseven['deflection_RMS_arcsec']/oldres['projected_deflection_RMS_arcsec']-1},
        'shard_overlap_errors':{'D':do,'A':ao},'covariance_min_eigenvalues':correlation_min,'direct_phase_error_max':phase_err,
        'checks_passed':sum(checks.values()),'checks':checks,'dynamics_checks_passed':dy['checks_passed'],'scope':scope}
    (OUT/'extension_results.json').write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(OUT/'complete_projection.npz',ell=ell,k=.05*np.arange(1,65),mode_variance=variance,
        seed=seed,static_covariance=static,static_seven_covariance=seven,new_tail_covariance=tail,dynamic_covariance=dyn)
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
if __name__=='__main__':main()
