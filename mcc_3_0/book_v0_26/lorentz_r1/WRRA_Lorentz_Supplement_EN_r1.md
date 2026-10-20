---
title: "Minimal Computing Cosmology 3.0: Chapter 135 Supplement"
subtitle: "Lorentz consistency of light transport and one-clock sequential output"
author: "Wonsik Choi · Jeongin Choi"
date: "2026-10-19 | v0.25 supplement r1"
lang: en
---

## Lorentz consistency of sequential output and the existing light-transport framework

**Verified inputs.** We retain the 15-channel, 64-shutter transport check in Chapter 112 (maximum relative speed discrepancy approximately $6.24\times10^{-14}$), the seven-direction, 64-shutter check in Chapter 117 (approximately $2.80\times10^{-13}$), the existing clock interval and its local-frame interpretation. Those checks reproduce the adopted light speed and directional consistency. The present calculation connects this framework to the two output events and intermediate conservation ledger of Chapter 135. Relativistic proper time and four-vector transformations provide verification and reinforcement [S4].

**WRRA-specific transformation.** Existing clock → local time on an effective source worldline → reservation of conjugate output → intermediate-state conservation → next output → frame-dependent readout. Physical proper time is not assigned to prephenotypic SOURCE addresses. Here, the source is an effective physical source/environment that owns the output events and energy-momentum in spacetime.

**(a) Making the local clock explicit.** The clock in section 135.9 is defined in the source rest frame. For this sequential-output interface, we adopt that interval as the proper-time interval along the source worldline. This construction makes the earlier local-time definition specific to sequential output.

$$\Delta\tau_{\rm clk}=1.4813019664158633\times10^{-21}\ {\rm s},\qquad\tau_{k+1}-\tau_k=\Delta\tau_{\rm clk},\qquad\kappa_{k+1}=-\kappa_k.$$

Each source's $k$ is its own worldline execution index. Equal indices at distant sources do not impose absolute simultaneity. Any required phase relationship between sources must be specified through physical preparation and interaction. The conjugate label $\kappa$ and code $n$ are not coordinate-axis names: changing inertial frame does not change matter into antimatter or alter $2n\to n+n$. Upper/lower placement denotes local internal structure, without a universal fixed vertical axis. Complete spin and internal-quantum-number dynamics remain a separate specification.

**(b) Transforming the output events.** Use metric signature $(+,-,-,-)$. An effective source moving inertially between outputs has four-velocity $u^\mu$ satisfying $u_\mu u^\mu=c^2$. The event displacement is

$$\Delta z^\mu=u^\mu\Delta\tau_{\rm clk},\qquad\Delta z_\mu\Delta z^\mu=c^2\Delta\tau_{\rm clk}^2>0.$$

In its rest frame, $\Delta\mathbf x=0$ and $\Delta t=\Delta\tau_{\rm clk}$. In a frame moving at velocity $V$ relative to that frame,

$$\Delta t'=\gamma_V\Delta\tau_{\rm clk},\qquad\Delta x'=-\gamma_V V\Delta\tau_{\rm clk},\qquad\gamma_V=(1-V^2/c^2)^{-1/2}.$$

Thus $\Delta t'>0$ under time-orientation-preserving Lorentz transformations. The first output precedes the second in every such frame. Coordinate-time intervals change; the proper-time interval remains one tick. An accelerated source requires $\Delta z^\mu=\int u^\mu d\tau$, rather than the constant-four-velocity expression. Event ordering along a future-directed timelike worldline also remains unchanged in that case.

| Relative speed $V/c$ | $\gamma_V$ | Coordinate-time interval between outputs (s) |
|---:|---:|---:|
| 0 | 1 | $1.4813019664\times10^{-21}$ |
| 0.6 | 1.25 | $1.8516274580\times10^{-21}$ |
| 0.8 | 1.666666667 | $2.4688366107\times10^{-21}$ |
| 0.99 | 7.088812050 | $1.0500671229\times10^{-20}$ |

The source execution rate per coordinate time in this example is $f'=f_0/\gamma_V$. This is distinct from the Doppler frequency of received light signals. The existing shutter is not interpreted as a photon's proper time.

**(c) Executing the intermediate ledger with recoil.** Use $c=m=1$ for the calculation. Assign the equal-rest-mass conjugate pair four-momenta $p_1=(E,p,0,0)$ and $p_2=(E,-p,0,0)$, with $E=\sqrt{1+p^2}$. Choose an initially neutral source $P=(10,0,0,0)$ and a final neutral remnant $q=(10-2E,0,0,0)$. These are consistency-test inputs, not fitted masses of new particles.

$$P=p_1+R,\qquad R=p_2+q,\qquad R=P-p_1.$$

After the first output, $R$ owns the opposite charge and remaining energy-momentum. The intermediate source has $m_R=\sqrt{R_\mu R^\mu}>0$, recoils with $u_R=R/m_R$ in these units, and emits the partner after one proper-time tick. This $u_R$ determines the output-event displacement. Charge is conserved at each stage: $0=(+1)+(-1)$ and $(-1)=(-1)+0$. Applying the same Lorentz transformation to all four-momenta preserves both conservation equations. This is an effective kinematic example with an explicit intermediate state; it does not calculate actual electron-positron production amplitudes or rates.

**(d) Reading separation.** The expression $d=|v_1|\Delta\tau$ in section 135.10 applies to the restricted nonrecoiling-source rest-frame example. It must not be applied indiscriminately using coordinate time in another frame. For simultaneous separation in the recoiling-source frame, select the event $x_1$ on the first particle's trajectory satisfying $u_R\cdot(x_1-z_B)=0$ and read

$$d_{\rm source}=\sqrt{-(x_1-z_B)_\mu(x_1-z_B)^\mu}.$$

This scalar distance is unchanged when the same source-simultaneous hypersurface is transformed. Different observers can choose different simultaneous hypersurfaces and obtain different distances without contradiction. The existing $c\Delta\tau=0.4440831575520451$ pm remains the light-speed reference distance in the source rest frame.

**Outputs.** With fixed random seed 135112117, we executed 630 combinations of 18 directions, seven speed magnitudes from zero through $0.99c$, and five momentum settings. The 126 transformation settings include directional duplicates at zero speed. Checks jointly cover the proper-time interval, conjugate mass shells, conservation at each output, inverse transformation, null transport and separation on the source-simultaneous hypersurface.

| Check | Maximum error |
|---|---:|
| Normalized timelike event interval | $4.27\times10^{-14}$ |
| Normalized mass-shell residual | $6.84\times10^{-13}$ |
| Two-stage four-momentum conservation, divided by initial energy 10 | $2.14\times10^{-15}$ |
| Normalized inverse-transformation residual of event displacement | $2.13\times10^{-14}$ |
| Relative light-speed discrepancy after transformation | $3.42\times10^{-14}$ |
| Normalized source-simultaneous separation residual | $2.71\times10^{-14}$ |

The second event remained future-directed in every case. Errors are double-precision numerical residuals. Mass-shell, inverse-transformation and separation residuals use $\max(1,|\text{reference value}|)$ in the denominator. As a negative control, transforming the spatial displacement while forcing every frame's coordinate interval to remain one tick gives a normalized interval of $-0.777777778$ instead of 1 at $V=0.8c$. This incorrect absolute-coordinate-time rule does not even preserve a timelike interval and is excluded.

**Falsification conditions.** This implementation fails if rerunning the fixed inputs produces a normalized residual above $10^{-10}$, if a future-directed transformation reverses event order, if the intermediate source requires negative energy or a nonphysical state, or if charge or four-momentum fails to close at either stage. This numerical threshold is an implementation criterion, not an experimental uncertainty. Once connected to an actual channel, disagreement with measured production timing, correlations or conserved quantities requires revising the physical interface.

**Conclusion.** Retaining the existing light-transport framework, we executed equal-only conjugate splitting, one-clock sequential output, recoil and intermediate bookkeeping as locally covariant kinematics. The clock reuses the existing WRRA input without fitting another time constant. This is a concrete connection achieved for Chapter 135. It does not establish covariance of the complete finite-grid operator under all boosts, interacting amplitudes, microscopic causality or phase synchronization across all sources.

[S4] Richard Fitzpatrick, University of Texas at Austin, [*Proper time* and the linked four-velocity lecture](https://farside.ph.utexas.edu/teaching/em/lectures/node114.html). This source supports the proper-time transformation; it is not observational evidence for the WRRA sequential-output hypothesis.
