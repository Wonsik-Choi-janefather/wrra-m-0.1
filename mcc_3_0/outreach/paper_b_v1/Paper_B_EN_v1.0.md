# Closed connections and state changes after a loop in WRRA

Wonsik Choi and Jeongin Choi  
Independent Research, Seoul, Republic of Korea  
Executive paper B · Revised version 1.0 · 8 October 2026  
Correspondence janefather@gmail.com · Wonsik Choi ORCID 0009-0001-4263-9772

## A guide for readers from other fields

This paper turns one WRRA question into an explicit calculation. Can a system have no terminal edge, yet return an internal state differently after a complete circuit? We construct such a system, calculate its state change and show which parts depend on its connection rules and its present state.

Imagine a grid whose opposite sides are joined. On one pair of sides the joining reverses the order of the points. A path can continue across either joining without falling off an edge. Each grid point also carries a small matrix describing its internal state. The rules for moving that matrix from one point to another are specified separately from the grid. This separation matters: a shape alone does not determine every internal response.

A *holonomy* is the complete transformation produced by going around a loop. A *residue* here is the difference between the state before and after that loop, compared at the same point. A *gauge change* is a change of local coordinates used to describe the same states and transformations. A *density matrix* is a positive matrix of trace one; it packages normalized state information. The *common carrier* is the state space on which WRRA's transformations and readouts act. Our two-channel matrices provide an explicit candidate internal transport module, not a measured two-dimensional physical space.

The result is precise but conditional. We obtain a boundaryless cell complex, consistent internal transport, a coordinate-independent measure of state mismatch, and an update rule that keeps states valid while decreasing a declared energy. A loop can give a nonzero mismatch, but it can also give zero. Going around twice can undo the mismatch. An ordinary torus can support the same mismatch under suitable internal rules. These controls identify what the proposed effect actually depends on. Connecting this energy to spacetime stress and gravity remains a further constitutive task.

## Abstract

We give an executable finite realization of the closure–transport–residue branch of WRRA. A rectangular cellulation with a reversed seam realizes a Klein bottle and supports an explicitly chosen flat orthogonal internal connection. Edge transport acts by conjugation on real two-channel density matrices. We prove gauge invariance of a based-loop mismatch and of a positive covariant difference energy, derive a weight response, and give a positivity-preserving relaxation with an energy monotonicity bound. Exact rational and finite-field incidence calculations distinguish the Klein and torus complexes; numerical controls distinguish a valid Klein connection, a flat torus connection with the same nonzero loop response, and an incompatible torus connection. A compatible mixed state has zero response, and repeated reflection reverses the single-loop change. For generic rotation holonomy and strictly positive edge weights, the mixed state is the unique zero-energy density field on one connected sheet. The construction therefore supplies a testable state-level interface and rules out topology alone as a source of compulsory persistent stress. The finite-source counts of paper A label an optional multi-sheet realization; they do not derive this topology, internal fiber dimension or gravitational field equations.

## 1 Inputs and the WRRA construction

The predecessor proposed global closure, distributed connection, holonomy, present-state residue and gravitational interpretation [1]. Original executive paper B expressed that chain schematically. This revision supplies a cell complex, edge maps, states, observables and an update. Standard mapping-torus and connection-Laplacian ideas [2,3] are acknowledged; the contribution is their specified WRRA assembly, exact interfaces and executable controls, not a new theorem about the Klein bottle itself.

**Inputs.** Choose integers $m,n\geq3$, an internal angle $\phi$, positive edge weights $c_e$, a scale $\kappa>0$, and present-state matrices $\rho_v$. The audit uses $m=5$, $n=7$, $\phi=0.7$ radians, $\kappa=1$ in model units, and declared pseudorandom states and weights. These are construction choices, not calibrated astronomical data.

**Transformation.** Glue the grid, assign internal transport, transport the state, compare it at a common location, aggregate covariant edge differences, and update the same state. **Outputs** are incidence relations, holonomy, loop mismatch, energy, weight response and relaxation. **Failure criteria** appear in Section 8. Existing verified calibrations can subsequently enter a physical rendering rule without changing the status of the mathematical construction. This paper does not perform such a fit.

## 2 Joining the grid without a terminal edge

Let $S^1=\mathbb R/\mathbb Z$ and define

$$K=([0,1]\times S^1)/((1,y)\sim(0,-y)).$$

This mapping torus of reflection is the Klein bottle [2]. Ordinary gluing with $y$ unchanged gives a torus. Compactness implies bounded diameter in any compatible metric, not finitely many points. A finite cellulation has finitely many cells but its geometric realization still contains continuously many points. Our later matrix model has finitely many components, also with continuous state values. None of these notions is identified with a finite number of possible universe states.

Use vertices $(i,j)$ with $0\leq i<m$, $j\in\mathbb Z_n$. Directed edges are

$$a_{ij}:(i,j)\longrightarrow\begin{cases}(i+1,j),&i<m-1,\\(0,-j),&i=m-1,\end{cases}\qquad b_{ij}:(i,j)\longrightarrow(i,j+1).$$

For $i<m-1$, the oriented face boundary is $a_{ij}+b_{i+1,j}-a_{i,j+1}-b_{ij}$. On the seam it is $a_{m-1,j}-b_{0,-j-1}-a_{m-1,j+1}-b_{m-1,j}$. All $j$ indices are modulo $n$, including corner faces.

**Proposition 1.** This quotient cellulation is a connected closed surface with $V=mn$, $E=2mn$, $F=mn$ and Euler characteristic zero. Its rational Betti numbers are $(1,1,0)$; over $\mathbb F_2$ they are $(1,2,1)$.

**Proof.** The circle direction has already been joined, and the two remaining boundary circles of the cylinder are glued by a homeomorphism. Interior points and glued points have disk neighborhoods, so no terminal boundary remains. The grid is connected. Each edge has two incident faces and the displayed oriented boundaries satisfy $\partial_1\partial_2=0$. A consistent orientation transported across the reversed seam returns with the opposite sign, so the surface is nonorientable. More explicitly, a rational 2-cycle assigns coefficients to faces: interior cancellations propagate a common coefficient, while the seam requires it to equal its negative. It is therefore zero. Over $\mathbb F_2$, all equal coefficients give a one-dimensional 2-cycle space. Connectedness gives $b_0=1$, and the Euler relation gives the remaining Betti numbers. Ordinary torus gluing instead has rational Betti numbers $(1,2,1)$. ∎

These are properties of the specified state-space geometry, not an inference about the observed topology of three-dimensional space. The drawn seam is a choice of fundamental domain rather than a physical wall.

## 3 Moving internal states on that grid

For a directed edge $e:u\to v$, $U_e$ maps the internal fiber at $u$ into that at $v$. Set

$$J=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad R(t)=\begin{pmatrix}\cos t&-\sin t\\\sin t&\cos t\end{pmatrix},\quad Q=R(\phi/n).$$

Choose $U_b=Q$, $U_a=I$ on ordinary horizontal edges, and $U_a=J$ at the reversed seam; reverse transport uses $U_e^{-1}=U_e^T$. This is an internal rank-two orthogonal bundle with connection. It is not being identified with the tangent bundle or a Levi-Civita connection. In particular $\phi$ is extra internal data, not fixed by the quotient.

**Proposition 2.** Every face has identity transport. The horizontal loop at $j=0$ has holonomy $A=J$, the vertical loop has $B=R(\phi)$, and $ABA^{-1}=B^{-1}$.

**Proof.** Products act on column states in traversal order, with the latest map on the left. Interior faces give $Q^{-1}Q=I$. A seam face gives $Q^{-1}JQ^{-1}J=I$, since $JR(t)J=R(-t)$. The marked horizontal loop meets the seam once at the reflection-fixed row $j=0$, giving $J$; the vertical loop gives $Q^n$. The stated group relation follows directly and agrees with the mapping-torus relation [2]. ∎

The connection is locally flat despite its nontrivial global holonomy. A display with identity maps on ordinary horizontal edges is convenient; changing local frames distributes the same transport among edges. Flatness is not a claim of zero or nonzero physical spacetime curvature.

A finite common-carrier realization is $\mathcal H=\bigoplus_{v\in V}\mathbb R^2$. Local state matrices satisfy $\rho_v=\rho_v^T\succeq0$ and $\operatorname{tr}\rho_v=1$. For explicit global normalization we choose $\sigma=|V|^{-1}\bigoplus_v\rho_v$, a positive trace-one state on $\mathcal H$. The local matrices are conditional blocks. This uniform block weight is a declared bookkeeping choice, not the nonuniform arithmetic measure of paper A. Orthogonal conjugation $\mathcal U_e(X)=U_e XU_e^T$ transports them. The linear cochain space uses $\operatorname{Sym}(2)$; the normalized positive states form a convex subset of the trace-one affine hyperplane, not a vector space. Define $(d_U^0\rho)_e=\rho_v-\mathcal U_e(\rho_u)$. Summing these differences around a face after transporting each contribution to a common corner telescopes to $\rho-\mathcal U_{\partial f}(\rho)=0$ up to the chosen orientation. Thus the covariant boundary-of-boundary test also closes. The audit implements this telescoping sum explicitly.

## 4 What remains after a loop

For a marked loop $\gamma$ based at $v$ with holonomy $W_\gamma$, define

$$D_\gamma(\rho_v)=\|W_\gamma\rho_vW_\gamma^T-\rho_v\|_F^2.$$

**Proposition 3.** Under independent orthogonal frame changes $G_v$, with $\rho'_v=G_v\rho_vG_v^T$ and $U'_e=G_vU_eG_u^T$, $D_\gamma$ is unchanged. Moreover $0\leq D_\gamma\leq2$ and it vanishes exactly when the state commutes with $W_\gamma$.

**Proof.** Intermediate frames cancel in the loop product, leaving $W'_\gamma=G_vW_\gamma G_v^T$. The matrix difference is conjugated by $G_v$, preserving Frobenius norm. Both compared matrices are positive and trace one, with squared norm at most one and nonnegative mutual trace; their squared distance is at most two. Vanishing is equality under conjugation, equivalently commutation. ∎

This is a state-and-marked-loop observable invariant under frame changes. It is not a scalar determined by topology alone. Changing the physical state or loop may change it. For $\rho=\left(\begin{smallmatrix}a&q\\q&1-a\end{smallmatrix}\right)$, reflection gives $D_A=8q^2$. Thus $q=1/4$, $a=1/2$ gives $D_A=0.5$, the aligned mixed state $I/2$ gives zero, and $q=1/2$, $a=1/2$ gives the maximum two. Since $J^2=I$, two horizontal circuits return the state exactly. This reversible mismatch is not irreversible stored history or automatic accumulated dissipation.

**Torus controls.** A torus requires commuting generator holonomies. It can carry $A=J$, $B=I$, giving exactly the same $D_A=0.5$ on the same state. Hence nonzero residue does not diagnose nonorientable base geometry. Conversely $J$ and $R(0.7)$ do not commute; installing the same seam maps on the ordinary torus produces nonidentity face transport. That is an invalid *flat* torus assignment, not an inconsistent torus or a ban on curved connections. The comparison tests the declared flat representation.

## 5 Energy and a valid state update

For one chosen orientation of each undirected edge, define the energy

$$E[\rho,U,c]=\frac{\kappa}{2}\sum_e c_e\|\rho_v-U_e\rho_uU_e^T\|_F^2.$$

**Proposition 4.** This energy is nonnegative, independent of edge orientation, and gauge invariant. At fixed states and connection,

$$\frac{\partial E}{\partial c_e}=\frac{\kappa}{2}\|\rho_v-U_e\rho_uU_e^T\|_F^2.$$

These statements follow from orthogonal invariance and the displayed linear dependence on $c_e$. The derivative is a scalar response to an edge coupling. It is not a spacetime stress tensor: no spacetime metric variation, volume conversion or gravitational coupling has been supplied. If $c_e$ and $\rho$ are dimensionless, $\kappa$ sets the energy unit; the audit fixes that unit rather than fitting a physical stiffness.

Let $d_v=\sum_{u\sim v}c_{uv}$ and $d_{\max}=\max_v d_v$. A declared relaxation rule is

$$\rho'_v=(1-\eta d_v)\rho_v+\eta\sum_{u\sim v}c_{uv}U_{vu}\rho_uU_{vu}^T,\qquad 0\leq\eta\leq d_{\max}^{-1}.$$

**Proposition 5.** This update preserves positivity and trace one, commutes with frame changes, and does not increase $E$.

**Proof.** The update is a convex combination of normalized positive matrices, establishing state validity. Conjugation gives covariance term by term. On the direct sum of symmetric matrices, let $L_U$ be the weighted connection Laplacian, so $E=(\kappa/2)\langle\rho,L_U\rho\rangle$ and the update is $\rho'=\rho-\eta L_U\rho$. The operator is self-adjoint and positive. The inequality $\|X-Y\|_F^2\leq2\|X\|_F^2+2\|Y\|_F^2$ gives $\lambda_{\max}(L_U)\leq2d_{\max}$. Each energy eigencomponent is multiplied by $(1-\eta\lambda)^2\leq1$. ∎

This is gradient relaxation with the energy scale absorbed in the step parameter. For $0<\eta<1/d_{\max}$, all positive-eigenvalue components decay. If every grid edge has positive weight and $\phi\notin\pi\mathbb Z$, a zero-energy field must be parallel and its base density must commute with both $J$ and $R(\phi)$. The first condition makes it diagonal and the second makes its diagonal entries equal. Trace one therefore gives the unique zero-energy field $\rho_v=I/2$. Consequently this unforced model relaxes toward zero energy. Persistent twist stress would need specified driving, constraints or a different dynamics; nonorientability alone does not provide it. Zeroing cycle weights or using exceptional angles changes this conclusion.

## 6 Connection to the finite source and physical calculations

Paper A fixes a conditional source with $L=500$, $H=29$, $C=70$ and $N=LHC=1,015,000$ [4]. Its count does not determine a topology. One explicit optional assignment uses $m=C$, $n=L$, with $H$ spectator sheets indexed by $h$. Identify $i=z$, $j=\ell$ and serialize by $n_{\mathrm{code}}=1+\ell+L(h+Hz)$. There are $N$ vertices, $2N$ edges and $N$ faces in this disjoint union. The audit verifies the seam permutation on all 35,000 vertices of one sheet; the same map acts independently on every $h$.

This assignment realizes the earlier seam rule in the inherited `phase_bridge.py`: increasing $z$ through its end reverses $\ell$. After $C$ steps, $\ell$ reverses; after $2C$ steps it returns. It adds cells and internal transport to that permutation. The 29 sheets are bookkeeping sectors, not a proven connected universe. No adjacency among sheets, compressed 128-dimensional carrier representation, or physical dimension follows from this assignment.

A necessary interface correction concerns address 1. Paper A excludes it from active arithmetic weighting. A single $z$ step maps it to code 14,501, so the active subset is not closed under the full geometric step. We retain address 1 as a geometric vertex with an inactive arithmetic role; deleting it and incident cells would change the complex. Our transport update is a separate candidate module and is not asserted to preserve the published arithmetic filter or its active subset. The optional $2N$-component realization is not the minimal carrier dimension claimed or required by WRRA.

The legitimate output interface is an explicit present-state energy and its declared responses, which a later WRRA readout may use. Identifying these with a dark-sector energy density requires a unit and volume map; deriving pressure requires a volume or metric dependence; deriving gravity requires a covariant source and consistency with conservation. The existing cosmological and galactic functions are not replayed with this new energy because that coupling has not been specified. Earlier successful downstream calculations do not validate a missing coupling. Conversely, requiring a new independent numerical prediction is not necessary to assess the internal consistency demonstrated here.

## 7 Reproduction and controls

Run `python audit_B.py` with NumPy 2.3.5; the released run uses Python 3.12.14. No network, source data download or parameter fitting is performed. Exact integer incidence, rational elimination and elimination modulo two establish the finite combinatorial checks. Trigonometric transport and matrix updates are floating-point checks with tolerances recorded in code. `evidence/results.json` records inputs, outputs, versions and the audit source hash.

| Quantity | Declared result or control |
|---|---|
| Small cellulation | 35 vertices, 70 edges, 35 faces |
| Klein Betti numbers over rational numbers | 1, 1, 0 |
| Klein Betti numbers modulo two | 1, 2, 1 |
| Torus Betti numbers over rational numbers | 1, 2, 1 |
| Reflection mismatch for the test density | 0.5 |
| Same density on a flat torus with internal reflection | 0.5 |
| Mixed-state mismatch and double-loop mismatch | 0 and 0 |
| Largest possible density mismatch | 2 |

In the released run, maximum face-identity error is $6.41\times10^{-18}$, covariant telescoping error $3.33\times10^{-16}$, energy frame-change error $3.56\times10^{-15}$, and update covariance error $2.23\times10^{-16}$ or smaller. The coupling derivative differs from its central finite difference by $1.60\times10^{-10}$ or less. After 1,000 steps with $\eta=0.1750046189721454$, energy decreases from 24.5580160949 to $4.07490\times10^{-10}$ model units; trace error stays below $3.96\times10^{-14}$ and the minimum eigenvalue over updated states is 0.1402661853. These are generated model calculations, not observations.

The additional audit checks face flatness, covariant telescoping, local-frame invariance of loop response, energy and update, a finite-difference coupling derivative, positivity and trace through 1,000 updates, energy monotonicity, and full-sheet seam inversion and return. The torus with noncommuting holonomies is a deliberately failing flatness control. `evidence/results.json` supplies all measured numerical errors rather than treating tolerance success as an exact proof.

## 8 Failure criteria and conclusion

The construction fails if an edge has an unpaired boundary in the declared cellulation, a face boundary does not close, the incidence composition is nonzero, or the finite homology disagrees with the stated quotient. The chosen flat connection fails if face products or its generator relation fail. A readout fails if simultaneous frame changes alter it; the proposed dynamics fails if allowed steps violate positivity, normalization or monotonicity. A claim of compulsory persistent stress is already refuted within this model by the mixed state and the relaxation result. A future physical coupling must expose its units, stress definition and conservation conditions before astronomical agreement can test that coupling.

The revised B establishes a concrete closure–transport–state-response module. It retains the WRRA program of explaining physical outputs through a shared present state while assigning each statement its actual mathematical or physical responsibility. Geometry, internal transport, initial state, update and gravitational interpretation are separately specified. This separation makes their connection reproducible and makes the remaining physical questions precise.

## References

[1] Choi, W. *Finite but Boundaryless*, version 1.0 (2026). https://github.com/Wonsik-Choi-janefather/wrra-finite-boundaryless-twist-cosmology. Original executive B is preserved in the accompanying `sources` directory.

[2] Evans, J. *Fundamental group of a mapping torus*, lecture 5.03. https://jde27.uk/tg/vkt03.html. Consulted 8 October 2026. Used for the standard quotient and group presentation.

[3] Singer, A. and Wu, H.-T. *Vector Diffusion Maps and the Connection Laplacian*. Communications on Pure and Applied Mathematics 65 (2012), 1067–1144. https://doi.org/10.1002/cpa.21395. Background on orthogonal transport and connection Laplacians; no theorem about WRRA is attributed to this work.

[4] Choi, W. and Choi, J. *Constructing and testing the WRRA model: from a finite set of numbers to physical quantities*, executive paper A, version 1.0 (2026). https://doi.org/10.5281/zenodo.23235447.

[5] Choi, W. and Choi, J. *Minimal Computing Cosmology 3.0* (2026). https://doi.org/10.5281/zenodo.23202732. Inherited seam implementation is included as provenance, not as this revision's new dynamical law.
