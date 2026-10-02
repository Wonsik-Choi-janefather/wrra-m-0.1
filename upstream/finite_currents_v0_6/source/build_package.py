"""Deterministic reproduction ZIP plus a fresh-extraction calculation check."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent.parent
ARCHIVE=ROOT/'paper/WRRA_M_Finite_Momentum_Currents_Beta_Corrections_v0_6_Reproducibility_2026_10_03.zip'
def payload():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and
        not any(x in ('qa','__pycache__') for x in p.relative_to(ROOT).parts) and
        p.suffix not in ('.zip','.log','.pyc') and p.name not in
        ('SHA256SUMS','package_verification.json','equations.docx','equations.txt'))
def run():
    files=payload()
    lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix() for p in files]
    (ROOT/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
    files.append(ROOT/'SHA256SUMS')
    with zipfile.ZipFile(ARCHIVE,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(files):
            info=zipfile.ZipInfo('finite_currents_v0_6/'+p.relative_to(ROOT).as_posix(),date_time=(2026,10,3,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes())
    with tempfile.TemporaryDirectory(prefix='u06_zip_') as td:
        with zipfile.ZipFile(ARCHIVE) as z:
            assert z.testzip() is None
            z.extractall(td)
        fresh=Path(td)/'finite_currents_v0_6'
        for line in (fresh/'SHA256SUMS').read_text().splitlines():
            expected,name=line.split('  ',1)
            assert hashlib.sha256((fresh/name).read_bytes()).hexdigest()==expected,name
        expected=(fresh/'code/results.json').read_bytes();(fresh/'code/results.json').unlink()
        env=dict(os.environ,OPENBLAS_NUM_THREADS='2')
        r=subprocess.run([sys.executable,str(fresh/'code/compute.py')],cwd=fresh,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        assert r.returncode==0,r.stdout
        assert (fresh/'code/results.json').read_bytes()==expected
        result=json.loads(expected);assert all(result['checks'].values())
    report={'zip_crc_pass':True,'all_payload_hashes_pass':True,'fresh_zip_results_bytes_identical':True,
        'fresh_zip_implementation_checks':result['checks_total'],'archive_members':len(files),
        'archive_sha256':hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
        'result_sha256':hashlib.sha256(expected).hexdigest()}
    (ROOT/'package_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':run()
