# WRRA M Upstream 0.7 to 0.10
## Reviewed collection - 0.7-0.10-r1
Wonsik Choi | ORCID 0009-0001-4263-9772 | 2026-10-03
DOI: 10.5281/zenodo.23115550 (registered on publication)

This edition reviews and corrects the finite implementation from SOURCE preparation through conditional particle currents. Upstream development ends at 0.10. A later 1.0 may consolidate and freeze the work; it does not imply new upstream development stages. The review preserves the disclosed numerical calibration and all baseline physical outputs.

## Verified inputs before conclusions
The finite SOURCE contains addresses n = 2,...,N with N = 1,000,000. The frozen parameters are alpha = 1.8996876950554356 and beta = 0.8654570124136961. The normalized amplitude is proportional to n^(-alpha/2) times exp[(epsilon_p/2 + i phase_p) v_p(n)] for the disclosed prime controls. Prime addresses are the SOURCE labels; composite indices organize finite descendants and filter outcomes. No realized infinite address space is required. Infinity = Null is the adopted frame; mathematical limiting expressions are not claims of physically realized infinity.

The 0.9/0.10 internal test uses the corrected, frozen 0.6 Hamiltonian and currents in a 95-dimensional basis. Its selector is odd v_3(n), the preparation strength is 0.2, the excited mode is 1, and the ensemble momentum grid is Q2 = 0, 0.01, 0.1 GeV2. These choices are construction inputs. Proton and neutron labels are supplied externally. The review does not add a species-selection law or an energy origin.

## 0.7 - SOURCE and finite filter ledger
WRRA transformation: even composites enter D; odd composites have phenotype weight beta and initial-reflection weight 1-beta; primes return through the normal-return channel. Each finite address contributes once to the normalized ledger. The four-outcome instrument conserves the input norm. Aggregating the two return outcomes gives the three-entry ledger.

| Output on the common SOURCE denominator | Baseline |
| --- | --- |
| Phenotype | 0.050000000000000 |
| D | 0.267999999999998 |
| Return | 0.682000000000002 |
| Actual = phenotype + D | 0.317999999999998 |

A single full release followed by closed events gives this reference split. Releasing 0.2 of available SOURCE for 32 events with no leakage gives Actual stock 0.8778861396212083. The reference 0.318 is a single-window result, not the recycling fixed point. The previously calibrated reproduction is a valid model accomplishment; independent new numerical predictions are not prerequisites for evaluating the declared construction.

Correction: the 0.7 reproduction runner now works when saved result files are absent. It regenerates the outputs twice, checks deterministic bytes, and still protects any existing partial references. Falsification conditions: branch totals fail normalization, an address is double counted, the independent scalar audit disagrees, or a claimed clean reproduction changes bytes under the pinned environment.

[[PAGEBREAK]]
## 0.8 - finite shutter and one record
WRRA transformation: the coarse three-label shutter is S_eta(rho) = (1-eta) rho + eta diag(rho), with 0 <= eta <= 1. The microscopic instrument instead retains four named branch vectors K_j psi. A supplied draw in [0,1) selects one positive-probability branch and returns its label and normalized conditional address vector. The two return vectors remain distinct until classical aggregation; their mixture is not asserted to be a pure state.

| Microscopic branch probability | Baseline |
| --- | --- |
| phi | 0.050000000000000 |
| D | 0.267999999999998 |
| Initial reflection | 0.00777294456318944 |
| Normal return | 0.674227055436812 |

The full coarse shutter gives purity 0.539448 and leaves all three branch probabilities unchanged. Coherent rotation and shutter order produce different phenotype readouts: approximately 0.00784598233 versus 0.06334350075. This is a finite order contrast in the declared coarse interface, not a reconstructed microscopic phase experiment.

Corrections: Hermiticity is checked with absolute tolerance 1e-12 and zero relative tolerance. Boolean shutter strengths and draws are rejected. Selection excludes zero-probability branches, including endpoint-rounding cases. Microscopic records require the four canonical branch names, aligned nonempty finite vectors, and normalized total branch norm; dictionary insertion order no longer changes the instrument order.

Falsification conditions: trace or positivity fails, the shutter changes diagonal probabilities, the microscopic norms disagree with 0.7, a zero-probability branch is selected, or malformed/nonfinite branch vectors yield a record. One supplied draw is one conditional record. The four test draws are not cosmic abundances or a sampled trajectory of stock depletion. A clock, minimal physical time, and a stable record medium remain unspecified.

## 0.9 - conditional residue and frozen currents
WRRA transformation: dephase the address label and let t be the conditional phi weight on odd v_3(n). Preparing those labels with strength s gives w = s t and rho_phi = (1-w)|g><g| + w|e1><e1|. The normalized conditional density has trace 1; its unnormalized version has trace f_phi. D and return are outside this nucleon test preparation.

The same frozen H evaluates E_excess = Tr(rho_phi H) - E_ground = w times the gap. The same-state current is the corresponding linear mixture of ground and excited-mode readouts, with the frozen charge width and counterterm. This executes the declared finite preparation map without refitting its excited-state outputs.

Corrections: conditional vectors must align with strictly increasing integer addresses and be finite; the selector must be prime. Internal modes must be finite, normalized, aligned, and orthogonal. Empty/duplicate scans and ambiguous SOURCE case names are rejected. The displayed reference is found by its baseline name and reference strength. The inherited current adapter is explicitly restricted to real frozen modes and rejects complex states; no general complex-current implementation is claimed.

[[PAGEBREAK]]
## Numerical outputs and their scope
| 0.9/0.10 baseline output | Value |
| --- | --- |
| Conditional selector t | 0.3998832725128899 |
| Excited population w | 0.07997665450257799 |
| Frozen excitation gap | 431.081244315 MeV |
| Conditional excess energy | 34.47643573911998 MeV |
| Proton GE at Q2 = 0.1 GeV2 | 0.7301767666507732 |
| Weak GAV at Q2 = 0.1 GeV2 | 0.8971258414783907 |

SOURCE intensity changes affect the conditional preparation: epsilon_3 = -0.15 gives w = 0.08051014298579888 and excess energy 34.70641261829451 MeV; epsilon_3 = +0.15 gives w = 0.07892297725436004 and 34.022215239851846 MeV. A phase-only control leaves this dephased preparation unchanged. Zero strength reproduces the frozen 0.6 ground-state calibration.

Falsification conditions: Kraus completeness/positivity fails, the conditional trace is not 1, scalar factorization disagrees with t, phase-only control changes the disclosed dephased output, energy disagrees with the same Hamiltonian, or charge-operator trace and current readout disagree. These are mathematical and implementation tests; they are not independent experimental confirmations.

## 0.10 - integrated closure
WRRA transformation: execute SOURCE -> ordered filters -> one record -> phi-only conditional preparation -> frozen same-state currents, alongside separately typed scalar stock protocols. Six SOURCE cases are computed. A selected phi record is prepared from its actual conditional address vector. Other branch records have no nucleon internal readout. Ensemble probabilities, records, information stocks, and MeV outputs retain distinct meanings.

Corrections: the baseline handoff is selected by the named uncontrolled baseline rather than list position. Stage-0.9 regression matches curves by Q2 value, and shared named cases must retain the same SOURCE controls. Record readout momentum is now the explicit input record_readout_Q2_GeV2 = 0.1; each readout reports Q2_GeV2 and currents. The old key current_at_Q2_0_1 is replaced. Protocol names must be unique, releases/leakage must be finite valid fractions, and the reference must be one full release followed by closed events with no leakage. The unused vectors_hash variable was removed.

Falsification conditions: rearranging case or momentum lists changes matched outputs or the baseline handoff; a shared case silently changes its controls; unsupported maps become non-null; or stock conservation/positivity fails. The review tests reversed lists and a 0.01 GeV2 record probe in an isolated copy.

Closure: the upstream conditional integration is complete at 0.10. Physical timing, SOURCE energy supply, information-to-energy conversion, species origin, and record-medium stability remain explicit null interfaces. The inherited neutron magnetic radius is approximately 0.83198710743 fm against the retained 0.864 fm reference, a difference of about 0.03201289257 fm. Existing finite-Q2 diagnostic discrepancies remain on the inherited ledger. This review does not erase them or claim their resolution.

[[PAGEBREAK]]
## Reproduction, preservation and assessment
Run from the repository root:
python upstream/review_0_7_0_10_r1/reproduce_all.py

The runner pins OPENBLAS_NUM_THREADS and OMP_NUM_THREADS to 2, recomputes all four stages in order, runs each independent audit, then executes verify_review.py. Dependencies are Python 3, NumPy and SciPy; the release environment records exact installed versions. PDFs are supplementary reports; JSON files and the supplied code are the executable evidence.

| Verification group | Count passed |
| --- | --- |
| 0.7 computation + independent audit | 113 |
| 0.8 microscopic + randomized shutter audit | 431 |
| 0.9 implementation + independent audit | 318 |
| 0.10 integration + independent scalar audit | 465 |
| New cross-stage review tests | 68 |
| Total counted checks | 1395 |

The count includes inherited checks, mathematical channel checks, regression checks, and malformed-input tests. It is not a count of independent physical discoveries. Additional assertions in the 0.8 computation are not included in the 431 counted checks. All 0.9 numerical rows remain exactly unchanged; all six 0.10 physical rows remain unchanged after the disclosed record-schema normalization. The 0.7 results and coarse 0.8 results remain byte-identical. Parent hashes and the 0.10 explicit input/schema necessarily change.

The baseline/ folder preserves the pre-review Python, JSON and Markdown files; baseline_sha256.json verifies them. Current stage folders hold the reviewed executable implementation. Original stage PDFs remain historical reports; this bilingual reviewed report supplies the corrections and supersedes their implementation descriptions where changed. The archive includes the necessary frozen 0.6 dependency, four stage sources/results/audits, historical reports, review tests and this report. A SHA-256 manifest covers archive contents.

Evaluation order is verified input -> WRRA transformation -> computed output -> falsification condition -> conclusion. Known-value calibration/reproduction is retained as an achieved result. Separate conditional integrations are credited only where actually calculated. No conversion from information fractions to physical energy, no physical clock, and no species-origin law is inferred from these finite computations.

Repository: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1
Zenodo: https://zenodo.org/records/23115550
Related upstream 0.4-0.6 reviewed collection: 10.5281/zenodo.23112253.
