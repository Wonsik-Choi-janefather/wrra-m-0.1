# Natural-number dimensional execution layers - v0.1

Wonsik Choi · Independent Researcher, Seoul · 16 October 2026

**최상류 1차원수 / 중간 2차원수 / 마지막 표현형 3차원수**

For each active integer address n >= 2, use this ordered readout:

```text
if is_prime(n):  dimension = 1
elif n % 2 == 0: dimension = 2
else:           dimension = 3
```

Primality is evaluated first, so 2 is 1D. Address 1 is the inherited inactive vacuum reference.

The declared WRRA interpretation assigns primes to the upstream layer, even composites to the intermediate resident-nonphenotype layer, and odd composites to the final phenotype-eligible layer. Actual phenotype admission is computed separately.

## Contents

- [Korean research note](WRRA_Number_Dimension_Layers_v0_1_KO_2026-10-16.pdf)
- [English research note](WRRA_Number_Dimension_Layers_v0_1_EN_2026-10-16.pdf)
- `manuscript.json`: editable bilingual source.
- `NOTE_KO.txt`, `NOTE_EN.txt`: accessible text editions.
- `reproduce.py`, `results.json`: full finite-domain replay and topology incidence checks.
- `build_pdf.py`: PDF generation source.
- `REPORT_KO.txt`: detailed computation memo.
- `BASELINE_EXCERPT_KO.txt`: inherited model contract from MCC 3.0 v0.20.
- `SHA256.json`: release file digests.

## Result and scope

For N = 1,015,000 (active addresses 2 through N):
1D: 79,608; 2D: 507,499; 3D: 427,892.

The inherited weights and actual four-mode/eight-frame admission reproduce
P / D / R = 5% / 26.8% / 68.2% with alpha and h unchanged.
These are calibrated address fractions. The new dimension interpretation does not itself determine mass-energy density, pressure, particle mass, or transition dynamics.

One optional topological realization uses intervals, annuli, and parity-reversed quotient bands. Its dimensions are minimum **ambient embedding dimensions**; a Mobius band remains intrinsically two-dimensional. The topology assignment and parity seam are declared model rules. They do not establish the universe's boundary or volume.

## Reproduce

```sh
python3 reproduce.py --output results.json
```

The numerical replay requires NumPy and SciPy. Exact environment versions are recorded in results.json.

For PDF generation, install ReportLab and obtain NanumGothic-Regular.ttf from the official Google Fonts source:
https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Regular.ttf

Place it in `fonts/NanumGothic-Regular.ttf`.
SHA-256: 76f45ef4a6bcff344c837c95a7dcc26e017e38b5846d5ae0cdcb5b86be2e2d31.
Then run `python3 build_pdf.py`. Published PDFs embed their used font glyphs.
The external font is licensed under SIL OFL 1.1; see FONT_OFL.txt.

## Provenance and license

Baseline: Minimal Computing Cosmology 3.0, Book v0.20, Chapters 39, 46, 75.
https://doi.org/10.5281/zenodo.23382565

Topology:
https://www.open.edu/openlearn/science-maths-technology/mathematics-statistics/surfaces/content-section-3.2
https://www.open.edu/openlearn/science-maths-technology/mathematics-statistics/surfaces/content-section-2.3.2

Comparison target background:
https://www.esa.int/Science_Exploration/Space_Science/Planck/Planck_reveals_an_almost_perfect_Universe

Original notes, code and data: CC BY 4.0, copyright 2026 Wonsik Choi.
Third-party font: SIL OFL 1.1. The inherited book excerpt is attributed to Wonsik Choi and Jeongin Choi.

