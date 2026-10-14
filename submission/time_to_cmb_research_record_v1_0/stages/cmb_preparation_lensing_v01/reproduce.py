"""Run the actual patched solver and native likelihoods serially.
Usage: python reproduce.py [--skip-camb | --verify-only]
Install requirements first. A working patched runtime is bundled for Linux;
otherwise run build.py with gfortran and make.
"""
from pathlib import Path
import os,sys,subprocess,argparse,json
import numpy as np
ROOT=Path(__file__).resolve().parent
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',
    PYTHONPATH=str(ROOT/'runtime')+os.pathsep+os.environ.get('PYTHONPATH',''))
def run(*args):
    subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,env=env,check=True)

def main():
    a=argparse.ArgumentParser();g=a.add_mutually_exclusive_group()
    g.add_argument('--skip-camb',action='store_true');g.add_argument('--verify-only',action='store_true')
    opt=a.parse_args()
    if not opt.verify_only:
        run('reconstruct_upstream.py')
        old=json.loads((ROOT/'inputs/address_results.json').read_text())
        new=json.loads((ROOT/'results/address_results.json').read_text())
        errors={}
        for x,y in zip(old['cases'],new['cases']):
            assert x['branch']==y['branch']
            assert np.allclose(x['mean_load_P_D_R'],y['mean_load_P_D_R'],rtol=1e-12,atol=1e-15)
            errors[x['branch']]=float(np.max(abs(np.array(x['mean_load_P_D_R'])-y['mean_load_P_D_R'])))
            for j,k in zip(x['amplitudes'],y['amplitudes']):
                assert abs(j['S_D']-k['S_D'])<1e-18 and abs(j['delta_R']-k['delta_R'])<1e-18
        (ROOT/'results/upstream_reproduction_check.json').write_text(json.dumps(dict(checks=new['checks'],
            all_checks_pass=new['all_checks_pass'],frozen_load_max_abs_difference=errors,mode_vectors_match=True),indent=2))
        run('preparation.py');run('check_initial.py')
        if not opt.skip_camb:
            run('lensing.py','standard',2.5)
            for acc in [1.5,2.5]:
                for kind in ['D','R']:run('lensing.py',kind,acc)
        run('lens_response.py');run('expanded_likelihood.py')
    run('validate.py');run('figures.py');run('write_report.py')
    print('Completed: results/validation_results.json and the expanded native likelihood evaluation.')

if __name__=='__main__':main()
