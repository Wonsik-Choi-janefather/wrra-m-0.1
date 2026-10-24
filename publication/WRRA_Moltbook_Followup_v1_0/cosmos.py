"""Directional extension of the published finite-scale receiver; not a new SOURCE.

The adopted receiver is the standard periodic nearest-neighbour Laplacian in
finite_scale_bridge_v0_1. Its use and physical limitations are inherited.
"""
import itertools
import math
import numpy as np


def symbol(n, mode, length=1.0):
    h = length / n
    k = 2 * math.pi * np.asarray(mode, dtype=float) / length
    lam = float(np.sum((2 * np.sin(k * h / 2) / h) ** 2))
    return lam, float(k @ k)


def direct_stencil(n, mode):
    """Evaluate the inherited stencil on a complex periodic mode on an actual grid."""
    q = np.arange(n) / n
    phase = sum(mode[j] * x for j, x in enumerate(np.meshgrid(q, q, q, indexing='ij', sparse=True)))
    u = np.exp(2j * np.pi * phase)
    minus_lap = sum(2*u - np.roll(u, 1, axis) - np.roll(u, -1, axis) for axis in range(3)) * n*n
    return float(np.vdot(u, minus_lap).real / np.vdot(u, u).real), float(np.linalg.norm(minus_lap - symbol(n, mode)[0]*u)/np.linalg.norm(u))


def run():
    modes = [(3,0,0), (2,2,1)]  # identical |k| = 6 pi, different directions
    rows = []
    grid_checks = []
    for n in (32,64,128,256):
        for mode in modes:
            lam, k2 = symbol(n, mode)
            phase_error = 1-math.sqrt(lam/k2)
            leading = (2*math.pi/n)**2 * sum(x**4 for x in mode)/(24*sum(x*x for x in mode))
            row = dict(n=n, mode=list(mode), wavelength_cells=n/3, phase_speed_error=phase_error,
                       poisson_relative_error=k2/lam-1, leading_phase_error=leading)
            if n > 32:
                prior = next(x for x in rows if x['n']==n//2 and x['mode']==list(mode))
                row['measured_order'] = math.log2(prior['phase_speed_error']/phase_error)
            rows.append(row)
            if n in (32,64):
                measured, residual = direct_stencil(n, mode)
                grid_checks.append(dict(n=n,mode=list(mode),symbol_absolute_error=abs(measured-lam),
                                        grid_eigen_residual=residual))
    perm_errors=[]
    base=symbol(64,(2,2,1))[0]
    for m in set(itertools.permutations((2,2,1))):
        for signs in itertools.product((-1,1),repeat=3):
            perm_errors.append(abs(symbol(64,tuple(a*b for a,b in zip(m,signs)))[0]-base))
    # Fixed spacing, doubled volume, same physical wavelength; not refinement.
    volume_difference=abs(symbol(32,(3,0,0),1)[0]-symbol(64,(6,0,0),2)[0])
    checks={
        'same_physical_wavelength':sum(x*x for x in modes[0])==sum(x*x for x in modes[1]),
        'grid_matches_modal_symbol':max(x['symbol_absolute_error'] for x in grid_checks)<1e-9,
        'grid_eigen_residual':max(x['grid_eigen_residual'] for x in grid_checks)<1e-9,
        'second_order_measured':all(1.97<x['measured_order']<2.03 for x in rows if 'measured_order' in x),
        'leading_coefficient_limit':all(abs(x['phase_speed_error']/x['leading_phase_error']-1)<0.001 for x in rows if x['n']==256),
        'cubic_symmetry_only':max(perm_errors)<1e-10,
        'finite_directional_difference_detected':rows[0]['phase_speed_error']>rows[1]['phase_speed_error'],
        'fixed_spacing_volume_does_not_remove_dispersion':volume_difference<1e-12,
    }
    assert all(checks.values()),checks
    return dict(rows=rows,grid_checks=grid_checks,checks=checks,
        volume_test_absolute_difference=volume_difference,
        boost_test='OPEN: no boosted receiver/state map specified; rotations do not prove Lorentz covariance',
        scope='Actual finite-scale receiver extension; n=32,64 grid runs; n=128,256 modal evaluations. No physical infinite universe, full relativistic closure or new cosmic length is inferred.')
