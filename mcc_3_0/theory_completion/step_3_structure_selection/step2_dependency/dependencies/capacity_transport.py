"""Frozen SOURCE-size transport through the published uniform macro branch.
Original pure functions are extracted, not full repository stages imported.
SOURCE changes are separate model probes, not time evolution of our universe.
"""
from pathlib import Path
from fractions import Fraction as F
from math import lcm
import ast,math,json,copy,hashlib
import numpy as np
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parent
SECTORS=('phenotype','resident_nonphenotype','return')
ns={'np':np,'math':math,'quad':quad,'SECTORS':SECTORS}

if __debug__ is False:
    raise RuntimeError('Run without -O: this research replay uses assertion guards.')
manifest=json.loads((ROOT/'source_manifest.json').read_text())
for pin in manifest['sources']:
    raw=(ROOT/'original'/pin['local']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==pin['sha256'], 'Pinned source changed: '+pin['local']

def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def extract(filename,functions,constants=()):
    path=ROOT/'original'/filename
    tree=ast.parse(path.read_text())
    nodes=[n for n in tree.body if
      (isinstance(n,ast.FunctionDef) and n.name in functions) or
      (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in constants for t in n.targets))]
    assert {n.name for n in nodes if isinstance(n,ast.FunctionDef)}==set(functions)
    actual_constants={t.id for n in nodes if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
    assert actual_constants==set(constants)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns)

extract('compute.py',{'address_base','phase_drive','effects'})
extract('m10_compute.py',{'response','address_moments','amplitudes'})
extract('run_stage5.py',{'nu','plummer','lens'},
        {'C','G','PARSEC_M','M_SUN_KG','H0_KM_S_MPC','FC','SPHERE_MASS_MSUN',
         'SPHERE_SCALE_KPC','TEST_RADIUS_KPC','PATCH_RADIUS_KPC','LENS_IMPACT_KPC'})
cfg=json.loads((ROOT/'original/parameters.json').read_text())
handoff=json.loads((ROOT/'original/stage2_handoff.json').read_text())['source_state']
cfg['upstream']['state']['alpha']=handoff['alpha']
cfg['upstream']['update']['sigmoid_threshold_h']=handoff['threshold_h']
params=json.loads((ROOT/'original/m10_parameters.json').read_text())
calibration=json.loads((ROOT/'original/m10_results.json').read_text())['calibration']
frozen=copy.deepcopy({'alpha':handoff['alpha'],'h':handoff['threshold_h'],
     'calibration':calibration,'energy_map':params['energy_map']})
macro_constant_names=('C','G','PARSEC_M','M_SUN_KG','H0_KM_S_MPC','FC','SPHERE_MASS_MSUN',
                     'SPHERE_SCALE_KPC','TEST_RADIUS_KPC','PATCH_RADIUS_KPC','LENS_IMPACT_KPC')
def all_frozen_inputs():
    return {'upstream':cfg,'energy_parameters':params,'calibration':calibration,
            'macro_constants':{name:ns[name] for name in macro_constant_names}}
frozen_input_hash=fingerprint(all_frozen_inputs())
contract=json.loads((ROOT/'source_contract.json').read_text())

def prime_list(limit):
    flags=np.ones(limit+1,dtype=bool);flags[:2]=False
    for p in range(2,math.isqrt(limit)+1):
        if flags[p]:flags[p*p::p]=False
    return np.flatnonzero(flags)

def streamed(N,chunk=200000):
    assert isinstance(N,int) and N>=4 and chunk>0
    c=copy.deepcopy(cfg);c['upstream']['address_cutoff_N']=N
    ep=copy.deepcopy(params);ep['upstream_0_9']=c
    primes=prime_list(math.isqrt(N))
    sums=np.zeros(3);moments=np.zeros(3);Z=0.;counts=np.zeros(3,dtype=np.int64)
    for lo in range(2,N+1,chunk):
        hi=min(N+1,lo+chunk);n=np.arange(lo,hi,dtype=np.int64)
        isprime=np.ones(hi-lo,dtype=bool)
        for pv in primes:
            p=int(pv)
            start=max(p*p,((lo+p-1)//p)*p)
            if start<hi:isprime[start-lo::p]=False
        even=(~isprime)&(n%2==0);odd=(~isprime)&(n%2==1)
        w=np.exp(-c['upstream']['state']['alpha']*np.log(n))
        base={'n':n,'prime':isprime,'even':even,'odd':odd,'w':w}
        effect=ns['effects'](c,base)
        assert np.all(effect>=0) and np.allclose(effect.sum(axis=0),1,atol=1e-14)
        sums+=effect@w
        moments+=ns['address_moments'](ep,base,effect)
        Z+=float(w.sum());counts+=np.array([isprime.sum(),even.sum(),odd.sum()])
    return sums/Z,moments/Z,counts

def macro(mu):
    E0=ns['amplitudes'](params,calibration,mu,1.0)*params['reference_volume_m3']
    n=np.array([params['energy_map']['energy_volume_exponents'][s] for s in SECTORS])
    V0=params['reference_volume_m3'];crit=calibration['ucrit_J_m3']
    H0=ns['H0_KM_S_MPC']*1000/(1e6*ns['PARSEC_M'])
    aT0=ns['C']*H0*math.sqrt(ns['FC']/8)
    rows=[];derivative_errors=[];continuity_errors=[];numeric_continuity_errors=[]
    for a in (.5,1.,2.):
        energy=V0*ns['amplitudes'](params,calibration,mu,a)
        V=V0*a**3;rho=energy/V;P=-n*rho/3
        # Same E(V) -> pressure finite difference, with fixed mu and uniform carrier.
        eps=1e-5
        Ep=E0*((V*(1+eps)/V0)**(n/3))
        Em=E0*((V*(1-eps)/V0)**(n/3))
        Pnum=-(Ep-Em)/(2*eps*V)
        derivative_errors.append(float(np.max(np.abs(Pnum-P))/rho.sum()))
        residual=(n-3)*rho+3*(rho+P)
        continuity_errors.append(float(np.max(np.abs(residual))/rho.sum()))
        # Independent centered derivative in log a for the continuity equation.
        log_step=1e-5
        ap=a*math.exp(log_step);am=a*math.exp(-log_step)
        rp=V0*ns['amplitudes'](params,calibration,mu,ap)/(V0*ap**3)
        rm=V0*ns['amplitudes'](params,calibration,mu,am)/(V0*am**3)
        numeric_residual=(rp-rm)/(2*log_step)+3*(rho+P)
        numeric_continuity_errors.append(float(np.max(np.abs(numeric_residual))/rho.sum()))
        q=.5*(rho.sum()+3*P.sum())/rho.sum()
        aT=aT0*math.sqrt(rho[1]/(crit*ns['FC']))
        r=ns['TEST_RADIUS_KPC']*1000*ns['PARSEC_M']
        aT_rotation=aT;aT_lensing=aT
        g,gm=ns['plummer'](r,aT_rotation)
        lens=ns['lens'](aT_lensing)
        rows.append({'a':a,'sector_density_J_m3':rho.tolist(),
          'density_J_m3':float(rho.sum()),'pressure_Pa':float(P.sum()),
          'H_over_H0':math.sqrt(rho.sum()/crit),'q':float(q),'aT_m_s2':aT,
          'aT_rotation_m_s2':aT_rotation,'aT_lensing_m_s2':aT_lensing,
          'rotation_km_s':math.sqrt(r*g)/1000,
          'direct_baryonic_km_s':math.sqrt(r*gm)/1000,
          'lensing_arcsec':lens['alpha_patch_arcsec'],
          'lens_quadrature_error_arcsec':lens['quad_abs_error_rad']*180/math.pi*3600})
    assert max(derivative_errors)<1e-9
    assert max(continuity_errors)<1e-12
    assert max(numeric_continuity_errors)<1e-8
    return {'E0_sector_J':E0.tolist(),'rows':rows,
        'transition_a':float(((E0[0]+E0[1])/(2*E0[2]))**(1/3)),
        'pressure_derivative_max_relative_error':max(derivative_errors),
        'continuity_max_relative_residual':max(continuity_errors),
        'numeric_continuity_max_relative_residual':max(numeric_continuity_errors)}

inputs=[case['fractions'] for case in contract['source_probes']]
branches=[]
for f in inputs:
    rational=[F(x) for x in f]
    assert all(x>=0 for x in rational) and sum(rational)==1
    L=lcm(*(x.denominator for x in rational));N=L*contract['H']*contract['C']
    shares,mu,counts=streamed(N)
    assert abs(shares.sum()-1)<1e-12 and counts.sum()==N-1
    row={'source_input_fractions':f,'L':L,'N':N,'active_addresses':N-1,
         'shares':shares.tolist(),'address_moments':mu.tolist(),'counts':counts.tolist(),
         'output_minus_source_input':[float(x)-float(y) for x,y in zip(shares,rational)],
         'macro':macro(mu)}
    row['frozen_input_hash_after_branch']=fingerprint(all_frozen_inputs())
    assert row['frozen_input_hash_after_branch']==frozen_input_hash
    branches.append(row)
    print(json.dumps({'N':N,'present':row['macro']['rows'][1]},ensure_ascii=False),flush=True)

# Cross-check streaming implementation against the original monolithic sieve.
c=copy.deepcopy(cfg);c['upstream']['address_cutoff_N']=1015000
base=ns['address_base'](c);effect=ns['effects'](c,base)
ep=copy.deepcopy(params);ep['upstream_0_9']=c
assert np.allclose(effect@base['w'],branches[0]['shares'],rtol=0,atol=3e-13)
assert np.allclose(ns['address_moments'](ep,base,effect),branches[0]['address_moments'],rtol=0,atol=3e-13)
streaming_matches_original=(np.allclose(effect@base['w'],branches[0]['shares'],rtol=0,atol=3e-13)
    and np.allclose(ns['address_moments'](ep,base,effect),branches[0]['address_moments'],rtol=0,atol=3e-13))
present=branches[0]['macro']['rows'][1]
assert abs(present['q']-(-.5285585894))<1e-9
assert abs(present['rotation_km_s']-207.5102418659)<1e-7
assert abs(present['lensing_arcsec']-.5355822400)<1e-9
assert frozen=={'alpha':cfg['upstream']['state']['alpha'],
                'h':cfg['upstream']['update']['sigmoid_threshold_h'],
                'calibration':calibration,'energy_map':params['energy_map']}
canonical_macro_reproduced=(abs(present['q']-(-.5285585894))<1e-9
    and abs(present['rotation_km_s']-207.5102418659)<1e-7
    and abs(present['lensing_arcsec']-.5355822400)<1e-9)
checks={'streaming_matches_original':bool(streaming_matches_original),
        'canonical_macro_reproduced':canonical_macro_reproduced,
        'all_address_normalizations':all(abs(sum(b['shares'])-1)<1e-12 for b in branches),
        'all_active_address_counts':all(sum(b['counts'])==b['N']-1 for b in branches),
        'all_pressure_derivatives':all(b['macro']['pressure_derivative_max_relative_error']<1e-9 for b in branches),
        'all_continuity_residuals':all(b['macro']['continuity_max_relative_residual']<1e-12 for b in branches),
        'all_numerical_continuity_residuals':all(b['macro']['numeric_continuity_max_relative_residual']<1e-8 for b in branches),
        'same_aT_used_for_rotation_and_lensing':all(r['aT_rotation_m_s2']==r['aT_lensing_m_s2']==r['aT_m_s2'] for b in branches for r in b['macro']['rows']),
        'direct_baryonic_source_frozen':max(r['direct_baryonic_km_s'] for b in branches for r in b['macro']['rows'])-min(r['direct_baryonic_km_s'] for b in branches for r in b['macro']['rows'])<1e-12,
        'all_macro_outputs_finite':all(all(math.isfinite(r[k]) for k in ('density_J_m3','pressure_Pa','q','H_over_H0','rotation_km_s','lensing_arcsec')) for b in branches for r in b['macro']['rows']),
        'all_macro_densities_positive':all(r['density_J_m3']>0 for b in branches for r in b['macro']['rows']),
        'parameters_not_refitted':all(b['frozen_input_hash_after_branch']==frozen_input_hash for b in branches),
        'SOURCE_changes_reach_macro_outputs':all(abs(b['macro']['rows'][1]['q']-present['q'])>1e-12 for b in branches[1:])}
out={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'branches':branches,
 'frozen_parameters':frozen,'scope':'uniform carrier, homogeneous energy-pressure branch, conditional Plummer local lens patch',
 'calibration_note':'Changed fractions select SOURCE sizes only; frozen filters are not recalibrated to those new targets.',
 'not_claimed':['real time evolution of SOURCE capacity','observational validation','nonuniform covariant completion','fixed total energy during expansion'],
 'source_provenance':manifest,'frozen_input_hash':frozen_input_hash,
 'software_versions':{'numpy':np.__version__,'scipy':__import__('scipy').__version__},
 'review_date':'2026-10-08'}
assert all(checks.values()),checks
(ROOT/'capacity_transport_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'status':out['status'],'checks':checks},ensure_ascii=False),flush=True)
