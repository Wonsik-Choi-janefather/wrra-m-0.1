from pathlib import Path
import json,numpy as np,csv
B=Path(__file__).resolve().parent;inp=json.loads((B/'input_abundance.json').read_text());pool=inp['pool']
a=np.array(inp['profiles']['small_first']['expected_parts']);b=np.array(inp['profiles']['large_first']['expected_parts'])
# New coarse decoder: each component -> either neutral p+e motif OR neutron.
# All 15 components retained; assignment common across assembly orders.
# n/p target=1/7 => neutron motif share 1/8 among component occurrences.
# Exhaustively fit contiguous threshold and all binary subsets separately.
rows=[]
for mask in range(1,2**15-1):
 neutron=np.array([(mask>>j)&1 for j in range(15)],bool)
 fa=float(a[neutron].sum()/a.sum());fb=float(b[neutron].sum()/b.sum())
 rows.append((mask,fa,fb,abs(fa-.125),abs(fb-.125)))
bestA=min(rows,key=lambda x:x[3]);bestB=min(rows,key=lambda x:x[4]);bestBoth=min(rows,key=lambda x:max(x[3],x[4]))
def output(row):
 mask,fa,fb,ea,eb=row
 ret={'neutron_prime_labels':[p for j,p in enumerate(pool) if mask>>j&1],'assignment_status':'fitted candidate, not derived particle identity'}
 for name,f in [('small_first',fa),('large_first',fb)]:
  # Motif count normalization gives p=e=1-f, n=f.
  vec=np.array([1-f,f,1-f]);ret[name]={'neutron_motif_fraction':f,'p_n_e_number_percent':(100*vec/vec.sum()).tolist(),'p_per_n':(1-f)/f,'helium_mass_fraction_proxy':2*f,'net_charge':0}
 return ret
threshold=[]
for t in pool:
 for side in ['below_equal','above_equal']:
  m=np.array([p<=t if side=='below_equal' else p>=t for p in pool]);fa=float(a[m].sum()/a.sum());fb=float(b[m].sum()/b.sum())
  threshold.append({'threshold':t,'side':side,'small_fraction':fa,'large_fraction':fb,'max_error':max(abs(fa-.125),abs(fb-.125))})
bestT=min(threshold,key=lambda x:x['max_error'])
res={'target':{'p_n_e':[7,1,7],'neutron_motif_fraction':.125,'helium_mass_fraction_proxy':.25,'scope':'rough H75/He25 primordial matter proxy, not all cosmic particles'},'decoder':'each assembled component makes one declared p+e neutral motif or one neutron; no antiproton/electron-positron requirement','masks_scanned':len(rows),'fit_small_apply_both':output(bestA),'fit_large_apply_both':output(bestB),'joint_fit':output(bestBoth),'best_contiguous_threshold_joint':bestT,'limitations':['assignment is calibrated to target; cannot claim independent recovery','helium proxy assumes all neutrons incorporated in He4 and proton surplus in H; no synthesis dynamics','mass/energy per-address conservation, baryon/lepton origin, spin/color binding not demonstrated','p/e equal by decoder construction; not a derived consequence','prior +/- identical-template pairs revised to different-species p+e neutral motifs; neutron neutral motif included','retained residue1 not assigned to species; abundance table conditions on assembled parts'],'input_sources':['input_abundance.json','NASA https://imagine.gsfc.nasa.gov/ask_astro/cosmology.html H/He rough composition']}
(B/'results.json').write_text(json.dumps(res,indent=2)+'\n')
with (B/'all_assignments.csv').open('w') as f:
 wr=csv.writer(f);wr.writerow(['mask','small_neutron_motif_fraction','large_neutron_motif_fraction','small_target_abs_error','large_target_abs_error']);wr.writerows(rows)
print(json.dumps({k:res[k] for k in ['fit_small_apply_both','fit_large_apply_both','joint_fit','best_contiguous_threshold_joint']},indent=2))
