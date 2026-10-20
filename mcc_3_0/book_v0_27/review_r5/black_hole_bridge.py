"""WRRA black-hole boundary bridge. Run with Python 3, NumPy and SymPy.
GR metric and Bekenstein-Hawking laws are disclosed reverse-design inputs.
This computes a local stationary spherical patch, not a global cosmological
embedding, rotating collapse, evaporation dynamics or quantum microstate count.
"""
import json,math,platform
from pathlib import Path
import numpy as np
import sympy as s

c=299792458.;G=6.67430e-11;h=6.62607015e-34
hbar=h/(2*math.pi);kb=1.380649e-23;lp2=hbar*G/c**3

def state(M):
    if not math.isfinite(M) or M<=0:raise ValueError('positive finite gravitating mass required')
    rs=2*G*M/c**2;area=4*math.pi*rs**2
    S=kb*area/(4*lp2);T=hbar*c**3/(8*math.pi*G*kb*M)
    return dict(M_kg=M,energy_J=M*c*c,rs_m=rs,area_m2=area,entropy_J_K=S,
                temperature_K=T,entropy_bits=S/(kb*math.log(2)))

def absorb(M,E):
    state(M)
    if not math.isfinite(E) or E<0:raise ValueError('classical positive-energy absorption only')
    return M+E/c**2

def admit_radial_signal(x):
    if not math.isfinite(x) or x<=0:raise ValueError('r/rs must be positive')
    return 1-1/math.sqrt(x)>0

def check_merger(m1,m2,erad):
    state(m1);state(m2)
    if not math.isfinite(erad) or erad<0:raise ValueError('invalid radiation energy')
    mf=m1+m2-erad/c**2
    if mf<=0 or mf*mf<(m1*m1+m2*m2)*(1-1e-13):
        raise ValueError('classical nonspinning area budget violated')
    return mf

def geometry():
    # Units rs=1, coordinates (ct/rs, r/rs, theta, phi).
    t,x,th,ph=s.symbols('t x theta phi',real=True)
    q=[t,x,th,ph];f=1-1/x
    g=s.diag(-f,1/f,x*x,x*x*s.sin(th)**2);gi=g.inv()
    dg=lambda a,b,k:s.diff(g[a,b],q[k])
    gamma={}
    for a in range(4):
      for b in range(4):
       for d in range(4):
        v=s.simplify(sum(gi[a,e]*(dg(e,d,b)+dg(e,b,d)-dg(b,d,e))/2 for e in range(4)))
        if v!=0:gamma[a,b,d]=v
    gam=lambda a,b,d:gamma.get((a,b,d),s.S.Zero)
    R={}
    for a in range(4):
     for b in range(4):
      for j in range(4):
       for k in range(4):
        v=s.simplify(s.diff(gam(a,k,b),q[j])-s.diff(gam(a,j,b),q[k])+
            sum(gam(a,j,e)*gam(e,k,b)-gam(a,k,e)*gam(e,j,b) for e in range(4)))
        if v!=0:R[a,b,j,k]=v
    Ric=s.Matrix(4,4,lambda a,b:s.simplify(sum(R.get((e,a,e,b),0) for e in range(4))))
    assert Ric==s.zeros(4)
    # Diagonal Schwarzschild chart permits direct contraction of R_abcd.
    K=s.simplify(sum(g[a,a]**2*v**2*gi[a,a]*gi[b,b]*gi[j,j]*gi[k,k]
                  for (a,b,j,k),v in R.items()))
    assert s.simplify(K-12/x**6)==0
    # Horizon-regular PG radial block in coordinates (ct/rs, r/rs).
    gp=s.Matrix([[-(1-1/x),s.sqrt(1/x)],[s.sqrt(1/x),1]])
    assert s.simplify(gp.det()+1)==0
    u=s.symbols('u',real=True)
    assert s.simplify((s.Matrix([[1,u]])*gp*s.Matrix([1,u]))[0].subs(u,1-s.sqrt(1/x)))==0
    return {'metric_input':'Schwarzschild / ingoing Painleve-Gullstrand',
       'Ricci_tensor_all_16_entries_zero':True,'Kretschmann_dimensionless':str(K),
       'Kretschmann_SI':'12*rs^2/r^6','PG_radial_determinant':-1,
       'PG_radial_null_equation_verified':True,'symbolic_nonzero_Riemann_components':len(R)}

def run():
    geom=geometry()
    masses=[1e20,1e25,1e30,1e35,1e40]
    radial=np.unique(np.r_[np.geomspace(.05,.999,60),1.,np.geomspace(1.001,100.,60)])
    nullerr=0.;radialcases=0;lawerr=0.;absorb_err=0.;absorb_cases=0
    for M in masses:
        st=state(M)
        # Analytic first law at each M; no finite-difference approximation.
        dS_dM=8*math.pi*kb*G*M/(hbar*c)
        lawerr=max(lawerr,abs(st['temperature_K']*dS_dM/c**2-1))
        for x in radial:
            v=math.sqrt(1/x)
            for sign in [-1,1]:
                u=-v+sign
                nullerr=max(nullerr,abs(-(1-1/x)+2*v*u+u*u)/(1+v*v+u*u))
                radialcases+=1
            assert admit_radial_signal(float(x))==(x>1)
        for frac in [1e-6,.001,.01,.1,.5]:
            E=M*c*c*frac;mf=absorb(M,E)
            absorb_err=max(absorb_err,abs((mf*c*c-(M*c*c+E))/(M*c*c+E)))
            assert state(mf)['entropy_J_K']>=st['entropy_J_K']
            absorb_cases+=1
    # Explicit ownership move, not disappearance of gravitating energy.
    M0=1e30;visible=.01*M0*c*c;total=M0*c*c+visible
    Mafter=absorb(M0,visible);visible=0.
    assert abs((Mafter*c*c+visible-total)/total)<1e-12
    # SWAP between equal-energy local registers, external reference retained.
    swap=np.zeros((8,8),complex)
    for k in range(8):
        r,a,b=(k>>2)&1,(k>>1)&1,k&1
        swap[(r<<2)|(b<<1)|a,k]=1
    Hreg=np.diag([((k>>1)&1)+(k&1) for k in range(8)]).astype(complex)
    assert np.max(np.abs(Hreg@swap-swap@Hreg))==0
    rng=np.random.default_rng(135207);qe=energyerr=0.
    for _ in range(200):
        v=rng.normal(size=4)+1j*rng.normal(size=4);v/=np.linalg.norm(v)
        initial=np.kron(v,[1,0]);moved=swap@initial
        ten=moved.reshape(2,2,2)
        rho=np.einsum('rab,sad->rbsd',ten,ten.conj()).reshape(4,4)
        qe=max(qe,float(np.max(np.abs(rho-np.outer(v,v.conj())))))
        energyerr=max(energyerr,abs(float(np.vdot(initial,Hreg@initial).real-np.vdot(moved,Hreg@moved).real)))
        assert np.max(np.abs(ten[:,1,:]))==0
    negative={}
    def reject(n,fn):
        try:fn()
        except ValueError:negative[n]=True
        else:raise AssertionError(n)
    reject('zero_mass',lambda:state(0));reject('negative_mass',lambda:state(-1))
    reject('negative_absorbed_energy',lambda:absorb(1e30,-1))
    reject('central_singularity_signal',lambda:admit_radial_signal(0))
    assert not admit_radial_signal(.5);negative['escape_from_inside_rejected']=True
    assert not admit_radial_signal(1.);negative['outward_horizon_signal_rejected']=True
    reject('area_decreasing_equal_mass_merger',lambda:check_merger(1e30,1e30,.4*2e30*c*c))
    accepted=[]
    for ratio in [.01,.1,1.]:
        m1=1e30;m2=m1*ratio
        # Pick a radiation fraction from within the area bound, not a prediction.
        maximum=1-math.sqrt(m1*m1+m2*m2)/(m1+m2)
        for f in [0.,maximum/4,maximum/2]:
            mf=check_merger(m1,m2,f*(m1+m2)*c*c)
            accepted.append({'ratio':ratio,'declared_radiated_fraction':f,'final_mass_kg':mf})
    assert max(nullerr,lawerr,absorb_err,qe,energyerr)<1e-12
    out={'version':'r5','status':'PASS_WITH_DECLARED_REVERSE_DESIGN_INPUTS',
      'constants':{'c':c,'G':G,'h':h,'k_B':kb,'source':'https://physics.nist.gov/cuu/Constants/Table/allascii.txt'},
      'geometry':geom,'mass_inputs_kg':masses,'radial_positions_per_mass':len(radial),
      'radial_null_checks':radialcases,'max_normalized_null_residual':nullerr,
      'first_law_checks':len(masses),'first_law_max_relative_error':lawerr,
      'positive_energy_absorption_checks':absorb_cases,'absorption_max_relative_energy_error':absorb_err,
      'quantum_ownership_cases':200,'external_reference_state_max_error':qe,
      'quantum_energy_max_error_in_declared_units':energyerr,
      'merger_budget_cases':len(accepted),'merger_examples':accepted,
      'rejected_controls':negative,'mass_examples':[state(M) for M in masses],
      'observer_scope':'external causal access closes; local infalling matter is not universally annihilated at horizon',
      'finite_universe_scope':'finite local patch; global cosmological matching and global event horizon not solved',
      'adopted_relations':['Schwarzschild/PG GR metric','Bekenstein-Hawking area entropy','Hawking temperature'],
      'not_claimed':['contact geometry uniquely derives metric','microscopic entropy state counting',
        'Hawking spectrum or greybody dynamics derived','complete quantum information recovery from radiation',
        'stationary patch solves rotating collapse or compact cosmological embedding'],
      'environment':{'python':platform.python_version(),'numpy':np.__version__,'sympy':s.__version__}}
    Path(__file__).with_name('black_hole_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':run()
