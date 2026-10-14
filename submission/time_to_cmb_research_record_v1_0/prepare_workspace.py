"""Restore exact stage files from the shared object store. No network needed."""
from pathlib import Path
import json,hashlib,argparse,shutil
ROOT=Path(__file__).resolve().parent
def main():
 p=argparse.ArgumentParser();p.add_argument('--stage');p.add_argument('--verify-only',action='store_true');a=p.parse_args()
 m=json.loads((ROOT/'release_manifest.json').read_text());count=0
 for row in m['files']:
  if a.stage and not row['path'].startswith('stages/'+a.stage+'/'):continue
  src=ROOT/row['stored_path'];data=src.read_bytes()
  if hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('Asset hash mismatch: '+str(src))
  if not a.verify_only:
   dst=ROOT/row['path'];dst.parent.mkdir(parents=True,exist_ok=True)
   if dst!=src:shutil.copyfile(src,dst)
  count+=1
 if not count:raise ValueError('No files selected')
 print('Verified '+str(count)+' frozen stage files'+('' if a.verify_only else '; restored original stage paths'))
if __name__=='__main__':main()
