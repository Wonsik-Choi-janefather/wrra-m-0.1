#!/usr/bin/env python3
"""Separate SM channel response audit on the supplied 15-chiral-channel carrier.

Representation content is an input from the frozen MCC/WRRA baseline and
the standard-model quantum numbers. This audit computes operators, color
singlet response, charge and spin addition, not prime selection or coupling
strengths from arithmetic factorization.
"""
from pathlib import Path
import itertools
import json
import numpy as np

ROOT=Path(__file__).resolve().parent

def main():
 # Order: four quark multiplets, each with three colors; three leptons.
 channels=[]
 for flavor,Y,T3 in [('uL',1/6,.5),('dL',1/6,-.5),('uR',2/3,0),('dR',-1/3,0)]:
  for color in ('r','g','b'):
   channels.append({'label':flavor+'_'+color,'color':color,'hypercharge_Y':Y,
                    'weak_T3':T3,'electric_Q_e':T3+Y,'spin':.5})
 for flavor,Y,T3 in [('nuL',-.5,.5),('eL',-.5,-.5),('eR',-1.,0.)]:
  channels.append({'label':flavor,'color':None,'hypercharge_Y':Y,
                   'weak_T3':T3,'electric_Q_e':T3+Y,'spin':.5})
 Y=np.diag([c['hypercharge_Y'] for c in channels])
 T3=np.diag([c['weak_T3'] for c in channels])
 Q=np.diag([c['electric_Q_e'] for c in channels])
 Tp=np.zeros((15,15),dtype=complex)
 for c in range(3):Tp[c,3+c]=1
 Tp[12,13]=1
 Tm=Tp.conj().T
 # Gell-Mann generators in fundamental color representation.
 gm=[np.array(x,dtype=complex) for x in [
  [[0,1,0],[1,0,0],[0,0,0]],[[0,-1j,0],[1j,0,0],[0,0,0]],
  [[1,0,0],[0,-1,0],[0,0,0]],[[0,0,1],[0,0,0],[1,0,0]],
  [[0,0,-1j],[0,0,0],[1j,0,0]],[[0,0,0],[0,0,1],[0,1,0]],
  [[0,0,0],[0,0,-1j],[0,1j,0]],np.diag([1,1,-2])/np.sqrt(3)]]
 color_generators=[]
 for g in gm:
  t=np.zeros((15,15),dtype=complex)
  for base in (0,3,6,9):t[base:base+3,base:base+3]=g/2
  color_generators.append(t)
 I3=np.eye(3)
 singlet=np.zeros(27,dtype=complex)
 for perm in itertools.permutations(range(3)):
  inversions=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
  singlet[perm[0]*9+perm[1]*3+perm[2]]=(-1)**inversions/np.sqrt(6)
 color_norms=[]
 for g in gm:
  t=g/2
  total=np.kron(np.kron(t,I3),I3)+np.kron(np.kron(I3,t),I3)+np.kron(np.kron(I3,I3),t)
  color_norms.append(float(np.linalg.norm(total@singlet)))
 # Three spin-1/2 constituents: build total J^2 independently of addresses.
 pauli=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
 I2=np.eye(2);Js=[]
 for s in pauli:
  Js.append((np.kron(np.kron(s,I2),I2)+np.kron(np.kron(I2,s),I2)+np.kron(np.kron(I2,I2),s))/2)
 J2=sum(j@j for j in Js)
 spin_eigen=np.linalg.eigvalsh(J2)
 checks={
  'carrier_has_15_channels':len(channels)==15,
  'Q_equals_T3_plus_Y':float(np.max(np.abs(Q-T3-Y)))<1e-14,
  'weak_raise_charge_commutator':float(np.max(np.abs(Q@Tp-Tp@Q-Tp)))<1e-14,
  'weak_SU2_commutator':float(np.max(np.abs(Tp@Tm-Tm@Tp-2*T3)))<1e-14,
  'color_commutes_with_weak_raise':all(np.max(np.abs(t@Tp-Tp@t))<1e-14 for t in color_generators),
  'color_commutes_with_EM_charge':all(np.max(np.abs(t@Q-Q@t))<1e-14 for t in color_generators),
  'three_color_singlet_normalized':abs(float(np.vdot(singlet,singlet).real)-1)<1e-14,
  'three_color_singlet_total_color_zero':max(color_norms)<1e-14,
  'three_spins_have_two_half_multiplets':int(np.count_nonzero(np.isclose(spin_eigen,.75)))==4,
  'three_spins_have_one_three_half_multiplet':int(np.count_nonzero(np.isclose(spin_eigen,3.75)))==4,
 }
 assert all(checks.values()),checks
 result={'title':'WRRA M separate channel response audit v0.1','date':'2026-10-01',
  'carrier_status':'supplied one-generation 15-chiral-channel representation content; antiparticle channels are conjugate representations, not extra entries in this basis',
  'hypercharge_convention':'Q = T3 + Y, with this Y equal to one half of the Y used in the PDG convention Q = T3 + Y_PDG/2',
  'state_record_schema':{
   'address':'candidate arithmetic residue label; may be shared by several internal states',
   'sector':'baryon, lepton or other selected physical readout sector',
   'valence':'net valence flavor counts; not the entire QCD constituent content',
   'internal_state':'color, chirality, spin-flavor-spatial state, orbital excitation and density matrix',
   'additional_QCD_content':'sea quark-antiquark pairs and gluons enter the effective state and response, not fixed prime multiplicities here',
   'environment':'free particle or bound system, external fields, scale and renormalization scheme',
   'response_parameters':'constrained energy, current and transition kernels; parameters must have independent input or a recorded calibration',
  },
  'channels':channels,
  'separate_responses':{
   'constituents':'valence flavor and channel counts; address prime factors are candidate labels',
   'strong':'eight color generators on each quark color triplet; three-quark color-singlet invariance checked. Binding energy and alpha_s running are separate constitutive inputs.',
   'residual_nuclear':'inter-nucleon binding and effective nuclear interactions require a bound-system environment; not computed by the free-nucleon color audit',
   'weak':'four left doublets (three colored quark and one lepton); right channels weak singlets. Raising dL->uL and eL->nuL computed. Transition strengths, mixing and gA are further inputs.',
   'electromagnetic':'Q=T3+Y; electric charges and signed magnetic-current readout are distinct',
   'spin':'three spin halves yield two spin-half multiplets and one spin-three-half multiplet; a full spin-flavor-spatial state must choose the branch',
   'mass':'shared nucleon energy response in the companion trial; not integer product or Omega alone',
   'decay':'allowed flavor-channel transition, energy condition and rate; Actual energy retention is distinct from phenotype lifetime'},
  'coupling_inputs_recorded':{'inverse_fine_structure_constant':137.035999177,
                            'Fermi_coupling_GeV_minus2':1.1663787e-5,
                            'strong_coupling':'must specify scale and renormalization scheme; no numerical alpha_s fit in this audit'},
  'color_singlet_total_generator_norms':color_norms,
  'spin_J_squared_eigenvalues_hbar2':spin_eigen.tolist(),
  'verification':{**checks,'all_passed':all(checks.values())},
  'sources':['https://pdg.lbl.gov/2026/reviews/rpp2026-rev-standard-model.pdf',
             'https://pdg.lbl.gov/2026/reviews/rpp2026-rev-quark-model.pdf',
             'https://physics.nist.gov/cuu/Constants/Table/allascii.txt'],
 }
 (ROOT/'channel_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({'channel_count':len(channels),'spin_eigenvalues':spin_eigen.tolist(),'verification':result['verification']},indent=2))

if __name__=='__main__':main()
