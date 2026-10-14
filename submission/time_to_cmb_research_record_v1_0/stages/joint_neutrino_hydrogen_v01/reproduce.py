#!/usr/bin/env python3
"""Coupled neutrino/hydrogen clock-bridge audit with explicit frozen anchors.
Run: python reproduce.py. numpy, scipy, matplotlib required.
"""
from pathlib import Path
import math,json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import neutrino_module as nu
import hydrogen_module as hy

OUT=Path(__file__).resolve().parent
ME_EV=510998.95069
ME_SIGMA_EV=.00016
ME_MP=5.446170214889e-4
ME_MP_SIGMA=9.4e-15
MU_RATIO=1/(1+ME_MP)
A0=ME_EV*MU_RATIO*hy.ALPHA**2/(2*hy.H_EV)
Q0=nu.BOOK_Q_EV
BETHE={(1,0):2.984128556,(2,0):2.811769893,(3,0):2.767663612,(8,2):-.008785043}
PHASE_NU=Q0**2*np.array([25.,816.])

def leading_self_energy_Hz(state):
 n,l,j=state
 logk=BETHE[(n,l)]
 pref=hy.ALPHA**5*ME_EV/(math.pi*hy.H_EV*n**3)
 if l==0:
  return pref*MU_RATIO**3*(4/3*math.log(1/(MU_RATIO*hy.ALPHA**2))+10/9-4/3*logk)
 kappa=2*(l-j)*(j+.5)
 return pref*(-MU_RATIO**3*4/3*logk-MU_RATIO**2/(2*kappa*(2*l+1)))

def matrix_h(include_se):
 base=np.array([A0*hy.dirac_coeff(r) for r in hy.DATA])
 if include_se:
  base+=np.array([leading_self_energy_Hz(r['hi'])-leading_self_energy_Hz(r['lo']) for r in hy.DATA])
 return np.column_stack([base,[hy.s_shift_coeff(r) for r in hy.DATA]])

def fit_model(include_se):
 row=nu.DATA[0]
 mh=matrix_h(include_se)
 yh=np.array([r['frequency_Hz'] for r in hy.DATA])
 sh=np.array([r['sigma_Hz'] for r in hy.DATA])
 yn=np.array([row['solar'],row['atm']])
 mn=np.column_stack([PHASE_NU,np.zeros(2)])
 # Hydrogen's first two transitions calibrate (common phase rate G, residual
 # S-level coefficient). Neutrino quantities and H 2S-8D are initially held out.
 theta=np.linalg.solve(mh[:2],yh[:2])
 transfer_pred_n=mn@theta
 transfer_pred_h=mh@theta
 sn=np.where(transfer_pred_n>=yn,[row['solar_hi'],row['atm_hi']],[row['solar_lo'],row['atm_lo']])
 # Joint training: the two neutrino summary values plus two H anchors.
 # The 2S-8D transition remains held out throughout.
 X=np.vstack([mn,mh[:2]]);y=np.r_[yn,yh[:2]];sig=np.r_[sn,sh[:2]]
 scale=np.array([1e-9,1e6])
 for _ in range(3):
  residual=y-X@theta
  weighted=X*scale/sig[:,None]
  dp=np.linalg.lstsq(weighted,residual/sig,rcond=None)[0]
  theta+=scale*dp
  pn=mn@theta
  sn=np.where(pn>=yn,[row['solar_hi'],row['atm_hi']],[row['solar_lo'],row['atm_lo']])
  sig=np.r_[sn,sh[:2]]
 covariance_p=np.linalg.inv(weighted.T@weighted)
 cov=scale[:,None]*covariance_p*scale[None,:]
 pn=mn@theta;ph=mh@theta
 nres=(pn-yn)/sn
 hres=ph-yh
 hsigma=math.sqrt(float(mh[2]@cov@mh[2]))
 comb=math.sqrt(hsigma**2+sh[2]**2)
 train_res=(X@theta-y)/sig
 assert theta[0]>0 and np.all(ph>0)
 assert abs(theta[0]-float(np.linalg.solve(mh[:2],yh[:2])[0]))<1e-9
 return {'model':'Dirac + leading self energy + common S residual' if include_se else 'Dirac + common S residual',
  'include_leading_self_energy':include_se,'G_common_phase_rate':float(theta[0]),'L_residual_Hz':float(theta[1]),
  'G_conditional_sigma_from_summaries':math.sqrt(float(cov[0,0])),
  'transfer_neutrino_predictions_eV2':transfer_pred_n.tolist(),
  'joint_neutrino_predictions_eV2':pn.tolist(),'neutrino_reference_eV2':yn.tolist(),
  'neutrino_relative_error_percent':(100*(pn/yn-1)).tolist(),'neutrino_marginal_residual_sigmas':nres.tolist(),
  'neutrino_both_within_marginal_1sigma':bool(np.all(abs(nres)<=1)),
  'hydrogen_predictions_Hz':ph.tolist(),'hydrogen_residuals_Hz':hres.tolist(),
  'hydrogen_heldout_residual_Hz':float(hres[2]),'hydrogen_heldout_relative_residual_ppm':float(hres[2]/yh[2]*1e6),
  'hydrogen_heldout_prediction_sigma_Hz':hsigma,'hydrogen_heldout_combined_summary_sigma_Hz':comb,
  'hydrogen_heldout_within_3sigma':bool(abs(hres[2])<=3*comb),
  'approx_training_chi2':float(train_res@train_res),'training_measurements':4,'fitted_parameters':2,
  'held_out':'Hydrogen 2S-8D5/2','fit_scope':'frozen Q0 and electron-based A0; zero cross covariance; incomplete atomic theory',
  'atomic_phase_cycle_s':float(1/ph[2]),
  'neutrino_first_Pee_minimum_1MeV_s':nu.first_full_pee_minimum(Q0*math.sqrt(theta[0]),1e6,row)['t_s']}

def degeneracy_audit():
 # Prior unanchored model: G*q^2 and G*A,G*L are the only observable combinations.
 row=nu.DATA[0];q=nu.joint_calibration(row)['q_joint_eV']
 M=np.array([[hy.dirac_coeff(r),hy.s_shift_coeff(r)] for r in hy.DATA])
 y=np.array([r['frequency_Hz'] for r in hy.DATA]);A,L=np.linalg.solve(M[:2],y[:2])
 original_n=q*q*np.array([25.,816.]);original_h=M@np.array([A,L])
 profiles=[]
 for G in [.5,.75,1.,1.25,1.5,2.]:
  qg=q/math.sqrt(G);Ag=A/G;Lg=L/G
  pn=G*qg*qg*np.array([25.,816.]);ph=G*(M@np.array([Ag,Lg]))
  rn=float(np.max(abs(pn/original_n-1)));rh=float(np.max(abs(ph/original_h-1)))
  assert rn<1e-12 and rh<1e-12
  profiles.append({'G':G,'q_eV':qg,'A_Hz':float(Ag),'L_Hz':float(Lg),'nu_max_relative_change':rn,'H_max_relative_change':rh})
 return {'analytic_null_direction':'d log G=+a; d log(q^2)=d log A=d log L=-a','parameters':4,'identifiable_combinations':3,'clock_identifiable_with_all_energy_scales_free':False,'profiles':profiles}

def main():
 degeneracy=degeneracy_audit()
 old=fit_model(False);new=fit_model(True)
 gain=abs(old['hydrogen_heldout_residual_Hz']/new['hydrogen_heldout_residual_Hz'])
 # Leading SE is an external fixed physical correction, not a new coefficient
 # fitted to the held-out transition. Unit and sign checks.
 assert leading_self_energy_Hz([1,0,.5])>0
 assert leading_self_energy_Hz([2,0,.5])>0
 assert math.isfinite(gain)
 se_rows=[{'state':str(s),'leading_self_energy_Hz':leading_self_energy_Hz(s)} for s in [[1,0,.5],[2,0,.5],[3,0,.5],[8,2,2.5]]]
 anchor_relative_sigma=math.sqrt((ME_SIGMA_EV/ME_EV)**2+(2*hy.ALPHA_SIGMA/hy.ALPHA)**2+(ME_MP_SIGMA/(1+ME_MP))**2)
 inputs={'version':'0.1','frozen_Q0_eV':Q0,'frozen_electron_energy_eV':ME_EV,'electron_energy_sigma_eV':ME_SIGMA_EV,'electron_proton_mass_ratio':ME_MP,'A0_Hz_from_electron_alpha_reduced_mass':A0,'Bethe_logarithms':{str(k):v for k,v in BETHE.items()},'neutrino_data':nu.DATA[0],'hydrogen_data':hy.DATA,'self_energy_source':'https://pml.nist.gov/cuu/pdf/RevModPhys_80_000633acc.pdf, Sec. IV.A.1.d, Table VII; leading A41/A40, reduced-mass factors','constants_source':'https://physics.nist.gov/cuu/pdf/all.pdf','common_clock_hypothesis':'one multiplicative lab phase-rate G across both domains with frozen physical energy anchors','limitations':['Q0 originally calibrated, not independent of historical neutrino data','CODATA constants have correlated adjustments, some using hydrogen spectroscopy','summary data instead of raw likelihoods','incomplete atomic QED/recoil/nuclear-size corrections','atomic rational code not derived from SOURCE grammar','G is a compatibility parameter, not a derivation of time or Planck constant']}
 results={'degeneracy_audit':degeneracy,'models':[old,new],'hydrogen_holdout_improvement_factor':gain,'leading_self_energy_states':se_rows,'frozen_energy_anchor_relative_sigma_zero_covariance_diagnostic':anchor_relative_sigma,'common_G_error_scope':'reported G sigma conditions on frozen constants; external anchor uncertainty and theory truncation are not included','validation':'rescaling degeneracy, adopted units, positive frequencies and frozen-anchor reconstruction checked','conclusion':'joint tuning is conditional and useful; neutrino summaries compatible, H holdout improves but precision reproduction remains incomplete; no unique universal arithmetic clock established'}
 (OUT/'frozen_inputs.json').write_text(json.dumps(inputs,indent=2,ensure_ascii=False)+'\n')
 (OUT/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
 with (OUT/'joint_results.csv').open('w',newline='') as f:
  fields=['model','G_common_phase_rate','L_residual_Hz','hydrogen_heldout_residual_Hz','hydrogen_heldout_relative_residual_ppm','hydrogen_heldout_within_3sigma','neutrino_both_within_marginal_1sigma','atomic_phase_cycle_s','neutrino_first_Pee_minimum_1MeV_s']
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows([{k:r[k] for k in fields} for r in [old,new]])
 with (OUT/'degeneracy_profiles.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(degeneracy['profiles'][0]));w.writeheader();w.writerows(degeneracy['profiles'])
 fig,axes=plt.subplots(1,2,figsize=(10,4.8),layout='constrained')
 axes[0].plot([p['G'] for p in degeneracy['profiles']],[max(p['nu_max_relative_change'],p['H_max_relative_change']) for p in degeneracy['profiles']],marker='o')
 axes[0].set(xlabel='Common phase-rate G, energy scales free',ylabel='Maximum relative observable change',title='Unanchored clock is non-identifiable')
 vals=[abs(old['hydrogen_heldout_residual_Hz']),abs(new['hydrogen_heldout_residual_Hz'])]
 axes[1].bar(['Previous\nS residual','Leading SE\n+ S residual'],vals,color=['#999999','#0072B2'])
 axes[1].set_yscale('log');axes[1].set(ylabel='Held-out hydrogen residual (Hz)',title='Added state-dependent physical correction')
 for i,v in enumerate(vals):axes[1].text(i,v*1.15,f'{v/1e6:.3f} MHz',ha='center')
 axes[1].axhline(2000,color='#D55E00',linestyle='--',label='Measurement sigma only');axes[1].legend(fontsize=8)
 axes[1].set_ylim(1e3,max(vals)*3)
 for ax in axes:ax.grid(axis='y',alpha=.2)
 fig.savefig(OUT/'joint_audit.png',dpi=150)
 print(json.dumps({'degeneracy':degeneracy['clock_identifiable_with_all_energy_scales_free'],'models':[old,new],'holdout_improvement_factor':gain},indent=2))

if __name__=='__main__':main()
