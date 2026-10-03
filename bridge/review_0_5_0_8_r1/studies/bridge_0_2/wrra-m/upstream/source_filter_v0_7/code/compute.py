"""WRRA M upstream 0.7 SOURCE preparation and ordered two-filter ledger.

Prime intensity/phase variables generate relation amplitudes multiplicatively.
The finite address weights are information stock, without energy or time units.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
TOL = 2e-11


def finite(x, name):
    if isinstance(x, (bool, str)) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(name + ' must be a finite real number')
    return float(x)


def integer(x, name, low, high):
    if type(x) is not int or not low <= x <= high:
        raise ValueError(f'{name} must be an integer in [{low}, {high}]')
    return x


def is_prime(p):
    return type(p) is int and p >= 2 and all(p % d for d in range(2, math.isqrt(p) + 1))


def prime_mask(N):
    a = np.ones(N + 1, dtype=bool)
    a[:2] = False
    for p in range(2, math.isqrt(N) + 1):
        if a[p]:
            a[p*p::p] = False
    return a


def valuations(numbers, p):
    v = np.zeros(numbers.size, dtype=np.int16)
    power = p
    while power <= int(numbers[-1]):
        v += numbers % power == 0
        power *= p
    return v


def validate_controls(controls, N):
    if not isinstance(controls, dict):
        raise ValueError('SOURCE controls must be a dictionary')
    clean = {}
    for key, value in controls.items():
        if isinstance(key, str):
            if not key.isascii() or not key.isdecimal() or key != str(int(key)):
                raise ValueError('prime keys must be canonical integers')
            p = int(key)
        else:
            p = key
        if not is_prime(p) or p > N:
            raise ValueError('a controlled SOURCE address must be prime and in range')
        if p in clean:
            raise ValueError('duplicate representations of a prime SOURCE key')
        if not isinstance(value, dict) or set(value) - {'epsilon', 'phase'}:
            raise ValueError('SOURCE fields are epsilon and phase')
        e = finite(value.get('epsilon', 0.0), 'epsilon')
        phase = finite(value.get('phase', 0.0), 'phase')
        if abs(e) > 2:
            raise ValueError('the supported log intensity control range is [-2, 2]')
        clean[p] = {'epsilon': e, 'phase': phase}
    return clean


def validate(c):
    if not isinstance(c, dict):
        raise ValueError('input must be a dictionary')
    integer(c['N'], 'N', 9, 2000000)
    if finite(c['alpha'], 'alpha') <= 1:
        raise ValueError('this release requires alpha > 1')
    if not 0 <= finite(c['beta'], 'beta') <= 1:
        raise ValueError('beta must be in [0, 1]')
    primes = c['controlled_primes']
    if not isinstance(primes, list) or not primes or any(type(p) is not int for p in primes) or len(set(primes)) != len(primes):
        raise ValueError('controlled_primes must be nonempty and unique')
    for p in primes:
        if not is_prime(p) or p > c['N']:
            raise ValueError('controlled_primes contains an invalid prime')
    scan = c['log_intensity_scan']
    if not isinstance(scan, list) or not scan or any(abs(finite(x, 'scan')) > 2 for x in scan):
        raise ValueError('invalid intensity scan')
    h = finite(c['derivative_step'], 'derivative_step')
    if not 0 < h < 0.01:
        raise ValueError('invalid derivative step')
    integer(c['coherent_N'], 'coherent_N', 9, 256)
    pair = c['coherent_pair']
    if not isinstance(pair, list) or len(pair) != 2 or any(type(p) is not int for p in pair) or len(set(pair)) != 2:
        raise ValueError('coherent_pair must contain two distinct addresses')
    for n in pair:
        integer(n, 'coherent address', 2, c['coherent_N'])
    if not is_prime(pair[0]) or is_prime(pair[1]) or pair[1] % 2 == 0:
        raise ValueError('the coherent contrast uses a prime and an odd composite')
    finite(c['mixing_angle'], 'mixing_angle')
    if not isinstance(c['phase_scan'], list) or not c['phase_scan']:
        raise ValueError('phase_scan must be nonempty')
    for x in c['phase_scan']:
        finite(x, 'phase')
    integer(c['reference_event_count'], 'reference_event_count', 1, 128)
    integer(c['recycling_event_count'], 'recycling_event_count', 1, 10000)
    for name in ['recycling_release_fraction', 'leakage_control', 'retention_target']:
        if not 0 < finite(c[name], name) < 1:
            raise ValueError(name + ' must be in (0, 1)')
    return c


def source_state(N, alpha, controls=None):
    integer(N, 'N', 2, 2000000)
    if finite(alpha, 'alpha') <= 1:
        raise ValueError('alpha must exceed one')
    controls = validate_controls({} if controls is None else controls, N)
    n = np.arange(2, N + 1, dtype=np.int64)
    lw = -alpha * np.log(n)
    theta = np.zeros(n.size)
    for p, control in controls.items():
        vp = valuations(n, p)
        lw += control['epsilon'] * vp
        theta += math.remainder(control['phase'], 2 * math.pi) * vp
    w = np.exp(lw - lw.max())
    w /= w.sum()
    psi = np.sqrt(w) * np.exp(1j * theta)
    return n, w, psi


def effects(N, beta):
    integer(N, 'N', 2, 2000000)
    if not 0 <= finite(beta, 'beta') <= 1:
        raise ValueError('beta must lie in [0, 1]')
    n = np.arange(2, N + 1)
    prime = prime_mask(N)[2:]
    even = (~prime) & (n % 2 == 0)
    odd = (~prime) & (n % 2 == 1)
    return {'phenotype': beta * odd, 'dark': even.astype(float),
            'return': prime + (1 - beta) * odd}


def fractions(w, es):
    row = {key: float(np.sum(w * effect)) for key, effect in es.items()}
    row['Actual'] = row['phenotype'] + row['dark']
    row['sum'] = row['Actual'] + row['return']
    return row


def psd_root(a):
    a = np.asarray(a, dtype=complex)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or not np.all(np.isfinite(a)):
        raise ValueError('a finite square matrix is required')
    if np.max(np.abs(a - a.conj().T)) > TOL:
        raise ValueError('matrix must be Hermitian')
    eigenvalues, vectors = np.linalg.eigh(a)
    if eigenvalues[0] < -TOL:
        raise ValueError('matrix must be positive semidefinite')
    return (vectors * np.sqrt(np.maximum(0., eigenvalues))) @ vectors.conj().T


def instrument(rho, A, B, Qphi):
    """Ordered contraction instrument, including both return branches."""
    rho, A, B, Qphi = [np.asarray(x, dtype=complex) for x in (rho, A, B, Qphi)]
    d = rho.shape[0] if rho.ndim == 2 else 0
    if not d or any(x.shape != (d, d) for x in (rho, A, B, Qphi)):
        raise ValueError('incompatible matrix shapes')
    if any(not np.all(np.isfinite(x)) for x in (rho, A, B, Qphi)):
        raise ValueError('nonfinite instrument input')
    psd_root(rho)
    if abs(np.trace(rho) - 1) > TOL:
        raise ValueError('rho must have unit trace')
    I = np.eye(d)
    L = psd_root(I - A.conj().T @ A)
    C = psd_root(I - B.conj().T @ B)
    F = psd_root(Qphi)
    D = psd_root(I - Qphi)
    ks = {'initial_reflection': L, 'normal_return': B @ A,
          'phenotype': F @ C @ A, 'dark': D @ C @ A}
    states = {key: k @ rho @ k.conj().T for key, k in ks.items()}
    vals = {key: float(np.trace(s).real) for key, s in states.items()}
    vals['return'] = vals['initial_reflection'] + vals['normal_return']
    vals['Actual'] = vals['phenotype'] + vals['dark']
    vals['sum'] = vals['return'] + vals['Actual']
    vals['completeness_error'] = float(np.max(np.abs(sum(k.conj().T @ k for k in ks.values()) - I)))
    vals['minimum_branch_eigenvalue'] = min(float(np.linalg.eigvalsh((s+s.conj().T)/2)[0]) for s in states.values())
    return vals, states, ks


def coherent_case(c, phase, coherence, angle):
    phase, coherence, angle = [finite(x, name) for x, name in ((phase, 'phase'), (coherence, 'coherence'), (angle, 'angle'))]
    if not 0 <= coherence <= 1:
        raise ValueError('coherence must be in [0, 1]')
    N, beta = c['coherent_N'], c['beta']
    pair = c['coherent_pair']
    n, w, psi = source_state(N, c['alpha'], {pair[0]: {'phase': phase}})
    rho = coherence * np.outer(psi, psi.conj()) + (1 - coherence) * np.diag(w)
    prime = prime_mask(N)[2:]
    odd = (~prime) & (n % 2 == 1)
    diagonal = np.ones(len(n)); diagonal[odd] = np.sqrt(beta)
    U = np.eye(len(n), dtype=complex)
    i, j = pair[0] - 2, pair[1] - 2
    U[i, i] = U[j, j] = np.cos(angle)
    U[i, j], U[j, i] = -np.sin(angle), np.sin(angle)
    A, B, Q = np.diag(diagonal) @ U, np.diag(prime.astype(float)), np.diag(odd.astype(float))
    values, states, ks = instrument(rho, A, B, Q)
    values.update({'N': N, 'phase': phase, 'coherence': coherence, 'mixing_angle': angle,
                   'commutator_AB_norm': float(np.linalg.norm(A @ B - B @ A))})
    return values, (rho, A, B, Q, states, ks)


def transport(f, releases, leakage=0.):
    """Scalar stock protocol: returned stock is reset to the declared SOURCE preparation.

    Leakage acts on old residue before each release. No clock or energy is assigned.
    """
    if not isinstance(releases, list) or not releases:
        raise ValueError('release protocol must be a nonempty list')
    leakage = finite(leakage, 'leakage')
    if not 0 <= leakage <= 1:
        raise ValueError('leakage outside [0, 1]')
    fs = [finite(f[k], k) for k in ('phenotype','dark','return')]
    if abs(sum(fs) - 1) > TOL or min(fs) < 0:
        raise ValueError('invalid branch fractions')
    S, P, D = 1., 0., 0.
    rows = []
    for event, release in enumerate(releases):
        release = finite(release, 'release fraction')
        if not 0 <= release <= 1:
            raise ValueError('release outside [0, 1]')
        old = P + D
        leaked = leakage * old
        S += leaked; P *= 1-leakage; D *= 1-leakage
        released = release * S
        born_p, born_d = released * f['phenotype'], released * f['dark']
        returned = released * f['return']
        S = S - released + returned
        P += born_p; D += born_d
        rows.append({'event': event, 'release_fraction': release, 'released': released,
                     'returned_this_event': returned, 'leaked_from_old_Actual': leaked,
                     'born_phenotype': born_p, 'born_dark': born_d,
                     'SOURCE_stock': S, 'phenotype_stock': P, 'dark_stock': D,
                     'Actual_stock': P+D, 'ledger_sum': S+P+D})
    return rows


def dump(path, result):
    Path(path).write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + '\n', encoding='utf-8')


def main(inputs=ROOT/'inputs.json', output=ROOT/'results.json'):
    c = validate(json.loads(Path(inputs).read_text()))
    checks = {}
    def check(name, value):
        checks[name] = bool(value)
    inherited = ROOT.parent/'inherited'
    manifest = json.loads((inherited/'SHA256.json').read_text())
    for name, digest in manifest.items():
        check('frozen_'+name, hashlib.sha256((inherited/name).read_bytes()).hexdigest() == digest)
    old = json.loads((inherited/'filter_results_26_8.json').read_text())
    check('alpha_inherited_without_refit', c['alpha'] == old['calibration']['alpha_fitted_to_26_8_percent'])
    check('beta_inherited_without_refit', c['beta'] == old['calibration']['beta_fitted_to_5_percent'])
    n, w, psi = source_state(c['N'], c['alpha'])
    es = effects(c['N'], c['beta']); base = fractions(w, es)
    check('source_weights_normalized', abs(w.sum()-1) < TOL)
    check('source_amplitude_norm', abs(np.vdot(psi, psi).real-1) < TOL)
    check('source_weights_nonnegative', w.min() >= 0)
    check('address_effect_completeness', np.max(np.abs(sum(es.values())-1)) < TOL)
    check('branch_effects_positive', all(e.min() >= 0 and e.max() <= 1 for e in es.values()))
    check('baseline_ledger', abs(base['sum']-1) < TOL)
    reference = base if c['N'] == 1000000 else fractions(source_state(1000000,c['alpha'])[1],effects(1000000,c['beta']))
    for key, prior in [('phenotype','phenotype_fraction'), ('dark','unexpressed_Actual_fraction'), ('return','source_return_fraction')]:
        check('reference_cutoff_'+key, abs(reference[key]-old['joint_output'][prior]) < TOL)
    controls, derivatives = [], []
    for p in c['controlled_primes']:
        vp = valuations(n, p)
        mean = float(w @ vp)
        analytic = {key: float(np.sum(w * effect * (vp-mean))) for key, effect in es.items()}
        h = c['derivative_step']
        fp = fractions(source_state(c['N'], c['alpha'], {p:{'epsilon':h}})[1], es)
        fm = fractions(source_state(c['N'], c['alpha'], {p:{'epsilon':-h}})[1], es)
        numerical = {key:(fp[key]-fm[key])/(2*h) for key in es}
        error = max(abs(analytic[key]-numerical[key]) for key in es)
        check(f'covariance_derivative_prime_{p}', error < 1e-8)
        check(f'derivative_conservation_prime_{p}', abs(sum(analytic.values())) < TOL)
        derivatives.append({'prime':p,'mean_valuation':mean,'analytic':analytic,'finite_difference':numerical,'maximum_error':error})
        for epsilon in c['log_intensity_scan']:
            _, ww, _ = source_state(c['N'], c['alpha'], {p:{'epsilon':epsilon}})
            f = fractions(ww, es)
            controls.append({'prime':p,'epsilon':epsilon,'alpha_refitted':False,'beta_refitted':False,**f})
        check(f'control_ledgers_prime_{p}', all(abs(r['sum']-1) < TOL for r in controls if r['prime']==p))
    phase_cases = []
    for coherence, angle, label in [(1.,0.,'diagonal_coherent'), (0.,c['mixing_angle'],'mixed_dephased'), (1.,c['mixing_angle'],'mixed_coherent')]:
        for phase in c['phase_scan']:
            row, _ = coherent_case(c, phase, coherence, angle)
            row['case'] = label; phase_cases.append(row)
        selected = [r for r in phase_cases if r['case']==label]
        check(label+'_branch_positivity', all(r['minimum_branch_eigenvalue'] > -TOL for r in selected))
        check(label+'_completeness', all(r['completeness_error'] < TOL for r in selected))
        check(label+'_ledger', all(abs(r['sum']-1) < TOL for r in selected))
        cn,cw,_=source_state(c['coherent_N'],c['alpha'])
        p,q=c['coherent_pair'];i,j=p-2,q-2
        power=0;tmp=q
        while tmp % p == 0:
            power+=1;tmp//=p
        s,t=math.sin(angle),math.cos(angle)
        odd=(~prime_mask(c['coherent_N'])[2:]) & (cn%2==1)
        predicted=[c['beta']*(float(cw[odd].sum())+s*s*(cw[i]-cw[j])+2*coherence*s*t*math.sqrt(cw[i]*cw[j])*math.cos((1-power)*phase)) for phase in c['phase_scan']]
        check(label+'_phase_contract', max(abs(row['phenotype']-expected) for row,expected in zip(selected,predicted)) < TOL)
    one = transport(base, [1.]+[0.]*(c['reference_event_count']-1))
    u, eps = c['recycling_release_fraction'], c['leakage_control']
    recycle = transport(base, [u]*c['recycling_event_count'])
    leak = transport(base, [u]*c['recycling_event_count'], eps)
    r = base['Actual']; stationary = u*r/(eps+(1-eps)*u*r)
    q = (1-eps)*(1-u*r)
    for label, rows in [('one_window',one),('forced_recycling',recycle),('recycling_with_leakage',leak)]:
        check(label+'_stock_conservation', all(abs(z['ledger_sum']-1) < TOL for z in rows))
        check(label+'_stock_positivity', all(min(z[k] for k in ['SOURCE_stock','phenotype_stock','dark_stock']) >= 0 for z in rows))
    check('one_window_preserves_reference', max(abs(z['Actual_stock']-r) for z in one) < TOL)
    check('forced_recycling_closed_form', max(abs(z['Actual_stock']-(-math.expm1((z['event']+1)*math.log1p(-u*r)))) for z in recycle) < TOL)
    check('leakage_closed_form', max(abs(z['Actual_stock']-stationary*(1-q**(z['event']+1))) for z in leak) < TOL)
    check('reference_is_not_recycling_attractor', abs((r+u*r*(1-r))-r) > TOL)
    check('recycling_no_leak_asymptote', 0 < u*r < 1)
    needed_eps = u*r*(1-c['retention_target'])/(c['retention_target']*(1-u*r))
    balance_feasible=0 <= needed_eps <= 1
    check('balance_feasibility_condition', balance_feasible == (c['retention_target'] >= u*r))
    cutoffs=[]
    for N in [10000,100000,c['N']]:
        nw=source_state(N,c['alpha'])[1]
        cutoffs.append({'N':N,**fractions(nw,effects(N,c['beta']))})
    check('cutoff_ledgers', all(abs(row['sum']-1) < TOL for row in cutoffs))
    _, dense = coherent_case(c,0.,1.,c['mixing_angle'])
    rho,A,B,Q,_,_=dense
    reversed_values,_,_=instrument(rho,B,A,Q)
    ordered_values,_,_=instrument(rho,A,B,Q)
    direct=float(np.trace((np.eye(A.shape[0])-B.conj().T@B)@A@rho@A.conj().T).real)
    check('ordered_gate_sequential_survival',abs(ordered_values['Actual']-direct)<TOL)
    count=len(checks)
    result={'version':c['version'],'date':'2026-10-03','N':c['N'],
        'calibration':{'alpha':c['alpha'],'beta':c['beta'],'origin':'inherited two-stage 1.0-r1 joint calibration; no new fit'},
        'baseline':base,'reference_cutoff_baseline':reference,'source_intensity_controls':controls,'source_derivatives':derivatives,
        'phase_controls':phase_cases,'ordered_gate_contrast':{'AB_order':ordered_values,'BA_order':reversed_values,
             'interpretation':'BA interchanges both gate positions and admission/return roles; its output difference alone is not a commutator test'},
        'transport':{'one_window':one,'forced_recycling':recycle,'recycling_with_leakage':leak},
        'recycling_analysis':{'release_fraction':u,'leakage':eps,'stationary_Actual':stationary,'stationary_SOURCE':1-stationary,
            'zero_leakage_limit_Actual':1.,'epsilon_needed_for_target':needed_eps,'target':c['retention_target'],
            'balance_feasible':balance_feasible,'balance_parameter_status':'separate conditional control; not an inferred cosmological parameter'},
        'fixed_parameters_cutoff_sensitivity':cutoffs,
        'scope':{'computed':'prime SOURCE preparation, factorized relation state, ordered positive filter instrument, amplitude/phase response, finite-stock flow',
                 'stock_units':'normalized information weight; no physical energy assigned',
                 'event_index':'ordered operation counter; no time unit or minimum time inferred',
                 'reset_rule':'returned stock is re-prepared using the specified SOURCE amplitudes; this is an explicit protocol assumption',
                 'diagonal_phase_rule':'phase-only changes cannot alter diagonal branch weights',
                 'coherent_probe':'finite N<=256 contrast with a declared mixing angle, without aggregate refitting',
                 'open_work':['physical SOURCE dynamics','time and quantization unit','common-carrier physical map','particle response decoder','energy map']},
        'verification':{'checks':checks,'check_count':count,'all_passed':all(checks.values())}}
    if not result['verification']['all_passed']:
        raise AssertionError([k for k,v in checks.items() if not v])
    dump(output,result)
    handoff={'version':c['version'],'address_basis':'n=2..N; prime-factor exponents label relation ports','N':c['N'],
             'alpha':c['alpha'],'beta':c['beta'],'source_amplitude_rule':'z_p=p^(-alpha/2) exp(epsilon_p/2+i theta_p); g_n=product z_p^v_p(n)',
             'baseline_density':'rho=|psi><psi| or dephased diag(|psi|^2); diagonal output agrees',
             'initial_gate':'A=diag(1 on primes/even composites, sqrt(beta) on odd composites)',
             'normal_return_gate':'B=prime projector; K=ker(B) is composite residue',
             'reference_protocol':'one complete initial release, followed by no new release and no fold leakage',
             'physical_time_unit':None,'energy_map':None,'baseline_outputs':base,
             'parent_upstream_0_6_sha256':manifest['upstream_0_6_results.json'],
             'source_filter_parent_doi':'10.5281/zenodo.23092499','upstream_0_4_to_0_6_doi':'10.5281/zenodo.23112253'}
    dump(Path(output).with_name('handoff.json'),handoff)
    print(json.dumps({'baseline':base,'checks':count,'all_passed':True,'stationary_Actual':stationary,'recycled_Actual_last_event':recycle[-1]['Actual_stock']}))
    return result


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--inputs',type=Path,default=ROOT/'inputs.json')
    p.add_argument('--out',type=Path,default=ROOT/'results.json')
    a=p.parse_args();main(a.inputs,a.out)
