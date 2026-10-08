"""Step 2: structural arithmetic readout and passive-address invariance.
Relations and costs are explicit model data; display labels are not relations.
"""
from pathlib import Path
import ast,copy,json,hashlib,math,itertools
import numpy as np

ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run without -O.')
dep=json.loads((ROOT/'dependency_manifest.json').read_text())
for name,digest in dep['files'].items():
    assert hashlib.sha256((ROOT/'dependencies'/name).read_bytes()).hexdigest()==digest,name

# Reuse pinned Step-1 setup and pure macro function; stop before its probe loop.
path=ROOT/'dependencies/capacity_transport.py'
tree=ast.parse(path.read_text());prefix=[]
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='inputs' for t in node.targets):break
    prefix.append(node)
adapter={'__file__':str(path),'__name__':'step1_pinned_adapter'}
exec(compile(ast.Module(body=prefix,type_ignores=[]),str(path),'exec'),adapter)
ns=adapter['ns'];cfg=copy.deepcopy(adapter['cfg']);params=adapter['params']
N=1015000;cfg['upstream']['address_cutoff_N']=N
base=ns['address_base'](cfg);reference_effect=ns['effects'](cfg,base)
frozen_input_hash=adapter['fingerprint']({'cfg':cfg,'params':params,'calibration':adapter['calibration']})
reference_shares=reference_effect@base['w']
ep=copy.deepcopy(params);ep['upstream_0_9']=cfg
reference_mu=ns['address_moments'](ep,base,reference_effect)
reference_macro=adapter['macro'](reference_mu)

# Build the intrinsic factor-composition coordinates of the finite structure.
# Unit 1 has zero factors and zero cost; the active domain is 2..N.
omega=np.zeros(N+1,dtype=np.int16)
v2=np.zeros(N+1,dtype=np.int16)
cost=np.zeros(N+1,dtype=float)
logp=np.log(np.arange(1,N+1,dtype=float))
for n in range(2,N+1):
    p=int(base['spf'][n-2]);parent=n//p
    omega[n]=omega[parent]+1
    v2[n]=v2[parent]+int(p==2)
    cost[n]=cost[parent]+logp[p-1]

def factors(n):
    out={}
    while n>1:
        p=int(base['spf'][n-2]);out[p]=out.get(p,0)+1;n//=p
    return out

struct_prime=omega[2:]==1
struct_even=(omega[2:]>=2)&(v2[2:]>=1)
struct_odd=(omega[2:]>=2)&(v2[2:]==0)
assert np.array_equal(struct_prime,base['prime'])
assert np.array_equal(struct_even,base['even'])
assert np.array_equal(struct_odd,base['odd'])
assert cost[1]==0 and omega[1]==0
cost_error=float(np.max(np.abs(cost[2:]-np.log(base['n']))))
assert cost_error<2e-14

def structural_effect(cost_vector,prime,even,odd):
    admission=np.zeros(len(cost_vector))
    spectrum=cfg['upstream']['spectrum'];update=cfg['upstream']['update']
    gamma=np.asarray(spectrum['gamma'])[:,None]
    coefficients=np.asarray(spectrum['coefficients'])[:,None]
    offsets=np.asarray(spectrum['phase_offsets'])[:,None]
    drives=np.array([(coefficients*np.cos(gamma*(cost_vector[odd][None,:]+update['phase_step_xi']*k)+offsets)).sum(axis=0)
                     for k in range(update['admission_frames_K'])])
    admission[odd]=-np.expm1(-np.logaddexp(0,drives-update['sigmoid_threshold_h']).sum(axis=0))
    return np.array([admission,even.astype(float),1-admission-even])

effect=structural_effect(cost[2:],struct_prime,struct_even,struct_odd)
raw_w=np.exp(-cfg['upstream']['state']['alpha']*cost[2:]);w=raw_w/raw_w.sum()
lam=np.array([params['energy_map']['address_response_lambda'][s] for s in ns['SECTORS']])
g=1+lam[:,None]*cost[2:][None,:]/math.log(N)
shares=effect@w;mu=(effect*g*w[None,:]).sum(axis=1)
assert np.allclose(effect,reference_effect,rtol=0,atol=2e-13)
assert np.allclose(w,base['w'],rtol=3e-14,atol=1e-16)
assert np.allclose(shares,reference_shares,rtol=0,atol=2e-13)
assert np.allclose(mu,reference_mu,rtol=0,atol=2e-13)

# Multiplication is partial: products >N are outside this finite address domain.
def product(a,b):
    value=a*b
    return value if value<=N else None

rng=np.random.default_rng(20261008)
product_rows=[]
max_phase_error=0.;max_raw_weight_rel_error=0.
for _ in range(1000):
    a=int(rng.integers(2,math.isqrt(N)+1));b=int(rng.integers(2,N//a+1))
    c=product(a,b);assert c is not None
    f=factors(a);fb=factors(b)
    for p,k in fb.items():f[p]=f.get(p,0)+k
    assert f==factors(c)
    gamma=np.asarray(cfg['upstream']['spectrum']['gamma'])
    left=np.exp(1j*gamma*cost[c]);right=np.exp(1j*gamma*cost[a])*np.exp(1j*gamma*cost[b])
    max_phase_error=max(max_phase_error,float(np.max(np.abs(left-right))))
    alpha=cfg['upstream']['state']['alpha']
    lhs=math.exp(-alpha*cost[c]);rhs=math.exp(-alpha*cost[a])*math.exp(-alpha*cost[b])
    max_raw_weight_rel_error=max(max_raw_weight_rel_error,abs(lhs/rhs-1))
assert product(N,2) is None
assert max_phase_error<3e-13 and max_raw_weight_rel_error<3e-14

# The distinguished atom can be expressed as the least-cost prime generator.
# This is a structural formulation of the adopted rule, not a physical proof
# that its composites must own the D-sector.
primes=base['n'][struct_prime]
minimum_cost_prime=int(primes[np.argmin(cost[primes])])
assert minimum_cost_prime==2
alternative_anchor_rows=[]
for anchor in (2,3,5):
    comp=omega[2:]>=2
    dark=comp&(base['n']%anchor==0);eligible=comp&(~dark)
    alt_effect=structural_effect(cost[2:],struct_prime,dark,eligible)
    alt_shares=alt_effect@w;alt_mu=(alt_effect*g*w[None,:]).sum(axis=1)
    assert np.all(alt_effect>=0) and abs(alt_shares.sum()-1)<1e-12
    alternative_anchor_rows.append({'distinguished_prime':anchor,
        'generator_cost':float(cost[anchor]),'shares':alt_shares.tolist(),
        'present_q':adapter['macro'](alt_mu)['rows'][1]['q'],
        'status':'adopted minimum-cost rule' if anchor==2 else 'changed structural readout law'})
assert np.allclose(alternative_anchor_rows[0]['shares'],shares,rtol=0,atol=2e-13)

# Passive reorder: transported attributes keep their state ownership.
permutation_rows=[]
for seed in (7,105,20261008):
    perm=np.random.default_rng(seed).permutation(N-1)
    transported_shares=effect[:,perm]@w[perm]
    transported_mu=(effect[:,perm]*g[:,perm]*w[perm][None,:]).sum(axis=1)
    sh_error=float(np.max(np.abs(transported_shares-shares)))
    mu_error=float(np.max(np.abs(transported_mu-mu)))
    assert sh_error<3e-13 and mu_error<3e-13
    out=adapter['macro'](transported_mu)
    permutation_rows.append({'seed':seed,'shares_max_abs_error':sh_error,
        'load_max_abs_error':mu_error,'present_q':out['rows'][1]['q'],
        'present_rotation_km_s':out['rows'][1]['rotation_km_s'],
        'present_lensing_arcsec':out['rows'][1]['lensing_arcsec']})
    # Re-encode the product relation as well, not just numerical outputs.
    inv=np.empty_like(perm);inv[perm]=np.arange(N-1)
    def display(n):return int(inv[n-2])+2 if n>1 else 1
    def intrinsic(label):return int(perm[label-2])+2 if label>1 else 1
    for a,b in ((3,5),(5,7),(9,25),(11,13),(2,4),(105,3)):
        la,lb=display(a),display(b)
        lc=display(product(intrinsic(la),intrinsic(lb)))
        assert intrinsic(lc)==a*b

# Explicitly test all six coordinate serialization orders of the SOURCE.
dimensions=(500,29,70);q0=base['n']-1
coords=(q0%500,(q0//500)%29,q0//(500*29))
tuple_order_rows=[]
for order in itertools.permutations(range(3)):
    i,j,k=order
    new_label=1+coords[i]+dimensions[i]*(coords[j]+dimensions[j]*coords[k])
    # Zero tuple stays reference 1; active labels are a permutation of 2..N.
    assert new_label.min()==2 and new_label.max()==N
    label_order=np.argsort(new_label)
    assert np.array_equal(new_label[label_order],base['n'])
    sorted_shares=effect[:,label_order]@w[label_order]
    sorted_mu=(effect[:,label_order]*g[:,label_order]*w[label_order][None,:]).sum(axis=1)
    assert np.allclose(sorted_shares,shares,rtol=0,atol=3e-13)
    assert np.allclose(sorted_mu,mu,rtol=0,atol=3e-13)
    tuple_order_rows.append({'fastest_to_slowest':['l','h','z'][i]+','+['l','h','z'][j]+','+['l','h','z'][k],
        'shares_max_abs_error':float(np.max(np.abs(sorted_shares-shares))),
        'load_max_abs_error':float(np.max(np.abs(sorted_mu-mu)))})

# Active reassignment control: attach new numeric predicates to unchanged states.
# This changes the structure/readout law; it is not passive relabelling.
controls=[]
for pair in ((2,4),(9,11)):
    permutation=np.arange(N-1);i,j=pair[0]-2,pair[1]-2
    permutation[i],permutation[j]=permutation[j],permutation[i]
    reassigned=effect[:,permutation]
    output=reassigned@w
    assert abs(output.sum()-1)<1e-12
    assert np.max(np.abs(output-shares))>1e-5
    # Here cost and measure remain fixed and only the filter effect is reassigned.
    changed_mu=(reassigned*g*w[None,:]).sum(axis=1)
    controls.append({'swapped_readout_labels':list(pair),'shares':output.tolist(),
                     'delta_shares':(output-shares).tolist(),
                     'present_q':adapter['macro'](changed_mu)['rows'][1]['q']})

sample_addresses=(1,2,4,9,11,15,25,105,1001)
samples=[]
for n in sample_addresses:
    samples.append({'intrinsic_address':n,'factors':factors(n),'Omega':int(omega[n]),
      'v2':int(v2[n]),'cost':float(cost[n]),
      'type':'inactive_unit' if n==1 else ('prime_atom' if omega[n]==1 else
             ('composite_with_minimum_prime' if v2[n] else 'composite_without_minimum_prime'))})

checks={'factor_coordinates_match_all_existing_classifier_masks':True,
 'factor_cost_matches_log_address':cost_error<2e-14,
 'factor_phase_drive_matches_existing_filter':bool(np.allclose(effect,reference_effect,rtol=0,atol=2e-13)),
 'factor_cost_weights_match_existing_measure':bool(np.allclose(w,base['w'],rtol=3e-14,atol=1e-16)),
 'factor_readout_reproduces_frozen_shares':bool(np.allclose(shares,reference_shares,rtol=0,atol=2e-13)),
 'factor_readout_reproduces_frozen_loads':bool(np.allclose(mu,reference_mu,rtol=0,atol=2e-13)),
 'sampled_products_add_factor_counts':True,
 'prime_factors_compose_phase':max_phase_error<3e-13,
 'unnormalized_weights_multiply':max_raw_weight_rel_error<3e-14,
 'passive_permutations_preserve_outputs':all(x['shares_max_abs_error']<3e-13 and x['load_max_abs_error']<3e-13 for x in permutation_rows),
 'transported_product_relations_preserved':True,
 'classifier_reassignment_detectably_changes_model':all(max(abs(x) for x in r['delta_shares'])>1e-5 for r in controls),
 'out_of_domain_product_rejected':product(N,2) is None}
checks['all_six_SOURCE_serializations_preserve_transport']=all(r['shares_max_abs_error']<3e-13 and r['load_max_abs_error']<3e-13 for r in tuple_order_rows)
checks['minimum_cost_prime_is_original_parity_anchor']=minimum_cost_prime==2
checks['all_reference_parameters_unchanged']=frozen_input_hash==adapter['fingerprint']({'cfg':cfg,'params':params,'calibration':adapter['calibration']})
result={'status':'PASS' if all(checks.values()) else 'FAIL','date':'2026-10-08',
 'scope':'structural arithmetic formulation and passive coordinate invariance of the frozen conditional model',
 'N':N,'shares':shares.tolist(),'address_moments':mu.tolist(),'reference_macro':reference_macro,
 'factorization_samples':samples,'passive_permutation_tests':permutation_rows,
 'SOURCE_coordinate_order_tests':tuple_order_rows,
 'alternative_distinguished_prime_probes':alternative_anchor_rows,
 'active_classifier_reassignment_controls':controls,'max_cost_error':cost_error,
 'max_factor_phase_error':max_phase_error,'max_raw_weight_relative_error':max_raw_weight_rel_error,
 'checks':checks,'dependency_provenance':dep,'frozen_input_hash':frozen_input_hash,
 'retained_assumptions':['arithmetic composition law is part of SOURCE model',
    'minimum-prime-containing composites use the D-sector readout',
    'composites without that prime are eligible for phenotype admission',
    'phase admission law and gamma spectrum are inherited calibrated rules'],
 'not_claimed':['a physical derivation of the selected arithmetic LAW',
               'derived particle identity from primality','all address labels have measurable spatial positions',
               'unnormalized product weights multiply after normalization without the Z factor']}
assert all(checks.values())
(ROOT/'address_structure_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({'status':result['status'],'shares':result['shares'],'permutations':permutation_rows,
                  'reassignment_controls':controls,'cost_error':cost_error,'checks':checks},ensure_ascii=False,indent=2))
