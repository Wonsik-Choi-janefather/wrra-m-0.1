"""Independent hdot/trace-Einstein evolution, with unscaled neutrino moments.

The main solver evolves scaled metric shear and scaled multipoles. This solver
instead evolves hdot via the trace equation, so comparing them is not merely
re-evaluating the main solver's Hamiltonian definition.
"""
import math
import numpy as np
from scipy.integrate import solve_ivp
from finite_gradient import GAMMA

def rhs(t,y,m,active,G,V):
    N,C,M,H,W,h,eta,L,dC,dG,dV,dM,PC,PG,PV,PM,sigma=y[:17]
    a=math.exp(N);rate=GAMMA if active else 0.;k=m.K
    dr=(dC+dG+dV)/a**4
    ed=1.5*(PC+PG+PV+PM)/a**3
    Ld=-3*H*L+2*k*k*eta/a**2-3*dr
    momentum=.75*rate*PC
    out=[H,-rate*C,rate*C/a,-.5*(4*(C+G+V)/a**4+3*M/a**3),H*(C+G+V)/a,
      L,ed,Ld,-k*k*PC/a-2*C*L/3-rate*(dC+C),
      -k*k*PG/a-2*G*L/3,-k*k*PV/a-2*V*L/3,
      -k*k*PM/a**2-M*L/2+rate*(dC+C)/a,
      dC/(3*a)-momentum,dG/(3*a),dV/(3*a)-4*V*sigma/(3*a),momentum,
      ((4/15)*k*k*PV/((4/3)*V)/a-(3/10)*k*y[17]/a+2*L/15+4*ed/5) if V else 0.]
    for ell in range(3,m.lmax+1):
        prev=2*sigma if ell==3 else y[17+ell-4]
        nxt=y[17+ell-2] if ell<m.lmax else 0.
        out.append(k*(ell*prev-(ell+1)*nxt)/((2*ell+1)*a) if V else 0.)
    return out

def evolve(m,rtol=1e-11,atol=2e-22):
    G=(1-m.beta)*(1-m.fnu);V=(1-m.beta)*m.fnu
    y=np.zeros(17+m.lmax-2);y[1]=m.beta;y[3]=1.
    for lo,hi,active in [(0.,1.,True),(1.,10.,False),(10.,30.,False)]:
        sol=solve_ivp(lambda t,y:rhs(t,y,m,active,G,V),(lo,hi),y,
                      method='DOP853',rtol=rtol,atol=atol,max_step=.03)
        if not sol.success:raise RuntimeError(sol.message)
        y=sol.y[:,-1]
    return y
