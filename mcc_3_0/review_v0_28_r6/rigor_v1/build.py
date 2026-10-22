from pathlib import Path
import json,sys,hashlib
import numpy as np
from core import resolution,window,ledger
P=Path(__file__).resolve().parent;O=P/'results';O.mkdir(exist_ok=True)
inputs={'shares':['0.05','0.268','0.682'],'harmonics':[0,5,29],'alpha':1.8996876950554356,'address_one':'inactive reference','kind_codes':{'0':'reference','1':'prime','2':'even composite','3':'odd composite'}}
L,nums=resolution(inputs['shares']);H=max(inputs['harmonics']);w=window(H);C=w['C'];a=ledger(L,H,C,inputs['alpha']);np.savez_compressed(O/'ledger.npz',**a)
summary={'L':L,'H':H,'C':C,'N':len(a['n']),'active':int((a['kind']!=0).sum()),'counts':{str(k):int((a['kind']==k).sum()) for k in range(4)},'weight_sum':float(a['weight'].sum()),'ledger_sha256':hashlib.sha256((O/'ledger.npz').read_bytes()).hexdigest()}
for n,v in [('inputs.json',inputs),('spectrum.json',w),('summary.json',summary)]: (O/n).write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps(summary,indent=2))
