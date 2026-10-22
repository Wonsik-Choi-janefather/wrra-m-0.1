
\clearpage

# Appendix J. Execution supplements and editorial conventions

## J.1 Verified inputs and edition scope

Preserve the complete Korean and English v0.28-r5 books and connect the actual records of KZF rigor v1.0, SPARC benchmark v0.3 and falsification v0.4. This appendix integrates results into the document. It does not join the separate programs into a complete cosmological execution path. This is edition v0.28-r6; DOI: https://doi.org/10.5281/zenodo.23551789. Historical DOIs identify their historical editions.

The evaluation order is verified inputs → WRRA-specific transformation → outputs → falsification conditions → conclusion. Known observations and constants are legitimate calibration inputs; reproduction through WRRA structures is an explanatory achievement. Independent novel numerical prediction is not required as a criterion of originality.

## J.2 Meaning, units and types

Retain the local symbols of inherited equations. The disambiguating aliases below are editorial conventions, not replacements of original code variables or additional physical quantities.

| Original symbol / distinguishing alias | Meaning, unit and boundary |
|---|---|
| $g_b,g_{obs}$ | Baryonic and observed gravitational acceleration, m/s$^2$ |
| $g_{opt}$ | Dimensionless optical coupling in Chapter 122; originally $g$ |
| $g_{\mu\nu},\det g$ | Metric and its determinant; coordinate/unit convention dependent |
| $L_{addr}$ | SOURCE integer resolution 500, dimensionless; originally $L$ |
| $L_{eff},D_{path}$ | Effective optical exposure and path difference, both m; not presumed identical |
| $H_{reg}$ | Register size 29 adopted from the maximum harmonic; serialization $h=0,\ldots,28$ |
| $H_{Hub},\widehat H$ | Hubble rate(s$^{-1}$) and Hamiltonian(energy in its physical form); distinct from a dimensionless generator |
| $C_{zero},\Sigma_{obs}$ | Zero count 70 and measurement covariance; covariance entries carry the product of the two observable units (variance has squared units) |
| $Q_{gate},Q_{stat},Q_A^\nu$ | Boolean permission, dimensionless residual statistic, energy-momentum exchange vector |
| $B_{bar},E_{ledger},origin\_id$ | Baryon count, ledger energy(MeV or stated units), source identifier |
| $N_{active\ parts},N_{reserve}$ | Active component count and reserve-origin count; one component may contain several origins |
| $A,p,s,q_{curv},t_{turn}$ | Fitted amplitude, gradient, stellar scale, curvature, turnover radius ratio; dimensionless |
| $R,R_{pivot},R_t$ | Physical radius, pivot and turnover radius; kpc in the fits, $R_t=t_{turn}R_{pivot}$ |
| $k_{fit},k_{wave}$ | Estimated parameter count and wave number; integer and inverse length respectively |

The curvature parameter $q_{curv}$ is not the cosmological deceleration $q_0$; $t_{turn}$ is not physical time. $A_m$ is a zeta output-port operator, not the fitting amplitude $A$. Identical letters do not authorize substitution across incompatible types, domains or units.

Baryons, active components, addresses and primitive component types are different counts. Unused origins may remain in an inactive reserve. Do not assign equal per-origin energies to aggregate terms lacking a defined allocation. Historical expansions of WRRA follow their source and the discussion in Chapter 137; editing does not invent a new expansion.

State unit conversions with their values. Energy density $u=\rho_{mass}c^2$ is J/m$^3$, dimensionally equivalent to pressure Pa. Record conversion factors between MeV and SI ledgers. A dimensionless numerical generator is distinct from a physical Hamiltonian. Covariance, residuals, AIC and BIC must identify the observable likelihood and definitions used.

## J.3 Mathematical and computational record

Use exact rational input denominators, the harmonic convention and the strict boundary $\gamma<T$. The result is $L=500,H=29,C=70$, with 1,015,000 addresses:1 inactive reference,79,608 primes,507,499 even composites and 427,892 odd composites. The active address domain 1,014,999 is not a material-particle count.

The attached package records 15/15 inherited checks,44/44 new boundary/exception checks, detection of 9/9 isolated corruptions, and comparison of the entire stored address ledger. The hardened audit implementation addresses the inherited use of global H instead of its argument, the C=0 case and boundary inclusion. It has not already replaced the published global execution path.

Euler–Maclaurin truncation error is separated from floating-point rounding. A recorded example shows that increasing the cutoff does not monotonically improve float64 error. Finite-zero verification is not an RH proof; the 50/80-digit comparison uses the same mpmath family.

## J.4 Observational record

Use the same SPARC sample and errors with galaxy-specific stellar mass-to-light scaling. The following full fits use 9 clean galaxies and 257 points. NFW has 3 parameters per galaxy; both new WRRA candidates have 4, with the additional penalty included. BIC is the sum of galaxy-level $\chi^2+k\log n$.

| Model | $\chi^2$ | AIC | BIC |
|---|---:|---:|---:|
| NFW | 1013.78 | 1067.78 | 1100.83 |
| WRRA curvature | 784.13 | 856.13 | 900.20 |
| WRRA turnover | 951.80 | 1023.80 | 1067.86 |

\Needspace{12\baselineskip}
For $x=R/R_{pivot}$, the two candidates are:

$$a_T=a_{T0}A\exp[p\ln x+q_{curv}(\ln x)^2],$$
$$a_T=a_{T0}Ax^p\frac{1+1/t_{turn}}{1+x/t_{turn}}.$$

Both actually invoke the inherited response:

$$g=\frac{g_b}{1-\exp(-\sqrt{g_b/a_T})}.$$ These are observationally calibrated extensions of the stress response, not derivations of a new covariant field equation.

| Held-out check | NFW $\chi^2$/point | Curvature | Turnover |
|---|---:|---:|---:|
| Interleaved 48 points | 2.0505 | 1.6763 | 2.3564 |
| Outer 20%,56 points | 15.2907 | 48.1963 | 4.2500 |

Curvature improves the full fit and interleaved check but deteriorates in the outer region. Turnover improves the outer check but is worse than NFW on the interleaved check. Do not combine the best scores from different candidates into one model's performance. Galaxy-level BIC wins are 3/9 and 2/9, respectively, and bootstrap intervals include zero. Aggregate fitting superiority is not superiority for every galaxy. Candidate development followed inspection of earlier results; this is not confirmation on a new external sample. It also does not complete lensing, CMB or a separate BTFR regression.

## J.5 Falsification, revision and execution status

Distinguish input/implementation failure, frozen-branch failure, joint-connection failure and failure of a core conservation/causal contract. A valid core counterexample requires review of that claim and dependent outputs. One candidate's failure does not automatically reject every structure. If outputs remain incompatible across the declared shared parameter and nuisance domain, revise the corresponding connection. A single optimizer failure does not prove an empty allowed domain.

For the new judge, exit 0 denotes observed comparison advantage or non-rejection;1 denotes failure of the specified claim or rejection of a frozen branch;2 denotes invalid input;3 denotes unconfirmed mapping or unestablished population superiority. This is a program-specific convention, not a retrospective reinterpretation of every historical exit code.

Twelve claim-level decisions were made on actual SPARC results, with 11/11 new rule checks and 22/22 inherited synthetic optical checks. Curvature outer superiority and turnover interleaved superiority exit 1. An unconfirmed natural optical coupling prevents interpreting a null signal as physical falsification. Passing synthetic checks does not complete an optical observation.

Calibration revision is legitimate model construction. Preserve previous inputs, parameters and failures; disclose new assumptions, freedoms and affected outputs. Undisclosed post-hoc refitting of the same output is prohibited. A new version's success does not erase the old version's failure.

\Needspace{15\baselineskip}
## J.6 Reproduction, editorial scope and conclusion

Appendix J incorporates the separate results of items 1–3 into both language versions and connects symbols, units and roles. Attached code ZIPs preserve actual logs. These checks are not counted as rerun during editing. Automated document checks cover inherited text and equations, heading identifiers, image existence and bilingual numerical tables. They do not certify semantic perfection of every equation or the truth of the entire physics model.

Edition v0.28-r6 has DOI 10.5281/zenodo.23551789; preceding published DOI: 23550759. See repository PUBLICATION_RESULT.json for online status. KDP registration and format validation were not performed. Document/code links are supplied, while complete cosmological execution integration remains a separate scope.
