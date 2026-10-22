"""Matched conditional SPARC comparison. Run from any cwd; no network needed."""
from pathlib import Path
import csv, json, hashlib, importlib.util, sys, platform
import numpy as np
import scipy
from scipy.optimize import least_squares, minimize_scalar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('wrra',P/'wrra_original/compute.py');w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)
KPC=1000*w.PC
# Recompute scale from the original shared load, not from the target rotation data.
state=next(x for x in json.loads((P/'wrra_original/inputs/shared_gravity_results.json').read_text())['cases'] if x['carrier_state']=='product' and x['epsilon']==0 and x['a']==1)
H0=67.4*1000/(1e6*w.PC);ucrit=3*H0**2*w.C**2/(8*np.pi*w.G)
AT=w.C*H0*np.sqrt(state['sector_density_J_m3'][1]/ucrit/8)

def load():
 meta={}
 for line in (P/'inputs/SPARC_Lelli2016c.mrt').read_text().splitlines():
  try:
   a=line.split();name=a[0];d=float(a[2]);inc=float(a[5]);q=int(a[17]);meta[name]=(d,inc,q)
  except (ValueError,IndexError):continue
 raw={}
 for line in (P/'inputs/MassModels_Lelli2016c.mrt').read_text().splitlines():
  a=line.split()
  if a and a[0] in meta:
   raw.setdefault(a[0],[]).append([float(x) for x in a[1:]])
 data={};selection=[]
 for name,a in sorted(raw.items()):
  a=np.array(a);d,inc,q=meta[name];r,v,e,gas,disk,bul=a[:,1:7].T
  vb2=gas*np.abs(gas)+.5*disk*np.abs(disk)+.7*bul*np.abs(bul)
  good=(r>0)&(v>0)&(e>0)&(vb2>0)&np.isfinite(a).all(1)
  reason='included' if q<=2 and inc>=30 and good.sum()>=5 else ('Q>2' if q>2 else 'inclination<30' if inc<30 else 'fewer_than_5_valid_points')
  selection.append(dict(galaxy=name,Q=q,inclination=inc,distance_Mpc=d,raw_points=len(a),valid_points=int(good.sum()),reason=reason))
  if reason=='included':data[name]=dict(r=r[good],v=v[good],e=e[good],gas=gas[good]*np.abs(gas[good]),stars=.5*disk[good]*np.abs(disk[good])+.7*bul[good]*np.abs(bul[good]))
 return data,selection

def wrra(d,aT=AT,scale=1.):
 vb2=d['gas']+scale*d['stars'];gb=vb2*1e6/(d['r']*KPC)
 # Directly call the published WRRA quadratic-exposure/admission response.
 return np.sqrt(aT*w.response(gb/aT)*d['r']*KPC/1e6)

def nfw_v2(r,v200,c):
 r200=v200/(10*.0674);x=r/r200;f=lambda z:np.log1p(z)-z/(1+z)
 return v200*v200*f(c*x)/(x*f(c))

def nfw(d,pars,free_stars=False):
 v200,c=10**np.array(pars[:2]);s=10**pars[2] if free_stars else 1.
 return np.sqrt(np.maximum(d['gas']+s*d['stars']+nfw_v2(d['r'],v200,c),1e-12))

def star_lower(d):
 return max(.1,float(np.max(np.divide(-d['gas'],d['stars'],out=np.zeros_like(d['gas']),where=d['stars']>0)))+1e-8)

def halo_fit(d,free=False):
 lo=np.log10([5,.1]+([star_lower(d)] if free else []));hi=np.log10([1000,100]+([5] if free else []))
 fits=[]
 for v in [30,100,300]:
  for c in [1,10,50]:
   x=np.log10([v,c]+([1.] if free else []))
   fits.append(least_squares(lambda p:(nfw(d,p,free)-d['v'])/d['e'],x,bounds=(lo,hi),ftol=1e-10,xtol=1e-10,gtol=1e-10,max_nfev=1500))
 best=min(fits,key=lambda f:np.dot(f.fun,f.fun));return best,bool(np.any(np.minimum(best.x-lo,hi-best.x)<1e-4))

def writecsv(path,rows):
 with path.open('w',newline='') as f:
  wri=csv.DictWriter(f,fieldnames=rows[0]);wri.writeheader();wri.writerows(rows)

def main():
 out=P/'results';out.mkdir(exist_ok=True);data,selection=load();writecsv(out/'selection.csv',selection)
 assert len(selection)==175
 # One shared acceleration calibration; explicitly uses these same observations.
 def objective(z):return sum(np.sum(((wrra(d,10**z)-d['v'])/d['e'])**2) for d in data.values())
 grid=np.linspace(-12,-8,161);z=grid[np.argmin([objective(z) for z in grid])]
 opt=minimize_scalar(objective,bounds=(max(-12,z-.05),min(-8,z+.05)),method='bounded',options={'xatol':1e-12});fitAT=10**opt.x
 rows=[];points=[]
 for name,d in data.items():
  n=len(d['r']);f,bound=halo_fit(d);f3,bound3=halo_fit(d,True)
  def obj(s):return np.sum(((wrra(d,scale=10**s)-d['v'])/d['e'])**2)
  sfit=minimize_scalar(obj,bounds=(np.log10(star_lower(d)),np.log10(5)),method='bounded',options={'xatol':1e-10});scale=10**sfit.x
  models={'WRRA_fixed':(wrra(d),0),'WRRA_global_aT':(wrra(d,fitAT),0),'NFW_fixed_stars':(nfw(d,f.x),2),'WRRA_free_stars':(wrra(d,scale=scale),1),'NFW_free_stars':(nfw(d,f3.x,True),3)}
  for model,(pred,k) in models.items():
   chi=float(np.sum(((pred-d['v'])/d['e'])**2))
   rows.append(dict(galaxy=name,model=model,n=n,k_local=k,chi2=chi,chi2_over_local_dof=chi/(n-k),stellar_scale=scale if model=='WRRA_free_stars' else 10**f3.x[2] if model=='NFW_free_stars' else 1.,v200_km_s=10**f.x[0] if model=='NFW_fixed_stars' else 10**f3.x[0] if model=='NFW_free_stars' else '',concentration=10**f.x[1] if model=='NFW_fixed_stars' else 10**f3.x[1] if model=='NFW_free_stars' else '',fit_success=bool(f.success) if model=='NFW_fixed_stars' else bool(f3.success) if model=='NFW_free_stars' else bool(sfit.success) if model=='WRRA_free_stars' else True,boundary=bound if model=='NFW_fixed_stars' else bound3 if model=='NFW_free_stars' else bool(min(scale-star_lower(d),5-scale)<.001) if model=='WRRA_free_stars' else False))
   for j in range(n):points.append(dict(galaxy=name,point=j,model=model,r_kpc=d['r'][j],observed_km_s=d['v'][j],error_km_s=d['e'][j],predicted_km_s=pred[j],gas_v2=d['gas'][j],stellar_v2_at_unit_scale=d['stars'][j],residual_sigma=(pred[j]-d['v'][j])/d['e'][j]))
 writecsv(out/'galaxy_fits.csv',rows);writecsv(out/'point_predictions.csv',points)
 summary=[]
 for model in models:
  rr=[r for r in rows if r['model']==model];N=sum(r['n'] for r in rr);k=sum(r['k_local'] for r in rr)+(model=='WRRA_global_aT');chi=sum(r['chi2'] for r in rr)
  summary.append(dict(model=model,galaxies=len(rr),N=N,k=int(k),chi2=chi,dof=int(N-k),chi2_per_dof=chi/(N-k),AIC_conditional=chi+2*k,BIC_conditional=chi+k*np.log(N),median_galaxy_chi2_per_local_dof=float(np.median([r['chi2_over_local_dof'] for r in rr])),fit_failures=sum(not r['fit_success'] for r in rr),boundary_fits=sum(r['boundary'] for r in rr)))
 writecsv(out/'comparison.csv',summary)
 result=dict(aT_native=float(AT),aT_calibrated=float(fitAT),global_fit_success=bool(opt.success),summary=summary,selection=dict(total_galaxies=len(selection),included=len(data),excluded=len(selection)-len(data)),versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),source_commit='8358c887d09de385ca7d6487e1ffcffa0557a91c',scope='Conditional diagonal-error disk-plane algebraic WRRA response versus uncontracted free NFW; not a full 3D WRRA PDE or full cosmological LCDM likelihood; fixed catalog distance/inclination; no intrinsic-scatter or systematic-error inflation.')
 (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
 fig,ax=plt.subplots(figsize=(8,5))
 for model in models:
  a=np.sort([r['chi2_over_local_dof'] for r in rows if r['model']==model]);ax.plot(a,np.arange(1,len(a)+1)/len(a),label=model)
 ax.set(xscale='log',xlabel='Conditional galaxy chi-square / local degrees of freedom',ylabel='Fraction of included galaxies',title='SPARC: matched conditional fits');ax.legend(fontsize=8);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(out/'chi2_distribution.png',dpi=180);plt.close(fig)
 ranked=sorted([r for r in rows if r['model']=='WRRA_fixed'],key=lambda r:(r['chi2_over_local_dof'],r['galaxy']))
 chosen=[ranked[int(q*(len(ranked)-1))]['galaxy'] for q in [0,.2,.4,.6,.8,1]]
 fig,axs=plt.subplots(2,3,figsize=(12,7))
 for name,ax in zip(chosen,axs.flat):
  d=data[name];ax.errorbar(d['r'],d['v'],d['e'],fmt='.',color='black',label='observed')
  for m in ['WRRA_fixed','WRRA_global_aT','NFW_fixed_stars']:
   pp=[x for x in points if x['galaxy']==name and x['model']==m];ax.plot([x['r_kpc'] for x in pp],[x['predicted_km_s'] for x in pp],label=m)
  ax.set(title=name,xlabel='R (kpc)',ylabel='V (km/s)')
 axs[0,0].legend(fontsize=7);fig.suptitle('Predefined rank quantiles (0,20,40,60,80,100%) of fixed-WRRA chi-square');fig.tight_layout();fig.savefig(out/'rotation_examples.png',dpi=170);plt.close(fig)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
