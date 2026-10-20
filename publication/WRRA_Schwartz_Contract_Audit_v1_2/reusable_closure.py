"""Reusable coefficient/mask audit for fixed qubit I/X evolution.

The supplied coefficient matrix includes all fixed address weights. Arrays encode arbitrary conditional
Bloch components ordered (address, X/Y/Z). No arithmetic construction is assumed.
"""
import numpy as np

def compile_fixed_ix(coefficients, identity_mask, tolerance=1e-12):
    F=np.asarray(coefficients,dtype=float);mask=np.asarray(identity_mask,dtype=bool)
    if F.ndim!=2 or min(F.shape)<1 or mask.shape!=(F.shape[1],) or not np.isfinite(F).all():
        raise ValueError('finite sector-by-address matrix and matching class mask required')
    if not np.isfinite(tolerance) or tolerance<=0:
        raise ValueError('positive finite tolerance required')
    def rank(x):
        s=np.linalg.svd(x,compute_uv=False)
        return int(np.count_nonzero(s>tolerance*s[0]))
    z=np.where(mask,1.,-1.)
    # State I/X maps X->X and (Y,Z)-> +/- (Y,Z).
    action=np.column_stack([np.ones(len(mask)),z,z]).reshape(-1)
    initial=np.kron(F,np.eye(3))
    orbit=np.vstack([initial,initial*action])
    _,s,vh=np.linalg.svd(orbit,full_matrices=False)
    r=int(np.count_nonzero(s>tolerance*s[0]))
    H=vh[:r]
    transition=(H*action)@H.T
    readout=initial@H.T
    masked=np.vstack([F*mask,F*~mask])
    return {'encoding':H,'transition':transition,'readout':readout,
      'snapshot_coefficient_rank':rank(F),'class_coefficient_rank':rank(masked),
      'fixed_update_variable_dimension':r,
      'predicted_fixed_update_dimension':rank(F)+2*rank(masked),
      'full_class_variable_dimension_qubit':3*rank(masked),
      'singular_value_cutoff':float(tolerance*s[0]),
      'closure_error':float(np.max(np.abs(H*action-transition@H))) if H.size else 0.,
      'readout_reconstruction_error':float(np.max(np.abs(initial-readout@H)))}

def encode(compiled,bloch):
    return compiled['encoding']@np.asarray(bloch,dtype=float).reshape(-1)

def advance(compiled,reduced_state):
    return compiled['transition']@reduced_state

def readout(compiled,reduced_state):
    return compiled['readout']@reduced_state

if __name__=='__main__':
    F=np.array([[1.,1.,0.,0.],[0.,0.,1.,1.]])
    c=compile_fixed_ix(F,[True,False,True,False])
    print({k:v for k,v in c.items() if not isinstance(v,np.ndarray)})
