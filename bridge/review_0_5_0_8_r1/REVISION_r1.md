# Bridge 0.5-0.8 review r1

Verified/frozen input -> WRRA transformation -> outputs -> falsification conditions are retained in both reports. Known-value reproduction remains an explanatory achievement; fixed-input unmeasured outputs are conditional model predictions.

- 0.5: replace the default absolute Hermitian matrix comparison with a relative matrix norm at the actual SI energy scale; verify calibration/energy scale. Checks 133 -> 134.
- 0.6: verify the inherited full 95D Hamiltonian's Hermiticity, invariant two-mode subspace, projected relative generator and initial excitation energy. Checks 83 -> 87.
- 0.7: verify spectral kinetic Hermiticity and matrix-versus-gradient energy equality; check quantitative second-order density and dynamic-energy refinement. Define the discrete continuity derivative as cell mass, d(dx*rho_i)/ds. Checks 40 -> 51.
- 0.8: replay current dependencies, read original result payloads directly from the archived original 0.8 ZIP, preserve all ten issue IDs and keep B09/full covariance open. Review checks 179 -> 188.

All scientific numerical payloads remain identical. Versions, checks, provenance hashes and continuity notation change intentionally. Stage 0.1-0.4 r1 source/result payloads are unchanged. Original 0.5-0.8 ZIPs remain in historical/.

Total: 1,116 stage checks + 188 review checks = 1,304 (25 added over the original 1,279). Current 0.5-0.7 stages contribute 272, prior dependency stages contribute 844. The prior 36 cross-stage checks are included once in the 188 review checks. Case counts are implementation/mathematical/provenance checks, not independent experiments.

Eight current result JSON files reproduce byte for byte in a clean directory with the recorded numerical environment. Physical driver selection, autonomous preparation/readout apparatus, durable medium/reset, coherent transition currents and full SI covariant geometry remain open. Clock/measurement snapshots in 0.7 are provenance only, confirmed by isolated perturbations; this review does not reinterpret them as executed couplings.

Upstream 0.10, downstream 0.12 and bridge 0.8 closure remain fixed. 1.0 consolidates the reviewed scope; corrections use r1/r2.

Release DOI: https://doi.org/10.5281/zenodo.23120693
Repository directory: bridge/review_0_5_0_8_r1
Authors: Wonsik Choi and Jeongin Choi.
