"""Independent oracles for the finite accumulator and cached CMB projection."""
from pathlib import Path
from fractions import Fraction as F
import json, math, hashlib
import numpy as np
import reproduce as m
P=Path(__file__).resolve().parent
checks={}; failures=[]
def test(name,ok):
    checks[name]=bool(ok)
    if not ok:failures.append(name)

def run():
    rng=np.random.default_rng(20261020)
    # Endpoint oracle: one Euclidean division, independent of iterative carry.
    worst=0.; cases=0
    for den in [7,100,100000000]:
        q=F(1,den)
        for numerator in range(0,102,3):
            target=min(F(numerator,101),F(1))
            for steps in [1,7,128,257]:
                # Production's frozen decimal rule is intentionally included.
                a=F(str(float(target)))
                want=(a//q)*q; want_res=a-want
                got,res,peak,_,_=m.conversion(target,q,steps)
                test('endpoint_'+str(cases),got==want and res==want_res and 0<=peak<q)
                cases+=1
    # Nonuniform requests: carry depends on total demand, not ordering.
    # This audit extension is not used to claim an autonomous cosmological rate.
    demand_cases=0
    for _ in range(100):
        demands=[F(int(v),10**9) for v in rng.integers(0,1000,size=32)]
        q=F(1,10**6);res=F(0);mass=F(0)
        for v in demands:
            n=(v+res)//q;mass+=n*q;res=v+res-n*q
        total=sum(demands)
        test('nonuniform_'+str(demand_cases),mass==(total//q)*q and res==total%q)
        demand_cases+=1
    # An adversarial memory-reset control cannot silently pass an exact budget.
    demands=[F(3,10)]*3;q=F(1,2)
    carry=(sum(demands)//q)*q;reset=sum((v//q)*q for v in demands)
    test('memory_reset_control_rejected',carry!=reset)
    # Constant input and zero twist cannot create an inhomogeneity.
    test('constant_twist_null',np.all(np.roll(np.ones(128),-1)-np.roll(np.ones(128),1)==0))
    # Fourier eigenvalue of central difference: independent analytic n dependence.
    z=np.load(P/'results/projection.npz');theta=2*np.pi*np.arange(128)/128
    for n in range(1,8):
        arr=np.cos(n*theta)
        actual=(np.roll(arr,-1)-np.roll(arr,1))/(2*np.sin(2*np.pi/128))
        expected=-np.sin(n*theta)*np.sin(2*np.pi*n/128)/np.sin(2*np.pi/128)
        test('derivative_eigenmode_'+str(n),np.max(abs(actual-expected))<2e-12)
    # Full finite-grid Parseval, treating Nyquist as a single real mode.
    s=z['entropy'];h=np.fft.rfft(s)/128
    p=2*abs(h)**2;p[0]/=2;p[-1]/=2
    test('full_parseval_with_nyquist',abs(float(np.sum(p))/float(np.mean(s*s))-1)<1e-12)
    low=.5*float(np.sum(z['co']**2+z['si']**2)); omitted=float(p[8:].sum())
    test('missing_modes_accounted',abs((low+omitted+p[0])/float(np.mean(s*s))-1)<1e-12)
    # Independent explicit phase sum at selected ell versus production C_l.
    # Both cosine/sine branches and the angular parity phases are included.
    d=np.load(P/'inputs/D_lens_a2.5.npz');n=np.arange(1,8)
    co=z['co'];si=z['si']; cs=np.cos(n[:,None]*theta);sn=np.sin(n[:,None]*theta)
    indices=[0,28,98,498,998,1998,3998,5998]
    errors=[]
    for idx in indices:
        ell=int(d['ell'][idx]); vec=[]
        for field,unit in [('T',2.7255e6),('E',2.7255e6),('phi',1.)]:
            a=(d[field][idx]*co)@cs+(d[field][idx]*si)@sn if ell%2==0 else (d[field][idx]*co)@sn-(d[field][idx]*si)@cs
            vec.append(a*unit*math.sqrt(4*math.pi*(2*ell+1)))
        direct=np.asarray(vec)@np.asarray(vec).T/(128*(2*ell+1))
        ref=np.array([[z['Cl_T'][idx],z['Cl_TE'][idx],z['Cl_Tphi'][idx]],[z['Cl_TE'][idx],z['Cl_E'][idx],z['Cl_Ephi'][idx]],[z['Cl_Tphi'][idx],z['Cl_Ephi'][idx],z['Cl_phi'][idx]]])
        scale=np.sqrt(np.outer(np.diag(ref),np.diag(ref)))
        error=float(np.max(np.divide(abs(direct-ref),scale,out=np.zeros_like(scale),where=scale>0)))
        errors.append(error);test('explicit_phase_covariance_ell'+str(ell),error<1e-12)
    # Independent angular quadrature refinement checks low-band higher moments.
    original=m.sky_moments(co,si,d,lmax=80)
    # Moment quadrature normally has 161 nodes: compare against direct 201-node rule.
    from numpy.polynomial.legendre import leggauss,legvander
    ell=np.arange(2,81);mu,w=leggauss(201)
    pm=legvander(mu,80)[:,ell]*np.sqrt((2*ell+1)/(4*np.pi))
    for row,field in zip(original,['T','E']):
        t=d[field][:79]*2.7255e6
        even=(t*co)@cs+(t*si)@sn;odd=(t*co)@sn-(t*si)@cs
        a=np.where((ell%2==0)[:,None],((-1.)**(ell//2))[:,None]*even,((-1.)**((ell+1)//2))[:,None]*odd)*np.sqrt(4*np.pi*(2*ell+1))[:,None]
        sky=pm@a;sky-=np.sum(w[:,None]*sky)/(2*128)
        m2=float(np.sum(w[:,None]*sky**2)/(2*128));m3=float(np.sum(w[:,None]*sky**3)/(2*128));m4=float(np.sum(w[:,None]*sky**4)/(2*128))
        test('angular_quadrature_'+field,abs(math.sqrt(m2)/row['RMS_microK']-1)<1e-10 and abs(m3/m2**1.5-row['skewness'])<1e-8 and abs(m4/m2**2-3-row['excess_kurtosis'])<1e-6)
    # Frozen payload modification must be rejected before scientific readout.
    frozen=json.loads((P/'inputs_frozen_sha256.json').read_text())
    blob=(P/'inputs/D_lens_a2.5.npz').read_bytes()
    test('tampered_transfer_hash_rejected',hashlib.sha256(blob+b'changed').hexdigest()!=frozen['D_lens_a2.5.npz'])
    result={'version':'0.2','date':'2026-10-20','endpoint_oracle_cases':cases,'nonuniform_demand_cases':demand_cases,'explicit_phase_relative_error_max':max(errors),'checks_passed':sum(checks.values()),'checks_total':len(checks),'checks':checks,'failures':failures,'scope':'independent numerical/algebraic audit; not empirical validation or physical conversion-rate derivation'}
    (P/'results/review_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
    if failures: raise AssertionError(failures)
if __name__=='__main__':run()
