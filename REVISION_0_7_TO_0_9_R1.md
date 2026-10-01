# WRRA M 0 7 to 0 9 review and correction record

Wonsik Choi / 최원식. Reviewed 2026-10-02. Series version 0.9-r1.
DOI: https://doi.org/10.5281/zenodo.23091892
Concept DOI: https://doi.org/10.5281/zenodo.23071877
Reviewed base commit: 0a5d8c579ea143bd0982e80ed5e22d91eab6c65b.
WRRA Core 1.0 and MCC 2.3.2 remain the baseline.

The review corrects numerical boundary handling and synchronizes the executable roadmap, Korean and English manuscripts, calculation tables and release metadata. Adopted inputs and canonical configuration hashes remain fixed. Floating-point normalization may change low-order numerical digits; the separately recorded comparison checks preserve the published reference values and exact charge assignments.

| Component | Verified correction | Completion evidence |
| --- | --- | --- |
| 0.7-r1 | Retain every positive load instead of deleting values below 10^-13. Normalize trace after accepting representation roundoff; reject negative density eigenvalues above machine roundoff. Use the same effective Jc and Jb in energy and gravity accounting. | 19 check groups. With phenotype 10^-15 and a zero carrier mode, the ledger retains the load and gives H/H0 = sqrt(10^-15). A trace perturbation of 9×10^-11 is normalized. |
| 0.8-r1 | Use logarithms for filter weights and the sufficient selection time, avoiding overflow of the initial-support ratio. | 23 check groups. Positive F_DX support 10^-320 converges; exactly zero winning support remains unselected. Exact charges and anomalies agree; all nine reference states select F_DX. |
| 0.9-r1 | Sum disjoint conditional channel contributions directly, replacing subtractive override corrections that could create negative roundoff. | 27 check groups. Twenty exhaustive sparse-kernel cases preserve positivity, zero support and the phenotype budget. The common arithmetic totals are unchanged. |

## Scope and denominators

0.7–0.8 use the inherited physical energy fractions 4.93%, 26.5% and 68.57%. The 0.9 address ledger uses the common arithmetic calibration 5%, 26.8% and 68.2%. Their physical conversion is a 0.10 task. Neither ledger silently overwrites the other. The alpha=2 and alpha=1.9 comparison rows use different measures and are never combined.

Resident upstream Actual is phenotype plus resident nonphenotype, totaling 31.8% of the original address denominator. Complete downstream accounting additionally carries the returned provenance in the background-response branch, totaling 100%. This bookkeeping does not yet calculate how that return maintains physical background energy. Pressure requires an energy-volume function; length requires physical load, response and geometry with boundary conditions.

The particle inventory contains 45 Standard-Model chiral components and three conditional neutral extension slots. The neutral slots are construction inputs, with no measured mass or occupation claimed. Filter optimizer weights and address admissions are calculation weights; physical measurement probabilities, outcomes and records remain for 0.13. Global twist record magnitude remains a current-state aggregate, with no new temporal accumulation law. Existing load-to-expansion calculation is distinguished from a future causal derivation of expansion from twist.

## Synchronized development order

0.9 common arithmetic ledger and upstream contract → 0.10 address energy and pressure → 0.11 sequential physical calibration G, H0, phenotype fraction, clustering fraction and electron mass energy → 0.12 shutter, proper time and allowed spectra → 0.13 physical quantization and records → 0.14 cutoffs, capacity and uncertainty → 0.15 stress, twist, curvature and size → 0.16 neutrino masses, mixing and oscillation → 0.17 propagation in the shared geometry → 1.0 integrated execution and claim freeze.

Each stage closes through verification input, WRRA-specific transformation, output and falsification conditions. Known values legitimately calibrate the constructed our-universe model. Reproducing those inputs is explanatory reproduction; later unmeasured outputs from the fixed model may be predictions. Microscopic origins of upstream rules remain subsequent upstream work.

## Reproduction and publication

Run `python calculations/wrra_m_0_7/run_release.py`, then the corresponding 0.8 and 0.9 commands. The 69 check groups include inherited exact 0.1–0.4 checks, numerical carrier and selection probes, energy and pressure accounting, common-address transport, source hashes and regression comparisons. All three individual archives remove captured numerical outputs before a clean-copy run and compare output bytes. The series archive includes the revised editions and code together with the preserved 0.1–0.6 release material. SHA256 manifests identify packaged bytes.

The bilingual editions retain 11, 15 and 12 matching native equations for 0.7, 0.8 and 0.9. Tables are checked against generated results; every final page is rendered and inspected before publication. Details are recorded in `review/0_7_to_0_9_r1/review_checks.json` and each component's document and reproduction reports.

## 한국어 교정 요약

0.7의 작은 양의 부하 삭제, 0.8의 작은 초기 지지 비율 계산, 0.9의 희소 채널 재배정 반올림을 수정했다. 검증 묶음은 각각 19개·23개·27개로 총 69개다. 입력 해시와 채택한 기준값·전하 배정을 유지하면서 한영 원고·실행 결과·재현 압축파일을 갱신했다.

0.7~0.8의 에너지 구성비와 0.9의 산술 구성비, 잔존 Actual 31.8%와 전체 장부 100%의 범위를 명시했다. 양자화와 물리 관측 기록은 최신 계획의 0.13으로 맞췄다. 0.10 이전에는 복귀 68.2%를 물리 압력값으로 표시하지 않는다. 기존 0.1~0.6 자료를 보존하고 같은 Zenodo 계보의 0.9-r1로 공개한다.

Copyright 2026 Wonsik Choi. CC BY 4.0.
