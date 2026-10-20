import verify_inputs
from pathlib import Path
import subprocess,sys,os,json,time
import numpy as np
P=Path(__file__).resolve().parent;start=time.time()
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
done=[]
for kind in ['D','A']:
    for offset in range(8):
        dest=P/'results'/f'{kind}_64_a2.5_s16_o{offset}_k50000.npz'
        expected=set(range(2,101))
        for lo in range(101+2*offset,6001,16):
            expected.add(lo)
            if lo+1<=6000:expected.add(lo+1)
        expected.update([5999,6000])
        valid=dest.exists() and set(np.load(dest)['ell'])==expected
        if not valid:
            with (P/f'run_{kind}_{offset}.log').open('w') as log:
                subprocess.run([sys.executable,str(P/'run_transfers.py'),'2.5',kind,'50000','16',str(offset)],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
        done.append([kind,offset]);(P/'progress.json').write_text(json.dumps({'done':done,'seconds':time.time()-start}))
        print(kind,offset,'complete',round(time.time()-start,1),flush=True)
print('ALL COMPLETE',flush=True)
