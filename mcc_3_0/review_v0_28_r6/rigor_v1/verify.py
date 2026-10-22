"""Independent reader: no import of generator/core; ignore its hash and PASS claims."""
from pathlib import Path
from fractions import Fraction
import json,sys,math
import numpy as np
import mpmath as mp

def req(ok,msg):
 if not ok:raise ValueError(msg)

def main(P):
 cfg=json.loads((P/'inputs.json').read_text());s=json.loads((P/'summary.json').read_text());w=json.loads((P/'spectrum.json').read_text())
 ff=[Fraction(v) for v in cfg['shares']];req(sum(ff)==1 and min(ff)>=0,'INVALID_SHARES');L=math.lcm(*(f.denominator for f in ff));H=max(cfg['harmonics'])
 with mp.workdps(80):
  T=2*mp.pi*H;C=int(mp.nzeros(T));last=mp.im(mp.zetazero(C)) if C else None
  if last==T:C-=1
  req(C==w['C'] and abs(mp.mpf(w['T'])-T)<mp.mpf('1e-45'),'SPECTRUM_MISMATCH')
  for key,k in [('gamma_last',C),('gamma_next',C+1)]:
   if k:req(abs(mp.mpf(w[key])-mp.im(mp.zetazero(k)))<mp.mpf('1e-45'),'ZERO_HEIGHT_MISMATCH')
 N=L*H*C;req((L,H,C,N)==tuple(s[k] for k in ['L','H','C','N']),'FACTOR_TOTAL_MISMATCH')
 with np.load(P/'ledger.npz',allow_pickle=False) as f:a={k:f[k] for k in f.files}
 req(set(a)=={'n','ell','h','z','kind','weight'},'LEDGER_SCHEMA')
 for k in a:req(a[k].shape==(N,),'ROW_COUNT_'+k)
 for k in ['n','ell','h','z','kind']:req(np.issubdtype(a[k].dtype,np.integer),'INTEGER_TYPE_'+k)
 n=np.arange(1,N+1);req(np.array_equal(a['n'],n),'ADDRESS_COVERAGE_OR_DUPLICATE')
 req(np.all((a['ell']>=0)&(a['ell']<L)&(a['h']>=0)&(a['h']<H)&(a['z']>=1)&(a['z']<=C)),'COORDINATE_DOMAIN')
 req(np.array_equal(1+a['ell']+L*(a['h']+H*(a['z']-1)),n),'SERIALIZATION_MISMATCH')
 # Boolean Eratosthenes, independent of generator's smallest-prime-factor classification.
 prime=np.ones(N+1,dtype=bool);prime[:2]=False
 for p in range(2,math.isqrt(N)+1):
  if prime[p]:prime[p*p:N+1:p]=False
 expected=np.where(prime[1:],1,np.where(n%2==0,2,3)).astype('uint8');expected[0]=0
 req(np.array_equal(a['kind'],expected),'FILTER_CLASS_MISMATCH')
 v=n[1:].astype(float)**(-cfg['alpha']);v/=math.fsum(v.tolist());ew=np.r_[0.,v]
 req(np.isfinite(a['weight']).all() and np.all(a['weight']>=0),'INVALID_WEIGHTS')
 req(np.allclose(a['weight'],ew,rtol=2e-13,atol=0),'WEIGHT_LAW_MISMATCH')
 req(abs(math.fsum(a['weight'].tolist())-1)<1e-13,'NORMALIZATION')
 counts={str(k):int((expected==k).sum()) for k in range(4)};req(counts==s['counts'] and s['active']==N-1,'COUNT_SUMMARY_MISMATCH')
 req(abs(s['weight_sum']-math.fsum(a['weight'].tolist()))<1e-13,'WEIGHT_SUMMARY_MISMATCH')
 print(json.dumps({'status':'PASS','rows_verified':N,'counts':counts,'spectrum_precision':80,'independent_filter':'Boolean Eratosthenes','all_address_coordinates_checked':True}))
if __name__=='__main__':
 try:main(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'results')
 except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
