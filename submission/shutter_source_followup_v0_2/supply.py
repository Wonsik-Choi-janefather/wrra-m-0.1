"""Actual address variance, explicit temporal correlation and refresh ledger."""
import math,json
import numpy as np
from scipy.special import xlogy
from common import IN,OUT,CFG,DT,C,csvwrite,save,checks_pass

def averaging_factor(N,r):
    """Var(mean)/Var(one) for stationary renewal autocov (1-r)^lag.
    Small-r series avoids catastrophic cancellation in the closed expression.
    """
    if int(N)!=N or N<1 or not np.isfinite(r) or not 0<=r<=1:
        raise ValueError('N must be a positive integer and 0 <= r <= 1')
    N=int(N)
    if N<=1 or r==0:return 1.
    if r==1:return 1./N
    # Var(mean)/V=[N*(2/r-1)-2*(1-r)*(1-(1-r)^N)/r^2]/N^2.
    if N*r<.05:
        # Finite expansion of weighted binomial moments, exact to truncation.
        # coefficient sum_(lag=1)^(N-1) (N-lag)*binom(lag,k)=binom(N+1,k+2).
        total=np.longdouble(1)
        term=-np.longdouble(r)*(N*N-1)/(3*N)
        total+=term
        for k in range(1,15):
            term*= -np.longdouble(r)*(N-k-1)/(k+3)
            total+=term
        return float(total)
    q=np.longdouble(1)-np.longdouble(r)
    diff=-np.expm1(np.longdouble(N)*np.log1p(-np.longdouble(r)))
    value=(np.longdouble(N)*(2/np.longdouble(r)-1)-2*q*diff/np.longdouble(r)**2)/np.longdouble(N)**2
    return float(value)

def threshold_count(r,ratio2):
    if not np.isfinite(r) or not 0<=r<=1 or not np.isfinite(ratio2) or ratio2<0:
        raise ValueError('Invalid refresh probability or variance ratio')
    if ratio2<=1:return 1
    if r==0:return None
    lo=1;hi=max(2,math.ceil(ratio2*(2/r-1)))
    while averaging_factor(hi,r)>1/ratio2:hi*=2
    while hi-lo>1:
        mid=(hi+lo)//2
        if averaging_factor(mid,r)>1/ratio2:lo=mid
        else:hi=mid
    return hi

def entropy(p):return -xlogy(p,p)-xlogy(1-p,1-p)

def main():
    archive=np.load(IN/'addresses.npz');n=archive['addresses'][1:]
    w=archive['address_weights'][1:];e=archive['sector_effects'][1:].T
    cfg=json.loads((IN/'source_config.json').read_text())
    eta=np.array(cfg['eta_J_m3']);gap=2*np.cos(np.pi/8)
    contributions=e*w[None,:]*(1+np.array([0,.25,0])[:,None]*np.log(n)[None,:]/np.log(n[-1]))
    prep=np.load(IN/'finite_preparation.npz');p=prep['probability']
    mask=np.arange(30)%3!=0;addrmask=n%3!=0
    squared=np.array([np.bincount(n%30,weights=x*x,minlength=30) for x in contributions])
    variance=(eta[:,None]*gap)**2*(squared[:,mask]@(p[mask]*(1-p[mask])))
    variance[0]=0
    means=prep['mean_total_energy'].mean(1)
    relative_rms=np.sqrt(variance.mean(1))/means
    phase_cov=np.cov(prep['dimensionless_fluctuation'][1:],bias=True)
    phase_rms=np.sqrt(np.diag(phase_cov))
    # One supplier bit per address: test actual sector ownership and cross variance.
    cross_by_r=np.bincount(n%30,weights=contributions[1]*contributions[2],minlength=30)
    cross_var=eta[1]*eta[2]*gap*gap*(cross_by_r[mask]@(p[mask]*(1-p[mask])))
    counts=np.bincount(n[addrmask]%30,minlength=30)
    joint_weights=(eta[:,None]*gap*contributions);joint_weights[0]=0
    total_weights=joint_weights.sum(0)
    absolute_by_r=np.bincount(n%30,weights=abs(total_weights),minlength=30)
    sq_total_by_r=np.bincount(n%30,weights=total_weights**2,minlength=30)
    rows=[];resource_rows=[]
    for r in CFG['supply']['refresh_probabilities_per_physical_shutter']:
        h_rate=(1-p)*entropy(r*p)+p*entropy(r*(1-p))
        path_entropy_per_transition=float(np.sum(counts[mask]*h_rate[mask].mean(1)))
        fresh_state_entropy_per_transition=float(r*np.sum(counts[mask]*entropy(p[mask]).mean(1)))
        # Expected absolute conditional energy turnover, not net energy depletion.
        absolute_turnover=float(2*r*np.sum(absolute_by_r[mask]*(p[mask]*(1-p[mask])).mean(1)))
        net_change_var=float(2*r*np.sum(sq_total_by_r[mask]*(p[mask]*(1-p[mask])).mean(1)))
        for index,sector in enumerate(['D','R'],start=1):
            ratio2=(relative_rms[index]/phase_rms[index-1])**2
            N=threshold_count(r,ratio2)
            time=None if N is None else N*DT
            row=dict(sector=sector,refresh_probability=r,one_frame_relative_RMS=float(relative_rms[index]),
                target_mean_profile_relative_RMS=float(phase_rms[index-1]),
                threshold_shutters=None if N is None else str(N),averaging_time_s=time,
                equivalent_light_distance_m=None if time is None else C*time,
                averaged_intrinsic_relative_RMS=None if N is None else float(relative_rms[index]*math.sqrt(averaging_factor(N,r))),
                retained_total_relative_RMS=None if N is None else float(math.sqrt(relative_rms[index]**2*averaging_factor(N,r)+phase_rms[index-1]**2)),
                correlation_law='Static' if r==0 else '(1-r)^lag; declared renewal law')
            rows.append(row)
            resource_rows.append(dict(sector=sector,refresh_probability=r,
                address_supply_bits=int(addrmask.sum()),initial_supplier_entropy_nats=float(np.sum(counts[mask]*entropy(p[mask]).mean(1))),
                threshold_shutters=None if N is None else str(N),
                expected_fresh_bit_preparations_at_threshold=None if N is None else int(addrmask.sum())*r*(N-1),
                new_state_entropy_at_threshold_nats=None if N is None else fresh_state_entropy_per_transition*(N-1),
                conditional_path_entropy_if_history_recorded_nats=None if N is None else path_entropy_per_transition*(N-1),
                mean_absolute_energy_turnover_density_per_shutter_J_m3=absolute_turnover,
                absolute_energy_turnover_density_rate_W_m3=absolute_turnover/DT,
                signed_energy_transfer_density_RMS_per_shutter_J_m3=math.sqrt(net_change_var),
                accumulated_absolute_turnover_at_threshold_J_m3=None if N is None else absolute_turnover*(N-1),
                budget_status='No per-shutter reservoir budget supplied; throughput is not assumed free or irreversibly consumed'))
    checks={}
    prior=json.loads((IN/'preparation_results.json').read_text())
    checks['actual_intrinsic_RMS_reproduced']=np.max(abs(relative_rms-np.array(prior['independent_supplier_intrinsic_relative_RMS_P_D_R'])))<1e-13
    checks['actual_variance_array_reproduced']=np.max(abs(variance-prep['intrinsic_supplier_variance']))<1e-34
    checks['phase_mean_covariance_reproduced']=np.max(abs(phase_cov-np.array(prior['covariance_finite_phase'])))<1e-30
    checks['sector_ownership_makes_intrinsic_DR_covariance_zero']=np.max(abs(cross_var))<1e-40
    for r in [0,.001,1/128,.2,1]:
        for N in [1,2,5,64,128]:
            lag=np.arange(1,N);direct=(N+2*np.sum((N-lag)*(1-r)**lag))/N**2
            checks[f'correlation_sum_N{N}_r{r:g}']=abs(averaging_factor(N,r)-direct)<1e-12
    for row in rows:
        if row['threshold_shutters']:
            N=int(row['threshold_shutters']);r=row['refresh_probability'];i=1 if row['sector']=='D' else 2
            target=(phase_rms[i-1]/relative_rms[i])**2
            checks[f'threshold_bracket_{row["sector"]}_r{r:g}']=averaging_factor(N,r)<=target*(1+2e-15) and averaging_factor(N-1,r)>=target*(1-2e-15)
    # Controlled-bit Monte Carlo is an independent check of the temporal law,
    # not a simulation of 10^15 physical shutters or the full million addresses.
    rng=np.random.default_rng(20261014);runs=60000;N=128;r=1/128
    z=rng.integers(0,2,runs);sums=z.copy().astype(float);changes=0
    for step in range(1,N):
        old=z.copy();refresh=rng.random(runs)<r
        z[refresh]=rng.integers(0,2,int(refresh.sum()))
        changes+=int(np.abs(z-old).sum());sums+=z
    sample_var=float(np.var(sums/N));exact=.25*averaging_factor(N,r)
    checks['Monte_Carlo_renewal_mean_variance']=abs(sample_var/exact-1)<.015
    # Independent sample checks required conditional energy turnover for a bit
    # with unit level gap, before multiplying actual address/sector energies.
    empirical_turnover=changes/(runs*(N-1))
    analytic_turnover=2*r*.5*(1-.5)
    checks['Monte_Carlo_energy_turnover']=abs(empirical_turnover/analytic_turnover-1)<.02
    u_total=float(means.sum())
    total_var=float(variance.mean(1).sum()+2*cross_var.mean())
    h_sensitivity=.5*math.sqrt(total_var)/u_total
    result=dict(validation_inputs=dict(actual_addresses=len(n)+1,controlled_supply_bits=int(addrmask.sum()),
        shutter_dt_s=DT,relative_intrinsic_RMS_P_D_R=relative_rms.tolist(),
        mean_profile_RMS_D_R=phase_rms.tolist()),
        WRRA_transformation=CFG['supply'],outputs=dict(averaging_boundaries=rows,
            resource_ledger=resource_rows,phase_mean_variance_floor=phase_rms.tolist(),
            one_frame_conditional_linear_Friedmann_H_relative_RMS=h_sensitivity,
            gravity_status='Dust/vacuum algebraic local linear sensitivity only; outside controlled small-noise regime, not a dynamical stochastic-gravity noise prediction',
            linear_gravity_small_noise_control_passed=bool(h_sensitivity<.1),
            Monte_Carlo_control=dict(runs=runs,steps=N,sample_variance=sample_var,analytic_variance=exact,
                empirical_unit_gap_energy_turnover=empirical_turnover,analytic_unit_gap_energy_turnover=analytic_turnover)),
        refutation_conditions=['False temporal independence','Unaccounted fresh memory, reset or reservoir flux','Failure of source plus reservoir conservation','Averaging with an unchanged state claimed to suppress intrinsic variance'],
        conclusion='Independent-shutter microsecond thresholds reproduced, but not selected by the inherited snapshot. Static bits do not average down. Finite correlations lengthen the threshold and require explicit refresh resources.',
        checks=checks_pass(checks))
    csvwrite('supply_averaging_boundaries.csv',rows);csvwrite('supply_refresh_resource_ledger.csv',resource_rows)
    save('supply_results.json',result)
    np.savez_compressed(OUT/'supply_covariance.npz',intrinsic_variance_by_phase=variance,
        phase_mean_covariance=phase_cov,relative_intrinsic_RMS=relative_rms,conditional_DR_variance=cross_var)
    print('Supply:',len(result['checks']),'checks passed',flush=True)
    return result

if __name__=='__main__':main()
