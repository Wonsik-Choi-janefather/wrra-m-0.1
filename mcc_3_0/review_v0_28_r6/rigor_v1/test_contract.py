from pathlib import Path
import json,math
import numpy as np
import mpmath as mp
import core
P=Path(__file__).parent;checks=[]
def check(n,b):
 if not b:raise AssertionError(n)
 checks.append(n)
def rejects(n,fn,code):
 try:fn()
 except ValueError as e:check(n,code in str(e));return
 raise AssertionError(n+' accepted invalid input')
check('exact L and integer shares',core.resolution(['0.05','0.268','0.682'])==(500,[25,134,341]))
check('changed calibration recomputes L',core.resolution(['0.0501','0.268','0.6819'])[0]==10000)
for n,x in [('nonunit',['.1','.2']),('negative',['-.1','1.1'])]:rejects(n,lambda:core.resolution(x),'SHARES_')
rejects('binary floats not silently exact',lambda:core.resolution([.05,.268,.682]),'STRINGS')
for n,args in [('negative ell',(-1,0,1)),('ell upper',(500,0,1)),('h upper',(0,29,1)),('z lower',(0,0,0)),('z upper',(0,0,71)),('bool index',(True,0,1)),('float index',(0.0,0,1))]:rejects(n,lambda:core.encode(*args,500,29,70),'INVALID_INTEGER' if n in ['negative ell','bool index','float index'] else 'OUT_OF_DOMAIN')
for n in [0,1015001]:rejects('address '+str(n),lambda:core.decode(n,500,29,70),'INVALID_INTEGER' if n==0 else 'OUT_OF_DOMAIN')
rejects('budget before allocation',lambda:core.ledger(10000,29,70,1.9),'BUDGET')
rejects('NaN alpha',lambda:core.ledger(2,2,2,float('nan')),'ALPHA')
rejects('underflow rejected',lambda:core.ledger(500,29,70,100),'UNDERFLOW')
check('empty spectrum ledger valid empty',len(core.ledger(500,1,0,1.9)['n'])==0)
rejects('empty spectrum no address',lambda:core.encode(0,0,1,500,1,0),'OUT_OF_DOMAIN')
check('small H empty spectrum',core.window(1)['C']==0)
check('nondefault H uses argument',core.window(3)['C']==1)
rejects('invalid H zero',lambda:core.window(0),'INVALID_INTEGER')
for t,c in [(0,0),(1,0),(2,1),(3,2)]:check('strict synthetic threshold '+str(t),core.spectral_count([mp.mpf(1),mp.mpf(2),mp.mpf(3)],mp.mpf(t))==c)
rejects('unsorted spectrum',lambda:core.spectral_count([2,1],1),'UNORDERED')
rejects('unbracketed spectrum',lambda:core.spectral_count([1,2],3),'UNBRACKETED')
rejects('zeta pole',lambda:core.finite_em(1,100),'POLE')
rejects('bad EM cutoff',lambda:core.finite_em(.5+1j,1),'INVALID_INTEGER')
rejects('nonfinite s',lambda:core.finite_em(complex('nan'),100),'NONFINITE')
rejects('remainder outside domain',lambda:core.finite_em(-5+1j,100),'BOUND_DOMAIN')
for N in [1,2,3,4,9,25,49,121]:
 a=core.ledger(N,1,1,1.9)
 def trial(n):return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
 exp=[0 if n==1 else 1 if trial(n) else 2 if n%2==0 else 3 for n in range(1,N+1)]
 check('small exact classification '+str(N),a['kind'].tolist()==exp)
# Every (ell,h) on both seam boundaries and a double full return at every ell.
for ell in range(500):
 for h in range(29):
  for z in [1,70]:
   x=(ell,h,z);y=core.seam(*x,500,29,70);assert core.seam(*y,500,29,70,inverse=True)==x
 x=(ell,0,1);y=x
 for j in range(70):y=core.seam(*y,500,29,70)
 assert y==((-ell)%500,0,1)
 for j in range(70):y=core.seam(*y,500,29,70)
 assert y==x
check('29000 seam boundary inverses',True);check('500 one-cycle reflections and double returns',True)
# Pinpoint the legacy global-H and empty-list defects with synthetic ordered zeros.
import importlib.util
spec=importlib.util.spec_from_file_location('legacy',P/'original/code/compute.py');legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
realzero=legacy.mp.zetazero
try:
 legacy.mp.zetazero=lambda k:mp.mpc(.5,10*k)
 r=legacy.zeta_focus_count(3,100)
 check('legacy nondefault-H defect reproduced with synthetic zeros',len(r['boundary_scan'])==29)
 try:legacy.zeta_focus_count(1,100)
 except ValueError:check('legacy empty-spectrum crash reproduced',True)
 else:raise AssertionError('legacy empty case unexpectedly succeeded')
finally:legacy.mp.zetazero=realzero
out={'passed':len(checks),'checks':checks,'synthetic_threshold_tests_are_not_measured_zeros':True,'seam_is_existing_coordinate_convention_not_spacetime_measurement':True}
(P/'results/contract_tests.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
