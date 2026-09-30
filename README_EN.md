# WRRA-M 0.3 English Overview

## Research decision

WRRA-M 0.3 turns the single open assumption left by version 0.2 into a finite selection problem. The cross-dimensional filter is not added as independent machinery. It is the stable winner of Source-supplied compatibility values under a fixed Law.

## Verification input

Version 0.3 retains the sixteen-channel space and target correspondence of version 0.2:

\[
\mathcal C_{16}=\mathbf1_0\oplus\mathbf7_A\oplus\mathbf7_B\oplus\mathbf1_N,
\]

\[
F_{\times}:\mathcal C_{16}\rightarrow
(\mathbf4,\mathbf2,\mathbf1)\oplus(\bar{\mathbf4},\mathbf1,\mathbf2).
\]

Independently swapping the left and right singlet assignments produces the complete minimal class

\[
\mathcal F_4=\{F_{DX},F_{XX},F_{DD},F_{XD}\}.
\]

Every candidate preserves all channels and the common color action.

## WRRA-specific transformation

Source supplies a left and right scalar compatibility table. Law scores a filter by summing the four entries selected by its two matchings.

Define the direct-left advantage and crossed-right advantage:

\[
\Delta_L=(\ell_{AA}+\ell_{BB})-(\ell_{AB}+\ell_{BA}),
\]

\[
\Delta_R=(r_{AN}+r_{B0})-(r_{A0}+r_{BN}).
\]

The values must be computed or measured by a rule fixed before the target filter is evaluated.

## Output

The 0.2 target \(F_{DX}\) is the unique maximum-score filter exactly when

\[
\Delta_L>0
\quad\text{and}\quad
\Delta_R>0.
\]

Positive filter weights evolve under the constant-score replicator flow

\[
\dot p_F=\eta p_F(C(F)-\bar C).
\]

If both gaps are positive and the target has nonzero initial weight, its weight converges to one. The minimum gap

\[
\delta=\min(\Delta_L,\Delta_R)
\]

sets the exponential convergence rate. The selection also survives every entrywise compatibility perturbation bounded by \(\rho\) when \(\delta>4\rho\).

## Falsification condition

The 0.3 result fails within its stated scope if:

- an independently specified Source and Law give either gap a nonpositive value;
- a fifth admissible filter equals or exceeds the target score;
- fixed-score filter weights violate the published ratio law;
- uncertainty exceeds the stated stability margin; or
- scores or candidates are changed after the target is inspected.

## Exact boundary

Version 0.3 proves a theorem inside a defined four-filter class. It does not calculate the compatibility tables from fundamental physics, prove that the class is complete in a deeper theory, or show that nature supplies positive gaps. Until upstream values are fixed independently, the result is a conditional theorem and a measurement protocol rather than empirical confirmation.

## Files

- [Full English paper PDF](paper/WRRA_M_0_3_EN.pdf)
- [Full English paper DOCX](paper/WRRA_M_0_3_EN.docx)
- [Korean overview](README_KO.md)
- [Version 0.2 English PDF](paper/WRRA_M_0_2_EN.pdf)
- [Version 0.1 English PDF](paper/WRRA_M_0_1_EN.pdf)

## Identity

Wonsik Choi · ORCID [0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772) · [janefather@gmail.com](mailto:janefather@gmail.com)
