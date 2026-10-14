MCC 3.0: Light–Shutter Shared-Carrier Space/Time Bridge v0.1
Research context: Wonsik Choi and Jeongin Choi. 2026-10-14.
Run: python reproduce.py (numpy, matplotlib). No online data required.

Validation input
Known c and SI h/eV conversion; the current book's mode scale 22217.345682174 eV
and conditional phase resolution epsilon=.05. These set dt=epsilon*hbar/E*.
The book distinguishes abstract carrier channels, internal compact coordinates,
and slots from externally measured positions. An arithmetic-address-to-metre
mapping was not specified in the reviewed definitions.

Architectural transformation
This audit constructs and EXECUTES a conditional external-space renderer:
dx=c*dt, one massless shift per shutter, U_shift tensor I_15 on a finite 512-cell
ring and 15 internal channels. It does not identify SOURCE addresses with sites.
The ring is a computational boundary, not an inferred universe size or topology.

Output
dt=1.481301966415863e-21 s; dx=0.444083157552045 pm.
After 64 common shifts, norm, channel weights and the adopted spectral energy
are conserved to floating precision. Packet velocity matches c to about 6.24e-14
relative error. Five admitted spectral modes also obey omega/k=c.
This is an executed structural consistency check; c is an input, not a prediction.

Existing hydrogen phase periods, a neutrino survival minimum, muon lifetime and
tau total/partial-rate times are re-expressed as integer shutter counts using
70-digit Decimal arithmetic. Nearest-tick rounding remains within dt/2. Different
time observables retain their meanings. c*T is a light-path equivalent and is not
the distance travelled by the massive particle. Two-photon transition frequency
is distinct from the frequency of each excitation photon.
Previous model residuals remain unchanged, including the hydrogen holdout failure.

A fixed direct-phase sampling interval has a Nyquist energy near 1.395957 MeV.
This is a numerical alias boundary, not a physical maximum photon energy.
Higher-energy cases are rejected on the base interval and reconstructed after
matched temporal/spatial refinement. Maintaining the anchor's epsilon phase
accuracy can require additional refinement; both criteria are recorded separately.

Falsification
Nonconservation, channel-dependent speeds, unrejected phase aliases, failure of
matched refinement, or inconsistency with a subsequently supplied SOURCE metric
falsifies the relevant bridge rule. The current scope is a free 1D massless branch;
Maxwell polarization/gauge dynamics, interactions, 3D isotropy, gravity and a
Lorentz-covariant microscopic completion are not tested. The local observer's
time is used, not photon proper time or absolute global simultaneity.

Conclusion
The operational light/shutter bridge is implemented and internally consistent.
Its spatial interval is a declared renderer output, not independently recovered
from the arithmetic SOURCE. That source-to-metric mapping remains open.
c fixes a length/time ratio; the mode-energy and phase-resolution anchor selects
the present conditional dt. A unique universal shutter is not established.

Exact input provenance and inherited result status: frozen_inputs.json.
Code, CSV ledgers, JSON, plot and file hashes are included.
