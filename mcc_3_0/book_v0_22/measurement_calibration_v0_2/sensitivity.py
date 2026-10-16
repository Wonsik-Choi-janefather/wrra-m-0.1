"""Conditional measurement-design audit; no measured values fitted."""
from pathlib import Path
import json,math
import numpy as np
R=Path(__file__).resolve().parent
REF=R.parent/'evidence'/'zeta_output_2026_10_16'/'zeta_superposition_v01'

def main():
 N=1015000;shape=(213,65,77);M=math.prod(shape);alpha=1.8996877935161325
 omega=np.zeros(N+1,dtype=np.int8);prime=np.ones(N+1,bool);prime[:2]=False
 for p in range(2,math.isqrt(N)+1):
  if prime[p]:prime[p*p::p]=False
 for p in np.flatnonzero(prime):omega[p::p]+=1
 ns=np.flatnonzero(omega>=2);ln=np.log(ns);index=np.ravel_multi_index(tuple(ns%m for m in shape),shape)
 g=np.loadtxt(REF/'zero_heights.csv',skiprows=1);C=len(g)
 k=np.zeros(len(ns),complex);kp=k.copy()
 for j,t in enumerate(g):
  v=np.exp(-1j*t*ln)/C;k+=v;kp+=v*np.exp(1j*.05*(2*j/(C-1)-1))
 axislam=[]
 for a,m in enumerate(shape):
  dims=[1]*3;dims[a]=m;axislam.append((4*np.sin(np.pi*np.arange(m)/m)**2).reshape(dims))
 def run(aa,kk,q):
  seed=ns.astype(float)**(-aa/2);seed/=np.linalg.norm(seed)
  field=np.zeros(M,complex);field[index]=seed*kk
  ev=np.exp(-1j*sum(x*w for x,w in zip(axislam,q)))
  out=np.fft.ifftn(ev*np.fft.fftn(field.reshape(shape),norm='ortho'),norm='ortho')
  I=abs(out)**2;P=I.sum();hold=np.sum((1-abs(kk)**2)*abs(seed)**2)
  assert abs(P+hold-1)<2e-12
  return I/P,float(P),float(abs(P+hold-1))
 base,P0,e=run(alpha,k,[1,1,1]);rows=[]
 for name,aa,kk,q in [('alpha_plus_0.05',alpha+.05,k,[1,1,1]),('phase_profile_0.05_rad',alpha,kp,[1,1,1]),('axis0_coupling_plus_5pct',alpha,k,[1.05,1,1]),('all_phase_plus_0.05_rad',alpha,k*np.exp(.05j),[1,1,1])]:
  p,P,err=run(aa,kk,q)
  rows.append(dict(case=name,TV=float(.5*abs(p-base).sum()),output_probability=P,relative_output_change=P/P0-1,conservation_error=err,
   axis_marginal_TV=[float(.5*abs(p.sum(axis=tuple(j for j in range(3) if j!=a))-base.sum(axis=tuple(j for j in range(3) if j!=a))).sum()) for a in range(3)]))
 assert rows[-1]['TV']<1e-12
 assert abs(rows[2]['relative_output_change'])<1e-12
 # d only attaches SI coordinates; it is absent from this dimensionless U=exp(-iL).
 out=dict(baseline=dict(shape=shape,N=N,selected=len(ns),alpha=alpha,output_probability=P0),cases=rows,
 metric_scale_identifiability='No sensitivity of dimensionless intensities or output probability to d under fixed U=exp(-iL); need a length/time measurement.',
 scope='Synthetic conditional sensitivities. TV is not an experimental significance or instrument sensitivity. No fitting or full Jacobian rank claim.')
 (R/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
