#!/usr/bin/env python3
"""Build a review archive with source/data/docs and an internal SHA256 manifest."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib
ROOT=Path(__file__).resolve().parent
NAME='WRRA_M_Upstream_0_4_to_0_6_Reviewed_Collection_r1_Reproducibility_2026_10_03.zip'
def files():
 return sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(x in p.parts for x in ('qa','__pycache__','archive')) and p.suffix not in ('.pyc','.log','.zip') and p.name not in ('SHA256SUMS','PUBLIC_FILES_SHA256SUMS','equations.docx'))
def main():
 entries=files()
 manifest=ROOT/'SHA256SUMS'
 manifest.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in entries))
 archive=ROOT.parent/NAME
 with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=9) as z:
  for p in entries+[manifest]:z.write(p,p.relative_to(ROOT).as_posix())
 print(str(archive));print(f'{len(entries)+1} archived files; {archive.stat().st_size} bytes')
if __name__=='__main__':main()
