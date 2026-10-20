WRRA v0.6: conditional nonlinear-lensing likelihood and MeV packet thermal completion.
Authors: Wonsik Choi and Jeongin Choi, independent researchers, 20 October 2026.

Install requirements.txt, then run python run_all.py.
No Fortran compilation is needed with a supported CAMB wheel.
prepare_inputs.py extracts the frozen NASA data ZIP and downloads the pinned
official CosmoMC CMBlikes.py reference, verifying its SHA256. That external
source is not redistributed here. The likelihood itself is our native NumPy/
SciPy implementation; official code is used only for independent crosscheck.
The only reference-code changes are syntax-only np.object/object and np.int/int
substitutions for NumPy 2 compatibility, performed in memory and disclosed.

run_camb.py calculates four NEW spectra: inherited WRRA background plus declared
calibrated adiabatic As=2.1e-9, ns=.9649, tau=.0544. Nonlinear lensing uses HMCode
2020 in standard CAMB 2.0.4; this empirical prescription is adopted, not derived
by WRRA. Native likelihood uses all 18 bins, covariance, windows and TT/PP
response corrections of the released SPT-Planck dataset.

thermal_history.py executes the v0.5 packet clock with finite-mass equilibrium
electron/positron thermodynamics, an effective free-streaming neutrino bath,
recording heat and pressure work. N_eff=3.044 is an input. It is not calculated
from a collision integral. Thermal time is ELAPSED since the inherited pulse
start, not cosmic age. Keeping the inherited time calibration changes the
physical initial scale inferred from today's photon entropy. The old v0.4 and
v0.5 frozen calculations are not overwritten.

run_checks.py executes 54 checks, including independent official likelihood,
heat-capacity differentiation, EOS quadrature, conservation and negative controls.
REPRODUCTION.json records an exact clean-folder repeat of scientific JSON,
CSV and arrays; wall-clock timings are excluded.

IMPORTANT SCOPE: full v0.4 metric/velocity/neutrino initial states and v0.5
event-time perturbations are NOT injected into these CAMB runs. The full-state
gate in results/full_state_gate.json remains blocked. A good conditional
background-plus-adiabatic likelihood is not a complete test of WRRA SOURCE
perturbations. No joint CMB/BAO/BBN posterior or BBN abundance calculation is
claimed. Main modules are implemented; complete Step 3 integration remains open.

Data acknowledgment: NASA LAMBDA, SPT and Planck; Simard et al. 2017,
arXiv:1712.07541; Omori et al. 2017, arXiv:1705.00743.
Theory tools: CAMB (Lewis, Challinor & Lasenby), HMCode 2020 (Mead et al.,
arXiv:2009.01858), official CosmoMC likelihood format (Anthony Lewis),
PDG 2025 Big-Bang Cosmology review for equilibrium thermodynamics.
New original WRRA code and reports: CC BY 4.0. External software/data retain
their original terms; upstream reference source and installed runtimes are not
included in the distribution. No new public release is asserted by this local package.

Rebuild PDF reports: python make_reports.py (also matplotlib, pandoc, xelatex,
Noto Sans CJK KR). Text sources and all computed outputs are included.
