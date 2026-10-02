# WRRA M upstream 0.6 — finite currents and beta corrections

Author: **Wonsik Choi / 최원식** · ORCID **0009-0001-4263-9772** · 2026-10-03

This release extends the same bounded spatial state from upstream 0.5 with actual finite-momentum monopole electromagnetic and weak currents, a disclosed joint charge-radius calibration, projected continuity controls, and recoil/radiative beta-decay calculations. It preserves the original 0.5 Hamiltonian implementation and existing published stages.

## Results and calibration status

| Quantity | Result | Role |
| --- | --- | --- |
| Common spatial width ℓ | 0.65715059784 fm | Jointly refitted using both charge radii |
| Zero-charge isovector radius counterterm cE | −0.09708290347 fm² | New disclosed fitted constitutive input |
| Proton Sachs charge radius | 0.84075 fm | Calibration return |
| Neutron Sachs mean-square radius | −0.1155 fm² | Calibration return, not independent prediction |
| Neutron magnetic radius | 0.83198710743 fm | Unfitted mismatch with PDG 0.864 +0.009/−0.008 fm |
| Full beta-rate ratio to frozen parent allowed approximation | 1.03792926261 | Exact tree recoil plus stated leading radiative scheme |
| Lifetime with unchanged parent κ=12.200294834431 | 846.20410238025 s | Frozen-normalization control |
| Separately refitted κ | 11.97530126586 | Returns input lifetime 878.3 s |
| Refitted κ²R | 1.00184722367 | Lifetime normalization, not a new weak-strength prediction |

The 84 implementation checks and 24 independent audits pass (108 total). Numerical reproduction and empirical agreement are separate claims. The finite-Q² curvature has not been fitted to scattering data and depends on the disclosed regulator aE/ℓ=0.5, 1, or 2.

## Exact conventions

- The inherited point charge is a **Sachs charge ansatz**. A Foldy term is not added to it a second time. Sachs form factors are completed first and then converted to Dirac/Pauli form factors.
- Magnetic moments remain in μN=e/(2mp). Dirac/Pauli conversion uses the common mass M̄=(mp+mn)/2, with GM multiplied by M̄/mp. Thus F2V(0)=3.70913344989. Physical masses remain in the decay phase space.
- Weak CVC is checked using independent n→p slot operators in the same-state, common-mass isospin convention. Longitudinal continuity is a finite projected completion J_L=[H,ρ]/q, not a full covariant gauge derivation.
- The weak vertex uses q=pp−pn and +iF2Vσq/(mp+mn)−GAγγ5. Small timelike form factors use first-order analytic continuation Q²=−t of the computed slopes.
- The Coulomb function is inherited. Leading Sirlin electron-inclusive outer radiation is **added to the leading allowed spectrum**. The inner reference is the explicitly frozen 2018 value ΔRV=0.02467(22), not a claim about the latest evaluation. The empirical axial/vector ratio is renormalized.
- Higher QED, complete mixed radiative recoil, induced pseudoscalar/second-class currents, dynamical isospin breaking and a microscopic hadronic γW box are omitted. No complete 10⁻⁴ precision claim is made.
- The direct magnetic b² coefficient is a declared free input, dB=0 at baseline and ±0.0001 MeV⁻¹ in controls. Internal response is not identified with complete experimental polarizability.

## Reproduce calculations

Tested runtime: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0.

```bash
python3 -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=2 python3 code/compute.py
OPENBLAS_NUM_THREADS=2 python3 verify_release.py
```

`compute.py` recomputes the shared 0.5 state and finite currents; it writes `code/results.json`. `verify_release.py` includes explicit spinor sums independent of the trace implementation, heavy-mass normalization/angular-correlation tests, adaptive radiative integration, regulator controls, invalid-input checks and a fresh-directory byte comparison. It writes `verification.json`.

The decay code computes rates from GF, Vud, κ²R, the phase integral and ℏ; the refitted lifetime is obtained from that rate, rather than being hardcoded as the returned result. The result ledger rounds serialized numerical values to 11 decimal places; test decisions use unrounded values.

## Paper and source

The Korean manuscript is `manuscript_KO.md`; editable native-equation Word and rendered PDF files are under `paper/`. `source/note.py` reads the executed result ledger, and `source/build_doc.py` builds the paper and scientific figures.

```bash
python3 -m pip install -r source/requirements.txt
python3 source/build_doc.py
```

Paper generation additionally requires Pandoc, NanumGothic and Latin Modern Math; PDF rendering uses LibreOffice. `document_checks.json` records the inspected layout and native equation/table counts. `SHA256SUMS` records release payload hashes. The reproduction archive contains the paper, inputs, code, result/audit ledgers and manuscript sources. Render QA images and transient caches are excluded.

## Provenance and next input contract

Baseline: [upstream 0.5 at 8ac07a7](https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/8ac07a7d33dcc29701e49d31650997ec77030eb6/upstream/spatial_scale_v0_5). Original Core 1.0, MCC 2.3.2 and downstream stages remain separate. Full source attribution, baseline hashes and exclusions are recorded in `source/provenance.json` and `code/inputs.json`.

The next stage must keep fitted radius returns distinct from predictions, preserve the explicit common-mass convention, distinguish frozen and separately refitted κ, and test finite-Q² currents against external data. The remaining magnetic-radius mismatch and unspecified charge curvature are retained as revision targets. This stage is published on GitHub; the final upstream integration is the intended next Zenodo edition.

License: CC BY 4.0 (see `LICENSE`).
