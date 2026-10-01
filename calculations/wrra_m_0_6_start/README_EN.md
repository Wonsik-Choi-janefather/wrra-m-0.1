# WRRA-M 0.6 start: information load, twist gravity and expansion

Wonsik Choi · 2026-10-01 · Scope and executed initial prototype

This start calculation connects a common-carrier state to a weighted physical information load, then to twist and the inherited local gravity response. It also compares expansion and twist evolution under three explicitly declared background pressure closures. WRRA Core 1.0 and MCC 2.3.2 remain the baseline. The Korean README gives the full scope and references.

For the positive semidefinite periodic cycle Laplacian K on 128 sites, the carrier state is R=(I₁₆/16)⊗ρ, with trace ρ=1. The dimensionless load is J=Tr(ρK). A single disclosed calibration gives u_pre=ηJ, with the uniform reference J₀=2 matched to the present hidden fraction 0.9507. The operator and calibration are constitutive choices, not a unique microscopic information law or universal energy per bit.

The clustering share χ=0.265/0.9507 is a declared input. The full hidden density determines ζκ_tot²=16πG u_pre/c⁴, whereas only u_c=χu_pre enters a_T²=πG u_c/3. The latter is the same calibrated relation as a_T=cH√(f_c/8) in 0.5. A changed load changes the instantaneous flat-background H consistently. The Plummer test-source rotation and finite-patch lensing reuse 0.5; lensing assumes Φ=Ψ. These state comparisons are not a new observed-galaxy fit or a galaxy's temporal evolution.

| State | J | a_T (m/s²) | Test velocity at 8.2 kpc (km/s) |
|---|---:|---:|---:|
| Uniform reference | 2.000000 | 1.191813e-10 | 207.510905 |
| Low mode | 0.152241 | 3.288204e-11 | 177.250177 |
| Coherent packet | 0.657554 | 6.833742e-11 | 192.003913 |
| High mode | 4.000000 | 1.685478e-10 | 219.215978 |
| Zero mode | 0 | 0 | 161.450511 |

The reference reproduces 0.5. The zero state is in this kernel's nullspace; zero-load lensing is uncomputed and recorded as null. The symmetric-carrier selection gaps remain zero.

For a representative T³ with L=L₀a and W=ζΣΘᵢ², u∝W/a². A source-free component with p=wu therefore requires dlnW/dln a=−1−3w. The program integrates this relation and compares it with its analytic solution and an independent finite-difference continuity check.

| Declared closure | q at a=1 |
|---|---:|
| Entire hidden record fixed, w=−1/3 | +0.024650 |
| Cold clustering plus fixed-record background | +0.157150 |
| Cold clustering plus constant-energy background, w_bg=−1 | −0.528550 |

Only the third test accelerates at the chosen present fractions. Its pressure is an input, and its background equations have the ΛCDM form. It is not a microscopic proof that twist causes acceleration. There is no separately added dark component or cosmological constant counted over the same background load. With fixed positive ζ, accumulated twist record and physical twist rate can evolve differently during expansion.

The current scope does not derive state evolution, a common covariant action, anisotropic stress, sound speed, lens slip, perturbation stability, a twist photon-redshift kernel, observed topology or an absolute cosmic length. A compact boundaryless T³ by itself does not imply an extra local gravity field. Fundamental nonquantum gravity remains a model premise, rather than a result of the matrix prototype.

The same fixed kernel and calibration impose a necessary load bound 0≤J≤4 on trace-one states. The background requires J=2u_pre(a)/u_pre(1). The three histories enter this domain at a=0.707107, 0.740789 and 0.601829 respectively. All three are outside it at a=0.5; those plot segments are dotted. Within the domain, a zero/high-mode mixture gives an algebraic state witness and its weight is recorded. This does not derive pressure or state evolution. Connecting the entire background interval requires an explicit geometric dependence of the kernel or a change in the state-density accounting.

## Reproduce

```bash
python -m pip install -r requirements.txt
python compute_start.py
```

Use parameters.json and baseline_0_5/parameters.json for all inputs and calibrations. Outputs are results/results.json and results/background_start.png. The baseline code includes the reviewed zero-phenotype boundary fix and the directly evaluated radius-response ratio. requirements.txt lists the required numerical libraries.

Background reference: Trodden & Carroll, TASI Lectures, §2.2, https://vo.ned.ipac.caltech.edu/level5/Sept03/Trodden/Trodden2_2.html. Project references and scope are listed in README_KO.md.

© 2026 Wonsik Choi. Executed start prototype; not a completed 0.6 paper.
