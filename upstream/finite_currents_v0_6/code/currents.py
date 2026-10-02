"""Same-state Breit monopole form factors and a disclosed charge completion.

The inherited point density was a Sachs-radius ansatz, not a Dirac density.
We preserve that definition, add one zero-charge isovector counterterm and
then convert Sachs to Dirac/Pauli. This avoids blindly adding a Foldy radius.
"""
import math
import numpy as np
from scipy.special import spherical_jn
import model

HC=.1973269804 # GeV fm; declared unit conversion

def projected_basis(m,nr,na):
    K=m['K'];lab=model.labels(K);n=len(lab)
    u,v,z,w=model.quadrature(nr,na);c=np.sqrt(u*v)*z
    F=model.functions(lab,u,v,z);sf,_,Fp,Fn,_,_,Qslots=model.sf_triplet()
    J=np.array([[1,-1,0],[1/math.sqrt(3),1/math.sqrt(3),-2/math.sqrt(3)]])/math.sqrt(2)
    reps=[]
    for r in sf['spatial_representations']:
        j=J@np.eye(3)[np.argsort(r['permutation'])]@J.T;a,b=j[0];d,e=j[1]
        uu=np.maximum(a*a*u+b*b*v+2*a*b*c,1e-30);vv=np.maximum(d*d*u+e*e*v+2*d*e*c,1e-30)
        zz=np.clip((a*d*u+b*e*v+(a*e+b*d)*c)/np.sqrt(uu*vv),-1,1)
        rr=F.T@(w[:,None]*model.functions(lab,uu,vv,zz));rr[np.abs(rr)<1e-13]=0
        reps.append(np.kron(Fp.T@model.v4.old.perm_matrix(r['permutation'])@Fp,rr))
    P=sum(reps)/6;P=(P+P.T)/2;shell=np.array([sum(x) for x in lab]);cols=[]
    for s in range(K+1):
        ii=np.array([a*n+i for a in range(3) for i in range(n) if shell[i]==s]);p=P[np.ix_(ii,ii)]
        rank=int(round(np.trace(p)))
        if rank:
            qq=model.v4.old.fixed_basis(p,rank)
            for j in range(rank):
                q=np.zeros(3*n);q[ii]=qq[:,j];cols.append(q)
    Q=np.column_stack(cols)
    if Q.shape[1]!=m['retained_dimension']:raise ValueError('inconsistent projection')
    r2=np.column_stack((u/2+v/6+c/math.sqrt(3),u/2+v/6-c/math.sqrt(3),2*v/3))
    return {'F':F,'weights':w,'Q':Q,'Fp':Fp,'Fn':Fn,'charge_slots':Qslots,'r2':np.maximum(r2,0),'nspace':n}

def prepare(m,p,g,inp,nr,na):
    c=projected_basis(m,nr,na);Q=c['Q'];F=c['F'];n=c['nspace'];w=c['weights']
    def amplitude(v):return F@(Q@v).reshape(3,n).T
    a=amplitude(g);b=amplitude(m['bounded']@g)
    c['g']=g;c['amp']=a;c['amp_link']=b;c['m']=m;c['p']=p
    mu_slot=np.diag([p['mu_u'],-p['mu_u'],p['mu_d'],-p['mu_d']])
    tp=np.array([[0,1],[0,0]]);sz=np.diag([1,-1]);vslots=[];aslots=[];mslots={}
    for i in range(3):
        vslots.append((c['Fp'].T@model.v4.old.parent.at_slot(np.kron(tp,np.eye(2)),i)@c['Fn']).real)
        aslots.append((c['Fp'].T@model.v4.old.parent.at_slot(np.kron(tp,sz),i)@c['Fn']).real)
    for name,Fsf in [('proton',c['Fp']),('neutron',c['Fn'])]:
        mslots[name]=[(Fsf.T@model.v4.old.parent.at_slot(mu_slot,i)@Fsf).real for i in range(3)]
    c['mag_slots']=mslots;c['vslots']=vslots;c['aslots']=aslots
    def density(slots):return np.column_stack([np.einsum('na,ab,nb->n',a,s,a) for s in slots])
    c['charge_density']={name:density(slots) for name,slots in c['charge_slots'].items()}
    c['mag_density']={name:density(slots) for name,slots in mslots.items()}
    c['weak_density']=density(vslots);c['axial_density']=density(aslots)
    c['norm_density']=np.sum(a*a,axis=1);c['link_density']=np.sum(a*b,axis=1)
    cp=float(g@m['radius_proton']@g);cn=float(g@m['radius_neutron']@g)
    rp=inp['radius_calibration']['proton_rms_charge_radius_fm'];rn=inp['charge_completion']['neutron_mean_square_radius_fm2']
    ell2=(rp*rp+rn)/(cp+cn)
    if ell2<=0:raise ValueError('incompatible common width')
    c['ell_fm']=math.sqrt(ell2);c['counterterm_radius_fm2']=rp*rp-ell2*cp
    c['mass_reference_GeV']=(inp['masses']['proton']+inp['masses']['neutron'])/2000
    c['magnetic_unit_scale']=(inp['masses']['proton']+inp['masses']['neutron'])/(2*inp['masses']['proton'])
    c['reference_regulator']=inp['charge_completion']['reference_regulator_in_ell']
    return c

def ground(c,Q2,regulator=None):
    if Q2<0:raise ValueError('spacelike Q2 must be nonnegative')
    p=c['p'];w=c['weights'];ell=c['ell_fm'];a=c['reference_regulator'] if regulator is None else regulator
    j=spherical_jn(0,math.sqrt(Q2)/HC*ell*np.sqrt(c['r2']));avg=np.mean(j,axis=1)
    extra=-Q2*c['counterterm_radius_fm2']/(6*HC*HC)*math.exp(-Q2*(a*ell)**2/(6*HC*HC))
    f=float(w@(c['norm_density']*avg));exchange=float(w@(c['link_density']*avg));tau=Q2/(4*c['mass_reference_GeV']**2)
    out={}
    for name,sign in [('proton',1),('neutron',-1)]:
        point=float(np.sum(w[:,None]*c['charge_density'][name]*j));GE=point+sign*extra
        moment=float(np.sum(w[:,None]*c['mag_density'][name]*j))+p['c0']*f+sign*p['eta']*p['x']*exchange
        GM=c['magnetic_unit_scale']*moment;F1=(GE+tau*GM)/(1+tau);F2=(GM-GE)/(1+tau)
        out[name]={'GE_point':point,'GE':GE,'GM_muN':moment,'GM_common_mass':GM,'F1':F1,'F2':F2}
    gvpoint=float(np.sum(w[:,None]*c['weak_density']*j));ga=float(np.sum(w[:,None]*c['axial_density']*j))
    out['weak']={'GV_point':gvpoint,'GEV':gvpoint+2*extra,'GAV':ga,'F1V':out['proton']['F1']-out['neutron']['F1'],'F2V':out['proton']['F2']-out['neutron']['F2']}
    out['Q2_GeV2']=Q2;return out

def full_charge(c,Q2,name):
    Q,F,w=c['Q'],c['F'],c['weights'];ell=c['ell_fm'];n=c['nspace']
    j=spherical_jn(0,math.sqrt(Q2)/HC*ell*np.sqrt(c['r2']))
    sp=[F.T@((w*j[:,i])[:,None]*F) for i in range(3)]
    op=Q.T@sum(np.kron(s,rr) for s,rr in zip(c['charge_slots'][name],sp))@Q
    sign=1 if name=='proton' else -1;a=c['reference_regulator']
    extra=-Q2*c['counterterm_radius_fm2']/(6*HC*HC)*math.exp(-Q2*(a*ell)**2/(6*HC*HC))
    return (op+op.T)/2+sign*extra*np.eye(len(c['g']))

def slopes(c):
    w=c['weights'];r2=c['r2']*c['ell_fm']**2;p=c['p'];extra=c['counterterm_radius_fm2'];scale=c['magnetic_unit_scale'];M=c['mass_reference_GeV'];zero=ground(c,0)
    out={}
    nr=float(w@(c['norm_density']*np.mean(r2,axis=1)));wr=float(w@(c['link_density']*np.mean(r2,axis=1)))
    for name,sign in [('proton',1),('neutron',-1)]:
        point=float(np.sum(w[:,None]*c['charge_density'][name]*r2));radius=point+sign*extra
        mr=float(np.sum(w[:,None]*c['mag_density'][name]*r2))+p['c0']*nr+sign*p['eta']*p['x']*wr
        gep=-radius/(6*HC*HC);gmp=-scale*mr/(6*HC*HC);f2=zero[name]['F2'];foldy=1.5*f2*HC*HC/(M*M)
        f1p=gep+f2/(4*M*M);f2p=gmp-gep-f2/(4*M*M)
        out[name]={'sachs_charge_radius_squared_fm2':radius,'point_radius_squared_fm2':point,'counterterm_signed_fm2':sign*extra,
            'dirac_radius_squared_fm2':radius-foldy,'foldy_radius_squared_fm2':foldy,
            'magnetic_radius_squared_fm2':mr/zero[name]['GM_muN'],'GE_derivative_GeV_minus2':gep,'GM_derivative_GeV_minus2':gmp,'F1_derivative_GeV_minus2':f1p,'F2_derivative_GeV_minus2':f2p}
    ar=float(np.sum(w[:,None]*c['axial_density']*r2));ga=zero['weak']['GAV']
    out['weak']={'F1V0':zero['weak']['F1V'],'F2V0':zero['weak']['F2V'],'GA0':ga,
        'F1V_prime':out['proton']['F1_derivative_GeV_minus2']-out['neutron']['F1_derivative_GeV_minus2'],
        'F2V_prime':out['proton']['F2_derivative_GeV_minus2']-out['neutron']['F2_derivative_GeV_minus2'],
        'GA_prime':-ar/(6*HC*HC),'axial_radius_squared_fm2':ar/ga}
    return out
