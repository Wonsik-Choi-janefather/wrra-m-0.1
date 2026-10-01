#!/usr/bin/env python3
"""WRRA residual-address inverse trials and neutron fold-transition ledger.

Trial A scans mass-compatible Ω=3 composite addresses under one calibrated
power readout. Trial B additionally imposes shared uud/udd prime factors.
Decay transport uses observed masses and a calibrated neutron lifetime.
The address encoding and readout are candidate rules, not particle IDs.
"""
from pathlib import Path
import json
import math
import hashlib
from fractions import Fraction
import numpy as np
from scipy.special import expit

ROOT=Path(__file__).resolve().parent
N=1_000_000
INPUT={
 'electron_rest_energy_MeV':.51099895069,
 'proton_rest_energy_MeV':938.27208943,
 'neutron_rest_energy_MeV':939.56542194,
 'neutron_proton_difference_MeV':1.29333251,
 'proton_electron_mass_ratio':1836.152673426,
 'proton_electron_ratio_standard_uncertainty':.000000032,
 'neutron_electron_mass_ratio':1838.68366200,
 'neutron_electron_ratio_standard_uncertainty':.00000074,
 'muon_electron_mass_ratio':206.7682827,
 'muon_electron_ratio_standard_uncertainty':.0000046,
 'neutron_mean_life_s':878.3,
 'neutron_mean_life_standard_uncertainty_s':.4,
 'proton_magnetic_moment_in_nuclear_magnetons':2.79284734463,
 'neutron_magnetic_moment_in_nuclear_magnetons':-1.91304276,
 'sources':{
 'masses_ratios_moments':'https://physics.nist.gov/cuu/Constants/Table/allascii.txt',
 'lifetime_and_decay':'https://pdg.lbl.gov/2026/tables/rpp2026-sum-baryons.pdf',
 'quark_properties':'https://pdg.lbl.gov/2026/tables/rpp2026-sum-quarks.pdf',
 'valence_model':'https://pdg.lbl.gov/2026/reviews/rpp2026-rev-quark-model.pdf'},
}

def factor_tables(limit):
 spf=np.zeros(limit+1,dtype=np.int32)
 for p in range(2,limit+1):
  if spf[p]==0:
   spf[p]=p
   if p*p<=limit:
    vals=spf[p*p::p];vals[vals==0]=p
 omega=np.zeros(limit+1,dtype=np.int8)
 for n in range(2,limit+1):omega[n]=omega[n//spf[n]]+1
 return spf,omega

def factorization(n,spf):
 factors=[]
 while n>1:
  p=int(spf[n]);factors.append(p);n//=p
 return factors

def main():
 spf,omega=factor_tables(N)
 addresses=np.arange(2,N+1)
 triples=addresses[(addresses%2==1)&(omega[2:]==3)]
 semis=addresses[(addresses%2==1)&(omega[2:]==2)]
 rp=INPUT['proton_electron_mass_ratio'];rn=INPUT['neutron_electron_mass_ratio']
 ne=9 # Smallest odd folded address, not an empirical electron identity.
 ps=triples[triples>ne]
 gamma=np.log(rp)/np.log(ps/ne)
 wanted=ps*np.exp(np.log(rn/rp)/gamma)
 pos=np.searchsorted(triples,wanted)
 lo=np.clip(pos-1,0,len(triples)-1);hi=np.clip(pos,0,len(triples)-1)
 lnlow=np.log(triples[lo]/ne)*gamma
 lnhigh=np.log(triples[hi]/ne)*gamma
 predlo=np.exp(lnlow);predhi=np.exp(lnhigh)
 pickhi=np.abs(predhi-rn)<np.abs(predlo-rn)
 ns=np.where(pickhi,triples[hi],triples[lo]);pred=np.where(pickhi,predhi,predlo)
 errors=np.abs(pred-rn)
 valid=(ns>ps)&(wanted<=N)
 candidate_indices=np.flatnonzero(valid)
 best=candidate_indices[np.argsort(errors[valid])[:20]]
 reference=ROOT/'zeta_reference.json'
 if not reference.exists():reference=ROOT.parent/'zeta_frame/results.json'
 zeta=json.loads(reference.read_text(encoding='utf8'))
 gz=np.array([r['gamma_used_double'] for r in zeta['zeta_zero_validation'][:4]])
 hz=zeta['calibration']['sigmoid_threshold_h'];az=zeta['calibration']['alpha']
 def admission(addr):
  d=np.array([np.cos(gz*(math.log(addr)+.1*k)).sum()/2 for k in range(8)])
  return float(-np.expm1(-np.logaddexp(0,d-hz).sum()))
 def muon_check(g):
  target=ne*math.exp(math.log(INPUT['muon_electron_mass_ratio'])/g)
  ii=int(np.searchsorted(semis,target));ix=[max(0,min(len(semis)-1,j)) for j in (ii-1,ii)]
  mi=min(ix,key=lambda i:abs((int(semis[i])/ne)**g-INPUT['muon_electron_mass_ratio']))
  addr=int(semis[mi]);r=(addr/ne)**g
  return {'address':addr,'factors':factorization(addr,spf),'predicted_muon_electron_ratio':r,
          'absolute_ratio_error':abs(r-INPUT['muon_electron_mass_ratio']),
          'within_quoted_muon_standard_uncertainty':bool(abs(r-INPUT['muon_electron_mass_ratio'])<=INPUT['muon_electron_ratio_standard_uncertainty'])}
 rows=[]
 for i in best:
  pp,nn,g=int(ps[i]),int(ns[i]),float(gamma[i])
  rows.append({'electron_address':ne,'proton_address':pp,'neutron_address':nn,
               'proton_factors':factorization(pp,spf),'neutron_factors':factorization(nn,spf),
               'calibrated_gamma_from_proton_electron':g,
               'predicted_neutron_electron_ratio':float(pred[i]),
               'absolute_neutron_ratio_error':float(errors[i]),
               'within_quoted_neutron_standard_uncertainty':bool(errors[i]<=INPUT['neutron_electron_ratio_standard_uncertainty']),
               'initial_electron_admission':admission(ne),
               'initial_proton_admission':admission(pp),'initial_neutron_admission':admission(nn),
               'nearest_muon_semiprime_check':muon_check(g),
               'particle_status':'mass-compatible address trial only; shared valence factors, charge, spin, current and lifetime not inferred by this trial'})

 # Trial B: shared up/down prime labels with uud and udd multiplicities.
 # For b>a, m_n/m_p=(b/a)^gamma. Calibrating m_p/m_e sets gamma;
 # ne=9 minimizes gamma and hence minimizes this ratio for every pair.
 primes=addresses[spf[2:]==addresses]
 linked=[]
 for a in primes[primes%2==1]:
  a=int(a)
  if a**3>N:break
  for b in primes[(primes>a)&(primes<=math.isqrt(N//a))]:
   b=int(b);pp=a*a*b;nn=a*b*b
   g=math.log(rp)/math.log(pp/ne)
   rr=rp*math.exp(g*math.log(b/a))
   linked.append({'up_prime':a,'down_prime':b,'electron_address':ne,
                  'proton_address':pp,'neutron_address':nn,'gamma':g,
                  'predicted_neutron_electron_ratio':rr,
                  'neutron_ratio_error':rr-rn,
                  'predicted_neutron_rest_energy_MeV':rr*INPUT['electron_rest_energy_MeV'],
                  'proton_charge_e':1,'neutron_charge_e':0})
 best_linked=min(linked,key=lambda x:abs(x['neutron_ratio_error']))
 observed_np=rn/rp
 best_linked['required_electron_address_for_exact_two_ratios']=float(np.exp(math.log(best_linked['proton_address'])-math.log(rp)/(math.log(observed_np)/math.log(best_linked['down_prime']/best_linked['up_prime']))))

 # Charge of valence factors is a supplied readout, independent of prime size.
 qu,qd=Fraction(2,3),Fraction(-1,3)
 assert 2*qu+qd==1 and qu+2*qd==0
 me=INPUT['electron_rest_energy_MeV'];mp=INPUT['proton_rest_energy_MeV'];mn=INPUT['neutron_rest_energy_MeV']
 qn=INPUT['neutron_proton_difference_MeV']-me
 qp=-INPUT['neutron_proton_difference_MeV']-me
 tau=INPUT['neutron_mean_life_s']
 # Trial C: shared lowest odd primes encode the nucleon isospin doublet.
 # Calibrate a common additive energy and signed-current readout; these
 # effective energies are NOT MS running quark masses.
 mean_nucleon=(mp+mn)/2
 energy_per_valence=mean_nucleon/3
 isospin_energy=INPUT['neutron_proton_difference_MeV']/2
 mu_p=INPUT['proton_magnetic_moment_in_nuclear_magnetons']
 mu_n=INPUT['neutron_magnetic_moment_in_nuclear_magnetons']
 mu_u=(4*mu_p+mu_n)/5
 mu_d=(mu_p+4*mu_n)/5
 prototype={
  'encoding':'u prime=3, d prime=5 in the baryon valence readout; chosen minimal odd distinct prime encoding. Electron address 9 belongs to a separate lepton channel, not two up quarks.',
  'charge_operator':'Q(n,channel): quark valence sector uses 2/3 ku - 1/3 kd; electron channel is assigned -1, antineutrino channel 0. Integer factorization alone does not supply channel labels.',
  'energy_readout':'E(ku,kd)=A*(ku+kd)+B*(kd-ku) for the spin-1/2 nucleon ground-state doublet',
  'energy_parameters_MeV':{'A':energy_per_valence,'B':isospin_energy},
  'energy_calibration':'A to mean p/n energy, B to neutron-proton mass difference',
  'current_readout':'mu_p=(4 mu_u-mu_d)/3, mu_n=(4 mu_d-mu_u)/3; SU(6) nucleon moment readout used as a calibrated map',
  'current_parameters_in_nuclear_magnetons':{'mu_u':mu_u,'mu_d':mu_d},
  'current_calibration':'two observed p/n magnetic moments',
  'scope':'nucleon isospin doublet only; binding/spin excitation and lepton mass readout beyond the fitted e baseline remain extensions',
  'addresses_chosen_from_lower_prime_support_not_identified_by_constants_alone':True,
  'proton':{'address':45,'factors':[3,3,5],'ku':2,'kd':1,
            'initial_admission':admission(45),'energy_MeV':3*energy_per_valence-isospin_energy,
            'charge_e':1,'magnetic_moment':(4*mu_u-mu_d)/3},
  'neutron':{'address':75,'factors':[3,5,5],'ku':1,'kd':2,
             'initial_admission':admission(75),'energy_MeV':3*energy_per_valence+isospin_energy,
             'charge_e':0,'magnetic_moment':(4*mu_d-mu_u)/3},
  'transition':'udd -> uud + e- + antinu_e; address 75 -> 45 with lepton channels; integer address product is a label, not a conserved energy',
  'decay_energy_from_shared_readout_MeV':(3*energy_per_valence+isospin_energy)-(3*energy_per_valence-isospin_energy)-me,
 }
 decay=[]
 for t in (0.,1.,100.,tau,1000.,5*tau):
  s=math.exp(-t/tau);b=-math.expm1(-t/tau)
  # One completed decay event creates p, e and antineutrino. Retain the
  # combined daughter kinetic/antineutrino energy as one ledger quantity.
  energy=s*mn+b*(mp+me+qn)
  decay.append({'time_s':t,'surviving_neutron_probability':s,
                'completed_decay_probability':b,
                'expected_neutron_count':s,'expected_proton_count':b,
                'expected_electron_count':b,'expected_antineutrino_count':b,
                'combined_daughter_kinetic_and_antineutrino_energy_MeV':b*qn,
                'energy_ledger_MeV':energy,'net_charge_e':b-b,
                'baryon_count':s+b,'lepton_number':b-b,
                'SOURCE_return_fraction':0.,
                'normal_return_note':'total energy remains in Actual in this beta-only trial; radiation energy is part of Actual ledger'})
 checks={
  'trial_A_addresses_folded':all(omega[x['electron_address']]>=2 and omega[x['proton_address']]==3 and omega[x['neutron_address']]==3 for x in rows),
  'trial_A_all_selected_have_nonzero_initial_admission':all(x['initial_proton_admission']>0 and x['initial_neutron_admission']>0 for x in rows),
  'trial_A_calibration_reproduces_proton_ratio':all(abs((x['proton_address']/ne)**x['calibrated_gamma_from_proton_electron']-rp)<1e-9 for x in rows),
  'trial_B_shared_valence_products':best_linked['proton_address']==best_linked['up_prime']**2*best_linked['down_prime'] and best_linked['neutron_address']==best_linked['up_prime']*best_linked['down_prime']**2,
  'trial_B_optimal_ne9_explained':'For b>a and positive gamma, increasing ne increases the predicted n/p ratio; ne=9 is the minimum admissible odd composite.',
  'charges_match_supplied_valence_readout':bool(2*qu+qd==1 and qu+2*qd==0),
  'trial_C_shared_energy_matches_nucleons':abs(prototype['proton']['energy_MeV']-mp)<1e-9 and abs(prototype['neutron']['energy_MeV']-mn)<1e-9,
  'trial_C_signed_current_matches_moments':abs(prototype['proton']['magnetic_moment']-mu_p)<1e-12 and abs(prototype['neutron']['magnetic_moment']-mu_n)<1e-12,
  'trial_C_addresses_in_folded_phenotype_support':omega[45]==3 and omega[75]==3 and admission(45)>0 and admission(75)>0,
  'free_neutron_beta_channel_has_positive_Q':qn>0,
  'proton_to_neutron_positron_channel_has_negative_Q':qp<0,
  'decay_total_energy_preserved':all(abs(x['energy_ledger_MeV']-mn)<1e-9 for x in decay),
  'decay_charge_baryon_lepton_ledgers_preserved':all(x['net_charge_e']==0 and abs(x['baryon_count']-1)<1e-12 and x['lepton_number']==0 for x in decay),
 }
 result={'title':'WRRA M particle residual-address inverse trials and fold-decay ledger v0.1',
  'date':'2026-10-01','author':'Wonsik Choi','verified_inputs':INPUT,
  'hypothesis':'Particle decay is a change of preserved prime-like composite fold relations and phenotype; residue energy need not return to SOURCE.',
  'mass_readout_trial':'m(n)/m_e=(n/9)^gamma; gamma calibrated with m_p/m_e for each candidate p address. A dimensionless mass exponent gamma is distinct from zeta weight alpha and zero heights gamma_j.',
  'fold_proxy':'Omega(n)-1, with admitted odd composites in phenotype support',
  'trial_A':{'name':'independent Omega3 baryon addresses','proton_addresses_tested':int(valid.sum()),
             'addresses_with_neutron_ratio_error_within_quoted_standard_uncertainty':int(np.count_nonzero(valid&(errors<=INPUT['neutron_electron_ratio_standard_uncertainty']))),
             'comparison_status':'numerical screening using central fitted proton ratio; not a full correlated statistical test or physical identification',
             'top_20_candidates':rows},
  'trial_B':{'name':'linked uud udd prime factors','pairs_tested':len(linked),
             'best_pair':best_linked,
             'status':'the simple common power readout does not match linked proton/neutron structure at N<=1e6; energy readout needs an interaction or binding term, a different encoding, or an expanded address range'},
  'trial_C':prototype,
  'particle_differences':{'proton':{'valence':'uud','charge_e':1,'spin_hbar':.5,'beta_to_n_eplus_nu_Q_MeV':qp,'beta_only_channel':'closed by energy'},
                          'neutron':{'valence':'udd','charge_e':0,'spin_hbar':.5,'beta_to_p_eminus_antinu_Q_MeV':qn,'mean_life_s':tau}},
  'decay_trial':{'transition':'n -> p + electron + electron antineutrino',
                 'physical_input_used_for_rate':'observed 878.3 s mean life; rate not derived from prime factors',
                 'channel_context':'free neutron, beta-only transition; neutrino rest masses and radiative branching resolution neglected',
                 'frame_probability_rule':'epsilon(dt)=1-exp(-dt/tau), S(k)=(1-epsilon)^k',
                 'dt_interpretation':'chosen physical observation step, not the uncalibrated fundamental universe frame',
                 'decay_v_return':'a phenotype transition among Actual states is distinct from fold leakage into SOURCE',
                 'rows':decay},
  'zeta_reference':{'sha256':hashlib.sha256(reference.read_bytes()).hexdigest(),
                    'source_commit':'f145b82856f53a45611c4cc18f22ea9f1589da73',
                    'source_repository_path':'upstream/zeta_frame_v0_1/code/results.json',
                    'used_parameters':{'zero_count':4,'frames':8,'xi':.1,'phase_offset':0.,'threshold_h':hz,'alpha':az}},
  'completed_response_components':['calibrated nucleon ground-state energy readout','calibrated signed nucleon magnetic-current readout','valence charges and free beta energy threshold','mean-life-calibrated conserved expectation ledger'],
  'companion_audit':'channel_readout.py computes separate color, weak, EM-charge and spin-addition responses; channel_results.json records the extended state schema and uncomputed force strengths',
  'next_readout_constraints':['nucleon mass splitting into isospin and electromagnetic contributions at stated scale/scheme','binding and interaction energy across spin, orbital and nuclear states','microscopic charge-preserving fold transition matrix element and phase space','common lepton mass response and alternative particle/environment holdouts'],
  'verification':checks,
  'falsification_conditions':['no folded address candidate under a stated finite search and readout','failure of shared valence-factor mass map, charge or current response','negative or nonconserved transition energy/probability','unreported lifetime or particle-specific fitting used as if derived'],
 }
 assert all(v is True for k,v in checks.items() if isinstance(v,bool)),checks
 ROOT.mkdir(exist_ok=True)
 (ROOT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({'trial_A_tested':result['trial_A']['proton_addresses_tested'],
                   'mass_compatible_count':result['trial_A']['addresses_with_neutron_ratio_error_within_quoted_standard_uncertainty'],
                   'trial_A_best':rows[0],'trial_B_best':best_linked,
                   'Q_neutron':qn,'Q_proton_beta_plus':qp,'verification':checks},indent=2))

if __name__=='__main__':main()
