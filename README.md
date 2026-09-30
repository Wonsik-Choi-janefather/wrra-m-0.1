# WRRA-M Research Notes

**Wonsik Reality Renderer Architecture Meta-dimensional Branch**

**원식 현실 렌더러 아키텍처 메타차원 연구 분기**

Latest version: **WRRA-M 0.3**

Latest result: **A necessary and sufficient two-gap criterion for unique and stable selection of the 0.2 cross-dimensional filter within a four-filter sector**

WRRA-M is a research branch of WRRA Core 1.0. It studies how predimensional degrees can be rendered into finite spacetime and particle-channel phenotypes. Version 0.3 keeps the sixteen-channel algebra of 0.2 and asks a narrower question: under what fixed Source and Law does the target filter win against every binary pairing alternative?

WRRA-M은 WRRA Core 1.0의 연구 분기다. 선차원 자유도가 유한한 시공간과 입자채널 표현형으로 렌더링되는 구조를 탐구한다. 0.3은 0.2의 16채널 대수를 그대로 두고 더 좁은 질문을 묻는다. 어떤 고정된 소스와 법칙 아래에서 목표 필터가 모든 이진 짝지음 대안을 이기는가이다.

## Latest documents

### WRRA-M 0.3

- [English PDF](paper/WRRA_M_0_3_EN.pdf) · [English DOCX](paper/WRRA_M_0_3_EN.docx)
- [한국어 PDF](paper/WRRA_M_0_3_KO.pdf) · [한국어 DOCX](paper/WRRA_M_0_3_KO.docx)
- [English overview](README_EN.md)
- [한국어 개요](README_KO.md)

### Earlier versions

- 0.2: [English PDF](paper/WRRA_M_0_2_EN.pdf) · [English DOCX](paper/WRRA_M_0_2_EN.docx) · [한국어 PDF](paper/WRRA_M_0_2_KO.pdf) · [한국어 DOCX](paper/WRRA_M_0_2_KO.docx)
- 0.1: [English PDF](paper/WRRA_M_0_1_EN.pdf) · [English DOCX](paper/WRRA_M_0_1_EN.docx) · [한국어 PDF](paper/WRRA_M_0_1_KO.pdf) · [한국어 DOCX](paper/WRRA_M_0_1_KO.docx)

## Fixed input from WRRA-M 0.2

The sixteen-channel space and target correspondence remain unchanged:

\[
\mathcal{C}_{16}=\mathbf{1}_{0}\oplus\mathbf{7}_{A}\oplus\mathbf{7}_{B}\oplus\mathbf{1}_{N},
\]

\[
F_{\times}:\mathcal{C}_{16}\longrightarrow
(\mathbf{4},\mathbf{2},\mathbf{1})\oplus(\bar{\mathbf{4}},\mathbf{1},\mathbf{2}).
\]

Version 0.3 does not use the Standard Model charges recovered in 0.2 as inputs to its selection score.

## Four-filter admissible sector

Two binary assignments generate four candidates:

\[
\mathcal{F}_{4}=\{F_{DX},F_{XX},F_{DD},F_{XD}\}.
\]

The first label records the left assignment. The second records the right assignment. The 0.2 target is \(F_{DX}\): direct on the left and crossed on the right. Every candidate preserves all sixteen channels and the common \(SU(3)\) action.

## Source values and Law

Source supplies two real scalar compatibility tables:

\[
W_L=(\ell_{ij})_{i,j\in\{A,B\}},
\qquad
W_R=(r_{ij})_{i\in\{A,B\},\ j\in\{N,0\}}.
\]

Law assigns each filter the sum of the four entries selected by its two matchings. For the target,

\[
C(F_{DX})=\ell_{AA}+\ell_{BB}+r_{AN}+r_{B0}.
\]

These scalar values rank pairings. They are not linear maps between inequivalent color representations and do not mix color components.

## Exact selection criterion

Define

\[
\Delta_L=(\ell_{AA}+\ell_{BB})-(\ell_{AB}+\ell_{BA}),
\]

\[
\Delta_R=(r_{AN}+r_{B0})-(r_{A0}+r_{BN}).
\]

The three target-minus-competitor score differences are \(\Delta_L\), \(\Delta_R\), and \(\Delta_L+\Delta_R\). Therefore

\[
F_{\times}=F_{DX}\text{ is unique}
\quad\Longleftrightarrow\quad
\Delta_L>0\text{ and }\Delta_R>0.
\]

A zero gap gives a degeneracy. A negative gap selects the corresponding alternative.

## Selection flow and stability

For positive initial weights, Law uses the constant-score replicator flow

\[
\dot p_F=\eta p_F\bigl(C(F)-\bar C\bigr),
\qquad
\bar C=\sum_{G\in\mathcal F_4}p_GC(G).
\]

When both gaps are positive, \(p_{\times}(t)\to1\). With

\[
\delta=\min(\Delta_L,\Delta_R),
\]

the non-target weight obeys

\[
1-p_{\times}(t)
\le
\frac{1-p_{\times}(0)}{p_{\times}(0)}
e^{-\eta\delta t}.
\]

If every score entry changes by at most \(\rho\), the same filter is guaranteed to remain selected whenever

\[
\min(\Delta_L,\Delta_R)>4\rho.
\]

## Boundary and falsification

WRRA-M 0.3 proves existence, uniqueness, convergence, and perturbation stability only inside the stated finite candidate class and only after the compatibility tables are fixed independently.

It does **not** derive numerical compatibility values from fundamental physics or prove that nature supplies positive gaps. The claim fails if an independently specified Source and Law give a nonpositive gap, if an admissible fifth filter matches or beats the target, if the published weight-ratio law fails, or if the scores are retuned after the target is inspected.

## Fixed evaluation rule

**Verification input → WRRA-specific transformation → Output → Falsification condition**

**검증 입력 → WRRA 고유 변환 → 산출값 → 반증조건**

The admissible class, compatibility rule, score tables, rate, and initial support must be fixed before the target outcome is evaluated. Until upstream values are supplied, 0.3 is an exact conditional theorem and measurement protocol rather than empirical confirmation.

## Author

**Wonsik Choi / 최원식**

ORCID: [0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772)

Email: [janefather@gmail.com](mailto:janefather@gmail.com)

## Citation and license

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). The papers and documentation are licensed under [CC BY 4.0](LICENSE).
