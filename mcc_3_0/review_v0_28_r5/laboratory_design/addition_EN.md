
### 122.1 Experimental specification: visibility under differential phase coupling

**Verification inputs.** Retain frozen optical model v1.0: the 128 values $f_D(J)$, $g=1$, preparation $I/128$, and one unchanged label during each photon's propagation. No new fit to optical data is performed. The following numbers are calculated design requirements, not experimental measurements. A frequency comb supplies optical-frequency calibration through $\nu_n=n f_{rep}+f_{CEO}$ [E1]. Frequency-comparison precision is not interpreted as shutter-time resolution.

**WRRA-specific transformation.** The existing $H_{int}$ maps the finite SOURCE mean-stress distribution into differential path phases, whose nonselective sum gives $v=V/V_0$. An apparatus must first calibrate its effective exposure $L$ and path-specific couplings. Neither apparatus length nor ordinary optical path difference $D$ automatically equals $L$. A physical procedure establishing natural SOURCE differential coupling in such an apparatus has not yet been fixed. A null result without that preparation does not test the conditional curve. Once the connection is established, freeze preparation, coupling, and memory rules and perform the numerical comparison below.

**Outputs: preregistered measurement range.** Recalculate the threshold, minimum, and revival for 532, 1064, and 1550 nm. At 1064 nm scan effective exposure $L$ from zero to $40\,\mathrm m$, with primary points at 13.578784206 m, 21.780958380 m, and 37.278764320 m. Matching $L/\lambda$ gives maximum effective exposures of 20 m and approximately 58.271 m at the other wavelengths. Preregister three primary points per wavelength, nine in total. Additional scan points are diagnostic and do not retrospectively enlarge the primary test. Minimum and revival normalized visibilities are 0.3586975046 and 0.6081539566.

The following are selected design targets, not measured apparatus specifications or achieved performance.

| Item | Target and assumptions |
|---|---|
| Normalized visibility | Absolute standard uncertainty 0.01 per point; shared-reference correlations included |
| Counting statistics | At least 98,766 independent detected trials in each signal and reference block gives ideal first-order propagated statistical error bound 0.005 if $V_0\ge0.9$ |
| Effective exposure calibration | Sufficient bounds for visibility error 0.002: 15.93/31.86/46.41 mm at 532/1064/1550 nm |
| Residual phase noise | Independent zero-mean Gaussian RMS at most 0.06328 rad for fractional visibility loss at most 0.002 |
| Optical frequency and path stability | At $D=40$ m and 1064 nm, assigning half the phase variance to each independent contribution gives RMS limits about 53.37 kHz and 7.577 nm |

The counting bound assumes ideal Bernoulli trials split equally between two fringe-extremum phases established by separate calibration. With $N_b$ total trials in each of the signal and reference blocks, use the first-order propagated bound $\sigma_v\le\sqrt{2/(V_0^2N_b)}$. This excludes retrospective selection of extrema, phase-estimation uncertainty, detector nonlinearity, dark counts, and losses; include them in actual analysis. No measurement duration follows without detection and independent-preparation rates.

The exposure requirement uses the global bound calculated from the actual finite profile,

$$|v(L+\delta L,\lambda)-v(L,\lambda)|\le\frac{2\pi}{\lambda}\langle|f_D|\rangle|\delta L|.$$

Propagate uncertainty in $g$ and preparation separately. For ordinary optical frequency and path noise, the design uses $\sigma_\phi^2=(2\pi D\sigma_\nu/c)^2+(2\pi\sigma_D/\lambda)^2$. This is an example of uncorrelated quasistatic noise over the exposure; replace it with integrated measured noise spectra and servo transfer functions where appropriate. These optical-noise limits are distinct from SOURCE effective-exposure uncertainty. Recheck the overall 0.01 budget by combining all terms and their covariance. High frequency accuracy alone does not establish the complete uncertainty budget [E2].

**Falsification conditions.** Randomize wavelength and exposure order. Record balanced common-coupling controls, exchanged coupling paths, single-label conditional visibility, and independent source/detector reference measurements. Balanced common coupling and a single conditioned label predict normalized visibility one. Record vibration, temperature, polarization, mode overlap, and shared-reference errors; additional loss alone is not a WRRA signal. For nine points with established physical preparation, use residuals $r=y-v_{WRRA}$ and measurement covariance $C$:

$$Q=r^{\mathsf T}C^{-1}r.$$

Under a Gaussian approximation with known covariance, no posterior fitting, and nine degrees of freedom, the preregistered rule rejects this frozen branch at significance 0.001 if $Q>27.8771648713$. If covariance is estimated from small samples or nuisance parameters are fitted jointly, calibrate the distribution by simulation of the actual procedure instead of retaining this threshold unchanged. Non-rejection is neither proof nor a signal discovery. Observation-driven model revision remains legitimate; record changed inputs, freedoms, and outputs in a new version. Apply the same standard to comparator models.

**Conclusion and execution scope.** All 29 original file hashes were checked before rerunning the optical model's 17+11 controls. Appendix H.7 records additional design and verifier tests. This section connects an actually computed WRRA curve to ranges, errors, and rejection rules. Establishing natural differential coupling and collecting measurements remain outstanding. Encoding the prescribed phases with an optical phase modulator or a seven-qubit label register and a path qubit would test a separate emulator implementation; success alone would not establish natural SOURCE coupling.

The reciprocal shutter interval is approximately $6.7508180\times10^{20}\,\mathrm{Hz}$, but this calculation predicts no detection line or frequency-comb signal there. Since $N\ell_{sh}=L$, shutter spacing cancels from the static phase law. This experiment cannot estimate the shutter interval itself. Do not assign a separate numerical laboratory resolution to twist stress before computing a transfer function to an actual laboratory frequency shift, force, or phase. This additional connection is distinct from the existing macroscopic response achievements.

[E1] NIST, *Femtosecond-Laser Frequency Combs for Optical Clocks*, https://www.nist.gov/programs-projects/femtosecond-laser-frequency-combs-optical-clocks (accessed 2026-10-22).

[E2] NIST, *Advancing Statistical Methods for Next-Generation Clock Networks*, https://www.nist.gov/programs-projects/advancing-statistical-methods-next-generation-clock-networks (accessed 2026-10-22). These sources support general metrology and uncertainty treatment; they are not WRRA validation evidence.

## H.7 v0.28-r3: experimental design and synthetic-data verification

Read Section 122.1 as verification inputs → WRRA-specific transformation → outputs → falsification conditions → conclusion. The source is optical_model_v1_0 in the preserved package for DOI 10.5281/zenodo.23380920. Input profile SHA-256: `8c53fb73b332db2805b7d614f166511094b54b3f1b2a291fbfdfe46312408d6b`. This revision executed 29 source-file hash checks, 17+11 inherited computational controls, and 22/22 new design checks. All data below are synthetic; these are not observational verdicts.

| Case | Q / error | Exit |
|---|---|---:|
| synthetic_nominal | 6.59879688770414 | 0 |
| synthetic_no_loss | 7177.529448321479 | 1 |
| synthetic_missing_revival | 2105.0240834042634 | 1 |
| hash_change | SOURCE_PROFILE_HASH_MISMATCH | 2 |
| order_change | POINT_ORDER_MISMATCH | 2 |
| covariance_invalid | Matrix is not positive definite | 2 |

Exit 0 means not rejected under the stated statistical conditions, 1 rejects the frozen branch, and 2 identifies invalid input. Malformed cases were tested in isolated copies. `design.py` produces the design and synthetic data; `verify_observations.py` recomputes predictions from the actual source profile and tests the recorded covariance; `test_design.py` executes nominal, no-signal, missing-revival, and malformed-input cases. The package retains logs and original code. This validates an analysis procedure, not an experimentally confirmed or wholly executed universe model.
