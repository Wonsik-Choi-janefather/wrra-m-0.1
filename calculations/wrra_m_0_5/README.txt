WRRA-M 0.5
Quantized Mass and Continuous Gravity in a Finite Twist Model
Wonsik Choi / 2026-10-01
ORCID: 0009-0001-4263-9772
Contact: janefather@gmail.com

This version selects B_C as a modeling premise. It does not claim a universal
experimental or mathematical proof that gravity cannot be quantized.
Expansion and twist coexist in the architecture; the executed calculation
is the present static twist-stress sector.

Run the calculations:
    python compute.py --out results

Required calculation packages: numpy scipy matplotlib
The values in parameters.json are editable calibrations, not immutable laws.
The response nu is the calibrated constitutive law adopted in the earlier
WRRA Galactic Disk paper. It is actually evaluated here and is not asserted
to have been derived from a unique microscopic WRRA action.

Executed results:
- discrete internal mass modes and finite-chain convergence
- homogeneous 16-channel transport response with full rank
- zero selection gaps for that homogeneous prototype
- cross-scale twist normalization
- spherical finite-patch stress, motion, and conditional lensing
- the earlier Milky Way algebraic disk renderer
- sensitivity to changing phenotype and clustering-stress fractions
- conditional information-load / twist / T^3 closure algebra

Limits:
- lensing is the contribution inside the 200 kpc patch, conditional on Phi=Psi
- the Milky Way comparison uses the earlier linearized Eilers reference
- no full covariant action, cosmological dynamics, or quantum-classical
  hybrid update law is supplied
- the declared T^3 example does not infer actual cosmic topology or size
- the homogeneous carrier fails to select the target filter uniquely

build_report.py additionally needs python-docx and pandoc. It creates native
Word math and consumes the results directory. The DOCX and PDF supplied
with this package were rendered and visually inspected.

Copyright 2026 Wonsik Choi. CC BY 4.0.
