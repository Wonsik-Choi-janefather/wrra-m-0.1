from pathlib import Path
import json,itertools,numpy as np,csv
B=Path(__file__).resolve().parent;fit=json.loads((B/'input_fit.json').read_text())
# Explicit color singlet epsilon_rgb, NOT complete nucleon wavefunction.
psi=np.zeros((3,3,3),complex)
for perm in itertools.permutations(range(3)):
 inv=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3));psi[perm]=(-1)**inv/np.sqrt(6)
assert abs(np.vdot(psi,psi)-1)<1e-14
# Check total color generators annihilate singlet (all 8 Gell-Mann).
z=np.zeros((3,3),complex);G=[]
for i,j in [(0,1),(0,2),(1,2)]:
 x=z.copy();x[i,j]=x[j,i]=1;G.append(x)
 x=z.copy();x[i,j]=-1j;x[j,i]=1j;G.append(x)
G.extend([np.diag([1,-1,0]),np.diag([1,1,-2])/np.sqrt(3)])
errors=[]
for g in G:
 v=np.einsum('ia,ajk->ijk',g,psi)+np.einsum('ja,iak->ijk',g,psi)+np.einsum('ka,ija->ijk',g,psi)
 errors.append(float(np.linalg.norm(v)))
assert max(errors)<1e-14
# Coarse calibrated composition used only as candidate output.
rows=[]
for name in ['small_first','large_first']:
 f=fit['joint_fit'][name]['neutron_motif_fraction']
 for withheld in [0,.05,.2]:
  P=(1-withheld)*(1-f);Ne=P;N=(1-withheld)*f
  U=2*P+N;D=P+2*N
  assert abs(2*U/3-D/3-Ne)<1e-14
  rows.append({'rule':name,'withheld_component_fraction':withheld,'proton':P,'neutron':N,'electron':Ne,'valence_u':U,'valence_d':D,'valence_u_per_d':U/D,'neutrino_photon_unresolved_branch':withheld,'net_charge':2*U/3-D/3-Ne})
# Physical rest energies are calibrated external inputs, no quark binding inferred.
mp=938.27208943;mn=939.56542194;me=.51099895069
# neutron beta transition ledger: d -> u + e- + anti-nu_e, energy released.
Q=mn-mp-me
assert Q>0 and abs(-1/3-(2/3-1))<1e-14
r={'color_singlet_norm':float(np.vdot(psi,psi).real),'color_generator_residuals':errors,'rows':rows,
 'beta_transition_Q_MeV':Q,'beta_decay_scope':'charge and calibrated rest-energy difference only; rate, weak amplitude, neutrino spectrum not computed',
 'all_information_assigned_to_pne':False,'withheld_scope':'0/5/20% hypothetical component routing fractions, NOT cosmic measured energy fractions or a fitted neutrino abundance',
 'non_baryonic_outputs':['neutrino and antineutrino','photon','unresolved state/residue'],
 'CMB_candidate_condition':'photon spectral occupation must match blackbody around 2.72548K; residue amount alone insufficient',
 'CMB_source':'https://lambda.gsfc.nasa.gov/resources/lambda_graphics/cmb_monopole.html',
 'CMB_energy_fraction_reference':5.38e-5,'CMB_fraction_scope':'external present-day critical-density fraction; not included silently in baryon 5%',
 'quark_scope':'valence bookkeeping and color singlet tested; sea/gluons, full spin-flavor wavefunction, confinement and binding Hamiltonian not calculated',
 'status':'lower-level structural test, not complete nucleon assembly'}
(B/'results.json').write_text(json.dumps(r,indent=2)+'\n')
with (B/'quark_open_branches.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps({'color_max_error':max(errors),'beta_Q':Q,'rows':rows[:3]},indent=2))
