"""New standard CAMB runs for a declared calibrated completion of WRRA background.
Not a claim of full-state injection of v0.4 or v0.5 events.
"""
from pathlib import Path
import sys,json,time,os
P=Path(__file__).resolve().parent
if (P/'runtime').exists():sys.path.insert(0,str(P/'runtime'))
import camb
import numpy as np

def params(branch='dark_weight_only',nonlinear=True,accuracy=1.):
    cases=json.loads((P/'inputs/address_results.json').read_text())['cases']
    bg=next(x['background'] for x in cases if x['branch']==branch)
    p=camb.CAMBparams();p.set_cosmology(**bg,omk=0,mnu=.06,nnu=3.044,tau=.0544,TCMB=2.7255)
    p.InitPower.set_params(As=2.1e-9,ns=.9649)
    p.set_for_lmax(4000,lens_potential_accuracy=1)
    p.set_accuracy(AccuracyBoost=accuracy,lAccuracyBoost=accuracy)
    p.NonLinear=camb.model.NonLinear_lens if nonlinear else camb.model.NonLinear_none
    p.NonLinearModel.set_params(halofit_version='mead2020')
    return p

def main():
    out=P/'results';out.mkdir(exist_ok=True);meta=[]
    for name,branch,nl,acc in [('linear','dark_weight_only',False,1.),
            ('nonlinear','dark_weight_only',True,1.),('unweighted_nonlinear','unweighted',True,1.),
            ('nonlinear_refined','dark_weight_only',True,1.5)]:
        t=time.time();p=params(branch,nl,acc);r=camb.get_results(p)
        cmb=r.get_cmb_power_spectra(p,CMB_unit='muK',lmax=4000)
        lens=r.get_lens_potential_cls(lmax=4000,raw_cl=True)
        np.savez_compressed(out/(name+'.npz'),ell=np.arange(4001),
            lensed=cmb['lensed_scalar'],unlensed=cmb['unlensed_scalar'],
            clpp=lens[:,0],clpT=lens[:,1],clpE=lens[:,2])
        (out/(name+'.params.txt')).write_text(str(p))
        q=dict(name=name,branch=branch,nonlinear=nl,accuracy=acc,
            seconds=time.time()-t,camb_version=camb.__version__,
            scalar_initial_condition=str(p.scalar_initial_condition),
            As=2.1e-9,ns=.9649,completion='calibrated adiabatic power law',
            full_v04_state_injected=False,finite_v05_events_injected=False)
        meta.append(q);print(q,flush=True)
    (out/'camb_runs.json').write_text(json.dumps(meta,indent=2)+'\n')
if __name__=='__main__':main()
