# WRRA-M 0.6 Information Load and Twist Gravity with Expansion

Wonsik Choi · 2026-10-01 · CC BY 4.0

Version 0.6 completes a finite homogeneous constitutive model. Weighted state loads are explicitly evaluated. One energy functional and classical homogeneous action connect state evolution, pressure, expansion and twist. Its clustering load is passed into the inherited calibrated local rotation and conditional lens response. WRRA Core 1.0 and MCC 2.3.2 remain the baseline.

| Stage | Executed content |
| --- | --- |
| Verification input | Whole-universe fractions: phenotype 4.93%, hidden load 95.07%, clustering 26.5%, residual background 68.57%; inherited response and 16-channel carrier |
| WRRA-specific transformation | State traces of positive load operators, one energy functional, volume-derived pressure, unitary update and classical homogeneous action |
| Output | Present q=-0.52855; reproduced aT=1.191812669e-10 m/s², rotation and lensing; evolving noncommuting loads with cancelling internal exchange |
| Falsification condition | Loss of trace/positivity, inconsistent pressure derivative, failed total conservation, violated independent acceleration constraint, inconsistent motion/lensing |

The exponents nc=0 and nb=3, operators and information clock are disclosed constitutive choices. Pressure and conservation follow from those choices. Unique microscopic laws, absolute cosmic length, a complete four-dimensional covariant local theory and spatial perturbation stability remain outside the completed claim. Symmetric-carrier filter gaps remain zero. Quantizable mass phenotypes and the nonquantum fundamental-gravity premise remain distinguished.

## 0.1–0.4 corrections / 0.1~0.4 수정

Correction r1 explicitly states complexification and independent Weyl-channel assumptions, the positive selection rate eta > 0 and nonzero target support, legitimate calibration provenance, and directly computed transport-Gram rank. Exact checks pass, including all 6,561 finite tables and 256 perturbation vertices. The 0.4 gap-eight construction and 0.5 gap-zero symmetric carrier are compatible. Stage 0.6 and its existing results are retained.

복소화·바일 채널 배정 가정, 양의 선택속도와 초기 지지, 보정 출처, 직접 계산한 랭크를 한영 원고에 명시했다. 기존 결과를 유지하며 네 검산 모두 통과했다.

- [Correction record / 수정 기록](REVISION_0_1_TO_0_4.md)
- [Reproduce 0.1–0.4 / 검산 실행](calculations/README_0_1_to_0_4.md)
- [Captured exact results](calculations/results/wrra_m_0_1_to_0_4)
- [Zenodo series release 0.6-r1](https://doi.org/10.5281/zenodo.23075976)

## Files

- [0.6 한국어 PDF](paper/WRRA_M_0_6_KO.pdf) · [DOCX](paper/WRRA_M_0_6_KO.docx)
- [0.6 English PDF](paper/WRRA_M_0_6_EN.pdf) · [DOCX](paper/WRRA_M_0_6_EN.docx)
- [Complete reproducibility ZIP](paper/WRRA_M_0_6_Reproducibility.zip) · [Calculation directory](calculations/wrra_m_0_6)

## Reproduce

```bash
python -m pip install -r calculations/wrra_m_0_6/requirements.txt
python calculations/wrra_m_0_6/compute.py
python calculations/wrra_m_0_6/verify.py
```

compute.py reads parameters.json and baseline_0_5/parameters.json, then creates results/results.json, summary and plots. verify.py compares the frozen 0.5 outputs and checks basis changes and boundary inputs. Outputs default to the script directory; --out selects another location. To regenerate manuscript tables, complete computation and verification in the default directory, then run:

```bash
python calculations/wrra_m_0_6/write_papers.py
python calculations/wrra_m_0_6/build_reports.py
```

Document creation additionally needs pandoc and python-docx. Korean rendering uses Noto Sans CJK KR and English uses Liberation Serif/Sans. Both editions have 22 editable native Word equations and identical numerical tables. PDFs were converted from Word using LibreOffice.

The complete ZIP includes both PDF/DOCX editions, full trajectories in results.json, summary, release checks, plots, source manuscripts and code. The GitHub calculation directory provides summary, checks and plots; obtain full trajectories from the ZIP or a computation. baseline_0_5/results.json is the corrected frozen 0.5 comparison record.

Preserved purity and state eigenvalues follow from the declared unitary construction. Numerical consistency is distinguished from observational validation. The geometric energy operator replaces the start model fixed-kernel restriction; its historical prototype remains separately available.

---

# WRRA-M 0.5 English Overview

**Information Load and Twist Gravity in a Finite Model**

Wonsik Choi · 2026-10-01 · ORCID [0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772) · [janefather@gmail.com](mailto:janefather@gmail.com)

## Verification input → WRRA-specific transformation → Output → Falsification condition

| Stage | Version 0.5 |
| --- | --- |
| Verification input | Minimal Computation Cosmology 2.3.2, the 0.4 carrier criterion, the constitutive response actually adopted in the earlier WRRA Galactic Disk paper, and editable observed calibrations. |
| WRRA-specific transformation | Distinguish discrete mass phenotypes from the upstream continuous geometric response; evaluate the same frozen twist response for motion and conditional lensing; evaluate a declared homogeneous 16-channel carrier. |
| Output | Transition scale 1.191812669 × 10⁻¹⁰ m/s²; finite spherical stress and rotation; conditional 200 kpc lens contribution; reproduction of the earlier Milky Way algebraic calculation with RMS 2.41784 km/s against its linearized Eilers reference; full transport rank 16 and both selection gaps zero. |
| Falsification condition | Loss of transport positivity or rank, failure of an asserted positive gap, negative static constitutive eigenvalues, or inconsistent motion and lensing in the same geometry require rejection or revision of the corresponding claim. |

## Scope and result

Version 0.5 selects the B_C branch as a model premise: mass may be quantized as a phenotype, while gravity has no fundamental quantum degree of freedom in this branch. This is not presented as a universal experimental or mathematical proof of nonquantization.

Expansion and twist coexist in the architecture. The executed sector is present static twist stress; cosmological expansion dynamics remain a subsequent calculation. The hidden energy-weighted information load is connected to twist through a quadratic stress relation. A declared T³ gluing example gives a conditional finite, boundaryless construction; it does not determine the actual cosmic topology or size.

The constitutive response is calibrated, explicitly evaluated inside this WRRA calculation, and not claimed to be uniquely derived from the microscopic carrier. The homogeneous carrier passes the transport conditions but does not uniquely select the target filter: ΔL = ΔR = 0. The carrier-specific response differences needed for positive selection remain unresolved.

The phenotype and hidden fractions are editable estimates rather than immutable 5/95 laws. The code distinguishes the whole hidden fraction from the clustering-stress fraction used for the local acceleration scale.

## Files and reproduction

- [English PDF](paper/WRRA_M_0_5_EN.pdf) · [English DOCX](paper/WRRA_M_0_5_EN.docx) · [English Markdown source](paper/WRRA_M_0_5_EN.md)
- [Korean PDF](paper/WRRA_M_0_5_KO.pdf) · [Korean DOCX](paper/WRRA_M_0_5_KO.docx)
- [Korean Markdown source](paper/WRRA_M_0_5_KO.md)
- [Complete reproduction ZIP](paper/WRRA_M_0_5_Reproducibility.zip)
- [Calculation directory](calculations/wrra_m_0_5) · [Recorded results](calculations/wrra_m_0_5/results/results.json)

The full English edition preserves all 15 equations and all 19 numerical table rows of the Korean original.

- [English reproduction ZIP](paper/WRRA_M_0_5_Reproducibility_EN.zip)
- [English document builder](calculations/wrra_m_0_5/build_report_en.py)

```bash
python -m pip install -r calculations/wrra_m_0_5/requirements.txt
python calculations/wrra_m_0_5/compute.py --out calculations/wrra_m_0_5/results
```

The lens output is conditional on Φ = Ψ and includes only the declared 200 kpc patch. The Milky Way RMS is a comparison with the earlier linearized reference, not a new fit to individual observations. A covariant completion and a quantum-matter/classical-geometry update law are not supplied.

CC BY 4.0. Earlier versions 0.1–0.4 remain available.

---

# WRRA-M 0.4 English Overview

## Research decision

WRRA-M 0.4 tests whether the common carrier of Minimal Computation Cosmology can own the compatibility rule left unspecified by WRRA-M 0.3. The answer is conditionally yes, but the established fifteen-channel carrier cannot simply be renamed as a sixteen-channel solution.

## Verification input

Version 0.2 supplied the sixteen-channel space

\[
\mathcal C_{16}=\mathbf1_0\oplus\mathbf7_A\oplus\mathbf7_B\oplus\mathbf1_N,
\]

and version 0.3 proved that the target filter is unique inside its fixed four-filter class exactly when

\[
\Delta_L>0,\qquad\Delta_R>0.
\]

Minimal Computation Cosmology supplies a common transport structure for fifteen chiral Standard-Model channels.

## WRRA-specific transformation

Version 0.4 conditionally extends the carrier by one gauge-neutral channel:

\[
\mathcal H_{16}=\mathcal H_{15}\oplus\mathcal H_N.
\]

The extension is admissible only if all sixteen channels share one principal causal geometry, the response Gram operator is positive semidefinite and full rank on the declared band, and the neutral channel has positive carrier norm. Gauge-current neutrality must not be confused with transport absence.

For response signatures fixed independently of the target, define

\[
c_C(i,j)=-\lVert u_i-u_j\rVert_C^2.
\]

The formerly free gaps then reduce exactly to

\[
\Delta_L=2\operatorname{Re}\langle u_{3_A}-u_{3_B},u_{1_A}-u_{1_B}\rangle_C,
\]

\[
\Delta_R=2\operatorname{Re}\langle u_{\bar3_A}-u_{\bar3_B},u_{1_N}-u_{1_0}\rangle_C.
\]

## Output

The existing common-carrier idea is structurally reusable after a genuine fifteen-to-sixteen-channel extension. One positive response metric replaces eight free compatibility entries by one rule and eight calculated signatures. An exact finite witness yields

\[
\Delta_L=\Delta_R=8
\]

and proves that the positive-gap region is nonempty.

## Falsification condition

The 0.4 bridge fails if the neutral channel is transport-null, the causal cone becomes channel-dependent, the response Gram operator is not positive semidefinite or full rank, the response construction is not gauge invariant, an independently frozen carrier gives either alignment a nonpositive sign, or the protocol is altered after inspecting the target.

## Exact boundary

The finite witness proves constructibility only. Version 0.4 does not calculate physical response signatures from a microscopic carrier and does not claim that nature supplies the required positive alignments. Version 0.5 executes a homogeneous carrier calculation and finds zero selection gaps; a microscopic positive-selection response remains open.

## Files

- [Full Korean paper PDF](paper/WRRA_M_0_4_KO.pdf)
- [Full Korean paper DOCX](paper/WRRA_M_0_4_KO.docx)
- [Korean Markdown source](paper/WRRA_M_0_4_Common_Carrier_Metric_Origin_KO.md)
- [Full English paper PDF](paper/WRRA_M_0_4_EN.pdf)
- [Full English paper DOCX](paper/WRRA_M_0_4_EN.docx)
- [Markdown source](paper/WRRA_M_0_4_Common_Carrier_Metric_Origin_EN.md)
- [Exact verification script](calculations/verify_wrra_m_0_4.py)
- [Korean overview](README_KO.md)
- [Version 0.3 English PDF](paper/WRRA_M_0_3_EN.pdf)

## Identity

Wonsik Choi · ORCID [0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772) · [janefather@gmail.com](mailto:janefather@gmail.com)



## Review corrections and 0.6 start

The local outputs use the clustering sector, 26.5% of the whole universe, within the hidden total of 95.07%. The information-load map in 0.5 is a constitutive hypothesis; individual state weights were not computed there. Zero phenotype input now executes, with undefined source ratios recorded as null, and the radius response ratio is evaluated from both accelerations. Original motion, lensing and carrier results reproduce unchanged.

The [0.6 start scope and calculation](calculations/wrra_m_0_6_start/README_EN.md) implement an explicit carrier load operator and compare declared background pressure closures. This is an executed prototype, the historical initial prototype.
