# Effective Carrier Routing, Control Work, and Stress in a Finite WRRA Model

Wonsik Choi and Jeongin Choi · release 0.2-r1 (corrected manuscript v0.2) · editorial revision 9 October 2026

Prepared research manuscript for Foundations of Physics. This package is not a record of journal submission, acceptance, or external peer review. Zenodo DOI: https://doi.org/10.5281/zenodo.23251977.

## Reproduce

Run `python reproduce.py` from a Python environment with NumPy, SciPy, and Matplotlib installed. The run is deterministic, offline, and does not require a large dense global-register matrix. It writes `results.json`, `run_log` if redirected, and figures, and re-executes both inherited scripts. A failed check raises an assertion error.

The recorded environment is Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0; `requirements.txt` gives package dependencies. Recent compatible versions should work, but exact floating-point errors can vary.

- `manuscript.md`: complete editable source, including proofs and references.
- `reproduce.py`: new carrier calculation; matrix-exponential, resonance, work, pressure, and composition checks.
- `results.json`: 123 carrier-level assertions and detailed outputs. Two assertions check success of inherited suites; inherited interface reports 47, decay reports 56. These are not independent empirical confirmations.
- `figures/`: the two new figures in vector PDF and PNG formats.
- `inherited/decay/reproduce.py`: unchanged third-paper v0.2 script.
- `inherited/decay/inherited/reproduce.py`: unchanged second-paper interface script, actually executed by the third-paper script.
- `inherited/decay/inherited/r11_controls.json`: frozen r11 control inputs; thresholds are not refitted.
- `provenance.json`: hashes identifying the inherited inputs and their source records.

The full N=10^6 ensemble uses the proved block formula; eight witness addresses use explicit full matrix exponentials on occupied support. Expansion handoff is a regression check. Its transport accuracy is separately covered by inherited time refinement and birth-time quadrature.

## Interpretation

The model supplies an effective comparator Hamiltonian, not a fundamental lepton-production vertex. Prime-register preparation, independence, physical species names, source energy, and pulse control are declared inputs. Standard two-state dynamics gives the pulse law. At fixed pulse parameters, the reference pressure-volume moment equals the negative log-volume derivative of mean switching work while the species probability is stationary. Decay is sequential and externally supplied. The full fifteen-channel carrier, weak-interaction derivation, controller resources, and self-consistent cosmological geometry are outside this calculation.

## Preceding records

1. r11: https://doi.org/10.5281/zenodo.23237629
2. Particle interface v0.2: https://doi.org/10.5281/zenodo.23241511
3. Dynamic decays v0.2: https://doi.org/10.5281/zenodo.23246308

Correspondence: Wonsik Choi, janefather@gmail.com. Author approval, contributions, funding, and competing-interest declarations require final author confirmation before journal submission. No automatic submission is part of this package.

Editorial revision of 9 October: contribution statement, assumption–derivation boundary, pressure-versus-preparation chain rule (11a), and validation terminology clarified. Scientific code and numerical results are unchanged. The third Astra medium internal review and post-correction check are now complete. Table 3 pressure wording and the PDF antielectron-neutrino overbar were corrected; no further mandatory technical corrections were identified.

## Public deposit

This archive preserves the reviewed v0.2 manuscript and its 9 October editorial revision. Preparation-time statements in the manuscript and original reproducibility ZIP about an unassigned DOI describe the pre-deposit state; the public record above supersedes those statements. This correction release changes the Table 3 explanation and PDF overbar rendering; scientific code and numerical results are unchanged.

- [English manuscript (PDF)](WRRA_Carrier_Coupling_v0_2_EN.pdf)
- [English manuscript (DOCX)](WRRA_Carrier_Coupling_v0_2_EN.docx)
- [Korean guide (PDF)](WRRA_Carrier_Coupling_v0_2_Guide_KO.pdf)
- [Reproducibility archive](Online_Resource_1_WRRA_Carrier_v0_2.zip)

License: Creative Commons Attribution 4.0 International (CC BY 4.0), consistent with the companion deposits.


## Correction release 0.2-r1

Previous immutable deposit: https://doi.org/10.5281/zenodo.23250062. Concept DOI: https://doi.org/10.5281/zenodo.23250061.

- [Third Astra medium review and final correction check](WRRA_Carrier_v0_2_Astra_Final_Review_KO.txt)
- [Earlier reviews with dated status update](WRRA_Carrier_Coupling_v0_2_Review_KO.txt)

Earlier two-review statements in the unchanged Korean guide describe the earlier editorial stage. This is AI internal technical review, not journal acceptance. Existing v0.2 filenames are retained to match the reviewed manuscript.
