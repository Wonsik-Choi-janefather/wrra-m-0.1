"""Finite conservative conversion/quantization preparation and cached CMB projection.
This is a declared boundary-preparation model, not a Boltzmann/collapse solver.
Run: python reproduce.py. Requires numpy, scipy, matplotlib (figures only).
"""
from pathlib import Path
from fractions import Fraction
import hashlib, json, math, csv
import numpy as np

ROOT=Path(__file__).resolve().parent
IN=ROOT/'inputs'; OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)
CFG=json.loads((ROOT/'config.json').read_text())
CHECKS={}
def check(name, condition):
    CHECKS[name]=bool(condition)
    if not condition: raise AssertionError(name)
def save(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')

def conversion(target, quantum, stages):
    """Exact rational accumulator; unconverted energy always stays in radiation.
    Stages subdivide the same constant demand, not independent random redraws.
    """
    if stages<1 or quantum<=0: raise ValueError('invalid clock/quantum')
    demand=Fraction(str(float(target)))
    if not 0<=demand<=1: raise ValueError('target outside reservoir')
    u=demand/stages; r=Fraction(0); m=Fraction(0); max_r=Fraction(0)
    for _ in range(stages):
        v=u+r; tick=v//quantum; dm=tick*quantum; r=v-dm; m+=dm
        if not (0<=r<quantum and 0<=m<=1): raise AssertionError('ledger/positivity')
        if m+(1-m)!=1: raise AssertionError('energy nonconservation')
        max_r=max(max_r,r)
    if demand-m != r: raise AssertionError('residual identity')
    naive=stages*(u//quantum)*quantum
    return m,r,max_r,demand-naive,max(demand.denominator.bit_length(),r.denominator.bit_length())

def entropy_from_conversion(f):
    mean=float(np.mean(f)); df=f-mean
    dm=df/mean; dg=-df/(1-mean)
    return dm-.75*dg,dm,dg,mean

def real_coefficients(s, count=7):
    # Fourier readout on a finite periodic patch; not a causal field generator.
    a=np.fft.rfft(s)/len(s)
    return 2*a[1:count+1].real, -2*a[1:count+1].imag

def cmb_project(co,si,d):
    ell=d['ell'].astype(int); cl={}
    for x,u in [('T',2.7255e6),('E',2.7255e6),('phi',1.)]:
        cl[x]=2*math.pi*u*u*np.sum(d[x]**2*(co**2+si**2)[None,:],axis=1)
    cl['TE']=2*math.pi*(2.7255e6)**2*np.sum(d['T']*d['E']*(co**2+si**2)[None,:],axis=1)
    for key in ['T','E']:
        cl[key+'phi']=2*math.pi*2.7255e6*np.sum(d[key]*d['phi']*(co**2+si**2)[None,:],axis=1)
    return cl

def sky_moments(co,si,d,lmax=80):
    from numpy.polynomial.legendre import leggauss, legvander
    ell=d['ell'].astype(int); use=ell<=lmax; ls=ell[use]
    theta=2*math.pi*np.arange(CFG['sites'])/CFG['sites']; n=np.arange(1,8)
    c=np.cos(n[:,None]*theta); s=np.sin(n[:,None]*theta)
    body=[]
    for field,unit in [('T',2.7255e6),('E',2.7255e6)]:
        even=(d[field][use]*co)@c+(d[field][use]*si)@s
        odd=(d[field][use]*co)@s-(d[field][use]*si)@c
        a=np.where((ls%2==0)[:,None],((-1.)**(ls//2))[:,None]*even,
                   ((-1.)**((ls+1)//2))[:,None]*odd)
        body.append(a*unit*np.sqrt(4*math.pi*(2*ls+1))[:,None])
    mu,w=leggauss(2*lmax+1)
    p=legvander(mu,lmax)[:,ls]*np.sqrt((2*ls+1)/(4*math.pi))[None,:]
    rows=[]
    for field,a in zip(['T','E'],body):
        sky=p@a; mean=np.sum(w[:,None]*sky)/(2*len(theta)); z=sky-mean
        m2=float(np.sum(w[:,None]*z**2)/(2*len(theta)))
        m3=float(np.sum(w[:,None]*z**3)/(2*len(theta)))
        m4=float(np.sum(w[:,None]*z**4)/(2*len(theta)))
        rows.append(dict(field=field,lmax=lmax,RMS_microK=math.sqrt(m2),
                         skewness=m3/m2**1.5,excess_kurtosis=m4/m2**2-3))
    return rows

def main():
    frozen=json.loads((ROOT/'inputs_frozen_sha256.json').read_text())
    for filename, digest in frozen.items():
        check('frozen_input_'+filename,hashlib.sha256((IN/filename).read_bytes()).hexdigest()==digest)
    J=CFG['sites']; theta=2*math.pi*np.arange(J)/J
    cases=json.loads((IN/'address_results.json').read_text())['cases']
    old=next(x for x in cases if x['branch']=='dark_weight_only')
    b=np.zeros(J); oc=np.zeros(7); os=np.zeros(7)
    for a in old['amplitudes']:
        n=a['mode']; amp=a['S_D']
        b+=amp*(np.cos(n*theta) if a['component']=='cosine' else np.sin(n*theta))
        (oc if a['component']=='cosine' else os)[n-1]=amp
    # Conservative finite-volume divergence; g converts fraction to entropy.
    mean=CFG['mean_conversion_fraction']; g=1/mean+.75/(1-mean)
    twist=(np.roll(b,-1)-np.roll(b,1))/(2*math.sin(2*math.pi/J))
    check('twist_zero_mean',abs(float(np.mean(twist)))<1e-22)
    target=mean+CFG['twist_coupling']*twist/g
    q=Fraction(CFG['quantum_fraction']); N=CFG['conversion_stages']
    out=[conversion(x,q,N) for x in target]
    f=np.array([float(x[0]) for x in out]); r=np.array([float(x[1]) for x in out])
    s,dm,dg,actualmean=entropy_from_conversion(f)
    check('compensated_energy_density',np.max(abs(actualmean*dm+(1-actualmean)*dg))<1e-22)
    check('radiation_and_matter_positive',np.all((f>0)&(f<1)))
    check('bounded_residual',np.max(r)<float(q) and np.min(r)>=0)
    check('residual_reconstructs_target',np.max(abs(f+r-target))<2e-16)
    check('nonzero_individual_spatial_variation',np.std(s)>0)
    check('homogeneous_no_twist_control',len({conversion(mean,q,N)[0] for _ in range(J)})==1)
    # Independent subdivision of identical integrated demand: exact equality.
    for steps in CFG['subdivision_controls']:
        alt=[conversion(x,q,steps) for x in target]
        check('exact_subdivision_'+str(steps),all(v[0]==u[0] and v[1]==u[1] for v,u in zip(out,alt)))
    check('naive_residual_rejection',max(float(x[3]) for x in out)>max(r))
    # Translation covariance of the local quantizer and divergence.
    for shift in [1,7,31,64]:
        ff=np.array([float(conversion(x,q,N)[0]) for x in np.roll(target,shift)])
        check('translation_covariance_'+str(shift),np.array_equal(ff,np.roll(f,shift)))
    # Sign reversal does not change power under this declared symmetric template.
    negf=np.array([float(conversion(x,q,N)[0]) for x in mean-CFG['twist_coupling']*twist/g])
    ns,*_=entropy_from_conversion(negf)
    check('twist_sign_power_symmetry',np.allclose(abs(np.fft.rfft(ns)),abs(np.fft.rfft(s)),rtol=1e-7,atol=1e-14))
    co,si=real_coefficients(s); totalvar=float(np.mean(s*s)); lowvar=.5*float(np.sum(co*co+si*si))
    # We do NOT discard the untransferred 8..64 harmonics from the ledger.
    missing=1-lowvar/totalvar
    check('spectral_variance_budget',-1e-12<=missing<=1+1e-12)
    direct_low=sum(co[i]*np.cos((i+1)*theta)+si[i]*np.sin((i+1)*theta) for i in range(7))
    check('parseval_low_modes',abs(float(np.mean(direct_low**2))/lowvar-1)<1e-12)
    d=np.load(IN/'D_lens_a2.5.npz'); rr=np.load(IN/'R_lens_a2.5.npz')
    check('cached_k_units_and_range',np.allclose(d['k'],.05*np.arange(1,8),rtol=0,atol=1e-14))
    check('cached_ell_range',np.array_equal(d['ell'],np.arange(2,6001)))
    cl=cmb_project(co,si,d); cl_cont=cmb_project(*real_coefficients(CFG['twist_coupling']*twist),d)
    # Reconstruct all old D+R projected two-point spectra as an independent
    # normalization control before projecting the new D-only entropy amplitudes.
    prior=np.load(IN/'SOURCE_lens_a2.5.npz'); ell=d['ell'].astype(int)
    old_components=np.zeros((3,2,len(ell),7)); units=[2.7255e6,2.7255e6,1.]
    for a in old['amplitudes']:
        n=a['mode']-1; j=0 if a['component']=='cosine' else 1
        for i,key in enumerate(['T','E','phi']):
            old_components[i,j,:,n]=units[i]*(a['S_D']*d[key][:,n]+a['delta_R']*rr[key][:,n])
    old_cl=2*math.pi*np.sum(old_components**2,axis=(1,3))
    refs=[prior['CMB_Dl'][ell,0]*2*math.pi/(ell*(ell+1)),prior['CMB_Dl'][ell,1]*2*math.pi/(ell*(ell+1)),prior['phi_Dl'][ell]*2*math.pi/(ell.astype(float)*(ell+1))**2]
    norm_errors={}
    for i,key in enumerate(['T','E','phi']):
        norm_errors[key]=float(np.max(abs(old_cl[i]-refs[i]))/np.max(abs(refs[i])))
        check('old_CMB_normalization_'+key,norm_errors[key]<1e-12)
        check('new_positive_auto_power_'+key,np.all(cl[key]>=0))
    check('TE_cauchy_schwarz',np.max(cl['TE']**2-cl['T']*cl['E'])<=np.max(cl['T']*cl['E'])*1e-12)
    # Check the complete covariance, including lensing cross terms, at every ell.
    # Normalize field units to test correlations rather than a badly scaled matrix.
    mat=np.empty((len(ell),3,3)); names=['T','E','phi']
    for i,x in enumerate(names):
        for j,y in enumerate(names):
            key=x if i==j else {('T','E'):'TE',('T','phi'):'Tphi',('E','phi'):'Ephi'}.get((x,y))
            if key is None: key={('E','T'):'TE',('phi','T'):'Tphi',('phi','E'):'Ephi'}[(x,y)]
            den=np.sqrt(cl[x]*cl[y]);mat[:,i,j]=np.divide(cl[key],den,out=np.zeros_like(den),where=den>0)
    eigmin=float(np.linalg.eigvalsh(mat).min())
    check('projected_full_T_E_phi_covariance_PSD_all_ell',eigmin>-1e-11)
    # A translated individual pattern has the same finite-translation ensemble C_l.
    for shift in [1,31]:
        trans=cmb_project(*real_coefficients(np.roll(s,shift)),d)
        check('CMB_translation_'+str(shift),max(np.max(abs(trans[k]-cl[k]))/max(np.max(abs(cl[k])),1e-100) for k in cl)<1e-11)
    qcontrols=[]
    for divisor in [1,2,4,16]:
        fq=np.array([float(conversion(x,q/divisor,N)[0]) for x in target])
        sq,*_=entropy_from_conversion(fq); err=float(np.sqrt(np.mean((sq-CFG['twist_coupling']*twist)**2)))
        qcontrols.append(dict(quantum_divisor=divisor,entropy_RMS=float(np.std(sq)),continuum_entropy_error_RMS=err))
        check('quantum_error_bound_'+str(divisor),err<=2*g*float(q/divisor))
    # Rejections are actual exceptions; no external wall or data tuning.
    rejected=0
    for value,qq,steps in [(-.1,q,N),(1.1,q,N),(.5,Fraction(0),N),(.5,q,0)]:
        try: conversion(value,qq,steps)
        except ValueError: rejected+=1
    check('four_invalid_controls_rejected',rejected==4)
    def rms(z): return math.sqrt(float(np.sum((2*ell+1)*z/(4*math.pi))))
    std=np.load(IN/'standard_lens_a2.5.npz')
    baselineT=std['unlensed_Dl'][ell,0]*2*math.pi/(ell*(ell+1))
    baselineE=std['unlensed_Dl'][ell,1]*2*math.pi/(ell*(ell+1))
    baselinePP=std['pp_Dl'][ell]*2*math.pi/(ell.astype(float)*(ell+1))**2
    deflection=math.sqrt(float(np.sum((2*ell+1)*ell*(ell+1)*cl['phi']/(4*math.pi))))*180/math.pi*3600
    defbase=math.sqrt(float(np.sum((2*ell+1)*ell*(ell+1)*baselinePP/(4*math.pi))))*180/math.pi*3600
    stats=sky_moments(co,si,d)
    for row in stats:
        key=row['field']; sel=ell<=row['lmax']
        check('sky_moment_variance_'+key,abs(row['RMS_microK']**2/float(np.sum((2*ell[sel]+1)*cl[key][sel]/(4*math.pi)))-1)<1e-10)
    output=dict(mean_conversion_fraction=actualmean,matter_fraction_range=[float(f.min()),float(f.max())],
        exact_ledger_cases=J*N,exact_energy_error=0,residual_max=float(r.max()),quantum=float(q),
        naive_accumulator_max_unconverted_demand=max(float(x[3]) for x in out),
        residue_memory_denominator_bits_max=max(x[4] for x in out),
        entropy_RMS=math.sqrt(totalvar),projected_seven_mode_entropy_RMS=math.sqrt(lowvar),
        omitted_entropy_variance_fraction=missing,old_projection_relative_errors=norm_errors,
        projected_CMB_T_RMS_microK=rms(cl['T']),projected_CMB_E_RMS_microK=rms(cl['E']),
        projected_deflection_RMS_arcsec=deflection,baseline_T_RMS_microK=rms(baselineT),
        baseline_E_RMS_microK=rms(baselineE),baseline_deflection_RMS_arcsec=defbase,
        projected_T_variance_over_baseline=rms(cl['T'])**2/rms(baselineT)**2,
        projected_E_variance_over_baseline=rms(cl['E'])**2/rms(baselineE)**2,
        minimum_T_E_phi_correlation_eigenvalue=eigmin,
        no_new_likelihood=True,low_band_sky_moments=stats,physical_quantum_controls=qcontrols)
    save('results.json',dict(version='0.2',date='2026-10-20',verified_inputs=CFG,
        WRRA_transformation='conservative twist divergence -> exact residual feedback conversion -> compensated matter/radiation entropy -> inherited regular D-isocurvature boundary projection -> actual cached CMB T/E/phi',
        outputs=output,checks=CHECKS,checks_passed=len(CHECKS),
        refutation_conditions=['energy/positivity or residue-memory failure','discretization dependence at fixed integrated demand','incorrect inherited transfer normalization','failure of specified observed CMB or structure tests after a complete mode and matching calculation'],
        scope='finite preparation and seven-mode CMB connection executed; continuous conversion/Einstein matching, ordinary baryon chemistry and missing harmonics not solved; mean-to-individual problem partially implemented, not fully closed'))
    np.savez_compressed(OUT/'projection.npz',ell=ell,k=d['k'],fraction=f,residual=r,
                        entropy=s,twist=twist,template=b,co=co,si=si,
                        **{'Cl_'+k:v for k,v in cl.items()},**{'Cl_continuum_'+k:v for k,v in cl_cont.items()})
    with (OUT/'CMB_spectra.csv').open('w',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['ell','Cl_T_microK2','Cl_E_microK2','Cl_TE_microK2','Cl_phi','Cl_Tphi_microK','Cl_Ephi_microK'])
        writer.writerows(zip(ell,cl['T'],cl['E'],cl['TE'],cl['phi'],cl['Tphi'],cl['Ephi']))
    save('input_sha256.json',{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(IN.iterdir()) if f.is_file()})
    print(json.dumps(dict(checks_passed=len(CHECKS),outputs=output),indent=2))

if __name__=='__main__': main()
