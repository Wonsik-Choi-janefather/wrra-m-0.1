"""0.7 microscopic SOURCE -> branch instrument -> finite record handoff."""
import importlib.util,json,hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'source_filter_v0_7/code'
spec=importlib.util.spec_from_file_location('parent07',PARENT/'compute.py')
parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)

def branches(N,alpha,beta,controls=None):
    n,w,psi=parent.source_state(N,alpha,controls)
    effects=parent.effects(N,beta)
    # Each vector is K_j psi. The two return outcomes stay distinct until classical aggregation.
    prime=parent.prime_mask(N)[2:]
    odd=(~prime)&(n%2==1)
    amplitudes={'phi':np.sqrt(effects['phenotype'])*psi,'D':np.sqrt(effects['dark'])*psi,
                'initial_reflection':np.sqrt((1-beta)*odd)*psi,'normal_return':prime*psi}
    probabilities={k:float(np.vdot(v,v).real) for k,v in amplitudes.items()}
    return n,amplitudes,probabilities

def record(amplitudes,draw):
    if isinstance(draw,bool) or not isinstance(draw,(int,float)) or not np.isfinite(draw) or not 0<=draw<1:raise ValueError('finite draw in [0,1) required')
    keys=['phi','D','initial_reflection','normal_return']
    if not isinstance(amplitudes,dict) or set(amplitudes)!=set(keys):raise ValueError('four named branches required')
    vectors={k:np.asarray(amplitudes[k]) for k in keys}
    shape=vectors[keys[0]].shape
    if len(shape)!=1 or not shape[0] or any(v.shape!=shape or not np.all(np.isfinite(v)) for v in vectors.values()):raise ValueError('finite aligned branch vectors required')
    p=np.array([np.vdot(vectors[k],vectors[k]).real for k in keys])
    if not np.all(np.isfinite(p)):raise ValueError('finite branch norms required')
    if abs(p.sum()-1)>2e-11:raise ValueError('instrument norm mismatch')
    positive=np.flatnonzero(p>0); cumulative=np.cumsum(p[positive]/p.sum())
    ix=min(int(np.searchsorted(cumulative,draw,side='right')),len(positive)-1);j=int(positive[ix])
    return keys[j],vectors[keys[j]]/np.sqrt(p[j])

def run():
    h=json.loads((PARENT/'handoff.json').read_text())
    n,a,p=branches(h['N'],h['alpha'],h['beta'])
    checks=0
    for controls in [None,{2:{'epsilon':.15}},{3:{'phase':.7}}]:
        _,vectors,probs=branches(h['N'],h['alpha'],h['beta'],controls)
        assert abs(sum(probs.values())-1)<2e-11;checks+=1
        for draw in [0,.02,.1,.5,np.nextafter(1.,0.)]:
            label,state=record(vectors,float(draw));assert abs(np.vdot(state,state).real-1)<2e-11;checks+=1
    aggregate={'phenotype':p['phi'],'dark':p['D'],'return':p['initial_reflection']+p['normal_return']}
    for k,v in aggregate.items(): assert abs(v-h['baseline_outputs'][k])<2e-11;checks+=1
    # Direct scalar weights offer an independent norm check.
    _,w,_=parent.source_state(h['N'],h['alpha'])
    direct=parent.fractions(w,parent.effects(h['N'],h['beta']))
    for k,v in aggregate.items():assert abs(v-direct[k])<2e-11;checks+=1
    for bad in [-1,1,float('nan'),True]:
        try:record(a,bad)
        except ValueError:checks+=1
        else:raise AssertionError('invalid record accepted')
    out={'version':'upstream-0.8-r1','N':h['N'],'alpha':h['alpha'],'beta':h['beta'],
         'microscopic_branch_probabilities':p,'aggregate_outputs':aggregate,'checks_passed':checks,
         'parent_sha256':hashlib.sha256((PARENT/'handoff.json').read_bytes()).hexdigest(),
         'state_contract':'classical label plus normalized microscopic conditional vector; returned mixture is not a fictitious pure amplitude',
         'frame_order':['SOURCE preparation','ordered parent filters','branch readout','one conditional record'],
         'minimum_readout_unit':'one finite branch record','physical_time_unit':None,'energy_map':None,
         'next_stage':'0.9: map microscopic conditional residue into frozen 0.6 particle/current readout'}
    (ROOT/'handoff.json').write_text(json.dumps(out,indent=2)+'\n');print(checks,'address bridge checks passed')
if __name__=='__main__':run()
