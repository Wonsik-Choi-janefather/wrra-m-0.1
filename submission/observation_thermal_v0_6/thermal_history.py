"""Finite-packet MeV thermal completion, massive e+- EOS, instantaneous-decoupling branch.
Natural-unit energy densities MeV^4, elapsed physical time seconds.
N_eff is inherited effective neutrino-energy input, not a decoupling prediction.
"""
from pathlib import Path
import math,json,csv
import numpy as np
from scipy.special import expit
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy import constants as sc
from packet_emission import schedule,Model,BETA,SECONDS
P=Path(__file__).resolve().parent
ME=sc.physical_constants['electron mass energy equivalent in MeV'][0]
HBAR=sc.hbar/sc.electron_volt/1e6
MPL=math.sqrt(sc.hbar*sc.c/sc.G)*sc.c**2/sc.electron_volt/1e6
TCMB=2.7255*sc.Boltzmann/sc.electron_volt/1e6
NEFF=3.044
NUCOEF=7/8*2*NEFF*math.pi**2/30

class EOS:
    def __init__(self,n=600,nquad=160):
        u,w=np.polynomial.legendre.leggauss(nquad);self.x=(u+1)*25;self.w=w*25
        ts=np.geomspace(.002,1000,n)
        v=np.array([self.exact(T) for T in ts]);self.grid=ts
        self.spl=[CubicSpline(np.log(ts),np.log(v[:,j])) for j in range(3)]
    def exact(self,T):
        x=self.x;E=np.sqrt(x*x+(ME/T)**2);f=expit(-E);g=4/(2*math.pi**2)
        rho=g*T**4*np.dot(self.w,x*x*E*f)+math.pi**2/15*T**4
        pressure=g*T**4/3*np.dot(self.w,x**4/E*f)+math.pi**2/45*T**4
        deriv=g*T**3*np.dot(self.w,x*x*E*E*f*(1-f))+4*math.pi**2/15*T**3
        return np.array([rho,pressure,deriv])
    def __call__(self,T):return np.exp([s(np.log(T)) for s in self.spl])
    def entropy(self,T):
        r,p,_=self(T);return (r+p)/T
    def gs(self,T):return self.entropy(T)/(2*math.pi**2/45*T**3)

def hubble(rho):return math.sqrt(8*math.pi/3*rho)/MPL/HBAR

def run(eos,cost=.01,rtol=2e-10):
    # Backward electromagnetic entropy anchor; neutrino ratio corresponds to
    # the ideal relativistic-decoupling entropy branch, with effective N_eff input.
    def tnu(T):return (2/5.5)**(1/3)*(eos.gs(T)/2)**(1/3)*T
    Ti=brentq(lambda T:hubble((eos(T)[0]+NUCOEF*tnu(T)**4)/(1-BETA))-1/SECONDS,.5,4.,xtol=1e-13)
    rhoi=(eos(Ti)[0]+NUCOEF*tnu(Ti)**4)/(1-BETA)
    C=BETA*rhoi;M=0.;Tnu0=tnu(Ti);q=BETA*rhoi/256
    y=np.array([0.,math.log(Ti),0.]);t=0.;samples=[];events=[];jumps=[];milestones=[]
    times,_=schedule(Model());targets=[*times,1.,10.,100.,1000.,5000.]
    # pressure work stored in units of initial physical energy per reference cell
    for j,target in enumerate(targets):
        def rhs(t,y):
            N,lnT,W=y;a=math.exp(N);T=math.exp(lnT);re,pe,der=eos(T)
            rn=NUCOEF*(Tnu0/a)**4;rx=C/a**4;rm=M/a**3
            H=hubble(re+rn+rx+rm)*SECONDS
            return [H,-3*H*(re+pe)/(T*der),3*H*(pe+(rn+rx)/3)*a**3/rhoi]
        sol=solve_ivp(rhs,(t,float(target)),y,method='DOP853',rtol=rtol,atol=rtol*1e-2,
            max_step=max(.02,(float(target)-t)/100),dense_output=True)
        if not sol.success:raise RuntimeError(sol.message)
        for Tmark in [1.,.5,.1,.05]:
            if math.exp(y[1])>=Tmark>=math.exp(sol.y[1,-1]) and not any(x['Tgamma_MeV']==Tmark for x in milestones):
                tm=brentq(lambda tt:sol.sol(tt)[1]-math.log(Tmark),t,float(target),xtol=1e-11)
                am=math.exp(sol.sol(tm)[0]);milestones.append(dict(Tgamma_MeV=Tmark,time_from_start_s=tm*SECONDS,
                    a_relative=am,Tnu_MeV=Tnu0/am))
        for tt in np.linspace(t,float(target),8):
            N,lnT,W=sol.sol(tt);a=math.exp(N);T=math.exp(lnT);re,pe,_=eos(T)
            rn=NUCOEF*(Tnu0/a)**4;rho=re+rn+C/a**4+M/a**3
            samples.append(dict(time_from_start_s=float(tt*SECONDS),a_relative=a,
                Tgamma_MeV=T,Tnu_MeV=Tnu0/a,H_s_inverse=hubble(rho),
                g_rho=30*(re+rn)/(math.pi**2*T**4),g_s_em=eos.gs(T),
                entropy_em_comoving=eos.entropy(T)*a**3,
                energy_work_residual=((re+rn)*a**3+C/a+M)/rhoi+W-1))
        y=sol.y[:,-1];t=float(target)
        if j<len(times):
            a=math.exp(y[0]);before=math.exp(y[1]);heat=cost*q/a**4
            after=brentq(lambda T:eos(T)[0]-eos(before)[0]-heat,before,before*(1+1e-4),xtol=5e-15)
            dm=(1-cost)*q/a;C=(255-j)*q;M+=dm;y[1]=math.log(after)
            # Independent finite-temperature energy jump rather than a radiation J shortcut.
            bal=(-q/a+dm+(eos(after)[0]-eos(before)[0])*a**3)/(q/a)
            jumps.append(float(bal));events.append(dict(event=j+1,time_s=t*SECONDS,T_before_MeV=before,T_after_MeV=after,a=a,
                entropy_change=eos.entropy(after)*a**3-eos.entropy(before)*a**3))
    # Final entropy determines physical scale normalization today, assuming no
    # later non-standard photon entropy production; neutrinos just redshift here.
    N,lnT,W=y;af=math.exp(N);Tf=math.exp(lnT)
    scale_initial_derived=(eos.entropy(TCMB)/eos.entropy(Tf))**(1/3)/af if TCMB>=.002 else (
        (4*math.pi**2/45*TCMB**3/eos.entropy(Tf))**(1/3)/af)
    late_ratio=Tnu0/af/Tf*(2/eos.gs(Tf))**(1/3)
    result=dict(Tinitial_MeV=Ti,Hinitial_s_inverse=1/SECONDS,elapsed_time_unit_s=SECONDS,
        a_initial_derived=scale_initial_derived,old_a_initial=1e-10,
        a_initial_relative_change=scale_initial_derived/1e-10-1,
        final_Tgamma_MeV=Tf,late_Tnu_over_Tgamma=late_ratio,
        effective_late_Neff=NEFF*(late_ratio/(4/11)**(1/3))**4,
        max_energy_work_residual=max(abs(s['energy_work_residual']) for s in samples),
        max_event_balance_relative=max(abs(x) for x in jumps),events=len(events),
        record_entropy_gain=sum(e['entropy_change'] for e in events),M_over_rhoi=M/rhoi,milestones=milestones,
        scope='Homogeneous packet thermal completion with equilibrium e+- and instantaneous relativistic neutrino decoupling. No collision integral, flavor transport, weak freezeout or BBN yields. Time is elapsed since pulse start, not cosmic age.')
    return result,samples,events

def main():
    eos=EOS();r,s,e=run(eos);r0,s0,e0=run(eos,cost=0.)
    refined,_,_=run(EOS(n=1200,nquad=240),rtol=2e-11)
    r['refinement']={key:abs(refined[key]/r[key]-1) for key in ['Tinitial_MeV','a_initial_derived','final_Tgamma_MeV','M_over_rhoi']}
    r['zero_cost_comparison']=r0
    r['EOS_checks']=dict(relativistic_em_g=eos.gs(1000),low_temperature_em_g=eos.gs(.005),
        max_pressure_below_rho_over_three=float(max(eos(T)[1]/eos(T)[0] for T in np.geomspace(.005,30,50))))
    (P/'results/thermal.json').write_text(json.dumps(r,indent=2)+'\n')
    (P/'results/thermal_events.json').write_text(json.dumps(e,indent=2)+'\n')
    with (P/'results/thermal_history.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=s[0].keys());w.writeheader();w.writerows(s)
    print(json.dumps(r,indent=2))
if __name__=='__main__':main()
