# Finite-frame exchange and conditional scalar bridge (v0.29.1)

Wonsik Choi · 13 October 2026 · Toy model / effective phenomenology

DOI: https://doi.org/10.5281/zenodo.23329214

## What is calculated

An explicit energy-conserving finite source/register swap and a conditional scalar GR mode with conservation-required vacuum momentum transfer. The supplied spatial preparation and interaction recipient are declared assumptions.

| Test | Weighted | Unweighted |
|---|---:|---:|
| Einstein 00 residual / common vacuum source | 9.9924e-9 | 1.03691e-8 |
| Same residual, required transfer omitted | 0.999992 | 0.999992 |
| Spatial Einstein trace residual, with transfer | 3.49e-16 | 5.77e-16 |
| Tighter-tolerance comparison | 1.38e-12 | 1.52e-12 |

The mode suite passes 26 construction checks; the separate audit passes 28. These are numerical checks, not empirical confirmation counts. The normalization is specified in the manuscript and JSON, not observational sigma.

## Start here

- [English technical note](WRRA_Finite_Frame_Bridge_v0_29_1_EN.pdf)
- [한국어 기술노트](WRRA_Finite_Frame_Bridge_v0_29_1_KO.pdf)
- [English editable manuscript](Manuscript_EN.md)
- [한국어 README](README_KO.md)
- [One-mode ledger](results/single_mode_ledger.json)
- [Independent audit](results/review_ledger.json)

## Reproduce

```bash
python -m pip install -r requirements.txt
python single_mode.py
python review.py
```

The one-mode calculation uses NumPy/SciPy/Matplotlib. The full historical homogeneous calculation additionally needs CAMB 2.0.4:

```bash
python frame_baseline/run.py
```

The bundled CAMB source archive is upstream code, with its separate license in `frame_baseline/CAMB_LICENSE.txt`. Compilation may require gfortran. The 31-file historical manifest is checked by `review.py`; the top-level manifest verifies all released evidence.

## Interpret results correctly

Addresses are finite state labels; 128 slots are information-processing units, not 128 physical cells. The finite-time window is temporal averaging, not a proof resolving every UV divergence. The source-plus-supply boundary is included in energy and pressure accounting.

The 1,015,000-address count is contingent in this construction: the interpretation does not privilege our universe. It is a frozen computational input, not an observed or uniquely derived universal constant; neither its generating probability law nor robustness across counts is established.

The earlier fixed standard-completion CAMB calculation gives H0=67.4499 / 66.9054 km/s/Mpc and first TT peaks 220 / 221. The new interacting mode has NOT been inserted into that radiation/recombination calculation. Flatness is an input; BBN values are inherited PRIMAT table interpolation. Official Planck -2 ln L and BAO covariance evaluation have not run. Primordial power and physical 3D address placement remain open. No observational optimizer was used.

## License and assistance

Original report, data and code: CC BY 4.0, consistent with the parent repository. Third-party CAMB and Planck materials retain their original terms. AI assisted implementation, computational auditing and language preparation; no independent peer review or publication recommendation is claimed.

## Documentation revision 0.29.1

This is a wording/scope revision; numerical code and outputs are unchanged. The normalization max|F|/max|S_R| is stated explicitly; finite residuals are distinguished from zero error. No additional observational optimization with frozen inputs is distinguished from a parameter-free physical derivation. The previous standard CMB calculation is separated from the new interacting single-mode test.

[Limited progress report](Physical_Status_Summary_EN.txt)
