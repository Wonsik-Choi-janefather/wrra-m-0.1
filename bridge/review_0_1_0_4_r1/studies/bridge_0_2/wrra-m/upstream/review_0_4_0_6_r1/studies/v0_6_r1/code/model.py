"""Complete L=0 oscillator shells, permutation projection and bounded mixing.

The dimensionless spatial modes are coupled Laguerre/Legendre polynomials
times the six-dimensional Gaussian. No tensor-grid spatial label is assigned
an empirical radius without evaluating the actual point-charge operator.
"""
import math
import numpy as np
from scipy.special import roots_genlaguerre, roots_legendre, roots_jacobi, eval_genlaguerre, eval_legendre, gammaln
from scipy.linalg import eigh
import inherited_v0_4 as v4

def labels(K):
    return [(l,nx,ny) for s in range(K+1) for l in range(s+1) for nx in range(s-l+1) for ny in [s-l-nx]]

def quadrature(nr,na):
    # s=u+v ~ Gamma(3), t=u/s ~ Beta(3/2,3/2), z uniform[-1,1].
    # A hypercentral denominator is integrated radially, so exact angular
    # permutation covariance is preserved at every radial quadrature order.
    s,ws=roots_genlaguerre(nr,2.);a,wt=roots_jacobi(na,.5,.5);z,wz=roots_legendre(na)
    ss,tt,angle=np.meshgrid(s,(a+1)/2,z,indexing='ij')
    wr,wpart,wa=np.meshgrid(ws/2,wt*2/math.pi,wz/2,indexing='ij')
    return (ss*tt).ravel(),(ss*(1-tt)).ravel(),angle.ravel(),(wr*wpart*wa).ravel()

def functions(lab,u,v,z):
    cols=[]
    for l,nx,ny in lab:
        lognorm=.5*(math.log(2*l+1)+gammaln(nx+1)+gammaln(ny+1)+2*gammaln(1.5)-gammaln(nx+l+1.5)-gammaln(ny+l+1.5))
        cols.append(math.exp(lognorm)*(u*v)**(l/2)*eval_legendre(l,z)*eval_genlaguerre(nx,l+.5,u)*eval_genlaguerre(ny,l+.5,v))
    return np.column_stack(cols)

def sf_triplet():
    sf,blocks=v4.old.finite_states();s=sf['state_basis']
    Fp=np.column_stack([v4.state_from_rows(s['proton_S'],'S')]+[v4.state_from_rows(s['proton_M'],'E'+str(a+1))*math.sqrt(2) for a in range(2)])
    Fn=np.column_stack([v4.state_from_rows(s['neutron_S'],'S')]+[v4.state_from_rows(s['neutron_M'],'E'+str(a+1))*math.sqrt(2) for a in range(2)])
    T=[]
    for a in (1,2):
        t=np.zeros((3,3));t[0,a]=t[a,0]=1/math.sqrt(2);T.append(t)
    tp=np.array([[0,1],[0,0]]);sz=np.diag([1,-1])
    Az=sum(v4.old.parent.at_slot(np.kron(tp,sz),i) for i in range(3))
    A=(Fp.T@Az@Fn).real
    Qslots={n:[(F.T@v4.old.parent.at_slot(np.diag([2/3,2/3,-1/3,-1/3]),i)@F).real for i in range(3)] for n,F in [('proton',Fp),('neutron',Fn)]}
    return sf,blocks,Fp,Fn,T,A,Qslots

def build(K,nr=32,na=18,lam=1.):
    sf,blocks,Fp,Fn,T,A,Qslots=sf_triplet()
    lab=labels(K);n=len(lab);shell=np.array([sum(x) for x in lab])
    u,v,z,w=quadrature(nr,na);c=np.sqrt(u*v)*z;s=u+v
    F=functions(lab,u,v,z);weighted=w[:,None]*F
    gram=F.T@weighted
    # The real Jacobi E pair is aligned with the inherited fixed spin-flavor E.
    X=np.column_stack(((u-v)/math.sqrt(3),-2*c/math.sqrt(3)))
    k=float(np.sum(w*np.sum(X*X,axis=1)/(1+lam*s))/2) if lam>0 else 1.
    spaceW=[F.T@(weighted*X[:,a,None]) for a in range(2)]
    spaceB=[F.T@(weighted*(X[:,a]/(1+lam*s)/k)[:,None]) for a in range(2)]
    W=sum(np.kron(t,m) for t,m in zip(T,spaceW))
    B=sum(np.kron(t,m) for t,m in zip(T,spaceB))
    J=np.array([[1,-1,0],[1/math.sqrt(3),1/math.sqrt(3),-2/math.sqrt(3)]])/math.sqrt(2)
    group=[];spatial_reps=[]
    for r in sf['spatial_representations']:
        inv=np.argsort(r['permutation']);j=J@np.eye(3)[inv]@J.T
        a,b=j[0];d,e=j[1]
        uu=np.maximum(a*a*u+b*b*v+2*a*b*c,1e-30)
        vv=np.maximum(d*d*u+e*e*v+2*d*e*c,1e-30)
        cc=a*d*u+b*e*v+(a*e+b*d)*c
        zz=np.clip(cc/np.sqrt(uu*vv),-1.,1.)
        R=F.T@(w[:,None]*functions(lab,uu,vv,zz))
        R[np.abs(R)<1e-13]=0
        spatial_reps.append(R)
        sfR=Fp.T@v4.old.perm_matrix(r['permutation'])@Fp
        group.append(np.kron(sfR,R))
    P=sum(group)/6;P=(P+P.T)/2
    # A shellwise fixed basis avoids arbitrary degenerate eigenvector phases.
    columns=[];column_shells=[]
    for ss in range(K+1):
        idx=np.array([a*n+i for a in range(3) for i in range(n) if shell[i]==ss])
        pp=P[np.ix_(idx,idx)];rank=int(round(np.trace(pp)))
        if rank:
            q=v4.old.fixed_basis(pp,rank)
            for j in range(rank):
                col=np.zeros(3*n);col[idx]=q[:,j];columns.append(col);column_shells.append(ss)
    Q=np.column_stack(columns)
    norm=(Q.T@Q);H0=np.diag(np.tile(shell,3))
    Qrho=Q.T@np.kron(np.eye(3),F.T@(weighted*s[:,None]))@Q
    Rp=[]
    spatialR=[u/2+v/6+c/math.sqrt(3),u/2+v/6-c/math.sqrt(3),2*v/3]
    Rsp=[F.T@(weighted*r[:,None]) for r in spatialR]
    for name in ('proton','neutron'):
        Rp.append(Q.T@sum(np.kron(charge,rad) for charge,rad in zip(Qslots[name],Rsp))@Q)
    Aret=Q.T@np.kron(A,np.eye(n))@Q
    Qret=Q.T@np.kron(np.diag([0.,1.,1.]),np.eye(n))@Q
    Svec=np.zeros(3*n);Svec[0]=1.
    Ec=F.T@(w[:,None]*X)
    Mvec=np.concatenate((np.zeros(n),Ec[:,0],Ec[:,1]))/math.sqrt(2)
    reference=np.column_stack((Q.T@Svec,Q.T@Mvec))
    bare=Q.T@W@Q;bounded=Q.T@B@Q
    checks={
      'spatial_gram':np.linalg.norm(gram-np.eye(n))<3e-10,
      'permutation_projector_idempotent':np.linalg.norm(P@P-P)<3e-10,
      'retained_basis_orthonormal':np.linalg.norm(norm-np.eye(len(columns)))<3e-10,
      'all_retained_states_permutation_symmetric':max(np.linalg.norm(g@Q-Q) for g in group)<3e-10,
      'bare_link_hermitian':np.linalg.norm(bare-bare.T)<3e-10,
      'bounded_link_hermitian':np.linalg.norm(bounded-bounded.T)<3e-10,
      'bare_link_permutation_invariant':max(np.linalg.norm(g@W-W@g) for g in group)<3e-9,
      'bounded_link_permutation_invariant':max(np.linalg.norm(g@B-B@g) for g in group)<3e-9,
      'point_radius_permutation_invariant':max(np.linalg.norm(g@sum(np.kron(charge,rad) for charge,rad in zip(Qslots['proton'],Rsp))-sum(np.kron(charge,rad) for charge,rad in zip(Qslots['proton'],Rsp))@g) for g in group)<3e-9,
      'proton_charge_one_neutron_zero':np.linalg.norm(sum(Qslots['proton'])-np.eye(3))<1e-12 and np.linalg.norm(sum(Qslots['neutron']))<1e-12,
      'axial_block_uses_same_E_weight':np.linalg.norm(Aret-(5/3*np.eye(len(columns))-4/3*Qret))<3e-10,
      'old_two_state_bare_block_recovered':np.linalg.norm(reference.T@bare@reference-np.array([[0,1],[1,0]]))<3e-10,
      'old_two_state_bounded_block_recovered':np.linalg.norm(reference.T@bounded@reference-np.array([[0,1],[1,0]]))<3e-10,
    }
    return {'K':K,'labels':lab,'spatial_dimension':n,'retained_dimension':len(columns),'column_shells':np.array(column_shells),
      'h0':Q.T@H0@Q,'bare':(bare+bare.T)/2,'bounded':(bounded+bounded.T)/2,'axial':Aret,'Eweight':Qret,'rho_squared':Qrho,
      'radius_proton':(Rp[0]+Rp[0].T)/2,'radius_neutron':(Rp[1]+Rp[1].T)/2,'reference':reference,
      'normalization_k':k,'bounded_norm_ceiling':1/(math.sqrt(6)*lam*k) if lam>0 else None,
      'checks':{k:bool(v) for k,v in checks.items()},'blocks':blocks}

def restrict(model,K):
    idx=np.flatnonzero(model['column_shells']<=K)
    m=dict(model);m['K']=K;m['retained_dimension']=len(idx);m['spatial_dimension']=len(labels(K));m['column_shells']=model['column_shells'][idx]
    for key in ('h0','bare','bounded','axial','Eweight','rho_squared','radius_proton','radius_neutron'):
        m[key]=model[key][np.ix_(idx,idx)]
    m['reference']=model['reference'][idx]
    return m

def diagonalize(model,x,link='bounded'):
    H=model['h0']-x*model[link];e,vec=eigh(H)
    g=vec[:,0]
    if np.dot(model['reference'][:,0],g)<0:g=-g
    return H,e,vec,g

def solve_x(model,q_target):
    from scipy.optimize import brentq
    def q(x):
        _,_,_,g=diagonalize(model,x)
        return float(g@model['Eweight']@g)
    lo,hi=0.,1.
    while q(hi)<q_target:
        hi*=2
        if hi>128:raise ValueError('target mixed weight not reached')
    return brentq(lambda x:q(x)-q_target,lo,hi,xtol=5e-14)
