# WRRA-M Research Notes

**Wonsik Reality Renderer Architecture Meta-dimensional Branch**

**원식 현실 렌더러 아키텍처 메타차원 연구 분기**

Latest development version: **WRRA-M 0.9** · 2026-10-01

Latest Zenodo archive: **WRRA-M 0.6-r2**.

WRRA-M continues WRRA Core 1.0 and Minimal Computation Cosmology 2.3.2.

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

## Completed 0.9 · 0.9 완료

Version 0.9 executes the common upstream arithmetic ledger and input contract, then routes phenotype weight through the actual 0.8 particle permutation. The frozen reference reproduces **5%·26.8%·68.2%**, **resident Actual 31.8%**, and **complete accounted weight 100%**. Pending SOURCE and completed return are distinct during the transition. All nine 0.8 results and their charges are unchanged.

같은 분모의 표현형·비표현형 잔존·복귀 장부를 실행하고 정규화한 조건부 채널 배분을 연결했다. 26개 검증 묶음을 통과했다. 산술 구성비는 기존 물리 에너지 구성비 4.93%·26.5%·68.57%와 별도로 보존한다. 복귀분을 배경 응답 출처로 대응시키되 SI 에너지·압력 함수는 다음 **0.10**에서 구현한다.

The revised roadmap incorporates all ten additional review items through 0.17 and the final 1.0 audit. Physical quantization and records now belong to **0.13**. Admission and channel weights here are construction and expected transport weights. The address-to-channel kernel is a disclosed constitutive input; masses, physical time and microscopic origins are subsequent work.

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

공통운반자 응답에서 네 필터의 점수를 실제 계산하고, 선택된 순열에서 입자 배치와 전하를 산출했다. 공개한 보정 아래 9개 상태 모두 F_DX를 선택했다. 22개 검증 묶음, 한영 수식·표 대조, 저장 결과를 지운 깨끗한 복사본의 재현을 완료했다. 같은 격자·상태를 0.7의 부하·에너지·중력·팽창 장부에 연결한다.

The readout offset is an auxiliary calibration in a fixed weak-component basis; it is not an added mass or energy sector. Generation count is an adopted input; masses and mixing are not newly derived. Optimizer weights are construction weights. Under the revised roadmap, physical quantization outcomes, probabilities, post-observation states and records are scheduled for **0.13** after common accounting and the physical energy/pressure bridge.

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

Actual·양자화·표현형·잔여·물리적 기록의 공통 정의와 에너지 가중 정보부하 측도를 확정했다. 기준 4.93%·95.07%를 재현하고 상태·공간 크기 변경 시 다시 계산한다. 같은 장부를 0.6-r2 물리 계산에 연결했다. 16개 검증 묶음과 한영 문서 대조를 완료했다.

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


