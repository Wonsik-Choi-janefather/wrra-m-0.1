from pathlib import Path
import itertools,json,csv
B=Path(__file__).resolve().parent
# Declared local trial: 3 colors, u/d valence flavors. Fixed common input
# exactly supports 7 protons+1 neutron. No fitted prime->quark rule asserted.
# 8 of each color, total u15,d9. Electron budget7.
particles=[('u','r')]*5+[('d','r')]*3+[('u','g')]*5+[('d','g')]*3+[('u','b')]*5+[('d','b')]*3
# Choose one r,g,b sequentially; prioritize uud or udd. Restricted baryon
# construction only; uuu,ddd,mesons/antiquarks and excited states excluded.
def assemble(priority):
 stock={c:{'u':5,'d':3} for c in 'rgb'};counts={'p':0,'n':0}
 chosen=[]
 while True:
  found=False
  for target in priority:
   flavors=('u','u','d') if target=='p' else ('u','d','d')
   for fs in sorted(set(itertools.permutations(flavors))):
    if all(stock[c][f]>0 for c,f in zip('rgb',fs)):
     for c,f in zip('rgb',fs):stock[c][f]-=1
     counts[target]+=1;chosen.append(target);found=True;break
   if found:break
  if not found:break
 remu=sum(v['u'] for v in stock.values());remd=sum(v['d'] for v in stock.values())
 # Retain 7 input electrons, even if some remain unbound.
 q=counts['p']+2*remu/3-remd/3-7
 assert abs(q)<1e-12
 assert 2*counts['p']+counts['n']+remu==15
 assert counts['p']+2*counts['n']+remd==9
 return {'priority':priority,'protons':counts['p'],'neutrons':counts['n'],'electrons':7,'remaining_u':remu,'remaining_d':remd,'net_charge':q,'sequence':chosen,'color_stock':stock}
A=assemble(['p','n']);C=assemble(['n','p'])
# Enumerate feasible aggregate allocations rather than claim greedy optimal.
feasible=[]
for p in range(9):
 for n in range(9):
  if 2*p+n<=15 and p+2*n<=9 and p+n<=8:
   feasible.append({'p':p,'n':n,'remaining_u':15-2*p-n,'remaining_d':9-p-2*n,'used_quarks':3*(p+n)})
best=[x for x in feasible if x['used_quarks']==max(y['used_quarks'] for y in feasible)]
r={'input':'5u+3d per color, 7 electrons: prescribed target-compatible input, NOT inferred cosmic distribution','proton_first':A,'neutron_first':C,'maximum_use_aggregate_candidates':best,'physical_status':'color-compatible valence bookkeeping; no QCD binding energies or confinement evolution','unbound_quark_status':'unresolved model residual, NOT claim of observable free quarks; requires hadronization/other channels','neutrino_photon_status':'separate open branches; no conversion rates or spectra calculated','conclusion':'same constituents, different greedy binding priorities leave different baryon composition/residue; global all-quark use constrains composition for this chosen input'}
(B/'results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
