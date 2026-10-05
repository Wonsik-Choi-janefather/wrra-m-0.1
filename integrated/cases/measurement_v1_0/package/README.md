# WRRA M Integrated Measurement Case 1.0

Wonsik Choi and Jeongin Choi · 5 October 2026

Principal manuscript: https://doi.org/10.5281/zenodo.23126800

This review sample executes address conditioning, one ideal finite record, reference-matched SI energy, and pressure/deceleration from the same energy expression. It uses the integrated research only. The separate prime-parts assembly model supplies no mathematical or physical input.

## Reproduce the fixed case

Use Python 3.12 with the dependency versions in `requirements.txt` (the tested environment is recorded in `runtime.json`).

```sh
python -m pip install -r requirements.txt
python reproduce.py --out replay
```

The command checks the unchanged frozen source archive hash, extracts into the output directory, replays original bridge stages 0.2, 0.3, 0.5 and 0.6, and forwards their fresh state and basis. It then computes the selected case and checks it against the published integrated boundary diagnostic in `reference_boundary.json`.

Success: original stage checks 95 + 134 + 134 + 87 = 450; case connection checks 26; failed checks 0. Original checks include other controls and are not all distinct measurements of this case. These are software checks, not experimental evidence. Dependencies require an ordinary package installation if absent; the model run itself makes no network requests.

`inputs.json` is the fixed case selection and provenance manifest. The numerical model inputs are frozen inside the included original archive. Unsupported selections are rejected rather than silently treated as a new parameterized model. Original source-control cases include phase and amplitude changes. General species mixtures or apparatus redesign require an explicit new computation and review.

## Read the outcome correctly

- One conditioned proton has an initial two-mode excited population 0.07997665450257789 and gap 431.0812443150 MeV. Its mean ideal write requires 2.9011460679e-11 J. Its original individual controller budget is 6.9070389311e-11 J.
- The 1 m3 cosmological reference uses externally matched expected occupancy 0.2425893463937076. It is a mean ensemble ledger, not a fractional proton realization. Its mean supply 7.0378712840e-12 J is paid from the disclosed mean budget. That small budget is not used to fund one actual proton write.
- Outside the supply boundary, system energy grows and q changes from -0.52855 to -0.519196728075. With its pressureless supplier included, energy and q remain constant; included q is -0.518507515893. Different initial boundaries contain different initial energies.
- Proper-time transition probabilities use the adopted clock mapping. Full repeated write/reset costs, accumulated physical storage and an autonomous energy-conserving apparatus are not calculated.
- The homogeneous numbers are diagnostics at V0 under the adopted volume law. They are not a measured expansion change, a time-dependent transfer Q(tau), or a unified SI covariant apparatus/background evolution. Coherent post-measurement current operators and nonuniform dynamics are outside this sample.

## Files

- `manuscripts/`: Korean and English PDF, editable DOCX and Markdown source.
- `reproduce.py`: case calculation and ordered fresh original-stage replay.
- `inputs.json`: selected calibration, constants, boundary and source hashes.
- `reference_boundary.json`: selected diagnostic from integrated bridge review 0.8.
- `expected/`: fresh tested numerical output, CSV energy/route ledgers, connection report and original-stage logs.
- `WRRA_M_Bridge_0_5_0_8_Reviewed_r1_2026_10_03.zip`: original reviewed source archive, unchanged, including required earlier frozen dependencies.
- `build_case.py`: optional manuscript builder; requires pandoc and python-docx, plus the documented fonts. Native equations are produced by pandoc and remain editable.
- `SHA256SUMS`: package file integrity manifest.

Numbers in papers are rounded. Full machine precision is in `expected/results.json`. Energy comparisons use relative 2e-10 and absolute 1e-23 J for the reference boundary; transition comparisons use 1e-9 absolute tolerance. The finite pressure derivative uses relative 1e-9 tolerance. Full checks and local tolerances are explicit in the code.

The existing integrated release and its authorship remain unchanged. This is a separate companion review case and has no newly assigned DOI.

## 한국어 안내

상류 주소로 내부 상태를 준비하고 한 번의 이상적 기록 비용을 같은 에너지·압력 장부에 연결한 검토용 사례이다. 통합논문의 최원식·최정인 공동저자를 유지한다. 부품 연구의 조립 규칙은 사용하지 않는다.

`python reproduce.py --out replay`로 원본 네 단계와 사례를 재실행한다. 원본 점검 450개, 연결 점검 26개가 모두 통과했다. 양성자 한 개의 제어기 예산과 1 m3의 기대 점유수 장부를 구분한다. 결과는 선언한 준비·기록·공급 경계·시계·부피 법칙의 조건부 계산이다. `manuscripts`의 한영 PDF로 검토하고 DOCX 수식을 직접 수정할 수 있다.
