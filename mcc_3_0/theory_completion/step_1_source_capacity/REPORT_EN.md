# WRRA 3.0 theory completion — reviewed Step 1

**8 October 2026 · review release r1**

## Verified inputs → WRRA-specific transformation → outputs → falsification conditions

| Assessment item | Evidence |
|---|---|
| Verified inputs | Frozen calibrated address fractions 0.05/0.268/0.682, inherited H=29 and C=70, published MCC 3.0 filter parameters, SI and local-gravity coefficients |
| WRRA-specific transformation | Minimal rational resolution → finite SOURCE → prime/composite phase filter → address load → SI energy → volume-derivative pressure → shared local gravity and homogeneous expansion |
| Outputs | Reference replay and capacity-dependent propagation in three configurations without refitting |
| Falsification conditions | Failed normalization/conservation/handoffs, hidden refitting, separate rotation/lensing gravity scales, duplicated resources |

**Decision: Step 1 remains complete within the declared uniform and conditional local-gravity branch.** This is a reproducibility and consistency result, not a new observational experiment.

## Construction and update policy

The adopted conditional rule is

\[
L=\operatorname{lcm}(\text{reduced denominators of frozen calibrated fractions}),\qquad N=LHC.
\]

The reference yields L=500 and N=1,015,000. Writing 0.05 as 0.0500 leaves the rational value unchanged. Changing the value is a model-input change, not a formatting change. New observations test a frozen model; an explicit recalibration regenerates its SOURCE in a new model version.

Capacity invariance under changed inputs is not required. The requirement is a declared generation rule with consistent downstream propagation. Calibration using verified values is legitimate. Known-value reproduction remains a consistency and explanatory achievement; numerical novelty is not imposed as an additional completion criterion.

N counts SOURCE address codes. The inactive reference address 1 makes the executable count N−1. N, rational resolution L, internal carrier channels and conditional-readout rank are distinct types. The existing origin kernel aggregates address contributions, so it does not require every address identity to remain separately distinguishable in the downstream channel inventory. The provisional composition-to-phase construction is not adopted in this release.

## Frozen probes and results

| SOURCE selecting fractions | L | N |
|---|---:|---:|
| 0.05 / 0.268 / 0.682 | 500 | 1,015,000 |
| 0.0505 / 0.2680 / 0.6815 | 2,000 | 4,060,000 |
| 0.0501 / 0.2680 / 0.6819 | 10,000 | 20,300,000 |

All probes retain alpha=1.8996877935161325, threshold h=1.4476744689338703, the zeta-phase drive, address-response lambda, SI eta, energy exponents and local-source/lens geometry. These are the previously calibrated MCC 3.0 reference values. Changed probe fractions select N; the filter is not recalibrated to reproduce those fractions. Output-minus-input residuals are retained in the results.

| N | q at a=1 | Rotation km/s | Conditional lensing arcsec |
|---:|---:|---:|---:|
| 1,015,000 | -0.5285585894376318 | 207.5102418659153 | 0.5355822400088303 |
| 4,060,000 | -0.5292825795228291 | 207.4541349970819 | 0.5352210185078975 |
| 20,300,000 | -0.529977941992902 | 207.40039181157826 | 0.5348750792521283 |

Each probe is evaluated at a=0.5, 1 and 2. The direct baryonic reference remains 161.45051053125528 km/s. SOURCE changes reach the load moments, energy, pressure and macro outputs through frozen rules. These probes are separate model configurations, not time evolution of SOURCE capacity.

For expansion, the conservation check is the continuity equation rather than constant total energy:

\[
P_s=-\partial E_s/\partial V,\qquad
d\rho_s/d\ln a+3(\rho_s+P_s)=0.
\]

## Review and completion scope

The review pins byte-exact original functions to one source commit, checks their hashes, and verifies all frozen inputs after each probe. Centered numerical continuity derivatives supplement the algebraic identity. Rotation and lensing acceleration inputs, fixed baryonic reference, finite outputs and positive densities are checked. The streamed address calculation matches the original monolithic reference calculation.

All 13 registered implementation/replay checks pass. These are not 13 independent physical experiments. One command regenerates and compares the registered arithmetic and macro outputs.

Completion covers conditional SOURCE generation and upstream-to-downstream capacity transport in the uniform carrier, homogeneous energy-pressure/expansion branch and conditional Plummer weak-field lens patch. H=29, T=2πH and C=70, the LHC product domain, arithmetic classifier, uniform carrier loads and the local Phi=Psi condition remain disclosed assumptions. No new proof of their physical necessity, direct measurement of cosmic capacity, or nonuniform covariant completion is claimed.

The next step examines the structural relation between address serialization and prime/composite classification.
