"""Replay recovered originals in temporary directories; stdlib only. No source edits."""
from pathlib import Path
import tempfile,zipfile,subprocess,sys,json,hashlib
BASE=Path(__file__).resolve().parent

def main():
 manifest=json.loads((BASE/'SHA256SUMS.json').read_text())
 for name,digest in manifest.items():
  if hashlib.sha256((BASE/name).read_bytes()).hexdigest()!=digest:
   raise ValueError('ARCHIVE_OR_RECORD_HASH_MISMATCH: '+name)
 rows=[]; internal=0
 with tempfile.TemporaryDirectory() as temp:
  for archive in sorted((BASE/'evidence').rglob('*.zip')):
   dest=Path(temp)/archive.stem
   with zipfile.ZipFile(archive) as z:
    for n in z.namelist():
     if not (dest/n).resolve().is_relative_to(dest.resolve()):raise ValueError('UNSAFE_ZIP_PATH')
    z.extractall(dest)
   for sums in [*dest.rglob('SHA256SUMS'),*dest.rglob('SHA256SUMS.txt')]:
    for line in sums.read_text().splitlines():
     digest,name=line.split(maxsplit=1); name=name.lstrip('*')
     assert hashlib.sha256((sums.parent/name).read_bytes()).hexdigest()==digest, name
     internal+=1
   programs=list(dest.rglob('*.py'));assert len(programs)==1
   p=programs[0];certs={f.name:json.loads(f.read_text()) for f in p.parent.glob('*CERTIFICATE.json')}
   done=subprocess.run([sys.executable,p.name],cwd=p.parent,capture_output=True,text=True)
   assert done.returncode==0,done.stderr
   actual=json.loads(done.stdout);expected=json.loads((BASE/'runs_2026_10_22'/f'{p.stem}.stdout.json').read_text())
   assert actual==expected,'OUTPUT_MISMATCH: '+p.name
   for name,old in certs.items():assert json.loads((p.parent/name).read_text())==old,'CERTIFICATE_MISMATCH: '+name
   rows.append({'script':p.name,'exit_code':done.returncode,'stdout_matches_recovery_run':True,'certificates_match_original':True})
 print(json.dumps({'programs':rows,'original_internal_hashes_verified':internal,'scope':'Finite source replay only; actual all-order xi positivity and RH OPEN'},indent=2))
if __name__=='__main__':
 try: main()
 except Exception as e:print(type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
