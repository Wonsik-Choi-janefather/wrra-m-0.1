#!/usr/bin/env python3
"""Hydrogen event synchronization candidate: calibrate, freeze, cross-check.
Adopted Coulomb/Dirac spectral templates; NOT derived from the MCC source grammar.
Run python reproduce.py; requires numpy and matplotlib.
"""
from pathlib import Path
from fractions import Fraction
import math,json,csv,hashlib,zipfile
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parent
ALPHA=7.2973525643e-3
ALPHA_SIGMA=1.1e-12
H_SI=6.62607015e-34
EV_J=1.602176634e-19
C=299792458.
H_EV=H_SI/EV_J
DATA=[
 {'label':'1S-2S','lo':[1,0,.5],'hi':[2,0,.5],'frequency_Hz':2466061413187035.,'sigma_Hz':10.,'source':'https://arxiv.org/abs/1107.3101','convention':'hyperfine centroid; total two-photon transition frequency'},
 {'label':'1S-3S','lo':[1,0,.5],'hi':[3,0,.5],'frequency_Hz':2922743278671500.,'sigma_Hz':2600.,'source':'https://arxiv.org/pdf/1801.08816','convention':'hyperfine centroid; total two-photon transition frequency'},
 {'label':'2S-8D5/2','lo':[2,0,.5],'hi':[8,2,2.5],'frequency_Hz':770649561570900.,'sigma_Hz':2000.,'source':'https://arxiv.org/abs/2111.08554','convention':'hyperfine centroid; total two-photon transition frequency'},
]

def coulomb_coeff(row):
 a,b=row['lo'][0],row['hi'][0]
 return float(Fraction(1,a*a)-Fraction(1,b*b))

def dirac_binding(n,j,alpha=ALPHA):
 # E_binding/h = -A*F(n,j); rest scale 2A/alpha^2. Rationalized
 # expressions avoid subtraction of nearly equal rest-energy terms.
 k=j+.5
 d=alpha**2/(k+math.sqrt(k*k-alpha**2))
 v=(alpha/(n-d))**2
 return 2/alpha**2*v/(math.sqrt(1+v)*(math.sqrt(1+v)+1))

def dirac_coeff(row,alpha=ALPHA):
 a,l,j=row['lo'];b,L,J=row['hi']
 return dirac_binding(a,j,alpha)-dirac_binding(b,J,alpha)

def s_shift_coeff(row):
 a,l,j=row['lo'];b,L,J=row['hi']
 return (1/b**3 if L==0 else 0)-(1/a**3 if l==0 else 0)

def main():
 obs=np.array([r['frequency_Hz'] for r in DATA]);sig=np.array([r['sigma_Hz'] for r in DATA])
 matrices={'inverse_square':np.array([[coulomb_coeff(r)] for r in DATA]),'dirac':np.array([[dirac_coeff(r)] for r in DATA]),'dirac_plus_S_shift':np.array([[dirac_coeff(r),s_shift_coeff(r)] for r in DATA])}
 fits=[]
 for name,M in matrices.items():
  p=M.shape[1]
  selections=[[i] for i in range(3)] if p==1 else [[0,1],[0,2],[1,2]]
  for idx in selections:
   # Minimal anchor set fixes the parameters. Other rows remain held out.
   if p==1:
    solution=np.array([obs[idx[0]]/M[idx[0],0]])
    covariance=np.array([[(sig[idx[0]]/M[idx[0],0])**2]])
   else:
    inv=np.linalg.inv(M[idx])
    solution=np.linalg.solve(M[idx],obs[idx])
    covariance=inv@np.diag(sig[idx]**2)@inv.T
   pred=M@solution
   for k,row in enumerate(DATA):
    pred_sigma=math.sqrt(max(float(M[k]@covariance@M[k]),0))
    combined=math.sqrt(pred_sigma**2+sig[k]**2)
    residual=float(pred[k]-obs[k])
    fits.append({'model':name,'anchors':','.join(DATA[i]['label'] for i in idx),'target':row['label'],'role':'calibration' if k in idx else 'held_out', 'A_Hz':float(solution[0]),'L_Hz':float(solution[1]) if p==2 else 0.,'prediction_Hz':float(pred[k]),'measurement_Hz':float(obs[k]),'residual_Hz':residual,'relative_residual_ppm':residual/obs[k]*1e6,'prediction_sigma_from_anchor_Hz':pred_sigma,'measurement_sigma_Hz':float(sig[k]),'approx_combined_sigma_Hz':combined,'approx_residual_sigma':residual/combined,'within_3sigma_summary_errors':bool(abs(residual)<=3*combined),'phase_cycle_time_s':1/float(pred[k]),'phase_pi_time_s':.5/float(pred[k]),'energy_gap_eV':H_EV*float(pred[k]),'wavelength_equivalent_m':C/float(pred[k])})
   # Physical transition frequencies are strictly positive.
   assert np.all(pred>0)
   assert np.max(abs(pred[idx]-obs[idx]))<5.
 # Shared SI convention with the neutrino audit; this is an adopted input,
 # not an independently verified cross-domain clock constant.
 for row in fits:
  assert abs(row['energy_gap_eV']*row['phase_cycle_time_s']/H_EV-1)<1e-12
  assert abs(row['wavelength_equivalent_m']/C/row['phase_cycle_time_s']-1)<1e-12
 # Dirac formula must tend to inverse-square as alpha decreases.
 for n,j in [(1,.5),(2,.5),(3,.5),(8,2.5)]:
  assert abs(dirac_binding(n,j,1e-5)*n*n-1)<1e-8
 assert coulomb_coeff(DATA[0])==.75
 assert abs(coulomb_coeff(DATA[1])/coulomb_coeff(DATA[0])-32/27)<1e-15
 assert abs(coulomb_coeff(DATA[2])/coulomb_coeff(DATA[0])-5/16)<1e-15
 # Alpha uncertainty propagation in the two-anchor corrected prediction.
 def corrected_holdout(alpha):
  M=np.array([[dirac_coeff(r,alpha),s_shift_coeff(r)] for r in DATA])
  return float(M[2]@np.linalg.solve(M[:2],obs[:2]))
 alpha_shift=abs(corrected_holdout(ALPHA+ALPHA_SIGMA)-corrected_holdout(ALPHA-ALPHA_SIGMA))/2
 # Repeat the two-anchor/one-holdout check using a different 1S-3S experiment.
 replica_f13=2922743278665790.
 replica_sigma=720.
 M=matrices['dirac_plus_S_shift']
 replica_solution=np.linalg.solve(M[:2],[obs[0],replica_f13])
 replica_prediction=float(M[2]@replica_solution)
 replica={'source':'https://doi.org/10.1126/science.abc7776','f13_Hz':replica_f13,'sigma_Hz':replica_sigma,'holdout_2S8D_prediction_Hz':replica_prediction,'holdout_residual_Hz':replica_prediction-obs[2],'holdout_relative_residual_ppm':(replica_prediction/obs[2]-1)*1e6,'purpose':'different published 1S-3S dataset sensitivity; not independent full-QED validation'}
 inputs={'version':'0.1','date':'2026-10-14','candidate':'rational hydrogen level codes u_n=1/n^2 and their transition gaps','relation_to_MCC':'new adopted spectral bridge audit; atomic n has not been derived from or identified with SOURCE arithmetic addresses','data':DATA,'constants':{'alpha':ALPHA,'alpha_sigma':ALPHA_SIGMA,'h_J_s':H_SI,'electronvolt_J':EV_J,'c_m_s':C},'conventions':['hyperfine centroids','total transition frequencies, not half-frequency excitation laser values','optical relative-phase period, not excitation waiting time or state lifetime'],'models':{'inverse_square':'E_n/h=-A/n^2','dirac':'E_nj/h=-A*F_Dirac(n,j;alpha), effective point-Coulomb template','dirac_plus_S_shift':'E_nlj/h=-A*F_Dirac(n,j;alpha)+L*delta_l0/n^3; two empirical calibrated coefficients; not full QED'},'limitations':['no full recoil/radiative/finite-size calculation','summary experimental errors, zero inter-experiment covariance','no theory truncation error assigned','same SI h as neutrino test is input, not a result']}
 main_holdout=[r for r in fits if r['model']=='dirac_plus_S_shift' and r['anchors']=='1S-2S,1S-3S' and r['role']=='held_out'][0]
 results={'fits':fits,'primary_corrected_holdout':main_holdout,'alternate_1S3S_dataset':replica,'alpha_sigma_effect_on_corrected_holdout_Hz':alpha_shift,'validation':'units, conventions, positivity, calibration reconstruction and Dirac limit passed','scientific_status':'tested truncated spectral candidates do not reproduce all holdouts within experimental-summary errors; this does not falsify full MCC or full QED','event_identity_status':'candidate correspondence only; no identification between SOURCE address events and atomic events established'}
 inputs['alternate_1S3S_dataset']=replica
 (OUT/'frozen_inputs.json').write_text(json.dumps(inputs,indent=2,ensure_ascii=False)+'\n')
 (OUT/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
 with (OUT/'cross_checks.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(fits[0]));w.writeheader();w.writerows(fits)
 selected=[r for r in fits if r['role']=='held_out' and ((r['anchors']=='1S-2S' and r['target']=='2S-8D5/2') or (r['model']=='dirac_plus_S_shift' and r['anchors']=='1S-2S,1S-3S'))]
 fig,ax=plt.subplots(figsize=(8,4.6),layout='constrained')
 labels=['Inverse-square\n1 anchor','Dirac\n1 anchor','Dirac + S shift\n2 anchors']
 vals=[abs(r['residual_Hz']) for r in selected]
 ax.bar(labels,vals,color=['#999999','#0072B2','#009E73'])
 ax.axhline(DATA[2]['sigma_Hz'],color='#D55E00',linestyle='--',label='Measurement uncertainty (not total theory error)')
 ax.set_yscale('log');ax.set(ylabel='Absolute held-out frequency residual (Hz)',title='Hydrogen 2S–8D5/2: held-out transition\nAdded physical structure reduces the residual; precision test still fails')
 for i,v in enumerate(vals):ax.text(i,v*1.12,f'{v/1e6:.3f} MHz',ha='center',fontsize=10)
 ax.set_ylim(1e3,max(vals)*3);ax.legend(fontsize=9);ax.grid(axis='y',alpha=.2)
 fig.savefig(OUT/'holdout_residuals.png',dpi=160)
 print(json.dumps({'one_anchor_inverse_square':[{k:r[k] for k in ['target','relative_residual_ppm','residual_Hz']} for r in fits if r['model']=='inverse_square' and r['anchors']=='1S-2S' and r['role']=='held_out'],'corrected_holdout':main_holdout,'alpha_uncertainty_effect_Hz':alpha_shift,'validation':results['validation']},indent=2))

if __name__=='__main__':main()
