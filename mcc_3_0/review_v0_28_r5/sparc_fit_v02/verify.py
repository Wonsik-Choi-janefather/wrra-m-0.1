"""Read saved records and independently reconstruct gate, halo and scores."""
from pathlib import Path
import csv,json,math,sys,hashlib
import numpy as np
from scipy.linalg import expm
P=Path(__file__).resolve().parent;D=Path(sys.argv[1]) if len(sys.argv)>1 else P/'results'
def req(ok,msg):
 if not ok:raise AssertionError(msg)
def read(n):return list(csv.DictReader((D/n).open()))
def close(a,b):return math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7)
summary=json.loads((D/'summary.json').read_text());req(summary['protocol_sha256']==hashlib.sha256((P/'PROTOCOL.json').read_bytes()).hexdigest(),'PROTOCOL_CHANGED')
fits=read('fits.csv');points=read('predictions.csv');groups={};seen=set()
for r in points:
 key=(r['galaxy'],r['phase'],r['model']);uid=key+(r['point'],);req(uid not in seen,'DUPLICATE_ROW');seen.add(uid);groups.setdefault(key,[]).append(r)
for f in fits:
 key=(f['galaxy'],f['phase'],f['model']);pp=groups[key];pars=json.loads(f['params']);n=0;chi=0;nt=0;tc=0;model=f['model']
 for r in pp:
  radius=float(r['r_kpc']);gas=float(r['gas_v2']);stars=float(r['stars_v2']);p=float(r['pred']);v=float(r['vobs']);e=float(r['error']);req(e>0 and math.isfinite(p),'INVALID_VALUE')
  if model=='NFW_ML':
   vv,c,s=10**np.array(pars);x=radius*.674/vv;v2=vv*vv*(math.log1p(c*x)-c*x/(1+c*x))/(x*(math.log1p(c)-c/(1+c)));expected=math.sqrt(gas+s*stars+v2)
  else:
   if model=='WRRA_native_ML':A,power,s=1.,0.,10**pars[0]
   elif model=='WRRA_amplitude_ML':A,power,s=10**pars[0],0.,10**pars[1]
   else:A,power,s=10**pars[0],pars[1],10**pars[2]
   gb=(gas+s*stars)*1e6/(radius*3.085677581491367e19);at=summary['aT_native']*A*(radius/float(f['pivot_kpc']))**power;req(gb>0 and at>0,'INVALID_ACCELERATION')
   mu=expm(np.array([[-1.,0.],[1.,0.]])*math.sqrt(gb/at))[1,0];expected=math.sqrt(gb/mu*radius*3.085677581491367e19)/1000
  req(close(expected,p),'PREDICTION_REPLAY_MISMATCH')
  is_test=r['test']=='True';req(is_test==(f['phase']=='train' and int(r['point'])%5==4),'SPLIT_MISMATCH')
  z=((p-v)/e)**2
  if is_test:nt+=1;tc+=z
  else:n+=1;chi+=z
 req(n==int(f['n_fit']) and nt==int(f['n_test']),'ROW_COUNT')
 req(close(chi,float(f['chi2'])),'CHI2_MISMATCH');req(close(chi+2*int(f['k']),float(f['AIC'])),'AIC_MISMATCH');req(close(chi+int(f['k'])*math.log(n),float(f['BIC'])),'BIC_MISMATCH')
 if nt:req(close(tc,float(f['test_chi2'])),'TEST_CHI2_MISMATCH')
 req(f['success']=='True','OPTIMIZATION_FAILURE')
for s in summary['summary']:
 ff=[f for f in fits if f['model']==s['model'] and f['phase']==s['phase'] and (s['sample']=='all' or f['clean']=='True')]
 for out,col in [('chi2','chi2'),('AIC','AIC'),('BIC_block','BIC'),('N','n_fit'),('k','k'),('test_N','n_test')]:req(close(sum(float(f[col]) for f in ff),s[out]),'SUMMARY_'+out)
for s in summary['summary']:
 ff=[f for f in fits if f['model']==s['model'] and f['phase']==s['phase'] and (s['sample']=='all' or f['clean']=='True')]
 if s['phase']=='train':
  tc=sum(float(f['test_chi2']) for f in ff);req(close(tc,s['test_chi2']),'SUMMARY_HELDOUT');req(close(tc/s['test_N'],s['test_chi2_per_point']),'SUMMARY_HELDOUT_MEAN')
for key,pp in groups.items():
 reference=groups[(key[0],key[1],'WRRA_native_ML')]
 req([(r['point'],r['r_kpc'],r['vobs'],r['error']) for r in pp]==[(r['point'],r['r_kpc'],r['vobs'],r['error']) for r in reference],'MATCHED_OBSERVATIONS')
clean=[]
for m in read('sample_metadata.csv'):
 n=len(groups[(m['galaxy'],'full','WRRA_native_ML')]);selected=int(m['Q'])==1 and 40<=float(m['inc'])<=80 and float(m['eD'])/float(m['D'])<=.1 and float(m['einc'])<=5 and n>=10
 req(selected==(m['clean']=='True'),'CLEAN_CRITERION')
 if selected:clean.append(m['galaxy'])
req(sorted(clean)==summary['clean_galaxies'],'CLEAN_LIST')
req(len(summary['clean_galaxies'])>0,'EMPTY_CLEAN_SAMPLE')
print(json.dumps({'status':'PASS','prediction_rows':len(points),'fit_rows':len(fits),'summary_rows':len(summary['summary']),'independent_gate':'matrix exponential','independent_NFW':True,'split_and_AIC_BIC':True}))
