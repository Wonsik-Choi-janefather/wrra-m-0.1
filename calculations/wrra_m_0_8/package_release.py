"""Build a self-contained 0.8 ZIP after reproducing a clean copy.

Document building and visual inspection precede this packaging step.
"""
from pathlib import Path
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile
import numpy
import scipy

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
OUTPUTS = ('results.json', 'case_table.csv', 'channel_table.csv',
           'particle_inventory.csv', 'verification.json', 'inherited_exact_checks.json')
BASELINE = tuple('calculations/wrra_m_0_6/'+n for n in
                 ('compute.py','parameters.json','baseline_0_5/compute.py',
                  'baseline_0_5/parameters.json','results/summary.json')) + tuple(
                  'calculations/wrra_m_0_7/'+n for n in
                  ('compute.py','parameters.json','results/results.json')) + tuple(
                  f'calculations/verify_wrra_m_0_{v}.py' for v in (1,2,3,4))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def eligible(path):
    return path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc'


def run():
    environment = {'python':platform.python_version(), 'numpy':numpy.__version__,
                   'scipy':scipy.__version__, 'platform':platform.system(),
                   'machine':platform.machine(), 'random_test_seed':808,
                   'dependency_policy':'See requirements.txt; this file records the checked runtime.'}
    (ROOT/'results/runtime_environment.json').write_text(json.dumps(environment,indent=2)+'\n')
    original = {name:sha(ROOT/'results'/name) for name in OUTPUTS}
    with tempfile.TemporaryDirectory(prefix='wrra08-package-') as temporary:
        stage = Path(temporary)
        for file in sorted(ROOT.rglob('*')):
            if eligible(file):
                target = stage/file.relative_to(REPO)
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(file,target)
        for name in BASELINE:
            target = stage/name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(REPO/name,target)
        for file in sorted((REPO/'paper').glob('WRRA_M_0_8_*')):
            if file.suffix in ('.md','.docx','.pdf'):
                (stage/'paper').mkdir(exist_ok=True)
                shutil.copyfile(file,stage/'paper'/file.name)
        for name in ('LICENSE','REVISION_0_8.md'):
            shutil.copyfile(REPO/name,stage/name)
        shutil.copyfile(ROOT/'README.md',stage/'README.md')
        shutil.copyfile(ROOT/'CITATION.cff',stage/'CITATION.cff')
        staged_root = stage/'calculations/wrra_m_0_8'
        for name in OUTPUTS:
            (staged_root/'results'/name).unlink()
        subprocess.run([sys.executable,str(staged_root/'run_release.py')],cwd=stage,check=True)
        reproduced = {name:sha(staged_root/'results'/name) for name in OUTPUTS}
        assert reproduced == original, 'clean-copy outputs differ'
        verification = json.loads((staged_root/'results/verification.json').read_text())
        assert verification['passed'] and verification['check_count'] == 22
        assert all(sha(REPO/name) == sha(stage/name) for name in BASELINE)
        report = {'version':'WRRA-M 0.8', 'passed':True,
                  'input_hash_sha256':verification['input_hash_sha256'],
                  'clean_copy_check_count':22, 'captured_results_removed_before_run':True,
                  'outputs_byte_identical':True, 'output_sha256':original,
                  'frozen_baseline_files_preserved':True,
                  'frozen_baseline_sha256':{name:sha(REPO/name) for name in BASELINE},
                  'command':'python calculations/wrra_m_0_8/run_release.py',
                  'runtime':environment}
        encoded = json.dumps(report,indent=2)+'\n'
        (ROOT/'results/reproduction_checks.json').write_text(encoded)
        (staged_root/'results/reproduction_checks.json').write_text(encoded)
        files = [p for p in sorted(stage.rglob('*')) if eligible(p)]
        manifest = ''.join(f'{sha(p)}  {p.relative_to(stage).as_posix()}\n' for p in files)
        (stage/'SHA256SUMS').write_text(manifest)
        (REPO/'SHA256SUMS_0_8').write_text(manifest)
        archive = REPO/'paper/WRRA_M_0_8_Reproducibility.zip'
        with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for file in files+[stage/'SHA256SUMS']:
                info = zipfile.ZipInfo(file.relative_to(stage).as_posix(),(2026,10,1,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                z.writestr(info,file.read_bytes())
        with zipfile.ZipFile(archive) as z:
            for line in z.read('SHA256SUMS').decode().splitlines():
                expected,name = line.split('  ',1)
                assert hashlib.sha256(z.read(name)).hexdigest() == expected, name
        print(json.dumps({'archive':archive.name,'files':len(files)+1,
                          'sha256':sha(archive),'clean_copy_passed':True},indent=2))


if __name__ == '__main__':
    run()
