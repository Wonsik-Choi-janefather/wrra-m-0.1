from pathlib import Path
import json,csv,hashlib,math
import numpy as np
from scipy.integrate import solve_ivp
from emission import *

P=Path(__file__).resolve().parent;O=P/'results';O.mkdir(exist_ok=True)
checks={}
def check(name,condition):
    checks[name]=bool(condition)
    if not condition:raise AssertionError(name)

base=simulate(Model());zero=simulate(Model(cost_fraction=0.))
cont=continuum();contcost=continuum(cost=.01)
check('event_energy_conservation',base['max_jump_balance_normalized']<3e-16)
check('independent_Friedmann_evolution',base['max_Friedmann_relative']<2e-9)
check('energy_plus_pressure_work',base['max_energy_plus_work_absolute']<2e-10)
check('strict_event_order',np.all(np.diff([e['time'] for e in base['events']])>0))
check('no_event_after_pulse',base['events'][-1]['time']<=1.)
check('nonnegative_resources',min(base['C'],base['M'],base['J'])>=0)
check('unflushed_credit_bounded',0<=base['credit_over_beta']<base['q_over_beta'])
check('heat_ledger_equals_event_cost',abs(base['J']-.01*base['count']*BETA/256)<1e-20)
check('finite_event_bound',base['count']<=256)

# Independent numerical root clock for all baseline events (no analytic schedule).
clock=[];t=0.;C=BETA;q=BETA/256
for i in range(base['count']):
    def ev(t,y):return y[0]-q
    ev.terminal=True;ev.direction=1
    sol=solve_ivp(lambda t,y:[GAMMA*C],(t,1.01),[0.],events=ev,
        rtol=1e-11,atol=1e-22,max_step=.037)
    t=float(sol.t_events[0][0]);clock.append(t);C=(255-i)*q
clockerr=float(np.max(abs(np.array(clock)-np.array([e['time'] for e in base['events']]))))
check('independent_root_clock',clockerr<2e-13)
refined=simulate(Model(),rtol=2e-12,max_step=.025)
referr=abs(refined['M']/base['M']-1)
check('background_time_refinement',referr<2e-9)
check('no_time_grid_in_event_schedule',[e['time'] for e in base['events']]==[e['time'] for e in refined['events']])

convergence=[]
for N in [32,128,512,2048,8192]:
    for eps in [0.,.01]:
        x=simulate(Model(packets=N,cost_fraction=eps));c=cont if eps==0 else contcost
        err=abs(x['M']/c['M']-1)
        convergence.append(dict(N=N,cost=eps,count=x['count'],M_relative_error=err,
            C_error_over_beta=abs(x['C']-c['C'])/BETA))
        check(f'bounded_inventory_{N}_{eps}',abs(x['C']-c['C'])/BETA<2/N)
        check(f'conserving_{N}_{eps}',x['max_jump_balance_normalized']<3e-16)
for eps in [0.,.01]:
    series=[x['M_relative_error'] for x in convergence if x['cost']==eps]
    check(f'continuum_refinement_{eps}',all(b<a for a,b in zip(series,series[1:])))
    check(f'finest_continuum_error_{eps}',series[-1]<4e-4)

# Avoid the accidental exact half-inventory at Gamma=ln2 and an even N.
offgrid=[]
for N in [31,127,511,2047]:
    x=simulate(Model(packets=N,pulse=.73,end=3.,xi=.017))
    c=continuum(xi=.017,cost=.01,pulse=.73,end=3.)
    err=abs(x['M']/c['M']-1)
    offgrid.append(dict(N=N,pulse=.73,xi=.017,M_relative_error=err,
        C_error_over_beta=abs(x['C']-c['C'])/BETA))
    check(f'offgrid_inventory_{N}',abs(x['C']-c['C'])/BETA<2/N)
check('offgrid_continuum_refinement',offgrid[-1]['M_relative_error']<offgrid[0]['M_relative_error']/10)

gate=simulate(Model(capacity=7));closed=simulate(Model(capacity=0))
check('record_capacity_stops_emission',gate['count']==7 and gate['credit_over_beta']==0.)
check('closed_gate_no_energy_transfer',closed['count']==0 and closed['C']==BETA and closed['M']==0.)
check('coarse_quantum_no_forced_flush',simulate(Model(packets=1))['count']==0)
empty=simulate(Model(packets=16,pulse=8.,end=10.))
check('exhausted_finite_reservoir',empty['count']==16 and empty['C']==0.)
allheat=simulate(Model(cost_fraction=1.))
check('all_record_heat_boundary',allheat['M']==0. and allheat['J']>0.)
check('cost_reduces_matter',base['M']<zero['M'])
check('cost_does_not_change_this_clock',[e['time'] for e in base['events']]==[e['time'] for e in zero['events']])
for name,m in [('zero_packets',Model(packets=0)),('negative_rate',Model(xi=-1.)),
    ('negative_cost',Model(cost_fraction=-.1)),('excess_cost',Model(cost_fraction=1.1)),
    ('negative_capacity',Model(capacity=-1)),('nonfinite',Model(xi=float('nan')))]:
    rejected=False
    try:schedule(m)
    except ValueError:rejected=True
    check('reject_'+name,rejected)
negative={}
for wrong in ['missing_heat','missing_redshift']:
    x=simulate(Model(),wrong=wrong);negative[wrong]=dict(
        jump_balance=x['max_jump_balance_normalized'],Friedmann=x['max_Friedmann_relative'])
    check('reject_control_'+wrong,x['max_jump_balance_normalized']>1e-3)

# Frozen actual seed: no Fourier interpolation or amplitude fit.
z=np.load(P/'inputs/quantized_seed.npz');seed=z['entropy']
cells=[];eventtimes=[];ent=[]
for j,xi in enumerate(seed):
    r=simulate(Model(xi=float(xi)));S=entropy_contrast(r,base);ent.append(S)
    ts=np.array([e['time'] for e in r['events']]);eventtimes.append(ts)
    cells.append(dict(cell=j,xi=float(xi),count=r['count'],first_time=float(ts[0]),
        last_time=float(ts[-1]),M=r['M'],R=r['R'],S_log=S))
    check(f'cell_{j}_timing_rate_law',np.max(abs(ts*(1+xi)-np.array([e['time'] for e in base['events']])))<2e-15)
    check(f'cell_{j}_event_conservation',r['max_jump_balance_normalized']<3e-16)
    check(f'cell_{j}_credit_bound',0<=r['credit_over_beta']<1/256)
np.savez_compressed(O/'actual_seed_event_times.npz',xi=seed,event_times=np.array(eventtimes),S_log=np.array(ent))

# Noncommuting small-seed / finite-q limits: compare actual plateau to smooth tangent.
d=1e-4
tangent=(entropy_contrast(continuum(xi=d),cont)-entropy_contrast(continuum(xi=-d),cont))/(2*d)
check('smooth_zero_cost_recovers_v03_entropy',abs(tangent-INPUT['entropy_response_to_rate_modulation'])<2e-7)
amplitude=[]
for delta in [1e-2,1e-4,1e-6,5e-8]:
    rp=simulate(Model(xi=delta,cost_fraction=0.));rm=simulate(Model(xi=-delta,cost_fraction=0.))
    slope=(entropy_contrast(rp,zero)-entropy_contrast(rm,zero))/(2*delta)
    amplitude.append(dict(delta=delta,N=256,count_plus=rp['count'],count_minus=rm['count'],entropy_slope=slope))
check('finite_q_seed_plateau_explicit',len(set(x['count'] for x in cells))==1)
check('do_not_claim_small_seed_continuum',abs(amplitude[-1]['entropy_slope']-tangent)>.1)

fixed_amplitude=[]
dc=.01
smooth=(entropy_contrast(continuum(xi=dc),cont)-entropy_contrast(continuum(xi=-dc),cont))/(2*dc)
for N in [128,512,2048,8192]:
    b=simulate(Model(packets=N,cost_fraction=0.))
    p=simulate(Model(packets=N,xi=dc,cost_fraction=0.))
    n=simulate(Model(packets=N,xi=-dc,cost_fraction=0.))
    slope=(entropy_contrast(p,b)-entropy_contrast(n,b))/(2*dc)
    fixed_amplitude.append(dict(N=N,delta=dc,slope=slope,error_vs_smooth=abs(slope-smooth)))
check('fixed_amplitude_entropy_recovers_continuum',fixed_amplitude[-1]['error_vs_smooth']<.01)

audit=dict(version='0.5',checks_passed=sum(checks.values()),checks=checks,
    verified_inputs=dict(beta=BETA,Gamma=GAMMA,time_unit_seconds=SECONDS,seed_field='entropy',seed_cells=128),
    assumptions=dict(quantum='q=beta/N comoving radiation debit per reference cell',N=256,
        cost_fraction=.01,clock='integrated credit threshold, Gamma(1+xi) C',
        cost_destination='perfect photon-like radiation heat',gate='one finite record token per event; freeze credit when closed',
        endpoint='include threshold exactly at pulse end; retain subthreshold credit, no flush',
        spatial_scope='independent local FLRW cells, no finite-k event junctions'),
    baseline={k:v for k,v in base.items() if k!='events'},
    first_event=base['events'][0],last_event=base['events'][-1],
    independent_clock_max_error=clockerr,time_refinement_M_relative=referr,
    continuum_zero_cost=cont,continuum_with_cost=contcost,convergence=convergence,offgrid_convergence=offgrid,
    cost_effect_M_relative=base['M']/zero['M']-1,capacity7_count=gate['count'],
    negative_controls=negative,smooth_entropy_tangent=tangent,seed_amplitude_scan=amplitude,
    fixed_amplitude_convergence=fixed_amplitude,
    actual_seed=dict(cells=128,min_count=min(x['count'] for x in cells),max_count=max(x['count'] for x in cells),
        max_time_shift=float(np.max(abs(np.array(eventtimes)-np.array([e['time'] for e in base['events']])))),
        entropy_log_RMS=float(np.std(ent)),seed_RMS=float(np.std(seed))),
    scope='Effective deterministic packet timing and recording heat in expanding local FLRW. Not particle quantum mechanics, not a universal energy quantum, not finite-k event/metric/neutrino integration, not new CMB spectra. q and cost are declared closure parameters, not fitted physical constants.')
(O/'audit.json').write_text(json.dumps(audit,indent=2,allow_nan=False)+'\n')
(O/'cells.json').write_text(json.dumps(cells,indent=2)+'\n')
with (O/'events.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=base['events'][0].keys());w.writeheader();w.writerows(base['events'])
print(json.dumps({k:audit[k] for k in ['checks_passed','first_event','last_event','actual_seed','cost_effect_M_relative','smooth_entropy_tangent','seed_amplitude_scan']},indent=2))
