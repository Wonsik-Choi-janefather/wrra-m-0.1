SOURCE local-sector, supply-frame and shutter bridge v0.2 — 2026-10-14
Research context: Wonsik Choi and Jeongin Choi.
Run python reproduce.py. Requirements: numpy, scipy, matplotlib. No online access.

Validation input
Actual v0.15 addresses, effects, weights and residue-owned kernels; v0.29.1
finite supply/energy rules, eta, uniform reference p=.5 and epsilon=1e-8;
the prior shutter and c; the supplied .05 Mpc^-1 diagnostic wave number.
The public upstream archive is DOI 10.5281/zenodo.23329214.

WRRA transformation
Recompute B_sector,residue,slot from every active address. Apply the original
normalized transmission kernel K_r using all p=2,3,5 taps. Retain each sector's
conditional residue composition. The previous TOTAL-slot kernel substitution
lost this ownership; the needed rule already existed in the inherited code.

A direct information-shape-to-density substitution is retained as a failed
linear negative control. The corrected typed extension uses the actual supply
register: p_r(X)=.5+epsilon*(K_r(X/L)-1) on the original mod3-complement group.
The inherited source/supply gap yields delta u_D,R=eta_D,R*DeltaA*epsilon*
sum_controlled B_D,R,r,j*(K_r-1); P is unchanged, delta p=-delta u_R.
No new amplitude fit is added. The kernel-to-supply preparation template is a
new explicit assumption; epsilon remains an inherited diagnostic input.
The prepared supplier is included before the swap at every spatial phase.

Outputs
Recomputed payload/local profiles match the archive exactly as arrays.
Independent direct-address versus slot reconstruction agrees to about 7e-15.
The supply-energy map gives relative density RMS 7.51e-9 / 7.47e-9 and maximum
contrast 2.14e-8 / 2.13e-8, preserving the mean and valid probabilities.
These are not measurements of primordial curvature power or CMB validation.

Calibrating the first harmonic to .05 Mpc^-1 yields seven source harmonics
.05,.10,.15,.20,.25,.30,.35 Mpc^-1 with computed energy/pressure amplitudes.
The macro-to-micro length ratio is conditional, not derived from N_U alone.
Finite shutter counts are evaluated with integer/phase accumulation rather
than iterating enormous counts. Light phase periods are instantaneous a=1
path equivalents, not integrated travel times in an expanding universe.

All 28 real weighted/unweighted cosine/sine components were integrated with
the inherited conditional late-epoch GR subsystem. Maximum normalized
vacuum-source residual is about 5.52e-7, or 6.90e-8 with tighter tolerance;
omission controls give about .999992. Solutions converge to about 2.25e-12.
Photons, neutrinos, recombination and a full CMB likelihood are not included.

Separate 3D transport probes
Adopt H=hbar*c*|k| on the calibrated 500x29x70 index graph. Execute its spectral
unitary with a shared identity on 15 channels. Seven directions/64 shutters
match c in phase speed to about 2.80e-13 and preserve norm to 6.66e-16.
The operator is nonlocal in position; strict microscopic causal support,
Maxwell gauge/polarization, Lorentz completion and photon generation are not proved.

Falsification
Lost ownership, failed independent reconstruction, invalid probabilities,
source/supplier energy or pressure imbalance, admitted aliases, inconsistent
directional propagation, or failed required-transfer GR constraints rejects
the relevant mapping. Proper observational comparisons remain future tests.

Conclusion
The local reconstruction issue is corrected using the original residue rule.
An actual SOURCE -> supply probability -> energy/stress -> harmonic GR bridge
is executed with inherited amplitude inputs. Metric/macro scale calibration
is legitimate model construction and remains identified as calibration;
universe-size/original-space derivation and full CMB testing remain open.

Correction record
v0.1's coarse-kernel failure remains a negative control. Any inference from it
that the original local spatial rule was absent is superseded by v0.2.
Input hashes, original code/data, CSV, JSON, local fields and plot are bundled.
