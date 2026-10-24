# WRRA — five discussion follow-ups, v1.0

This package executes scoped additions arising from six Moltbook discussions. The author-approved order is: (1) directional receiver resolution, (2) next-execution readiness, (3) resource-limited choice, (4) verification controls, (5) information retention.

## Results and reading

- Cosmos, verification and information: [한국어](docs/cosmos_KO.md) · [English](docs/cosmos_EN.md)
- Life readiness: [한국어](docs/life_KO.md) · [English](docs/life_EN.md)
- Neuropsychology: [한국어](docs/neuro_KO.md) · [English](docs/neuro_EN.md)

Original books and authors are credited in each supplement. No frozen Core is modified. Every claim follows inputs → WRRA transformation → outputs → falsification → conclusion. The standard Laplacian and information theory are adopted ingredients, not renamed WRRA inventions.

## Execution

Python 3.11 or later, NumPy, mpmath.

```bash
python run.py
python verify.py
```

The first command exports four domain result files. The second runs 52 separately named checks including 16 corrupted/missing-evidence controls and writes verification.json. The same workflow performed both calculations; this is not independent human review.

Inherited finite_scale_bridge_v0_1 was separately rerun with its original frozen inputs: 179/179 and modal/Parseval PASS. In the full repository its commands are `python publication/WRRA_Five_Reinforcements_v1_0/modules/finite_scale_bridge_v0_1/compute.py` and `python publication/WRRA_Five_Reinforcements_v1_0/modules/finite_scale_bridge_v0_1/verify.py`. Run inherited scripts in a copy because they overwrite their local outputs. `inputs/finite_scale_original.py` is a source snapshot, not a standalone rerun without the inherited input files.

Scope: finite receiver extension, synthetic audit execution, hypothetical choice model, listed verifier controls and finite information retention. Not full Lorentz covariance, cell self-reproduction, human validation, FEP integration, device energy measurement, or whole-cosmology execution. The online supplements do not silently replace archived book PDFs or claim a new Zenodo DOI.
