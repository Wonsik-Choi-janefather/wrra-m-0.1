"""Offline finite-response witnesses. Python 3, NumPy, SciPy, Matplotlib.
All numerical data are constructed model data, not observations.
"""
from pathlib import Path
import json, numpy as np
from scipy.special import logsumexp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
checks={}
def check(name,value,tol=1e-10):
    value=float(value); checks[name]={'residual':value,'tolerance':tol,'pass':abs(value)<=tol}
def stats(p,b):
    m=p@b; c=(b-m).T@(p[:,None]*(b-m)); return m,c
def response(p,b,x,beta=1,eps=1):
    logs=np.log(p)-beta*eps*(b@x); z=logsumexp(logs)
    q=np.exp(logs-z); m,c=stats(q,b)
    return -z/beta,eps*m,-beta*eps**2*c

def main():
    # Actual even-composite response f_D from v1.8, retaining its N and alpha.
    n=np.array([4.,6.,8.]); N=1015000; alpha=1.8996877935161325
    w=n**(-alpha); w/=w.sum(); f=1+.25*np.log(n)/np.log(N)
    # Exact null direction t annihilates sum(t) and sum(f*t).
    t=np.array([f[1]-f[2],f[2]-f[0],f[0]-f[1]])
    delta=t/w; delta*=.2/np.max(np.abs(delta)); z0=.1
    pa=np.column_stack((.5+z0+delta,.5-z0-delta))
    pb=np.column_stack((.5+z0-delta,.5-z0+delta))
    p=(w[:,None]*pa).ravel(); q=(w[:,None]*pb).ravel()
    assert np.all(pa>0) and np.all(pb>0)
    check('conditional_normalization_A',np.max(abs(pa.sum(axis=1)-1)))
    check('conditional_normalization_B',np.max(abs(pb.sum(axis=1)-1)))
    b=np.column_stack((np.zeros(3),2*f)).ravel()[:,None]
    ma,ca=stats(p,b); mb,cb=stats(q,b)
    check('same_carrier_marginal',np.max(abs(w@pa-w@pb)))
    check('same_weighted_D_operator',np.max(abs((w*f)@pa-(w*f)@pb)))
    check('same_load',ma[0]-mb[0]); check('null_sum',w@delta);check('null_f',(w*f)@delta)
    difference=-8*np.sum(w*f*f*delta)
    check('covariance_gap_identity',ca[0,0]-cb[0,0]-difference)
    assert abs(difference)>1e-8
    cca=np.sum(w*f*f*(1-4*(z0+delta)**2)); ccb=np.sum(w*f*f*(1-4*(z0-delta)**2))
    check('clamped_covariance_gap',(cca-ccb)-2*z0*difference)
    # Field bias cancels reference mean; response is evaluated at x=0.
    k0=2.; eps=1.; beta=1.
    ra=1/(k0-ca[0,0]); rb=1/(k0-cb[0,0])
    h=1e-5
    for label,prior in [('A',p),('B',q)]:
        _,g,H=response(prior,b,np.array([0.]))
        gp=response(prior,b,np.array([h]))[1];gm=response(prior,b,np.array([-h]))[1]
        check('gradient_difference_'+label,((gp-gm)/(2*h)-H)[0,0],1e-8)
    def clamped_grad(rows,x):
        return sum(w[i]*response(rows[i],np.array([[0.],[2*f[i]]]),np.array([x]))[1][0] for i in range(3))
    for lab,rows,cc in [('A',pa,cca),('B',pb,ccb)]:
        check('clamped_gradient_difference_'+lab,(clamped_grad(rows,h)-clamped_grad(rows,-h))/(2*h)+cc,1e-8)
    # Same complete global load distribution, distinct clamped response.
    rflat=np.array([[.5,.5],[.5,.5]]);rsplit=np.array([[.8,.2],[.2,.8]])
    pairb=np.array([[0.],[2.]])
    check('same_global_load_distribution',np.max(abs(rflat.mean(axis=0)-rsplit.mean(axis=0))))
    cflat=sum(stats(row,pairb)[1][0,0] for row in rflat)/2
    csplit=sum(stats(row,pairb)[1][0,0] for row in rsplit)/2
    check('clamped_contract_gap',cflat-csplit-.36)
    # Same entropy and mean, different susceptibility, same prescribed load alphabet.
    sb=np.array([-2.,-1.,1.,2.])[:,None]
    sp=np.array([.1,.4,.4,.1]);sq=sp[::-1].copy() # overwrite with permutation changing second moments
    sq=np.array([.4,.1,.1,.4])
    check('same_entropy',-sp@np.log(sp)+sq@np.log(sq))
    check('same_entropy_example_mean',(sp@sb-sq@sb).item())
    sv=[float(stats(v,sb)[1][0,0]) for v in (sp,sq)]
    # Two grounded graph nodes: complete spectrum of relative response.
    K=np.array([[2.,-1.],[-1.,2.]])
    bb=np.array([[1.,0.],[-1.,0.],[0.,2.],[0.,-2.]])
    pp=np.ones(4)/4;C=stats(pp,bb)[1]
    ev,U=np.linalg.eigh(K);km=(U*ev**(-.5))@U.T
    lam=np.linalg.eigvalsh(km@C@km);threshold=1/lam.max()
    eta=.3;Ke=K-eta*C;R=np.linalg.inv(Ke)
    assert np.linalg.eigvalsh(Ke).min()>0
    assert np.linalg.eigvalsh(K-1.01*threshold*C).min()<0
    gains=1/(1-eta*lam)
    for u in np.eye(2):
        assert u@R@u >= u@np.linalg.inv(K)@u
    check('matrix_inverse',np.linalg.norm(Ke@R-np.eye(2)))
    # Schur complement includes an internal source and energy constant.
    K3=np.array([[3.,-1.,-.5],[-1.,3.,-1.],[-.5,-1.,2.5]])
    j=np.array([.3,-.2,.7]);A=K3[:2,:2];B=K3[:2,2:];D=K3[2:,2:]
    S=A-B@np.linalg.solve(D,B.T);jt=j[:2]-B@np.linalg.solve(D,j[2:]);constant=-.5*j[2:]@np.linalg.solve(D,j[2:])
    full=-np.linalg.solve(K3,j); reduced=-np.linalg.solve(S,jt)
    check('schur_response',np.linalg.norm(full[:2]-reduced))
    ef=.5*full@K3@full+j@full;er=.5*reduced@S@reduced+jt@reduced+constant
    check('schur_energy',ef-er)
    wrong=-np.linalg.solve(S,j[:2]);assert np.linalg.norm(wrong-full[:2])>.01
    # Duplicate-load class exact partition, including finite nonzero fields.
    bd=np.array([[-1.],[-1.],[2.],[2.],[2.]])
    pd=np.array([.1,.2,.1,.25,.35]);cg=np.array([.3,.7]);bg=np.array([[-1.],[2.]])
    for i,x in enumerate(np.linspace(-1,1,9)):
        check('load_class_partition_'+str(i),response(pd,bd,np.array([x]))[0]-response(cg,bg,np.array([x]))[0])
    # Single energy function pressure. E_a=eps*v^(-1/3)*b_a*x, K=k*v^(1/3).
    v=1.3;xx=.2;k=2.;bp=np.array([0.,1.,2.]);pr=np.array([.2,.5,.3])
    def FV(vv):
        E=vv**(-1/3)*bp*xx
        return .5*k*vv**(1/3)*xx**2-logsumexp(np.log(pr)-E)
    E=v**(-1/3)*bp*xx;post=np.exp(np.log(pr)-E-logsumexp(np.log(pr)-E))
    P=-k/6*v**(-2/3)*xx**2+(post@E)/(3*v)
    check('isothermal_pressure',-(FV(v+h)-FV(v-h))/(2*h)-P,1e-9)
    # Finite reference measure cannot fix dimensional scale.
    scale=7.;check('dimensional_rescaling',np.linalg.norm(np.linalg.inv(scale*Ke)-R/scale))
    output={'witness':{'addresses':n.tolist(),'weights':w.tolist(),'f_D':f.tolist(),'delta':delta.tolist(),'conditional_A':pa.tolist(),'conditional_B':pb.tolist(),'load':ma[0],'variance_A':ca[0,0],'variance_B':cb[0,0],'gap':difference,'clamped_variance_A':cca,'clamped_variance_B':ccb,'response_A':ra,'response_B':rb},'clamped_contract':{'flat':cflat,'split':csplit},'entropy_example':{'entropy':float(-sp@np.log(sp)),'variances':sv},'graph':{'generalized_covariance_eigenvalues':lam.tolist(),'eta_critical':threshold,'eta':eta,'gains':gains.tolist(),'response':R.tolist()},'schur':{'correct':reduced.tolist(),'wrong':wrong.tolist(),'constant':float(constant)},'checks':checks,'all_pass':all(c['pass'] for c in checks.values())}
    (ROOT/'results.json').write_text(json.dumps(output,indent=2))
    fig,ax=plt.subplots(1,2,figsize=(9,3.5))
    etas=np.linspace(0,.9*threshold,150)
    for i,l in enumerate(lam): ax[0].plot(etas,1/(1-etas*l),label=f'Mode {i+1}')
    ax[0].set(xlabel='Dimensionless feedback strength',ylabel='Relative response gain');ax[0].legend();ax[0].grid(alpha=.2)
    xs=np.linspace(-.8,.8,101)
    diffs=np.array([response(p,b,np.array([x]))[0]-response(q,b,np.array([x]))[0] for x in xs])
    ax[1].plot(xs,1e6*diffs,label='Exact A minus B')
    ax[1].plot(xs,-.5*1e6*difference*xs**2,'--',label='Quadratic response')
    ax[1].set(xlabel='Dimensionless probe field',ylabel='Free energy difference (millionths)');ax[1].legend();ax[1].grid(alpha=.2)
    fig.tight_layout();fig.savefig(ROOT/'response_figure.png',dpi=250);fig.savefig(ROOT/'Fig1.pdf');plt.close(fig)
    assert output['all_pass'];print(json.dumps(output,indent=2))
if __name__=='__main__':main()
