# Conservative quantization residues and CMB preparation in WRRA v0.2

Wonsik Choi and Jeongin Choi, independent researchers. 20 October 2026.

Read REPORT_EN.md or WRRA_Quantization_Twist_CMB_v0_2_EN.pdf. The Korean manuscript is REPORT_KO.md. Paper DOI: https://doi.org/10.5281/zenodo.23488763 (reserved during preparation; PUBLICATION_STATUS.json records actual release state).

## Reproduce

Python 3.12. Install the versions in requirements.txt. Run `python reproduce.py`, then `python review.py`. Main checks: 46. Separate oracle checks: 530. Run `python figures.py` for bilingual diagnostics. Actual cached patched-CAMB transfers are included; a new CAMB installation/build is not needed. The previous CAMB Boltzmann evolution is not rerun.

The entry point enforces the eight input hashes in inputs_frozen_sha256.json before readout. Main outputs: results/results.json, results/projection.npz and results/CMB_spectra.csv. Review output: results/review_results.json. All inputs, source and results are in the GitHub repository; Zenodo receives the Korean/English full manuscripts and PDFs, with GitHub data links only.

## Executed scope

Inherited address-generated seven-harmonic template -> adopted conservative twist difference -> exact rational residue-carry radiation/effective-matter conversion -> compensated entropy -> inherited regular D-isocurvature boundary projection -> actual cached T/E/phi transfers. The old R means return/vacuum, not radiation; old delta_R=0 for the new preparation.

New adopted inputs: 128 cells, half-conversion reference, quantum 1e-8 and coupling 1. The quantum is not derived from hbar or Planck time. Stage number is not a cosmological elapsed-time result. The normalized cell-energy ledger is not a complete covariant stress-energy matching calculation. A mean-stress single spatial realization is not a Born-rule outcome of the supplier bits.

Results: exact ledger error zero over 16,384 cell-stages; final residue below one quantum; T RMS 0.0017288344573261484 microK, E RMS 0.0000639105071995112 microK, deflection RMS 0.002319493345455457 arcsec. These are conditional WRRA outputs from disclosed rules, not measured detections. The previous observed-CMB background remains the comparator.

The untransferred harmonics 8-64 contain 10.8971852% of initial entropy variance. They are retained in the arrays and ledger. This does not specify their uncomputed CMB sky fraction. Conversion-time metric/velocity/pressure matching, ordinary-baryon reaction rates, full thermal history, complete modes and single-outcome supplier resource dynamics remain OPEN. The separate 100 nonuniform-demand identities do not implement an autonomous reaction-rate law. No new likelihood, full-CMB replacement or full Item 6 closure is claimed.

## Input provenance

Inputs are copied byte-for-byte from WRRA_Shutter_SOURCE_and_Macroscopic_Cases_v0_3_r1_2026-10-15.zip, retained version 3, shutter_three_tests_v02/inputs. The exact input manifest is frozen. The old study's 176-check execution is not claimed as a new rerun here.

Related full book: https://zenodo.org/records/23488205. Technical references appear in both manuscripts. New text/code: Wonsik Choi and Jeongin Choi, CC BY 4.0. Retain attribution and provenance of inherited scientific inputs. This package does not redistribute CAMB itself or external likelihood software.

Assessment order: verified inputs -> WRRA transformation -> outputs -> refutation conditions. Reproducing known inputs is an explanatory and compatibility achievement; independent prediction is an additional achievement. Input values are not newly derived outputs, and a connection is called integrated only to its internally executed scope.
