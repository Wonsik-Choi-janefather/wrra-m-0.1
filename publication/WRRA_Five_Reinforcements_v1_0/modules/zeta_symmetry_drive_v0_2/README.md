# WRRA zeta symmetry and driven dynamics v0.2

Wonsik Reality-Renderer Architecture. Continuation of zeta physical readout v0.1.

## Run

```sh
OPENBLAS_NUM_THREADS=2 python3 compute.py
OPENBLAS_NUM_THREADS=2 python3 verify.py
python3 plot.py
```

Python 3, NumPy, SciPy and Matplotlib. Main: 79/79; separate: 26/26 internal checks. Full 935,155-address, 70-branch endpoints are recomputed. Separate DOP853 integration checks a 3-branch/11-address driven system, work integral and positivity; exact finite phase-error enumeration checks the noise density law.

## New contracts and scope

1. Branch-blind normalized single pure port, with complete-graph coefficient-contrast cost, uniquely selects the original equal combining ray. This is stronger than relabeling covariance and is not inferred from cosmological nonprivilege alone. The cost is not energy or total universal computing cost. Maximum-pass and minimum-contrast objectives remain distinct.
2. Prescribed positive Hamiltonian H(t)=H0+U0(t) B U0(t)^dagger, B=(hbar/tau) Gamma tensor log-address, executes U(t)=U0(t)exp(-iBt/hbar). This exactly reaches the old phase/transport endpoint. The controller is external and generally nonlocal; no autonomous device is claimed.
3. Mean control potential, switch energies and within-interval work are counted. Ideal recovery does not establish zero reset cost. Wrapped generator alternatives preserve the endpoint with lower spectral scale but higher separation rank on a verified 70x12 subset. One product factor is not proof of minimum gates or physical apparatus cost.
4. Independent Gaussian branch phase noise gives eta=exp(-s^2), rho_out=eta*rho_coh+(1-eta)*rho_mix/C. Counts can increase as original interference disappears. No measurement data or fit are used.

The zero list, original sector-specific SOURCE link, apparatus locality/autonomy and particle species remain separate open connections. No original composition, RAR or GR/CMB output is reassigned to these test preparations. SOURCE allocation is timeless; t only applies after spatial embedding.

## Files

`inputs/` freezes previous outputs/code/report, actual zeros and full Gram matrices. Input hashes are in `input_manifest.json`. Executable code, `drive_energy.csv`, `driven_path.csv`, `phase_noise.csv`, `results.json`, `independent_verification.json`, a figure, and KO/EN reports are supplied. PDFs are included in the deliverable archive.

Original book: https://doi.org/10.5281/zenodo.23516661 . This research package is not a new GitHub/GitBook/Zenodo release.
