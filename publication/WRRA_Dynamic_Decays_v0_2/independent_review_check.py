"""Independent 1D continuum checks of WRRA v0.2; no manuscript-module import.
Usage: python astra_independent_review_check.py [path/to/results.json]
Uses archived cohort weights, but recomputes moments by analytic angular
integration and scipy adaptive electron-energy integration (not p,z quadrature).
"""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / 'deliverables/WRRA_Dynamic_Decays_v0_2/results.json'
r = json.loads(path.read_text())
M, m = r['inputs']['m_mu_MeV'], r['inputs']['m_e_MeV']
hi = (M*M+m*m)/(2*M)
def g(e):
    p = np.sqrt(e*e-m*m)
    return M*p/2*((M-e)*(M*e-m*m)-M*p*p/3)
def integrate(f):
    return quad(f, m, hi, epsabs=1e-4, epsrel=1e-12)[0]
norm = integrate(g)
mean_e = integrate(lambda e:e*g(e))/norm

def moments(b):
    def integrand(e, pressure):
        p2 = e*e-m*m
        er = np.sqrt(m*m+b*b*p2)
        nu = b*(M-e)
        return g(e)*((b*b*p2/er+nu)/3 if pressure else er+nu)
    return np.array([integrate(lambda e:integrand(e,t))/norm/M for t in (False, True)])

c = r['cohort_witness']
wp, wm = np.array(c['weights_plus']), np.array(c['weights_minus'])
current = np.array([moments(b) for b in c['age_scales']]).T
future = np.array([moments(c['future_redshift']*b) for b in c['age_scales']]).T
now_delta = current@(wp-wm)
later_delta = future@(wp-wm)
report = dict(mean_e_MeV=mean_e,
              mean_e_difference_from_archived=mean_e-r['kernel']['mean_e_MeV'],
              present_difference_EoverM_PVoverM=now_delta.tolist(),
              future_difference_EoverM_PVoverM=later_delta.tolist(),
              future_difference_from_archived=(later_delta-np.array(c['future_difference'])).tolist(),
              weight_sums=[float(wp.sum()), float(wm.sum())],
              minimum_weight=float(min(wp.min(),wm.min())))
print(json.dumps(report,indent=2))
assert abs(report['mean_e_difference_from_archived']) < 1e-9
assert max(abs(now_delta)) < 1e-10
assert abs(later_delta[0]) > 1e-6 and abs(later_delta[1]) > 1e-7
assert max(abs(later_delta-np.array(c['future_difference']))) < 1e-10
assert min(wp.min(),wm.min()) > 0
assert abs(wp.sum()-1) < 1e-12 and abs(wm.sum()-1) < 1e-12
