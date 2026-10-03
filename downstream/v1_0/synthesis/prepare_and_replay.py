"""Reproduce the integrated manuscript audit in a fresh directory."""
from pathlib import Path, PurePosixPath
import argparse, os, shutil, subprocess, sys, zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--work-dir',type=Path,default=ROOT/'audit_work')
    args=parser.parse_args()
    work=args.work_dir.resolve()
    work.mkdir(parents=True,exist_ok=False)
    archive=ROOT/'WRRA_M_0_12_r1_Series_Release.zip'
    baseline=work/'baseline_series'
    with zipfile.ZipFile(archive) as z:
        for item in z.infolist():
            path=PurePosixPath(item.filename)
            if path.is_absolute() or '..' in path.parts:
                raise ValueError('Unsafe archive path')
        z.extractall(baseline)
    replay=work/'replay_series'
    shutil.copytree(baseline,replay)
    for path in sorted((replay/'calculations').rglob('results'),key=lambda p:len(p.parts),reverse=True):
        if path.is_dir():shutil.rmtree(path)
    for n in (10,11,12):
        for lang in ('en','ko'):
            (replay/f'calculations/wrra_m_0_{n}/source_{lang}.md').unlink()
    shutil.copyfile(ROOT/'replay_expected.json',work/'replay_expected.json')
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1')
    commands=['calculations/wrra_m_0_10/run_release.py','calculations/wrra_m_0_12/run_release.py']
    with (work/'replay.log').open('w') as log:
        for script in commands:
            subprocess.run([sys.executable,script],cwd=replay,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
        # These receipts describe the already published documents. They do not validate new PDFs.
        for n in (10,11,12):
            name=f'calculations/wrra_m_0_{n}/results/document_checks.json'
            shutil.copyfile(baseline/name,replay/name)
        subprocess.run([sys.executable,'review/0_10_to_0_12_r1/review_contracts.py'],cwd=replay,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    subprocess.run([sys.executable,str(HERE/'audit_synthesis.py'),'--evidence-dir',str(work),'--archive',str(archive)],check=True)

if __name__=='__main__':main()
