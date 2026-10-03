from pathlib import Path
import numpy as np,json,csv,math
B=Path(__file__).resolve().parent;N=1000000
s=np.ones(N+1,bool);s[:2]=False
for p in range(2,1001):
 if s[p]:s[p*p::p]=False
v=np.arange(2,N+1);n=v[(v%2==1)&~s[2:]];pool=np.flatnonzero(s)[:15]
w=v.astype(float)**(-1.8996876950554356);w/=w.sum();w=.8654570124136961*w[(v%2==1)&~s[2:]];w/=w.sum()
profiles={};tails={}
for name,parts in [('small_first',pool),('large_first',pool[::-1])]:
 cyc=n//parts.sum();c=np.repeat(cyc[:,None],15,axis=1);r=n-cyc*parts.sum()
 # Same one-each cyclic rule as prior task; stop when no prime fits.
 for it in range(int(parts.sum())//2+1):
  for j,p in enumerate(parts):
   t=r>=p;c[:,j]+=t;r-=p*t
  if np.all(r<2):break
 assert np.all(c@parts+r==n)
 expected=w@c;order=np.argsort(parts);expected=expected[order]
 profiles[name]={'expected_parts':expected,'number_share':expected/expected.sum()}
 tails[name]={'residue1_weight':float(w[r==1].sum()),'expected_parts':float(expected.sum())}
# Alternative completed ascending rule: 2 repeated, reserve 3 on odd input.
e=np.zeros(15);e[0]=float(w@((n-3)//2));e[1]=1
profiles['small_repeat_avoid1']={'expected_parts':e,'number_share':e/e.sum()}
# Neutral +/- pair rendering adds one + and one - per component.
# Labels here are NOT proton/electron or known species assignments.
for data in profiles.values():
 data['expected_plus']=data['expected_parts'].copy();data['expected_minus']=data['expected_parts'].copy()
 assert np.all(data['expected_plus']==data['expected_minus'])
# Same monotone numerical energy proxy in both rules, for sensitivity only.
# Prime integer is NOT a measured rest mass.
for data in profiles.values():
 data['address_value_share']=data['expected_parts']*pool/(data['expected_parts']@pool)
rows=[]
for i,p in enumerate(pool):
 row={'prime_label':int(p)}
 for name,data in profiles.items():
  row[name+'_number_percent']=float(100*data['number_share'][i]);row[name+'_address_value_percent']=float(100*data['address_value_share'][i])
 rows.append(row)
with (B/'component_abundance.csv').open('w') as f:
 wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
a=profiles['small_first']['number_share'];b=profiles['large_first']['number_share']
res={'addresses':len(n),'pool':pool.tolist(),'weight_scope':'conditional admitted phenotype weight, not physical particle population',
 'number_distribution_total_variation':float(np.abs(a-b).sum()/2),'tails':tails,
 'profiles':{k:{z:x.tolist() for z,x in data.items()} for k,data in profiles.items()},
 'charge_pair_rule':'each component -> one + and one - template; equality constructed, not derived',
 'physical_mass_ratio':'not determined without component-to-species and energy map',
 'relabeling_ambiguity':'15 distinct species labels allow up to 15! assignments; counts alone do not select names',
 'relabeling_count':math.factorial(15),'energy_ratio_formula':'R_a = expected_count_a * E_a / sum_b(expected_count_b * E_b)',
 'scope':'arithmetic composition and conditional pair counts calculated; no physical force/spin/species spectrum claimed'}
(B/'results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'total_variation':res['number_distribution_total_variation'],'tails':tails,'first5':rows[:5]},indent=2))
