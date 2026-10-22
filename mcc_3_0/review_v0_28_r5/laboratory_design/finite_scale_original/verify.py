"""Independent modal/Parseval audit of the receiver CSV, without a grid solve."""
from pathlib import Path
import csv,json,math
import numpy as np
P=Path(__file__).resolve().parent
modes=[((1,0,0),.05),((1,2,0),.025),((1,1,1),.01)]
errors=[]
for row in csv.DictReader((P/'refinement.csv').open()):
 h=1/int(row['n']);pn=pd=gn=gd=0.
 for mt,a in modes:
  k=2*np.pi*np.array(mt);k2=k@k;lam=sum((2*np.sin(k*h/2)/h)**2)
  pn+=(a/lam-a/k2)**2;pd+=(a/k2)**2
  gn+=sum((a*np.sin(k*h)/(h*lam)-a*k/k2)**2)
  gd+=sum((a*k/k2)**2)
 for field,value in [('poisson_relative_L2',math.sqrt(pn/pd)),('center_force_relative_L2',math.sqrt(gn/gd))]:
  errors.append(abs(value-float(row[field])))
  assert errors[-1]<2e-13,(field,row['n'],value,row[field])
# Independently check the sufficient error thresholds by the defining inequalities.
d=json.loads((P/'results.json').read_text());b=d['scale_bounds']
assert abs((2*math.pi/b['wave_1percent_min_wavelength_cells'])**2/12-(2*.01-.01**2))<1e-15
assert abs((2*math.pi/b['poisson_1percent_min_wavelength_cells'])**2/12-.01/1.01)<1e-15
# Re-evaluate coarsening invariants from every exported row.
rows=list(csv.DictReader((P/'source_coarse_graining.csv').open()))
assert len(rows)==16
assert max(float(r['sector_integral_relative_error']) for r in rows)<1e-14
assert all((r['alias_free_for_original_7_modes']=='True')==(int(r['coarse_cells'])>14) for r in rows)
result={'method':'Independent modal/Parseval calculation; CSV conservation and threshold audit', 'max_absolute_difference_from_grid_L2_errors':max(errors),'status':'PASS','scope':'Algebraic cross-check, not an external review or observational validation'}
(P/'independent_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
