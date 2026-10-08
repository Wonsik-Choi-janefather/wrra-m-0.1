# Dynamic Decays and Nonequilibrium State Transitions in a Finite WRRA Model

Wonsik Choi and Jeongin Choi · Version 0.2 · 8 October 2026

Preprint and reproducibility materials. DOI: https://doi.org/10.5281/zenodo.23246308

## Reproduce

Run `python reproduce.py` with NumPy, SciPy and Matplotlib (tested versions in `results.json`). This reruns the inherited interface calculation and writes results, an expansion trajectory and figures. The 56 implementation checks include one check of the inherited 47-check suite; they are not 103 independent empirical tests.

The finite kinetic model uses measured masses and a supplied muon lifetime, a tree-level three-body decay quadrature, massless neutrinos and prescribed expansion. Radiative corrections and self-consistent cosmological evolution are outside its scope.

`manuscript.md` is the equation source. The PDF is the reading copy; DOCX equations are editable. `inherited/` preserves the interface inputs and conventions. `independent_review_check.py` provides additional numerical checks; it is not journal peer review.

Preceding r11 model: https://doi.org/10.5281/zenodo.23237629

License: Creative Commons Attribution 4.0 International, consistent with this repository. https://creativecommons.org/licenses/by/4.0/
