"""Independent release audit of the finite SOURCE/filter/stock model.

Run after code/compute.py. Uses trial factorization, direct complex products,
closed pair-rotation formulae, a Choi matrix and independently iterated stocks.
It does not interpret information stock as energy or assign a physical clock.
"""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import numpy as np

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('source_compute',ROOT/'code/compute.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
TOL=3e-11

def factor(n):
    f={};p=2
    while p*p<=n:
        while n%p==0:f[p]=f.get(p,0)+1;n//=p
        p+=1
    if n>1:f[n]=f.get(n,0)+1
    return f

def run():
    c=json.loads((ROOT/'code/inputs.json').read_text())
    r=json.loads((ROOT/'code/results.json').read_text())
    checks={}
    def check(name,value):checks[name]=bool(value)
    def rejects(name,fn):
        try:fn()
        except ValueError:check(name,True)
        else:check(name,False)
    N=161;alpha=c['alpha'];beta=c['beta']
    controls={2:{'epsilon':.13,'phase':.3},3:{'epsilon':-.08,'phase':.6},5:{'epsilon':.05,'phase':-.2}}
    n,w,psi=m.source_state(N,alpha,controls)
    direct=[]
    for address in range(2,N+1):
        z=1+0j
        for p,v in factor(address).items():
            d=controls.get(p,{});z*=(p**(-alpha/2)*np.exp(d.get('epsilon',0)/2+1j*d.get('phase',0)))**v
        direct.append(z)
    direct=np.array(direct);direct/=math.sqrt(math.fsum(float(abs(z)**2) for z in direct))
    check('factor_product_amplitudes',np.max(np.abs(direct-psi))<TOL)
    check('factor_product_weights',np.max(np.abs(abs(direct)**2-w))<TOL)
    check('trial_factorization_addresses',all(math.prod(p**v for p,v in factor(int(a)).items())==a for a in n))
    sieve=m.prime_mask(N)
    check('prime_sieve_vs_trial_factorization',all(bool(sieve[a])==(factor(int(a))=={int(a):1}) for a in n))
    for p in [2,3,5]:
        check('valuation_prime_'+str(p),all(int(v)==factor(int(a)).get(p,0) for a,v in zip(n,m.valuations(n,p))))
    es=m.effects(N,beta);f=m.fractions(w,es)
    reference={key:math.fsum(float(abs(z)**2*e) for z,e in zip(direct,effect)) for key,effect in es.items()}
    check('direct_complex_product_sector_ledger',max(abs(f[key]-value) for key,value in reference.items())<TOL)
    _,base_w,_=m.source_state(c['N'],alpha)
    # An independently grouped finite sum, using the frozen baseline masks.
    eb=m.effects(c['N'],beta)
    for key in eb:
        independent=math.fsum(float(x) for x in base_w[eb[key]>0]*eb[key][eb[key]>0])
        check('full_cutoff_fsum_'+key,abs(independent-r['baseline'][key])<TOL)
    for p in [2,3,5]:
        vp=np.array([factor(int(a)).get(p,0) for a in n]);mu=math.fsum(float(x*v) for x,v in zip(w,vp))
        derivative={key:math.fsum(float(x*e*(v-mu)) for x,e,v in zip(w,effect,vp)) for key,effect in es.items()}
        h=2e-5;high=copy.deepcopy(controls);low=copy.deepcopy(controls)
        high[p]['epsilon']+=h;low[p]['epsilon']-=h
        plus=m.fractions(m.source_state(N,alpha,high)[1],es);minus=m.fractions(m.source_state(N,alpha,low)[1],es)
        check('controlled_covariance_derivative_'+str(p),max(abs(derivative[key]-(plus[key]-minus[key])/(2*h)) for key in es)<1e-8)
        check('controlled_derivative_sum_'+str(p),abs(sum(derivative.values()))<TOL)
    # Independent closed expression for rotation of addresses 3 and 9.
    small=copy.deepcopy(c);small['coherent_N']=N;small['coherent_pair']=[3,9]
    nn,ww,_=m.source_state(N,alpha);odd=np.array([a%2==1 and factor(int(a))!={int(a):1} for a in nn])
    angle=c['mixing_angle'];s,t=math.sin(angle),math.cos(angle)
    for coherence in [0.,.37,1.]:
        errors=[]
        for phase in [0.,.73,math.pi]:
            observed,_=m.coherent_case(small,phase,coherence,angle)
            phi=beta*(math.fsum(float(x) for x in ww[odd])+s*s*(ww[1]-ww[7])+2*coherence*s*t*math.sqrt(ww[1]*ww[7])*math.cos(phase))
            errors.append(abs(observed['phenotype']-phi))
        check('closed_rotation_formula_coherence_'+str(coherence),max(errors)<TOL)
    # Generic noncommuting, nonprojective instrument on a 3-dimensional state.
    rng=np.random.default_rng(70107)
    v=rng.normal(size=3)+1j*rng.normal(size=3);v/=np.linalg.norm(v);rho=np.outer(v,v.conj())
    U=np.linalg.qr(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))[0]
    V=np.linalg.qr(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))[0]
    A=np.diag([.2,.65,.9])@U;B=np.diag([.4,.7,.1])@V;Q=np.diag([.15,.55,.95])
    values,states,ks=m.instrument(rho,A,B,Q)
    survived=A@rho@A.conj().T
    check('sequential_admission_probability',abs(1-values['initial_reflection']-np.trace(survived).real)<TOL)
    check('sequential_normal_return_probability',abs(values['normal_return']-np.trace(B@survived@B.conj().T).real)<TOL)
    check('generic_completeness',np.max(np.abs(sum(k.conj().T@k for k in ks.values())-np.eye(3)))<TOL)
    J=sum(np.outer(k.ravel(order='F'),k.ravel(order='F').conj()) for k in ks.values())
    check('choi_complete_positivity',np.linalg.eigvalsh((J+J.conj().T)/2)[0]>-TOL)
    # Column-major vectorization: partial trace over output restores I_input.
    check('choi_trace_preservation',np.max(np.abs(np.trace(J.reshape(3,3,3,3),axis1=1,axis2=3)-np.eye(3)))<TOL)
    check('generic_branch_positivity',all(np.linalg.eigvalsh(x)[0]>-TOL for x in states.values()))
    check('generic_ledger',abs(values['sum']-1)<TOL)
    ff=r['baseline'];u=c['recycling_release_fraction'];eps=c['leakage_control'];rr=ff['Actual']
    a=0.;independent=[]
    for _ in range(c['recycling_event_count']):
        a=(1-eps)*a+u*rr*(1-(1-eps)*a);independent.append(a)
    check('stock_independent_scalar_recurrence',max(abs(a-row['Actual_stock']) for a,row in zip(independent,r['transport']['recycling_with_leakage']))<TOL)
    rows=m.transport(ff,[u]*1000,eps)
    steady=u*rr/(eps+(1-eps)*u*rr)
    check('stationary_stock_after_1000_events',abs(rows[-1]['Actual_stock']-steady)<TOL)
    balance=r['recycling_analysis']['epsilon_needed_for_target']
    check('separate_balance_reaches_target',abs(m.transport(ff,[u]*1000,balance)[-1]['Actual_stock']-c['retention_target'])<TOL)
    check('unbounded_recycling_accumulates',abs(m.transport(ff,[u]*1000)[-1]['Actual_stock']-1)<TOL)
    check('one_window_closure',all(abs(x['Actual_stock']-rr)<TOL for x in m.transport(ff,[1.,0.,0.,0.])))
    check('zero_release_leaves_source',m.transport(ff,[0.,0.],1.)[-1]['SOURCE_stock']==1.)
    check('total_leakage_reset',abs(m.transport(ff,[1.,0.],1.)[-1]['SOURCE_stock']-1)<TOL)
    check('changing_protocol_stock_conservation',all(abs(x['ledger_sum']-1)<TOL for x in m.transport(ff,[.3,0.,1.,.07,.6],.21)))
    for name,fn in [
        ('non_mapping_controls',lambda:m.source_state(10,alpha,[])),
        ('nonprime_source',lambda:m.source_state(10,alpha,{4:{}})),
        ('noncanonical_key',lambda:m.source_state(10,alpha,{'03':{}})),
        ('duplicate_key',lambda:m.source_state(10,alpha,{3:{},'3':{}})),
        ('intensity_outside_domain',lambda:m.source_state(10,alpha,{3:{'epsilon':2.01}})),
        ('nan_phase',lambda:m.source_state(10,alpha,{3:{'phase':float('nan')}})),
        ('infinite_alpha',lambda:m.source_state(10,float('inf'))),
        ('nan_fraction',lambda:m.transport({**ff,'dark':float('nan')},[1.])),
        ('negative_fraction',lambda:m.transport({'phenotype':-.1,'dark':.3,'return':.8},[1.])),
        ('invalid_release',lambda:m.transport(ff,[1.01])),
        ('invalid_leakage',lambda:m.transport(ff,[1.],-0.01)),
        ('invalid_coherence',lambda:m.coherent_case(small,0.,1.1,angle)),
        ('nonpositive_state',lambda:m.instrument(np.diag([1.1,-.1,0]),A,B,Q)),
        ('nonunit_state_trace',lambda:m.instrument(rho*.9,A,B,Q)),
        ('noncontractive_A',lambda:m.instrument(rho,np.eye(3)*1.1,B,Q)),
        ('noncontractive_B',lambda:m.instrument(rho,A,np.eye(3)*1.1,Q)),
        ('invalid_readout_effect',lambda:m.instrument(rho,A,B,np.diag([1.1,0.,0.]))),
        ('matrix_shape',lambda:m.instrument(rho,np.eye(2),B,Q))]:
        rejects('reject_'+name,fn)
    # Reordered/reduced grids, a zero mixing angle and a smaller valid cutoff
    # must exercise contract checks without assuming a particular scan length.
    with tempfile.TemporaryDirectory(prefix='source_v07_audit_') as tmp:
        tmp=Path(tmp);shutil.copytree(ROOT/'code',tmp/'code',ignore=shutil.ignore_patterns('__pycache__'));shutil.copytree(ROOT/'inherited',tmp/'inherited')
        env={**os.environ,'OPENBLAS_NUM_THREADS':'2','OMP_NUM_THREADS':'2'}
        proc=subprocess.run([sys.executable,str(tmp/'code/compute.py')],capture_output=True,text=True,env=env)
        check('fresh_copy_runner',proc.returncode==0)
        for filename in ['results.json','handoff.json']:
            check('fresh_copy_byte_exact_'+filename,(tmp/'code'/filename).read_bytes()==(ROOT/'code'/filename).read_bytes())
        alternate=copy.deepcopy(c);alternate.update({'N':997,'controlled_primes':[5,2],'log_intensity_scan':[.07,-.04],
            'phase_scan':[.37],'mixing_angle':0.,'reference_event_count':1,'recycling_event_count':3})
        m.dump(tmp/'alternate.json',alternate)
        proc=subprocess.run([sys.executable,str(tmp/'code/compute.py'),'--inputs',str(tmp/'alternate.json'),'--out',str(tmp/'alternative_results.json')],capture_output=True,text=True,env=env)
        check('alternate_configuration_runner',proc.returncode==0)
        if proc.returncode==0:
            alternative=json.loads((tmp/'alternative_results.json').read_text())
            check('alternate_grid_preserved',len(alternative['phase_controls'])==3 and len(alternative['source_intensity_controls'])==4)
            check('zero_angle_reversed_roles_give_zero_residue',abs(alternative['ordered_gate_contrast']['BA_order']['Actual'])<TOL and alternative['ordered_gate_contrast']['AB_order']['Actual']>0)
        else:raise AssertionError(proc.stderr)
    check('parent_compute_all_passed',r['verification']['all_passed'])
    result={'version':'upstream-0.7','date':'2026-10-03','compute_checks':r['verification']['check_count'],
        'independent_checks':len(checks),'total_checks':r['verification']['check_count']+len(checks),
        'checks':checks,'all_passed':all(checks.values()),'numpy_version':np.__version__,
        'reproducibility':'fresh-copy results.json and handoff.json are byte-exact; OPENBLAS_NUM_THREADS=2',
        'scope':'finite address/stock model audit, without external physical validation'}
    if not result['all_passed']:raise AssertionError([k for k,v in checks.items() if not v])
    (ROOT/'verification').mkdir(exist_ok=True);m.dump(ROOT/'verification/independent_audit.json',result)
    print(json.dumps({k:result[k] for k in ['compute_checks','independent_checks','total_checks','all_passed']}))
    return result

if __name__=='__main__':run()
