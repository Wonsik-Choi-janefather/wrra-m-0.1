# WRRA-M 0.6 Information Load and Twist Gravity with Expansion

Wonsik Choi · 2026-10-01 · CC BY 4.0

Version 0.6 completes a finite homogeneous constitutive model. Weighted state loads are explicitly evaluated. One energy functional and classical homogeneous action connect state evolution, pressure, expansion and twist. Its clustering load is passed into the inherited calibrated local rotation and conditional lens response. WRRA Core 1.0 and MCC 2.3.2 remain the baseline.

| Stage | Executed content |
| --- | --- |
| Verification input | Whole-universe fractions: phenotype 4.93%, hidden load 95.07%, clustering 26.5%, residual background 68.57%; inherited response and 16-channel carrier |
| WRRA-specific transformation | State traces of positive load operators, one energy functional, volume-derived pressure, unitary update and classical homogeneous action |
| Output | Present q=-0.52855; reproduced aT=1.191812669e-10 m/s², rotation and lensing; evolving noncommuting loads with cancelling internal exchange |
| Falsification condition | Loss of trace/positivity, inconsistent pressure derivative, failed total conservation, violated independent acceleration constraint, inconsistent motion/lensing |

The exponents nc=0 and nb=3, operators and information clock are disclosed constitutive choices. Pressure and conservation follow from those choices. Unique microscopic laws, absolute cosmic length, a complete four-dimensional covariant local theory and spatial perturbation stability remain outside the completed claim. Symmetric-carrier filter gaps remain zero. Quantizable mass phenotypes and the nonquantum fundamental-gravity premise remain distinguished.

## Reproduce

```bash
python -m pip install -r requirements.txt
python compute.py
python verify.py
```

compute.py reads parameters.json and baseline_0_5/parameters.json, then creates results/results.json, summary and plots. verify.py compares the frozen 0.5 outputs and checks basis changes and boundary inputs. Outputs default to the script directory; --out selects another location. To regenerate manuscript tables, complete computation and verification in the default directory, then run:

```bash
python write_papers.py
python build_reports.py
```

Document creation additionally needs pandoc and python-docx. Korean rendering uses Noto Sans CJK KR and English uses Liberation Serif/Sans. Both editions have 22 editable native Word equations and identical numerical tables. PDFs were converted from Word using LibreOffice.

The complete ZIP includes both PDF/DOCX editions, full trajectories in results.json, summary, release checks, plots, source manuscripts and code. The GitHub calculation directory provides summary, checks and plots; obtain full trajectories from the ZIP or a computation. baseline_0_5/results.json is the corrected frozen 0.5 comparison record.

Preserved purity and state eigenvalues follow from the declared unitary construction. Numerical consistency is distinguished from observational validation. The geometric energy operator replaces the start model fixed-kernel restriction; its historical prototype remains separately available.

## 0.6-r2 shared grid and record magnitude

`parameters.json:lattice_N` controls both information-state loads and transport tests. `baseline_0_5/parameters.json:internal_lattice_N` is retained as provenance; the carrier receives a private copy with the 0.6 grid. `lattice_contract` reports configured and effective sizes. `verify.py` checks the 64/128 and 128/64 combinations and unchanged uniform reference outputs. Nonuniform state loads may depend on lattice size.

“Global twist record magnitude” is an instantaneous aggregate from load density and spatial size at the current state and scale. No independent temporal accumulation law is computed. Reference q₀, rotation and conditional lensing remain unchanged. See [the revision record](../../REVISION_0_6_R2.md).
