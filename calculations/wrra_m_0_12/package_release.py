"""Clean-copy numerical replay, provenance manifest and deterministic ZIP."""
from pathlib import Path
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile
import numpy
import scipy

ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent.parent
META={'document_checks.json','reproduction_checks.json','runtime_environment.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def eligible(p):return p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'

def run():
    assert json.loads((ROOT/'results/document_checks.json').read_text())['passed']
    runtime={'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,'mpmath':__import__('mpmath').__version__,'platform':platform.system(),'machine':platform.machine(),'randomness':'No random sampling in the 0.12 calculation.'}
    (ROOT/'results/runtime_environment.json').write_text(json.dumps(runtime,indent=2)+'\n')
    own=[p for p in sorted(ROOT.rglob('*')) if eligible(p)]
    baseline=[]
    for version in (6,7,8,9,10,11):baseline += [p for p in sorted((REPO/f'calculations/wrra_m_0_{version}').rglob('*')) if eligible(p)]
    baseline += [REPO/f'calculations/verify_wrra_m_0_{v}.py' for v in (1,2,3,4)]
    raw=[p for p in sorted((ROOT/'results').rglob('*')) if eligible(p) and p.name not in META]
    raw += [ROOT/'source_ko.md',ROOT/'source_en.md']
    raw += [p for version in (10,11) for p in sorted((ROOT.parent/f'wrra_m_0_{version}/results').rglob('*')) if eligible(p) and p.name not in META]
    raw += [ROOT.parent/'wrra_m_0_11/source_ko.md',ROOT.parent/'wrra_m_0_11/source_en.md']
    names=[p.relative_to(REPO).as_posix() for p in raw];original={name:sha(REPO/name) for name in names}
    with tempfile.TemporaryDirectory(prefix='wrra12-release-') as temporary:
        stage=Path(temporary)
        for p in own+baseline:
            target=stage/p.relative_to(REPO);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
        for p in sorted((REPO/'paper').glob('WRRA_M_0_12_*')):
            if p.suffix in ('.md','.docx','.pdf'):
                target=stage/'paper'/p.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(p,target)
        for name in ('LICENSE','REVISION_0_12.md'):shutil.copyfile(REPO/name,stage/name)
        shutil.copyfile(ROOT/'CITATION.cff',stage/'CITATION.cff')
        (stage/'README.md').write_text(
            '# WRRA_M 0.12 reproducibility package\n\nWonsik Choi · 2026-10-03 · CC BY 4.0\n\n'
            'Worldline proper-time updates and finite boundary spectra retain the frozen 0.11 calibration. '
            'The construction epsilon=0.05 is not a measured minimum time. The old slow expansion-state '
            'clock fails identification with the SI energy phase; that failure is preserved.\n\n'
            '[Calculation guide](calculations/wrra_m_0_12/README.md) · [Completion record](REVISION_0_12.md)\n\n'
            '- [한국어 PDF](paper/WRRA_M_0_12_KO.pdf) · [Word](paper/WRRA_M_0_12_KO.docx)\n'
            '- [English PDF](paper/WRRA_M_0_12_EN.pdf) · [Word](paper/WRRA_M_0_12_EN.docx)\n\n'
            '```bash\npython -m pip install -r calculations/wrra_m_0_12/requirements.txt\n'
            'python calculations/wrra_m_0_12/run_release.py\n```\n\n'
            'This regenerates numerical outputs, 36 new checks, 60 inherited checks and bilingual sources. '
            'Published Word/PDF editions are checked final artifacts. All captured result directories '
            'were removed before the byte comparison recorded in results/reproduction_checks.json. '
            'SHA256SUMS verifies archive contents. package_release.py is a publication-maintenance script, '
            'rather than the ordinary numerical reproduction command.\n')
        for directory in sorted((stage/'calculations').rglob('results'),reverse=True):
            if directory.is_dir():shutil.rmtree(directory)
        own_stage=stage/'calculations/wrra_m_0_12'
        for source_stage in (own_stage,stage/'calculations/wrra_m_0_11'):
            for name in ('source_ko.md','source_en.md'):(source_stage/name).unlink()
        subprocess.run([sys.executable,str(own_stage/'run_release.py')],cwd=stage,env=dict(os.environ,OPENBLAS_NUM_THREADS='1'),check=True)
        reproduced={name:sha(stage/name) for name in names};assert reproduced==original,'clean-copy byte mismatch'
        verified=json.loads((own_stage/'results/verification.json').read_text());assert verified['passed'] and verified['check_count']==36
        previous=json.loads((stage/'calculations/wrra_m_0_10/results/verification.json').read_text());assert previous['passed'] and previous['check_count']==32
        inherited11=json.loads((stage/'calculations/wrra_m_0_11/results/verification.json').read_text());assert inherited11['passed'] and inherited11['check_count']==28
        for p in baseline:
            target=stage/p.relative_to(REPO);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
        for name in ('document_checks.json','runtime_environment.json'):shutil.copyfile(ROOT/'results'/name,own_stage/'results'/name)
        report={'version':'WRRA-M 0.12','passed':True,'input_hash_sha256':verified['input_hash_sha256'],'clean_copy_check_count':36,'inherited_0_11_check_count':28,'inherited_0_10_check_count':32,'inherited_check_count':60,'captured_results_removed_before_run':True,'outputs_byte_identical':True,'reproduced_file_count':len(names),'output_sha256':original,'frozen_dependency_sources_sha256':{p.relative_to(REPO).as_posix():sha(p) for p in baseline if 'results' not in p.relative_to(REPO).parts},'command':'python calculations/wrra_m_0_12/run_release.py','runtime':runtime}
        encoded=json.dumps(report,indent=2)+'\n';(ROOT/'results/reproduction_checks.json').write_text(encoded);(own_stage/'results/reproduction_checks.json').write_text(encoded)
        files=[p for p in sorted(stage.rglob('*')) if eligible(p)]
        manifest=''.join(f'{sha(p)}  {p.relative_to(stage).as_posix()}\n' for p in files)
        (stage/'SHA256SUMS').write_text(manifest);(REPO/'SHA256SUMS_0_12').write_text(manifest)
        archive=REPO/'paper/WRRA_M_0_12_Reproducibility.zip'
        with zipfile.ZipFile(archive,'w') as z:
            for p in files+[stage/'SHA256SUMS']:
                info=zipfile.ZipInfo(p.relative_to(stage).as_posix(),(2026,10,3,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
        with zipfile.ZipFile(archive) as z:
            for line in z.read('SHA256SUMS').decode().splitlines():
                expected,name=line.split('  ',1);assert hashlib.sha256(z.read(name)).hexdigest()==expected,name
        print(json.dumps({'archive':archive.name,'files':len(files)+1,'sha256':sha(archive),'clean_copy_passed':True,'reproduced_files':len(names)},indent=2))

if __name__=='__main__':run()
