# Clock and boundary source contract

Wonsik Choi · WRRA_M 0.12 · 2026-10-03 · CC BY 4.0

Source actually read: WRRA_M_Upper_Two_Stage_Filter_Hypothesis_v1_0_r1_KO_2026_10_02.pdf, 15 pages. The following is a source summary and implementation contract, not a new measured input.

- Page 5: an ordered update X_(k+1)=T_k(X_k) introduces a candidate shutter interval; no measured minimum-time identification follows.
- Pages 11–12: U=exp(-i H delta_tau/hbar) connects allowed modes and boundary conditions to an energy branch E=hbar(theta+2 pi ell)/delta_tau. The integer branch and generator must be supplied. A free continuous dispersion and confined discrete spectrum can coexist with discrete updates.
- Pages 11–12: clocks follow their own worldlines and causal order; there is no externally visible universal simultaneous shutter. Lorentz/proper-time comparisons and numerical continuum approximations must be checked.
- Planck time is a comparison scale. No physical infinite support, new particle identity, confinement length or measured epsilon is supplied by this contract.

Implementation decisions: epsilon=0.05 with the frozen electron energy unit; finite spectral N=128; periodic/antiperiodic fold phases; periodic/Dirichlet spatial boundaries; cavity length 20 hbar c/mu_E. All appear as constitutive inputs in parameters.json.

External primary reference for adopted spacetime clock formulas: Scott Hughes, MIT 8.033 Fall 2024 lecture notes, sections 18.2–18.3: https://ocw.mit.edu/courses/8-033-introduction-to-relativity-and-spacetime-physics-fall-2024/mit8_033_f24_lec_full.pdf . The finite matrix, phase-branch and convergence controls are explicitly computed in this release.
