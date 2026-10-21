---
title: "WRRA: A finite SOURCE and common-carrier action"
subtitle: "Source-carrier action v0.1 · Continuous dynamics from registered material"
author: "Won sik Choi · Jeongin Choi | MCC / WRRA research record"
date: "2026-10-21"
---

# 1. Verified inputs: existing material first

**WRRA means Wonsik Reality–Renderer Architecture.** This calculation develops task 2, a finite dynamical and variational connection between SOURCE and the common carrier. Assessment follows verified inputs → WRRA transformation → outputs → falsification conditions.

We checked MCC 3.0 v0.27-r1: common-carrier definitions and the rank-one failure (Chapter 6), shutter/transport (112/117), and finite preparation with remaining dynamics (120). We read the original SOURCE-supplier-record exchange in `finite_frame_spatial_bridge_v0_29_1/frame_baseline/run.py` and common spectral transport in `source_shutter_bridge_v02/reproduce.py`. Original exchange permutation, initial/final probabilities and both SOURCE payload branches are frozen with hashes in this package.

| Layer | Existing result | Addition here |
|---|---|---|
| SOURCE/supplier | Resonant energy-preserving finite gate $G$ | Continuous generator reproducing that endpoint |
| Record | Separate degenerate record-bit ownership | Intermediate record probabilities and reversal control |
| Common carrier | $H_C=\hbar c|k|$ and $I_{15}$ | Joint execution within one action |
| Spatial profile | Positive residue kernel and actual payloads | Explicit rate-coupling candidate using that profile |
| Resources | Before/after SOURCE+supplier account | Intermediate account and full interaction-energy audit |

SOURCE address labels (1,015,000), timeless prephenotypic allocation slots (128) and quantum mode labels (128) remain distinct. The mode register here is the one used by the registered finite exchange; no time or flow is assigned to allocation slots. A two-state supplier and a separate two-state record give a 512-state exchange register. Neither SOURCE nor the common carrier is introduced as an extra particle or fifth force.

# 2. WRRA transformation: gate to minimum generator

The existing mode cost is $A_k=1-\cos(2\pi k/128)$. The registered exchange swaps

$$
|a\rangle=|8,1,0\rangle,\quad |b\rangle=|72,0,1\rangle,\quad
\Delta A=A_{72}-A_8=2\cos(\pi/8).
$$

Matching the supplier gap to $\Delta A$ gives equal resource energy $E_a=E_b$ in $H_0$. The gate exchanges these states and leaves all other basis states unchanged: $G^2=I$, $G^\dagger=G$ and $[G,H_0]=0$.

A continuous generator over prescribed interval $\tau$ is

$$
P_-=(I-G)/2,\qquad H_G=\frac{\pi\hbar}{\tau}P_-,\qquad
 e^{-iH_G\tau/\hbar}=G.
$$

**Specified minimality:** restrict to nonnegative, time-independent Hermitian generators, an exact endpoint $G$, and fixed energy-origin/gate-phase conventions. The $+1$ eigenspace requires phase $0\bmod2\pi$ and the $-1$ eigenspace $\pi\bmod2\pi$. Minimizing the squared generator norm among nonnegative logarithm branches selects 0 and $\pi$. This yields the minimum generator in that class. Without the nonnegative restriction, $-\pi$ has equal squared cost, so unconditional uniqueness is not asserted. This quadratic cost is an adopted generator-cost measure, not a proof of the universe's total computational cost.

On the active pair, $H_G=(\pi\hbar/2\tau)(I-X)$ and

$$
P_{a\to b}(t)=\sin^2\!\left(\frac{\pi t}{2\tau}\right).
$$

It reproduces the old exchange at $\tau$ and reverses at $2\tau$ if left on. Continuous interaction therefore does not constitute irreversible recording or automatic reset. Permission, termination and reusable resources for one accepted event retain separate ownership.

# 3. One action and the common carrier

For a normalized finite state $\Psi$, adopt the conditional action

$$
S=\int dt\left[\frac{i\hbar}{2}(\Psi^\dagger\dot\Psi-\dot\Psi^\dagger\Psi)
-\Psi^\dagger H\Psi+\lambda(t)(\Psi^\dagger\Psi-1)\right].
$$

Variation gives $i\hbar\dot\Psi=(H-\lambda I)\Psi$; fix the global-phase gauge with $\lambda=0$. The same spatial operator acts on all fifteen internal channel labels:

$$
H=H_0+H_C\otimes I_{512}\otimes I_{15}
+\frac{\pi\hbar}{\tau}w(x)\otimes P_-\otimes I_{15},\qquad
H_C=\hbar c|k|.
$$

Stationarity yields evolution for the declared $H$. It does not by itself select the Hamiltonian, initial state, SOURCE cardinality or supplier prior. Global phase symmetry conserves norm; time independence conserves total $\langle H\rangle$. The common $I_{15}$ structure preserves channel ownership. This does not derive all Standard-Model gauge interactions or generations.

**New explicit coupling candidate:** use the existing positive SOURCE profile to define

$$
w(x)=I_{\rm SOURCE}(x)/\langle I_{\rm SOURCE}\rangle
$$

and multiply the resonant exchange rate by it. Once fixed, the internal state equation determines evolution. This spatial law is an additional candidate assumption, not uniquely forced by minimality, and does not identify information with mass density. Uniform $w=1$ exactly recovers the old gate endpoint. Nonuniform $w$ has $[H_C,w]\ne0$, producing genuine SOURCE/carrier coupling in the execution.

# 4. Executed geometry, state and complete account

Retain the original adopted profile period $L=1024c\tau$. In coordinates $x/L$ and time $s=t/\tau$, the carrier coefficient is $c\tau/L=1/1024$. Resolutions $N=64,128,256$ represent this same period. This new coupling runs on the one-dimensional periodic profile with fifteen internal channels; it is not presented as a newly executed fully three-dimensional interaction. Spatial nonlocality of spectral transport is retained.

Initial spatial amplitude is uniform, the supplier has the existing uniform-g-parity excitation probability $p=1/2$, and the record is blank. Both original payload branches reconstruct their own $w$. The minimum-generator endpoint separately reproduces both the original uniform and Gibbs supplier preparations. The spatial-coupling test uses $p=1/2$.

Projector decomposition gives $K_+=K_C$ and $K_-=K_C+\pi w$. After evolving $\psi_+$ and $\psi_-$, pair amplitudes are $(\psi_++\psi_-)/2$ and $(\psi_+-\psi_-)/2$. Record probability is $P_b=p\|\psi_b\|^2$ and remaining supplier excitation is $P_a=p-P_b$.

At each time, the SOURCE increase $+\eta_s\Delta A M_sP_b$ cancels the supplier decrease $-\eta_s\Delta A M_sP_b$. Here $M_s$ is the retained payload sum on controlled $r\bmod3\ne0$ addresses; the P sector is uncontrolled. Existing resource and pressure ownership are retained.

**Interaction energy is included.** We track $\langle H_C+H_{\rm int}\rangle$, not carrier kinetic energy alone. Including the separately conserved $H_0$ yields the conserved full generator energy. If $\tau=1.4813019664\times10^{-21}$ s and physical $\hbar$ are used, the conditional pair coefficient is $g=\pi\hbar/(2\tau)\simeq0.6979785$ MeV. This is not a detected particle energy. In the nonnegative-generator convention, the initial interaction expectation for $p=1/2$ and mean $w=1$ is $pg\simeq5.59142\times10^{-14}$ J. Physical implementation, volume dependence and metric variation of this term require their own ownership map. It is neither silently added to the existing 5/26.8/68.2 cosmological account nor omitted as free control.

# 5. Outputs and independent verification

| Result at $t=\tau$ | Uniform | SOURCE weighted | SOURCE unweighted |
|---|---:|---:|---:|
| Record probability $P_b$ | 0.5000000000 | 0.3498817302 | 0.3486031973 |
| Reduced active-pair purity | 1 | 0.5835688259 | 0.5817213788 |

Purity is for the exchange pair after tracing spatial modes within the supplier-excited branch, not the full mixed-state purity or a single-outcome collapse probability. Its reduction diagnoses entanglement in this candidate, not an observed cosmic signal. Maximum drift of the complete dimensionless kinetic-plus-interaction energy is below approximately $10^{-15}$; resource-account relative error is also below approximately $10^{-15}$.

Weighted record probability is 0.3498817301578032 at $N=64$, 0.3498817301555508 at 128 and 0.3498817301555505 at 256. The final two differ by approximately $3.3\times10^{-16}$. This finite numerical stability does not derive the physical period from first principles.

All **218/218 internal checks** pass. These include repeated invariants at sampled times and are not 218 independent physical experiments. Independent `verify.py` integrates the full two-component equation directly by RK4 at $N=64$ and compares with the projector-reduced eigenmode solution:

| Time steps | State $L^2$ discrepancy |
|---:|---:|
| 1024 | $1.12306\times10^{-11}$ |
| 2048 | $7.02106\times10^{-13}$ |
| 4096 | $4.42245\times10^{-14}$ |

Separate full $2N\times2N$ block diagonalization agrees within $3.755\times10^{-15}$. The independently differenced action-equation residual is approximately $6.05\times10^{-12}$. These are internal independent numerical checks, not external peer review or observational confirmation.

Negative controls omit the coupling energy, detune the supplier gap by 0.01, and replace the fifteen-channel identity by democratic rank-one coupling. They respectively reveal energy-account failure, loss of resource conservation and channel rank one. Uniform evolution reversing at $2\tau$ also detects a false irreversible-reset interpretation.

# 6. Falsification and conclusion

Revise the implementation if frozen input hashes or endpoint replay disagree; action equations and evolution conflict; probabilities, SOURCE+supplier resources or full energy including interaction drift; channel ownership is lost; or results fail resolution stability. Observational use must retain fixed coupling, preparation and units rather than change them after inspecting the outcome.

**Conclusion:** a minimum nonnegative generator reproduces the registered finite exchange and joins the common carrier in one conditional action. A nonuniform coupling candidate using the actual SOURCE profile is executed and independently verified. SOURCE/carrier dynamics have therefore advanced from an architectural declaration to a finite dynamical candidate. SOURCE cardinality and preparation origin, autonomous one-shot permission/termination and reusable costs, metric stress of the new generator, and complete Standard-Model interactions remain separate tasks.

# 7. Sources and reproduction

MCC 3.0 v0.27-r1: DOI **10.5281/zenodo.23516661**. Existing finite-frame spatial bridge: DOI **10.5281/zenodo.23329214**. Repository: <https://github.com/Wonsik-Choi-janefather/wrra-m-0.1>.

This is a new computation record, separate from those registered editions, with no new DOI or public release assigned. The book and previous cosmological outputs are not overwritten. With Python 3 and NumPy, run `python3 compute.py` then `python3 verify.py` from the package directory. Frozen inputs, original code, hashes, full CSV/JSON results and bilingual reports are included.
