# WRRA 64-mode expanding conversion v0.3

Wonsik Choi and Jeongin Choi, independent researchers, 20 October 2026.

Read REPORT_EN.md / WRRA_64Mode_Conversion_v0_3_EN.pdf; Korean equivalents are also included.

Python 3.12. Install requirements.txt. The included Linux x86-64 runtime needs libgfortran 5; rebuild elsewhere using gfortran, make and C/C++ tools with `python source/build.py` in a fresh tree. The original CAMB source archive, license and both patches are included.

Execute `python run_all.py`, `python dynamics.py`, `python check_basis.py`, then `python analyze.py`. The first calculates 16 shifted actual-transfer shards, taking several minutes and limiting memory. All 64 exact k values and all integer ell=2..6000 are assembled with no k extrapolation or missing-ell interpolation. Combined D/A transfer arrays are supplied; redundant individual shard NPZ files are omitted from the archive and can be regenerated. Accuracy controls are supplied; run `python review_extension.py` and `python figures.py` for independent controls and plots.

The additional accuracy runs are `python run_transfers.py 2.5 D 50000 32 0` and `python run_transfers.py 3.0 D 50000 32 0`. The supplied original 2.5 comparison file lacks the _o0 suffix; review_extension.py accepts either filename.

New checks: 96 projection/coverage, 15 dynamics, four actual initial-basis checks and eight precision/nonlinear-slicing/Nyquist controls = 123. Previous v0.2's 576 checks are not recounted.

The dynamical closure uses local patches of one universe at leading gradient order. It evolves radiation/matter exchange, pressure work, expansion and tangent curvature, and inserts the generated entropy/radiation curvature into actual CAMB initial bases with the verified sign. The convertible reservoir fraction is calibrated to the adopted observed CDM/radiation ratio. Starting scale, pulse and rate-modulation law are disclosed conditional inputs. A quantized spatial seed is used; a finite-quantum emission-time solver is not supplied.

Full finite-gradient metric/momentum/free-streaming-neutrino matching, ordinary matter reactions, detailed thermal history, nonlinear evolution and a new likelihood remain OPEN. Finite-grid variance coverage is not all cosmic scales or ell>6000 coverage. Prior publication: https://zenodo.org/records/23488763. v0.3 DOI: https://doi.org/10.5281/zenodo.23489547 (registered upon publication).

Provenance and hashes are included. New manuscripts: Wonsik Choi and Jeongin Choi, CC BY 4.0. Preserve the bundled CAMB license for original/derived code and runtime.

## GitHub distribution

GitHub supplies code, pristine CAMB archive and patches, frozen inputs, result JSON and computed complete_projection.npz. Compiled runtime and large/redundant transfer caches are omitted. In a fresh checkout install dependencies, run `python source/build.py`, then `python run_all.py` before the remaining verification commands. Generate both precision controls before review_extension.py. The local reproduction ZIP additionally includes runtime and assembled transfer arrays.
