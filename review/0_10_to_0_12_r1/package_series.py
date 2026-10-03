"""Preserve the 0.9-r1 history and add reviewed 0.10--0.12 with clean replay."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile,zipfile
REPO=Path(__file__).resolve().parents[2]
BASELINE_SHA='72beff499bf7ee53d767d887b963be9f7b4c1b7a18c1c0e5702c295f602dd579'
META={'document_checks.json','reproduction_checks.json','runtime_environment.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def eligible(p):return p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'
def main():
 baseline=REPO/'paper/WRRA_M_0_9_r1_Series_Release.zip';assert sha(baseline)==BASELINE_SHA
 with tempfile.TemporaryDirectory(prefix='wrra12-reviewed-series-') as tmp:
  stage=Path(tmp)
  with zipfile.ZipFile(baseline) as z:
   assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
   for line in z.read('SHA256SUMS').decode().splitlines():
    h,n=line.split('  ',1);assert hashlib.sha256(z.read(n)).hexdigest()==h
   z.extractall(stage)
  historical={p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*') if eligible(p) and p.relative_to(stage).parts[0] in ('calculations','paper')}
  for name in ('README.md','README_EN.md','README_KO.md','CITATION.cff','.zenodo.json'):
   source=stage/name;dest=stage/'review/0_9_r1_original_metadata'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
  files=[]
  for v in (10,11,12):
   files += [p for p in (REPO/f'calculations/wrra_m_0_{v}').rglob('*') if eligible(p)]
   files += [p for p in (REPO/'paper').glob(f'WRRA_M_0_{v}_*') if p.suffix in ('.md','.docx','.pdf','.zip') and p.name!='WRRA_M_0_12_r1_Series_Release.zip']
  files += [p for p in (REPO/'review/0_10_to_0_12_r1').rglob('*') if eligible(p) and p.name not in ('series_reproduction_checks.json','publication_record.json')]
  files += [REPO/n for n in ('README.md','README_EN.md','README_KO.md','CITATION.cff','LICENSE','.zenodo.json','REVISION_0_10.md','REVISION_0_11.md','REVISION_0_12.md','REVISION_0_10_TO_0_12_R1.md','SHA256SUMS_0_10','SHA256SUMS_0_11','SHA256SUMS_0_12')]
  for p in files:
   target=stage/p.relative_to(REPO);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
  raw=[p for v in (10,11,12) for p in (stage/f'calculations/wrra_m_0_{v}/results').rglob('*') if eligible(p) and p.name not in META]
  raw += [stage/f'calculations/wrra_m_0_{v}/source_{l}.md' for v in (10,11,12) for l in ('ko','en')]
  expected={p.relative_to(stage).as_posix():sha(p) for p in raw}
  for directory in sorted((stage/'calculations').rglob('results'),reverse=True):
   if directory.is_dir():shutil.rmtree(directory)
  for v in (10,11,12):
   for l in ('ko','en'):(stage/f'calculations/wrra_m_0_{v}/source_{l}.md').unlink()
  env=dict(os.environ,OPENBLAS_NUM_THREADS='1')
  for v in (10,12):subprocess.run([sys.executable,str(stage/f'calculations/wrra_m_0_{v}/run_release.py')],cwd=stage,env=env,stdout=subprocess.DEVNULL,check=True)
  assert expected=={n:sha(stage/n) for n in expected},'clean-copy result/source mismatch'
  for v,n in ((10,32),(11,28),(12,36)):
   result=json.loads((stage/f'calculations/wrra_m_0_{v}/results/verification.json').read_text());assert result['passed'] and result['check_count']==n
  # Reinstate checked publication metadata and preserve all historical bytes.
  for v in (10,11,12):
   for name in META:shutil.copyfile(REPO/f'calculations/wrra_m_0_{v}/results/{name}',stage/f'calculations/wrra_m_0_{v}/results/{name}')
  # Historical files came from the exact archived baseline; replay may only have changed result dirs.
  with zipfile.ZipFile(baseline) as z:
   for n,h in historical.items():
    if not (stage/n).exists() or sha(stage/n)!=h:
     (stage/n).parent.mkdir(parents=True,exist_ok=True);(stage/n).write_bytes(z.read(n))
  assert all(sha(stage/n)==h for n,h in historical.items())
  subprocess.run([sys.executable,str(stage/'review/0_10_to_0_12_r1/review_contracts.py')],cwd=stage,env=env,check=True)
  report={'release':'0.12-r1','passed':True,'baseline_archive_sha256':BASELINE_SHA,'historical_files_preserved':len(historical),'historical_bytes_unchanged':True,'captured_result_directories_removed':True,'all_six_sources_removed_and_regenerated':True,'reproduced_files':len(expected),'outputs_and_sources_byte_identical':True,'component_groups':[32,28,36],'distinct_component_groups':96,'review_groups':9,'output_sha256':expected}
  relative=Path('review/0_10_to_0_12_r1/series_reproduction_checks.json');encoded=json.dumps(report,indent=2)+'\n';(REPO/relative).write_text(encoded);(stage/relative).write_text(encoded)
  (stage/'SHA256SUMS').unlink();allfiles=sorted(p for p in stage.rglob('*') if eligible(p))
  manifest=''.join(f'{sha(p)}  {p.relative_to(stage).as_posix()}\n' for p in allfiles);(stage/'SHA256SUMS').write_text(manifest);(REPO/'SHA256SUMS_0_12_R1_SERIES').write_text(manifest)
  target=REPO/'paper/WRRA_M_0_12_r1_Series_Release.zip'
  with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as z:
   for p in allfiles+[stage/'SHA256SUMS']:
    info=zipfile.ZipInfo(p.relative_to(stage).as_posix(),(2026,10,3,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
  with zipfile.ZipFile(target) as z:
   for line in z.read('SHA256SUMS').decode().splitlines():
    h,n=line.split('  ',1);assert hashlib.sha256(z.read(n)).hexdigest()==h,n
  print(json.dumps({'archive':target.name,'files':len(allfiles)+1,'bytes':target.stat().st_size,'sha256':sha(target),'clean_replay':True}))
if __name__=='__main__':main()
