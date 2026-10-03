from pathlib import Path
import json,csv
B=Path(__file__).resolve().parent
# Reconstruct all fully used allocations from preceding inventory.
mp=938.27208943;mn=939.56542194;me=.51099895069;mdelta=1232.;mpi=139.57039
rows=[]
for x in range(6):
 for p in range(8):
  for n in range(5):
   for y in range(4):
    if 3*x+2*p+n!=15 or p+2*n+3*y!=9:continue
    # Conditional identification uuu->Delta++, ddd->Delta-.
    # Delta++->p pi+; Delta-->n pi-; pion/muon chains yield e+/e-
    P=p+x;NN=n+y;em=7+y;ep=x
    annih=min(em,ep);em-=annih;ep-=annih
    assert P-em+ep==0 and P+NN==8
    initial=(x+y)*mdelta+p*mp+n*mn+7*me
    rest=P*mp+NN*mn+(em+ep)*me
    excess=initial-rest
    assert excess>=-1e-9
    # Free-neutron branch only: all n beta-decay if no nuclear protection.
    Pfree=P+NN;efree=em+NN
    assert Pfree-efree==0
    rows.append({'initial_Delta_pp':x,'initial_p':p,'initial_n':n,'initial_Delta_minus':y,'after_resonances_p':P,'after_resonances_n':NN,'electrons':em,'positrons':ep,'chain_neutrinos_antineutrinos':3*(x+y),'annihilation_photons_count':2*annih,'initial_rest_MeV':initial,'final_rest_MeV':rest,'nonrest_energy_budget_MeV':excess,'free_late_p':Pfree,'free_late_e':efree,'free_late_neutrino_count':3*(x+y)+NN})
assert len(rows)==11
r={'rows':rows,'input_scope':'fixed u15 d9 e7 inventory, conditional resonance identifications','verified_external_inputs':'PDG Delta mass approx1232MeV, charged pion mass139.57039MeV; prior p,n,e calibrated masses','Delta_pp_to_p_pi_Q_MeV':mdelta-mp-mpi,'Delta_minus_to_n_pi_Q_MeV':mdelta-mn-mpi,'checks':'all 11 charge+baryon budgets pass; nonrest budget nonnegative','rates':'not calculated; chains supplied as known comparison/decoder rules','energy_scope':'rest-energy difference available to kinetic/radiation/neutrino outputs, NOT calculated partition or spectrum','annihilation_photons_scope':'two-photon channel assumed after pair annihilation; energies and thermalization not calculated','late_free_scope':'isolated free-neutron decay limit only; bound neutron survival/helium formation not implemented','conclusion':'neutrality+decay allow non-pne output. Without capture/binding and time, target7:1:7 is not a guaranteed endpoint; free decay limit gives8:0:8.'}
(B/'results.json').write_text(json.dumps(r,indent=2)+'\n')
with (B/'decay_channels.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps({'Qpp':r['Delta_pp_to_p_pi_Q_MeV'],'Qminus':r['Delta_minus_to_n_pi_Q_MeV'],'examples':rows[:3]},indent=2))
