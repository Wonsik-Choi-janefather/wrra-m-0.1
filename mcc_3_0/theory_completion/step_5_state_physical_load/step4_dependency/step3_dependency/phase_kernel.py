"""Chunked finite phase admission with inherited frame-transfer semantics.
No fitting occurs here. The caller supplies the complete frozen model inputs.
"""
import numpy as np

def iter_frame_transfers(cost,gamma,coefficients,offsets,phase_step,threshold,frames,*,chunk=65536,method='rotation'):
    cost=np.asarray(cost,dtype=float)
    gamma=np.asarray(gamma,dtype=float);coefficients=np.asarray(coefficients,dtype=float);offsets=np.asarray(offsets,dtype=float)
    if cost.ndim!=1 or gamma.ndim!=1 or not len(gamma) or coefficients.shape!=gamma.shape or offsets.shape!=gamma.shape:
        raise ValueError('phase input shapes do not match')
    if not all(np.isfinite(v).all() for v in (cost,gamma,coefficients,offsets)) or not np.isfinite(phase_step) or not np.isfinite(threshold):
        raise ValueError('phase inputs must be finite')
    if not isinstance(frames,int) or isinstance(frames,bool) or frames<1 or not isinstance(chunk,int) or isinstance(chunk,bool) or chunk<1:
        raise ValueError('positive integer frames and chunk required')
    if method not in ('direct','rotation'):raise ValueError('unknown kernel')
    gamma=gamma[:,None];coefficients=coefficients[:,None];offsets=offsets[:,None]
    ct=np.cos(gamma*phase_step);st=np.sin(gamma*phase_step)
    for lo in range(0,len(cost),chunk):
        hi=min(len(cost),lo+chunk);values=cost[lo:hi];remaining=np.ones(hi-lo)
        if method=='rotation':
            angle=gamma*values[None,:]+offsets;c=np.cos(angle);z=np.sin(angle)
        for k in range(frames):
            if method=='rotation':drive=(coefficients*c).sum(axis=0)
            else:drive=(coefficients*np.cos(gamma*(values[None,:]+phase_step*k)+offsets)).sum(axis=0)
            transfer=remaining*(-np.expm1(-np.logaddexp(0,drive-threshold)))
            remaining=remaining-transfer
            # Emitted buffers remain valid after resuming this generator.
            yield lo,hi,k,transfer,remaining if k+1==frames else None
            if method=='rotation' and k+1<frames:
                c,z=c*ct-z*st,z*ct+c*st
