# WRRA-M 0.10 — address information load to physical energy and pressure

Released 2026-10-02. Author: Wonsik Choi. WRRA Core 1.0 remains fixed.

| Evaluation | Completed 0.10 connection |
| --- | --- |
| Verification input / 검증 입력 | Frozen reviewed 0.9 address ledger, 0.8 particle/filter and charge mapping, 0.6-r2 carrier operators and disclosed constants, energy targets, response coefficients and volume exponents. |
| WRRA-specific transformation / WRRA 고유 변환 | Address weights and sector effects → positive address response → once-fitted SI coefficients and carrier traces → one energy operator → volume-derived pressure, state exchange, gravity and homogeneous expansion. |
| Output / 산출값 | Thirty-two numerical check groups pass; all nine inherited state/volume cases reproduce. Reference q=-0.52855, v=207.5109051266 km/s and conditional finite-patch deflection=0.5355865106 arcsec. Frozen-coefficient address probes, address energy samples, 48-channel budgets and the conversion-work ledger are executed. |
| Falsification / 반증조건 | Negative admissible energy, failed calibrated reproduction, pressure-derivative mismatch, noncancelling internal exchange, missing conversion-work ownership, duplicated channel energy, invalid states, altered undeclared input or document/execution mismatch. |

## Fixed distinctions

Arithmetic shares 5%/26.8%/68.2% remain distinct from inherited calibrated
energy shares 4.93%/26.5%/68.57%. Three positive SI coefficients are fitted once
on the frozen reference, then held for changed-address and changed-carrier
calculations. A separately identified alternate target yields q=-0.523.

Pressure is derived from the same volume-dependent energy function. Its
exponents are disclosed constitutive inputs, not newly discovered microscopic
laws. The dimensionless carrier clock is inherited; physical proper time is
scheduled for 0.12. Physical quantization and measurement records remain 0.13.

The signed conversion-work account records exchange between the representative
calculation system and the environment owning the conversion work. It is not
a fourth cosmic density fraction. The required exchange and accounting close;
the microscopic environment driving that conversion is subsequent work.
Nonphenotype loads are retained, including arbitrarily small positive loads.
The 48 channels allocate one phenotype budget without a generation multiplier.

## Validation and artifacts

- Numerical verification: 32 groups; reviewed 0.9 baseline: 27 groups.
- Two language editions: 12 matching native equations and 12 calculated table
  body rows each; all ten final PDF pages inspected individually.
- Clean-copy reproduction deletes captured numerical results and regenerates
  calculation results and both source manuscripts. Byte comparisons and the
  archive SHA256 manifest are recorded alongside the results.
- The ZIP includes the frozen dependency sources, inputs, checked outputs,
  bilingual DOCX/PDF/Markdown and citation/license information.

```bash
python -m pip install -r calculations/wrra_m_0_10/requirements.txt
python calculations/wrra_m_0_10/run_release.py
```

The expanded roadmap remains 0.10 energy/pressure, 0.11 sequential calibration,
0.12 clock/spectra, 0.13 measurement/records, 0.14 cutoff/uncertainty,
0.15 stress/curvature/size, 0.16 neutrino parameters, 0.17 propagation, then
the 1.0 integration audit. The model is not being declared WRRA_M 1.0 here.

The reviewed 0.9 baseline DOI is 10.5281/zenodo.23091892. This reference is not
a DOI assigned to 0.10. GitHub publication and the self-contained reproduction
archive constitute the completed 0.10 deliverables.
