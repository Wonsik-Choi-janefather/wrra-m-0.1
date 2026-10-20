#### 135.17 A Reverse-Engineered Interpreter of Observed Structure: Executed Example

**Verified inputs.** Use arithmetic code $n=9$, singly even parent $r=18$, conjugate orientation $\chi=\pm1$ and declared momentum, permission and source states. Freeze the NIST 2022 CODATA mass energies $m_ec^2=0.51099895069$ MeV and $m_\mu c^2=105.6583755$ MeV [S6]. Their listed standard uncertainties are $0.00000000016$ MeV and $0.0000023$ MeV. Spin magnitude $1/2$ and opposite conjugate charges/lepton numbers are also declared physical inputs. The execution uses central values; it does not newly fit constants or propagate their uncertainties.

**WRRA-specific transformation.** Distinguish interpreter configurations $\theta_e$ and $\theta_\mu$. Code 9 is not asserted to uniquely name both species simultaneously: the interpreter configuration is part of the full input.

| Interpreter | Same code and conjugate orientation | Implemented states | Mass energy per particle |
|---|---|---|---:|
| $\theta_e$ | $(9,+1),(9,-1)$ | Electron $e^-$, positron $e^+$ | $0.51099895069$ MeV |
| $\theta_\mu$ | $(9,+1),(9,-1)$ | Muon $\mu^-$, antimuon $\mu^+$ | $105.6583755$ MeV |

Within each profile, read $q(\chi)=-\chi e$, lepton number $L(\chi)=\chi$ and spin magnitude $s=1/2$. Here $\chi=+1$ denotes the example's matter orientation; it does not say that all matter is negatively charged. Adopt the relativistic momentum readout

$$E=\sqrt{m_\theta^2c^4+c^2|\mathbf p|^2}.$$

Mass and species are disclosed readout inputs, not newly derived from prime factors alone. The implemented contribution connects arithmetic code, conjugate orientation, output reservation, physical state and energy ownership in one execution path.

Decomposition renders the state selected by the current phase first, then its conjugate at the next shutter opportunity. The intermediate source owns the pending partner's charge, energy and momentum. Recombination admits opposite conjugates with the same profile and code and requires an explicitly admitted joint interaction event. Arithmetic addition or the earlier emission delay alone does not establish recontact or annihilation.

The combined intermediate state owns parent $r=18$, the two declared state records and their total four-momentum. On transfer to a selected two-photon carrier channel, its active four-momentum ownership is set to zero and assigned to the outgoing photons. The parent and history remain records; energy is not counted twice. The declared classical record can be inversely read, but this does not prove recovery of all quantum amplitudes or entanglement. Atomic structure, scattering/decay dynamics and spin/polarization amplitudes remain extensions of this finite implementation.

**Outputs.** The same $9+9$ has rest-energy sums $1.02199790138$ MeV and $211.316751$ MeV in the two fixed interpreters. These are implementations of observed inputs. The audit executes 288 cases: two profiles, six momentum/mass ratios, three axes, two first-output orientations and four boosts. Six negative controls reject an unregistered interpreter, an unregistered code, invalid orientation, same-sector recombination, mixed-profile recombination and a missing interaction permission.

| Executed check | Maximum normalized error |
|---|---:|
| Massive-state mass shells | $5.634\times10^{-14}$ |
| Two-stage source/output four-momentum | $8.608\times10^{-16}$ |
| Photon null condition | $6.820\times10^{-16}$ |
| Aggregate-to-carrier four-momentum transfer | $1.717\times10^{-15}$ |

These are finite-interpreter and ownership-transfer checks, not the previous 630-case audit or 288 independent observations. The shutter delay is the adopted earlier value and is not physically validated anew. Reproduction files are `renderer_r4/reverse_interpreter.py`, its input table and `reverse_interpreter_results.json`.

**Falsification conditions and assessment.** Revise the implementation if it fails to reproduce its input constants/conjugate properties, reads identical full inputs inconsistently within a frozen profile, loses or duplicates conserved quantities, or admits undeclared states. Claiming complete derivation of masses, charges, spins or reaction rates would exceed its scope. Uniquely necessary selection of this interpreter is not a failure criterion. Reassess the earlier “arithmetic-to-physical structure not derived” item as **implementation scope, reproducibility and cross-consistency of a reverse-engineered interpreter**. This reinforcement supplies an executed finite state readout and energy ledger; full interactions remain a separately tracked implementation task.

[S6] NIST, [2022 CODATA Fundamental Physical Constants: complete listing](https://physics.nist.gov/cuu/Constants/Table/allascii.txt). Source of electron/muon mass energies and standard uncertainties, not evidence that WRRA newly predicted those constants.
