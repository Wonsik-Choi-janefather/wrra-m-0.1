from pathlib import Path
import math,csv,json
B=Path(__file__).resolve().parent
# Conditional initial neutron fraction from previous fixed decoder.
f=.12483936387544717;tau=878.3
rows=[]
# Effective n-capture sink vs beta decay, prescribed finite window.
# No full nuclear reaction network or fitted physical capture rate.
for ratio in [0,.1,1,10,100]:
 for T in [30,180,600]:
  d=1/tau;k=ratio*d;total=d+k
  free=f*math.exp(-total*T)
  captured=f*k/total*(1-math.exp(-total*T))
  decayed=f*d/total*(1-math.exp(-total*T))
  proton=1-f+decayed;electron=proton
  assert abs(free+captured+decayed-f)<1e-14
  assert abs(proton+free+captured-1)<1e-14
  # Potential He4 proxy: captured neutrons paired with equal protons.
  # Captures insufficient to establish actual He4 formation.
  he_proxy=2*captured
  h_proxy=proton-captured
  assert h_proxy>=0
  rows.append({'capture_decay_rate_ratio':ratio,'window_s':T,'free_neutron_fraction':free,'captured_neutron_fraction':captured,'beta_decayed_fraction':decayed,'proton_fraction':proton,'electron_fraction':electron,'helium4_mass_proxy':he_proxy,'hydrogen_mass_proxy':h_proxy,'free_neutron_mass_proxy':free,'beta_antineutrino_per_initial_baryon':decayed})
r={'input_neutron_fraction':f,'input_status':'prior calibrated arithmetic decoder candidate, not derived physical freezeout abundance','lifetime_s':tau,'capture_model':'constant effective lambda_capture/lambda_decay; finite exposure time; capture sink not nuclear network','cases':len(rows),'target_helium_mass_proxy':.25,'max_possible_proxy_no_neutron_loss':2*f,'results':rows,'energy':'mass-energy release and photon spectrum not calculated in this count model','conclusion':'near25% neutron-derived He proxy requires high capture survival. Rough baryon target alone cannot choose prime pool/order because capture and decay change endpoint.'}
(B/'results.json').write_text(json.dumps(r,indent=2)+'\n')
with (B/'capture_grid.csv').open('w') as file:
 w=csv.DictWriter(file,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps([x for x in rows if x['window_s']==180],indent=2))
