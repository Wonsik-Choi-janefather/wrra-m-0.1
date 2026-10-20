"""Exact first variation of the declared v0.5/v0.6 local-cell event model.

This is a k=0 tangent, NOT a finite-k source or a CAMB injection. Event count
is held fixed only inside the open interval bounded by pulse-edge events.
The saltation term transports the event-time derivative onto a common slice.
"""
from pathlib import Path
import json, math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy import constants as sc
from thermal_history import EOS, hubble, NUCOEF, TCMB, SECONDS
from packet_emission import BETA, Model, schedule

P=Path(__file__).resolve().parent
U_MEV4=(sc.electron_volt*1e6)**4/(sc.hbar*sc.c)**3
U100=3*(100000/(sc.parsec*1e6))**2*sc.c**2/(8*math.pi*sc.G)

def run(eos,beta=BETA,xi=0.,cost=.01,end=5000.,tangent=True,omit_saltation=False,rtol=1e-10):
    def tnu(T):return (2/5.5)**(1/3)*(eos.gs(T)/2)**(1/3)*T
    Ti=brentq(lambda T:hubble((eos(T)[0]+NUCOEF*tnu(T)**4)/(1-beta))-1/SECONDS,.5,4.,xtol=1e-13)
    rhoi=(eos(Ti)[0]+NUCOEF*tnu(Ti)**4)/(1-beta)
    rn0=NUCOEF*tnu(Ti)**4; q=beta*rhoi/256; C=beta*rhoi
    times,_=schedule(Model(xi=xi)); y=np.array([0.,math.log(Ti),0.,0.]);z=np.zeros(4)
    t=0.;events=[];work=[]
    def flow(y,CC,jac=False):
        N,L,M,W=y;a=np.exp(N);T=np.exp(L); re,pe,der=eos(T)
        rn=rn0/a**4;rx=CC/a**4;rm=M/a**3;rho=re+rn+rx+rm
        H=hubble(float(rho))*SECONDS; A=(re+pe)/(T*der); pres=pe+(rn+rx)/3
        f=np.array([H,-3*H*A,0.,3*H*pres*a**3/rhoi])
        if not jac:return f
        dr,dp,dd=np.array([re,pe,der])*np.array([s(L,1) for s in eos.spl])
        dH=H/(2*rho)*np.array([-4*(rn+rx)-3*rm,dr,a**-3,0.])
        dA=A*((dr+dp)/(re+pe)-1-dd/der)
        J=np.zeros((4,4));J[0]=dH;J[1]=-3*A*dH;J[1,1]-=3*H*dA
        J[3]=3*a**3/rhoi*pres*dH
        J[3,0]+=3*H*a**3/rhoi*(3*pres-4*(rn+rx)/3)
        J[3,1]+=3*H*a**3/rhoi*dp
        return f,J
    for j,target in enumerate([*times,end]):
        if target<t:raise ValueError('end must follow the pulse events')
        def rhs(tt,v):
            if tangent:
                f,J=flow(v[:4],C,True);return np.r_[f,J@v[4:]]
            return flow(v,C)
        v=np.r_[y,z] if tangent else y
        sol=solve_ivp(rhs,(t,float(target)),v,method='DOP853',rtol=rtol,
            atol=np.array([1e-13,1e-13,rhoi*beta*1e-13,1e-13]* (2 if tangent else 1)),
            max_step=max(.01,(target-t)/32))
        if not sol.success:raise RuntimeError(sol.message)
        y=sol.y[:4,-1]; z=sol.y[4:,-1] if tangent else z;t=float(target)
        a=math.exp(y[0]);re=eos(math.exp(y[1]))[0]
        work.append(((re+rn0/a**4)*a**3+C/a+y[2])/rhoi+y[3]-1)
        if j==len(times):break
        before=y.copy();fm=flow(before,C);T=math.exp(y[1]);heat=cost*q/a**4
        Ta=brentq(lambda u:eos(u)[0]-eos(T)[0]-heat,T,T*(1+1e-4),xtol=5e-15)
        dm=(1-cost)*q/a;y[1]=math.log(Ta);y[2]+=dm; C=(255-j)*q
        DR=np.eye(4);DR[2,0]=-dm
        # Derivatives of the actual interpolated energy reset, not an assumed T^4 EOS.
        rb=eos(T)[0];ra=eos(Ta)[0]
        db=rb*eos.spl[0](math.log(T),1);da=ra*eos.spl[0](math.log(Ta),1)
        DR[1,0]=-4*heat/da;DR[1,1]=db/da
        tp=-t/(1+xi)
        salt=(DR@fm-flow(y,C))*tp
        if tangent:z=DR@z+(0 if omit_saltation else salt)
        events.append(dict(event=j+1,t=t,time_derivative=tp,saltation=salt.tolist()))
    N,L,M,W=y;T=math.exp(L);a=math.exp(N);re,pe,der=eos(T)
    # Photon entropy today is an input normalization, as in v0.6.
    ai=(4*math.pi**2/45*TCMB**3/(eos.entropy(T)*a**3))**(1/3)
    wh2=M*ai**3*U_MEV4/U100
    dr=re*eos.spl[0](L,1)
    S=z[2]/M-3*z[0]-dr*z[1]/(re+pe)
    return dict(beta=beta,xi=xi,count=len(times),y=y.tolist(),tangent=z.tolist(),
        S_m_em_response=float(S),a_initial=ai,omch2_from_packets=wh2,
        Tinitial_MeV=Ti,final_temperature_MeV=T,max_energy_work_residual=max(abs(np.array(work))),
        events=events,scope='k=0 common-proper-time tangent of the fixed-count local-cell model')

def main():
    eos=EOS();base=run(eos);bad=run(eos,omit_saltation=True)
    fd=[]
    for eps in [1e-3,3e-4,1e-4]:
        plus=run(eos,xi=eps,tangent=False);minus=run(eos,xi=-eps,tangent=False)
        ym=np.array(minus['y']);yp=np.array(plus['y']);zfd=(yp-ym)/(2*eps)
        # Energy entropy S is linearized at the same unperturbed state.
        N,L,M,_=base['y'];T=math.exp(L);re,pe,_=eos(T)
        S=zfd[2]/M-3*zfd[0]-re*eos.spl[0](L,1)*zfd[1]/(re+pe)
        fd.append(dict(epsilon=eps,count_plus=plus['count'],count_minus=minus['count'],
            S_response=float(S),relative_error=float(abs(S/base['S_m_em_response']-1))))
    target=next(x['background']['omch2'] for x in json.loads((P/'inputs/address_results.json').read_text())['cases'] if x['branch']=='dark_weight_only')
    calibrated_beta=brentq(lambda b:run(eos,beta=b,tangent=False)['omch2_from_packets']/target-1,
        BETA*.5,BETA*2,xtol=1e-18)
    calibrated=run(eos,beta=calibrated_beta)
    seed=np.load(P/'inputs/quantized_seed.npz')['entropy'];seed-=seed.mean()
    predicted=seed*base['S_m_em_response']
    np.savez_compressed(P/'results/local_seed_tangent.npz',rate_modulation=seed,S_m_em=predicted)
    result=dict(base=base,missing_event_time_negative_control=bad,finite_difference=fd,
        calibration=dict(target_omch2=target,old_relative_mismatch=base['omch2_from_packets']/target-1,
            recalibrated_beta=calibrated_beta,beta_relative_change=calibrated_beta/BETA-1,
            recalibrated_result=calibrated,meaning='Background calibration only; not yet a finite-k perturbation rerun'),
        actual_seed=dict(rate_RMS=float(np.std(seed)),entropy_RMS=float(np.std(predicted)),
            approximation='linear k=0 fixed-count tangent, not a finite-k realization'),
        smooth_v04_entropy_response=json.loads((P/'inputs/dynamics_results.json').read_text())['entropy_response_to_rate_modulation'])
    (P/'results/event_tangent.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['base','missing_event_time_negative_control','calibration']},indent=2))
    print('base S',base['S_m_em_response'],'old omch2',base['omch2_from_packets'],'new beta',calibrated_beta)
if __name__=='__main__':main()
