#!/usr/bin/env python3
"""WRRA-M fold-current matrix and allowed beta phase-space response.

Arithmetic labels and a local Euler-factor response are declared choices.
Empirical masses, GF, Vud, axial ratio and one neutron lifetime anchor are
recorded inputs. SU(4) symmetric three-quark spin-flavor states and a color
singlet give explicit finite matrix elements. No QCD Hamiltonian is solved.
"""
from pathlib import Path
import hashlib
import itertools
import json
import math
import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar
from scipy.special import roots_legendre

ROOT=Path(__file__).resolve().parent
REFERENCE=ROOT/'nucleon_reference.json'
ADDRESS_CUTOFF=1_000_000
INPUT={
 'GF_GeV_minus2':1.1663787e-5,
 'Vud':.97367,'Vud_uncertainty':.00032,
 'lambda_axial_vector':-1.2753,'lambda_uncertainty':.0013,
 'hbar_MeV_s':6.582119569e-22,
 'alpha_em':7.2973525643e-3,
 'neutron_mean_life_s':878.3,'mean_life_uncertainty_s':.4,
 'sources':{
  'constants':'https://physics.nist.gov/cuu/Constants/Table/allascii.txt',
  'Vud':'https://pdg.lbl.gov/2026/reviews/rpp2026-rev-ckm-matrix.pdf',
  'lambda_and_lifetime':'https://pdg.lbl.gov/2026/tables/rpp2026-sum-baryons.pdf',
  'beta_formula':'https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=902353',
  'quark_model':'https://pdg.lbl.gov/2026/reviews/rpp2026-rev-quark-model.pdf'},
}

def at_slot(op,slot):
 ops=[np.eye(4) for _ in range(3)];ops[slot]=op
 return np.kron(np.kron(ops[0],ops[1]),ops[2])

def symmetric_sector(ku,twice_Jz):
 # One-slot basis u_up,u_down,d_up,d_down. Spin-flavor symmetrized S-wave.
 cols=[]
 for seq in itertools.combinations_with_replacement(range(4),3):
  if sum(x<2 for x in seq)!=ku:continue
  if sum(1 if x%2==0 else -1 for x in seq)!=twice_Jz:continue
  permutations=sorted(set(itertools.permutations(seq)))
  v=np.zeros(64)
  for a,b,c in permutations:v[16*a+4*b+c]=1/math.sqrt(len(permutations))
  cols.append(v)
 return np.column_stack(cols)

def spin_flavor():
 sx=np.array([[0,1],[1,0]],complex);sy=np.array([[0,-1j],[1j,0]],complex);sz=np.diag([1,-1])
 pauli=[sx,sy,sz]
 Js=[sum(at_slot(np.kron(np.eye(2),s/2),i) for i in range(3)) for s in pauli]
 Is=[sum(at_slot(np.kron(s/2,np.eye(2)),i) for i in range(3)) for s in pauli]
 J2=sum(j@j for j in Js);I2=sum(i@i for i in Is)
 tp=np.array([[0,1],[0,0]])
 one_vector=np.kron(tp,np.eye(2));one_axial=np.kron(tp,sz)
 V=sum(at_slot(one_vector,i) for i in range(3))
 Az=sum(at_slot(one_axial,i) for i in range(3))
 Q=sum(at_slot(np.diag([2/3,2/3,-1/3,-1/3]),i) for i in range(3))
 states={};delta={}
 for label,ku in [('proton',2),('neutron',1)]:
  basis=symmetric_sector(ku,1)
  matrix=(basis.conj().T@J2@basis).real
  eig,vec=np.linalg.eigh(matrix)
  states[label]=(basis@vec[:,np.argmin(eig)]).real
  delta[label]=(basis@vec[:,np.argmax(eig)]).real
  # Choose deterministic phase before fixing relative isospin convention.
  for state in (states[label],delta[label]):
   pivot=int(np.argmax(np.abs(state)))
   if state[pivot]<0:state*=-1
 p=states['proton'];n=states['neutron']
 if float(np.vdot(p,V@n).real)<0:n*=-1
 vector=float(np.vdot(p,V@n).real);axial=float(np.vdot(p,Az@n).real)
 def exchange(v,permutation):return v.reshape(4,4,4).transpose(permutation).reshape(64)
 perms=list(itertools.permutations(range(3)))
 symmetry_error=max(np.linalg.norm(exchange(s,perm)-s) for s in (p,n) for perm in perms)
 color=np.zeros((3,3,3))
 for perm in perms:
  inv=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
  color[perm]=(-1)**inv/math.sqrt(6)
 anti_error=0.
 for perm in perms:
  inv=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
  anti_error=max(anti_error,np.linalg.norm(color.transpose(perm)-(-1)**inv*color))
 # Current is color identity: full state is antisymmetric color times
 # symmetric spin-flavor times a supplied symmetric spatial ground state.
 gm=[np.array(x,dtype=complex)/2 for x in [
  [[0,1,0],[1,0,0],[0,0,0]],[[0,-1j,0],[1j,0,0],[0,0,0]],
  [[1,0,0],[0,-1,0],[0,0,0]],[[0,0,1],[0,0,0],[1,0,0]],
  [[0,0,-1j],[0,0,0],[1j,0,0]],[[0,0,0],[0,0,1],[0,1,0]],
  [[0,0,0],[0,0,-1j],[0,1j,0]],np.diag([1,1,-2])/math.sqrt(3)]]
 color_norms=[];i3=np.eye(3)
 for g in gm:
  total=np.kron(np.kron(g,i3),i3)+np.kron(np.kron(i3,g),i3)+np.kron(np.kron(i3,i3),g)
  color_norms.append(float(np.linalg.norm(total@color.reshape(27))))
 def state_rows(s):
  names=['3u_up','3u_down','5d_up','5d_down'];rows=[]
  for index in np.flatnonzero(np.abs(s)>1e-12):
   a,b,c=np.unravel_index(index,(4,4,4))
   rows.append({'basis':[names[a],names[b],names[c]],'amplitude':float(s[index])})
 checks={
  'nucleon_states_normalized':all(abs(np.vdot(s,s).real-1)<1e-12 for s in (p,n)),
  'spin_flavor_exchange_symmetric':symmetry_error<1e-12,
  'color_exchange_antisymmetric':anti_error<1e-12,
  'color_singlet_total_generators_zero':max(color_norms)<1e-12,
  'nucleon_total_spin_half':all(np.linalg.norm(J2@s-.75*s)<1e-12 for s in (p,n)),
  'nucleon_isospin_half':all(np.linalg.norm(I2@s-.75*s)<1e-12 for s in (p,n)),
  'spin_projection_half':all(np.linalg.norm(Js[2]@s-.5*s)<1e-12 for s in (p,n)),
  'proton_charge_one_neutron_zero':np.linalg.norm(Q@p-p)<1e-12 and np.linalg.norm(Q@n)<1e-12,
  'current_raises_charge_one':np.linalg.norm(Q@V-V@Q-V)<1e-12,
  'vector_current_preserves_total_spin':np.linalg.norm(J2@V-V@J2)<1e-12,
  'vector_matrix_element_one':abs(vector-1)<1e-12,
  'bare_axial_matrix_element_five_thirds':abs(axial-5/3)<1e-12,
  'vector_to_spin_three_half_zero':abs(np.vdot(delta['proton'],V@n))<1e-12,
 }
 result={'one_slot_basis':['3u_up','3u_down','5d_up','5d_down'],
  'state_scope':'supplied symmetric S-wave three-valence-quark spin-flavor ansatz, antisymmetric color singlet; not a QCD bound-state solution',
  'state_dimensions':{'spin_flavor':64,'color':27,'combined':1728},
  'proton_state':state_rows(p),'neutron_state':state_rows(n),
  'matrix_elements':{'vector_n_to_p':vector,'bare_axial_z_n_to_p':axial,
                    'vector_to_J_three_half':float(np.vdot(delta['proton'],V@n).real),
                    'axial_z_to_J_three_half':float(np.vdot(delta['proton'],Az@n).real)},
  'color_singlet_generator_norms':color_norms,'checks':checks}
 result['checks']={k:bool(x) for k,x in checks.items()}
 return result

def spectrum_W(W,W0,coulomb=True,alpha=INPUT['alpha_em']):
 W=np.asarray(W);momentum=np.sqrt(np.maximum(W*W-1,0))
 if coulomb:
  # Sommerfeld/Fermi point-charge approximation. Evaluate p*F stably.
  x=np.divide(2*math.pi*alpha*W,momentum,out=np.full_like(W,np.inf),where=momentum>0)
  pF=2*math.pi*alpha*W/(-np.expm1(-x))
 else:pF=momentum
 return pF*W*np.maximum(W0-W,0)**2

def phase(Q,me,coulomb=True,method='quad'):
 if Q<=0:return 0.
 W0=1+Q/me
 if method=='quad':
  f,error=quad(lambda W:float(spectrum_W(W,W0,coulomb)),1,W0,epsabs=1e-20,epsrel=2e-12,limit=150)
  return float(f)
 # W=1+(W0-1)t^2 removes the no-Coulomb endpoint square-root.
 x,w=roots_legendre(160);t=(x+1)/2;W=1+(W0-1)*t*t
 return float(np.sum(w/2*spectrum_W(W,W0,coulomb)*2*(W0-1)*t))

def power_cutoff(p):
 k=0;power=p
 while power<=ADDRESS_CUTOFF:k+=1;power*=p
 return k

def euler_activity(p,alpha):
 # Finite prime-power family with the same inherited arithmetic cutoff.
 k=power_cutoff(p);x=math.exp(-alpha*math.log(p))
 return x*(-math.expm1(-alpha*math.log(p)*k))/(-math.expm1(-alpha*math.log(p)))

def transport(rate,total_energy):
 # basis n, complete p+e+antinu bundle, SOURCE. The final bundle includes
 # all released kinetic/antineutrino energy, so this is one energy shell.
 L=np.zeros((3,3));L[1,0]=math.sqrt(rate)
 eye=np.eye(3);LdL=L.T@L
 generator=np.kron(L,L)-.5*(np.kron(eye,LdL)+np.kron(LdL.T,eye))
 rho0=np.diag([1.,0.,0.]);H=np.diag([total_energy,total_energy,0.])
 charges=np.zeros((3,3));baryon=np.diag([1.,1.,0.])
 rows=[]
 for t in (0.,1.,100.,878.3,1000.,4391.5):
  rho=(expm(generator*t)@rho0.reshape(9,order='F')).reshape(3,3,order='F')
  rows.append({'time_s':t,'neutron_survival':float(rho[0,0]),'daughter_bundle':float(rho[1,1]),
               'SOURCE':float(rho[2,2]),'trace':float(np.trace(rho)),
               'minimum_eigenvalue':float(np.linalg.eigvalsh(rho).min()),
               'energy_MeV':float(np.trace(rho@H)),'charge_e':float(np.trace(rho@charges)),
               'baryon_number':float(np.trace(rho@baryon))})
 dt=1.;s=math.exp(-rate*dt)
 K0=np.diag([math.sqrt(s),1.,1.]);K1=np.zeros((3,3));K1[1,0]=math.sqrt(-math.expm1(-rate*dt))
 once=K0@rho0@K0.T+K1@rho0@K1.T
 by_generator=(expm(generator*dt)@rho0.reshape(9,order='F')).reshape(3,3,order='F')
 return {'rows':rows,'K0':K0.tolist(),'K1':K1.tolist(),
         'description':'Markov coarse-grained beta channel after continuum integration; not fundamental time discretization or derivation of a QCD Hamiltonian',
         'checks':{'Kraus_trace_preserving':np.linalg.norm(K0.T@K0+K1.T@K1-eye)<1e-12,
                   'Kraus_equals_generator':np.linalg.norm(once-by_generator)<1e-12,
                   'trace_positive':all(abs(r['trace']-1)<1e-12 and r['minimum_eigenvalue']>=-1e-12 for r in rows),
                   'survival_matches_rate_exponential':all(abs(r['neutron_survival']-math.exp(-rate*r['time_s']))<1e-12 for r in rows),
                   'Actual_energy_preserved':all(abs(r['energy_MeV']-total_energy)<1e-9 for r in rows),
                   'SOURCE_return_zero':all(r['SOURCE']==0 for r in rows),
                   'baryon_charge_preserved':all(abs(r['baryon_number']-1)<1e-12 and r['charge_e']==0 for r in rows)}}

def main():
 ref=json.loads(REFERENCE.read_text(encoding='utf8'))
 known=ref['verified_inputs'];me=known['electron_rest_energy_MeV']
 mp=known['proton_rest_energy_MeV'];mn=known['neutron_rest_energy_MeV']
 Q0=mn-mp-me;alpha=ref['zeta_reference']['used_parameters']['alpha']
 sf=spin_flavor();v=sf['matrix_elements']['vector_n_to_p'];a=sf['matrix_elements']['bare_axial_z_n_to_p']
 etaA=abs(INPUT['lambda_axial_vector'])*abs(v)/abs(a)
 axial=etaA*a
 GF=INPUT['GF_GeV_minus2']*1e-6 # GeV^-2 -> MeV^-2
 pref=GF*GF*INPUT['Vud']**2*me**5/(2*math.pi**3*INPUT['hbar_MeV_s'])
 fc=phase(Q0,me,True);f0=phase(Q0,me,False)
 base_rate=pref*(v*v+3*axial*axial)*fc
 bare_rate=pref*(v*v+3*a*a)*fc
 activity3=euler_activity(3,alpha);activity5=euler_activity(5,alpha)
 fold_product=activity3*activity5
 kappa=math.sqrt(1/(INPUT['neutron_mean_life_s']*base_rate*fold_product))
 def rate(Q,pa=3,pb=5,axial_value=axial,overlap=1.):
  return kappa*kappa*euler_activity(pa,alpha)*euler_activity(pb,alpha)*pref*(v*v+3*axial_value**2)*overlap**2*phase(Q,me,True)
 gamma0=rate(Q0)
 def rate_row(Q):
  gamma=rate(Q)
  return {'Q_MeV':float(Q),'phase_factor':phase(Q,me,True),'rate_per_s':gamma,
          'mean_life_s':1/gamma if gamma>0 else None,'rate_relative_to_anchor':gamma/gamma0,
          'context':'controlled same-kernel energy case, not identification of a real bound nucleus'}
 energy_cases=[rate_row(q) for q in (-1.80433146069,0.,.05,.1,.25,.5,Q0,1.,1.5,2.,3.)]
 prime_cases=[]
 for pa,pb in ((3,5),(3,7),(5,7),(3,11),(5,11)):
  gamma=rate(Q0,pa,pb)
  prime_cases.append({'up_prime':pa,'down_prime':pb,'proton_label':pa*pa*pb,'neutron_label':pa*pb*pb,
                      'Euler_activity_product':euler_activity(pa,alpha)*euler_activity(pb,alpha),
                      'rate_relative_to_anchor':gamma/gamma0,'mean_life_s':1/gamma,
                      'status':'controlled arithmetic-label case holding energy and supplied physical currents fixed; not a particle identification'})
 eps=1e-4
 Q_deriv=(math.log(rate(Q0*(1+eps)))-math.log(rate(Q0*(1-eps))))/(math.log(1+eps)-math.log(1-eps))
 phase_checks=[]
 for Q in (.01,.05,.25,Q0,1.,2.,3.):
  for coulomb in (False,True):
   x=phase(Q,me,coulomb,'quad');y=phase(Q,me,coulomb,'gauss')
   phase_checks.append({'Q_MeV':Q,'Coulomb':coulomb,'adaptive':x,'Gaussian':y,'relative_difference':abs(x-y)/x})
 lam=INPUT['lambda_axial_vector'];den=1+3*lam*lam
 correlations={'lambda_input':lam,'a_electron_antineutrino':(1-lam*lam)/den,
               'A_electron_spin_asymmetry':-2*lam*(lam+1)/den,
               'B_antineutrino_spin_asymmetry':2*lam*(lam-1)/den,
               'scope':'leading allowed V-A correlation outputs using observed signed lambda; not independent of the lambda input or its extraction data'}
 correlations['central_value_comparison']=[
  {'name':'a','calculated':correlations['a_electron_antineutrino'],'PDG_2026_central':-.1044,'PDG_quoted_uncertainty':.0007},
  {'name':'A','calculated':correlations['A_electron_spin_asymmetry'],'PDG_2026_central':-.11958,'PDG_quoted_uncertainty':.00021},
  {'name':'B','calculated':correlations['B_antineutrino_spin_asymmetry'],'PDG_2026_central':.9807,'PDG_quoted_uncertainty':.003},
 ]
 for row in correlations['central_value_comparison']:row['central_difference']=row['calculated']-row['PDG_2026_central']
 correlations['comparison_status']='No simultaneous refit to a,A,B performed; central differences are recorded, not a correlated goodness-of-fit statistic. Normalization kappa cannot change these leading ratios.'
 W0=1+Q0/me
 meanT=quad(lambda W:float(spectrum_W(W,W0,True))*(W-1)*me,1,W0,epsabs=1e-18,epsrel=2e-12)[0]/fc
 def cdfT(T):
  if T<=0:return 0.
  if T>=Q0:return 1.
  return quad(lambda W:float(spectrum_W(W,W0,True)),1,1+T/me,epsabs=1e-18,epsrel=2e-12)[0]/fc
 medianT=brentq(lambda T:cdfT(T)-.5,0,Q0,xtol=1e-14)
 peak=minimize_scalar(lambda T:-float(spectrum_W(1+T/me,W0,True)),bounds=(0,Q0),method='bounded',options={'xatol':1e-13})
 spectrum={'scope':'leading unpolarized electron kinetic spectrum with point-charge Coulomb factor, massless antineutrino and neglected proton recoil; normalized shape independent of lifetime anchor',
  'endpoint_T_MeV':Q0,'mean_T_MeV':meanT,'median_T_MeV':medianT,'mode_T_MeV':float(peak.x),
  'mean_antineutrino_energy_MeV':Q0-meanT,
  'samples':[{'T_MeV':T,'normalized_density_per_MeV':float(spectrum_W(1+T/me,W0,True))/fc/me,'CDF':cdfT(T)} for T in (0.,.1,.2,.3,.4,.5,.6,.7,Q0)]}
 current_cases=[]
 for axial_value in (0.,axial,a):
  gamma=rate(Q0,axial_value=axial_value)
  current_cases.append({'effective_axial':axial_value,'mean_life_s':1/gamma,'rate_relative_to_anchor':gamma/gamma0})
 overlap_cases=[]
 for overlap in (1.,.75,.5,0.):
  gamma=rate(Q0,overlap=overlap)
  overlap_cases.append({'additional_amplitude_overlap':overlap,'rate_per_s':gamma,'mean_life_s':1/gamma if gamma>0 else None})
 tr=transport(gamma0,mn)
 tr['checks']={k:bool(x) for k,x in tr['checks'].items()}
 checks={**sf['checks'],**tr['checks'],
  'phase_integrals_independently_agree':max(r['relative_difference'] for r in phase_checks)<2e-9,
  'closed_channel_rate_zero':rate(-1.80433146069)==0 and rate(0.)==0,
  'positive_Q_cases_have_positive_rates':all(r['rate_per_s']>0 for r in energy_cases if r['Q_MeV']>0),
  'calibrated_neutron_lifetime_returned':abs(1/gamma0-INPUT['neutron_mean_life_s'])<1e-9,
  'dressed_axial_matches_observed_magnitude':abs(axial-abs(lam))<1e-12,
  'fold_labels_have_equal_three_factor_multiplicity':all(r['proton_label']==r['up_prime']**2*r['down_prime'] and r['neutron_label']==r['up_prime']*r['down_prime']**2 for r in prime_cases),
  'zero_overlap_blocks_channel':rate(Q0,overlap=0.)==0,
  'finite_Euler_family_sum':all(abs(euler_activity(p,alpha)-sum(p**(-alpha*k) for k in range(1,power_cutoff(p)+1)))<1e-12 for p in (3,5,7,11)),
  'spectrum_mean_energies_sum_to_Q':abs(spectrum['mean_T_MeV']+spectrum['mean_antineutrino_energy_MeV']-Q0)<1e-12,
  'spectrum_median_and_endpoint':abs(cdfT(medianT)-.5)<1e-10 and cdfT(Q0)==1.,
 }
 checks={k:bool(x) for k,x in checks.items()}
 assert all(checks.values()),checks
 result={'title':'WRRA-M fold-current and neutron beta-rate bridge v0.2','date':'2026-10-02','author':'Wonsik Choi',
  'hypothesis':'a retained arithmetic fold admits internal prime-label substitution; charge/current matrix elements, available final-state phase space and a calibrated response strength set phenotype decay while Actual energy remains retained',
  'empirical_inputs':INPUT,'mass_inputs':{k:known[k] for k in ('electron_rest_energy_MeV','proton_rest_energy_MeV','neutron_rest_energy_MeV')},
  'reference_provenance':{'sha256':hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),'commit':'fa761e6f67abcc74ac9589e5a501f005c66a6993','repository_path':'upstream/particle_residue_decay_v0_1/code/results.json'},
  'spin_flavor':sf,
  'fold_response':{'alpha_from_cosmic_zeta_calibration':alpha,'arithmetic_cutoff_N':ADDRESS_CUTOFF,
    'Euler_activity_definition':'r_p(N)=sum_(k=1)^K p^(-alpha*k)=x*(1-x^K)/(1-x), x=p^(-alpha), K=max integer with p^K<=N',
    'chosen_kernel':'kappa*sqrt(r_up*r_down)*sum_i |up_prime>_i<down_prime| for vector; axial has sigma_z at that slot',
    'status':'symmetric local Euler-factor amplitude is a declared WRRA kernel ansatz; calibration cannot uniquely select this ansatz',
    'activity_3':activity3,'activity_5':activity5,'activity_product_3_5':fold_product,
    'calibrated_kappa':kappa,'anchor_rate_multiplier_kappa2_r3_r5':kappa*kappa*fold_product,
    'calibration':'one observed neutron mean life fixes kappa at the supplied masses, GF, Vud and axial ratio; kappa also absorbs omitted radiative, recoil and constitutive corrections'},
  'rate_bridge':{'formula':'Gamma=kappa^2*r_up*r_down*GF^2*|Vud|^2*me^5/(2*pi^3*hbar)*(|v|^2+3|etaA*a|^2)*f_C(Q)*overlap^2',
    'units':'GF converted to MeV^-2; c=1 for energy algebra; hbar in MeV*s restores inverse seconds',
    'axial_dressing_etaA':etaA,'bare_axial':a,'effective_axial':axial,
    'axial_sign_convention':'effective_axial is the positive magnitude; the signed observed lambda is used separately in V-A angular correlations',
    'Q_anchor_MeV':Q0,
    'phase_factor_no_Coulomb':f0,'phase_factor_Coulomb_approximation':fc,
    'Coulomb_model':'point-charge Sommerfeld/Fermi factor 2*pi*alpha*W/p divided by 1-exp(-2*pi*alpha*W/p); not full precision beta radiative/recoil theory',
    'physical_kernel_before_fold_calibration_rate_per_s':base_rate,'physical_kernel_before_fold_calibration_mean_life_s':1/base_rate,
    'bare_SU6_axial_same_physical_kernel_mean_life_s':1/bare_rate,
    'calibrated_rate_per_s':gamma0,'calibrated_mean_life_s':1/gamma0,'local_log_rate_Q_elasticity':Q_deriv},
  'energy_cases':energy_cases,'prime_label_cases':prime_cases,'axial_current_cases':current_cases,'extra_overlap_cases':overlap_cases,
  'leading_angular_correlations':correlations,'electron_spectrum':spectrum,'phase_integral_cross_checks':phase_checks,'transport':tr,
  'calibration_held_fixed_in_responses':'kappa, GF, Vud, axial dressing and cosmic alpha held fixed; only explicitly named Q, prime labels, axial override or additional overlap changes',
  'next_constraints':['separate radiative/recoil correction from fold-response normalization','derive the axial dressing from a specified internal state or binding Hamiltonian','test a fixed constitutive mass kernel and transition against another measured particle without refitting per case','compare alternative arithmetic kernels at fixed calibration and common physical cases'],
  'verification':{'checks':checks,'passed':sum(checks.values()),'total':len(checks),'all_passed':all(checks.values())}}
 (ROOT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({'vector':v,'bare_axial':a,'effective_axial':axial,'phase_C':fc,'uncalibrated_tau':1/base_rate,'kappa':kappa,'calibrated_tau':1/gamma0,'Q_elasticity':Q_deriv,'checks':result['verification']},indent=2))

if __name__=='__main__':main()

