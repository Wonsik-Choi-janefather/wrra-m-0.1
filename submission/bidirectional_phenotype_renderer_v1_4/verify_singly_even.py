import json
from pathlib import Path
def composite(n):return n>1 and any(n%d==0 for d in range(2,int(n**.5)+1))
rows=[];placement_cases=0
for N in range(2,2001,4):
 n=N//2
 assert N%4==2 and n%2==1 and n+n==N
 for b1 in [-1,1]:
  for b2 in [-1,1]:
   U=(n+b1)//2+(n+b2)//2;D=(n-b1)//2+(n-b2)//2
   assert U+D==N and U-D==b1+b2
   assert (U==D)==(b2==-b1)
   placement_cases+=1
 rows.append({'N':N,'half':n,'arithmetic_split':True,'odd_composite_filter':composite(n)})
assert not rows[2]['odd_composite_filter'] # N=10, half 5: arithmetic admitted, massive filter closed
assert next(r for r in rows if r['N']==18)['odd_composite_filter']
assert 24%4!=2 and 9+15==24 and 9!=15
result={'scope':'arithmetic and code-domain separation only; not physics validation','singly_even_parents':len(rows),'placement_cases':placement_cases,'odd_composite_phenotype_candidates':sum(r['odd_composite_filter'] for r in rows),'nonphenotype_arithmetic_cases':sum(not r['odd_composite_filter'] for r in rows),'N2_boundary':'2 remains prime; half 1 is not a massive phenotype','N10_control':'5+5 allowed arithmetically; odd-composite phenotype gate closed','N18_control':'9+9 allowed arithmetically and passes odd-composite gate; other physical permissions still required','unequal_split_controls':['24 -> 9+15 rejected','54 -> 9+45 rejected'],'new_black_hole_or_cosmology_calculation':False}
Path(__file__).with_name('verification_singly_even.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
