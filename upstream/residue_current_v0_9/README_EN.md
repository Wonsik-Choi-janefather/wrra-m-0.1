# WRRA_M upstream 0.9 — conditional residue preparation and same-state currents

Wonsik Choi · 2026-10-03 · ORCID 0009-0001-4263-9772 · CC BY 4.0

| Evaluation | Evidence |
|---|---|
| Verification inputs | Actual million-address branch vectors from 0.8/0.7 and frozen reviewed 0.6-r1 Hamiltonian/current code and calibration inputs. |
| WRRA-specific transformation | Prime SOURCE → relation amplitudes → phi residue → address selector → internal density state → electromagnetic/weak current readout. |
| Outputs | 183 implementation checks and 135 independent audits pass. SOURCE intensity changes propagate to internal populations and finite-Q² currents. |
| Falsification conditions | Failed positivity, trace/branch conservation, same-H excitation accounting, current trace agreement, CVC, deterministic reproduction or disagreement of an adopted physical map with observations. |

The declared preparation channel reads s_n=1 when v_3(n) is odd, otherwise zero. With t=Tr(S rho_phi), a=lambda*t, it prepares sigma=(1-a)|g><g|+a|e1><e1| using the frozen 95-dimensional internal basis. Lambda=0,0.2,1 are construction controls. The selector, lambda and mode index are disclosed constitutive inputs, not uniquely derived microscopic laws. For each address, Kraus maps sqrt(1-lambda*s_n)|g><n| and sqrt(lambda*s_n)|e1><n| give a trace-preserving channel. This measure/prepare map discards address coherence; phase-only changes are consequently invariant.

Only phi is prepared as a conditional nucleon test state. Its conditional trace is one, while f_phi*sigma retains trace f_phi in the original ledger. D and R retain their own stock. Proton and neutron are separately specified readout channels; the computation does not infer species abundance from address parity.

At lambda=0.2, baseline t=0.3998832725128899 and excited population=0.07997665450257799. The frozen excitation gap is 431.081244315 MeV and the conditional excess energy is 34.47643573911998 MeV. Changing SOURCE p3 log intensity from -0.15 to +0.15 changes the excess energy from 34.70641261829451 to 34.022215239851846 MeV. These are construction outputs, not measured cosmic energy densities or nucleon creation masses.

At Q²=0.1 GeV², baseline GE(proton)=0.7301767666507732 and GA=0.8971258414783907. Electromagnetic and weak currents use the same density state, frozen width/counterterm and 0.6 operators. Charge expectations are independently checked against full operator traces. CVC GE(V)=GE(p)-GE(n) and zero-momentum charges remain intact. Lambda=0 reproduces ground-state calibrations without refitting; nonzero lambda genuinely changes the readout.

The inherited neutron magnetic-radius mismatch (0.83198710743 versus 0.864 fm), finite-Q² empirical validation and regulator/precision exclusions remain open. Physical preparation origin, species selection, energy supply, seconds per frame and record-medium stability are not supplied by this conditional channel. The energy expectation is evaluated from the same H; dimensionless stock is not silently relabeled as conserved physical energy.

Run `python reproduce_all.py` with Python 3, NumPy 2.x and SciPy. The independent audit uses explicit Kraus/Choi matrices, random density states and trial integer factorization rather than the parent's sieve/valuation implementation. Upstream 0.10 integrates SOURCE/filter/record/preparation/current ledgers. Independent prediction and numerical novelty are not added completion requirements; calibrated reproduction and executed structural connections remain achievements. Infinity=Null remains the adopted premise.

Inherited reviewed 0.4–0.6 DOI: 10.5281/zenodo.23112253. No new 0.9 DOI has been issued.


## 2026-10-03 reviewed collection

This executable implementation is reviewed in [0.7-0.10-r1](../review_0_7_0_10_r1/README.md), DOI 10.5281/zenodo.23115550. Physical baseline outputs are preserved; input validation, clean reproduction and named/Q2-matched references are corrected. Historical PDFs remain available; consult the bilingual review report for the corrected implementation contract. Upstream development ends at 0.10.
