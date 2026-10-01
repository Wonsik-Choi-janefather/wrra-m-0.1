# WRRA-M series corrections, 1 October 2026

This series release retains scientific stage 0.6. It supplies correction r1 of the Korean and English manuscripts for 0.1–0.4, plus public standalone exact verification scripts and captured results. The existing 0.5 and 0.6 manuscripts, models and numerical results are retained.

| Manuscript | Correction | Retained result |
| --- | --- | --- |
| 0.1 and 0.2 | Compact G2's seven is real; complexification and independent left-handed Weyl-channel assignment are separately stated assumptions. Baez's primary representation reference is added. | Exact color multiplicities; conditional 16-channel correspondence, charges and listed anomaly cancellations |
| 0.3 | eta > 0 and nonzero initial target support are explicit convergence conditions. eta = 0 and eta < 0 are distinguished. All-candidate positive support is a model convention. | Two-gap uniqueness theorem, closed-form flow and perturbation bound |
| 0.3 and 0.4 | Known particle assignments may calibrate the model; the provenance of calibrated choices is distinguished from selection calculated from fixed carrier responses. | Exact calculations after inputs are frozen |
| 0.4 | Rank 16 is calculated by exact Gaussian elimination for I16; a rank-15 control and positive neutral norm are checked. Transport Gram rank is separate from the 2D response witness. | Gap identities, constructed gaps 8, 8 and scores 0, −8, −8, −16 |
| 0.4 to 0.5 | Different constructed and tested carriers can respectively have gaps eight and zero. | The symmetric 0.5 carrier does not select the target; no contradiction with the 0.4 construction |

All four verification scripts pass. The 0.3 check enumerates all 6,561 tables with entries in {−1, 0, 1}, finding 961 unique target selections and 2,717 tables with tied maxima. It checks rational flow samples, rate-sign and initial-support boundaries, 256 extreme perturbations, and a tie at the sharp stability threshold. The 0.4 rank calculations return 16 and 15 for the identity and singular control respectively. Existing exact charge and anomaly results remain unchanged.

The Korean and English DOCX/PDF files carry stage labels 0.1-r1 through 0.4-r1. Equation drawings in 0.1–0.3 and the 77 native math objects in each 0.4 manuscript are preserved. The release archive includes both languages for stages 0.1–0.6, this correction record, code, checks and SHA-256 sums. Earlier Zenodo version records remain historical originals; corrected earlier-stage manuscripts are provided in the latest series release.

이번 반영은 0.6까지의 성과를 유지하면서 0.1~0.4 한영 원고의 빠진 가정과 조건을 보강한다. G2 실수 표현과 복소 바일 채널의 연결, 양의 선택속도와 초기 지지, 보정의 정당성과 계산 출처, 직접 계산한 랭크를 명시했다. 0.1~0.3의 독립 실행 검산 코드를 추가하고 0.4의 랭크 계산을 구현했다. 네 검산은 모두 통과했고 기존 전하·이상 소거·격차 결과는 유지된다.

The series correction release DOI is **10.5281/zenodo.23075976**. Its all-version DOI is **10.5281/zenodo.23071877**.
