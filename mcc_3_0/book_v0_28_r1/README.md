# Minimal Computing Cosmology 3.0 — Book v0.28-r1

Wonsik Choi and Jeongin Choi · 22 October 2026.

Complete bilingual book: https://doi.org/10.5281/zenodo.23549809 (see publication status). Previous edition: https://doi.org/10.5281/zenodo.23524780.

Adds Sections 132.6, 133.4, 134.5 and Appendix H.6 to the preserved v0.28 book. Five recovered original programs exit 0, four available historical JSON outputs match, and 25 original internal file hashes match. An isolated archive corruption is rejected with exit code 1. These finite program/file checks are not independent experiments, an RH proof, or a completed whole-model execution.

Originals and actual replay logs: [pinned recovery](https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/e5a833afd65c282b06fa1318467362de90156338/mcc_3_0/chapter_132_134_recovery_2026_10_22).

Run `python ../chapter_132_134_recovery_2026_10_22/reproduce.py` for finite source replay. Run `python review/integrate.py` to reconstruct the revision from the bundled v0.28 text baselines, then `bash review/render.sh` to render both books (Pandoc, XeLaTeX and Noto Sans CJK KR required). `review/INTEGRATION_AUDIT.json` verifies exact inverse removal restores each baseline. All 50 image references are retained. The full books keep the original 139 numbered chapters and their historical scope.

`evidence/` preserves the recovered five originals. Earlier historical archives remain at their established repository paths; this directory is not a replacement for every historical data archive. The PDF files are distributed on Zenodo. Source Markdown, media, rendering tools and editorial audit are here.
