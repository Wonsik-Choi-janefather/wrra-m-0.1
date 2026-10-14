#!/usr/bin/env python3
"""Conditional MCC neutrino synchronization audit; no fitting of integer modes.
Run: python reproduce.py
Requires numpy, scipy, matplotlib. Sources and all frozen inputs are below.
Masses in this file mean rest-energy equivalents, m*c^2, in eV.
"""
from pathlib import Path
import csv, json, math, hashlib
import numpy as np
from scipy.optimize import minimize_scalar, brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
N = np.array([0., 5., 29.])
D = {'21': 25., '31': 841., '32': 816.}
H_SI = 6.62607015e-34
EV_J = 1.602176634e-19
C = 299792458.
HBAR = H_SI / EV_J / (2*math.pi)
BOOK_Q_EV = 1.725929280e-3
ENERGIES_EV = [1e6, 4e6, 1e9]
SOURCES = {
 'model': 'MCC_3_0_Full_Book_KO_v0.12.pdf, pp. 106-107, 113, 130; Library version 2',
 'solar': 'https://arxiv.org/abs/2312.12907',
 'dayabay': 'https://arxiv.org/abs/2211.14988',
 'pdg': 'https://pdg.lbl.gov/2026/reviews/rpp2026-rev-neutrino-mixing.pdf',
 'si': 'https://www.bipm.org/en/publications/si-brochure',
}
# The primary audit uses published normal-ordering parameter summaries, not
# event-level spectra. Their correlations with nuisance parameters are unavailable.
# PDG rows share data: they are sensitivity checks, NOT independent replications.
DATA = [
 {'name':'Solar+KamLAND 2024 / Daya Bay final 2023', 'solar':7.50e-5, 'solar_lo':0.18e-5, 'solar_hi':0.19e-5, 'atm':2.466e-3, 'atm_lo':0.060e-3, 'atm_hi':0.060e-3, 's12':0.307, 's13':(1-math.sqrt(1-0.0851))/2, 'kind':'primary_published_summary_cross_check'},
 {'name':'PDG2026 table14.7 ref193 without SK-ATM/IC24', 'solar':7.49e-5, 'solar_lo':0.20e-5, 'solar_hi':0.19e-5, 'atm':2.459e-3, 'atm_lo':0.023e-3, 'atm_hi':0.025e-3, 's12':0.307, 's13':0.02195, 'kind':'overlapping_global_fit_sensitivity'},
 {'name':'PDG2026 table14.7 ref193 with SK-ATM/IC24', 'solar':7.49e-5, 'solar_lo':0.20e-5, 'solar_hi':0.19e-5, 'atm':2.438e-3, 'atm_lo':0.019e-3, 'atm_hi':0.021e-3, 's12':0.308, 's13':0.02215, 'kind':'overlapping_global_fit_sensitivity'},
 {'name':'PDG2026 table14.7 ref194 with SK-ATM/IC24', 'solar':7.37e-5, 'solar_lo':0.16e-5, 'solar_hi':0.15e-5, 'atm':2.458e-3, 'atm_lo':0.020e-3, 'atm_hi':0.020e-3, 's12':0.303, 's13':0.0223, 'kind':'overlapping_global_fit_sensitivity'},
 {'name':'PDG2026 table14.7 ref195 with SK-ATM', 'solar':7.55e-5, 'solar_lo':0.20e-5, 'solar_hi':0.22e-5, 'atm':2.42e-3, 'atm_lo':0.02e-3, 'atm_hi':0.02e-3, 's12':0.304, 's13':0.0220, 'kind':'overlapping_global_fit_sensitivity'},
]

def audit(row):
 s, a = row['solar'], row['atm']
 qs, qa = math.sqrt(s/25), math.sqrt(a/816)
 r = 816/25
 # Symmetrized marginal errors and zero cross-covariance only for a diagnostic.
 sig_s = (row['solar_lo']+row['solar_hi'])/2
 sig_a = (row['atm_lo']+row['atm_hi'])/2
 sig_res = math.sqrt(sig_a**2+(r*sig_s)**2)
 qs_interval = [math.sqrt((s-row['solar_lo'])/25), math.sqrt((s+row['solar_hi'])/25)]
 qa_interval = [math.sqrt((a-row['atm_lo'])/816), math.sqrt((a+row['atm_hi'])/816)]
 return {
  'name':row['name'], 'kind':row['kind'], 'q_solar_eV':qs, 'q_atmos_eV':qa,
  'q_difference_percent':100*(qa/qs-1), 'q_solar_interval_eV':qs_interval,
  'q_atmos_interval_eV':qa_interval,
  'marginal_1sigma_q_intervals_overlap':max(qs_interval[0],qa_interval[0])<=min(qs_interval[1],qa_interval[1]),
  'pred_dm32_from_solar_eV2':r*s, 'reference_dm32_eV2':a,
  'dm32_relative_error_percent':100*(r*s/a-1),
  'pred_dm21_from_atmos_eV2':a/r, 'reference_dm21_eV2':s,
  'dm21_relative_error_percent':100*(a/r/s-1),
  'approx_residual_sigma_zero_covariance':(r*s-a)/sig_res,
  'q_solar_vs_book_percent':100*(qs/BOOK_Q_EV-1),
 }

def joint_calibration(row):
 # One positive z=q^2; asymmetric marginal summary uncertainties, zero
 # cross-covariance. This is calibration to BOTH inputs, not a holdout test.
 obs=np.array([row['solar'],row['atm']])
 coeff=np.array([25.,816.])
 low=np.array([row['solar_lo'],row['atm_lo']])
 high=np.array([row['solar_hi'],row['atm_hi']])
 def objective(u):
  z=u*1e-6
  residual=coeff*z-obs
  sigma=np.where(residual>=0,high,low)
  return float(np.sum((residual/sigma)**2))
 opt=minimize_scalar(objective,bounds=(2.,4.),method='bounded',options={'xatol':1e-13})
 u=float(opt.x); value=float(opt.fun)
 a=brentq(lambda x:objective(x)-value-1,1.,u,xtol=1e-13)
 b=brentq(lambda x:objective(x)-value-1,u,5.,xtol=1e-13)
 z=u*1e-6
 pred=coeff*z
 sig=np.where(pred>=obs,high,low)
 # The central ratio mismatch cannot be removed with a common scale.
 ratio_observed=row['atm']/row['solar']
 return {'name':row['name'],'kind':'joint_summary_calibration' if row['kind']=='primary_published_summary_cross_check' else row['kind'],'q_joint_eV':math.sqrt(z),
  'q_profile_delta_chi2_1_interval_eV':[math.sqrt(a*1e-6),math.sqrt(b*1e-6)],
  'approx_min_chi2':value,'nominal_degrees_of_freedom':1,
  'pred_dm21_eV2':float(pred[0]),'pred_dm32_eV2':float(pred[1]),
  'solar_central_error_percent':100*(pred[0]/obs[0]-1),
  'atmos_central_error_percent':100*(pred[1]/obs[1]-1),
  'marginal_residual_sigmas':((pred-obs)/sig).tolist(),
  'both_predictions_within_marginal_1sigma':bool(np.all(abs(pred-obs)<=sig)),
  'observed_ratio_dm32_over_dm21':ratio_observed,'fixed_model_ratio':816/25,
  'central_ratio_offset_percent':100*(ratio_observed/(816/25)-1),
  'interpretation':'approximate asymmetric summary fit; zero covariance; joint calibration, not independent validation'}

def h_from_masses(masses, energy):
 # Equal common momentum pc=energy; subtract the common energy stably.
 return masses**2 / (np.sqrt(energy**2+masses**2)+energy)

def pee_from_masses(t_s, masses, energy, s12, s13):
 w=np.array([(1-s12)*(1-s13),s12*(1-s13),s13])
 eig=h_from_masses(masses,energy)
 phase=np.exp(-1j*np.outer(np.atleast_1d(t_s),eig)/HBAR)
 return abs(phase@w)**2

def pee(q, t_s, energy, row):
 return pee_from_masses(t_s,N*q,energy,row['s12'],row['s13'])

def first_full_pee_minimum(q, energy, row):
 # Search the first local minimum of the FULL three-flavour Pee curve.
 masses=N*q
 h=h_from_masses(masses,energy)
 scale=math.pi*HBAR/(h[2]-h[0])
 grid=np.linspace(0,2*scale,3001)
 p=pee(q,grid,energy,row)
 idx=np.flatnonzero((p[1:-1]<p[:-2])&(p[1:-1]<p[2:]))+1
 if len(idx)==0: raise RuntimeError('first minimum not bracketed')
 i=int(idx[0])
 opt=minimize_scalar(lambda u:float(pee(q,u*scale,energy,row)[0]),bounds=(grid[i-1]/scale,grid[i+1]/scale),method='bounded',options={'xatol':1e-12})
 return {'t_s':float(opt.x*scale), 'L_m':float(opt.x*scale*C), 'Pee':float(opt.fun)}

def main():
 audits=[audit(x) for x in DATA]
 joints=[joint_calibration(x) for x in DATA]
 row=DATA[0]
 qs,qa=audits[0]['q_solar_eV'],audits[0]['q_atmos_eV']
 qj=joints[0]['q_joint_eV']
 qlo,qhi=joints[0]['q_profile_delta_chi2_1_interval_eV']
 model_masses=N*qj
 phase_events=[]
 for energy in ENERGIES_EV:
  eig=h_from_masses(model_masses,energy)
  for pair,(j,i) in {'21':(1,0),'31':(2,0),'32':(2,1)}.items():
   dt=float(eig[j]-eig[i])
   tp=math.pi*HBAR/dt
   # Relative phase pi = maximum of this pair's disappearance component.
   # This is NOT generally a minimum of full Pee (interference among 3 terms).
   phase_events.append({'pair':pair,'energy_eV':energy,'delta_integer_squared':D[pair], 't_relative_phase_pi_s':tp,'baseline_m_ultrarelativistic':tp*C,'t_relative_phase_2pi_s':2*tp})
 full_minima={}
 for anchor,q in [('solar_anchor',qs),('atmospheric_anchor',qa),('joint_calibration',qj),('book_scale',BOOK_Q_EV)]:
  full_minima[anchor]=[{'energy_eV':e,**first_full_pee_minimum(q,e,row)} for e in ENERGIES_EV]
 # Reference: measured splittings with identical adopted mixing inputs.
 ref_masses=np.sqrt([0.,row['solar'],row['solar']+row['atm']])
 ref_h=h_from_masses(ref_masses,1e6)
 ref_scale=math.pi*HBAR/(ref_h[2]-ref_h[0])
 ref_min=minimize_scalar(lambda u:float(pee_from_masses(u*ref_scale,ref_masses,1e6,row['s12'],row['s13'])[0]),bounds=(.8,1.2),method='bounded',options={'xatol':1e-12})
 reference_first_minimum={'energy_eV':1e6,'t_s':float(ref_min.x*ref_scale),'L_m':float(ref_min.x*ref_scale*C),'Pee':float(ref_min.fun),'meaning':'computed from published parameters; not a directly measured event timestamp'}
 grids=[np.linspace(0,4e-6,2501),np.linspace(0,120e-6,6001)]
 validation={}
 envelopes={}
 all_curves=[]
 for window,grid in zip(['fast','slow'],grids):
  series={'published_parameter_reference':pee_from_masses(grid,ref_masses,1e6,row['s12'],row['s13']), 'solar_anchor':pee(qs,grid,1e6,row), 'atmospheric_anchor':pee(qa,grid,1e6,row), 'joint_calibration':pee(qj,grid,1e6,row), 'book_scale':pee(BOOK_Q_EV,grid,1e6,row)}
  for name,p in series.items():
   if not(np.all(p>=-1e-12) and np.all(p<=1+1e-12)):raise AssertionError('probability range')
   if abs(float(p[0])-1)>1e-12:raise AssertionError('initial Pee')
  ref=series['published_parameter_reference']
  validation[window]={name:{'max_abs_Pee_difference':float(np.max(abs(p-ref))), 'rms_Pee_difference':float(np.sqrt(np.mean((p-ref)**2)))} for name,p in series.items() if name!='published_parameter_reference'}
  sampled=np.array([pee(q,grid,1e6,row) for q in np.unique(np.r_[np.linspace(qlo,qhi,161),qj])])
  lower,upper=sampled.min(axis=0),sampled.max(axis=0)
  envelopes[window]={'lower':lower,'upper':upper,'reference_pointwise_fraction_inside':float(np.mean((ref>=lower-1e-12)&(ref<=upper+1e-12)))}
  assert np.all(lower<=series['joint_calibration']+1e-12) and np.all(upper>=series['joint_calibration']-1e-12)
  all_curves.append((window,grid,series))
 # Dimensional / convention checks: n^2 differences, probability normalization,
 # SI t->L map, exact Hamiltonian against relativistic limiting phase.
 assert D['31']==D['32']+D['21']
 for x in phase_events:
  t_limit=2*math.pi*HBAR*x['energy_eV']/(x['delta_integer_squared']*qj**2)
  assert abs(x['t_relative_phase_pi_s']/t_limit-1)<1e-12
  assert abs(x['baseline_m_ultrarelativistic']/C/x['t_relative_phase_pi_s']-1)<1e-12
  assert abs(math.sin(math.pi/2)**2-1)<1e-14
 for anchor,items in full_minima.items():
  assert abs((items[1]['t_s']/items[0]['t_s'])/4-1)<1e-7
 # Independent optimizer check: within its active asymmetry branch this fit
 # has a closed weighted least-squares solution for z.
 obs=np.array([row['solar'],row['atm']]); coeff=np.array([25.,816.])
 fitted=coeff*qj**2
 sigma=np.where(fitted>=obs,[row['solar_hi'],row['atm_hi']],[row['solar_lo'],row['atm_lo']])
 z_closed=float(np.sum(coeff*obs/sigma**2)/np.sum(coeff**2/sigma**2))
 assert abs(z_closed/qj**2-1)<1e-7
 assert abs(joints[0]['pred_dm32_eV2']/joints[0]['pred_dm21_eV2']-816/25)<1e-12
 sigma_times={}
 for e in ENERGIES_EV:
  centre=first_full_pee_minimum(qj,e,row)
  lo=first_full_pee_minimum(qhi,e,row)['t_s']
  hi=first_full_pee_minimum(qlo,e,row)['t_s']
  assert lo<centre['t_s']<hi
  sigma_times[str(int(e))]={'central':centre,'conditional_q_only_profile_time_interval_s':[lo,hi]}
 inputs={'modes':N.tolist(),'book_q_eV':BOOK_Q_EV,'sources':SOURCES,'datasets':DATA,'SI_constants':{'h_J_s':H_SI,'electronvolt_J':EV_J,'c_m_s':C,'hbar_eV_s':HBAR},'assumptions':['normal ordering','mass-energy spectrum m_i*c^2=q*n_i','m1=0','coherent vacuum propagation','equal common momentum; pc=stated energy scale','known electron-flavour mixing inputs adopted; not derived','no matter, source spectrum, detector response or raw-event likelihood fit']}
 results={'audits':audits,'phase_events':phase_events,'full_Pee_first_local_minima':full_minima,'reference_first_minimum':reference_first_minimum,'parameter_reference_curve_comparison':validation,'calibrated_solar_masses_eV':model_masses.tolist(),'calibrated_solar_mass_sum_eV':float(sum(model_masses)), 'rest_recurrence_s_solar_scale':2*math.pi*HBAR/qs,'moving_common_recurrence_ultrarelativistic_s_at_1MeV':4*math.pi*HBAR*1e6/qs**2,'linear_rest_phase_control':{'prediction_dm32_equivalent_if_ratio_24_over_5':row['solar']*24/5,'reference_dm32':row['atm'],'relative_error_percent':100*((row['solar']*24/5)/row['atm']-1)},'verification':'numerical checks passed','status':'conditional calibrated correspondence candidate; event identity and common time mapping across domains remain unestablished'}
 # Correct field ownership after moving the main evolution to common q.
 results.pop('calibrated_solar_masses_eV');results.pop('calibrated_solar_mass_sum_eV')
 results.update({'version':'0.2','joint_calibrations':joints,'joint_masses_eV':model_masses.tolist(),'joint_mass_sum_eV':float(sum(model_masses)),'joint_time_profile_intervals':sigma_times,'phase_events_anchor':'joint_calibration','uncertainty_scope':'asymmetric published marginal errors, zero cross-covariance; mixing coefficients fixed; no raw-data likelihood', 'status':'conditional correspondence compatible with summary uncertainties; common scale jointly calibrated; exact central-value matching and event identity not established'})
 results.update({'pointwise_envelope_diagnostic':{k:{'reference_pointwise_fraction_inside':v['reference_pointwise_fraction_inside'],'meaning':'sampled conditional q-only envelope; not a simultaneous confidence test'} for k,v in envelopes.items()},'mode_mapping_diagnostic':{'effective_n3_needed_to_match_both_central_values_with_n2_5':math.sqrt(25*(1+row['atm']/row['solar'])),'integer_n3':29,'note':'diagnostic only; integer modes are not changed; a nonzero difference does not justify a new parameter when observational uncertainties overlap'}})
 inputs.update({'version':'0.2','calibration_policy':'one common q jointly calibrated to both summaries; preserve separate-anchor holdout checks','statistical_assumptions':['asymmetric Gaussian marginal approximation','zero cross-covariance','profile interval delta chi2=1','fixed mixing inputs']})
 (OUT/'frozen_inputs.json').write_text(json.dumps(inputs,indent=2,ensure_ascii=False)+'\n')
 (OUT/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
 with (OUT/'cross_checks.csv').open('w',newline='') as f:
  fields=['name','kind','q_solar_eV','q_atmos_eV','q_difference_percent','pred_dm32_from_solar_eV2','reference_dm32_eV2','dm32_relative_error_percent','pred_dm21_from_atmos_eV2','reference_dm21_eV2','dm21_relative_error_percent','approx_residual_sigma_zero_covariance']
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows([{k:r[k] for k in fields} for r in audits])
 with (OUT/'phase_events.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(phase_events[0]));w.writeheader();w.writerows(phase_events)
 with (OUT/'joint_calibration.csv').open('w',newline='') as f:
  fields=['name','kind','q_joint_eV','approx_min_chi2','pred_dm21_eV2','pred_dm32_eV2','solar_central_error_percent','atmos_central_error_percent','both_predictions_within_marginal_1sigma','central_ratio_offset_percent']
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows([{k:r[k] for k in fields} for r in joints])
 with (OUT/'curves.csv').open('w',newline='') as f:
  names=list(all_curves[0][2]);w=csv.writer(f);w.writerow(['window','time_s',*names,'conditional_q_envelope_lower','conditional_q_envelope_upper'])
  for window,g,s in all_curves:
   for k,t in enumerate(g):w.writerow([window,float(t),*[float(s[n][k]) for n in names],float(envelopes[window]['lower'][k]),float(envelopes[window]['upper'][k])])
 fig,axes=plt.subplots(2,1,figsize=(9,7),layout='constrained')
 styles={'published_parameter_reference':dict(color='black',linewidth=1.7,label='Published-parameter reference'), 'joint_calibration':dict(color='#0072B2',linewidth=1.1,linestyle='--',label='MCC: one jointly calibrated scale')}
 for ax,(window,g,s) in zip(axes,all_curves):
  # A pointwise min-max over the conditional q profile interval. This is
  # NOT a simultaneous confidence band or an experimental error band.
  ax.fill_between(g*1e6,envelopes[window]['lower'],envelopes[window]['upper'],color='#0072B2',alpha=.16,label='Conditional q interval: pointwise envelope')
  for name,style in styles.items():ax.plot(g*1e6,s[name],**style)
  ax.set(xlabel='Laboratory propagation time (microseconds), pc = 1 MeV',ylabel='Electron-flavour survival probability',title=window.capitalize()+' vacuum window')
  ax.grid(alpha=.2)
 axes[0].legend(fontsize=9)
 fig.suptitle('Neutrino synchronization v0.2: fixed integer modes (0, 5, 29)\nCommon calibration with asymmetric summary uncertainties',fontsize=12)
 fig.savefig(OUT/'vacuum_cross_check.png',dpi=160)
 print(json.dumps({'joint_primary':joints[0],'joint_time_1MeV':sigma_times['1000000'],'curve_comparison':validation,'verification':results['verification']},indent=2))

if __name__=='__main__':main()
