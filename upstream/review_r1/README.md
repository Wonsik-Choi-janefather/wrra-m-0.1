# WRRA M upstream reviewed collection r1

**Wonsik Choi / 최원식 · 2026-10-02 · collection version 1.0-r1**

DOI: [10.5281/zenodo.23092499](https://doi.org/10.5281/zenodo.23092499)

다섯 상류 연구를 검증 입력 → WRRA 변환 → 출력 → 반증 조건의 순서로
재검토하고 원고와 구현을 교정한 자료집입니다. 알려진 관측값의 재현은
설명 성과로 기록하고, 보정 입력과 고정된 상태에서 계산한 출력의 역할을
명시했습니다. Core 1.0, MCC 2.3.2 및 downstream 0.9-r1은 보존합니다.

## Read the papers

- **two_stage_filter_v1_0**: [PDF](WRRA_M_Upper_Two_Stage_Filter_Hypothesis_v1_0_r1_KO_2026_10_02.pdf) · [Word](WRRA_M_Upper_Two_Stage_Filter_Hypothesis_v1_0_r1_KO_2026_10_02.docx)
- **zeta_frame_v0_1**: [PDF](WRRA_M_Zeta_Zero_Frame_Filter_Appendix_v0_1_r1_KO_2026_10_02.pdf) · [Word](WRRA_M_Zeta_Zero_Frame_Filter_Appendix_v0_1_r1_KO_2026_10_02.docx)
- **particle_residue_decay_v0_1**: [PDF](WRRA_M_Particle_Residue_Decay_Trial_v0_1_r1_KO_2026_10_02.pdf) · [Word](WRRA_M_Particle_Residue_Decay_Trial_v0_1_r1_KO_2026_10_02.docx)
- **fold_decay_v0_2**: [PDF](WRRA_M_Fold_Transition_Decay_Rate_v0_2_r1_KO_2026_10_02.pdf) · [Word](WRRA_M_Fold_Transition_Decay_Rate_v0_2_r1_KO_2026_10_02.docx)
- **internal_mixing_v0_3**: [PDF](WRRA_M_Internal_Fold_Mixing_Shared_Currents_v0_3_r1_KO_2026_10_02.pdf) · [Word](WRRA_M_Internal_Fold_Mixing_Shared_Currents_v0_3_r1_KO_2026_10_02.docx)
- **통합 검토 보고서**: [PDF](WRRA_M_Upstream_Review_r1_KO_2026_10_02.pdf) · [Word](WRRA_M_Upstream_Review_r1_KO_2026_10_02.docx)

## Reproduce

[전체 원고·코드·검증 결과 ZIP](WRRA_M_Upstream_Reviewed_Collection_r1_Reproducibility_2026_10_02.zip)을 풀고:

```sh
python -m pip install -r requirements.txt
python reproduce_all.py --contracts
```

**122개 구현 검사 + 56개 추가 검사 = 178개 통과.** 원래 연구의 121개
검사와 기준 결과는 ZIP의 `baseline/`에 보존했습니다. 교정 결과는
[reproduction_results.json](reproduction_results.json)에서 확인할 수 있습니다.

## Corrections

내부 혼합 0.3의 N·전자기 상수 입력 전달을 고치고 부모 보정 기준을 동결했습니다.
제타 부록 생성기의 공개 디렉터리 경로를 교정했으며, 입자 탐색의 원시 후보
142,527개와 유한 범위 유효 후보 141,790개를 구분했습니다. 기준 물리 출력은
유지됩니다. 각 r1 원고에는 연구의 입력·변환·출력·반증 및 결론 장부를 추가했습니다.

5%·26.8%·68.2%의 공동 장부, 제타 프레임, 핵자 공통 구성 및 붕괴 수송,
공동 내부 전류의 연결을 유지합니다. 자기모멘트만 보정한 제한 상태의 축벡터
차이와 자유 보정 계열도 원고에 기록했습니다.

[변경 내역](CHANGES.txt) · [인용 정보](CITATION.cff) · [파일 SHA256](SHA256SUMS)

ORCID: https://orcid.org/0009-0001-4263-9772 · License: CC BY 4.0
Historical repository baseline: `e9dc4be98c095152cf94d9eb631b921da3ab51e7`.
