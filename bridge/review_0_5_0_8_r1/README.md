# WRRA M bridge 0.5-0.8 reviewed r1

Wonsik Choi and Jeongin Choi · 2026-10-03 · CC BY 4.0

The review closes the declared 0.1-0.8 bridge development series. It preserves upstream closure at 0.10 and downstream closure at 0.12. Version 1.0 is consolidation of the executed scope; revisions use r1/r2 without automatic new development stages.

## Result and scientific scope

Verified/frozen inputs -> WRRA address-conditioned state and common internal generator -> nonduplicated SI energy ledger, homogeneous pressure/FRW, ideal measurement and effective spatial feedback -> explicit trace, energy, pressure, clock, current, convergence and dependency checks.

Seven stages pass 1,116 implementation/mathematical case checks. The 0.8 review passes 188 checks (including the previous 36 cross-stage checks once): 1,304 total, zero implementation failures. These counts include provenance and tests of expected limitations; they are not independent experimental confirmations. Eight numerical result JSON files reproduce byte for byte in a clean directory with the recorded numerical environment.

The 0.2 -> 0.3 -> 0.4 energy/pressure path, 0.2 + 0.5 -> 0.6 measurement path and 0.2 -> 0.7 occupancy-feedback path actually execute. Perturbing the 0.7 clock and measurement snapshots changes no numerical field result: they are provenance only. Perturbing the actual population changes the field. The 0.7 density has equal occupancy source weight for both internal components, not the full SI stress-energy source. Thus there is no claim that all stages form one autonomously coupled covariant simulator.

The ideal 0.6 readout increases internal population to 1/2 and consumes finite work. The 0.8 boundary diagnostic inserts that mean write work into the existing 0.3/0.4 matched-population ledger once, keeping record energy separate and opposing controller supply explicit. For the inherited/proton reference, total supply is 7.037871284040674e-12 J per reference 1 m3, leaving 5.237112150317267e-13 J in the diagnostic reservoir. External q changes to -0.5191967280747398; when the pressureless reservoir is included, q stays -0.518507515893292. This is a conditional finite ledger calculation after a write, not a time-resolved apparatus, repeated reset cycle or spatial geometry.

Known-value reproduction is an explanatory and consistency result. With verified inputs and construction choices fixed, unmeasured outputs are conditional WRRA model predictions. Rate, apparatus, abundance and spatial SI/covariant adapters remain explicit open interfaces; old slow-clock identity failure is retained. See final_issue_register.json for all ten original issues and results.json for evidence. The review directly reads original result payloads from historical/bridge_0_8_original.zip to verify unchanged scientific outputs. Changes: relative SI-Hermitian check, full-H two-mode invariance/generator projection, spectral kinetic-versus-gradient energy and quantitative density/energy refinement. See REVISION_r1.md and numerical_comparison.json.

## Reproduce

```sh
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 python reproduce_all.py
```

Run from this directory or use its absolute script path. The orchestrator removes any external WRRA_REPO selection for subprocesses, uses the bundled frozen source, forwards newly generated state/basis and clock/result files in dependency order, and runs four isolated input sensitivity probes. It preserves historical stage results byte for byte and fails if the frozen numerical result hashes change. Cross-platform numerical dependencies can alter floating-point bytes; use environment.json for the exact reproduction environment. A legitimate changed result requires a reviewed revision of the frozen reference, not silently replacing its expected hash.

Results: results.json. Clean replay: clean_replay.json. Inputs and stage code: studies/. Issues: final_issue_register.json. SHA256SUMS covers the delivered files. Prior stage documents inside studies are historical stage descriptions, with their at-the-time open issues; the 0.8 report and issue register carry the final reviewed status.

## PDFs and prior public sources

Korean and English reports are included. To rebuild them, install reportlab, supply NanumGothic through WRRA_FONT_PATH if needed, then run build_reports.py. Numerical replay does not require PDF dependencies or the font.

- Reviewed bridge 0.1-0.4 r1: https://doi.org/10.5281/zenodo.23119802
- Upstream integrated 1.0-r1: https://doi.org/10.5281/zenodo.23119041
- Downstream reviewed 0.10-0.12: https://doi.org/10.5281/zenodo.23113101
- Repository: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1

Reviewed release DOI: https://doi.org/10.5281/zenodo.23120693 . Repository release directory: bridge/review_0_5_0_8_r1 . This collection preserves the original 0.5-0.8 packages in historical/. It does not claim journal submission or acceptance. Bundled inherited material retains its recorded provenance.
