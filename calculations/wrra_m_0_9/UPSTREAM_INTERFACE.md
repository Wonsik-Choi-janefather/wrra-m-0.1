# WRRA upstream ledger interface version 1

Identifier: `wrra.upstream-ledger/1`. `parameters.json` is the single serialized input. This contract executes the declared arithmetic reference. Origins of the input state, spectrum, couplings and boundary remain upstream work.

| Field | Meaning and accepted range | Reference |
| --- | --- | --- |
| `upstream.address_cutoff_N` | Integer ≥4; addresses 2…N; arithmetic support, not physical volume or bits | 1,000,000 |
| `upstream.state` | `normalized_power_law`, finite alpha>1; w_n=n^-alpha / sum | alpha 1.8996876950554356 |
| `upstream.spectrum` | Adopted increasing positive gamma array; J≥1; finite equal-length coefficient/phase arrays | J=4, c_j=1/2, theta_j=0 |
| `upstream.update` | Integer K≥1, finite xi≥0, finite h, dimensionless order, identity resident boundary | K=8, xi=0.1, h=1.44767317035244 |
| `upstream.targets` | Nonnegative normalized phi/D/R reference for validation and explicit arithmetic refit | .05/.268/.682 |
| `upstream.scalar_comparison` | Constant odd-composite beta∈[0,1]; comparison only | .8654570124136961 |
| `channel_coupling` | Normalized 16-origin default kernel; optional odd-prime family kernels; normalized generation weights | 1/16 and 1/3 |
| `baseline_0_8` | Embedded validated 0.8 input including carrier state recipes, grid, filter and charge calibration | Carrier N=128 |
| `physical_bridge` | Structural phi→expressed, D→clustering, R→background response; SI maps absent | pending_0.10 |
| `provenance` | Source commit and SHA256 of five bundled upstream snapshots | 9ca21c547e5238be34ceace5a1015db50cb824ff |

Gamma heights and coefficients are dimensionless mathematical inputs. J_zero, N_address and the physical carrier lattice N are independent cutoffs. The lattice does not change when the address cutoff changes. No information-capacity value, energy unit, physical clock or length is inferred from these cutoffs.

`address_base(cfg, explicit_state)` accepts an optional normalized nonnegative diagonal state vector of length N−1 for computational probes. The serialized reference accepts the power-law state only. Full address coherences are not an implemented large-scale evolution input; a small coherent-state positivity check verifies the diagonal effects as a mathematical extension.

Sector effects after recovery are e_phi=1_odd T_n, e_D=1_even, e_R=1−e_phi−e_D. All effects are positive and sum to one. Address class assignment and post-recovery fold retention are constitutive rules. Initial transport includes the fourth field S, pending SOURCE. R=0 before k=K; S=0 from k=K. Identity resident updates are executed twice after the boundary to check retention.

`channel_join` routes w_n e_phi through normalized q_i(n), then the computed 0.8 permutation and normalized family state. The reference kernel is shared across addresses; overrides condition on an odd smallest prime. D and R remain separate sector budgets and are not assigned to Standard-Model particle channels. Arithmetic channel weights are neither measured occupations nor physical Born probabilities.

`calibrate(cfg, base)` is an explicit arithmetic refit operation for alpha and h. `run()` does not refit. Effective beta is derived for the frame profile. This is separate from the physical sequential calibration scheduled for 0.11. Negative weights, bad cutoffs, incompatible spectra, unnormalized kernels, physical records and nonnull SI maps are rejected.

Outputs contain the full input, its canonical SHA256, sector and conditional-scope rows, recovery frames, sample address effects, channel ledger, separate exponent comparisons and inherited 0.8 results. Reference snapshots are source provenance, not a physical observation record. Software logs are not called accumulated twist records.

In paper equation 12, the held condition S denotes the fixed address state, sector effects and coupling configuration for differentiation with volume. It is distinct from the pending SOURCE field S_k in equation 7. Equation 12 states a 0.10 interface requirement; neither an SI load nor its derivative is evaluated in 0.9.
