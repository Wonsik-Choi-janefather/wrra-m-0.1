"""New patched-CAMB evolution at 64 exact finite-source wavenumbers."""
from pathlib import Path
import sys,json,time,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'source/runtime'))
import camb
from camb.dark_energy import SourceVacuum

def params(accuracy=2.5,kind='D',etak=50000,stride=32,offset=0):
    case=json.loads((ROOT/'inputs/address_results.json').read_text())['cases']
    bg=next(x['background'] for x in case if x['branch']=='dark_weight_only')
    p=camb.CAMBparams();p.set_cosmology(**bg,omk=0,mnu=.06,nnu=3.044,tau=.0544,TCMB=2.7255,
        bbn_predictor='PRIMAT_Yp_DH_ErrorMC_2024.dat')
    p.InitPower.set_params(As=2.1e-9,ns=.9649,pivot_scalar=.05)
    p.DarkEnergy=SourceVacuum();p.DarkEnergy.discrete_modes=True
    p.DarkEnergy.delta_R_initial=0.;p.DarkEnergy.force_multiplier=1.;p.DarkEnergy.start_factor=1.
    p.set_for_lmax(6000,lens_potential_accuracy=0)
    p.NonLinear=camb.model.NonLinear_none
    p.set_accuracy(AccuracyBoost=accuracy,lAccuracyBoost=accuracy,lSampleBoost=49)
    p.min_l_logl_sampling=stride+1000*offset
    p.Accuracy.IntTolBoost=3;p.Accuracy.TimeStepBoost=2
    p.DoLensing=False;p.Want_CMB_lensing=True;p.max_l=6000;p.max_eta_k=etak
    p.SourceTerms.limber_windows=True;p.SourceTerms.limber_phi_lmin=100000
    p.DoLateRadTruncation=False
    p.scalar_initial_condition='initial_vector';p.InitialConditionVector=[1 if kind=='A' else 0,1 if kind=='D' else 0,0,0,0]
    return p

def run(accuracy=2.5,kind='D',etak=50000,stride=32,offset=0):
    start=time.time();p=params(accuracy,kind,etak,stride,offset)
    r=camb.get_transfer_functions(p);t=r.get_cmb_transfer_data();ell=t.L.astype(np.float64)
    assert t.L[0]==2 and t.L[-1]==6000 and np.all(np.diff(t.L)>0)
    assert t.q.shape==(64,) and np.max(abs(t.q-.05*np.arange(1,65)))<2e-14
    assert np.isfinite(t.delta_p_l_k).all()
    target=ROOT/'results'/f'{kind}_64_a{accuracy:g}_s{stride}_o{offset}_k{etak}.npz'
    np.savez_compressed(target,ell=t.L,k=t.q,T=t.delta_p_l_k[0],
        E=t.delta_p_l_k[1]*np.sqrt((ell-1)*ell*(ell+1)*(ell+2))[:,None],phi=t.delta_p_l_k[2])
    (target.with_suffix('.params.txt')).write_text(str(p))
    meta={'accuracy':accuracy,'kind':kind,'max_eta_k':etak,'paired_ell_stride':stride,'ell_grid_offset_index':offset,'conformal_time_today_Mpc':float(r.tau0),
          'kmax_times_tau0':float(t.q[-1]*r.tau0),'elapsed_seconds':time.time()-start,
          'new_Boltzmann_evolution':True,'extrapolated_modes':0,'k_count':64,'ell_count':len(ell),
          'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    target.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps(meta),flush=True)

if __name__=='__main__':
    run(float(sys.argv[1]) if len(sys.argv)>1 else 2.5,sys.argv[2] if len(sys.argv)>2 else 'D',int(sys.argv[3]) if len(sys.argv)>3 else 50000,int(sys.argv[4]) if len(sys.argv)>4 else 32,int(sys.argv[5]) if len(sys.argv)>5 else 0)
