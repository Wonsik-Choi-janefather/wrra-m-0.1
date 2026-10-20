"""Finite reverse-engineered WRRA readout; supplied constants, not mass derivation.

c=1. Energies in MeV; spatial components represent pc in MeV.
Reaction ledger controls assume an admitted coincident interaction state.
No cross sections, decay dynamics or complete quantum-state inverse are claimed.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import json
import math
import numpy as np

DT = 1.4813019664158633e-21
PROFILES = {
    "electron": {"code": 9, "mass_energy_MeV": 0.51099895069,
                 "uncertainty_MeV": 0.00000000016, "spin": 0.5,
                 "negative_species": "e-", "positive_species": "e+",
                 "source": "https://physics.nist.gov/cuu/Constants/Table/allascii.txt"},
    "muon": {"code": 9, "mass_energy_MeV": 105.6583755,
             "uncertainty_MeV": 0.0000023, "spin": 0.5,
             "negative_species": "mu-", "positive_species": "mu+",
             "source": "https://physics.nist.gov/cuu/Constants/Table/allascii.txt"},
}

def dot(p, q):
    return float(p[0]*q[0] - np.dot(p[1:], q[1:]))

def boost(p, beta):
    beta = np.asarray(beta, dtype=float)
    b2 = float(beta @ beta)
    if not b2:
        return p.copy()
    g = 1/math.sqrt(1-b2)
    bp = float(beta @ p[1:])
    return np.r_[g*(p[0]-bp), p[1:]+((g-1)*bp/b2-g*p[0])*beta]

@dataclass(frozen=True)
class State:
    profile: str
    code: int
    orientation: int
    species: str
    charge_e: int
    lepton_number: int
    spin: float
    mass_energy_MeV: float
    four_momentum: tuple
    shutter_index: int

def render(profile, n, orientation, pc, shutter_index):
    if profile not in PROFILES:
        raise ValueError("unknown interpreter")
    cfg = PROFILES[profile]
    if n != cfg['code']:
        raise ValueError("undeclared code; this finite profile admits code 9 only")
    if orientation not in (-1, 1):
        raise ValueError("conjugate orientation must be -1 or +1")
    pc = np.asarray(pc, dtype=float)
    if pc.shape != (3,) or not np.isfinite(pc).all():
        raise ValueError("invalid momentum")
    m = cfg['mass_energy_MeV']
    energy = math.sqrt(m*m + float(pc@pc))
    species = cfg['negative_species'] if orientation == 1 else cfg['positive_species']
    return State(profile, n, orientation, species, -orientation, orientation,
                 cfg['spin'], m, tuple(np.r_[energy, pc]), shutter_index)

def recombine(a, b, interaction_ready):
    # Admission of a physical interaction is an explicit input, not inferred
    # from a shared arithmetic parent or from their emission-time separation.
    if not interaction_ready:
        raise ValueError("no admitted interaction event")
    if a.profile != b.profile or a.code != b.code or a.orientation != -b.orientation:
        raise ValueError("not a declared conjugate pair")
    if a.charge_e+b.charge_e or a.lepton_number+b.lepton_number:
        raise ValueError("unbalanced charges")
    return {'parent': 2*a.code,
            'owned_four_momentum': (np.array(a.four_momentum)+b.four_momentum).tolist(),
            'charge_e': 0, 'lepton_number': 0,
            'record': [asdict(a), asdict(b)],
            'information_scope': 'classical declared record only; not full quantum state'}

def inverse_record(aggregate):
    return tuple(State(**{**x, 'four_momentum': tuple(x['four_momentum'])})
                 for x in aggregate['record'])

def release_two_photons(aggregate):
    p = np.array(aggregate['owned_four_momentum'])
    if p[0] <= 0 or dot(p, p) <= 0:
        raise ValueError("timelike energetic aggregate required")
    # Selected center-of-momentum two-photon ledger channel. Its probability
    # and polarization amplitudes are not implemented.
    e = math.sqrt(dot(p, p))/2
    beta = -p[1:]/p[0]
    photons = [boost(np.array([e, 0, 0, sign*e]), beta) for sign in [-1, 1]]
    aggregate['owned_four_momentum'] = [0., 0., 0., 0.]
    aggregate['energy_owner_after_release'] = 'two outgoing photons'
    return photons

def run():
    errors = {'mass_shell': 0., 'two_stage_conservation': 0.,
              'photon_null': 0., 'carrier_conservation': 0.}
    cases = 0
    profiles_seen = []
    examples = []
    def check_error(name, value):
        errors[name] = max(errors[name], float(value))
    def reject(call):
        try:
            call()
        except ValueError:
            return 1
        raise AssertionError('invalid control accepted')
    for profile, cfg in PROFILES.items():
        m = cfg['mass_energy_MeV']
        for ratio in [0., .1, .5, 1., 2., 3.]:
            for axis in np.eye(3):
                for first in [-1, 1]:
                    a = render(profile, 9, first, ratio*m*axis, 0)
                    b = render(profile, 9, -first, -ratio*m*axis, 1)
                    pa, pb = np.array(a.four_momentum), np.array(b.four_momentum)
                    source = np.array([10*m, 0., 0., 0.])
                    pending, residual = source-pa, source-pa-pb
                    # Source charge cancels the first output until its partner
                    # is emitted. No unmatched charge is deferred without owner.
                    assert 0 == a.charge_e + (-a.charge_e)
                    assert -a.charge_e == b.charge_e
                    assert dot(pending, pending) > 0 and residual[0] > 0
                    for beta_size in [0., .3, .8, .95]:
                        beta = beta_size*np.array([1., 2., -1.])/math.sqrt(6)
                        P, A, B, R, Q = [boost(x, beta) for x in [source, pa, pb, pending, residual]]
                        for v in [A, B]:
                            check_error('mass_shell', abs(dot(v, v)-m*m)/(m*m))
                        check_error('two_stage_conservation', max(np.max(abs(P-A-R)), np.max(abs(R-B-Q)))/(10*m))
                        agg = recombine(a, b, True)
                        assert agg['parent'] == 18
                        assert inverse_record(agg) == (a, b)
                        agg['owned_four_momentum'] = (A+B).tolist()
                        photons = release_two_photons(agg)
                        for photon in photons:
                            check_error('photon_null', abs(dot(photon, photon))/max(m*m, photon[0]**2))
                        check_error('carrier_conservation', np.max(abs(sum(photons)-(A+B)))/max(m, (A+B)[0]))
                        assert agg['owned_four_momentum'] == [0., 0., 0., 0.]
                        cases += 1
        profiles_seen.append(profile)
        a=render(profile, 9, 1, [0.,0.,0.], 0)
        b=render(profile, 9, -1, [0.,0.,0.], 1)
        examples.append({'interpreter':profile, 'input_code':9, 'parent':18,
                         'outputs':[a.species,b.species], 'mass_energy_each_MeV':m,
                         'total_pair_rest_energy_MeV':2*m,
                         'shutter_index_difference':1, 'adopted_delay_s':DT})
    a=render('electron',9,1,[0.,0.,0.],0)
    b=render('electron',9,-1,[0.,0.,0.],1)
    controls=sum([
        reject(lambda:render('unknown',9,1,[0,0,0],0)),
        reject(lambda:render('electron',5,1,[0,0,0],0)),
        reject(lambda:render('electron',9,0,[0,0,0],0)),
        reject(lambda:recombine(a,a,True)),
        reject(lambda:recombine(a,render('muon',9,-1,[0,0,0],1),True)),
        reject(lambda:recombine(a,b,False)),
    ])
    assert max(errors.values()) < 1e-10
    frozen=json.dumps(PROFILES,sort_keys=True,separators=(',',':')).encode()
    result={'scope':'finite reverse-engineered readout and kinematic/ownership audit',
            'profiles':profiles_seen, 'profile_sha256':hashlib.sha256(frozen).hexdigest(),
            'cases':cases, 'rejected_controls':controls, 'max_normalized_errors':errors,
            'examples':examples,
            'excluded':['mass derivation','unique arithmetic-to-species assignment',
                        'reaction cross sections','spin/polarization amplitudes',
                        'muon decay dynamics','complete quantum-state inverse',
                        'observational timing validation','upstream pseudo-prime generator']}
    Path(__file__).with_name('reverse_interpreter_results.json').write_text(json.dumps(result,indent=2)+'\n')
    Path(__file__).with_name('reverse_interpreter_inputs.json').write_text(json.dumps(PROFILES,indent=2)+'\n')
    return result

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
