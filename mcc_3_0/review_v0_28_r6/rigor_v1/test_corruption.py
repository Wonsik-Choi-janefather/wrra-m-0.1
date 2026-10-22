from pathlib import Path
import json,shutil,tempfile,subprocess,sys
import numpy as np
P=Path(__file__).parent;records=[]
cases=['delete_row','duplicate_replace','unknown_address','swap_coordinates','swap_filter_preserve_counts','vacuum_marked_prime','change_weight_preserve_sum','alter_zero_height','alter_reported_count']
for case in cases:
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)/'data';shutil.copytree(P/'results',d)
  with np.load(d/'ledger.npz') as f:a={k:f[k] for k in f.files}
  if case=='delete_row':a={k:v[:-1] for k,v in a.items()}
  if case=='duplicate_replace':
   for k in a:a[k][-1]=a[k][-2]
  if case=='unknown_address':a['n'][-1]+=1
  if case=='swap_coordinates':a['ell'][10],a['ell'][11]=a['ell'][11],a['ell'][10]
  if case=='swap_filter_preserve_counts':a['kind'][1],a['kind'][3]=a['kind'][3],a['kind'][1]
  if case=='vacuum_marked_prime':a['kind'][0]=1
  if case=='change_weight_preserve_sum':a['weight'][1],a['weight'][2]=a['weight'][2],a['weight'][1]
  if case=='alter_zero_height':
   s=json.loads((d/'spectrum.json').read_text());s['gamma_last']='182.0';(d/'spectrum.json').write_text(json.dumps(s))
  if case=='alter_reported_count':
   s=json.loads((d/'summary.json').read_text());s['counts']['1']+=1;(d/'summary.json').write_text(json.dumps(s))
  np.savez_compressed(d/'ledger.npz',**a)
  p=subprocess.run([sys.executable,str(P/'verify.py'),str(d)],capture_output=True,text=True)
  assert p.returncode!=0 and 'FAIL:' in p.stderr,(case,p.stdout,p.stderr)
  record={'case':case,'exit':p.returncode,'error':p.stderr.strip(),'summary_unchanged':(d/'summary.json').read_bytes()==(P/'results/summary.json').read_bytes()};records.append(record);print(json.dumps(record),flush=True)
(P/'results/corruption_tests.json').write_text(json.dumps({'detected':len(records),'cases':records},indent=2))
