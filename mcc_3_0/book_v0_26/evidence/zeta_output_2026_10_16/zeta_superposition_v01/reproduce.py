"""Finite, conditional Mellin-phase interference on the MCC prime CRT space.
No finite Dirichlet sum is identified with analytically continued zeta.
Run: OPENBLAS_NUM_THREADS=1 python3 reproduce.py
"""
import json, math
from pathlib import Path
import numpy as np
import mpmath as mp

ROOT=Path(__file__).resolve().parent
N=1015000
SHAPE=(213,65,77)
M=math.prod(SHAPE)
C=70
ALPHA=1.8996877935161325

def main():
    mp.mp.dps=35
    zeros=[mp.zetazero(k) for k in range(1,C+1)]
    gamma=np.array([float(z.imag) for z in zeros])
    np.savetxt(ROOT/'zero_heights.csv',gamma,header='gamma',comments='')
    zero_residual=max(float(abs(mp.zeta(z))) for z in zeros)
    n=np.arange(1,N+1)
    prime=np.ones(N+1,dtype=bool);prime[:2]=False
    for p in range(2,math.isqrt(N)+1):
        if prime[p]:prime[p*p::p]=False
    omega=np.zeros(N+1,dtype=np.int8)
    for p in np.flatnonzero(prime):omega[p::p]+=1
    keep=omega[n]>=2
    ids=n[keep]
    logn=np.log(ids)
    index=np.ravel_multi_index(tuple(ids%m for m in SHAPE),SHAPE)
    assert len(np.unique(index))==len(ids)
    lam=np.zeros(SHAPE)
    for axis,m in enumerate(SHAPE):
        shape=[1,1,1];shape[axis]=m
        lam+=(4*np.sin(np.pi*np.arange(m)/m)**2).reshape(shape)
    evolution=np.exp(-1j*lam) # dimensionless source parameter tau=1, NOT seconds
    def spatial(v):
        a=np.zeros(M,dtype=complex);a[index]=v
        return np.fft.ifftn(evolution*np.fft.fftn(a.reshape(SHAPE),norm='ortho'),norm='ortho')
    def kfilter(gammas):
        k=np.zeros(len(ids),complex)
        for g in gammas:k+=np.exp(-1j*g*logn)/len(gammas)
        return k
    k=kfilter(gamma)
    shifted=kfilter(gamma+.5)
    spaced=kfilter(np.linspace(gamma[0],gamma[-1],C))
    rng=np.random.default_rng(20261016)
    offsets=rng.uniform(-np.pi,np.pi,C)
    random_phase=np.zeros(len(ids),complex)
    for g,o in zip(gamma,offsets):random_phase+=np.exp(1j*o-1j*g*logn)/C
    rows={}
    checks={}
    for name,alpha in [('uniform',0.),('inherited_alpha',ALPHA)]:
        seed=ids.astype(float)**(-alpha/2)
        seed/=np.linalg.norm(seed)
        out=spatial(k*seed)
        intensity=abs(out)**2
        success=float(intensity.sum())
        held=float(np.sum((1-abs(k)**2)*abs(seed)**2))
        conditional=intensity/success
        # Independent incoherent mixture; no arbitrary phase-sensitive rescaling.
        incoherent=np.zeros(SHAPE)
        for j,g in enumerate(gamma):
            mode=spatial(seed*np.exp(-1j*g*logn))
            incoherent+=abs(mode)**2/C
            if name=='uniform' and j%20==0:print('modes',j+1,flush=True)
        cases={}
        for label,kk in [('shifted_heights_gate_forced_open',shifted),('equally_spaced_gate_forced_open',spaced),('random_relative_phase',random_phase)]:
            a=spatial(kk*seed);i=abs(a)**2;p=float(i.sum())
            cases[label]={'success_probability':p,'conditional_intensity_TV_from_zero_coherent':float(.5*np.sum(abs(i/p-conditional)))}
        # Test FFT/inverse and linear synthesis on a nontrivial 3-mode subproblem.
        a=np.array([.2+.1j,-.3j,.5]);direct=np.zeros(SHAPE,complex);address=np.zeros(len(ids),complex)
        for coef,g in zip(a,gamma):
            v=seed*np.exp(-1j*g*logn);address+=coef*v;direct+=coef*spatial(v)
        synthesis_error=float(np.max(abs(direct-spatial(address))))
        inverse=np.fft.ifftn(np.conj(evolution)*np.fft.fftn(out,norm='ortho'),norm='ortho').ravel()
        inverse_error=float(np.max(abs(inverse[index]-k*seed)))
        gram12=np.sum(abs(seed)**2*np.exp(-1j*(gamma[1]-gamma[0])*logn))
        rows[name]={'alpha':alpha,'coherent_success_probability':success,'hold_probability':held,
            'norm_conservation_error':abs(success+held-1),
            'incoherent_total_probability':float(incoherent.sum()),
            'coherent_vs_incoherent_conditional_TV':float(.5*np.sum(abs(conditional-incoherent))),
            'gram_first_two_modes_abs':float(abs(gram12)),
            'synthesis_max_error':synthesis_error,'inverse_max_error':inverse_error,
            'controls':cases}
        checks[name+'_conservation']=abs(success+held-1)<1e-12
        checks[name+'_incoherent_norm']=abs(float(incoherent.sum())-1)<1e-12
        checks[name+'_linear_synthesis']=synthesis_error<1e-12
        checks[name+'_inverse']=inverse_error<1e-12
        checks[name+'_interference_visible']=rows[name]['coherent_vs_incoherent_conditional_TV']>1e-4
        # Export exact marginal probabilities, not a physical mass density.
        for axis in range(3):
            others=tuple(i for i in range(3) if i!=axis)
            np.savetxt(ROOT/f'{name}_axis{axis}_probabilities.csv',np.column_stack([np.arange(SHAPE[axis]),conditional.sum(axis=others),incoherent.sum(axis=others)]),delimiter=',',header='coordinate,coherent_conditional,incoherent',comments='')
    checks.update({'zero_residual':zero_residual<1e-25,'correct_selected_count':len(ids)==935155,
        'contraction':float(abs(k).max())<=1+1e-12,
        'shift_common_phase_identity':float(np.max(abs(shifted-k*np.exp(-.5j*logn))))<1e-12,
        'permutation_invariance':float(np.max(abs(k-kfilter(gamma[::-1]))))<1e-12})
    result={'N':N,'M':M,'shape':SHAPE,'zero_count':C,'selected_count':len(ids),
        'max_zeta_residual_high_precision':zero_residual,
        'max_filter_modulus':float(abs(k).max()),'rows':rows,'checks':checks,
        'all_checks_pass':all(checks.values()),
        'scope':'conditional finite Mellin-phase superposition; geometry and coherent combining are specified; no derivation of physical 3D or unique zero-to-Laplacian-eigenmode map'}
    (ROOT/'results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2),flush=True)
    assert all(checks.values())

if __name__=='__main__':main()
