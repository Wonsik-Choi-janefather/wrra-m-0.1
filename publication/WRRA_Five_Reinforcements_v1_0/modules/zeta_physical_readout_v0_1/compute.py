"""WRRA: finite zeta phase instrument -> calibrated massless carrier readout.
The zero heights are not spatial energy eigenvalues or physical clock rates.
"""
from pathlib import Path
import numpy as np,json,math,hashlib,csv
P=Path(__file__).resolve().parent
N=1015000;SHAPE=(213,65,77);M=math.prod(SHAPE);C=70
ALPHA=1.8996877935161325;HBAR=1.054571817e-34
LIGHT=299792458.;TAU=1.481301966415863e-21;D=LIGHT*TAU
EV=1.602176634e-19;SCALE=HBAR/TAU;CHECKS={}
def check(name,value):
 CHECKS[name]=bool(value)
 if not value:raise AssertionError(name)
def selected():
 prime=np.ones(N+1,bool);prime[:2]=False
 for p in range(2,math.isqrt(N)+1):
  if prime[p]:prime[p*p::p]=False
 omega=np.zeros(N+1,np.int8)
 for p in np.flatnonzero(prime):omega[p::p]+=1
 return np.flatnonzero(omega>=2)
def main():
 for name,meta in json.loads((P/'input_manifest.json').read_text()).items():
  check('hash_'+name,hashlib.sha256((P/'inputs'/name).read_bytes()).hexdigest()==meta['sha256'])
 ids=selected();idx=np.ravel_multi_index(tuple(ids%m for m in SHAPE),SHAPE);logn=np.log(ids)
 gamma=np.loadtxt(P/'inputs/zero_heights.csv',skiprows=1)
 check('selected_count',len(ids)==935155);check('injective_CRT',len(np.unique(idx))==len(ids))
 axes=[]
 for i,m in enumerate(SHAPE):
  shape=[1]*3;shape[i]=m;axes.append((2*np.pi*np.fft.fftfreq(m)).reshape(shape))
 rad=np.sqrt(sum(a*a for a in axes));band=rad<=.8*np.pi
 evolution=np.exp(-1j*rad) # physical time TAU; H TAU/hbar = |k|d
 def embed(v):
  a=np.zeros(M,complex);a[idx]=v;return a.reshape(SHAPE)
 def fft(v):return np.fft.fftn(embed(v),norm='ortho')
 def energy(f):return float(np.sum(rad*abs(f)**2))
 def profile(f):
  state=np.fft.ifftn(f*band*evolution,norm='ortho');pr=abs(state)**2;prob=float(pr.sum())
  return pr/prob,prob
 old=json.loads((P/'inputs/original_phase_results.json').read_text())
 rows=[];summaries={};distributions={};bins=np.linspace(0,float(rad.max()),101)
 for prep,alpha in [('uniform',0.),('inherited_alpha',ALPHA)]:
  seed=ids.astype(float)**(-alpha/2);seed/=np.linalg.norm(seed)
  initial=fft(seed);ein=energy(initial)
  # Full selected-address Gram matrix, block accumulation; no sampled surrogate.
  gram=np.zeros((C,C),complex)
  for start in range(0,len(ids),8192):
   sl=slice(start,start+8192);v=np.exp(-1j*gamma[:,None]*logn[sl])*seed[sl]
   gram+=v.conj()@v.T
  vals,vec=np.linalg.eigh(gram);b=vec[:,-1]
  b*=np.exp(-1j*np.angle(np.sum(b)))
  check(prep+'_gram_trace',abs(np.trace(gram).real-C)<2e-12)
  check(prep+'_gram_psd',vals[0]>-1e-12)
  check(prep+'_combiner_upper_bound',vals[-1]<=C+1e-10)
  np.savez_compressed(P/(prep+'_combiner.npz'),gram=gram,coefficients=b,eigenvalues=vals)
  summary={'input_energy_dimensionless':ein,'input_energy_J':ein*SCALE,
    'optimal_pass_probability':float(vals[-1]/C),'gram_min_eigenvalue':float(vals[0])}
  for case,heights in [('zeta',gamma),('equally_spaced_forced_open',np.linspace(gamma[0],gamma[-1],C)),('shifted_0.5_forced_open',gamma+.5)]:
   print(prep,case,flush=True)
   filt=np.zeros(len(ids),complex);fopt=np.zeros(len(ids),complex)
   mean_energy=0.;mean_band_prob=0.;mixture_spectrum=np.zeros(len(bins)-1)
   for j,g in enumerate(heights):
    phase=np.exp(-1j*g*logn);filt+=phase/C
    if case=='zeta':fopt+=b[j]*phase/np.sqrt(C)
    f=fft(seed*phase);w=abs(f)**2
    mean_energy+=energy(f)/C;mean_band_prob+=float(w[band].sum())/C
    mixture_spectrum+=np.histogram(rad,bins,weights=w)[0]/C
   out=fft(seed*filt);pw=abs(out)**2;prob=float(pw.sum());eout=energy(out)
   holdprob=1-prob;ehold=mean_energy-eout;work=mean_energy-ein
   prof,pband=profile(out);eband=float(np.sum(rad[band]*pw[band]))
   ehigh=eout-eband;phigh=prob-pband
   check(prep+'_'+case+'_probability',abs(pband+phigh+holdprob-1)<2e-14)
   check(prep+'_'+case+'_energy',abs((eband+ehigh+ehold)-(ein+work))<2e-14)
   check(prep+'_'+case+'_positive_remainders',min(ehold,ehigh,phigh,holdprob)>-1e-12)
   check(prep+'_'+case+'_unitary_transport_energy',abs(energy(out*evolution)-eout)<2e-14)
   # H and |p| commute with transport; each spectral component is massless.
   shellerr=float(np.max(abs((rad*SCALE)**2-LIGHT**2*(rad*HBAR/D)**2)))/(SCALE**2)
   check(prep+'_'+case+'_massless_dispersion',shellerr<2e-14)
   row={'preparation':prep,'case':case,'pass_probability':prob,'band_detect_probability':pband,
    'high_frequency_probability':phigh,'hold_probability':holdprob,'input_mean_keV':ein*SCALE/EV/1e3,
    'all_ports_mean_keV':mean_energy*SCALE/EV/1e3,'phase_work_mean_keV':work*SCALE/EV/1e3,
    'pass_energy_weighted_keV':eout*SCALE/EV/1e3,'hold_energy_weighted_keV':ehold*SCALE/EV/1e3,
    'pass_conditional_mean_keV':eout/prob*SCALE/EV/1e3,
    'band_conditional_mean_keV':eband/pband*SCALE/EV/1e3,
    'all_ports_band_probability':mean_band_prob}
   if case=='zeta':
    baseline=old['rows'][prep]['coherent_success_probability']
    check(prep+'_old_pass_replayed',abs(prob-baseline)<2e-14)
    check(prep+'_gram_uniform_pass',abs(np.sum(gram).real/C**2-prob)<2e-14)
    opt=fft(seed*fopt);popt=float(np.sum(abs(opt)**2));optprofile,optband=profile(opt)
    check(prep+'_optimal_combiner',abs(popt-vals[-1]/C)<2e-14)
    summary.update({'uniform_pass_probability':prob,'optimal_to_uniform_ratio':popt/prob,
     'optimal_band_probability':optband,'optimal_conditional_energy_keV':energy(opt)/popt*SCALE/EV/1e3})
    distributions[prep]=prof
    np.savetxt(P/(prep+'_spectrum.csv'),np.column_stack(((bins[:-1]+bins[1:])/2*SCALE/EV/1e3,np.histogram(rad,bins,weights=pw)[0]/prob,mixture_spectrum)),delimiter=',',header='energy_keV,pass_conditional_probability,all_port_probability',comments='')
   else:row['band_spatial_TV_from_zeta']=float(.5*np.sum(abs(prof-distributions[prep])))
   rows.append(row)
   for a in range(3):
    marginal=prof.sum(axis=tuple(x for x in range(3) if x!=a))
    np.savetxt(P/(prep+'_'+case+'_axis'+str(a)+'.csv'),np.column_stack((np.arange(SHAPE[a])*D,marginal)),delimiter=',',header='coordinate_m,conditional_band_probability',comments='')
  summaries[prep]=summary
 with (P/'physical_readout.csv').open('w',newline='') as f:
  keys=list(dict.fromkeys(k for r in rows for k in r));w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
 result={'architecture':'Wonsik Reality-Renderer Architecture','version':'zeta physical readout v0.1',
  'constants':{'N':N,'C':C,'shape':SHAPE,'capacity':M,'selected':len(ids),'hbar_J_s':HBAR,'c_m_s':LIGHT,'shutter_s':TAU,'edge_m':D,'energy_unit_keV':SCALE/EV/1e3,'band_kd_max':.8*np.pi},
  'rows':rows,'combiner':summaries,'checks':CHECKS,'all_checks_pass':all(CHECKS.values()),
  'scope':'Finite calibrated massless single-excitation reference instrument. All-port energy and mean phase-control work included. No particle masses, SM quantum numbers, RH, unique zeta optimality or autonomous apparatus derived.'}
 (P/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps({'checks':len(CHECKS),'combiner':summaries},indent=2),flush=True)
if __name__=='__main__':main()
