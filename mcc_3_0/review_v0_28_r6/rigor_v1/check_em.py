from pathlib import Path
import json
import mpmath as mp
from core import finite_em,em_analytic_bound
P=Path(__file__).parent;rows=[]
def high_em(s,M):
 return mp.fsum(mp.power(n,-s) for n in range(1,M))+mp.power(M,1-s)/(s-1)+mp.power(M,-s)/2+s/12*mp.power(M,-s-1)-s*(s+1)*(s+2)/720*mp.power(M,-s-3)
for dps in [50,80]:
 with mp.workdps(dps):
  s=mp.mpc(.5,mp.im(mp.zetazero(70)))
  for M in [7250,14500,29000]:
   v=high_em(s,M);ref=mp.zeta(s);b=em_analytic_bound(s,M);err=abs(v-ref)
   # For float evaluation compare against the same rounded complex argument.
   sd=complex(s);fd=finite_em(sd,M);floaterr=abs(mp.mpc(fd)-mp.zeta(mp.mpc(sd)))
   assert err<=b
   row={'dps':dps,'M':M,'high_precision_abs_error':mp.nstr(err,24),'exact_arithmetic_truncation_bound':mp.nstr(b,24),'float64_error_same_argument':float(floaterr),'bound_satisfied_high_precision':True};rows.append(row);print(json.dumps(row),flush=True)
with mp.workdps(80):
 a=rows[1];b=rows[4];stable=abs(mp.mpf(a['high_precision_abs_error'])-mp.mpf(b['high_precision_abs_error']))<mp.mpf('1e-40')
 assert stable
out={'rows':rows,'50_80_digit_error_agreement_abs_1e_40':stable,'bound_formula':'|(s)_5| M^(-Re(s)-5)/30240 + 2 zeta(6)/(2 pi)^6 |(s)_6| M^(-Re(s)-5)/(Re(s)+5)','domain':'Re(s)>-5; M integer>=2; s!=1','bound_scope':'analytic truncation in exact arithmetic; no interval certificate for floating rounding or library zero count','zero_index':70}
(P/'results/em_refinement.json').write_text(json.dumps(out,indent=2))
