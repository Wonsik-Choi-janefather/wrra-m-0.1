# WRRA M 0 9 Common Sector Accounting and the Upstream Input Contract

Arithmetic calibration on one denominator and connection to particle channels

최원식 Wonsik Choi

WRRA-M 0.9-r1 | 2026-10-02

Independent Researcher Seoul Republic of Korea

ORCID 0009-0001-4263-9772 | janefather@gmail.com

## Evaluation scope and completed calculation

Version 0.9 computes phenotype, resident nonphenotype and return using one address measure, then connects the expressed budget to the selected 0.8 particle channels. Verification inputs are WRRA Core 1.0, MCC 2.3.2, frozen 0.8 inputs, and the upstream two-stage filter and zeta-zero update calculations. Known particle assignments and composition targets are legitimate calibration inputs for this constructed model.

The WRRA-specific transformation takes the address state and spectrum, accumulates admission from a depleted reservoir, closes the three-sector ledger at the recovery boundary, and applies normalized conditional channel routing followed by the computed selection permutation. Outputs are 5%, 26.8% and 68.2%, resident Actual 31.8%, total accounted weight 100%, and a 48-channel ledger. Twenty-seven verification groups pass, and all nine 0.8 results and their charge assignments are reproduced unchanged.

Falsification conditions are failure of frozen calibrated reproduction, negative or incomplete sector effects, inconsistent transition accounting, duplicated channel or generation weight, charge disagreement, or undisclosed calibration changes. Mapping arithmetic load to physical energy and pressure belongs to 0.10; individual 0/1 measurement outcomes and physical records belong to 0.13. Admission weights here are deterministic expected transport, with no newly implemented physical Born measurement rule.

## Address state and calibration on a common denominator

Addresses run from 2 through N_address=1,000,000. Every sector uses the same n^-alpha measure. Primes initially occupy the SOURCE reservoir, even composites form resident nonphenotype D, and odd composites support phenotype admission. The physical interpretation and origin of this arithmetic classification remain constitutive assumptions and upstream questions.



$$
w_n=\frac{n^{-\alpha}}{\sum_{m=2}^{N_{\mathrm{address}}}m^{-\alpha}},\qquad \sum_n w_n=1. \tag{1}
$$



The input alpha=1.8996876950554356 is the arithmetic calibration fitting D=0.268. The threshold h=1.447673170352440 fits phenotype 0.05. Return 0.682 follows by closure. Beta in the constant-admission comparison and beta_eff in the zeta update have different roles. In the default update, beta_eff=0.8654570124137115 is computed as phenotype divided by available odd-composite weight and is not supplied as an extra free coefficient.

The 4.8769% comparison admits all odd composites at alpha=2, while 26.7942% is the even-composite comparison at alpha=1.9. Values across those rows are never added. Each row has its own normalized denominator; the joint reference instead uses alpha about 1.899687695 and the update threshold h.



| alpha | Odd composite % | Even composite % | Prime % |
| --- | --- | --- | --- |
| 2.0 | 4.876893 | 24.999961 | 70.123145 |
| 1.9 | 5.774215 | 26.794200 | 67.431586 |



## Upstream inputs and the update boundary

Interface wrra.upstream-ledger/1 fixes the address state, measure, adopted spectrum, coefficients and phases, admission update, recovery boundary, channel coupling and source hashes. The reference address state is a normalized diagonal n^-alpha distribution; the computational API also checks supplied normalized diagonal states. Large-scale dynamics of a general full address density matrix are outside this run. Downstream carrier rho and the address state are inputs on different state spaces, coupled by the declared conditional routing rule.

The spectrum is the first four positive zeta-zero heights gamma_j, rechecked by independent high-precision computation and Euler Maclaurin expansion. Each coefficient is 1/2, initial phases are zero, xi=0.1, and there are K=8 admission updates. Selecting zeta heights and cosine driving is an upstream model input. Update index k and xi are dimensionless; seconds and proper time are not assigned. Physical spectral energies require allowed modes and boundary conditions in 0.12.



$$
\delta_n(k)=\sum_{j=1}^{J}c_j\cos\!\left[\gamma_j(\log n+\xi k)+\theta_j\right]. \tag{2}
$$





$$
a_n(k)=\frac{1}{1+e^{h-\delta_n(k)}},\qquad T_n(K)=1-\prod_{k=0}^{K-1}(1-a_n(k)). \tag{3}
$$



New admission b_n is removed from the still-unadmitted odd-composite reservoir r_n. Adding attempts without depletion would count previously admitted weight again. Cumulative products and sequential depletion are computed independently and agree. Even composites occupy D from the start; primes and unadmitted odd composites remain pending SOURCE S until the recovery boundary.



$$
b_n(k)=r_n(k)a_n(k),\qquad r_n(k+1)=r_n(k)-b_n(k),\quad r_n(0)=w_n. \tag{4}
$$



At the declared boundary k=K, pending S is transferred to the return ledger R. Subsequent resident folds use an identity update, the retention rule of this release. Its origin and dynamical cosmological recovery are not derived. S and R are never counted twice. Row k=-1 denotes the state before admission and is not a negative physical time.



$$
e_\varphi(n)=\mathbf1_{\mathrm{odd\ comp}}T_n(K),\quad e_D(n)=\mathbf1_{\mathrm{even\ comp}},\quad e_R(n)=1-e_\varphi(n)-e_D(n). \tag{5}
$$





$$
f_s=\sum_n w_ne_s(n),\quad e_s(n)\geq0,\quad\sum_se_s(n)=1,\quad\sum_sf_s=1. \tag{6}
$$





$$
\varphi_k+D_k+S_k+R_k=1,\quad R_{k<K}=0,\quad S_{k\geq K}=0. \tag{7}
$$





| k | Phenotype % | Resident D % | Pending S % | Return R % |
| --- | --- | --- | --- | --- |
| -1 | 0.000000 | 26.800000 | 73.200000 | 0.000000 |
| 0 | 1.501794 | 26.800000 | 71.698206 | 0.000000 |
| 1 | 2.513899 | 26.800000 | 70.686101 | 0.000000 |
| 2 | 3.044795 | 26.800000 | 70.155205 | 0.000000 |
| 3 | 3.704795 | 26.800000 | 69.495205 | 0.000000 |
| 4 | 4.050025 | 26.800000 | 69.149975 | 0.000000 |
| 5 | 4.630648 | 26.800000 | 68.569352 | 0.000000 |
| 6 | 4.853503 | 26.800000 | 68.346497 | 0.000000 |
| 7 | 5.000000 | 26.800000 | 68.200000 | 0.000000 |
| 8 | 5.000000 | 26.800000 | 0.000000 | 68.200000 |
| 9 | 5.000000 | 26.800000 | 0.000000 | 68.200000 |
| 10 | 5.000000 | 26.800000 | 0.000000 | 68.200000 |



## Resident Actual and complete Actual scopes

Upstream resident Actual is phi+D after the recovery boundary and occupies 31.8% of the full address denominator. The downstream complete Actual ledger accounts for phenotype, resident nonphenotype and the returned provenance of a background response, totaling 100%. This does not mean returned R remains in the resident address state. Its provenance is represented separately in the downstream response ledger.



$$
A_{\mathrm{resident}}=f_\varphi+f_D=0.318,\qquad A_{\mathrm{complete\ ledger}}=f_\varphi+f_D+f_R=1. \tag{8}
$$





$$
f_{\varphi\mid A}=\frac{f_\varphi}{f_\varphi+f_D},\quad f_{D\mid A}=\frac{f_D}{f_\varphi+f_D},\quad f_{R\mid A}=0. \tag{9}
$$



Renormalization within the resident scope gives about 15.72327% phenotype and 84.27673% D. These conditional shares differ from the full 5%, 26.8% and 68.2% partition. The following sector, resident and complete rows all use the original denominator. Stored inputs and ledgers remain unrounded; only displayed tables are rounded.



| Scope | Original denominator | Share % |
| --- | --- | --- |
| Phenotype phi | 1 | 5.00000000 |
| Resident nonphenotype D | 1 | 26.80000000 |
| Return R | 1 | 68.20000000 |
| Resident Actual | 1 | 31.80000000 |
| Complete accounted Actual | 1 | 100.00000000 |



## Conditional connection to selected particle channels

The actual 0.8 selection F_DX and its permutation P on sixteen origins are executed unchanged. Phenotype address weight is routed through a conditional origin kernel q_i(n), then the selected permutation and normalized generation state p_g are applied. The reference uses an address-independent 1/16 kernel and 1/3 per generation. A family classified by its odd smallest prime can supply a different normalized kernel; nonuniform kernels and generation weights are executed as controls.



$$
x_i=\sum_nw_ne_\varphi(n)q_i(n),\quad\sum_iq_i(n)=1,\qquad y=Px. \tag{10}
$$





$$
W_{g,i}=p_gy_i,\quad P^\dagger P=I,\quad\sum_gp_g=1,\quad\sum_{g,i}W_{g,i}=f_\varphi. \tag{11}
$$



The address-to-channel correspondence is a disclosed constitutive input. It does not uniquely derive particle identities or masses from prime genealogy. Y and Q use the same 0.8 charge operator. The weights below divide the reference 5% phenotype budget and are not measured particle populations or new cosmic composition fractions. The inventory retains 45 Standard-Model chiral components and three conditional neutral extension slots; their existence, mass and occupation are not measured here.



| Field | Count | Y | Full ledger weight % |
| --- | --- | --- | --- |
| Q_L | 18 | 1/6 | 1.87500000 |
| L_L | 6 | -1/2 | 0.62500000 |
| u_c | 9 | -2/3 | 0.93750000 |
| d_c | 9 | 1/3 | 0.93750000 |
| nu_c | 3 | 0 | 0.31250000 |
| e_c | 3 | 1 | 0.31250000 |



## The next boundary to physical energy and pressure

The common arithmetic partition is 5%, 26.8% and 68.2%, while the 0.6 to 0.8 physical energy calibration remains 4.93%, 26.5% and 68.57%. Separate ledgers preserve both; arithmetic calibration never silently overwrites physical inputs. Existing 0.8 load and pressure calculations leading to gravity and expansion are reproduced. Returned provenance is structurally assigned to the background-response branch in physical_bridge, but its energy and pressure functions remain unset.

Version 0.10 must specify physical energy load epsilon_s(n,V), sector coupling and volume dependence. The following relation is a requirement for that interface, not an executed 0.9 output. The fixed state mathcal S means the address state, effects and coupling configuration, distinct from pending SOURCE S_k. R=68.2% alone does not determine pressure, and 95:5 alone does not determine length. Existing expansion response and the future causal account of twist remain distinct. The SI defining value of c stays a fixed input.



$$
E_s(V)=\sum_nw_ne_s(n)\epsilon_s(n,V),\qquad P_s=-\left.\frac{\partial E_s}{\partial V}\right|_{\mathcal S}. \tag{12}
$$



Subsequent stages separate update order from physical time, address cutoff from zeta cutoff and information capacity, and local thresholds from global Capacity. Microscopic generation of upstream inputs, global overload and reset, initial opening and initial cutoff selection remain upstream questions. Software execution provenance is not called a physical observation record or an accumulated twist record.

## Verification and reproduction

The 27 groups cover independent primality, frozen upstream code and results, independently checked zeta heights, cumulative products versus depletion, address and frame conservation, Actual denominators, equality of all 0.8 results, nonuniform channel coupling, arbitrary diagonal states and effect positivity on a small coherent state, explicit arithmetic refitting, boundary changes, equal aggregates from different microscopic rules, separate cutoffs, rejection of sixteen invalid inputs, and provenance hashes. Revision r1 also checks twenty exhaustive sparse-kernel cases; direct positive accumulation preserves zero channel support without negative cancellation residuals.

Changing K to 4 and 16 with other calibrations frozen gives phenotype about 3.704795% and 5.682474%. With xi=0, explicitly refitting h restores 5% while address admissions differ. Aggregate reproduction therefore does not establish a unique microscopic rule. Explanatory reproduction under validated calibration and declared rules is accepted; prediction is reserved for later unmeasured outputs after model fixation.

```bash
python -m pip install -r calculations/wrra_m_0_9/requirements.txt
python calculations/wrra_m_0_9/run_release.py
```

From the archive root, the command generates the input and result JSON, frame, scope, address and channel CSVs, and verification report. Parameters.json is the single configuration input, embedding the 0.8 input and five upstream snapshots. A clean copy removes captured outputs before execution and checks byte-identical reproduction and the SHA256 manifest. Bilingual equations and calculated tables are matched.

Input SHA256 7986e6afcbe26e3546111387f34f953147e16cb3c8cb6b900264adf214e51e95

## Subsequent development order

The sequence continues with 0.10 energy and pressure mapping; 0.11 sequential calibration G → H0 → f_phi → f_c → m_e c^2; 0.12 shutter, proper time and spectra; 0.13 quantization, observation and records; 0.14 cutoffs and capacity; 0.15 stress, twist and size; 0.16 neutrino mass, mixing and oscillation; 0.17 propagation in the same geometry; and 1.0 integration audit and fixation. Each version closes through verification input, WRRA-specific transformation, output and falsification conditions.

## References

Choi Wonsik. WRRA-M 0.1 to 0.8 and upstream hypotheses. GitHub research repository. https://github.com/Wonsik-Choi-janefather/wrra-m-0.1

Choi Wonsik. Upstream two stage filter v1.0 and zeta frame v0.1. Source commit 9ca21c547e5238be34ceace5a1015db50cb824ff. Included reference snapshots.

Choi Wonsik. Minimal Computation Cosmology 2.3.2. Common carrier baseline. https://github.com/Wonsik-Choi-janefather/minimal-computing-cosmology-2.3.2

NIST Digital Library of Mathematical Functions. Sections 25.10 and 25.11 iii. Zeta zeros and Euler Maclaurin representation. https://dlmf.nist.gov/25.10 https://dlmf.nist.gov/25.11

Copyright 2026 Wonsik Choi. CC BY 4.0. https://creativecommons.org/licenses/by/4.0/
