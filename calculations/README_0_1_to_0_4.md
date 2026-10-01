# Exact verification for WRRA-M 0.1–0.4

Run from the repository root with Python 3.10 or later. These four scripts use only the standard library.

```bash
python calculations/verify_wrra_m_0_1.py
python calculations/verify_wrra_m_0_2.py
python calculations/verify_wrra_m_0_3.py
python calculations/verify_wrra_m_0_4.py
```

| Version | Verification input | WRRA-specific transformation | Output | Falsification |
| --- | --- | --- | --- | --- |
| 0.1 | Established complexified G2-to-SU(3) branching; calibrated hypercharges | Two seven sectors plus one invariant channel | Color multiplicities 2, 2, 3; dimension 15; benchmark anomaly sums zero | Character or dimension mismatch, or later incompatible channel assignment |
| 0.2 | Independent complex left-handed Weyl channels, declared cross pairing, two charge normalizations | One operator Y = T3R + (B−L)/2 | Six field-group charges and electric charges; local anomaly sums zero; both SU(2) doublet counts even | Charge relation, anomaly sum or parity failure |
| 0.3 | Four filters and eight fixed scalar entries | Score differences and constant-score selection flow | Three coefficient identities; all 6,561 finite tables; rate-sign/support cases; 256 perturbation vertices | Gap/flow/support or declared stability-condition failure |
| 0.4 | Carrier responses and one positive mismatch metric | Negative squared mismatch becomes two alignment products | Exact gaps 8, 8 in the constructed witness; explicit Gaussian-elimination rank 16 and rank-15 control | Identity failure, inadmissible transport, or nonpositive gaps for a positive-selection claim |

The scripts print JSON records. Captured results are in `results/wrra_m_0_1_to_0_4/`. The 0.3 finite table count is 3^8 = 6,561: each of eight entries takes one of −1, 0, 1. There are 961 tables selecting F_DX uniquely and 2,717 tables with tied maxima. These finite checks support the manuscript's general algebraic proof, rather than proving an unrestricted theorem by enumeration.

The 0.3 flow samples use exp(eta t) = 2^k with integer scores, so probabilities, score-ratio laws and sampled convergence bounds are checked with exact fractions. Positive rate drives the maximum-score weight upward; zero rate fixes weights; negative rate drives the minimum-score weight upward. Zero initial target support remains zero. The continuous-time convergence theorem assumes eta > 0 and nonzero initial target support. Positive support for all four candidates is a model convention used to compare every candidate, not a stronger mathematical necessity for target convergence.

The G2 branching is an established input. The code does not derive physical chirality: real-to-complex representation passage and assignment of independent left-handed Weyl fields are separate physical assumptions. The 0.1 anomaly benchmark uses calibrated known charges; 0.2 generates its charges from one operator under the stated normalization and pairing inputs.

Known particle assignments may legitimately calibrate the compatibility tables or carrier metric. Record calibration provenance separately from a selection calculated using carrier responses frozen before evaluating the target. After inputs are fixed, scores, gaps and conditional consequences are calculated in either case.

The 0.4 two-dimensional response witness is separate from its sixteen-dimensional transport-Gram example. Rank 16 is now directly calculated for I16, with a singular rank-15 control. This does not establish that a microscopic physical carrier has rank 16. The constructed gaps 8, 8 and the symmetric carrier's tested gaps 0, 0 in 0.5 use different response assignments and are compatible.

네 코드는 Python 표준 라이브러리만 사용한다. 0.1·0.2의 색 계수와 전하·이상 합, 0.3의 6,561개 표와 속도 부호·초기 지지·섭동 경계, 0.4의 격차 항등식과 직접 계산한 랭크를 재현한다. 복소화와 손지기성 배정은 물리 가정으로 명시하고, 알려진 입자 배정을 이용한 정당한 보정과 고정 전달자 응답에서 계산한 선택의 출처를 구분한다.
