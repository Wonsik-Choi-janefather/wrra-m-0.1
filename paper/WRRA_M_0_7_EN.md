# WRRA M 0 7 Actual and Phenotype in an Energy Weighted Information Ledger

Common definitions and a reproducible load measure for our universe model

Wonsik Choi  
WRRA-M 0.7-r1 | October 2 2026  
Independent Researcher Seoul Republic of Korea  
ORCID 0009-0001-4263-9772 | janefather@gmail.com

## Evaluation order and result

Verification inputs are the public 0.6-r2 code and calibration ledger continuing WRRA Core 1.0 and MCC 2.3.2. The speed of light is fixed by the SI definition; late-universe fractions and local test-source conditions remain editable inputs. The WRRA-specific transformation adds positive state loads in three sectors, normalizes their total as the energy-weighted information load of Actual, and computes phenotype and hidden shares. The same loads enter the existing energy, pressure, gravity and expansion calculation.

Outputs reproduce the reference phenotype share of 4.93 percent and hidden share of 95.07 percent, recalculate shares for changed states and scale, and retain the inherited rotation, lensing and expansion outputs. Falsification conditions include a negative admissible load, a failed partition, disagreement with the same-input 0.6 energy or pressure, or claiming an unexecuted transition as complete.

Version 0.7 establishes the common definitions, measure and computed ledger. Its completed connection is weighted accounting to the inherited load calculation. Physical quantization events and particle-filter selection are executed in subsequent releases. Calibration with established values is legitimate model construction; independent prediction is not required for this completion.

## Definitions of Actual quantization and phenotype

Actual is the complete current state, scale, constitutive inputs and records represented by this model. One hundred percent means normalization by the adopted total weighted load. It does not assert an infinite bit inventory or that every microscopic state of the universe has already been observed. Theta denotes the common input ledger of constants, calibrations, operators and test-source conditions; R denotes physical outcome records. The physical record list is empty in 0.7.


$$\mathscr A=(a,\rho,\Theta,\mathcal R),\qquad \rho\succeq0,\quad\mathrm{Tr}\rho=1.\tag{1}$$


Quantization is defined as an operation taking the Actual state to a discrete phenotype outcome, a post-observation state and a physical record. This release prepares its input and output accounting. It does not yet execute boundary selection of 0 or 1, outcome probabilities or a measurement state update. The result explicitly reports quantization_status as unexecuted.

Phenotype is the load allocated to the currently expressed sector in the adopted our-universe branch. Hidden load comprises clustering and background sectors. Both belong to Actual and contribute to gravity and expansion. Lack of expression does not set their loads to zero. Residue denotes retained unexpressed state content and is not added as an independent fourth energy component.

A physical record is a system state retaining a transition outcome. Input provenance and execution logs are reproducibility records, distinguished from physical observation records. Future record-system energy is a suballocation within existing sectors. It must not be counted again under a separate record-cost label.

## Common carrier and positive load operators

The sixteen test channels and N internal lattice sites of 0.6 are retained. N=128 is a load-computation grid size, not a particle-channel count. The inherited product state uses the common channel state I16/16 and internal state rho. This release evaluates internal loads and does not newly select particle assignments or filters.


$$K_c=2I-T-T^\dagger,\qquad K_b=\frac{K_c+\epsilon|0\rangle\langle0|}{1+\epsilon/(2N)}.\tag{2}$$


For the uniform state, Jc=Tr(rho Kc)=2 and Jb=Tr(rho Kb)=2. Epsilon zero is the reference carrier; epsilon eight is the inherited noncommuting test choice, not a measurement of the actual universe. Sector weighting operators are defined below. The background fraction is computed as 1 minus the phenotype and clustering fractions rather than entered independently.


$$A_\phi=f_\phi I,\quad A_c=\frac{f_c}{2}a^{n_c}K_c,\quad A_b=\frac{f_b}{2}a^{n_b}K_b.\tag{3}$$


The reference adopts fphi=0.0493, fc=0.265, fb=0.6857, nc=0 and nb=3. Aphi=fphi I retains the pressureless phenotype comoving energy of 0.6. This term does not itself generate a microscopic observation event. The sectors are weighted accounting terms and are not orthogonal outcome projectors.

## The measure underlying approximately five percent

For a set of sector labels S, the information-load measure sums state traces against positive weighting operators. Admissible states and operators give nonnegative weights and additivity for disjoint sets of sector labels.


$$\mu_a(S)=\sum_{s\in S}\mathrm{Tr}(\rho A_s),\qquad W=\mu_a(\{\phi,c,b\}).\tag{4}$$


Information weight means the state-dependent expected load entering the energy response. It is distinct from Shannon information, von Neumann entropy, a bit count or a channel count. Trace-one states can carry different loads. State entropy is reported separately as a diagnostic.


$$F_\phi=\frac{\mathrm{Tr}(\rho A_\phi)}{W},\quad F_h=\frac{\mathrm{Tr}(\rho(A_c+A_b))}{W},\quad F_\phi+F_h=1.\tag{5}$$


Fphi and Fh are shares of the total weighted load at the current state and scale. They are not probabilities of a zero or one measurement outcome. If W is zero, normalized shares are undefined and represented by JSON null. A trace-one carrier state can lie in the common null space of its load operators.


$$a=1,\quad\rho=I/N:\quad(F_\phi,F_c,F_b)=(0.0493,0.265,0.6857).\tag{6}$$


Mapping the approximately five percent late-universe reference to the phenotype sector is a disclosed WRRA constitutive choice. It connects the inherited energy-weighted calibration and the information-load measure in one ledger, reproducing 4.93 percent at the reference. This is not relabeled as a direct count of information bits. Established constants and observations remain valid calibration material for the selected our-universe branch.

## Shares under state and scale changes

The 4.93 percent value is a calibrated reference at a=1 in the uniform state. Even with the same constitution, a changed state or scale requires recalculation. Retaining clustering exponent zero and background exponent three gives the following uniform-state formula.


$$\rho=I/N:\quad F_\phi(a)=\frac{f_\phi}{f_\phi+f_c+f_ba^3},\qquad n_c=0,\quad n_b=3.\tag{7}$$



|State|Jc|Jb|Phenotype %|Hidden %|
|---|---|---|---|---|
|Uniform a 0.5|2.000000|2.000000|12.324615|87.675385|
|Uniform a 1|2.000000|2.000000|4.930000|95.070000|
|Uniform a 2|2.000000|2.000000|0.850015|99.149985|
|Low mode|0.152241|0.152241|40.520194|59.479806|
|High mode|4.000000|4.000000|2.527298|97.472702|
|Zero mode|0.000000|0.000000|100.000000|0.000000|
|Coherent packet|0.657554|0.657554|13.623750|86.376250|
|Uniform noncommuting|2.000000|2.000000|4.930000|95.070000|
|Packet noncommuting|0.657554|0.819446|11.811981|88.188019|


Low-mode, high-mode, zero-mode and packet rows are structural test states, not new observed cosmic fractions. Low and high pure modes both have zero state entropy but different phenotype shares. This distinguishes the adopted weighted measure from entropy or the number of states.

The uniform phenotype share is approximately 12.324615 percent at a=0.5 and 0.850015 percent at a=2. These are conditional outputs of the fixed volume dependence and sector allocation. If used as future-universe predictions, the frozen model and calibration conditions must accompany them.

## Energy pressure gravity and expansion from the same ledger

V0 is a representative comoving volume; its default of one cubic metre is a bookkeeping unit, not the size of the universe. The reference energy density is ucrit,0=3H0 squared c squared divided by 8 pi G. Mapping weighted loads to physical energy reproduces exactly the three sector energies of 0.6. The phenotype exponent is zero.


$$E_s=u_{\mathrm{crit},0}V_0\mathrm{Tr}(\rho A_s),\quad u_s=\frac{E_s}{V_0a^3},\quad p_s=-\frac{n_s}{3}u_s.\tag{8}$$



$$H^2=\frac{8\pi G}{3c^2}u_{\mathrm{tot}},\qquad q=\frac{u_{\mathrm{tot}}+3p_{\mathrm{tot}}}{2u_{\mathrm{tot}}}.\tag{9}$$


The present uniform reference reproduces H/H0=1 and q=-0.52855. Sending the same clustering load into the inherited local response retains test rotation 207.510905 km/s and conditional deflection 0.535586511 arcsec. The local test source and Phi=Psi condition are unchanged; no new observational galaxy fit is performed.

Global twist record magnitude remains an instantaneous aggregate of load and spatial size. No independent temporal accumulation law is added. Calculation of twist and expansion from the same load is distinguished from a claim that twist causes expansion. The pressure and expansion equations use external mathematics already executed in 0.6; the WRRA contribution here is the actual connection of state loads and phenotype accounting to those calculations.

## Verification and failure conditions

Nineteen check groups pass. In addition to nine representative ledgers, twenty-four mixed-state, grid and exponent combinations are evaluated. Nine invalid input or state cases, including a fictitious physical record, are rejected. Independent comparisons use rational reference fractions, finite volume differences, simultaneous basis changes and fixed-scale unitary propagation.


$$A=A_\phi+A_c+A_b,\quad\rho^{\prime}=U\rho U^\dagger,\quad U=e^{-i\tau A},\quad\mathrm{Tr}(\rho^{\prime}A)=\mathrm{Tr}(\rho A).\tag{10}$$


Equation ten tests energy conservation at fixed scale. Individual sector loads may change under unitary evolution while the energy of the same total operator is preserved. This is not expanded into a completed test of energy exchange during a physical quantization event.


|No|Check|Result|
|---|---|---|
|1|exact reference fraction at three scales|Pass|
|2|positive additive weight and normalized partition|Pass|
|3|same energy and pressure as 0 6 r2|Pass|
|4|inherited reference rotation and lensing|Pass|
|5|pressure from independent volume difference|Pass|
|6|joint basis covariance|Pass|
|7|fixed scale unitary energy and state spectrum|Pass|
|8|admissible mixed states and exponent changes|Pass|
|9|declared recalibration propagates|Pass|
|10|bookkeeping volume does not change density or share|Pass|
|11|information weight is distinct from entropy or state count|Pass|
|12|zero total weight is undefined fraction not false probability|Pass|
|13|zero background sector|Pass|
|14|invalid inputs and states rejected|Pass|
|15|no fictitious measurement or double counted record|Pass|
|16|input ledger preserved|Pass|
|17|tiny positive load is retained with matching gravity|Pass|
|18|accepted trace roundoff is normalized before accounting|Pass|
|19|negative state above roundoff is rejected|Pass|


The maximum reference-share error is 6.939e-18; the maximum sector-weight partition error is 1.776e-15. The independent pressure difference has maximum relative error 1.241e-11; fixed-scale unitary total-energy relative error is 2.220e-16. Inherited rotation and lensing discrepancies are recorded in verification.json. Revision r1 retains positive load 10^-15, normalizes accepted trace roundoff and rejects negative states beyond numerical roundoff. These establish computation consistency and reproduction within the declared model.

A negative admissible load, inconsistent sector sum, loss of state positivity or trace, or mismatch between pressure and the same energy-volume derivative requires revision of the corresponding calculation. Undisclosed recalibration and reporting an unexecuted measurement law as complete are also failure conditions.

## Ledger passed to subsequent releases

Parameters.json is the sole executable input for constants, fractions, grid, exponents, test source and bookkeeping volume. Outputs include a SHA256 hash of its canonical JSON representation. Changing the input changes the result and hash; mutation during execution fails. Results.json retains sector weights, energy, density, pressure, the 0.6 bridge outputs, state recipes and the unexecuted measurement status.

Version 0.8 connects particle and filter selection; 0.9 executes upstream inputs and common arithmetic accounting. Version 0.10 maps address information weights to physical energy and pressure; 0.11 performs sequential physical calibration. Version 0.12 connects shutter order, proper time and allowed spectra; 0.13 implements quantization outcomes, probabilities, post-observation states and records. Repeated-event uncertainty and capacity belong to 0.14. The next equation is a future accounting contract, not an executed measurement law in 0.7.


$$E_{\mathrm{before}}+E_{\mathrm{environment,before}}=E_{\mathrm{after}}+E_{\mathrm{environment,after}}.\tag{11}$$


Version 0.15 connects stress, twist, curvature and size; 0.16 covers neutrino masses, mixing and oscillation; 0.17 propagates neutrinos in the shared geometry. Version 1.0 compares the integrated run, documents and claim ledger before fixation. Completion of 0.7 covers common definitions, the energy-weighted measure and the inherited load bridge. It does not pre-emptively certify particle selection, measurement dynamics or full theoretical integration. The same evidentiary standard distinguishes external validation inputs and actual WRRA execution.

## Reproduction and references

From the archive root, run python calculations/wrra_m_0_7/run_release.py to produce the case table and verification.json. Computation requires numpy and scipy. Document authoring additionally requires pandoc and python-docx; PDF rendering requires LibreOffice. Inputs and state recipes are fixed. The additional mixed-state tests use seed 707.

Choi Wonsik. WRRA-M 0.6-r2. 2026. https://doi.org/10.5281/zenodo.23076547

WRRA-M repository. https://github.com/Wonsik-Choi-janefather/wrra-m-0.1

Planck Collaboration. Planck 2018 results VI Cosmological parameters. Astronomy and Astrophysics 641 A6 2020. https://doi.org/10.1051/0004-6361/201833910 . This is calibration context; no new raw-data fit is performed in 0.7. The exact executable values 4.93 percent and 26.5 percent are rounded calibrations inherited from the 0.6-r2 ledger.

BIPM. The International System of Units SI defining constants. https://www.bipm.org/en/measurement-units/si-defining-constants . The speed of light 299792458 m/s is a fixed defining input, not a WRRA prediction.

Copyright 2026 Wonsik Choi. CC BY 4.0. https://creativecommons.org/licenses/by/4.0/
