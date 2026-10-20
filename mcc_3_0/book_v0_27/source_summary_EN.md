### 38.A Reader's Summary: How the Finite SOURCE Candidate Is Constructed

**Verified inputs.** The address-share targets 0.05, 0.268 and 0.682, the inherited harmonic ledger $(0,5,29)$ and standard tabulated positive zeta-zero heights are disclosed inputs. The decimal shares are the declared finite calibration targets, not infinitely precise measurements. Their exact rational representation fixes an arithmetic resolution conditional on those targets.

| Step / owner | Definition or constraint | Output and status |
|---|---|---|
| Address calibration | $0.05=1/20$, $0.268=67/250$, $0.682=341/500$ | Supplied address-share targets; distinct from ENERGY shares |
| Arithmetic resolution | $L=\operatorname{lcm}(20,250,500)$ | $L=500$ for the stated rational targets |
| Harmonic input | Largest index of inherited $(0,5,29)$ | $H=29$; not rederived by this table |
| Declared phase window | $T_H=2\pi H$ | $182.212373908208$; construction assumption |
| Finite spectral count | $C=\#\{j:0<\gamma_j<T_H\}$ | $C=70$, since $\gamma_{70}<T_H<\gamma_{71}$ |
| Finite product domain | $N_U=LHC$ | $500\times29\times70=1{,}015{,}000$ address labels |
| Executable domain | Address 1 inactive; $n=2,\ldots,N_U$ | $N_U-1=1{,}014{,}999$ active addresses |

**WRRA-specific transformation.** Serialize the finite product by $n=1+\ell+L[h+H(z-1)]$, with $0\le\ell<L$, $0\le h<H$, $1\le z\le C$. Thus multiplication counts the declared product domain. It is not an iterative convergence process toward $N_U$. The Euler–Maclaurin cutoff $M=LH=14{,}500$ is a separate numerical cutoff, not an additional factor in the address count.

**Outputs and falsification conditions.** The product and inactive-address count follow exactly from the declared construction. A failed denominator calculation, zero count, serialization bijection or frozen downstream replay would invalidate its associated claim. The physical selection of the harmonic input and phase rule, and robustness under alternative disclosed calibration/preparation branches, remain open. In particular $C$ depends on $H$ through $T_H$; the factors must not be described as three established statistically independent measurements. This table supplies traceability, not a new derivation of a universal cosmic capacity. See Chapters 37–40 and 102.
