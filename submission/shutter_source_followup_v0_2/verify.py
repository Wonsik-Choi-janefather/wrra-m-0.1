"""Default verifies inputs/source and numerics; --archive also verifies output bytes."""
from pathlib import Path
import argparse,hashlib,json
from metrics import collect,compare
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--archive',action='store_true')
    options=parser.parse_args();root=Path(__file__).resolve().parent;count=0
    for row in (root/'SHA256SUMS.txt').read_text().splitlines():
        digest,path=row.split('  ',1)
        if not options.archive and 'results' in Path(path).parts:continue
        assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest,path
        count+=1
    compare(collect(root/'results'),json.loads((root/'numerical_reference.json').read_text()))
    for name in ['supply','photon','CMB_higher','review']:
        result=json.loads((root/f'results/{name}_results.json').read_text());assert all(result['checks'].values()),name
    summary=json.loads((root/'results/summary.json').read_text());assert summary['all_passed']
    print(f'{count} file hashes and stable numerical observables verified; all recorded controls passed')
if __name__=='__main__':main()
