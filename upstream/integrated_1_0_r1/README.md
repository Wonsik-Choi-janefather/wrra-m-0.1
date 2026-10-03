# WRRA M upstream integrated manuscript 1.0-r1

Authors: Wonsik Choi and Jeongin Choi. Correspondence: janefather@gmail.com. ORCID: 0009-0001-4263-9772.
DOI: https://doi.org/10.5281/zenodo.23119041

Upstream development closes at 0.10. This is its integrated reviewed research edition.
The Korean and English manuscripts retain 24 native equations and four tables.

## Review changes

- Distinguish dimensional magnetic readouts M from dimensionless Sachs G_M.
- Distinguish scalar Actual stock A from the admission operator A.
- Identify q0=-0.523 as the V0 reference result; energy fractions evolve with volume.
- Identify fixed-input unmeasured readouts as conditional WRRA predictions within their declared physical mapping.
- Cite the coauthored Physics preparation r9/r8 as prepared manuscripts.
- Add the release DOI, bilingual files, reproduction sources and SHA-256 manifest.

## Reproduction

Python 3 with NumPy, SciPy and mpmath is required for calculations.
Extract sources/upstream_0_4_0_6_r1.zip and run its reproduce_all.py.
Extract sources/upstream_0_7_0_10_r1.zip and run its reproduce_all.py.
These executions passed 395 and 1395 implementation/mathematical checks in this review.
Extract sources/physics_preparation_r9_r8.zip into a separate folder.
Run review_r8/vacuum_reference_check.py, twist_bridge_check.py and phase_ledger_check.py in that order; 33, 12 and 38 checks passed.
The original first three particle/filter stages are contained in that Physics source archive and cited at DOI 10.5281/zenodo.23092499.
The verification directory records this review's actual re-execution results.
Archive manifests remain the original release manifests; current replay records are stored separately.

To rebuild editable documents from this package root, install python-docx and lxml,
install Pandoc plus NanumGothic and Latin Modern Math fonts, and run:
python tmp/synthesis_r1/build.py
Use LibreOffice to convert the resulting DOCX files to PDFs.

## Evidence and scope

Verified inputs → WRRA transformations → output → falsification conditions are presented in the manuscripts.
Known-input reproduction is an explanatory achievement; conditional unmeasured readouts after fixing the model are WRRA predictions.
Check counts are implementation and mathematical audits, not independent experimental observations.
Physical clock, excitation supply, species selection and durable recording retain their declared interfaces.
Before journal submission, the authors should complete the journal-specific affiliation, funding and competing-interest declarations.
This Zenodo release is a preprint, not a journal acceptance or submission.

Papers and documentation: CC BY 4.0. Bundled sources retain their original licenses and provenance.
