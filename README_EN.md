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

The finite witness proves constructibility only. Version 0.4 does not calculate physical response signatures from a microscopic carrier and does not claim that nature supplies the required positive alignments. That numerical carrier calculation is reserved for 0.5 or later.

## Files

- [Full English paper PDF](paper/WRRA_M_0_4_EN.pdf)
- [Full English paper DOCX](paper/WRRA_M_0_4_EN.docx)
- [Markdown source](paper/WRRA_M_0_4_Common_Carrier_Metric_Origin_EN.md)
- [Exact verification script](calculations/verify_wrra_m_0_4.py)
- [Korean overview](README_KO.md)
- [Version 0.3 English PDF](paper/WRRA_M_0_3_EN.pdf)

## Identity

Wonsik Choi · ORCID [0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772) · [janefather@gmail.com](mailto:janefather@gmail.com)
