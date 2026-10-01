"""Independent arithmetic, transport, routing and frozen-baseline checks."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction
import json
import math
import sys
import numpy as np
import mpmath as mp
import compute as m

ROOT = Path(__file__).resolve().parent


def close(a, b, tol=2e-12):
    return bool(np.allclose(a, b, atol=tol, rtol=0))


def run():
    cfg = json.loads((ROOT/'parameters.json').read_text()); out = ROOT/'results'
    result = m.run(cfg, out); base = m.address_base(cfg); E = m.effects(cfg, base)
    checks = []; evidence = {}
    def check(name, passed, detail):
        checks.append({'id':len(checks)+1, 'check':name, 'passed':bool(passed), 'evidence':detail})
        if not passed: raise AssertionError(name+': '+str(detail))
    t = result['terminal_common_arithmetic_ledger']; u = cfg['upstream']
    check('reference_three_sector_calibration', close(list(t.values()), [u['targets'][s] for s in m.SECTORS], 1e-10), t)
    check('per_address_positive_complete_effects', E.min() >= 0 and E.max() <= 1 and close(E.sum(axis=0), 1),
          {'minimum':float(E.min()), 'maximum':float(E.max()), 'max_sum_error':float(abs(E.sum(axis=0)-1).max())})
    # Trial division is independent of the production smallest-factor sieve.
    test_cfg = deepcopy(cfg); test_cfg['upstream']['address_cutoff_N'] = 300
    small = m.address_base(test_cfg)
    trial = np.array([all(n%d for d in range(2, math.isqrt(int(n))+1)) for n in small['n']])
    check('independent_arithmetic_classification', np.array_equal(small['prime'], trial) and
          np.all(small['n']%small['spf'] == 0), {'addresses_checked':299})
    source = m.module('upper_frames_independent', ROOT/'references/upper_frames/compute.py')
    old_compute = sys.modules['compute']
    try:
        sys.modules['compute'] = m.module('upper_scalar_sieve', ROOT/'references/upper_scalar/compute.py')
        scalar_source = m.module('upper_scalar_independent', ROOT/'references/upper_scalar/partition_26_8.py')
    finally: sys.modules['compute'] = old_compute
    scalar = scalar_source.sectors(u['address_cutoff_N'], u['state']['alpha'], u['scalar_comparison']['odd_composite_admission_beta'])
    check('frozen_upstream_scalar_source_reproduction', close([result['scalar_comparison_ledger'][s] for s in m.SECTORS],
          [scalar['phenotype_fraction'], scalar['unexpressed_Actual_fraction'], scalar['source_return_fraction']]),
          {'independent_upstream_ledger_sum':scalar['ledger_sum']})
    upper = json.loads((ROOT/'references/upper_frames/results.json').read_text())
    check('frozen_upstream_phase_source_reproduction', close([t[s] for s in m.SECTORS],
          [upper['terminal']['phenotype'], upper['terminal']['nonphenotypic_Actual'], upper['terminal']['return']]), upper['terminal'])
    gamma = np.asarray(u['spectrum']['gamma'])
    residuals = []
    with mp.workdps(40):
        for i, value in enumerate(gamma, 1): residuals.append(abs(float(mp.im(mp.zetazero(i)))-value))
    em = [abs(source.zeta_euler_maclaurin(.5+1j*g)) for g in gamma]
    check('adopted_zero_heights_independent_validation', max(residuals) < 1e-13 and max(em) < 1e-11,
          {'high_precision_height_max_error':max(residuals), 'Euler_Maclaurin_max_residual':float(max(em))})
    d = m.phase_drive(cfg, base['n'][base['odd']]); cumulative = 1-np.prod(1-expit(d-u['update']['sigmoid_threshold_h']), axis=0)
    product_error = float(abs(cumulative-E[0,base['odd']]).max())
    check('stable_log_product_vs_direct_survival_product', product_error < 2e-14, {'maximum_error':product_error})
    frames = result['frame_transport']; last = frames[-1]
    check('every_frame_four_sector_conservation', all(abs(r['ledger_sum']-1) < 2e-12 for r in frames),
          {'frames_checked':len(frames), 'maximum_sum_error':max(abs(r['ledger_sum']-1) for r in frames)})
    check('depleted_reservoir_birth_vs_terminal_effect', close([last[s] for s in m.SECTORS], [t[s] for s in m.SECTORS]),
          {'sum_of_new_births':sum(r['new_phenotype'] for r in frames)})
    K = u['update']['admission_frames_K']
    check('pending_SOURCE_and_return_are_separate', all(r['return']==0 for r in frames if r['frame']<K) and
          all(r['source_pending']==0 for r in frames if r['frame']>=K), {'recovery_frame':K})
    check('resident_retention_under_declared_identity_boundary', all(close([r[s] for s in m.SECTORS], [t[s] for s in m.SECTORS])
          for r in frames if r['frame']>=K), {'post_recovery_dynamics':'identity; microscopic origin deferred'})
    scopes = result['scope_rows']; resident = result['upstream_resident_Actual']
    check('Actual_denominators_explicit', abs(resident-.318)<1e-10 and abs(result['complete_current_Actual']-1)<2e-12 and
          close([scopes[1]['phenotype'], scopes[1]['resident_nonphenotype']], [.05/.318,.268/.318], 1e-10), scopes)
    check('different_exponents_never_added', close([r['alpha'] for r in result['separate_exponent_comparisons']], [2,1.9]) and
          all(abs(r['full_odd_composite_share']+r['even_composite_share']+r['prime_share']-1)<2e-12
              for r in result['separate_exponent_comparisons']), result['separate_exponent_comparisons'])
    baseline = json.loads((out/'baseline_0_8/results.json').read_text())
    frozen = json.loads((ROOT.parent/'wrra_m_0_8/results/results.json').read_text())
    check('all_nine_frozen_0_8_cases_and_charges_unchanged', baseline == frozen, {'case_count':len(baseline['cases']), 'entire_result_equal':baseline==frozen})
    reference = next(v for v in baseline['cases'] if v['case_name']=='uniform_a1.0')
    inventory = result['channel_inventory']; total = sum(v['arithmetic_phenotype_weight'] for v in inventory)
    check('reference_48_channel_routing_preserves_phenotype', abs(total-t['phenotype'])<2e-12 and len(inventory)==48,
          {'channels':len(inventory), 'phenotype_sum':total, 'SM_components':45, 'conditional_neutral_slots':3})
    different = deepcopy(cfg); weights = np.arange(1,17,dtype=float); weights /= weights.sum()
    different['channel_coupling']['odd_smallest_prime_overrides']={'3':weights.tolist()}
    different['channel_coupling']['family_weights']=[.1,.2,.7]
    m.validate(different); routed = m.channel_join(different, base, E, reference)
    changed = max(abs(a['arithmetic_phenotype_weight']-b['arithmetic_phenotype_weight']) for a,b in zip(routed, inventory))
    check('nonuniform_conditional_address_and_family_kernel', abs(sum(v['arithmetic_phenotype_weight'] for v in routed)-total)<2e-12 and changed>1e-4 and
          all(a['Q']==b['Q'] and a['Y']==b['Y'] for a,b in zip(routed,inventory)), {'maximum_channel_change':changed, 'charge_table_preserved':True})
    zero = deepcopy(cfg); zero['channel_coupling']['default_origin_weights']=[1.0]+[0.0]*15
    one_channel = m.channel_join(zero, base, E, reference)
    check('zero_support_and_no_channel_family_multiplicity', abs(sum(r['arithmetic_phenotype_weight'] for r in one_channel)-total)<2e-12 and
          sum(r['arithmetic_phenotype_weight']>0 for r in one_channel)==3, {'occupied_reference_slots':3, 'total_weight':sum(r['arithmetic_phenotype_weight'] for r in one_channel)})
    rng = np.random.default_rng(909); p = rng.random(299); p /= p.sum()
    arbitrary = m.address_base(test_cfg, p); e = m.effects(test_cfg, arbitrary)
    check('arbitrary_normalized_diagonal_state_transport', abs(sum(m.shares(e,p).values())-1)<2e-12 and e.min()>=0,
          {'seed':909, 'state_size':299, 'scope':'explicit diagonal state API; calibrated fractions are reference-state dependent'})
    # Diagonal address effects are tested on coherent small density matrices too.
    a = rng.normal(size=(20,20))+1j*rng.normal(size=(20,20)); rho = a@a.conj().T; rho /= np.trace(rho)
    et = e[:,:20]; outputs = [np.diag(np.sqrt(v))@rho@np.diag(np.sqrt(v)) for v in et]
    check('positive_effect_extension_on_coherent_test_state', all(np.linalg.eigvalsh(v).min()>-1e-13 for v in outputs) and
          abs(sum(np.trace(v) for v in outputs)-1)<2e-12, {'dimension':20, 'scope':'mathematical effect positivity; no physical outcome selection or Born claim'})
    refit = m.calibrate(cfg, base)
    check('explicit_arithmetic_refit_and_derived_beta', close([refit['alpha'],refit['threshold_h'],refit['derived_effective_beta']],
          [u['state']['alpha'],u['update']['sigmoid_threshold_h'],result['derived_effective_beta']], 2e-10), refit)
    sensitivity = []
    for Knew in (4,16):
        c = deepcopy(cfg); c['upstream']['update']['admission_frames_K']=Knew
        sensitivity.append(m.shares(m.effects(c,base),base['w'])['phenotype'])
    check('frozen_recovery_boundary_changes_output', sensitivity[0] < .05 < sensitivity[1], {'K4':sensitivity[0], 'K16':sensitivity[1]})
    c = deepcopy(cfg); c['upstream']['update']['phase_step_xi']=0
    fitted = m.calibrate(c,base); c['upstream']['update']['sigmoid_threshold_h']=fitted['threshold_h']
    alternative = m.effects(c,base); diff = float(np.dot(base['w'],abs(alternative[0]-E[0])))
    check('same_totals_do_not_identify_microscopic_address_rule', abs(m.shares(alternative,base['w'])['phenotype']-.05)<1e-10 and diff>.001,
          {'weighted_address_difference':diff,'explicitly_refitted_static_threshold':fitted['threshold_h']})
    cut = deepcopy(cfg); cut['upstream']['address_cutoff_N']=10000
    cutbase = m.address_base(cut); cutshares = m.shares(m.effects(cut,cutbase),cutbase['w'])
    oldphys = result['inherited_physical_reference_0_8']
    check('address_zero_and_carrier_cutoffs_separate', result['cutoffs']=={'address_N':1000000,'zero_J':4,'carrier_lattice_N':128,'physical_capacity_bits':None} and
          cfg['baseline_0_8']['ledger_0_7']['carrier_and_background']['lattice_N']==128 and abs(cutshares['phenotype']-.05)>1e-5,
          {'cutoffs':result['cutoffs'], 'N10000_frozen_shares':cutshares})
    check('physical_fraction_and_pressure_boundary_preserved', close(list(oldphys.values()),[.0493,.265,.6857]) and
          result['physical_bridge']['energy_map'] is None and result['physical_bridge']['pressure_map'] is None,
          {'old_physical_fractions':oldphys, 'new_arithmetic_fractions':t, 'energy_and_pressure_map':'pending 0.10'})
    mutations = []
    def mutated(field,value):
        c = deepcopy(cfg); obj=c
        for key in field[:-1]:obj=obj[key]
        obj[field[-1]]=value; mutations.append(c)
    for field,value in [(['upstream','address_cutoff_N'],True),(['upstream','state','alpha'],float('nan')),
        (['upstream','spectrum','gamma'],[1]),(['upstream','spectrum','J_zero'],0),
        (['upstream','update','admission_frames_K'],0),(['upstream','update','frame_unit'],'seconds'),
        (['upstream','update','phase_step_xi'],-1),(['upstream','scalar_comparison','odd_composite_admission_beta'],1.1),
        (['channel_coupling','default_origin_weights'],[1]*16),(['channel_coupling','family_weights'],[1,1,1]),
        (['channel_coupling','odd_smallest_prime_overrides'],{'9':[.0625]*16}),
        (['physical_bridge','energy_map'],1),(['physical_bridge','pressure_map'],.682),
        (['measurement_events'],[{'outcome':1}]),(['physical_records'],[{'bit':1}]),
        (['upstream','sample_addresses'],[1000001])]:mutated(field,value)
    rejected=0
    for c in mutations:
        try:m.validate(c)
        except (ValueError,TypeError):rejected+=1
    check('invalid_inputs_and_unimplemented_physical_claims_rejected', rejected==len(mutations), {'rejected_cases':rejected})
    check('source_hashes_and_single_input_immutability', m.digest(cfg)==result['input_hash_sha256'] and
          len(cfg['provenance']['source_files_sha256'])==5, {'input_hash_sha256':m.digest(cfg),'source_snapshots':5})
    # Exhaustive sparse overrides formerly left negative cancellation residuals.
    sparse_cfg=deepcopy(test_cfg)
    sparse_cfg['channel_coupling']['odd_smallest_prime_overrides']={
        str(p):[1.0]+[0.0]*15 for p in np.unique(small['spf'][small['odd']])}
    sparse_cfg['upstream']['sample_addresses']=[9]
    m.validate(sparse_cfg)
    sparse_effect=m.effects(sparse_cfg,small); sparse_rng=np.random.default_rng(9)
    min_weight=0.; max_error=0.
    for i in range(20):
        w=sparse_rng.random(len(small['w']))*small['odd']; w/=w.sum()
        sparse_base=dict(small,w=w)
        rows=m.channel_join(sparse_cfg,sparse_base,sparse_effect,reference)
        min_weight=min(min_weight,min(r['arithmetic_phenotype_weight'] for r in rows))
        max_error=max(max_error,abs(sum(r['arithmetic_phenotype_weight'] for r in rows)-
                                  m.shares(sparse_effect,w)['phenotype']))
        assert sum(r['arithmetic_phenotype_weight']>0 for r in rows)==3
    check('exhaustive_sparse_overrides_preserve_positive_channel_budget',
          min_weight>=0 and max_error<2e-12,
          {'cases':20,'seed':9,'minimum_weight':min_weight,'maximum_partition_error':max_error})
    report={'version':'WRRA-M 0.9','passed':all(c['passed'] for c in checks),'check_count':len(checks),
            'input_hash_sha256':m.digest(cfg),'checks':checks}
    (out/'verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    print(json.dumps({'version':report['version'],'passed':report['passed'],'check_count':len(checks),'common_ledger':t}))
    return report


from scipy.special import expit
if __name__=='__main__':run()
