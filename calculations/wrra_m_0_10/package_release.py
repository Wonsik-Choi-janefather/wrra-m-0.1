"""Reproduce raw results without captured outputs, then build a checked archive.

Document building and visual QA must finish before invoking this command.
Run_release.py reproduces calculation outputs and manuscript sources; DOCX/PDF
are included as checked publications and are not silently regenerated here.
"""
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

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def eligible(path):
    return path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc'


def run():
    document = json.loads((ROOT/'results/document_checks.json').read_text())
    assert document['passed']
    runtime = {'python': platform.python_version(), 'numpy': numpy.__version__,
               'scipy': scipy.__version__, 'mpmath': __import__('mpmath').__version__,
               'platform': platform.system(), 'machine': platform.machine(),
               'randomness': 'No random sampling in the 0.10 calculation.',
               'dependency_policy': 'requirements.txt specifies dependencies; this records the checked runtime.'}
    (ROOT/'results/runtime_environment.json').write_text(json.dumps(runtime, indent=2)+'\n')
    outputs = [p for p in sorted((ROOT/'results').rglob('*')) if eligible(p) and
               p.name not in ('document_checks.json', 'reproduction_checks.json', 'runtime_environment.json')]
    output_names = [p.relative_to(ROOT).as_posix() for p in outputs]
    output_names += ['source_ko.md', 'source_en.md']
    original = {name: sha(ROOT/name) for name in output_names}
    baseline = []
    for version in (6, 7, 8, 9):
        baseline += [p for p in sorted((REPO/f'calculations/wrra_m_0_{version}').rglob('*')) if eligible(p)]
    baseline += [REPO/f'calculations/verify_wrra_m_0_{v}.py' for v in (1, 2, 3, 4)]
    with tempfile.TemporaryDirectory(prefix='wrra10-release-') as temporary:
        stage = Path(temporary)
        for p in [p for p in sorted(ROOT.rglob('*')) if eligible(p)] + baseline:
            target = stage/p.relative_to(REPO)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, target)
        for p in sorted((REPO/'paper').glob('WRRA_M_0_10_*')):
            if p.suffix in ('.md', '.docx', '.pdf'):
                target = stage/'paper'/p.name
                target.parent.mkdir(exist_ok=True)
                shutil.copyfile(p, target)
        for name in ('LICENSE', 'REVISION_0_10.md'):
            shutil.copyfile(REPO/name, stage/name)
        (stage/'README.md').write_text(
            '# WRRA-M 0.10-r1 reproducibility package\n\n'
            'Wonsik Choi · 2026-10-03 · CC BY 4.0\n\n'
            'Address information load → physical energy and volume-derived pressure. '
            'The frozen calibration reproduces q=-0.52855, v=207.5109051266 km/s '
            'and conditional deflection=0.5355865106 arcsec.\n\n'
            '[Input, scope and calculation guide](calculations/wrra_m_0_10/README.md) · '
            '[Evaluation and completion record](REVISION_0_10.md)\n\n'
            '- [한국어 PDF](paper/WRRA_M_0_10_KO.pdf) · [DOCX](paper/WRRA_M_0_10_KO.docx)\n'
            '- [English PDF](paper/WRRA_M_0_10_EN.pdf) · [DOCX](paper/WRRA_M_0_10_EN.docx)\n\n'
            '```bash\npython -m pip install -r calculations/wrra_m_0_10/requirements.txt\n'
            'python calculations/wrra_m_0_10/run_release.py\n```\n\n'
            'The command regenerates numerical results, 32 checks and both manuscript '
            'sources. Published Word/PDF files are the checked final editions. '
            'SHA256SUMS verifies every included file; runtime versions and the clean-copy '
            'byte comparison are recorded under calculations/wrra_m_0_10/results.\n')
        shutil.copyfile(ROOT/'CITATION.cff', stage/'CITATION.cff')
        staged_root = stage/'calculations/wrra_m_0_10'
        # Remove every cached numerical result, also in the frozen dependencies.
        for result_dir in sorted((stage/'calculations').rglob('results'), reverse=True):
            if result_dir.is_dir():
                shutil.rmtree(result_dir)
        for name in ('source_ko.md', 'source_en.md'):
            (staged_root/name).unlink()
        env = dict(os.environ, OPENBLAS_NUM_THREADS='1')
        subprocess.run([sys.executable, str(staged_root/'run_release.py')], cwd=stage, env=env, check=True)
        reproduced = {name: sha(staged_root/name) for name in output_names}
        assert reproduced == original, 'clean reproduction differs'
        verification = json.loads((staged_root/'results/verification.json').read_text())
        assert verification['passed'] and verification['check_count'] == 32
        # Preserve the original checked dependency snapshot in the publication ZIP.
        for p in baseline:
            target = stage/p.relative_to(REPO)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, target)
        for name in ('document_checks.json', 'runtime_environment.json'):
            shutil.copyfile(ROOT/'results'/name, staged_root/'results'/name)
        report = {'version': 'WRRA-M 0.10', 'passed': True,
                  'input_hash_sha256': verification['input_hash_sha256'],
                  'clean_copy_check_count': 32, 'captured_results_removed_before_run': True,
                  'outputs_byte_identical': True, 'reproduced_file_count': len(output_names),
                  'output_sha256': original,
                  'frozen_dependency_sources_sha256': {p.relative_to(REPO).as_posix(): sha(p)
                      for p in baseline if 'results' not in p.relative_to(REPO).parts},
                  'command': 'python calculations/wrra_m_0_10/run_release.py', 'runtime': runtime}
        encoded = json.dumps(report, indent=2)+'\n'
        (ROOT/'results/reproduction_checks.json').write_text(encoded)
        (staged_root/'results/reproduction_checks.json').write_text(encoded)
        files = [p for p in sorted(stage.rglob('*')) if eligible(p)]
        manifest = ''.join(f'{sha(p)}  {p.relative_to(stage).as_posix()}\n' for p in files)
        (stage/'SHA256SUMS').write_text(manifest)
        (REPO/'SHA256SUMS_0_10').write_text(manifest)
        archive = REPO/'paper/WRRA_M_0_10_Reproducibility.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            for p in files + [stage/'SHA256SUMS']:
                info = zipfile.ZipInfo(p.relative_to(stage).as_posix(), (2026,10,2,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                z.writestr(info, p.read_bytes())
        with zipfile.ZipFile(archive) as z:
            for line in z.read('SHA256SUMS').decode().splitlines():
                expected, name = line.split('  ', 1)
                assert hashlib.sha256(z.read(name)).hexdigest() == expected, name
        print(json.dumps({'archive': archive.name, 'files': len(files)+1,
                          'sha256': sha(archive), 'clean_copy_passed': True,
                          'reproduced_files': len(output_names)}, indent=2))


if __name__ == '__main__':
    run()
