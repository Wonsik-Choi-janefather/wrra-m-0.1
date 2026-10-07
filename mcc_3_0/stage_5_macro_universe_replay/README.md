# Minimal Computing Cosmology 3.0 — Stage 5 Macro-Universe Replay

**Status:** PASS  
**Date:** 2026-10-07  
**Authors:** Wonsik Choi, Jeongin Choi

Stage 5 propagates the Stage-4 finite-SOURCE Master Ledger through the frozen WRRA_M homogeneous expansion and local gravity renderer without refitting any SI coefficient.

## Verification input

From Stage 4:

[
(E_phi,E_D,E_R)=
(3.78079124953614	imes10^{-11},
2.03218543006515	imes10^{-10},
5.25855017259595	imes10^{-10}) {m J}
]

at the reference volume (V_0=1,{m m^3}), with

[
P_R=-ho_R,qquad P_phi=P_D=0.
]

Frozen WRRA_M macro inputs remain unchanged:

- (u_{m crit}=7.668947767821907	imes10^{-10},mathrm{J,m^{-3}})
- (H_0=67.4,mathrm{km,s^{-1},Mpc^{-1}})
- local clustering fraction reference (f_c=0.265)
- test Plummer source: (6	imes10^{10}M_odot), scale radius 3 kpc
- test radius 8.2 kpc
- conditional lens patch radius 200 kpc, impact 10 kpc
- same frozen local interpolation and lensing rule

No macro coefficient is refitted.

## WRRA-specific transformation

The inherited volume exponents are

[
(n_phi,n_D,n_R)=(0,0,3).
]

Therefore at scale factor (a),

[
ho_phi(a)=E_phi/a^3,
]

[
ho_D(a)=E_D/a^3,
]

[
ho_R(a)=E_R,
]

and

[
P(a)=-ho_R.
]

The homogeneous diagnostics are

[
rac{H(a)}{H_0}=sqrt{rac{ho(a)}{u_{m crit}}},
]

[
q(a)=rac12rac{ho(a)+3P(a)}{ho(a)}.
]

The same (D)-sector density drives the inherited local scale

[
a_T(a)=a_{T,0}
sqrt{rac{ho_D(a)}{u_{m crit}f_c}}.
]

That same (a_T) is passed to both the reference rotation and the conditional finite-patch lensing calculation. No independent rotation or lensing fit is allowed.

## Output

### Homogeneous expansion replay

| (a) | (ho) J/m³ | (H/H_0) | (q) |
|---:|---:|---:|---:|
| 0.5 | (2.4540666613	imes10^{-9}) | 1.7888556123 | 0.1785814590 |
| 1.0 | (7.6688147276	imes10^{-10}) | 0.9999913260 | -0.5285585894 |
| 2.0 | (5.5598332420	imes10^{-10}) | 0.8514575347 | -0.9187161585 |

The acceleration-transition scale factor in this uniform constitutive branch is

[
oxed{a_{m trans}=0.6119598068}.
]

At (a=1), the unchanged reference (H_0) normalization gives an effective replay value

[
67.39941537 {m km,s^{-1},Mpc^{-1}},
]

the tiny offset arising solely because the new finite SOURCE changes the frozen-reference total density by (1.73	imes10^{-5}).

### Local gravity, rotation and conditional lensing

| (a) | (a_T) m/s² | rotation km/s | lensing arcsec |
|---:|---:|---:|---:|
| 0.5 | (3.3708841807	imes10^{-10}) | 247.7482202 | 0.8146640474 |
| 1.0 | (1.1917875314	imes10^{-10}) | 207.5102419 | 0.5355822400 |
| 2.0 | (4.2136052259	imes10^{-11}) | 181.5744855 | 0.3743154242 |

The direct baryonic rotation reference remains

[
161.4505105 {m km,s^{-1}}
]

at all three scale factors because the test baryonic source itself is frozen.

### Difference from the legacy (N=1,000,000) branch

At (a=1):

[
Delta q=-8.58944	imes10^{-6},
]

[
Delta v=-6.63261	imes10^{-4} {m km,s^{-1}},
]

[
Delta	heta=-4.27055	imes10^{-6} {m arcsec}.
]

Relative changes are only

[
1.63	imes10^{-5},quad
3.20	imes10^{-6},quad
7.97	imes10^{-6},
]

respectively.

Across (a=0.5,1,2), all macro outputs remain close to the frozen legacy branch without any SI refit.

## Interpretation

Stage 5 establishes a single executed path

[
oxed{
	ext{finite SOURCE}
ightarrow
	ext{address/filter}
ightarrow
	ext{Master energy ledger}
ightarrow
	ext{pressure/expansion}
ightarrow
	ext{same local gravity}
ightarrow
	ext{rotation+lensing}
}.
]

This is a model consistency result. The reference rotation and conditional lensing values are not new astronomical measurements.

## Falsification conditions

Stage 5 fails if:

1. the finite-SOURCE Master Ledger produces negative total density;
2. homogeneous pressure is not the derivative-compatible pressure inherited from the same energy ledger;
3. the Friedmann-like (H/H_0) diagnostic becomes undefined;
4. rotation and lensing require separate refits or different local gravity scales;
5. the direct baryonic source changes during candidate replay;
6. any SI response coefficient or local-gravity coefficient is refitted;
7. a macro result is reported without its legacy delta and verification data;
8. internal component views from Stage 4 are added again as extra cosmic energy.

## Verdict

[
oxed{	ext{Stage 5 = PASS}}
]

The finite-SOURCE candidate survives the full declared macro replay with frozen coefficients and one shared energy/gravity ledger.

Stage 6 may now perform the final end-to-end closure, provenance audit and MCC 3.0 release build.
