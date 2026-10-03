# WRRA-M Research Notes

## Upstream integrated manuscript 1.0-r1 — reviewed release

상류 개발은 0.10에서 마감했습니다. 한·영 통합 논문 1.0-r1은 단위·기호·기준 부피의 적용 범위와 Physics 준비 원고 인용을 재검토한 개정판입니다.

- [Zenodo preprint and complete package](https://doi.org/10.5281/zenodo.23119041)
- [Bilingual PDFs, editable manuscripts, sources and verification](upstream/integrated_1_0_r1/README.md)
- Re-executed implementation/mathematical checks: 395 + 1,395 + 83 passed; both manuscripts: 13 pages, 24 native equations, four tables.


## Upstream 0.7-0.10 reviewed collection r1 · 2026-10-03

0.7~0.10의 코드·입력·결과·문서를 다시 검토하고 수정했습니다. **기존 단계 검사 1,327개 + 새 재검토 검사 68개 = 총 1,395개 통과**. 비정상 상태 입력, 확률 0 분기, 기준 사례와 Q² 목록 순서 의존, 결과 파일 없는 재생성을 보완했습니다. 기존 물리 수치는 유지합니다. 초기 ROADMAP의 1.0 개발 목표 표기도 정정했습니다. **상류 개발은 0.10에서 마감**하고, 미계산 물리 대응은 null 계약과 기존 불일치 장부에 남깁니다.

- [한·영 재검토 보고서와 재현 안내](upstream/review_0_7_0_10_r1/README.md)
- [한국어 검토 PDF](upstream/review_0_7_0_10_r1/paper/WRRA_M_Upstream_0_7_0_10_Reviewed_r1_KO_2026_10_03.pdf) · [English reviewed PDF](upstream/review_0_7_0_10_r1/paper/WRRA_M_Upstream_0_7_0_10_Reviewed_r1_EN_2026_10_03.pdf)
- [전체 재현 ZIP](upstream/review_0_7_0_10_r1/archive/WRRA_M_Upstream_0_7_0_10_Reviewed_Collection_r1_2026_10_03.zip) · [검증 장부](upstream/review_0_7_0_10_r1/review_checks.json)
- [Zenodo DOI 10.5281/zenodo.23115550](https://doi.org/10.5281/zenodo.23115550)


## Downstream 1.0 completed · 하류 통합정리 1.0 완료 · 2026-10-03

**하류 개발은 0.12에서 마감했고, 0.1–0.12 통합정리 논문 1.0을 최종 확정했습니다.** 공동저자는 **Wonsik Choi (최원식), Jeongin Choi (최정인)**입니다. Physics 투고용 물질 구성비 r9·확장 및 접속조건 r8의 용어, 보정값과 검증 범위를 유지했습니다.

**Final downstream research consolidation: WRRA M 1.0.** [Zenodo final edition, DOI 10.5281/zenodo.23115883](https://zenodo.org/records/23115883) includes the complete reproducible package and both editable manuscripts.

- [한국어 PDF](downstream/v1_0/synthesis/WRRA_M_1_0_Downstream_Synthesis_KO.pdf) · [Word](downstream/v1_0/synthesis/WRRA_M_1_0_Downstream_Synthesis_KO.docx)
- [English PDF](downstream/v1_0/synthesis/WRRA_M_1_0_Downstream_Synthesis_EN.pdf) · [Word](downstream/v1_0/synthesis/WRRA_M_1_0_Downstream_Synthesis_EN.docx)
- [Release and reproduction instructions](downstream/v1_0/README.md) · [Final review and completion scope](DOWNSTREAM_1_0_COMPLETION.md) · [Validation report](downstream/v1_0/synthesis/WRRA_M_1_0_Validation_Report.json)

The final editorial review clarifies J units, powers of ten, function parentheses, τ and ℏ in the SI phase, τ/T_coord for the accelerated path, and the finite potential boundary. Both final PDFs were inspected in full: 12 English pages and 11 Korean pages. The editions share 22 native numbered equations and six tables. All 312 current archive manifest entries, 37 byte-identical replay files, 96 component check groups and nine cross-version checks remain verified.

**1.0 completion refers to the reviewed integrated research edition.** Physical measurement operations, post-observation states, physical record formation and repeated-measurement uncertainty remain unimplemented downstream; the failed slow-clock identification and open connection conditions remain in the scope ledger. Core 1.0 and MCC 2.3.2 are frozen. Historical 0.12-r1 source archive: [DOI 10.5281/zenodo.23113101](https://zenodo.org/records/23113101).


## Upstream closes at 0.10 · 상류 개발 0.10 마감

**상류 개발은 0.10에서 마무리합니다.** SOURCE → 필터 → 실제 조건부 기록 → 내부 상태 → 동일 상태 전류와 유한 stock 장부를 한 번 실행으로 통합했습니다. **156개 통합 검사 + 309개 독립 감사**, 새 복사본의 바이트 동일 재현을 완료했습니다. 미계산 물리 대응은 0.10 마감 장부에 남기며 추가 개발 단계는 만들지 않습니다. 1.0을 만든다면 0.10까지의 검토·정리·동결판으로만 둡니다.

[0.10 한국어 PDF](upstream/generator_v0_10/paper/WRRA_M_Upstream_0_10_KO_2026_10_03.pdf) · [한국어 원고](upstream/generator_v0_10/README.md) · [English](upstream/generator_v0_10/README_EN.md) · [단일 재현 실행](upstream/generator_v0_10/reproduce_all.py) · [최종 전달 장부](upstream/generator_v0_10/handoff.json)

[0.8 PDF](upstream/shutter_v0_8/paper/WRRA_M_Upstream_0_8_r1_KO_2026_10_03.pdf) · [0.9 PDF](upstream/residue_current_v0_9/paper/WRRA_M_Upstream_0_9_KO_2026_10_03.pdf)

## Upstream 0.9 · conditional residue and same-state current connection

상류 0.8의 실제 표현 잔존을 교정된 0.6의 내부 밀도 상태와 전자기·약전류에 연결했습니다. SOURCE 세기 변화가 내부 모드 비중과 전류 판독에 전달됩니다. **183개 구현 검사 + 135개 독립 감사**, ZIP 새 복사본의 바이트 동일 재현을 완료했습니다. 준비 사상·강도·종 선택은 공개한 구성 입력이고, 에너지 공급·물리 시간·기록 매체와 기존 자기반경 오차는 열린 장부에 남깁니다.

[한국어 원고](upstream/residue_current_v0_9/README.md) · [English](upstream/residue_current_v0_9/README_EN.md) · [재현](upstream/residue_current_v0_9/reproduce_all.py) · [0.10 전달 명세](upstream/residue_current_v0_9/handoff.json)

## Upstream 0.8-r1 · finite shutter and microscopic record contract

상류 0.7의 백만 주소 SOURCE·필터 상태에서 분기 norm과 조건부 기록을 실행했습니다. **28개 주소 연결 검사 + 403개 셔터 감사 검사**, 새 복사본의 바이트 동일 재현을 완료했습니다. 물리 시간 환산·기록 매체·입자 사상은 전달 장부에 열린 항목으로 남깁니다.

[한국어 설명](upstream/shutter_v0_8/README.md) · [English](upstream/shutter_v0_8/README_EN.md) · [재현 코드](upstream/shutter_v0_8/reproduce_all.py) · [0.9 전달 명세](upstream/shutter_v0_8/handoff.json)

## Downstream endpoint correction · 하류 마감 범위 정정 · 2026-10-03

**하류 개발은 0.12에서 마감한다. WRRA_M 1.0은 0.1~0.12 통합 확정판이다.**
**Downstream development ends at 0.12; WRRA_M 1.0 consolidates 0.1–0.12.**

The automatic downstream extension to 0.13–0.17 is withdrawn. [Dated scope correction and closure ledger](DOWNSTREAM_CLOSURE_0_12.md) supersedes prospective stage numbers in the archived papers and packages. Published numerical results and their validation are retained. Physical outcomes, post-observation states, records/repeated uncertainty and the nonuniform covariant clock connection remain unimplemented/open in the reviewed release; These scope entries are retained in the completed downstream 1.0 research consolidation.

## Current downstream reviewed 0.10 to 0.12 series r1 · 2026-10-03

주소·공통운반자 부하의 SI 에너지·압력 연결, 첫 다섯 입력의 순차 보정, 고유시간 갱신과 유한 경계 스펙트럼을 재검토했습니다. 입력 해시와 기존 계산값을 유지하며 **96개 구성 검사**가 통과했습니다. 시계 환산의 범위를 앞선 원고에 반영하고, 시작점을 포함한 사건 수와 두 모드 overlap의 적용 상태를 교정했습니다. 양의 유한 간격 오차 한계를 검증했습니다.

**English PDF and Word editions of all three papers are included**, together with their Korean counterparts and reproducible code. The old slow nonuniform expansion schedule differs from the SI energy phase; that connection remains open.

- [Six papers and calculation guide](review/0_10_to_0_12_r1/README.md)
- [Review and corrections](REVISION_0_10_TO_0_12_R1.md) · [Review checks](review/0_10_to_0_12_r1/review_checks.json)
- [Complete reviewed series ZIP](paper/WRRA_M_0_12_r1_Series_Release.zip)
- [Zenodo DOI 10.5281/zenodo.23113101](https://doi.org/10.5281/zenodo.23113101)

## Current upstream 0.7 · SOURCE와 두 단계 필터의 생성 장부 · 2026-10-03

소수 SOURCE 진폭을 관계 주소와 순서 있는 양성 필터에 연결했습니다.
이전 α·β를 동결하여 **5%·26.8%·68.2%**를 재현하고, SOURCE 세기·위상 변화와
유한 stock의 반복 방출을 계산했습니다. 기준 잔존 31.8%는 무제한 재방출의 자동 고정점이 아니며,
생성 창의 닫힘 또는 별도 균형 제어가 필요하다는 조건을 공개합니다.
**53개 구현 검사 + 60개 독립 감사, 총 113개 통과**, 9쪽 한글 원고와 새 ZIP 재현을 완료했습니다.

- [상류 0.7 원고·계산·재현 안내](upstream/source_filter_v0_7/README.md)
- [한글 PDF 9쪽](upstream/source_filter_v0_7/paper/WRRA_M_SOURCE_State_Two_Stage_Filter_Generation_Ledger_v0_7_KO_2026_10_03.pdf) · [Word](upstream/source_filter_v0_7/paper/WRRA_M_SOURCE_State_Two_Stage_Filter_Generation_Ledger_v0_7_KO_2026_10_03.docx)
- [전체 재현 ZIP](upstream/source_filter_v0_7/archive/WRRA_M_SOURCE_State_Two_Stage_Filter_v0_7_Reproducibility_2026_10_03.zip) · [113개 검증](upstream/source_filter_v0_7/verification/independent_audit.json)
- [다음 단계 전달 명세](upstream/source_filter_v0_7/code/handoff.json) · [상류 0.10 마감 범위](upstream/source_filter_v0_7/ROADMAP.md)

## Upstream 0.4–0.6 reviewed collection r1 · 2026-10-03

상류 0.4, 0.5, 0.6의 논문·실행 코드·계승 입력을 재검토하고 교정했습니다.
기저 정렬 표기, 비유한 입력 계약, 공간 구적 조건과 운동량 배열에 의존하던 검증을 고쳤습니다.
기존 물리 수치와 남은 불일치를 유지했고, **395개 검사 및 최종 ZIP 새 환경 재현**을 완료했습니다.
세 한국어 교정 Word/PDF와 4쪽 통합 검토보고서를 함께 공개합니다.

- [교정 자료집·논문·코드·재현 안내](upstream/review_0_4_0_6_r1/README.md)
- [통합 검토보고서 PDF](upstream/review_0_4_0_6_r1/report/paper/WRRA_M_Upstream_0_4_to_0_6_Review_r1_KO_2026_10_03.pdf) · [Word](upstream/review_0_4_0_6_r1/report/paper/WRRA_M_Upstream_0_4_to_0_6_Review_r1_KO_2026_10_03.docx)
- [전체 재현 ZIP](upstream/review_0_4_0_6_r1/archive/WRRA_M_Upstream_0_4_to_0_6_Reviewed_Collection_r1_Reproducibility_2026_10_03.zip) · [395개 검증 장부](upstream/review_0_4_0_6_r1/reproduction_results.json)
- [Zenodo DOI 10.5281/zenodo.23112253](https://doi.org/10.5281/zenodo.23112253)

## 학회 등록용 분리 원고 두 편 · 2026-10-03

공동저자: **최원식 Wonsik Choi · 최정인 Jeongin Choi**

- [보통 물질 5퍼센트 구성비의 재현 · r9 · 한글 22쪽](submission/matter_fraction_r9/README.md) — 두 단계 차원필터와 공동 구성비 계산, 구동 대조 및 검산 부록
- [WRRA의 확장 가능성과 접속 조건 · r8 · 한글 7쪽](submission/extensions_r8/README.md) — 공통전달자·진공 기준·뒤틀림·균일 팽창과 후속 미시 구현
- [두 원고와 계산 자료 안내](submission/README.md)

## Original upstream 0.6 · 핵자 전하 반지름과 유한 운동량 전류 · 2026-10-03

0.5와 같은 내부 상태에서 유한 운동량 전자기·약한 전류를 계산하고,
영전하 아이소벡터 항과 공간 폭을 두 전하 반지름에 공동 보정했습니다.
Sachs–Dirac–Pauli 변환, CVC와 투영 연속 방정식을 확인했습니다.
반동·선도 복사 보정 뒤 **고정 부모 κ의 수명은 846.204102초**이며,
878.3초에 맞춘 **별도 κ=11.975301266**을 구분해 기록했습니다.
중성자 자기 반지름의 남은 불일치와 유한 Q² 곡률의 구성 의존성을 공개했습니다.
**구현 84개 + 독립 감사 24개, 총 108개 통과**.

- [상류 0.6 원고·코드·재현 안내](upstream/finite_currents_v0_6/README.md)
- [한글 PDF 10쪽](upstream/finite_currents_v0_6/paper/WRRA_M_Finite_Momentum_Currents_Beta_Corrections_v0_6_KO_2026_10_03.pdf) · [Word](upstream/finite_currents_v0_6/paper/WRRA_M_Finite_Momentum_Currents_Beta_Corrections_v0_6_KO_2026_10_03.docx)
- [전체 재현 ZIP](upstream/finite_currents_v0_6/paper/WRRA_M_Finite_Momentum_Currents_Beta_Corrections_v0_6_Reproducibility_2026_10_03.zip) · [검증](upstream/finite_currents_v0_6/verification.json)

## Original upstream 0.5 · 내부 공간의 안정성, 여기 척도와 핵자 크기 · 2026-10-02

0.4의 이차 결합을 무한 공간으로 확장할 때 드러나는 에너지 무하한을 기록하고,
기존 두 상태 결합과 순열 대칭을 보존하는 제한 결합으로 보강했습니다.
같은 바닥상태의 공동 전류와 알려진 여기·양성자 반지름 입력으로
**Δ=507.032217686 MeV, ℓ=0.61619621794 fm**를 보정했습니다.
보정값을 고정한 K=10에서 여기 간격 변화는 **0.00854213 MeV**입니다.
중성자 전하 반지름의 불일치와 제한 방식의 선택 자유도를 공개했습니다.
**구현 118개 + 별도 검증 22개, 총 140개 통과**, 새 디렉터리 결과 바이트 재현을 확인했습니다.

- [상류 0.5 원고·코드·재현 안내](upstream/spatial_scale_v0_5/README.md)
- [한글 PDF](upstream/spatial_scale_v0_5/paper/WRRA_M_Spatial_Stability_Excitation_Scale_v0_5_KO_2026_10_02.pdf) · [Word](upstream/spatial_scale_v0_5/paper/WRRA_M_Spatial_Stability_Excitation_Scale_v0_5_KO_2026_10_02.docx)
- [전체 재현 ZIP](upstream/spatial_scale_v0_5/paper/WRRA_M_Spatial_Stability_Excitation_Scale_v0_5_Reproducibility_2026_10_02.zip) · [검증](upstream/spatial_scale_v0_5/verification.json)

## Original upstream 0.4 · 내부 공간 결합과 핵자의 공동 전류 · 2026-10-02

실제 가우스·야코비 공간 모드의 결합과 그 자기장 미분 전류를 구현했습니다.
같은 내부 고유상태에서 **gA=1.2753**과 두 핵자 자기모멘트를 공동 반환하며,
**c₁=0.439987792930 μN**을 결합 미분의 기대값으로 연결합니다.
자기장 응답 η의 보정, 유한 공간 투영과 Δ의 선택을 원고에 명시했습니다.
**86개 구현 검사와 17개 별도 검증, 총 103개 통과** 및 새 ZIP 재현을 완료했습니다.

- [상류 0.4 논문·코드·재현 안내](upstream/internal_coupling_v0_4/README.md)
- [한글 PDF 10쪽](upstream/internal_coupling_v0_4/paper/WRRA_M_Internal_Spatial_Coupling_Joint_Currents_v0_4_KO_2026_10_02.pdf) · [Word](upstream/internal_coupling_v0_4/paper/WRRA_M_Internal_Spatial_Coupling_Joint_Currents_v0_4_KO_2026_10_02.docx)
- [전체 재현 ZIP](upstream/internal_coupling_v0_4/paper/WRRA_M_Internal_Spatial_Coupling_Joint_Currents_v0_4_Reproducibility_2026_10_02.zip) · [검증 결과](upstream/internal_coupling_v0_4/verification.json)

## Current upstream reviewed collection r1 · 2026-10-02

[Zenodo DOI: 10.5281/zenodo.23092499](https://doi.org/10.5281/zenodo.23092499) ·
[교정 자료집과 여섯 PDF](upstream/review_r1/README.md)

상류 다섯 연구의 원고와 코드를 다시 검토하고 교정했습니다. 내부 혼합 모델의
N·전자기 상수 입력 전달, 제타 부록 생성 경로 및 후보 집계를 수정했습니다.
122개 구현 검사와 56개 추가 검사, 총 178개가 통과했으며 새 압축 해제 환경에서
결과 파일의 바이트 단위 재현과 여섯 Word 원고 재생성을 확인했습니다.
교정 코드 전체는 자료집의 재현 ZIP에 있고, 기존 버전 파일은 기록으로 보존합니다.

**Wonsik Reality Renderer Architecture Meta-dimensional Branch**

**원식 현실 렌더러 아키텍처 메타차원 연구 분기**

Latest completed downstream research edition: **WRRA M 1.0** · 2026-10-03. Downstream development endpoint: **0.12**.

Reviewed predecessor: **WRRA-M 0.9-r1**.

Latest Zenodo edition: **WRRA M 1.0**, final 0.1–0.12 downstream synthesis, [DOI 10.5281/zenodo.23115883](https://zenodo.org/records/23115883). Historical 0.12-r1 scientific source archive: [DOI 10.5281/zenodo.23113101](https://doi.org/10.5281/zenodo.23113101).

WRRA-M continues WRRA Core 1.0 and Minimal Computation Cosmology 2.3.2.

The 0.7–0.9 review corrects small positive loads, trace normalization, tiny filter support and sparse channel routing. All 69 check groups pass. [Review and correction record](REVISION_0_7_TO_0_9_R1.md). The bilingual revised papers and reproduction packages are linked below.

## Upper structure hypothesis 1.0 · 상위 구조 가설 1.0

초기 진입과 정상 0차원 복귀라는 **두 단계 차원필터**로 접힘 상태의 잔존을 구성하는 상류 가설이다. **5%·26.8%·68.2%** 공동 보정 장부와 프레임 갱신에 따른 시간·양자화 가설을 담았다. 지수 2의 고정 시험에서는 **4.8769%** 산술적 잔존율을 계산했다.

The upper hypothesis constructs residue through initial admission and normalized return. It includes the common calibrated partition and the frame-update hypothesis, together with the interfaces for particle constants and physical loads.

- [상류 가설과 재현 안내](upstream/two_stage_filter_v1_0)
- [한국어 PDF](upstream/two_stage_filter_v1_0/paper/WRRA_M_Upper_Two_Stage_Filter_Hypothesis_v1_0_KO_2026_10_01.pdf) · [Word](upstream/two_stage_filter_v1_0/paper/WRRA_M_Upper_Two_Stage_Filter_Hypothesis_v1_0_KO_2026_10_01.docx) · [GitHub 원고](upstream/two_stage_filter_v1_0/manuscript_KO.md)
- [전체 재현 ZIP](upstream/two_stage_filter_v1_0/paper/WRRA_M_Upper_Two_Stage_Filter_Hypothesis_v1_0_Reproducibility_2026_10_01.zip) · [계산 장부](upstream/two_stage_filter_v1_0/code/results_26_8.json)

## Zeta zero frame appendix 0.1 · 제타 영점 프레임 계산 부록 0.1

초기 필터 변동을 첫 4개 제타 영점의 위상으로 구현하고, 미진입 잔량을 프레임별로 운반했다. **5%에 보정한 임계값을 고정**하면 초기 구간 4·8·16프레임의 표현형 잔존이 **3.7048%·5%·5.6825%**로 바뀐다. 최소 소인수 3·5·7·11 가족은 기준 표현형의 **98.7275%**를 차지한다. 정상화 후 접힘 보존과 복귀 누수의 수명 조건을 계산했으며 14개 검증 항목이 통과했다.

- [계산 부록과 재현 안내](upstream/zeta_frame_v0_1)
- [한국어 PDF 6쪽](upstream/zeta_frame_v0_1/paper/WRRA_M_Zeta_Zero_Frame_Filter_Appendix_v0_1_KO_2026_10_01.pdf) · [Word](upstream/zeta_frame_v0_1/paper/WRRA_M_Zeta_Zero_Frame_Filter_Appendix_v0_1_KO_2026_10_01.docx) · [GitHub 부록](upstream/zeta_frame_v0_1/appendix_KO.md)
- [전체 재현 ZIP](upstream/zeta_frame_v0_1/paper/WRRA_M_Zeta_Zero_Frame_Filter_v0_1_Reproducibility_2026_10_01.zip) · [계산 장부](upstream/zeta_frame_v0_1/code/results.json)

## Particle residue and fold-decay trial 0.1 · 입자 잔존과 붕괴 탐색 0.1

잔존 주소에서 **구성 소립자·강력과 색·잔여 핵력·약력·전자기 전류·스핀**을 별도 응답으로 읽는다. 질량비 탐색에서 후보쌍 15개를 얻고, 단순 공통 거듭제곱 판독의 핵자·뮤온 불일치를 기록했다. **선택한 45·75 핵자 구성**에 알려진 질량·자기모멘트로 보정한 에너지와 전류를 적용했다. 별도 15 카이럴 채널의 색·약력·전하·스핀 대수 10개 검사가 통과했다. 자유 중성자 붕괴의 기대 장부는 관측 평균수명을 입력해 에너지와 양자수를 보존하며, 같은 주소의 내부 상태·결합·환경 차이를 허용한다.

- [입자 탐색과 재현 안내](upstream/particle_residue_decay_v0_1)
- [한국어 PDF 7쪽](upstream/particle_residue_decay_v0_1/paper/WRRA_M_Particle_Residue_Decay_Trial_v0_1_KO_2026_10_01.pdf) · [Word](upstream/particle_residue_decay_v0_1/paper/WRRA_M_Particle_Residue_Decay_Trial_v0_1_KO_2026_10_01.docx) · [GitHub 원고](upstream/particle_residue_decay_v0_1/manuscript_KO.md)
- [전체 재현 ZIP](upstream/particle_residue_decay_v0_1/paper/WRRA_M_Particle_Residue_Decay_Trial_v0_1_Reproducibility_2026_10_01.zip) · [입자 장부](upstream/particle_residue_decay_v0_1/code/results.json) · [분리한 채널 장부](upstream/particle_residue_decay_v0_1/code/channel_results.json)

## Fold-current beta-rate bridge 0.2 · 접힘 전환과 붕괴율 계산 0.2

선택한 **45·75 핵자 주소**의 64차원 스핀·맛 상태에서 전환 원소 **벡터 1·기본 축벡터 5/3**을 계산하고, 유한 소수 계열 응답과 베타 최종 상태공간을 연결했다. 관측 축벡터 비율과 중성자 평균수명 **878.3 s**으로 정한 공통 보정을 고정해 방출 에너지·소수 표식·전류·상태 겹침의 변화에 따른 전환율을 계산한다. 정규화 전자 에너지 분포, 각도 계수의 관측 중심값과 차이, Actual 보존 수송을 함께 기록했다. **30개 계산 검사와 독립 ZIP 재현**을 완료했다.

The chosen nucleon spin-flavor states yield vector and bare axial matrix elements 1 and 5/3. A declared finite Euler-family response, supplied weak constants and allowed beta phase space connect them to rates. One neutron-lifetime anchor fixes the common response strength; subsequent controlled cases retain it. Normalized spectra and angular-response differences remain explicit.

- [계산 안내와 재현](upstream/fold_decay_v0_2/README.md)
- [한국어 PDF 7쪽](upstream/fold_decay_v0_2/paper/WRRA_M_Fold_Current_Beta_Rate_Bridge_v0_2_KO_2026_10_02.pdf) · [Word](upstream/fold_decay_v0_2/paper/WRRA_M_Fold_Current_Beta_Rate_Bridge_v0_2_KO_2026_10_02.docx) · [GitHub 원고](upstream/fold_decay_v0_2/manuscript_KO.md)
- [전체 재현 ZIP](upstream/fold_decay_v0_2/paper/WRRA_M_Fold_Current_Beta_Rate_Bridge_v0_2_Reproducibility_2026_10_02.zip) · [계산 코드](upstream/fold_decay_v0_2/code/compute.py) · [결과 장부](upstream/fold_decay_v0_2/code/results.json)


## Internal fold mixing and shared currents 0.3 · 내부 접힘 혼합과 핵자 전류 0.3

소수 계열 결합을 가진 내부 Hamiltonian의 고유상태에 전자기·약한 전류를 따로 적용했다. 자기모멘트만 보정한 단순 경로는 **혼합 7.3532%, 축벡터 1.568624**를 내놓으며 관측 축벡터와 23.0004% 차이가 남는다. 관측 축벡터를 함께 사용한 구성은 **혼합 29.3525%, 집단 자기 응답 c1=0.4399877929 μN**로 두 자기모멘트와 축벡터를 반환한다. 부모 수명 보정을 고정한 소수 계열 사례와 같은 자기모멘트에 대응하는 상태 자유도를 기록했다. **38개 구현 검사, 7쪽 원고와 독립 ZIP 재현**을 완료했다.

The finite Euler-family Hamiltonian replaces the earlier scalar axial dressing with an explicit internal eigenstate. The magnetic-only inverse and the joint calibrated realization are both recorded, including their input roles, electromagnetic/weak current blocks, fixed prime-family responses and conserved transport.

- [계산 안내와 재현](upstream/internal_mixing_v0_3/README.md)
- [한국어 PDF 7쪽](upstream/internal_mixing_v0_3/paper/WRRA_M_Internal_Fold_Mixing_Shared_Currents_v0_3_KO_2026_10_02.pdf) · [Word](upstream/internal_mixing_v0_3/paper/WRRA_M_Internal_Fold_Mixing_Shared_Currents_v0_3_KO_2026_10_02.docx) · [원고](upstream/internal_mixing_v0_3/manuscript_KO.md)
- [전체 재현 ZIP](upstream/internal_mixing_v0_3/paper/WRRA_M_Internal_Fold_Mixing_Shared_Currents_v0_3_Reproducibility_2026_10_02.zip) · [계산](upstream/internal_mixing_v0_3/code/compute.py) · [결과 장부](upstream/internal_mixing_v0_3/code/results.json)

## Completed 0.12 · 0.12 완료

0.11의 고정 보정 위에서 **경로별 고유시간 갱신과 유한 경계의 모드 스펙트럼**을 실행했다. epsilon=0.05를 공개한 구성 입력으로 두어 **delta_tau=1.4813019664158691e-21 s**를 계산했다. 평탄·가속·유한 중력·균질 FRW 시계, 접힘과 periodic·Dirichlet 공간 스펙트럼, 자유 연속 분산 및 정수 위상 가지를 대조했다. 이 간격은 측정한 최소시간으로 확정하지 않는다.

The same fixed-volume SI energy operator now evolves with converted proper-time phases and conserves its energy. **The old slow expansion schedule fails identification with that SI clock:** omega_info/(E_star/hbar)=2.102556972196466e-43. Historical nonuniform trajectories remain constitutive-schedule outputs; fully covariant interacting dynamics and empirical shutter/confinement selection remain open.

**36 new checks + 60 inherited checks pass.** Both six-page editions contain matching 18 native equations and five tables with 21 computed body rows. A clean copy with captured results removed reproduces 35 numerical/source files byte for byte. Realized operators and supports are finite.

| Evaluation | WRRA_M 0.12 |
| --- | --- |
| 검증 입력 / Verification inputs | Frozen 0.11 inputs and exact SI units; declared epsilon, finite basis, boundary phases and cavity length. |
| WRRA 고유 변환 / WRRA-specific transformation | Worldline proper-time integral → update events; finite modes/boundaries → Hamiltonian → unitary eigenphases; inherited SI ledger → exact time conversion. |
| 산출값 / Outputs | Path clocks and 57 accelerated-worldline events, fold and spatial spectra, continuous free dispersion, alias controls, conserving fixed-volume load exchange and inherited-clock failure. |
| 반증조건 / Falsifiers | Lorentz disagreement, energy/phase mismatch, missing integer branch, failed conservation or unconverted identification of the slow schedule with the SI Hamiltonian phase. |

- [0.12 한국어 PDF](paper/WRRA_M_0_12_KO.pdf) · [Word](paper/WRRA_M_0_12_KO.docx) · [원고](paper/WRRA_M_0_12_KO.md)
- [0.12 English PDF](paper/WRRA_M_0_12_EN.pdf) · [Word](paper/WRRA_M_0_12_EN.docx) · [Source](paper/WRRA_M_0_12_EN.md)
- [Reproducibility ZIP](paper/WRRA_M_0_12_Reproducibility.zip) · [Calculation guide](calculations/wrra_m_0_12/README.md)
- [Verification](calculations/wrra_m_0_12/results/verification.json) · [Document checks](calculations/wrra_m_0_12/results/document_checks.json) · [Clean-copy replay](calculations/wrra_m_0_12/results/reproduction_checks.json)
- [Completion record](REVISION_0_12.md) · [SHA256 manifest](SHA256SUMS_0_12)

```bash
python -m pip install -r calculations/wrra_m_0_12/requirements.txt
python calculations/wrra_m_0_12/run_release.py
```

## Completed 0.11 · 0.11 완료

첫 다섯 물리 입력 **G→H0→f_phi→f_c→m_e c²**를 순차 보정했다. 각 부분 단계가 뒤의 목표를 읽지 않으며, 단계별 산출값과 남은 자유도를 공개한다. 전자 모드 23과 영 절편 아래 **mu_E=22217.345682173913 eV**를 계산했다. 주소 alpha_addr·입장 beta_eff의 재표현에서 두 추가 산술 입력을 명시하고, 전자기 alpha와 구분한다.

The staged calibration retains all nine 0.10 cases and the reference **q0=−0.52855**, **v=207.5109051266 km/s** and conditional deflection **0.5355865106 arcsec**. The five-anchor dependency matrix has rank five conditional on fixed model choices. Two separately fitted response shapes reproduce the same anchors but give different subsequent K=4 responses, explicitly retaining the unfitted shape freedom.

**28 new checks + 32 inherited checks pass.** Both five-page editions contain matching 14 native equations and four tables with 21 body rows. A clean copy with captured outputs removed reproduces 23 numerical/source files byte for byte. Frozen dependency sources remain unchanged.

| Evaluation | WRRA_M 0.11 |
| --- | --- |
| 검증 입력 / Verification inputs | Frozen 0.10 ledger, ordered five physical anchors, exact SI references and declared address/carrier/mass choices. |
| WRRA 고유 변환 / WRRA-specific transformation | Partial calibration → density and sector load → same energy/pressure/gravity/expansion → mass-mode and electron-unit re-expression. |
| 산출값 / Outputs | Sequential outputs, 28 checks, nine inherited cases, mass unit, address alpha/beta re-expression, sensitivity rank and explicit residual-freedom controls. |
| 반증조건 / Falsifiers | Future-input leakage, failed reproduction or pressure differentiation, nonconservation, duplicated electron budget or treating unidentified quantities as fixed. |

Weighted twist fixes zeta*kappa_h², not the separate factors. The calculated length coefficient is not a measured cosmic size; W0 remains unassigned. Physical quantization and records remain unimplemented in the 0.12 closure ledger; the dated endpoint correction supersedes the earlier expanded roadmap.

- [0.11 한국어 PDF](paper/WRRA_M_0_11_KO.pdf) · [Word](paper/WRRA_M_0_11_KO.docx) · [Markdown](paper/WRRA_M_0_11_KO.md)
- [0.11 English PDF](paper/WRRA_M_0_11_EN.pdf) · [Word](paper/WRRA_M_0_11_EN.docx) · [Markdown](paper/WRRA_M_0_11_EN.md)
- [Reproducibility ZIP](paper/WRRA_M_0_11_Reproducibility.zip)
- [Calculation and input guide](calculations/wrra_m_0_11/README.md) · [28 checks](calculations/wrra_m_0_11/results/verification.json)
- [Document comparison](calculations/wrra_m_0_11/results/document_checks.json) · [Clean-copy reproduction](calculations/wrra_m_0_11/results/reproduction_checks.json)
- [Completion record](REVISION_0_11.md) · [Archive-content SHA256 manifest](SHA256SUMS_0_11)

```bash
python -m pip install -r calculations/wrra_m_0_11/requirements.txt
python calculations/wrra_m_0_11/run_release.py
```

## Completed 0.10 · 0.10 완료

주소별 정보 가중치를 양의 SI 에너지 응답에 연결하고, 같은 에너지의 부피 미분으로 압력을 계산했다. 기준 보정을 한 번 적용한 뒤 주소·상태 변경에도 계수를 고정한다. 32개 수치 검사, 한영 12개 수식과 12개 결과표 행 대조, 저장 결과를 제거한 복사본에서 17개 파일의 바이트 단위 재현을 완료했다.

The positive address energy map, carrier traces and one energy operator now calculate pressure, sector exchange, gravity and homogeneous expansion. The inherited reference reproduces **q=-0.52855**, **v=207.5109051266 km/s** and conditional finite-patch deflection **0.5355865106 arcsec**. All nine inherited state/volume cases agree. Arithmetic 5%/26.8%/68.2% and calibrated energy 4.93%/26.5%/68.57% remain distinct.

Conversion work is a signed exchange with the environment owning that work; it is not a fourth cosmic density fraction. The microscopic environment and measurement records remain open entries in the 0.12 closure ledger. Proper-time connections completed in 0.12 have the scope stated above.

| Evaluation | WRRA-M 0.10 |
| --- | --- |
| 검증 입력 / Verification input | Frozen reviewed 0.9 address inputs, 0.8 particle/filter ledger, 0.6-r2 carrier and disclosed constants, target energies and constitutive responses. |
| WRRA 고유 변환 / WRRA-specific transformation | Address-state effects → positive SI response and carrier loads → energy operator → volume pressure and conserved exchanges → gravity and expansion. |
| 산출값 / Output | 32 checks; inherited reference and all nine cases reproduced; frozen-coefficient address responses, 48-channel budgets and conversion-work ledger. |
| 반증조건 / Falsification | Failed positivity, calibrated reproduction, pressure derivative, exchange conservation, channel accounting or document/execution agreement. |

- [0.10 한국어 PDF](paper/WRRA_M_0_10_KO.pdf) · [DOCX](paper/WRRA_M_0_10_KO.docx) · [Markdown](paper/WRRA_M_0_10_KO.md)
- [0.10 English PDF](paper/WRRA_M_0_10_EN.pdf) · [DOCX](paper/WRRA_M_0_10_EN.docx) · [Markdown](paper/WRRA_M_0_10_EN.md)
- [Bilingual reproducibility ZIP](paper/WRRA_M_0_10_Reproducibility.zip)
- [Calculation and input ledger](calculations/wrra_m_0_10) · [32 verification groups](calculations/wrra_m_0_10/results/verification.json)
- [Document checks](calculations/wrra_m_0_10/results/document_checks.json) · [Clean-copy reproduction](calculations/wrra_m_0_10/results/reproduction_checks.json)
- [Completion record](REVISION_0_10.md) · [SHA256 manifest](SHA256SUMS_0_10)

```bash
python -m pip install -r calculations/wrra_m_0_10/requirements.txt
python calculations/wrra_m_0_10/run_release.py
```

## Completed 0.9 · 0.9 완료

Version 0.9 executes the common upstream arithmetic ledger and input contract, then routes phenotype weight through the actual 0.8 particle permutation. The frozen reference reproduces **5%·26.8%·68.2%**, **resident Actual 31.8%**, and **complete accounted weight 100%**. Pending SOURCE and completed return are distinct during the transition. All nine 0.8 results and their charges are unchanged.

같은 분모의 표현형·비표현형 잔존·복귀 장부를 실행하고 정규화한 조건부 채널 배분을 연결했다. 27개 검증 묶음을 통과했다. 산술 구성비는 기존 물리 에너지 구성비 4.93%·26.5%·68.57%와 별도로 보존한다. 복귀분을 배경 응답 출처로 대응시키되 SI 에너지·압력 함수는 다음 **0.10**에서 구현한다.

The corrected roadmap ends downstream development at **0.12** and retains **1.0** as the consolidated final edition. Physical quantization and records remain unimplemented in the closure ledger. Admission and channel weights here are construction and expected transport weights. The address-to-channel kernel is a disclosed constitutive input; masses, physical time and microscopic origins are subsequent work.

- [0.9 한국어 PDF](paper/WRRA_M_0_9_KO.pdf) · [DOCX](paper/WRRA_M_0_9_KO.docx) · [Markdown](paper/WRRA_M_0_9_KO.md)
- [0.9 English PDF](paper/WRRA_M_0_9_EN.pdf) · [DOCX](paper/WRRA_M_0_9_EN.docx) · [Markdown](paper/WRRA_M_0_9_EN.md)
- [0.9 bilingual reproducibility ZIP](paper/WRRA_M_0_9_Reproducibility.zip)
- [Calculation and input ledger](calculations/wrra_m_0_9) · [Verification](calculations/wrra_m_0_9/results/verification.json)
- [Upstream input contract](calculations/wrra_m_0_9/UPSTREAM_INTERFACE.md) · [Revised roadmap](calculations/wrra_m_0_9/ROADMAP_0_9_TO_1_0.md)
- [Document checks](calculations/wrra_m_0_9/results/document_checks.json) · [Clean-copy reproduction](calculations/wrra_m_0_9/results/reproduction_checks.json)
- [Development record](REVISION_0_9.md) · [SHA256 manifest](SHA256SUMS_0_9)

```bash
python -m pip install -r calculations/wrra_m_0_9/requirements.txt
python calculations/wrra_m_0_9/run_release.py
```

## Completed 0.8 · 0.8 완료

Version 0.8 runs the common carrier response, four-filter comparison, selection flow, channel permutation and one hypercharge operator in the same input ledger. With disclosed particle-origin orientation and readout calibration, all nine cases select **F_DX**. The reference gaps are **0.046691930387696756**. Exact charges and anomaly sums pass; adoption of three known generations gives 45 Standard-Model chiral components plus three conditional neutral extension slots.

공통운반자 응답에서 네 필터의 점수를 실제 계산하고, 선택된 순열에서 입자 배치와 전하를 산출했다. 공개한 보정 아래 9개 상태 모두 F_DX를 선택했다. 23개 검증 묶음, 한영 수식·표 대조, 저장 결과를 지운 깨끗한 복사본의 재현을 완료했다. 같은 격자·상태를 0.7의 부하·에너지·중력·팽창 장부에 연결한다.

The readout offset is an auxiliary calibration in a fixed weak-component basis; it is not an added mass or energy sector. Generation count is an adopted input; masses and mixing are not newly derived. Optimizer weights are construction weights. Under the corrected endpoint, physical quantization outcomes, probabilities, post-observation states and records remain unimplemented in the **0.12 closure ledger**.

- [0.8 한국어 PDF](paper/WRRA_M_0_8_KO.pdf) · [DOCX](paper/WRRA_M_0_8_KO.docx) · [Markdown](paper/WRRA_M_0_8_KO.md)
- [0.8 English PDF](paper/WRRA_M_0_8_EN.pdf) · [DOCX](paper/WRRA_M_0_8_EN.docx) · [Markdown](paper/WRRA_M_0_8_EN.md)
- [0.8 bilingual reproducibility ZIP](paper/WRRA_M_0_8_Reproducibility.zip)
- [Calculation and input ledger](calculations/wrra_m_0_8) · [Verification results](calculations/wrra_m_0_8/results/verification.json)
- [48-component charge inventory](calculations/wrra_m_0_8/results/particle_inventory.csv)
- [Document checks](calculations/wrra_m_0_8/results/document_checks.json) · [Clean-copy reproduction](calculations/wrra_m_0_8/results/reproduction_checks.json)
- [Development record](REVISION_0_8.md) · [SHA256 manifest](SHA256SUMS_0_8)

| Evaluation | WRRA-M 0.8 |
| --- | --- |
| Verification input / 검증 입력 | MCC 2.3.2, frozen 0.1–0.7 calculations, known particle-origin assignments, three generations and disclosed response calibration. |
| WRRA-specific transformation / WRRA 고유 변환 | Same-state resolvent intensities → common mismatch metric → four scores and selection flow → channel permutation → one hypercharge operator → normalized family replication. |
| Output / 산출값 | F_DX selected in nine cases; exact charge inventory and anomaly cancellation; computed ranks 16 and 48; unchanged inherited physical ledgers. |
| Falsification / 반증조건 | Failed calibrated selection, positivity/rank, charge or energy agreement; changed undisclosed input; treating optimizer weights as physical measurement probabilities. |

```bash
python -m pip install -r calculations/wrra_m_0_8/requirements.txt
python calculations/wrra_m_0_8/run_release.py
```

## Completed 0.7 · 0.7 완료

Version 0.7 fixes the common definitions of Actual, quantization, phenotype, residue and physical records. A positive additive **energy-weighted information-load measure** reproduces the 4.93% phenotype and 95.07% hidden reference, recalculates shares for changed states and scale, and bridges to the same 0.6-r2 energy, pressure, gravity and expansion calculations. The shares are allocation weights; measurement outcome probabilities and particle/filter selection are the subsequent development stages.

Actual·양자화·표현형·잔여·물리적 기록의 공통 정의와 에너지 가중 정보부하 측도를 확정했다. 기준 4.93%·95.07%를 재현하고 상태·공간 크기 변경 시 다시 계산한다. 같은 장부를 0.6-r2 물리 계산에 연결했다. 19개 검증 묶음과 한영 문서 대조를 완료했다.

- [0.7 한국어 PDF](paper/WRRA_M_0_7_KO.pdf) · [DOCX](paper/WRRA_M_0_7_KO.docx) · [Markdown](paper/WRRA_M_0_7_KO.md)
- [0.7 English PDF](paper/WRRA_M_0_7_EN.pdf) · [DOCX](paper/WRRA_M_0_7_EN.docx) · [Markdown](paper/WRRA_M_0_7_EN.md)
- [0.7 bilingual reproducibility ZIP](paper/WRRA_M_0_7_Reproducibility.zip)
- [Calculation and input ledger](calculations/wrra_m_0_7) · [Verification results](calculations/wrra_m_0_7/results/verification.json)
- [Development record](REVISION_0_7.md)

| Evaluation | WRRA-M 0.7 |
| --- | --- |
| Verification input / 검증 입력 | Frozen 0.6-r2 code and disclosed constants, late-universe fractions, state recipes and constitutive inputs. |
| WRRA-specific transformation / WRRA 고유 변환 | Positive sector-load traces, additive Actual measure, normalized phenotype/hidden shares and the same energy-pressure-gravity-expansion bridge. |
| Output / 산출값 | 4.93% / 95.07% reference reproduced; nine case ledgers, twenty-four additional state/exponent tests; inherited reference outputs retained. |
| Falsification / 반증조건 | Negative admissible load, partition or pressure mismatch, changed undisclosed inputs, failed bridge or claim of an unexecuted transition. |

```bash
python -m pip install -r calculations/wrra_m_0_7/requirements.txt
python calculations/wrra_m_0_7/run_release.py
```

## 0.6-r2 correction / 0.6-r2 교정

The 0.6 `lattice_N` now controls both information loads and the transport carrier test. Cross-input tests at 64/128 and 128/64 pass, with preserved baseline inputs and unchanged uniform reference outputs. Both language editions and the figure use “global twist record magnitude,” defined as the instantaneous load/size aggregate, without a separate temporal accumulation law. The adopted reference values remain q₀=−0.52855, v=207.510905 km/s and conditional deflection=0.535586511 arcsec.

정보부하와 수송 검사에 공통 격자를 적용하고 교차 입력을 검증했다. 한영 원고·그림에서 “전역 뒤틀림 기록의 크기”를 현재 부하·크기의 집계값으로 명시했다. 기존 기준 수치는 유지한다.

- [Correction record / 수정 기록](REVISION_0_6_R2.md)
- [Shared-grid regression results](calculations/wrra_m_0_6/results/release_checks.json)
- [Zenodo series release 0.6-r2](https://doi.org/10.5281/zenodo.23076547)

## 0.1–0.4 corrections / 0.1~0.4 수정

Correction r1 explicitly states complexification and independent Weyl-channel assumptions, the positive selection rate eta > 0 and nonzero target support, legitimate calibration provenance, and directly computed transport-Gram rank. Exact checks pass, including all 6,561 finite tables and 256 perturbation vertices. The 0.4 gap-eight construction and 0.5 gap-zero symmetric carrier are compatible. Stage 0.6 and its existing results are retained.

복소화·바일 채널 배정 가정, 양의 선택속도와 초기 지지, 보정 출처, 직접 계산한 랭크를 한영 원고에 명시했다. 기존 결과를 유지하며 네 검산 모두 통과했다.

- [Correction record / 수정 기록](REVISION_0_1_TO_0_4.md)
- [Reproduce 0.1–0.4 / 검산 실행](calculations/README_0_1_to_0_4.md)
- [Captured exact results](calculations/results/wrra_m_0_1_to_0_4)
- [Zenodo series release 0.6-r1](https://doi.org/10.5281/zenodo.23075976)

## Completed 0.6 · 0.6 완료

A finite homogeneous constitutive model now connects actual information-state loads, volume-derived pressure, state evolution, expansion and twist in one energy functional and classical action. The same clustering load enters the inherited calibrated rotation and conditional lens response. The energy exponents and information clock are disclosed choices; a unique microscopic law or full four-dimensional covariant completion is not claimed.

상태별 정보부하를 실제 계산하고 한 에너지 함수와 고전 동질 작용으로 압력·상태 진화·팽창·뒤틀림을 연결했다. 같은 모이는 부하를 기존 국소 회전·조건부 렌즈에 전달한다. 지수·연산자·정보 시계는 구성 선택으로 공개하며 실제 우주의 유일한 미시 법칙이나 완전한 4차원 공변 이론을 확정하지 않는다.

- [0.6 한국어 PDF](paper/WRRA_M_0_6_KO.pdf) · [DOCX](paper/WRRA_M_0_6_KO.docx) · [Markdown](paper/WRRA_M_0_6_KO.md)
- [0.6 English PDF](paper/WRRA_M_0_6_EN.pdf) · [DOCX](paper/WRRA_M_0_6_EN.docx) · [Markdown](paper/WRRA_M_0_6_EN.md)
- [0.6 complete bilingual reproducibility ZIP](paper/WRRA_M_0_6_Reproducibility.zip) · [Calculation](calculations/wrra_m_0_6) · [Summary](calculations/wrra_m_0_6/results/summary.json)

| Evaluation | WRRA-M 0.6 |
| --- | --- |
| Verification input / 검증 입력 | MCC 2.3.2, individual twist papers, editable whole-universe energy fractions and the corrected 0.5 calibration. |
| WRRA-specific transformation / WRRA 고유 변환 | Positive state-load traces; one energy operator, pressure derivative, unitary update and homogeneous classical action. |
| Output / 산출값 | q₀=-0.52855; 0.5 rotation and lensing reproduced; noncommuting state loads evolve; internal exchanges cancel and the independent acceleration solution preserves the Friedmann constraint. |
| Falsification / 반증조건 | Loss of positivity or trace, mismatched pressure derivative, failed conservation, acceleration constraint failure, or inconsistent inherited motion/lensing. |

```bash
python -m pip install -r calculations/wrra_m_0_6/requirements.txt
python calculations/wrra_m_0_6/compute.py
python calculations/wrra_m_0_6/verify.py
```

The PDFs contain matching 22 numbered native equations and 27 numerical/claim table rows. Full trajectories are in the complete ZIP and are regenerated by compute.py. The 0.6 start prototype is retained as a historical stage in calculations/wrra_m_0_6_start.

## Version 0.5 archive

- [한국어 개요](README_KO.md) · [English overview](README_EN.md)
- [0.5 한국어 PDF](paper/WRRA_M_0_5_KO.pdf) · [DOCX](paper/WRRA_M_0_5_KO.docx) · [Markdown](paper/WRRA_M_0_5_KO.md)
- [0.5 English PDF](paper/WRRA_M_0_5_EN.pdf) · [DOCX](paper/WRRA_M_0_5_EN.docx) · [Markdown](paper/WRRA_M_0_5_EN.md)
- [0.5 English reproduction ZIP](paper/WRRA_M_0_5_Reproducibility_EN.zip)
- [0.5 reproduction package](paper/WRRA_M_0_5_Reproducibility.zip) · [Calculation and results](calculations/wrra_m_0_5)

## Verification input → WRRA-specific transformation → Output → Falsification condition

| Stage | WRRA-M 0.5 |
| --- | --- |
| Verification input / 검증 입력 | MCC 2.3.2 mass modes, the 0.4 carrier criterion, earlier twist papers, and editable observed calibrations. |
| WRRA-specific transformation / WRRA 고유 변환 | Discrete mass phenotype and upstream continuous gravity; the same frozen twist response for motion and conditional lensing; a declared homogeneous 16-channel carrier. |
| Output / 산출값 | aT = 1.191812669 × 10⁻¹⁰ m/s²; finite spherical stress, rotation and conditional lensing; earlier Milky Way calculation reproduced with RMS 2.41784 km/s against its linearized reference; transport rank 16, ΔL = ΔR = 0. |
| Falsification condition / 반증조건 | Failed positivity/rank, a nonpositive gap for a positive-selection claim, static constitutive instability, or inconsistent motion/lensing require rejection or revision of the corresponding claim. |

## Scope / 범위

Version 0.5 selects the B_C model branch: quantized mass phenotypes and gravity without fundamental quantum degrees of freedom. Expansion and twist coexist; this calculation covers present static twist stress. Hidden information load is linked to twist and to a conditional finite, boundaryless T³ construction. It does not determine the actual cosmic topology or size.

0.5는 질량 양자화·중력 비양자화의 B_C 가지를 모형 전제로 선택한다. 팽창과 뒤틀림의 공존을 유지하고 현재의 정적 뒤틀림 응력을 계산한다. 표현형 이전 정보 부하와 꼬임 및 유한·무경계 공간을 조건부 수식으로 연결한다. 팽창 동역학과 실제 우주의 위상·크기 확정은 후속 범위다.

The calibrated constitutive response is actually computed within WRRA. The homogeneous carrier passes transport conditions but cannot uniquely select the target filter. The phenotype and hidden fractions remain editable estimates. The full Korean and English papers and bilingual overviews distinguish the executed results from the remaining microscopic and covariant work.

## Reproduce 0.5

```bash
python -m pip install -r calculations/wrra_m_0_5/requirements.txt
python calculations/wrra_m_0_5/compute.py --out calculations/wrra_m_0_5/results
```

## Earlier documents

- 0.4: [English PDF](paper/WRRA_M_0_4_EN.pdf) · [English DOCX](paper/WRRA_M_0_4_EN.docx) · [한국어 PDF](paper/WRRA_M_0_4_KO.pdf) · [한국어 DOCX](paper/WRRA_M_0_4_KO.docx) · [Verification script](calculations/verify_wrra_m_0_4.py)
- 0.3: [English PDF](paper/WRRA_M_0_3_EN.pdf) · [English DOCX](paper/WRRA_M_0_3_EN.docx) · [한국어 PDF](paper/WRRA_M_0_3_KO.pdf) · [한국어 DOCX](paper/WRRA_M_0_3_KO.docx)
- 0.2: [English PDF](paper/WRRA_M_0_2_EN.pdf) · [English DOCX](paper/WRRA_M_0_2_EN.docx) · [한국어 PDF](paper/WRRA_M_0_2_KO.pdf) · [한국어 DOCX](paper/WRRA_M_0_2_KO.docx)
- 0.1: [English PDF](paper/WRRA_M_0_1_EN.pdf) · [English DOCX](paper/WRRA_M_0_1_EN.docx) · [한국어 PDF](paper/WRRA_M_0_1_KO.pdf) · [한국어 DOCX](paper/WRRA_M_0_1_KO.docx)

## Version 0.4 foundations

## Verified inputs

The sixteen-channel space and target correspondence remain unchanged:

\[
\mathcal C_{16}=\mathbf1_0\oplus\mathbf7_A\oplus\mathbf7_B\oplus\mathbf1_N,
\]

\[
F_\times:\mathcal C_{16}\longrightarrow
(\mathbf4,\mathbf2,\mathbf1)\oplus(\bar{\mathbf4},\mathbf1,\mathbf2).
\]

Version 0.3 established the four-filter criterion

\[
F_{DX}\text{ is unique}\Longleftrightarrow\Delta_L>0\text{ and }\Delta_R>0.
\]

Minimal Computation Cosmology supplies a fifteen-channel common carrier. Version 0.4 does not relabel it as a sixteen-channel result. It asks whether it admits the extension

\[
\mathcal H_{16}=\mathcal H_{15}\oplus\mathcal H_N
\]

with one principal causal geometry, a positive semidefinite response Gram operator of rank sixteen, and positive carrier norm for the gauge-neutral channel.

## WRRA-specific transformation

For independently fixed common-carrier response signatures, 0.4 defines

\[
c_C(i,j)=-\lVert u_i-u_j\rVert_C^2.
\]

The two selection gaps then become exact carrier-metric alignments:

\[
\Delta_L=2\operatorname{Re}\langle u_{3_A}-u_{3_B},u_{1_A}-u_{1_B}\rangle_C,
\]

\[
\Delta_R=2\operatorname{Re}\langle u_{\bar3_A}-u_{\bar3_B},u_{1_N}-u_{1_0}\rangle_C.
\]

An exact finite witness gives \(\Delta_L=\Delta_R=8\), proving that the positive-gap region is nonempty. It is a constructibility witness, not a microscopic prediction.

## Boundary and falsification

The bridge fails if the neutral channel is transport-null, the principal causal cone splits by channel, the response metric is not positive semidefinite or full rank on the declared band, either independently calculated alignment is nonpositive, or the carrier protocol is retuned after the target is inspected. Version 0.5 evaluates a homogeneous numerical carrier and obtains zero selection gaps. Channel-specific microscopic responses that produce positive gaps remain open.

## Fixed evaluation rule

**Verification input → WRRA-specific transformation → Output → Falsification condition**

**검증 입력 → WRRA 고유 변환 → 산출값 → 반증조건**

The carrier, band, response extraction, metric, and channel labels must be fixed before the target outcome is evaluated. Version 0.4 is a conditional bridge theorem and calculation protocol, not empirical confirmation.

## Author

**Wonsik Choi / 최원식**

ORCID: [0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772)

Email: [janefather@gmail.com](mailto:janefather@gmail.com)

## Citation and license

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). The papers and documentation are licensed under [CC BY 4.0](LICENSE).



## Review corrections · 검토 반영

The 0.5 titles and claim ledger now foreground information load and twist gravity. Its local calculation uses 26.5% of the whole universe within the hidden total of 95.07%. The zero-phenotype input executes with undefined ratios recorded as null; the radius response ratio is evaluated numerically. The original scientific outputs reproduce unchanged.

[0.6 start, Korean](calculations/wrra_m_0_6_start/README_KO.md) · [0.6 start, English](calculations/wrra_m_0_6_start/README_EN.md) · [Start reproducibility archive](calculations/wrra_m_0_6_start/WRRA_M_0_6_Start_Reproducibility.zip). These files preserve the initial prototype. The completed finite homogeneous model and bilingual paper are provided above.


