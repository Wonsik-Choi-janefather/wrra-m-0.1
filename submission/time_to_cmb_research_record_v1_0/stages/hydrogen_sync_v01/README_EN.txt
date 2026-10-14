Hydrogen event synchronization candidate — v0.1, 14 October 2026

INPUTS: hyperfine centroids, total two-photon transition frequencies:
1S-2S 2466061413187035 +/-10 Hz (Parthey 2011).
1S-3S 2922743278671500 +/-2600 Hz (Fleurbaey 2018).
2S-8D5/2 770649561570900 +/-2000 Hz (Brandt 2022).
Alternate 1S-3S: 2922743278665790 +/-720 Hz (Grinin 2020).
Alpha from CODATA 2022; shared SI h,e,c are adopted inputs.

CANDIDATE MAPPING: rational level code u_n=1/n^2 -> atomic state transitions.
Atomic n has not been derived from or identified with an MCC SOURCE address.
Coulomb and Dirac spectral templates are adopted physics, not new WRRA derivations.
The audit executes the proposed calibration/frozen-rule/holdout workflow.

MODELS: inverse-square (one A), point-Coulomb Dirac template (one A),
Dirac plus empirical L*delta_l0/n^3 S-level shift (two A,L).
All minimal anchor subsets were used, with other transitions held out.
There is no full QED, recoil or finite-size calculation here.

RESULTS: 1S-2S anchor, inverse-square residuals -1.309046 ppm (1S-3S),
-6.968083 ppm (2S-8D5/2). All are much larger than experimental precision.
For the held-out 2S-8D5/2 line, the absolute residual falls from 5369.950 MHz
(inverse-square) to 1177.021 MHz (Dirac) to 7.880335 MHz (Dirac+S shift).
The latter uses 1S-2S and 1S-3S as anchors. Predicted frequency:
770649553690564.875 Hz; prediction sigma from anchors 5210 Hz;
measurement sigma 2000 Hz. It still fails the precision holdout check.
Theory truncation error is absent, so this is NOT a significance against full QED/MCC.
The alternate 1S-3S dataset leaves a residual -7.891777250 MHz.

TIME: the corrected model's relative-phase cycle at the 2S-8D5/2 energy gap is
1.297606668571 fs. This is an optical phase period, NOT an excitation
waiting time, transition duration or level lifetime. Total resonance frequency
is distinguished from the half-frequency excitation laser.
Shared SI constants make the units consistent with the neutrino audit, but do
not independently establish a universal arithmetic clock map.

FALSIFICATION/DIAGNOSIS: the tested truncated spectral bridges fail precision
holdouts. Scale-only adjustment is insufficient. Preserve state distinctions
(n,l,j) and calculate state-dependent radiative/recoil/finite-size corrections.
No third-line-specific fudge parameter was introduced. Event identity and
mapping uniqueness remain unestablished. The MCC book is unchanged.

Run python reproduce.py; requires numpy and matplotlib.
Frozen inputs, results, all anchor/holdout CSV rows and a plot are included.

Sources:
https://arxiv.org/abs/1107.3101
https://arxiv.org/pdf/1801.08816
https://arxiv.org/abs/2111.08554
https://doi.org/10.1126/science.abc7776
https://physics.nist.gov/cuu/pdf/all.pdf
https://arxiv.org/pdf/2302.06288
