"""Preserve the published 0.6-r2 series and add reviewed 0.7--0.9.

Usage: python review/0_7_to_0_9_r1/package_series.py --baseline-archive PATH
The baseline ZIP is available from doi:10.5281/zenodo.23076547.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile

REPO = Path(__file__).resolve().parents[2]
BASELINE_SHA = 'bdf320d8d8a3c7a041551d501c0574243482b75ae0b95d6938e34e8e35f54357'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def eligible(path):
    return path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-archive',type=Path,required=True)
    args = parser.parse_args()
    assert sha(args.baseline_archive) == BASELINE_SHA, 'unexpected baseline archive'
    with tempfile.TemporaryDirectory(prefix='wrra09-series-') as temporary:
        stage = Path(temporary)
        with zipfile.ZipFile(args.baseline_archive) as archive:
            for name in archive.namelist():
                assert not Path(name).is_absolute() and '..' not in Path(name).parts
            for line in archive.read('SHA256SUMS').decode().splitlines():
                expected,name = line.split('  ',1)
                assert hashlib.sha256(archive.read(name)).hexdigest() == expected,name
            archive.extractall(stage)
        preserved = {p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*')
                     if eligible(p) and (p.relative_to(stage).parts[0] in ('calculations','paper'))}
        for name in ('README.md','README_EN.md','README_KO.md','CITATION.cff','.zenodo.json'):
            old = stage/name
            history = stage/'review/0_6_r2_original_metadata'/name
            history.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(old,history)
        overlay = []
        for version in (7,8,9):
            overlay.extend(p for p in (REPO/f'calculations/wrra_m_0_{version}').rglob('*') if eligible(p))
            overlay.extend(p for p in (REPO/'paper').glob(f'WRRA_M_0_{version}_*') if p.suffix in ('.md','.docx','.pdf'))
        overlay.extend(p for p in (REPO/'review/0_7_to_0_9_r1').rglob('*') if eligible(p) and p.name != 'series_reproduction_checks.json')
        overlay.extend(REPO/name for name in ('README.md','README_KO.md','README_EN.md','CITATION.cff','LICENSE','.zenodo.json','ZENODO_METADATA_0_6_R2.json','REVISION_0_7.md','REVISION_0_8.md','REVISION_0_9.md','REVISION_0_7_TO_0_9_R1.md','SHA256SUMS_0_7','SHA256SUMS_0_8','SHA256SUMS_0_9'))
        for file in overlay:
            target = stage/file.relative_to(REPO)
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(file,target)
        assert all(sha(stage/name) == expected for name,expected in preserved.items()), 'historical calculation or paper changed'
        checks = {}
        for version,expected_count in ((7,19),(8,23),(9,27)):
            component = stage/f'calculations/wrra_m_0_{version}'
            namespace = {}
            # Read the declared output list without importing its packaging dependencies.
            code = (component/'package_release.py').read_text()
            start = code.index('OUTPUTS = ')
            end = code.index('\nBASELINE',start)
            exec(code[start:end],namespace)
            outputs = namespace['OUTPUTS']
            expected = {name:sha(component/'results'/name) for name in outputs}
            for name in outputs:
                (component/'results'/name).unlink()
            subprocess.run([sys.executable,str(component/'run_release.py')],cwd=stage,check=True,stdout=subprocess.DEVNULL)
            assert expected == {name:sha(component/'results'/name) for name in outputs}, f'0.{version} output mismatch'
            verification = json.loads((component/'results/verification.json').read_text())
            assert verification['passed'] and verification['check_count'] == expected_count
            checks[f'0.{version}-r1'] = {'passed':True,'checks':expected_count,'outputs_byte_identical':True,'captured_outputs_removed_before_run':True,'input_sha256':verification['input_hash_sha256']}
        report = {'version':'0.9-r1','baseline_archive_sha256':BASELINE_SHA,'preserved_historical_files':len(preserved),'preserved_historical_files_unchanged':True,'checks':checks,'total_checks':69,'passed':True}
        relative = Path('review/0_7_to_0_9_r1/series_reproduction_checks.json')
        encoded = json.dumps(report,indent=2)+'\n'
        (REPO/relative).write_text(encoded)
        (stage/relative).write_text(encoded)
        (stage/'SHA256SUMS').unlink()
        files = sorted(p for p in stage.rglob('*') if eligible(p))
        manifest = ''.join(f'{sha(p)}  {p.relative_to(stage).as_posix()}\n' for p in files)
        (stage/'SHA256SUMS').write_text(manifest)
        (REPO/'SHA256SUMS_0_9_R1_SERIES').write_text(manifest)
        target = REPO/'paper/WRRA_M_0_9_r1_Series_Release.zip'
        with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as archive:
            for file in files+[stage/'SHA256SUMS']:
                info = zipfile.ZipInfo(file.relative_to(stage).as_posix(),(2026,10,2,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info,file.read_bytes())
        with zipfile.ZipFile(target) as archive:
            for line in archive.read('SHA256SUMS').decode().splitlines():
                expected,name = line.split('  ',1)
                assert hashlib.sha256(archive.read(name)).hexdigest() == expected,name
        print(json.dumps({'archive':target.name,'files':len(files)+1,'bytes':target.stat().st_size,'sha256':sha(target),'clean_copy_passed':True},indent=2))

if __name__ == '__main__':
    main()
