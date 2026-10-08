from pathlib import Path
import numpy as np,json
from scipy.special import expit
R=Path(__file__).resolve().parent
source=json.loads((R/'review_r9/phase_control_comparison_results.json').read_text())
a=source['inputs']['alpha'];N=source['inputs']['N'];K=source['inputs']['K']
n=np.arange(2,N+1,dtype=float);w9=9.**(-a)/np.sum(n**(-a));rows=[];checks=[]
for c in source['outputs']:
 freqs=c['frequencies'];h=c['refitted_threshold']
 delta=np.zeros(K) if freqs is None else np.cos(np.asarray(freqs)[:,None]*(np.log(9)+c['xi']*np.arange(K)))/np.sqrt(len(freqs))
 if freqs is not None:delta=delta.sum(axis=0)
 t=1-np.prod(1-expit(delta-h))
 f=np.array([.05,.268,.682]);fine_at9=w9*np.array([t,0,1-t]);F=(f+fine_at9)/(1+w9)
 checks.extend([{'name':c['case']+' admission reproduced','passed':bool(abs(t-c['address_9_admission'])<1e-12)},{'name':c['case']+' energy fractions positive and normalized','passed':bool(np.all(F>=0) and abs(F.sum()-1)<1e-12)}])
 rows.append({'drive':c['case'],'T9':float(t),'energy_fractions':F.tolist()})
checks += [{'name':'address-sensitive readout distinguishes all four controls','passed':len(set(round(r['energy_fractions'][0],10) for r in rows))==4}]
out={'scope':'Declared address-sensitive load before aggregation; no measured carrier energy assigned','w9':float(w9),'rows':rows,'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks)}
(R/'address_readout_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));assert all(x['passed'] for x in checks)
