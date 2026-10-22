# Chapters 132–134: original-source recovery and finite replay

## 검증 입력 / Inputs

Recovered on 2026-10-22 from the original 76,970,934-byte `MCC_3_0_Book_v0.24_Projector_Focus_Complete_Package.zip`, SHA-256 `09e8f19d163931792b501e36ba6f070d2745916065a592925bfd829cf3072b93`. Five R1–R5 ZIPs are preserved byte-for-byte under `evidence/`; nested earlier studies remain inside them. Original 2026-10-17 replay records are under `verification/`, new outputs under `runs_2026_10_22/`.

Public main at `0c3f22619c96114ff88779f237dbbefe217dbd7a` had no `riemann_connection_2026_10_17` or `projector_focus_2026_10_17` paths. The v0.25 publication commit `abab705e68` included the book text and older zeta-output archives, but omitted these two evidence directories. Zenodo v0.28 (23524780) contained only the two complete-book PDFs. The preserved v0.24 package contains all five sources. Thus this was a public packaging omission, not absence of original research code. The precise historical cause of the selection is unknown.

## WRRA 고유 변환 / WRRA transformation

Chapter 132: declared moment coefficients → logarithmic-derivative relation coefficients → two Hankel determinants; the separate growth-barrier kernel supplies an exact negative quadratic witness. These are conditional algebraic diagnostics, not a proof of actual xi positivity.

Chapter 133: prime construction → odd-address Euler products → composite projection; common-coordinate carrier gains distinguish minimax centering from componentwise norm preservation. Synthetic beta values are controls, not measured zeta zeros.

Chapter 134: complementary all-natural amplitudes → mode-resolved pair energy and visibility → finite focus/cost optimum. Raw coherent pixel intensity and empirical optical image quality are different observables.

## 산출값 / Outputs

All five recovered programs executed with exit code 0. Four programs' JSON stdout matches the preserved 2026-10-17 replay stdout. `exact_check.py` has no corresponding historical stdout in that directory; its exact assertions passed in this new execution.

- `exact_check.py`: determinants `3/25`, `-223/70000`.
- `projector_contract.py`: centered gain 1; symmetric off-line diagnostic central worst gain 2, outer centers 4; gain product 1 and mean 5/4.
- `analyze_odd_hologram.py`: exact projection and Euler-address checks pass at N=1000.
- `clarity_analysis.py`: N=1000, central pair energy 14.97094172110069 and visibility 1; endpoint energy 1001.6439345666815 and visibility 0.014946370865388635.
- `certify_double_exponential_counterkernel.py`: outward witness interval approximately [-8.750604288241009e-9, -8.750061502880118e-9], strictly below -1/200000000, for the separately declared kernel.

The exact interval certificates, rather than their decimal displays, carry the enclosure. `REPLAY_RESULT.json` records an additional clean temporary-directory replay and original internal checksum checks. Original certificates match replayed certificates.

## 반증조건 / Falsification

Run `python reproduce.py` from this directory (Python standard library only). It rejects missing or altered archived inputs/results by SHA-256, verifies the original internal manifests, executes the original scripts in temporary directories, and compares parsed outputs and certificates. It does not trust historical PASS labels. A nonzero process status, assertion failure, checksum discrepancy, or output discrepancy fails the replay.

This replay verifies declared finite calculations, not every analytic argument in the chapters. Nested historical programs are preserved but were not all rerun. The full xi/theta all-order positivity, RH, physical optical quality, and full MCC 3.0 end-to-end execution remain unresolved by this package.

## 결론 / Conclusion

The five originals are recovered and the cited top-level finite calculations are reproduced. The missing relative evidence paths are restored under book_v0_25, book_v0_26, book_v0_27 and book_v0_28. Original book/PDF text and original source bytes are not revised. This supplements the previous full-model audit: its “132–134 source packages unavailable” limitation is now resolved, but its other findings and whole-model execution limitations remain.
