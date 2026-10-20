"""Supplementary release checks; run after run_all.py. Original 54 not recounted."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from lensing_likelihood import LensingLikelihood,spectra
from thermal_history import EOS,TCMB,MPL,HBAR,BETA
P=Path(__file__).resolve().parent;checks={}
def check(n,v):
    checks[n]=bool(v)
    if not v:raise AssertionError(n)

like=LensingLikelihood();pp,tt=spectra('nonlinear');r,b=like.evaluate(pp,tt)
delta=b-like.d;L=np.linalg.cholesky(like.cov);white=np.linalg.solve(L,delta)
check('independent_whitened_chi_square',abs(float(white@white)-r['chi2'])<2e-12)
ix=np.arange(18)[::-1];rev=delta[ix]
check('bin_permutation_invariance',abs(rev@np.linalg.solve(like.cov[np.ix_(ix,ix)],rev)-r['chi2'])<2e-12)
scaled=float(delta@np.linalg.solve(4*like.cov,delta))
check('covariance_scaling_identity',abs(scaled-r['chi2']/4)<2e-12)
sign,logdet=np.linalg.slogdet(like.cov)
check('normalized_likelihood_determinant',sign==1 and abs(r['normalized_loglike']+.5*(r['chi2']+logdet+18*math.log(2*math.pi)))<1e-12)

thermal=json.loads((P/'results/thermal.json').read_text());events=json.loads((P/'results/thermal_events.json').read_text())
rhoi=(thermal['Hinitial_s_inverse']*MPL*HBAR)**2*3/(8*math.pi)
q=BETA*rhoi/256
expected_entropy=math.fsum(.01*q/(e['a']*e['T_before_MeV']) for e in events)
entropy_diff=abs(thermal['record_entropy_gain']/expected_entropy-1)
check('record_heat_first_law_entropy',entropy_diff<3e-5)
eos=EOS();last=np.genfromtxt(P/'results/thermal_history.csv',delimiter=',',names=True)[-1]
T=last['Tgamma_MeV'];a=last['a_relative'];rho,p,_=eos.exact(T)
entropy=(rho+p)/T
anchor=(4*math.pi**2/45*TCMB**3/entropy)**(1/3)/a
check('independent_exact_EOS_scale_anchor',abs(anchor/thermal['a_initial_derived']-1)<1e-8)
manifest=json.loads((P/'SHA256SUMS.json').read_text())
scientific_names=[n for n in manifest if n.startswith('results/') and n!='results/camb_runs.json']
check('rerun_frozen_scientific_files_exact',all(hashlib.sha256((P/n).read_bytes()).hexdigest()==manifest[n] for n in scientific_names))
gate=json.loads((P/'results/full_state_gate.json').read_text())
check('full_state_gate_still_blocked',gate['full_state_injected'] is False)
result=dict(date='2026-10-20',original_checks_passed=54,supplementary_checks_passed=sum(checks.values()),
    checks=checks,record_entropy_first_law_relative_difference=entropy_diff,
    exact_EOS_anchor_relative_difference=abs(anchor/thermal['a_initial_derived']-1),
    reexecuted_CAMB_and_thermal_pipeline=True,
    wall_clock_metadata_note='results/camb_runs.json retains original timing metadata; results/revalidation_camb_runs.json records the new run. Scientific outputs reproduce exactly.',
    scope='Conditional WRRA-background lensing comparison and separate MeV packet thermal completion. No full-state injection or joint posterior claimed.')
(P/'REVALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
