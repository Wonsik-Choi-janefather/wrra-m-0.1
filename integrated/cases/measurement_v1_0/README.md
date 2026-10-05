# WRRA M Integrated Measurement Case 1.0

Wonsik Choi and Jeongin Choi · 5 October 2026

**Case DOI: [10.5281/zenodo.23149260](https://doi.org/10.5281/zenodo.23149260)**  
Principal integrated manuscript: [10.5281/zenodo.23126800](https://doi.org/10.5281/zenodo.23126800)

This companion review case executes address conditioning, a prepared proton internal state, one ideal finite record, reference-matched SI energy and homogeneous pressure/deceleration from the same energy expression. The evaluation order is verified/frozen inputs → WRRA transformations → numerical outputs → declared falsification checks. The separate prime-parts research supplies no inputs.

## Read and reproduce

- [English PDF](package/manuscripts/WRRA_M_Integrated_Measurement_Case_v1_0_EN_2026_10_05.pdf) · [Korean PDF](package/manuscripts/WRRA_M_Integrated_Measurement_Case_v1_0_KO_2026_10_05.pdf)
- [Editable English DOCX](package/manuscripts/WRRA_M_Integrated_Measurement_Case_v1_0_EN_2026_10_05.docx) · [Editable Korean DOCX](package/manuscripts/WRRA_M_Integrated_Measurement_Case_v1_0_KO_2026_10_05.docx)
- [Complete frozen package ZIP](archive/WRRA_M_Integrated_Measurement_Case_v1_0_Package_2026_10_05.zip)
- [Fixed inputs and provenance](package/inputs.json) · [Full-precision results](package/expected/results.json) · [Connection check report](package/expected/check_report.json)

Use Python 3.12 and the pinned dependencies:

```sh
cd integrated/cases/measurement_v1_0/package
python -m pip install -r requirements.txt
python reproduce.py --out replay
```

The replay executes original bridge stages 0.2, 0.3, 0.5 and 0.6 in order, forwards fresh state and basis, and evaluates the selected connection case. Expected result: **450 original-stage software checks + 26 case connection checks, zero failures**. The original checks include controls beyond this selected case; they are not independent physical experiments.

## Interpretation

The 1 m³ diagnostic uses externally matched expected occupancy 0.2425893463937076. Its mean supply is 7.0378712840e-12 J. Individual proton writes use the separately disclosed individual controller budget. Outside the supplier boundary q changes from -0.52855 to -0.519196728075. Including the pressureless supplier conserves total energy and keeps its own q at -0.518507515893. These boundaries contain different initial energy.

This is a conditional computational review sample. Repeated-readout probabilities depend on the declared proper-time clock mapping. Autonomous apparatus, repeated reset/storage costs, actual abundance and full nonuniform covariant evolution remain open.

## Frozen archive and publication metadata

The contents of `package/` and the release ZIP preserve the verified files byte for byte. The inner README records the pre-deposit state; this page and `CITATION.cff` provide the subsequently assigned case DOI. ZIP SHA256: `22f7ddcb214a4cf7afa7e8565ce658dc95f2cd1c037173bacb420071f14f2c51`.

License: Creative Commons Attribution 4.0 International (CC BY 4.0).

## 한국어 안내

상류에서 준비된 상태를 이상적 측정·기록 비용에 연결하고, 같은 SI 에너지 표현으로 압력과 균질 감속계수를 계산한 검토용 사례입니다. 최원식·최정인 공동저자를 유지하며 부품 연구의 입력과 조립 규칙을 사용하지 않습니다. 한영 원고와 모든 재현 자료를 함께 공개합니다.
