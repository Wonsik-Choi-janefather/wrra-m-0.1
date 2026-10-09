# Dynamic Decays and Nonequilibrium State Transitions in a Finite WRRA Model

Wonsik Choi and Jeongin Choi · Version 0.2 · 8 October 2026

Preprint and reproducibility materials. Release 0.2-r1 DOI: https://doi.org/10.5281/zenodo.23252334

Previous release: https://doi.org/10.5281/zenodo.23246308

## Reproduce

Run `python reproduce.py` with NumPy, SciPy and Matplotlib (tested versions in `results.json`). This reruns the inherited interface calculation and writes results, an expansion trajectory and figures. The 56 implementation checks include one check of the inherited 47-check suite; they are not 103 independent empirical tests.

The finite kinetic model uses measured masses and a supplied muon lifetime, a tree-level three-body decay quadrature, massless neutrinos and prescribed expansion. Radiative corrections and self-consistent cosmological evolution are outside its scope.

`manuscript.md` is the equation source. The PDF is the reading copy; DOCX equations are editable. `inherited/` preserves the interface inputs and conventions. `independent_review_check.py` provides additional numerical checks; it is not journal peer review.

Preceding r11 model: https://doi.org/10.5281/zenodo.23237629

License: Creative Commons Attribution 4.0 International, consistent with this repository. https://creativecommons.org/licenses/by/4.0/

## Final AI rereview and packaging correction — 9 October 2026

The final Astra Medium AI rereview is archived in `review/Astra_Medium_Final_Rereview_Dynamic_Decays_v0_2_KO.txt`. It recommends submission and reports no mandatory manuscript revisions, 56/56 checks passing, independent integral verification, and direct inspection of all 15 PDF pages. This is AI technical review, not external journal peer review or acceptance.

After that review, only the auxiliary checker's default path and usage filename were corrected. Run `python independent_review_check.py` from this directory, or invoke it by its full path from another directory. Its no-argument run passed all assertions. Scientific inputs, propositions, algorithms and numerical results are unchanged. The report remains a historical record of the pre-correction checker.

The exact reviewed PDF and DOCX are included in the Zenodo 0.2-r1 archive; hashes are recorded in the review.
