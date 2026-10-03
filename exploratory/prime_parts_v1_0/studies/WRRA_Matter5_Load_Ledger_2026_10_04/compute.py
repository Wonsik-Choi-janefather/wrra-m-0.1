from pathlib import Path
import numpy as np,json,csv
B=Path(__file__).resolve().parent;inp=json.loads((B/'input_abundance.json').read_text());p=np.array(inp['pool']);out=[];summary={}
# Explicit calibration model E(n)=epsilon*n, residual E(r)=epsilon*r.
# Not inferred from prior source Hamiltonian; address load is new assumption.
for name in ['small_first','large_first']:
 c=np.array(inp['profiles'][name]['expected_parts']);r=inp['tails'][name]['residue1_weight'];total=float(c@p+r)
 share=.05*c*p/total;rs=.05*r/total
 assert abs(share.sum()+rs-.05)<1e-14
 # Equal-energy-per-part alternative also budget normalized but changed E(n).
 equal=.05*c/c.sum()
 assert abs(equal.sum()-.05)<1e-14
 for j,prime in enumerate(p):out.append({'rule':name,'prime_label':int(prime),'linear_load_whole_universe_percent':float(share[j]*100),'equal_part_load_whole_universe_percent':float(equal[j]*100),'linear_pair_plus_and_minus_counts_equal':True})
 summary[name]={'conditional_mean_address_load_units':total,'residual_whole_universe_percent':rs*100,'component_whole_universe_percent':float(share.sum()*100),'whole_matter_budget_percent':float((share.sum()+rs)*100)}
assert abs(summary['small_first']['conditional_mean_address_load_units']-summary['large_first']['conditional_mean_address_load_units'])<1e-9
r={'input_scope':'conditional admitted 5% arithmetic weights','new_load_assumption':'E(n)=epsilon*n, each component E(p)=epsilon*p, residual E(r)=epsilon*r; epsilon fixed to fit whole-universe 5%','calibration_status':'5% imposed common budget, not new derived observation','summary':summary,'rows':out,'energy_and_charge':'linear arithmetic load conserved; +/- equal-count pairing compatible; physical mass/spin/species not identified','residual_status':'included within 5% load as unresolved residue, not automatically dark matter or source return','equal_part_alternative':'same fixed 5% total but different per-address load function; demonstrates load-map sensitivity','conclusion':'Under declared common linear load both assembly orders preserve the same total while allocating it differently. Species and SI energy map remain open.'}
(B/'results.json').write_text(json.dumps(r,indent=2)+'\n')
with (B/'whole_universe_load.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print(json.dumps({'summary':summary,'first_rows':out[:3]+out[15:18]},indent=2))
