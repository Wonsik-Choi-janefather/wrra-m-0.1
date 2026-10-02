# WRRA_M 0.11 · First five inputs, sequential calibration

Wonsik Choi · 2026-10-02 · Fixed WRRA Core 1.0 / MCC 2.3.2 · CC BY 4.0

## 검증 입력 / Verification inputs

The frozen 0.10 input is embedded in `parameters.json` and has canonical SHA256
`8342c02c3d872994b13c54c9512d6e7440a45e7ef9602cb1ac4ebe34eddb540f`.
The five physical anchors enter in this order:

| Step | Input | Value | Role |
| --- | --- | --- | --- |
| 1 | G | 6.67430e-11 SI | Action/response normalization |
| 2 | H0 | 67.4 km/s/Mpc | Planck 2018 base-LambdaCDM benchmark |
| 3 | f_phi | 0.0493 | Inherited physical energy fraction |
| 4 | f_c | 0.265 | Inherited clustering energy fraction |
| 5 | m_e c² | 510998.95069 eV | CODATA 2022 electron rest energy |

c, exact SI h and eV conversion are fixed references. The parsec conversion,
finite carrier, gravity response and local-source geometry remain inherited.
Electron mode **23**, zero mass intercept, address profiles and energy-volume
exponents are declared constitutive inputs. The 0.9 arithmetic targets
**5% / 26.8% / 68.2%** remain distinct from physical energy targets
**4.93% / 26.5% / 68.57%**. Two independent arithmetic target values are
additional disclosed inputs beyond the five physical anchors.

## WRRA 고유 변환 / WRRA-specific transformation

`prefix_outputs` accepts only an ordered prefix of the five physical inputs.
It never reads future target values from the configuration. Stage results
report all available outputs and the remaining physical anchors.

The 0.10 address/carrier energy operator is reused with explicit SI calibration.
Coefficients eta_s are fitted once for each declared target set and then held
fixed for address/state controls. Pressure is its volume derivative; the
same load enters inherited gravity and homogeneous expansion. Electron energy
sets the mass-mode unit and re-expresses the existing operator without adding
an extra energy-density budget.

`alpha_addr` is the address power-law exponent, not electromagnetic alpha.
It and the admission threshold h are refitted to the two legacy arithmetic
targets for comparison. `beta_eff` is derived, so an independent third beta
input is unnecessary. Electromagnetic alpha remains undetermined.

## 산출값 / Outputs

- mu_E = **22217.345682173913 eV**, conditional on n_e=23 and zero intercept.
- q0 = **−0.52855**, v = **207.51090512661662 km/s**, conditional finite-patch
  deflection = **0.5355865105583804 arcsec**; all nine 0.10 cases are retained.
- zeta*kappa_h² = **3.028112744666204e-52 m⁻²**. zeta and kappa_h are not
  separately identified.
- Length coefficient = **5.746639841098109e25 m**; actual L0 remains
  `coefficient*sqrt(W0)`, with W0 unassigned.
- The five-anchor logarithmic dependency matrix has rank five, conditional
  on frozen model choices. Response-shape controls demonstrate residual
  freedom despite reproducing the same five anchors.
- **28 new check groups** plus **32 inherited 0.10 groups** pass. Generic
  mass modes are not predictions identifying other particle masses/charges.

## 반증조건 / Falsifiers

Future-target leakage, failed calibrated reproduction, mismatched pressure
derivative, nonconservation, duplicated electron budget or a claim that an
unidentified quantity is fixed requires revision. Invalid inputs, records,
modified exact units and out-of-order prefixes are rejected.

```bash
python -m pip install -r calculations/wrra_m_0_11/requirements.txt
python calculations/wrra_m_0_11/run_release.py
```

The command regenerates 0.10 and 0.11 numerical outputs, runs their checks,
and writes bilingual Markdown manuscripts. Published Word/PDF files are
visually checked editions. `results/reproduction_checks.json` records the
clean-copy byte comparison. `SHA256SUMS_0_11` is the archive-content manifest.

| File | Content |
| --- | --- |
| parameters.json | Full input ledger and provenance |
| results/results.json | All stage, physical and degeneracy outputs |
| results/sequential_calibration.csv | Stage ownership and available outputs |
| results/physical_cases.csv | Nine inherited physical cases |
| results/mass_modes.csv | Zero/intercept/sign mass controls |
| results/input_response_probes.csv | Ten ±1% construction probes, not confidence intervals |
| results/verification.json | 28 named numerical falsifiers and evidence |
| results/document_checks.json | Matched native equations and computed tables |
| references/ | Candidate-sheet selected-row snapshot and source contract |

## 판정 / Completion scope

The disclosed sequential calibration and residual-freedom accounting close
0.11. Reproduction through calibration is a legitimate completed result;
independent prediction is not a prerequisite. Version 0.12 addresses clock,
boundary conditions and spectra; physical measurement/records remain 0.13.
The frozen 0.9 roadmap remains the authoritative development order.

- [한국어 PDF](../../paper/WRRA_M_0_11_KO.pdf) · [Word](../../paper/WRRA_M_0_11_KO.docx)
- [English PDF](../../paper/WRRA_M_0_11_EN.pdf) · [Word](../../paper/WRRA_M_0_11_EN.docx)
- [Reproducibility ZIP](../../paper/WRRA_M_0_11_Reproducibility.zip)
- [Completion record](../../REVISION_0_11.md)
