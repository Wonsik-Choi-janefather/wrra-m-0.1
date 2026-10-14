#!/usr/bin/env python3
"""Muon-anchored tau partial-rate transfer and finite event-ledger audit.
Run: python reproduce.py. Requires numpy, matplotlib; no online data access.
"""
from pathlib import Path
import csv, hashlib, json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent

def phase(x):
    if x == 0: return 1.0
    if not 0 < x < 1: raise ValueError('Closed/invalid decay channel')
    return 1-8*x+8*x**3-x**4-12*x*x*math.log(x)

def wfactor(parent, daughter, mw):
    return 1 + (3*parent**2+9*daughter**2)/(5*mw**2)

def rates(v, use_w=True, G=1.0):
    me, mm, mt, tm, mw = v
    fm = phase((me/mm)**2)
    rm = wfactor(mm, me, mw) if use_w else 1.0
    # G is a compatibility assumption. It is absorbed by muon calibration.
    coupling = 1/(tm*G*mm**5*fm*rm)
    return np.array([G*coupling*mt**5*phase((ml/mt)**2)*
                     (wfactor(mt, ml, mw) if use_w else 1.0)
                     for ml in (me, mm)])

def propagated_cov(fun, v, sigmas):
    # Linear propagation with independent external input summaries.
    v, sigmas = np.array(v), np.array(sigmas)
    jac = []
    for k, sigma in enumerate(sigmas):
        step = max(abs(v[k])*1e-6, sigma*.1)
        plus, minus = v.copy(), v.copy()
        plus[k] += step; minus[k] -= step
        jac.append((np.asarray(fun(plus))-np.asarray(fun(minus)))/(2*step))
    J = np.asarray(jac).T
    return (J*sigmas**2) @ J.T

def write_csv(name, rows):
    with (ROOT/name).open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def main():
    cfg=json.loads((ROOT/'frozen_inputs.json').read_text())
    v=np.array([cfg[k]['value'] for k in ('me_MeV','mmu_MeV','mtau_MeV','tmu_s','mW_MeV')])
    sig=np.array([cfg[k]['sigma'] for k in ('me_MeV','mmu_MeV','mtau_MeV','tmu_s','mW_MeV')])
    tt, st = cfg['ttau_s']['value'], cfg['ttau_s']['sigma']
    pred=rates(v); pcov=propagated_cov(rates,v,sig)
    rows=[]; comparisons={}
    for dataset, d in cfg['branching_datasets'].items():
        b=np.array(d['values']); sb=np.array(d['sigmas']); obs=b/tt
        for i, channel in enumerate(('electron','muon')):
            os=math.sqrt((sb[i]/tt)**2+(b[i]*st/tt**2)**2)
            cs=math.sqrt(os**2+pcov[i,i])
            row=dict(dataset=dataset,channel=channel,predicted_rate_s_inv=float(pred[i]),
                     observed_rate_s_inv=float(obs[i]),prediction_input_sigma=float(math.sqrt(pcov[i,i])),
                     observation_sigma=os,relative_error_percent=float(100*(pred[i]/obs[i]-1)),
                     marginal_residual_sigma=float((pred[i]-obs[i])/cs),
                     predicted_inverse_partial_rate_ps=float(1e12/pred[i]),
                     observed_inverse_partial_rate_ps=float(1e12/obs[i]),
                     implied_branching_percent=float(100*pred[i]*tt))
            rows.append(row)
        rp=pred[1]/pred[0]; ro=b[1]/b[0]
        # Known experimental branch covariance only; shared lifetime cancels in ratio.
        rho=d.get('rho_e_mu')
        rr=dict(predicted=float(rp),observed=float(ro),known_branch_correlation=rho)
        rr['secondary_tau_e_normalization_multiplier']=float(obs[0]/pred[0])
        rr['secondary_tau_mu_holdout_relative_error_percent']=float(100*(rp/ro-1))
        rr['secondary_tau_mu_implied_branching']=float(b[0]*rp)
        rr['secondary_scope']='Separate additional calibration to tau electron channel; not part of the primary muon-only transfer.'
        if rho is not None:
            bcov=np.diag(sb**2); bcov[0,1]=bcov[1,0]=rho*sb.prod()
            J=np.array([-b[1]/b[0]**2,1/b[0]])
            rs=math.sqrt(float(J@bcov@J))
            rJ=np.array([-pred[1]/pred[0]**2,1/pred[0]])
            rps=math.sqrt(max(0,float(rJ@pcov@rJ)))
            rr.update(observed_sigma=rs,prediction_input_sigma=rps,
                      residual_sigma=float((rp-ro)/math.hypot(rs,rps)))
            ocov=bcov/tt**2+np.outer(b,b)*st**2/tt**4
            residual=pred-obs
            rr['two_channel_chi2_with_known_branch_covariance']=float(residual@np.linalg.solve(ocov+pcov,residual))
            rr['chi2_scope']='measurement/input-summary diagnostic, theory truncation excluded; lifetime independent of branching assumed'
        else:
            # No fabricated HFLAV / PDG-average covariance or combined significance.
            rr['sigma_range_for_all_possible_branch_correlations']=[
                float(ro*abs(sb[1]/b[1]-sb[0]/b[0])),
                float(ro*(sb[1]/b[1]+sb[0]/b[0]))]
        comparisons[dataset]=rr
    write_csv('rate_comparison.csv',rows)

    # Operational finite event mapping: resolution is chosen, not predicted.
    # Muon survival at 2**k ticks equals exp(-1); tau uses the same SI tick.
    # The unmodelled tau channels are closed USING the measured total lifetime.
    total=1/tt; other=total-pred.sum()
    if other < 0: raise ValueError('Negative residual rate: closure fails')
    hazards=np.r_[pred,other]
    finite=[]; rng=np.random.default_rng(20261014); population=1_000_000
    for k in (24,28,32):
        dt=v[3]/2**k
        n=round(tt/dt); elapsed=n*dt
        per_tick=-math.expm1(-total*dt)*hazards/total
        stay=math.exp(-total*dt)
        state=np.array([1.0,0,0,0])
        for _ in range(n):
            moved=state[0]*per_tick
            state[1:]+=moved; state[0]*=stay
        analytic=np.r_[math.exp(-total*elapsed),
                       -math.expm1(-total*elapsed)*hazards/total]
        assert np.min(state)>=0 and abs(state.sum()-1)<1e-11
        assert np.max(abs(state-analytic))<1e-11
        # Integer cohorts use the same categorical transition; parent is debited once.
        ledger=np.array([population,0,0,0],dtype=np.int64)
        for _ in range(n):
            draw=rng.multinomial(int(ledger[0]),np.r_[stay,per_tick])
            ledger[0]=draw[0]; ledger[1:]+=draw[1:]
        assert ledger.sum()==population
        # Each complete daughter cohort retains the parent rest-energy budget,
        # including invisible neutrinos. No spectra/daughter energy split is generated.
        energy_initial=population*v[2]
        energy_final=ledger[0]*v[2]+ledger[1:].sum()*v[2]
        assert abs(energy_final-energy_initial)<1e-6
        euler_survival=(1-total*dt)**n if total*dt<1 else float('nan')
        finite.append(dict(ticks_per_muon_lifetime=2**k,dt_s=float(dt),tau_ticks=n,
          elapsed_s=float(elapsed),survival=float(state[0]),analytic_survival=float(analytic[0]),
          max_probability_error=float(max(abs(state-analytic))),
          first_order_Euler_survival=euler_survival,
          Euler_survival_error=float(euler_survival-analytic[0]),
          integer_survivors=int(ledger[0]),integer_e_cohorts=int(ledger[1]),
          integer_mu_cohorts=int(ledger[2]),integer_other_cohorts=int(ledger[3]),
          leptonic_charged_daughters=int(ledger[1]+ledger[2]),
          leptonic_neutrino_daughters=int(2*(ledger[1]+ledger[2])),
          integer_count_error=int(ledger.sum()-population),aggregate_energy_error_MeV=float(energy_final-energy_initial)))
    write_csv('finite_event_ledger.csv',finite)

    prior=json.loads((ROOT/'prior_time_anchor.json').read_text())
    gs=[.5,1.,2.,prior['G']]
    scaling=[dict(G=g,rate_e=float(rates(v,G=g)[0]),rate_mu=float(rates(v,G=g)[1])) for g in gs]
    assert all(np.allclose(rates(v,G=g),pred,rtol=1e-14,atol=0) for g in gs)
    hbar=cfg['h_J_s']/cfg['e_J_per_eV']/(2*math.pi)
    result=dict(version='0.1',anchor='Muon mean lifetime; tau partial rates not used for calibration',
      baseline='Adopted SM m^5 phase space plus leading finite-W correction. Universal fixed-alpha, massless O(alpha) QED factor cancels.',
      theory_limits='No channel-dependent finite-mass QED, running-alpha/higher-order QED, full weak radiative corrections, or hadronic rate prediction. No full precision SM calculation.',
      rates=rows,ratio_comparisons=comparisons,prediction_input_covariance=pcov.tolist(),
      tree_phase_space_rates_s_inv=rates(v,use_w=False).tolist(),
      finite_W_relative_change_percent=(100*(pred/rates(v,use_w=False)-1)).tolist(),
      tau_leptonic_total_fraction_using_measured_total_lifetime=float(pred.sum()*tt),
      other_rate_closed_with_measured_tau_total_s_inv=float(other),
      total_tau_lifetime_predicted=False,finite_event_ledger=finite,
      common_G_rescaling=scaling,common_G_independently_identified=False,
      adopted_hbar_eVs=hbar,muon_width_eV=float(hbar/v[3]),
      tau_predicted_partial_widths_eV=(hbar*pred).tolist(),
      prior_time_anchor=prior,
      tau_rates_used_for_primary_calibration=False,weak_normalization_independently_predicted=False,
      independence_explanation='Muon calibrates the weak normalization; tau summaries are comparison inputs. ALEPH/L3 also contribute to PDG/HFLAV and cannot be counted as additional independent validations.',
      falsification='Wrong frozen tau partial rates beyond measurement uncertainty and documented theory truncation; negative probabilities or residual rates; omitted cohorts/energy; failed resolution convergence. Common-G universality requires a separate nondegenerate test.',
      verdict='Operational muon-to-tau time/rate transfer is compatible at current summary precision. It uses an adopted weak-interaction module, not a SOURCE derivation or proof of arithmetic/physical event identity.')
    (ROOT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

    # Plot scientific comparison, not a speculative illustration.
    fig,axs=plt.subplots(1,2,figsize=(10,4.4),layout='constrained')
    mainrows=[r for r in rows if r['dataset']=='PDG2026_HFLAV']
    for i,r in enumerate(mainrows):
        axs[0].errorbar(i-.07,r['observed_rate_s_inv']/1e11,yerr=r['observation_sigma']/1e11,fmt='o',color='#2563eb',label='Observed summary' if i==0 else None,capsize=4)
        axs[0].errorbar(i+.07,r['predicted_rate_s_inv']/1e11,yerr=r['prediction_input_sigma']/1e11,fmt='s',color='#b45309',label='Muon transfer (truncated)' if i==0 else None,capsize=4)
    axs[0].set(xticks=[0,1],xticklabels=['Tau → electron','Tau → muon'],ylabel='Partial rate (10¹¹ s⁻¹)',title='Frozen muon anchor → tau channels')
    axs[0].legend(fontsize=8); axs[0].grid(axis='y',alpha=.25)
    axs[1].plot([x['dt_s']/1e-15 for x in finite],[abs(x['Euler_survival_error']) for x in finite],'o-',label='First-order survival error')
    axs[1].set(xscale='log',yscale='log',xlabel='Common tick (fs)',ylabel='Absolute survival error',title='Resolution audit at ≈ one tau lifetime')
    axs[1].grid(alpha=.25); axs[1].legend(fontsize=8)
    fig.savefig(ROOT/'muon_tau_audit.png',dpi=180); plt.close(fig)
    (ROOT/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name+'\n' for f in sorted(ROOT.iterdir()) if f.is_file() and f.name!='SHA256SUMS.txt'))
    print(json.dumps(dict(primary=mainrows,ratio=comparisons['PDG2026_HFLAV'],ledger_checks='passed',G_identifiable=False),ensure_ascii=False,indent=2))

if __name__=='__main__': main()
