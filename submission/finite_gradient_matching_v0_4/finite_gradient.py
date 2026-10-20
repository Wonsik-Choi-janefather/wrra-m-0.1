"""Finite-k, linear-amplitude Einstein--Boltzmann conversion experiment.

8 pi G / 3 = 1; local proper time and initial relative scale factor = 1.
The rate-modulation amplitude is normalized to one for a linear response;
the actual frozen WRRA seed multiplies the resulting response afterwards.
Synchronous gauge: h, eta (Ma--Bertschinger), residual gauge fixed by zero
initial perturbations on the declared conversion-start proper-time slice.
"""
from pathlib import Path
from dataclasses import dataclass
import json, math
import numpy as np
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parent
GAMMA=math.log(2.)

@dataclass(frozen=True)
class Model:
    beta: float
    fnu: float
    K: float
    lmax: int=12
    wrong_momentum: bool=False
    no_shear: bool=False

def rhs(t,y,m,active,G,V):
    # N,C,M,H,W,h,eta,g,dC,dG,dV,dM,PC,PG,PV,PM,s,F3/K^3,...
    N,C,M,H,W,h,eta,g,dC,dG,dV,dM,PC,PG,PV,PM,s=y[:17]
    a=math.exp(N); k2=m.K*m.K
    R=C+G+V; rad=R/a**4; matter=M/a**3
    rate=GAMMA if active else 0.
    P=PC+PG+PV+PM
    etad=1.5*P/a**3
    hd=k2*g/a-6*etad
    gd=-2*H*g+2*eta/a-12*V*s/a**3
    if m.no_shear: gd=-2*H*g+2*eta/a
    # Density sources +/- Gamma*(dC+C) include intrinsic rate modulation.
    # Momentum transfer is Q_m^mu=-Q_C^mu=Gamma*rho_C*u_C^mu.
    mom=.75*rate*PC
    out=[H,-rate*C,rate*C/a,-.5*(4*rad+3*matter),H*R/a,hd,etad,gd,
         -k2*PC/a-.5*(4/3)*C*hd-rate*(dC+C),
         -k2*PG/a-(2/3)*G*hd,
         -k2*PV/a-(2/3)*V*hd,
         -k2*PM/a**2-.5*M*hd+rate*(dC+C)/a,
         dC/(3*a)-mom,dG/(3*a),
         dV/(3*a)-(0 if m.no_shear else (4/3)*V*k2*s/a),
         0 if m.wrong_momentum else mom,
         0.]
    if not m.no_shear and V:
        vnu=PV/((4/3)*V) if V else 0.
        out[16]=(4/15*vnu+2/15*g-.3*k2*y[17])/a
    for ell in range(3,m.lmax+1):
        prev=2*s if ell==3 else y[17+ell-4]
        nxt=y[17+ell-2] if ell<m.lmax else 0.
        out.append(0. if m.no_shear or not V else (ell*prev-(ell+1)*k2*nxt)/((2*ell+1)*a))
    return np.array(out)

def evolve(m,rtol=2e-10,atol=2e-21,max_step=.04,tmatch=10.,tend=30.,merge=False):
    G=(1-m.beta)*(1-m.fnu);V=(1-m.beta)*m.fnu
    y=np.zeros(17+m.lmax-2);y[1]=m.beta;y[3]=1.
    segments=[]
    for lo,hi,active in [(0.,1.,True),(1.,tmatch,False)]:
        sol=solve_ivp(lambda t,y:rhs(t,y,m,active,G,V),(lo,hi),y,
                      method='DOP853',rtol=rtol,atol=atol,max_step=max_step,dense_output=True)
        if not sol.success:raise RuntimeError(sol.message)
        segments.append((sol,G,V,active));y=sol.y[:,-1].copy()
    before=y.copy();Gbefore=G
    if merge:
        G+=y[1];y[1]=0.;y[9]+=y[8];y[8]=0.;y[13]+=y[12];y[12]=0.
    after=y.copy()
    sol=solve_ivp(lambda t,y:rhs(t,y,m,False,G,V),(tmatch,tend),y,
                  method='DOP853',rtol=rtol,atol=atol,max_step=max_step,dense_output=True)
    if not sol.success:raise RuntimeError(sol.message)
    segments.append((sol,G,V,False))
    return dict(model=m,segments=segments,before=before,after=after,
                Gbefore=Gbefore,Gafter=G,V=V,tmatch=tmatch,tend=tend)

def diagnostics(t,y,m,G,V,active=False):
    d=rhs(t,y,m,active,G,V)
    N,C,M,H,W,h,eta,g,dC,dG,dV,dM,PC,PG,PV,PM,s=y[:17]
    a=np.exp(N);rho=(C+G+V)/a**4+M/a**3
    dr=(dC+dG+dV)/a**4;dm=dM/a**3;dp=dr/3
    P=PC+PG+PV+PM;hd=d[5];ed=d[6]
    # Independent Hamiltonian constraint; neither eta nor hdot is reset to it.
    ham=m.K**2*eta-.5*a*a*H*hd+1.5*a*a*(dr+dm)
    # Derivative of hdot from the evolved shear/momentum system.
    edd=1.5/a**3*(sum(d[12:16])-3*H*P)
    hdd=m.K**2/a*(d[7]-H*g)-6*edd
    trace=hdd+3*H*hd-2*m.K**2*eta/a**2+9*dp
    # Independently sum density and momentum conservation with Q eliminated.
    drhot=(sum(d[8:11])-4*H*(dC+dG+dV))/a**4+(d[11]-3*H*dM)/a**3
    energy=drhot+3*H*((dr+dm)+dp)+m.K**2*P/a**5+.5*((4/3)*(C+G+V)/a**4+M/a**3)*hd
    momentum=sum(d[12:16])-(dC+dG+dV)/(3*a)+(0 if m.no_shear else (4/3)*V*m.K**2*s/a)
    # Gauge invariant post-exchange species curvatures and relative entropies.
    zr=-eta+(dC+dG+dV)/(4*(C+G+V))
    zm=-eta+dM/(3*M) if M>0 else 0.
    zg=-eta+dG/(4*G) if G else 0.
    zn=-eta+dV/(4*V) if V else 0.
    ent=(dM/M-.75*(dC+dG+dV)/(C+G+V)) if M>0 else 0.
    return dict(a=float(a),H=float(H),h=float(h),eta=float(eta),hdot=float(hd),
        eta_dot=float(ed),shear_scaled=float(g),sigma_nu=float(m.K**2*s),
        zeta_r=float(zr),zeta_m=float(zm),S_mr=float(ent),S_nugamma=float(3*(zn-zg)),
        delta_rho=float(dr+dm),momentum_scaled=float(P/a**4),delta_pressure=float(dp),
        Hamiltonian_residual=float(ham),trace_residual=float(trace),
        energy_residual=float(energy),momentum_residual=float(momentum),
        background_friedmann=float((H*H-rho)/rho),background_energy_work=float((C+G+V)/a+M+W-1),
        k_over_aH=float(m.K/(a*H)))

def sample_audit(run):
    m=run['model'];rows=[]
    for sol,G,V,active in run['segments']:
        for t in np.linspace(sol.t[0],sol.t[-1],101):
            rows.append(diagnostics(t,sol.sol(t),m,G,V,active))
    # Normalize against response amplitudes over the entire history, avoiding
    # division by individual zeros. Scale choices and absolute residuals reported.
    scales={'Hamiltonian_residual':max(max(abs(x['eta']),abs(x['h']),abs(x['delta_rho'])) for x in rows),
            'trace_residual':max(abs(x['delta_pressure']) for x in rows),
            'energy_residual':max(abs(x['delta_rho']) for x in rows),
            'momentum_residual':max(abs(x['momentum_scaled']) for x in rows)}
    residuals={k:{'max_absolute':max(abs(x[k]) for x in rows),'normalizer':max(v,1e-100),
                  'normalized':max(abs(x[k]) for x in rows)/max(v,1e-100)} for k,v in scales.items()}
    residuals['background_friedmann']=max(abs(x['background_friedmann']) for x in rows)
    residuals['background_energy_work']=max(abs(x['background_energy_work']) for x in rows)
    return residuals,rows

def full_state(run,side='before'):
    y=run[side];m=run['model'];G=run['Gbefore' if side=='before' else 'Gafter'];V=run['V']
    a=np.exp(y[0]);C=y[1];M=y[2]
    v=lambda P,w:float(P/w) if w else 0.
    return dict(time=run['tmatch'],a_relative=float(a),h=float(y[5]),eta=float(y[6]),
      shear_scaled=float(y[7]),delta_C=float(y[8]/C) if C else 0.,
      delta_gamma=float(y[9]/G),delta_nu=float(y[10]/V) if V else 0.,delta_m=float(y[11]/M),
      theta_C=float(m.K**2*v(y[12],4*C/3)),theta_gamma=float(m.K**2*v(y[13],4*G/3)),
      theta_nu=float(m.K**2*v(y[14],4*V/3)),theta_m=float(m.K**2*v(y[15],a*M)),
      F_nu=[float(y[10]/V) if V else 0.,float(4*m.K*v(y[14],4*V/3)/3),float(2*m.K**2*y[16])]+
           [float(m.K**ell*y[17+ell-3]) for ell in range(3,m.lmax+1)])
