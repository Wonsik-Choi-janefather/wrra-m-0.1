# WRRA zeta-to-physics correspondence v0.1

**Wonsik Reality-Renderer Architecture**. Research item 4, following the local twist/load study. Original book: MCC 3.0 v0.27-r1, https://doi.org/10.5281/zenodo.23516661 .

## Reproduce

Python 3 with NumPy, SciPy, mpmath and Matplotlib:

```sh
OPENBLAS_NUM_THREADS=2 python3 compute.py
OPENBLAS_NUM_THREADS=2 python3 verify.py
python3 plot.py
```

Validated with NumPy 2.3.5. Compute evaluates the full 935,155 selected addresses and 70 zero branches; no sampled Gram surrogate. Main 49/49 checks; separate verification 20/20. Reproduction can take a few minutes. The optional figure uses Matplotlib. No tests count as independent physical experiments.

## What is new

Chapter 131's frozen Mellin-phase map is embedded in the inherited CRT geometry and read through the physical H = hbar*c*|k|. It is not the earlier dimensionless exp(-iL) propagation. The shutter/distance calibration remains inherited, not a newly predicted physical scale.

A 70-state unitary port dilation preserves every complementary branch. All-port energy, selected-band detection, high-frequency remainder, and mean energy transfer from phase control are computed. The simple square-root probability complement is not misused as a physical energy complement. The auxiliary register is ideally energy-degenerate; apparatus generation/reset costs remain open. The free carrier is a scalar spatial single-excitation reference register, not complete Maxwell/SM physics.

A full-address 70x70 Gram calculation gives a concrete optimality diagnostic: original equal combination does not maximize selected-port success for either fixed preparation. The optimized vector changes only the diagnostic combining port, not the registered model. It optimizes unfiltered pass probability, not low-band detection, fidelity, or physical preparation cost.

## Files

- `inputs/` and `input_manifest.json`: frozen zero file, original phase code/results, book chapter excerpts and source-carrier timing-code evidence, with SHA256.
- `compute.py`, `verify.py`, `plot.py`: main and separate calculations.
- `results.json`, `physical_readout.csv`, `independent_verification.json`: outputs and checks.
- `*_spectrum.csv`, `*_axis*.csv`: calibrated energy bins and band-conditional directional distributions.
- `*_combiner.npz`: full Gram matrix, eigenvalues and maximum-pass coefficients.
- `REPORT_KO.md`, `REPORT_EN.md`, `physical_readout.png`: bilingual accounts and figure.

## Scope and ownership

Both inputs are inherited test preparations, not original sector-specific SOURCE payloads. The CRT geometry differs from the 500x29x70 graph. No cosmic fractions, old RAR predictions, complete GR/CMB pipeline or earlier scores are reassigned to the new output. The old phase port probabilities replay exactly. Arbitrary finite real phase lists also define valid conservative instruments; zero necessity, autonomous permission/phase preparation, actual particle masses, quantum numbers and species creation rates remain open.

The package is an executable conditional research result. It has not been published as a new GitHub/GitBook/Zenodo release.
