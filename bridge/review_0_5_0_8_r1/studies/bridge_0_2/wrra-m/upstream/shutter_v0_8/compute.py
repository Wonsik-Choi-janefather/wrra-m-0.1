"""Finite conditional shutter contract; no physical time calibration."""
import json, hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'source_filter_v0_7/code/handoff.json'

def shutter(rho, eta):
    if isinstance(eta,bool) or not isinstance(eta,(int,float)) or not np.isfinite(eta) or not 0<=eta<=1: raise ValueError('eta outside [0,1]')
    rho=np.asarray(rho)
    if rho.shape!=(3,3) or not np.all(np.isfinite(rho)): raise ValueError('state')
    if not np.allclose(rho,rho.conj().T,rtol=0,atol=1e-12) or np.linalg.eigvalsh(rho).min() < -1e-12: raise ValueError('positive state required')
    if abs(np.trace(rho)-1)>1e-12: raise ValueError('normalized state required')
    return (1-eta)*rho+eta*np.diag(np.diag(rho))

def select_record(rho, draw):
    if isinstance(draw,bool) or not isinstance(draw,(int,float)) or not np.isfinite(draw) or not 0 <= draw < 1: raise ValueError('draw outside [0,1)')
    probabilities=np.real(np.diag(shutter(rho,1)))
    probabilities=np.maximum(probabilities,0)
    positive=np.flatnonzero(probabilities>0)
    cumulative=np.cumsum(probabilities[positive]/probabilities.sum())
    j=int(positive[min(int(np.searchsorted(cumulative,draw,side='right')),len(positive)-1)])
    state=np.zeros((3,3)); state[j,j]=1
    return j,state

def run():
    parent=json.loads(PARENT.read_text()); b=parent['baseline_outputs']
    # Branch order phi,D,R. This is a new coarse interface, not reconstructed microscopic coherence.
    p=np.array([b['phenotype'],b['dark'],b['return']]); p=p/p.sum()
    psi=np.sqrt(p); rho=np.outer(psi,psi)
    rows=[]
    for eta in [0,.25,.5,1]:
        out=shutter(rho,eta)
        rows.append({'eta':eta,'trace':float(np.trace(out)), 'probabilities':np.diag(out).tolist(), 'purity':float(np.trace(out@out)), 'off_diagonal_norm':float(np.linalg.norm(out-np.diag(np.diag(out))))})
        assert np.allclose(np.diag(out),p) and np.linalg.eigvalsh(out).min()>-1e-12
    # Full shutter is an idempotent record operation; partial shutter composes with eta_eff.
    assert np.allclose(shutter(shutter(rho,1),1),shutter(rho,1))
    assert np.allclose(shutter(shutter(rho,.25),.5),shutter(rho,.625))
    # Quantum instrument: unnormalized branch matrices add to the dephased state.
    branches=[]
    for j in range(3):
        proj=np.zeros((3,3));proj[j,j]=1
        sigma=proj@rho@proj; prob=float(np.trace(sigma))
        assert np.isclose(prob,p[j])
        conditional=sigma/prob
        assert np.isclose(np.trace(conditional),1)
        branches.append(sigma)
    assert np.allclose(sum(branches),shutter(rho,1))
    # Same rho has different readout after a coherent rotation: filter/shutter order is material.
    c,s=np.cos(.25),np.sin(.25); U=np.array([[c,-s,0],[s,c,0],[0,0,1]])
    before=np.diag(shutter(U@rho@U.T,1)); after=np.diag(U@shutter(rho,1)@U.T)
    assert np.max(abs(before-after))>0.01
    for draw, expected in [(0,0),(.1,1),(.9,2)]:
        j,state=select_record(rho,draw)
        assert j==expected and np.trace(state)==1
    result={'version':'upstream-0.8','parent_sha256':hashlib.sha256(PARENT.read_bytes()).hexdigest(),'branch_order':['phi','D','R'],'baseline_probabilities':p.tolist(),'shutter_scan':rows,'order_contrast':{'rotate_then_record':before.tolist(),'record_then_rotate':after.tolist()},'physical_time_unit':None,'minimal_physical_time':None,'frame':'one finite ordered update; no realized infinite address space','record_contract':'one branch per supplied draw; probability is not a simultaneously actualized record','status':'conditional finite shutter construction'}
    (ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': run()
