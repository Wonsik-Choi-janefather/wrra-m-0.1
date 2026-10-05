# A Single Measurement in the WRRA M Integrated Model
## From address preparation to a finite record and homogeneous energy response

Wonsik Choi and Jeongin Choi

Corresponding author Wonsik Choi · Independent researcher Seoul Republic of Korea  
janefather@gmail.com · ORCID 0009-0001-4263-9772

Review case 1.0 · 5 October 2026  
Companion to the integrated manuscript DOI 10.5281/zenodo.23126800 [1]

# 1 Purpose and assessment

We give reviewers one executable case in the completed WRRA M integrated model. A finite address distribution prepares a proton internal state. An ideal write transfers its state and record costs to the same energy ledger used for homogeneous response.

**Verified inputs.** We retain the published address, internal Hamiltonian, constants and inherited energy calibration. The preparation strength, measurement basis, record gap, supply boundary and clock mapping are declared choices.

**WRRA transformation.** Address conditioning fixes an excited population. Its energy replaces the reference phenotype allocation. A supplier pays one write; the adopted volume law then gives pressure and deceleration from that energy.

**Outputs and falsifiers.** Baseline excitation is 34.4764357391 MeV. The mean supplier transfers 7.0378712840 × 10⁻¹² J and retains a positive balance. A failed state normalization, unmatched energy transfer, pressure derivative or proper-time transition rejects the corresponding connection.

Table 1 Fixed case inputs and declared roles

| Input | Value and role |
|---|---|
| Address support | $2\leq n\leq10^6$; finite source labels |
| Address parameters | $\alpha=1.8996876950554356$, $\beta=0.8654570124136961$ |
| Internal support | Two inherited modes within the symmetric 95D space |
| Preparation | $a_p=0.2$, selector prime 3, first excited mode |
| Energy fractions | $f_\phi=0.0493$, $f_D=0.265$, $f_R=0.6857$ |
| Reference density and volume | $u_0=7.6689477678\times10^{-10}\ \mathrm{J\,m^{-3}}$, $V_0=1\ \mathrm{m^3}$ |

We distinguish the individual write and controller from the expected-occupancy ledger. $D$ is the nonphenotypic resident sector. Prime-parts assembly rules are not used.

CASEPAGEBREAK

# 2 Address conditioning and reference energy

Within the admitted phenotype branch, normalize the address weights as $w_n=|\phi_n|^2/\sum_m|\phi_m|^2$. Let $\nu_3(n)$ count the factors of 3 in address $n$, and let $\chi_n=1$ when that count is odd. The original address computation yields

$$t_3=\sum_n w_n\chi_n=0.3998832725128894,\qquad p_e=a_pt_3=0.07997665450257789.$$

The two selected modes $|g\rangle$ and $|e\rangle$ belong to the same inherited Hamiltonian $H$. We prepare the address-dephased internal mixture

$$\rho_0=(1-p_e)|g\rangle\langle g|+p_e|e\rangle\langle e|,\qquad \Delta E=431.0812443150\ \mathrm{MeV}.$$

Here $\Delta E$ is the first selected gap of the full 95D generator. Its two-mode subspace is invariant under that generator; it is not an unrelated replacement Hamiltonian. Thus $\operatorname{Tr}(\rho_0H)-E_g=p_e\Delta E=34.47643573912226\ \mathrm{MeV}$.

**Reference matching.** We adopt the inherited pure-proton illustration at $V_0$. The exact conversion is $1\ \mathrm{MeV}=1.602176634\times10^{-13}\ \mathrm{J}$. Set

$$\overline{N}=\frac{E_{\phi,\mathrm{ref}}}{E_{p,\mathrm{rest}}+p_e\Delta E}=0.2425893463937076,\qquad E_{\phi,\mathrm{ref}}=f_\phi u_0V_0.$$

Both denominator terms are expressed in J before evaluation. $\overline{N}$ is an externally matched expected occupancy. It is neither a derived cosmic proton abundance nor a fractional proton realization. The integer one-proton calculation on the next page has its own controller budget.

Table 2 Replacement of the inherited phenotype allocation

| Reference quantity | Energy in J |
|---|---:|
| Rest energy per proton | $1.5032776180\times10^{-10}$ |
| Expected rest allocation | $3.6467913480\times10^{-11}$ |
| Expected initial excitation | $1.3399990150\times10^{-12}$ |
| Rest plus excitation | $3.7807912495\times10^{-11}$ |
| Original phenotype allocation | $3.7807912495\times10^{-11}$ |

We replace the last row with the preceding split. Adding the split to the original total a second time would duplicate exactly $E_{\phi,\mathrm{ref}}$. The $D$ and $R$ allocations retain their inherited energies. Address branch probability 0.05 and energy fraction 0.0493 have different roles and are kept separate.

CASEPAGEBREAK

# 3 One write and conditional time prediction

Choose $|\pm\rangle=(|g\rangle\pm|e\rangle)/\sqrt2$, with $P_\pm=|\pm\rangle\langle\pm|$. The blank record is $|0\rangle$ with gap $\varepsilon_r=3.5596112121\times10^{-15}\ \mathrm{J}$ from the electron-mode energy $\mu$ defined below. The original write coupling is

$$W=P_+\otimes I+P_-\otimes X,\qquad H_s=\operatorname{diag}(0,\Delta E),\quad H_r=\operatorname{diag}(0,\varepsilon_r).$$

$W$ is unitary, and the pointer maps the two outcomes to bits 0 and 1. Each conditional outcome has probability 1/2. Ignoring the outcome leaves system state $I/2$ and mean record energy $\varepsilon_r/2$. The relative system energy therefore changes from $p_e\Delta E$ to $\Delta E/2$.

For **one conditioned proton**, the mean write work is

$$w_{\mathrm{write}}=(\tfrac12-p_e)\Delta E+\tfrac12\varepsilon_r=2.9011460679\times10^{-11}\ \mathrm{J}.$$

All energies in this equation are evaluated in J. The individual original controller starts with $\Delta E+\varepsilon_r=6.9070389311\times10^{-11}\ \mathrm{J}$ and retains $4.0058928632\times10^{-11}\ \mathrm{J}$ after the mean write. It covers both outcome-dependent costs. This controller is an externally controlled budget; an autonomous energy-conserving apparatus Hamiltonian has not been constructed.

**Complete source routing.** Conditional measurement splits only the $\phi$ branch. The five probabilities are $0.025$, $0.025$, $0.268$, $0.007772944563$, and $0.674227055437$ for $\phi_+$, $\phi_-$, $D$, initial reflection and normal return. They sum to one; residents alone sum to 0.318.

**Proper-time prediction.** Adopt $\mu=510998.95069/23\ \mathrm{eV}$, $\omega=\mu/\hbar$ and $\delta\tau=0.1/\omega=2.9626039328317383\times10^{-21}\ \mathrm{s}$. We convert $\mu$ to J in the rate equation. After a selected first result,

$$U(\tau)=e^{-iH_s\tau/\hbar},\qquad P_{\mathrm{same}}(k)=\cos^2\!\left(\frac{\Delta E\,k\delta\tau}{2\hbar}\right).$$

| Separation in adopted frames | Same outcome probability |
|---:|---:|
| 1 | 0.675164206721 |
| 2 | 0.122729997265 |
| 4 | 0.569330619854 |

The clock mapping is an adopted construction, not an identified physical clock rate. These are conditional transition predictions. They do not include the energy of a repeated write/reset cycle or cumulative storage of all simulated records.

CASEPAGEBREAK

# 4 The same energy in the homogeneous ledger

To connect the individual state calculation to the inherited reference volume, multiply its mean increments by $\overline{N}$. This defines a mean ensemble ledger for one ideal write per occupant. It does not make the small volume budget sufficient to perform one actual proton write; the individual controller on page 3 provides that separate illustration.

The mean internal increase is $7.0374395222\times10^{-12}\ \mathrm{J}$ and the mean record increase is $4.3176187869\times10^{-16}\ \mathrm{J}$. Their sum, $\delta E_{\mathrm{write}}=7.0378712840\times10^{-12}\ \mathrm{J}$, is supplied once. The finite mean supplier begins with $7.5615824991\times10^{-12}\ \mathrm{J}$.

Table 3 Mean energy accounts at the same reference volume

| Boundary quantity | Before | After |
|---|---:|---:|
| System including record in J | $7.6689477678\times10^{-10}$ | $7.7393264807\times10^{-10}$ |
| Supplier in J | $7.5615824991\times10^{-12}$ | $5.2371121503\times10^{-13}$ |
| System plus supplier in J | $7.7445635928\times10^{-10}$ | $7.7445635928\times10^{-10}$ |
| Pressure in Pa | $-5.2585974844\times10^{-10}$ | $-5.2585974844\times10^{-10}$ |
| $q$ with supplier outside | −0.528550000000 | −0.519196728075 |
| $q$ with pressureless supplier inside | −0.518507515893 | −0.518507515893 |

**Volume law and boundary.** At fixed comoving occupancy and fixed state, rest, excitation, $D$ and the modeled record are volume-independent energies. The $R$ sector is extensive in volume:

$$E_{\mathrm{out}}(V)=M+\delta E_{\mathrm{write}}+LV,\quad L=\frac{E_{R,0}}{V_0},\quad P=-\frac{\partial E}{\partial V}=-L.$$

$M$ contains the pre-write constant energies. Before the write, omit $\delta E_{\mathrm{write}}$. With $u=E/V$, the adopted homogeneous response is $q=\tfrac12(1+3P/u)$. The derivative and this response use the same energy expression.

If the supplier is outside, the system gains energy and its $q$ changes as shown. If a pressureless comoving supplier is included, its loss exactly offsets the system gain, so total energy and $q$ remain constant. The two initial $q$ values differ because the two boundaries contain different initial energies. The enlarged boundary includes the write supplier defined here, not an independently added copy of the individual controller budget.

These values are boundary diagnostics at $V_0$ under the stated volume law. They do not constitute a measured expansion change, a time-resolved source $Q(\tau)$, or a common SI covariant evolution of an apparatus and the cosmological background.

CASEPAGEBREAK

# 5 Reproduction and review questions

We replayed unchanged bridge programs 0.2, 0.3, 0.5 and 0.6, forwarding the fresh state and basis. Their 95, 134, 134 and 87 checks pass, including controls beyond this case. The additional 26 contracts test this case's transfers and predictions. These are software consistency checks, not physical experiments.

Table 4 Controls that can reject or distinguish the construction

| Control | Calculated response or rejection |
|---|---|
| Change source phase by 0.7 rad | Address-dephased excitation unchanged within numerical tolerance |
| Double adopted frame duration | First-repeat probability changes from 0.675164206721 to 0.122729997265 |
| Reduce mean supplier to half the required work | Original exchange rule rejects the transfer |
| Add rest and excitation to the unreplaced phenotype energy | Duplicate $3.7807912495\times10^{-11}\ \mathrm{J}$ detected |
| Differentiate energy with respect to volume | Finite difference agrees with pressure $-L$ |

The package includes frozen source, inputs and hashes, executable code, expected results and CSV ledgers. `reference_boundary.json` retains the published comparison. Word equations are editable.

With Python and `requirements.txt`, run `python reproduce.py --out replay` in the unpacked package. It verifies the source hash and writes fresh results and logs. Success means 450 original checks, 26 case contracts and zero failures. Comparisons use declared numerical tolerances; displayed values are rounded.

**Questions for a reviewer**

1. Is the address selector a justified physical preparation of $\rho_0$, and do connected inputs affect the state as declared?
2. Are energy replacement and matched $\overline{N}$ legitimate mean calibration without implying a derived species abundance?
3. Do the instrument, supplier boundary and volume law support the calculated work and homogeneous response?
4. Which preparation, timing and record measurements distinguish these predictions from alternative rules at the same calibration?

**References**

[1] W. Choi and J. Choi. *WRRA M Integrated Upstream and Downstream Model*. Integrated 1.0 reviewed r1, 3 October 2026. https://doi.org/10.5281/zenodo.23126800

[2] W. Choi and J. Choi. *WRRA M Bridge 0.5–0.8 Reviewed r1*. Frozen executable source included unchanged in this package. Its source identity and the enclosing integrated package are recorded by SHA256 in `inputs.json`.
