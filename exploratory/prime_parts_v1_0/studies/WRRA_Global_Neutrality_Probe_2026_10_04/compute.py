from pathlib import Path
import json,csv
B=Path(__file__).resolve().parent
# Same finite input as last trial. Four color-singlet-compatible valence
# flavors: uuu,uud,udd,ddd. No masses/stability/production rates assigned.
# Counts in u,d units; electric charges in e units: 2,1,0,-1.
species=[('uuu',3,0,2),('uud',2,1,1),('udd',1,2,0),('ddd',0,3,-1)]
rows=[]
for x in range(6):
 for p in range(8):
  for n in range(5):
   for y in range(4):
    u=3*x+2*p+n;d=p+2*n+3*y
    if u>15 or d>9 or x+p+n+y>8:continue
    ru=15-u;rd=9-d
    # three colors available; aggregate feasibility only, not matching solver.
    q=2*x+p-y-7+(2*ru-rd)/3
    assert abs(q)<1e-12
    rows.append({'uuu':x,'uud':p,'udd':n,'ddd':y,'remaining_u':ru,'remaining_d':rd,'used_quarks':u+d,'electrons':7,'whole_charge_e':q,'bound_plus_e_charge_e':2*x+p-y-7})
full=[r for r in rows if r['used_quarks']==24]
# For any full allocation Q_hadrons=7; electrons cancel. Degenerate species.
assert all(r['bound_plus_e_charge_e']==0 for r in full)
res={'input':'u15 d9 e7, same chosen trial inventory; not cosmological generation result','neutrality_constraint':'global sum_i N_i q_i=0 with unresolved reservoir charge included','scanned_allocations':len(rows),'full_use_allocations':len(full),'full_use_examples':full[:8],'counterexample_to_neutrality_selects_pne':'non-uud/udd candidates also globally neutral','constraints_not_added':['binding energies','stability','full spin/flavor and statistics','prime-to-quark rendering','antiquark/meson channels','initial physical baryon-lepton supply'], 'color_scope':'one rgb singlet can carry any listed flavor composition; aggregate feasible counts only, no full dynamical state','neutrality_scope':'electric charge tested only; signed weak/color/orientation variables need separate operators; not all signs one scalar','neutrino_photon':'electrically neutral outputs do not fix their abundance or energy; open ledger','conclusion':'whole charge conservation necessary but does not uniquely fix hadron composition, ordering, or neutral output fractions'}
(B/'results.json').write_text(json.dumps(res,indent=2)+'\n')
with (B/'neutral_allocations.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(res,indent=2))
