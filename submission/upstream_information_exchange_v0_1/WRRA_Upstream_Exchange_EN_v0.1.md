---
title: "Finite Information Exchange Between Two Upstream Layers in WRRA"
author: "Wonsik Choi · Jeongin Choi"
date: "2026-10-20 | Version 0.1"
lang: en
abstract: "This paper implements a finite information-exchange interface between the topmost and intermediate layers of WRRA. A reversible composite transport envelope encodes the existing KZF coordinates without changing the SOURCE domain. Exclusive ownership, gated forward/reply transfers, reversible feedback and a typed connection to singly even transition candidates are specified. Exhaustive address checks preserve the original classification. A separate three-qubit SWAP test checks transfer of externally entangled payloads without cloning. The result completes one conditional engineering interface; the encoding is replaceable and does not establish the physical layers empirically."
---

DOI: <https://doi.org/10.5281/zenodo.23487587>


## Verified inputs and reverse-design criterion

The baseline is Chapters 38 and 135.12 of *Minimal Computing Cosmology 3.0*, book v0.25-r4, DOI [10.5281/zenodo.23486923](https://zenodo.org/records/23486923). Preserve the finite KZF domain

$$0\le\ell<500,\qquad0\le h<29,\qquad1\le z\le70,$$

and its frozen serialization

$$a=1+\ell+500[h+29(z-1)],\qquad1\le a\le N=1{,}015{,}000.$$

Address 1 is an inactive multiplicative/vacuum reference. No physical seconds, metres, shutter period, Planck interval or information flow rate is assigned to the upstream exchange. Event identifiers describe protocol events; they are not physical time coordinates.

The engineering criterion is reverse design: construct an interpreter for observed structure and revise mismatched connections. Reproduction counts as compatibility and explanatory achievement. Independent predictions are additional achievements. This work specifies and executes a finite interface, rather than reporting a new experiment or an unmeasured physical quantity. The input domain is adopted, not newly derived.

## WRRA transformation

### 1. An explicit quasi-prime transport envelope

Choose the following finite encoding:

$$Q(\ell,h,z)=2^{\ell+1}3^{h+1}5^z.$$

The term **WRRA quasi-prime carrier** denotes a structured composite envelope handled as one atomic transfer unit. It does not mean a Fermat pseudoprime or a composite that passes a specified primality test. This is one concrete implementation of the working term in Chapter 135.12. The chosen primes label coordinates; they are not physically privileged constants.

All three exponents are positive, so every evaluated carrier integer is composite. Recover its coordinates using prime valuations:

$$\ell=v_2(Q)-1,\qquad h=v_3(Q)-1,\qquad z=v_5(Q).$$

Unique factorization makes the encoding injective. The recovered coordinates give the original address through the unchanged KZF serialization. Reject additional prime factors and out-of-domain or missing exponents. Conversely, every declared coordinate triple generates a valid carrier, so the permitted carrier set has exactly $N$ elements.

The carrier's numerical magnitude is not mass, energy, spatial size or additional physical state count. Integers outside the declared sparse carrier set are not added as SOURCE states. Although the audit evaluates big integers, an implementation can retain the three exponents. Fixed coordinate fields need $9+5+7=21$ bits; a serialized address needs 20 bits. The largest evaluated label is 709 bits. This does not prove globally optimal computational cost or require storing a 709-bit physical amplitude for every event.

### 2. Bidirectional exchange with exclusive ownership

An active packet is owned by exactly one layer: topmost or intermediate. An allowed forward event moves ownership from top to middle and clears the original active ownership. A reply moves it back by the same rule. One session contains one accepted forward event and one accepted reply event. Replayed event identifiers, invalid source ownership, occupied destinations and active transmission of reference address 1 are rejected. A closed permission gate leaves the packet unchanged and does not commit a successful event.

The transferred information can include a response, rather than only an echoed address. The implemented register is a 16-bit value $x$, with illustrative reversible feedback

$$F_a(x)=x\mathbin{\mathrm{XOR}}(a\bmod65536),\qquad F_a(F_a(x))=x.$$

The middle layer can change the response while preserving recoverability. This XOR is a declared finite example, not a physical force or a uniquely required upstream law. A general payload $\xi$ needs an explicit module-specific transformation before that module is called integrated. The source address remains unchanged by the response. Original per-address weights are therefore referenced through the same owner and address.

### 3. Quantum payload transfer without copying

An unknown quantum payload is transferred by subsystem SWAP, rather than copying its amplitudes while keeping an active original. For an external reference $R$, top register $T$ and initially blank middle register $M$, the tested relation is

$$|\psi\rangle_{RT}|0\rangle_M\longmapsto|0\rangle_T|\psi\rangle_{RM}.$$

The external correlations are retained, and the old top register is blank after transfer. Applying SWAP again restores the initial state. The finite address relabeling is a bijection between permitted bases, so its linear extension defines an isometry between their finite state spaces. This mathematical extension does not amount to constructing or simulating the complete million-address quantum operator. The executed quantum audit uses three qubits and checks 200 externally entangled input states. It does not generate quantum amplitudes from number codes.

### 4. A typed map to the middle-layer singly even interface

Decode $Q$ to its original SOURCE address $a$, and define the total typed map $\mathcal A$ by three branches:

| Original address | Middle state | Inverse information |
|---|---|---|
| $a=1$ | Inactive reference | Retain $a$ and payload |
| Even $a$ | Retained upstream state | Retain $a$ and payload |
| Odd $a>1$ | Singly even candidate $r=2a$ | Recover $a=r/2$ and payload |

For the third branch, $r\equiv2\pmod4$, so the equal-only decomposition is $r\to a+a$. No asymmetric split is introduced. Invalid branch tags, undeclared or missing registers, out-of-range addresses and invalid parents are rejected by inverse decoding. Including the retained and reference branches makes the map reversible on its declared typed domain; it is not a claim that every address becomes massive matter.

For example, $a=9$ has coordinates $(8,0,1)$ and $Q=2^9\cdot3\cdot5=7680$. The chain is $Q\to9\to18\to9+9$. Address 5 yields the arithmetic candidate $10\to5+5$, but fails the odd-composite massive-phenotype filter. Even address 10 is exchangeable upstream and remains retained at this interface. Address 105 yields the structural candidate $210\to105+105$.

Structural candidacy and actual particle production are separate. Massive implementation additionally requires the original odd-composite admission rule, permission, species and inclusive energy/momentum/correlation accounting. This audit executes no physical particle emission. The transition label $r$ is not a newly allocated SOURCE address, nor an energy value.

### 5. Connection to the frozen book

Keep dimension classification and weights as functions of the original address $a$. Do not turn prime SOURCE labels into three-dimensional matter merely because their envelopes are composite. In particular, do not replace $w(a)$ with $w(Q)$ or $w(r)$. No source size, $\alpha$, $\beta$, weight table, shutter value or cosmic composition is recalibrated.

The permitted range of upstream transport is broader than massive-phenotype admission. The implementation introduces no extra global asymmetry register. Initial matter predominance, black-hole geometry and the later two-resolution measurement interface are separate connections, not outputs newly derived from this carrier encoding. Source classification invariance is checked exhaustively; the entire GR/CMB pipeline is not rerun here.

## Outputs and executed audit

Run `python3 exchange.py` with the dependency recorded in `requirements.txt`. `inputs.json` identifies the frozen book source and construction inputs. `results.json` records outputs, rejected controls, environment and the deterministic carrier-stream digest.

| Audit | Output |
|---|---|
| All SOURCE carrier generation, decoding and typed inverse checks | 1,015,000 addresses |
| Active forward/reply sessions | 1,014,999 |
| One-way ownership transfers | 2,029,998 |
| Source reference / prime / even composite / odd composite | 1 / 79,608 / 507,499 / 427,892 |
| Middle reference / even retained / odd candidate | 1 / 507,500 / 507,499 |
| Odd-composite structural candidates | 427,892 |
| Actual physical emissions | 0 |
| Rejected invalid requests and states | 18 controls |
| Three-qubit quantum transfer cases | 200 |
| SWAP unitarity and roundtrip amplitude error | 0 |
| External-reference joint-state error | At most $1.13\times10^{-16}$ |
| Joint-spectrum error | At most $7.77\times10^{-16}$ |

For every active address, a closed transfer gate is checked before the accepted session, and the reversible 16-bit response is recovered. The 18 negative controls cover invalid addresses, zero carrier, extra or missing factors, out-of-range exponents, inactive reference transmission, invalid owner, replay, parent congruence, unknown or mismatched tags, extra unowned fields, invalid payload, out-of-SOURCE candidates and non-Boolean permission. These counts are finite verification coverage, not independent observations.

## Falsification conditions

Revise the implementation if distinct addresses collide, inverse decoding fails, a transfer leaves two active owners, replay is accepted, original weights or classifications change, an invalid singly even candidate is emitted, a closed permission gate admits massive output, or transfer requires cloning an unknown state while preserving its active original. If a later implemented physical interface disagrees with tested reality, revise its feedback or interpretation rule.

The choice of encoding is replaceable and need not be unique to constitute a completed engineering interface candidate. Physical identification of the layers and any complete interacting microscopic dynamics require further implemented connections. Successful finite transport by itself is not empirical proof of the upstream ontology.

## Conclusion and availability

One explicit candidate now supplies the previously unspecified carrier generator and topmost/intermediate exchange map, including response, admission, exclusive ownership and inverse decoding. It closes that finite interface specification and passes the stated exhaustive checks. It does not assign physical time upstream or change the frozen SOURCE classification.

The authors are Wonsik Choi and Jeongin Choi, independent researchers. ChatGPT assisted drafting and code preparation; the authors retain responsibility. No new external peer review is claimed. This is a separate publication of the exchange result; it does not imply that the existing book or other released paper PDFs have already been revised.

Manuscripts are deposited on Zenodo. Code, inputs, results and reproduction files are linked through GitHub only:

<https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/main/submission/upstream_information_exchange_v0_1>.
