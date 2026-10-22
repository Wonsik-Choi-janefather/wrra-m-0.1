"""Implementation-convention tests; no cosmological length is inferred."""
from fractions import Fraction as F
from math import lcm, pi, sqrt, isclose
import numpy as np
import mpmath as mp
import json
from pathlib import Path
checks=[]
def check(name,ok):
 checks.append({'name':name,'pass':bool(ok)})
 if not ok: raise AssertionError(name)
L=lcm(*(x.denominator for x in [F('0.05'),F('0.268'),F('0.682')]))
H=29; threshold=2*mp.pi*H
C=int(mp.nzeros(threshold)); N=L*H*C
check('declared SOURCE count',N==1015000)
a=np.arange(N,dtype=np.int64); ell=a%L; h=(a//L)%H; z=a//(L*H)+1
check('all address serialization round trips',np.array_equal(1+ell+L*(h+H*(z-1)),a+1))
check('active carrier basis', (N-1)*128==129919872)
# Synthetic energies and transfer convention, not a fitted SOURCE allocation.
E=[F(2),F(3),F(5)]; K=[[F(1,2),F(0),F(0)],[F(1,2),F(1),F(0)],[F(0),F(0),F(1)]]
check('column stochastic transfer',all(sum(row[n] for row in K)==1 for n in range(3)))
Ej=[sum(row[n]*E[n] for n in range(3)) for row in K]
vol=[F(1,3),F(2,3)]; density=[Ej[j]/vol[j] for j in range(2)]; reserve=Ej[2]
check('spatial plus reserve conservation',sum(density[j]*vol[j] for j in range(2))+reserve==sum(E))
check('omit reserve negative control detected',sum(density[j]*vol[j] for j in range(2))!=sum(E))
check('volume weighted coarsening',sum(density[j]*vol[j] for j in range(2))/sum(vol)==sum(Ej[:2])/sum(vol))
check('fixed energy doubled physical length',F(10)/F(2)**3==F(10)*F(1,8))
G=6.67430e-11; rho=2e-20; length=3e19
potential=4*pi*G*rho*length**2; acceleration=potential/length
check('Poisson unit restoration',isclose(acceleration,4*pi*G*rho*length,rel_tol=1e-14))
delta=.01; cells=2*pi/sqrt(12*delta/(1+delta)); eps=(2*pi/cells)**2/12
check('inverse Poisson one percent bound',isclose(eps/(1-eps),delta,rel_tol=1e-14))
out={'L':L,'H':H,'C':C,'N_U':N,'poisson_1percent_min_wavelength_cells':cells,'checks':checks,'passed':len(checks),'scope':'Declared address construction and synthetic unit/conservation interface; not cosmic-scale calibration'}
Path(__file__).with_name('scale_contract_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
