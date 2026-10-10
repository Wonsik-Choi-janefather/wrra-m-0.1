# Record Capacity and Irreversibility in a Finite-State Model — v0.2

Subtitle: Conditions for Residue Accumulation and Overflow in WRRA

Authors listed in the manuscript: Wonsik Choi and Jeongin Choi.
Date: 2026-10-10.

## Main result

The model distinguishes adequate local response from preservation of every history distinction. A two-state parity residue preserves a declared response of sixteen four-bit histories. The remaining eight-way distinctions can accumulate in a finite residual tape. Three octal cells admit three transfers; under fixed pointer/flag semantics, the fourth transfer cannot preserve the distinctions and clear the incoming register. With one preoccupied cell, this happens on the third new transfer. The STALL policy keeps the incoming digit; OVERWRITE is eight-to-one and requires additional outputs for reversible completion.

The philosophical interpretation is minimum-computation cosmology: an adequate state need not be a perfectly restorative or uniquely privileged universe. Physical completed infinity is assigned Null as an adopted premise. The proved minimum is query-relative record capacity, not a minimum of the universe's total computational cost.

## Reproduce

Use Python 3 with NumPy and Matplotlib. Exact package versions used are in requirements.txt and environment.txt.

    python -m pip install -r requirements.txt
    python reproduce.py

After dependencies are installed, the calculation needs no network. It overwrites results.json, figure.png and accumulation.png. All 38 checks passed in the reported environment. Numeric rounding can vary slightly across platforms. The checks support, and do not replace, the manuscript's proofs. The script enumerates actual accumulation outputs and overwrite preimages.

## Files

- WRRA_Record_Capacity_v0.2_EN.docx / .pdf: English manuscript.
- WRRA_Record_Capacity_v0.2_KO.docx / .pdf: Korean counterpart.
- manuscript_en.md / manuscript_ko.md: editable text sources.
- reproduce.py, results.json: computational model and outputs.
- figure.png: history/response capacities and thermal ledger (Figure 2).
- accumulation.png: residual-load threshold (Figure 1).
- build_documents.py: DOCX builder; additionally requires python-docx, Pillow and Noto Sans CJK KR for Korean. PDF conversion requires LibreOffice. The research calculation does not require these document dependencies.
- REVISION_NOTES.md: changes following an independent simulated review.
- SHA256SUMS.txt: checksums of packaged files, excluding itself.

## Scope and submission status

The preparation pair is reproduced from the sixth WRRA manuscript, Zenodo DOI 10.5281/zenodo.23270998. Counting, reversible completion, finite-reservoir Landauer accounting and majorization are established tools, not claimed as new laws. The present contribution is their linked finite application to response sufficiency, residue and overflow.

The finite tape and full-support thermal auxiliary are separate resource regimes. No reservoir is assumed to be infinitely reusable. The input source, preparation and actuator remain external to the controlled model. An autonomous mechanism coupling overflow to a new physical preparation or cosmic renewal has not been derived. The toy STALL event does not change the susceptibility.

This is a research preprint v0.2 prepared for public archiving; it is not a peer-reviewed journal publication. Astra review is not an actual journal review or an acceptance decision. Target journal suitability remains subject to substantive editorial assessment. Before submission, author affiliations, corresponding-author details, funding/conflict declarations, author contributions, approval of the final text, and the journal's current assistance-disclosure requirements must be completed with the authors. They have not been invented in the manuscript.

## Numerical metadata

`query_tolerance: 0` denotes the exact-response task, and `exact_response_states: 2` its record size. JSON numbers are raw NumPy floating-point outputs; printed response differences in the manuscript use stable rounded digits. The thermal bath uses beta = 1 and unit energy spacing (beta times energy spacing = 1).
