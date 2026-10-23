WRRA Time-Crystal Responses — standalone paper v1.0
Wonsik Choi (sole author)
23 October 2026

Read publication/WRRA_Time_Crystal_Responses_v1_0_KO.pdf or the EN.pdf edition.
Both are seven pages and contain the input → WRRA transformation → output → falsification sequence.

Internal revalidation: 12/12 verification families passed after fresh isolated replay.
Main scope: finite-time period-doubled rigidity, observation-level comparison and device calibration.
A finite-chain response is reproduced; an asymptotic time-crystal phase and exact apparatus reconstruction are not claimed.
The reused held points are not an independent new experiment. Calibration counts and residual disagreements are retained.

DOI: 10.5281/zenodo.23585846

REPRODUCE
Install requirements.txt in a suitable Python environment.
Obtain https://iontrap.duke.edu/files/2025/03/nature21413.pdf as nature21413.pdf in this directory.
Expected SHA256: 645b138317304e38fbc15a949a741aad6897bd49fca14d4a5a20a39bea08805f.
The publisher PDF is not redistributed.
Run:
  python refine_time_crystal.py
  python verify_release.py
  python finalize_refinement.py
  python write_paper.py

Paper generation additionally needs /usr/local/share/fonts/noto/NotoSansCJKkr-Regular.otf;
adapt the @font-face source in write_paper.py to an installed equivalent if needed.
Intermediate trajectory caches are regenerated rather than distributed.
The input observations and baseline data are in WRRA_Time_Crystal_Observation_v0_5/.
All eight model comparisons, residuals and revalidation records are in WRRA_Time_Crystal_Observation_v0_6/.

REUSE
Original paper and code: copyright 2026 Wonsik Choi; public release under CC BY 4.0 with full attribution.
The extracted experimental aggregate values are attributed to Zhang et al. (2017), DOI 10.1038/nature21413.
Their article's copyright is not relicensed here.
