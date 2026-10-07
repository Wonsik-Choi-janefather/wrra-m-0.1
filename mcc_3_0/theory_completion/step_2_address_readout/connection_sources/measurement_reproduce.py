"""Replay the frozen WRRA bridge, then calculate one mean measurement ledger.

Run: python reproduce.py --out replay
The included original archive is unchanged. The case does not fit new parameters.
"""
from pathlib import Path
import argparse, csv, hashlib, json, math, os, shutil, subprocess, sys, zipfile
import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent

def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def dump(p, obj):
    Path(p).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def replay(out, config):
    archive = ROOT / config['source_archive']
    if sha(archive) != config['source_archive_sha256']:
        raise ValueError('Frozen source archive hash mismatch')
    source = out / 'original_source'
    source.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for n in z.namelist():
            if not (source / n).resolve().is_relative_to(source.resolve()):
                raise ValueError('Unsafe archive member')
        z.extractall(source)
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    env.pop('WRRA_REPO', None)
    stages = {}
    for k in (2, 3, 5, 6):
        stage = source / 'studies' / f'bridge_0_{k}'
        previous = source / 'studies' / 'bridge_0_2'
        if k == 3:
            shutil.copy2(previous / 'results.json', stage / 'source/bridge_0_2_results.json')
        if k == 5:
            shutil.copy2(previous / 'results.json', stage / 'source/bridge_0_2_results.json')
            shutil.copy2(previous / 'internal_and_carrier_basis.npz', stage / 'source/internal_and_carrier_basis.npz')
        if k == 6:
            shutil.copy2(previous / 'results.json', stage / 'source/state_0_2.json')
            shutil.copy2(previous / 'internal_and_carrier_basis.npz', stage / 'source/internal_and_carrier_basis.npz')
            shutil.copy2(source / 'studies/bridge_0_5/results.json', stage / 'source/clock_0_5.json')
        proc = subprocess.run([sys.executable, str(stage / f'compute_0_{k}.py')], cwd=stage, env=env,
                              capture_output=True, text=True)
        (out / f'original_stage_0_{k}.log').write_text(proc.stdout + proc.stderr, encoding='utf-8')
        if proc.returncode:
            raise RuntimeError(f'Original stage 0.{k} failed; see its log')
        result = read(stage / 'results.json')
        stages[str(k)] = {'passed': result['passed'], 'failed': result['failed']}
        if result['failed']:
            raise RuntimeError(f'Original stage 0.{k} contract failure')
        print(f'Original stage 0.{k}: {result["passed"]} passed, 0 failed', flush=True)
    return source, stages

def validate_case_selection(config):
    expected = {'calibration':'inherited','species':'proton','reference_volume_m3':1,
                'energy_fractions':{'phi':0.0493,'D':0.265,'R':0.6857},
                'supplier_initial_fraction_of_phi':0.2,'preparation_strength':0.2,
                'selector_prime':3,'excited_mode_index':1}
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f'{key} is not the supported frozen case selection')

def compute(source, out, config, stages):
    s = source / 'studies'
    a, ledger, clock, measure = [read(s / f'bridge_0_{k}/results.json') for k in (2, 3, 5, 6)]
    b = next(r for r in a['rows'] if r['case'] == 'baseline')
    ref = next(r for r in ledger['rows'] if r['calibration'] == 'inherited' and r['species'] == 'proton' and r['case'] == 'baseline')
    inputs = read(s / 'bridge_0_2/wrra-m/upstream/residue_current_v0_9/inputs.json')
    handoff = read(s / 'bridge_0_2/wrra-m/upstream/shutter_v0_8/handoff.json')
    basis = np.load(s / 'bridge_0_2/internal_and_carrier_basis.npz')
    B = np.column_stack([basis['ground'], basis['excited']])
    H = basis['H_MeV']; Hp = B.conj().T @ H @ B
    gap = float((Hp[1, 1] - Hp[0, 0]).real)
    conv = ledger['unit_conversion_MeV_to_J']; gapJ = gap * conv
    p = b['excited_population']; n = ref['expected_population_input']
    hb = clock['calibration']['hbar_J_s']; dt = clock['calibration']['chosen_frame_duration_s']
    record_gap = measure['record_gap_J']
    I = np.eye(2); X = np.array([[0., 1.], [1., 0.]])
    vp = np.array([1., 1.]) / math.sqrt(2); vm = np.array([1., -1.]) / math.sqrt(2)
    P = [np.outer(vp, vp), np.outer(vm, vm)]
    rho = np.diag([1-p, p]); blank = np.diag([1., 0.])
    Hs = np.diag([0., gapJ]); Hr = np.diag([0., record_gap])
    W = np.kron(P[0], I) + np.kron(P[1], X)
    j0 = np.kron(rho, blank); j1 = W @ j0 @ W.conj().T
    ht = np.kron(Hs, I) + np.kron(I, Hr)
    work = float(np.trace((j1-j0) @ ht).real)
    dsys = n * (0.5-p) * gapJ; drecord = n * record_gap / 2; supply = n * work
    E0 = ref['system_energy_J']; reservoir0 = ref['environment_initial_J']
    E1 = E0 + supply; reservoir1 = reservoir0 - supply
    ED = E0 * config['energy_fractions']['D']; ER = E0 * config['energy_fractions']['R']
    V0 = config['reference_volume_m3']; pressure = -ER/V0
    def q(E): return 0.5 * (1 + 3 * pressure / (E/V0))
    checks = []
    def ck(name, ok): checks.append({'name': name, 'passed': bool(ok)})
    def close(x, y, r=2e-10, at=1e-25): return math.isclose(float(x), float(y), rel_tol=r, abs_tol=at)
    ck('address state input strength preserved', close(p, inputs['reference_preparation_strength']*b['selector_fraction']))
    ck('inherited state source Hermitian and invariant', np.linalg.norm(H@B-B@Hp)/np.linalg.norm(H)<1e-12)
    ck('original excitation transferred', abs(p*gap-b['conditional_excitation_MeV'])<2e-8)
    ck('rest and excitation replace phenotype allocation once', close(ref['rest_total_J']+ref['excitation_total_J'], ref['reference_phi_allocation_J']))
    ck('initial density benchmark preserved', close(E0, ledger['ucrit_J_m3']*V0))
    ck('X instrument complete and W unitary', np.linalg.norm(P[0]+P[1]-I)<1e-12 and np.linalg.norm(W.conj().T@W-np.eye(4))<1e-12)
    ck('joint write state positive and normalized', np.linalg.eigvalsh(j1).min()>-1e-12 and abs(np.trace(j1)-1)<1e-12)
    ck('energy computed from write state agrees with inherited measurement', close(work, measure['write_work_J']))
    ck('system and record increments cover supply exactly', close(dsys+drecord, supply))
    ck('mean supplier balance closes', close(E0+reservoir0, E1+reservoir1))
    ck('finite mean supplier remains nonnegative', reservoir1>=0)
    ck('individual conditional controller covers both outcomes', measure['finite_controller_initial_energy_J']>=max(x['conditional_controller_work_J'] for x in measure['outcomes']))
    branch_supply = []
    for bit in (0, 1):
        Q = np.kron(I, np.diag([1., 0.]) if bit == 0 else np.diag([0., 1.]))
        prob = float(np.trace(Q@j1).real)
        cj = Q@j1@Q/prob
        branch_supply.append(n*float(np.trace((cj-j0)@ht).real))
        ck(f'outcome {bit} Born probability', close(prob, .5, at=1e-12))
    ck('both mean boundary branch allocations covered', reservoir0>=max(branch_supply))
    weights = [b['four_branch_probabilities']['phi']/2]*2 + [b['four_branch_probabilities'][x] for x in ('D','initial_reflection','normal_return')]
    ck('full source routing complete', close(sum(weights),1.,at=2e-11))
    M = E0-ER
    def energy_at_volume(v, extra=0): return M+extra+ER*v/V0
    eps = 1e-3*V0
    fd = -(energy_at_volume(V0+eps,supply)-energy_at_volume(V0-eps,supply))/(2*eps)
    ck('pressure equals negative volume derivative after readout', close(fd,pressure,r=1e-9))
    ck('included pressureless supplier q unchanged', close(q(E0+reservoir0),q(E1+reservoir1)))
    repeat = []
    for k in (1, 2, 4):
        U = expm(-1j*Hs*k*dt/hb)
        analytic = math.cos(gapJ*k*dt/(2*hb))**2
        matrix = float(np.trace(P[0]@U@P[0]@U.conj().T).real)
        archived = next(x['same_probability'] for x in measure['repeated_readout'] if x['frame_separation']==k)
        ck(f'repeated k{k} analytic and matrix prediction', abs(analytic-matrix)<1e-10 and abs(analytic-archived)<1e-9)
        repeat.append({'frames':k,'proper_time_s':k*dt,'same_outcome_probability':analytic})
    phase = next(r for r in a['rows'] if r['case']=='p3_phase')
    ck('phase control leaves address-dephased state energy unchanged', abs(phase['conditional_excitation_MeV']-b['conditional_excitation_MeV'])<1e-9)
    ck('doubling the clock interval changes repeated probability', abs(repeat[0]['same_outcome_probability']-repeat[1]['same_outcome_probability'])>.5)
    # The original exchange rule is executed for an intentionally insufficient supply.
    exhausted_rejected = False
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location('original_exchange', s/'bridge_0_3/compute_0_3.py')
        mod = importlib.util.module_from_spec(spec)
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(mod)
        mod.exchange(E0, supply/2, supply)
    except ValueError:
        exhausted_rejected = True
    ck('original exchange rejects insufficient mean supply', exhausted_rejected)
    ck('naive duplicate phenotype allocation identified', close(E0+ref['rest_total_J']+ref['excitation_total_J']-E0, ref['reference_phi_allocation_J']))
    reference = read(ROOT/'reference_boundary.json')
    vals = {'expected_population_input':n,'system_excitation_increase_J':dsys,'record_energy_increase_J':drecord,
            'controller_supply_J':supply,'reservoir_before_J':reservoir0,'reservoir_after_J':reservoir1,
            'external_q_before':q(E0),'external_q_after':q(E1),'included_pressureless_q':q(E0+reservoir0)}
    ck('case agrees with published integrated boundary diagnostic', all(close(v, reference[k], at=1e-23 if k.endswith('_J') else 1e-11) for k,v in vals.items()))
    result = {'case':'WRRA M integrated single measurement v1.0','date':'2026-10-05',
      'authors':['Wonsik Choi','Jeongin Choi'],'principal_reference_doi':config['principal_reference_doi'],
      'interpretation':'Conditional expected-occupancy ledger at V0; not a realized fractional proton or a time-resolved cosmological run.',
      'address':{'N':handoff['N'],'alpha':handoff['alpha'],'beta':handoff['beta'],'selector_fraction':b['selector_fraction'],'excited_population':p,'routes':weights},
      'state':{'gap_MeV':gap,'conditional_excitation_MeV':b['conditional_excitation_MeV'],'rest_energy_per_particle_J':ref['rest_energy_per_particle_J'],'expected_occupancy':n,'rest_total_J':ref['rest_total_J'],'excitation_total_J':ref['excitation_total_J']},
      'measurement':{'outcomes':[.5,.5],'record_gap_J':record_gap,'write_work_per_conditioned_particle_J':work,'individual_controller_initial_J':measure['finite_controller_initial_energy_J'],'individual_controller_after_mean_write_J':measure['finite_controller_initial_energy_J']-work,'mean_branch_supplier_allocations_J':branch_supply},
      'boundary':dict(vals, system_before_J=E0,system_after_J=E1,pressure_Pa=pressure,initial_included_total_J=E0+reservoir0,after_included_total_J=E1+reservoir1),
      'clock':dict(clock['calibration'],repeated_readout=repeat),
      'controls':{'phase_energy_change_MeV':phase['conditional_excitation_MeV']-b['conditional_excitation_MeV'],'doubled_interval_probability_change':repeat[1]['same_outcome_probability']-repeat[0]['same_outcome_probability'],'half_supply_rejected':exhausted_rejected},
      'original_stage_checks':stages,'case_contracts':{'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks)},
      'provenance':config,'source_results_sha256':{str(k):sha(s/f'bridge_0_{k}/results.json') for k in (2,3,5,6)}}
    dump(out/'results.json',result)
    dump(out/'check_report.json',checks)
    with (out/'energy_ledger.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['item','before_J','after_J'])
        w.writerows([['rest',ref['rest_total_J'],ref['rest_total_J']],['excitation',ref['excitation_total_J'],ref['excitation_total_J']+dsys],['record',0,drecord],['D',ED,ED],['R',ER,ER],['external_system',E0,E1],['supplier',reservoir0,reservoir1],['included_total',E0+reservoir0,E1+reservoir1]])
    with (out/'route_ledger.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['route','probability']);w.writerows(zip(['phi_plus','phi_minus','D','initial_reflection','normal_return'],weights))
    print(json.dumps({'original_checks':sum(v['passed'] for v in stages.values()),'case_contracts':result['case_contracts'],'boundary':result['boundary']},indent=2))
    if result['case_contracts']['failed']:
        raise SystemExit('Case contract failure; inspect check_report.json')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,default=Path('replay'))
    ap.add_argument('--source-dir',type=Path,help='Use an already freshly replayed source tree for local analysis')
    args=ap.parse_args();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    config=read(ROOT/'inputs.json')
    validate_case_selection(config)
    if args.source_dir:
        source=args.source_dir.resolve()
        stages={str(k):{key:read(source/f'studies/bridge_0_{k}/results.json')[key] for key in ('passed','failed')} for k in (2,3,5,6)}
    else:
        source,stages=replay(out,config)
    compute(source,out,config,stages)
