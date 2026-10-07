# Finite Source Closure in WRRA_M
## A Klein–Zeta candidate generator for a 1,015,000-address universe

**Wonsik Choi, Jeongin Choi**  
7 October 2026  
Independent research note / WRRA_M upstream candidate v0.1

## Abstract

WRRA_M is a finite-source implementation of the WRRA framework for our universe. Its published upstream ledger uses finite integer addresses, an address weight proportional to \(n^{-\alpha}\), a finite zeta-driven admission rule, and a three-sector arithmetic partition. The previous implementation used \(N=1,000,000\) as a declared finite address cutoff, while the size of the finite generation window remained an upstream open problem. This work tests a candidate closure rule that replaces a computational cutoff by a generated finite source size.

The construction uses three already-present WRRA_M structures. First, the exact decimal sector ledger \(0.05:0.268:0.682\) has least common denominator \(L=500\). Second, the inherited harmonic neutrino ledger contains the integer modes \((0,5,29)\), giving \(H=29\). Third, the interval \(0<t\le 2\pi H\) contains exactly \(C=70\) nontrivial Riemann-zeta zeros. A finite Euler–Maclaurin evaluator truncated at \(M=LH=14,500\) reproduces the first 70 zero locations with a maximum residual \(5.29\times10^{-13}\) in \(|\zeta_M(1/2+i\gamma_k)|\). The candidate finite source size is therefore defined by the explicit construction hypothesis

\[
N_U=LHC=500\times29\times70=1,015,000.
\]

With all original arithmetic parameters frozen, replacing \(N=1,000,000\) by \(N_U\) changes the three-sector shares only to \(5.000002539\%\), \(26.800001829\%\), and \(68.199995632\%\). A minimal two-parameter recalibration to the already-validated sector targets gives \(\alpha=1.8996877935161325\) and \(h=1.4476744689338703\), with derived \(\beta_{\rm eff}=0.8654567230719301\). Keeping the downstream SI response coefficients frozen then yields \(q_0=-0.5285585894\), a reference rotation speed of \(207.5102419\,\mathrm{km\,s^{-1}}\), and conditional finite-patch lensing of \(0.5355822400\) arcsec. The 0.12 proper-time energy update conserves total energy to a maximum relative error below \(10^{-15}\).

The result is classified **PASS-C**: \(N_U=1,015,000\) is admissible as a WRRA_M finite-generation-window candidate, but not yet as a uniquely derived fundamental constant. The unresolved step is the physical derivation of the product rule \(N_U=LHC\) and of the mapping \(T=2\pi H\); both are explicit falsifiable construction hypotheses rather than hidden assumptions.

## 1. Scope and evaluation rule

This paper evaluates the candidate in the sequence required by WRRA methodology:

\[
\text{verification inputs}\rightarrow\text{WRRA-specific transformation}\rightarrow\text{outputs}\rightarrow\text{falsification conditions}.
\]

The objective is not to claim an independent prediction as a prerequisite for theoretical value. Validated constants and observed quantities may be used to fix a model. Once those inputs are frozen, quantities calculated through WRRA-specific structure are treated as model outputs. The present task is narrower: determine whether the previously unresolved finite generation window can be replaced by an explicit finite generator without breaking the published WRRA_M ledger.

## 2. Verification inputs

The frozen upstream arithmetic inputs are

\[
\alpha_0=1.8996876950554356,
\qquad
h_0=1.44767317035244,
\qquad
\beta_0=0.8654570124136961,
\]

with eight admission frames, phase step \(\xi=0.1\), and the first four adopted zeta-zero ordinates

\[
14.134725141734695,\;21.022039638771556,\;25.01085758014569,\;30.424876125859512.
\]

The common arithmetic target ledger is

\[
(\phi,D,R)=(0.05,0.268,0.682).
\]

The inherited harmonic candidate uses

\[
(n_1,n_2,n_3)=(0,5,29).
\]

The downstream test keeps the published 0.10 SI response coefficients frozen:

\[
\eta_\phi=7.561582499072265\times10^{-10},
\]
\[
\eta_D=7.285761328795971\times10^{-10},
\]
\[
\eta_R=7.646102818811323\times10^{-10}\;\mathrm{J\,m^{-3}}.
\]

No downstream coefficient is refitted in the regression tests reported below.

## 3. WRRA-specific transformation

### 3.1 Minimal finite sector ledger

The three arithmetic shares can be written with the common denominator 500:

\[
0.05=\frac{25}{500},\qquad
0.268=\frac{134}{500},\qquad
0.682=\frac{341}{500}.
\]

The least common denominator of the reduced fractions is therefore

\[
L=500.
\]

This is an address-ledger resolution, not a claim that cosmic energy is made of 500 literal objects.

### 3.2 Harmonic address

The previously frozen harmonic ledger contains the maximum integer mode

\[
H=29.
\]

No new fit is performed to obtain 29 in this paper.

### 3.3 Finite zeta focus window

Define the finite phase window

\[
0<t\le T_H,\qquad T_H=2\pi H.
\]

For \(H=29\),

\[
T_H=182.2123739082080.
\]

There are exactly 70 standard nontrivial zeta zeros with positive ordinate below this boundary. The last included ordinate is

\[
\gamma_{70}=182.20707848436646,
\]

so

\[
T_H-\gamma_{70}=0.00529542384155.
\]

The next zero is

\[
\gamma_{71}=184.87446784838751,
\]

and is outside the window.

To keep the numerical evaluation finite, the verification code uses the Euler–Maclaurin form

\[
\zeta_M(s)=\sum_{n=1}^{M-1}n^{-s}
+\frac{M^{1-s}}{s-1}
+\frac12M^{-s}
+\frac{s}{12}M^{-s-1}
-\frac{s(s+1)(s+2)}{720}M^{-s-3},
\]

with

\[
M=LH=14,500.
\]

At the first 70 standard zero ordinates, the maximum finite-evaluator residual is

\[
\max_{k\le70}\left|\zeta_M\left(\frac12+i\gamma_k\right)\right|
=5.29\times10^{-13}.
\]

The residual at \(\gamma_{70}\) is \(6.98\times10^{-14}\).

A secondary alignment check scans \(H=1,\ldots,29\). The distance between \(2\pi H\) and its nearest zeta zero is smallest at \(H=29\); the next-best case is \(H=9\), with a distance of about 0.10242. This is supporting structure only and is not used as a fit target.

### 3.4 Candidate finite SOURCE size

The candidate rule is

\[
\boxed{N_U=LHC}.
\]

Therefore

\[
\boxed{N_U=500\times29\times70=1,015,000}.
\]

This product is an explicit construction hypothesis. The present paper verifies its consequences but does not claim that the independence of the three factors has already been microscopically derived.

### 3.5 Boundary closure

A Klein-type closure may be imposed by identifying one boundary after an orientation reversal. In schematic coordinates,

\[
(0,y)\sim(1,y),\qquad(x,0)\sim(1-x,1).
\]

This provides a finite but boundaryless address topology without requiring a physically realized completed infinity. In the present release the topology supplies the closure interpretation; it does not alter the arithmetic regression calculation.

## 4. Outputs

### 4.1 Zero-refit address test

With \(N=1,015,000\) and all original upstream parameters frozen, the ledger becomes

| Sector | Baseline \(N=1,000,000\) | Candidate \(N=1,015,000\) |
|---|---:|---:|
| phenotype \(\phi\) | 5.000000000% | 5.000002539% |
| resident nonphenotype \(D\) | 26.800000000% | 26.800001829% |
| return \(R\) | 68.200000000% | 68.199995632% |

The ledger remains positive and sums to unity. The candidate domain contains 79,608 prime addresses, 507,499 even-composite addresses, and 427,892 odd-composite addresses over \(n=2,\ldots,N_U\).

### 4.2 Minimal target-preserving recalibration

The validated arithmetic targets are then reimposed using only the same two fit degrees of freedom already present in the 0.9 model: \(\alpha\) fixes the even-composite share and \(h\) fixes the phenotype admission share. No third fit is used for \(\beta\).

The result is

\[
\alpha_1=1.8996877935161325,
\]
\[
h_1=1.4476744689338703,
\]
\[
\beta_{\rm eff,1}=0.8654567230719301.
\]

Relative to the frozen baseline,

\[
\Delta\alpha=9.8461\times10^{-8},
\]
\[
\Delta h=1.2986\times10^{-6},
\]
\[
\Delta\beta_{\rm eff}=-2.8934\times10^{-7}.
\]

The recalibrated arithmetic ledger is, to numerical precision,

\[
(\phi,D,R)=(0.05,0.268,0.682).
\]

### 4.3 Frozen-SI downstream regression

The SI response coefficients are not recalibrated after changing the address window. The resulting reference outputs are

| Output | Published baseline | \(N_U=1,015,000\), minimal arithmetic recalibration |
|---|---:|---:|
| \(q_0\) | -0.5285500000 | **-0.5285585894** |
| rotation speed | 207.5109051 km/s | **207.5102419 km/s** |
| conditional finite-patch lensing | 0.5355865106 arcsec | **0.5355822400 arcsec** |

The small changes are genuine consequences of the altered address moments under frozen downstream coefficients. They are not hidden refits.

### 4.4 Proper-time energy conservation

The 128-site noncommuting carrier test was repeated with the candidate address moments and the frozen energy coefficients. At proper frames \(0,1,2,4,8\), the total energy remains constant at approximately

\[
3.20076293\times10^{-10}\;\mathrm{J}.
\]

The maximum relative energy variation is

\[
9.99\times10^{-16},
\]

and the maximum trace error of the evolved density matrix is below \(10^{-15}\). Internal \(D/R\) loads change while the total is conserved, as required by the existing 0.12 ledger.

## 5. Falsification conditions

The candidate must be rejected or revised if any of the following occurs.

1. **Product-rule failure.** A more primitive WRRA derivation shows that \(L\), \(H\), and \(C\) are not independent address axes or that their combination is not multiplicative.
2. **Window-rule failure.** The mapping \(T=2\pi H\) cannot be derived from the WRRA phase ledger or a competing finite mapping provides a better closed account with fewer assumptions.
3. **Topology failure.** The Klein-type orientation-reversing closure conflicts with the actual carrier or filter state transformation.
4. **Ledger failure.** The generated finite window cannot preserve the validated sector ledger under the declared limited calibration policy.
5. **Downstream failure.** Frozen SI coefficients produce negative energy, broken normalization, nonconservation, or unacceptable failure of the previously validated gravity/expansion outputs.
6. **Non-uniqueness without resolution.** Multiple equally simple finite generators survive all tests but produce materially different \(N_U\) values. In that case \(1,015,000\) remains one admissible construction rather than a unique WRRA_M prediction.

## 6. Assessment

### Verification input

Existing WRRA_M arithmetic targets, frozen \(\alpha_0,h_0,\beta_0\), harmonic mode 29, zeta structure, and the previously calibrated downstream SI coefficients.

### WRRA-specific transformation

\[
(0.05,0.268,0.682)\to L=500,
\]
\[
(0,5,29)\to H=29,
\]
\[
0<t\le2\pi H\to C=70,
\]
\[
(L,H,C)\to N_U=LHC=1,015,000,
\]
followed by the existing finite address filter, residue partition, SI energy bridge, and proper-time update.

### Output

The candidate window is finite, preserves arithmetic completeness, requires only minute target-preserving changes to the already-declared arithmetic calibration, and remains stable under the frozen downstream physical bridge.

### Falsification condition

The construction is not accepted as uniquely fundamental until the multiplicative independence rule and the \(2\pi H\) zeta-window rule are derived or independently constrained inside WRRA_M.

## 7. Conclusion

The present result is classified

\[
\boxed{\text{PASS-C}}
\]

and the value

\[
\boxed{N_U=1,015,000}
\]

is adopted as a **WRRA_M finite-generation-window candidate**. This changes the status of the address bound from a purely convenient numerical cutoff to a value produced by an explicit finite WRRA construction. It is not yet promoted to a uniquely derived fundamental constant.

The next decisive task is not another numerical fit. It is to derive, reduce, or falsify the two remaining construction laws: \(T=2\pi H\) and \(N_U=LHC\). If those survive a more primitive carrier/filter derivation, the finite SOURCE closure can be promoted from candidate to internal WRRA_M law.

## Reproducibility

Run:

```bash
python verify_kzf.py
```

Dependencies: Python 3, NumPy, SciPy, mpmath. The script writes `results.json` and reports the candidate generator, arithmetic regression, downstream outputs, and proper-time conservation test.

## Provenance

This note extends the WRRA_M 0.1–0.12 integrated line and preserves the distinction between arithmetic address shares and the inherited physical energy calibration. No claim is made that the decimal sector targets, harmonic mode 29, or downstream SI anchors were independently predicted in this paper. The original provenance of those inputs remains unchanged.
