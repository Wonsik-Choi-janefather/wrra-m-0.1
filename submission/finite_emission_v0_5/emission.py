"""WRRA finite packet event closure; local FLRW, not finite-k perturbations.

Packet q is a comoving radiation-energy debit per fixed reference cell.
It is NOT a universal particle rest energy or a derived Planck quantum.
The accumulator is transfer credit, never a second energy reservoir.
"""
from dataclasses import dataclass
from pathlib import Path
import json, math
import numpy as np
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parent
INPUT=json.loads((ROOT/'inputs/dynamics_results.json').read_text())
BETA=INPUT['calibrated_convertible_radiation_fraction']
GAMMA=math.log(2.)
SECONDS=INPUT['time_unit_seconds']

@dataclass(frozen=True)
class Model:
    packets:int=256
    xi:float=0.
    cost_fraction:float=0.01
    pulse:float=1.
    end:float=10.
    capacity:int|None=None
    def validate(self):
        if not isinstance(self.packets,int) or isinstance(self.packets,bool) or self.packets<1:
            raise ValueError('packets must be a positive finite integer')
        if not all(math.isfinite(x) for x in [self.xi,self.cost_fraction,self.pulse,self.end]):
            raise ValueError('nonfinite input')
        if self.xi<=-1 or not 0<=self.cost_fraction<=1 or not 0<=self.pulse<=self.end:
            raise ValueError('invalid rate, cost or time')
        if self.capacity is not None and (not isinstance(self.capacity,int) or self.capacity<0):
            raise ValueError('invalid recording capacity')

def schedule(m):
    """Exact integral of rdot=Gamma*(1+xi)*C between jumps.

    Initial r=0. At r=q: C-=q, r-=q. Gate exhaustion pauses credit
    generation; it does not secretly debit energy or build a backlog.
    Events exactly at pulse closure are included; no forced final flush.
    """
    m.validate();rate=GAMMA*(1+m.xi);N=m.packets
    dt=1/(rate*np.arange(N,0,-1,dtype=float))
    times=np.cumsum(dt)
    count=int(np.searchsorted(times,m.pulse,side='right'))
    allowed=N if m.capacity is None else min(N,m.capacity)
    count=min(count,allowed);times=times[:count]
    last=float(times[-1]) if count else 0.
    closed=count==allowed
    r=0. if closed else rate*(N-count)/N*(m.pulse-last) # r/beta
    return times,float(r)

def free_rhs(t,y,R,M):
    N,H,W=y;a=math.exp(N)
    return [H,-.5*(4*R/a**4+3*M/a**3),H*R/a]

def simulate(m,rtol=2e-11,max_step=.1,wrong=None):
    times,credit=schedule(m);q=BETA/m.packets;C=BETA;J=0.;M=0.
    y=np.array([0.,1.,0.]);t=0.;rows=[];maxfried=0.;maxwork=0.
    for j,target in enumerate([*times,m.end]):
        target=float(target)
        if target>t:
            sol=solve_ivp(lambda t,y:free_rhs(t,y,1-BETA+C+J,M),(t,target),y,
                method='DOP853',rtol=rtol,atol=rtol*1e-3,max_step=max_step)
            if not sol.success:raise RuntimeError(sol.message)
            aa=np.exp(sol.y[0]);rho=(1-BETA+C+J)/aa**4+M/aa**3
            maxfried=max(maxfried,float(np.max(abs(sol.y[1]**2/rho-1))))
            maxwork=max(maxwork,float(np.max(abs((1-BETA+C+J)/aa+M+sol.y[2]-1))))
            y=sol.y[:,-1];t=target
        if j==len(times):break
        a=math.exp(y[0]);heat=m.cost_fraction*q
        dm=(1-m.cost_fraction)*q/a
        if wrong=='missing_heat':heat=0.
        if wrong=='missing_redshift':dm=(1-m.cost_fraction)*q
        local_balance=(-q+a*dm+heat)/q
        before=C;C=(m.packets-j-1)*q;M+=dm;J+=heat
        rows.append(dict(event=j+1,time=t,time_seconds=t*SECONDS,a=a,
            reservoir_before=before,reservoir_after=C,q_comoving=q,
            physical_energy_per_reference_cell=q/a,matter_gain=dm,
            record_heat_comoving=heat,credit_after=0.,records_left=(
                m.packets if m.capacity is None else m.capacity)-j-1,
            local_balance_normalized=local_balance))
    a=math.exp(y[0]);R=1-BETA+C+J
    return dict(parameters=m.__dict__,events=rows,count=len(times),credit_over_beta=credit,
        q_over_beta=1/m.packets,C=C,J=J,M=M,R=R,a=a,H=float(y[1]),W=float(y[2]),
        matter_over_radiation_comoving=M/R,
        max_Friedmann_relative=maxfried,max_energy_plus_work_absolute=maxwork,
        max_jump_balance_normalized=max([abs(x['local_balance_normalized']) for x in rows],default=0.))

def continuum(xi=0.,cost=0.,pulse=1.,end=10.):
    """Independent smooth RHS, same cost branch, no packet scheduling."""
    def rhs(t,y,rate):
        N,C,J,M,H,W=y;a=math.exp(N);R=1-BETA+C+J
        return [H,-rate*C,cost*rate*C,(1-cost)*rate*C/a,
            -.5*(4*R/a**4+3*M/a**3),H*R/a]
    y=np.array([0.,BETA,0.,0.,1.,0.])
    for lo,hi,rate in [(0.,pulse,GAMMA*(1+xi)),(pulse,end,0.)]:
        if hi<=lo:continue
        s=solve_ivp(lambda t,y:rhs(t,y,rate),(lo,hi),y,method='DOP853',
            rtol=2e-12,atol=2e-23,max_step=.025)
        if not s.success:raise RuntimeError(s.message)
        y=s.y[:,-1]
    N,C,J,M,H,W=y;R=1-BETA+C+J
    return dict(C=C,J=J,M=M,R=R,a=math.exp(N),H=H,W=W,matter_over_radiation_comoving=M/R)

def entropy_contrast(run,base):
    """Nonlinear log species contrast; delta N cancels. Zero-gradient only."""
    return math.log1p((run['M']-base['M'])/base['M'])-.75*math.log1p((run['R']-base['R'])/base['R'])
