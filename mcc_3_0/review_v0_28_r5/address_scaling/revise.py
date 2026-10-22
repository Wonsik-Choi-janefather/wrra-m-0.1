from pathlib import Path
import json, math, hashlib
root=Path(__file__).resolve().parent
ko=r'''
### 38.B 주소 수, 상태 공간, 물리적 해상도의 구분

**검증 입력.** 이 절은 37–38장의 유한 SOURCE 구성, 85장의 주소–운반자 상태, 139.3절의 스케일링 실행을 연결한다. 선언한 유리수 몫에서 얻은 $L=500$, 하모닉 장부의 $H=29$, 선택한 제타 높이 아래의 $C=70$을 사용한다. 따라서 $N_U=LHC=1,015,000$은 이 입력과 선택 규약에 조건부인 주소 수다. 관측값의 무한 정밀도나 우주 크기의 직접 측정값이라는 뜻이 아니다.

**WRRA 고유 변환.** $L,H,C$는 각각 기존 산술·하모닉·스펙트럼 구성의 인덱스이며, 세 공간 방향의 길이나 최소 공간 셀 수가 아니다. 주소 직렬화는 기존 식 $n=1+\ell+L[h+H(z-1)]$을 따른다. 다음 수량을 구별한다.

| 수량 | 의미 및 범위 |
|---|---|
| $N_U=1,015,000$ | 진공 기준 주소 1을 포함한 SOURCE 주소 수 |
| $N_{act}=N_U-1=1,014,999$ | 주소 2부터 시작하는 활성 주소 영역; 특정 사례에서 점유한 부품 수와 다름 |
| $d=128$ | 85장 수치 예에서 선택한 운반자 차원 |
| $N_{grid}=m^3$ | 139.3절의 정육면체 수신 격자를 일반화한 공간 표본 수 |
| $\ell_{ref}$, $h_{phys}=\ell_{ref}/m$ | 별도로 지정·보정하는 물리 영역 길이와 격자 간격 |

85장의 $\Omega=\sum_n w_n|n\rangle\langle n|\otimes\rho_n$는 주소별 운반자 블록을 가진 상태다. 해당 활성 주소–운반자 표현의 기저 차원은 $(N_U-1)d=129,919,872$이다. 이는 가능한 우주 전체 상태의 개수가 아니며, 독립 공간 셀마다 상태를 복제한 텐서곱의 차원도 아니다. 연속적인 가중치와 밀도행렬의 정밀도를 별도로 제한하지 않으면 유한 주소만으로 모든 상태의 정보량이 유한 비트로 결정되지 않는다.

물리 단위는 다음과 같이 분리한다. 단위 정육면체 좌표 $\boldsymbol\xi\in[0,1)^3$에서

$$\mathbf x=\ell_{ref}\boldsymbol\xi,\qquad h_{phys}=\ell_{ref}/m,\qquad V_j=h_{phys}^3.$$

$\ell_{ref}$는 해당 수신 문제의 기준 길이 또는 관측 보정으로 정해야 한다. $N_U$만으로 우주 반경이나 최소 길이가 산출되지는 않는다. 격자 세분화는 같은 SOURCE 장부를 더 세밀하게 표현하는 연산이며, 각 셀에 독립 SOURCE 자원을 새로 생성하는 연산이 아니다.

**산출값과 장부 연결.** 다음은 물리적 배정 법칙의 추가 증명이 아니라, 이미 정의된 가산적 에너지 장부를 격자에 전달할 때 요구하는 보존 인터페이스다. 원천 에너지 $E_n$과 비음수 전달 계수 $K_{jn}$가 주어지고 각 원천에 대해 $\sum_jK_{jn}=1$이면

$$E_j=\sum_nK_{jn}E_n,\qquad u_j=E_j/V_j,\qquad \sum_j u_jV_j=\sum_nE_n.$$

표현형에 참여하지 않은 자원은 별도 예비 장부에 포함하여 마지막 등식의 합산 범위를 완성한다. 예비 장부에는 임의의 공간 부피나 밀도를 부여하지 않는다. 정규화 가중치만 제공된 경우에는 에너지 기준량과 부피가 추가로 필요하며, 가중치를 곧바로 에너지로 읽지 않는다. 개별 원천 에너지가 정의되지 않은 집계 항목은 집계 상태로 유지한다. 이 인터페이스를 전 우주 코드에 통합했다는 뜻은 아니다.

**반증조건.** 격자 수를 바꾸면서 총량이 증가하거나, 예비 항목을 제외한 합을 전체 장부와 같다고 보고하거나, 물리 길이 입력 없이 미터 단위 크기를 제시하면 이 구분을 위반한다. $L,H,C$ 또는 제타 절단 규약을 바꾸면 주소 수를 다시 계산해야 한다.

**결론.** $1,015,000$은 선언된 유한 SOURCE의 주소 용량이다. 공간 해상도는 수신 문제의 $\ell_{ref}$와 $m$으로 정한다. 실제 공간 매핑 및 물리 보정은 해당 수신 모듈의 추가 계약이며, 주소 수 하나가 우주 전체 상태 수나 공간 최소 셀을 확정하지 않는다.

'''
en=r'''
### 38.B Address count, state space, and physical resolution

**Verification inputs.** This section connects the finite SOURCE construction in Chapters 37–38, the address–carrier state in Chapter 85, and the scaling execution in Section 139.3. The declared rational shares give $L=500$, the harmonic ledger supplies $H=29$, and the selected zeta-height cutoff gives $C=70$. Thus $N_U=LHC=1,015,000$ is an address count conditional on these inputs and conventions, not an infinitely precise observation or a direct measurement of cosmic size.

**WRRA-specific transformation.** The indices $L,H,C$ belong to the arithmetic, harmonic, and spectral construction. They are neither three spatial lengths nor counts of minimum spatial cells. Serialization retains $n=1+\ell+L[h+H(z-1)]$.

| Quantity | Meaning and scope |
|---|---|
| $N_U=1,015,000$ | SOURCE addresses, including vacuum reference address 1 |
| $N_{act}=N_U-1=1,014,999$ | Active address domain beginning at 2; not the occupied component count in a particular case |
| $d=128$ | Carrier dimension selected in the numerical example of Chapter 85 |
| $N_{grid}=m^3$ | Spatial samples in a cubic receiver generalizing Section 139.3 |
| $\ell_{ref}$, $h_{phys}=\ell_{ref}/m$ | Separately specified or calibrated physical domain length and grid spacing |

The Chapter 85 state $\Omega=\sum_n w_n|n\rangle\langle n|\otimes\rho_n$ has address-indexed carrier blocks. The active address–carrier basis dimension is $(N_U-1)d=129,919,872$. This is not the number of possible global universe states, nor the dimension of a tensor product of independent spatial-cell copies. Without an additional precision constraint on continuous weights and density matrices, finite addresses alone do not fix the information in every state to a finite number of bits.

For unit-cube coordinates $\boldsymbol\xi\in[0,1)^3$, separate physical units as

$$\mathbf x=\ell_{ref}\boldsymbol\xi,\qquad h_{phys}=\ell_{ref}/m,\qquad V_j=h_{phys}^3.$$

The receiver must specify or observationally calibrate $\ell_{ref}$. Neither a cosmic radius nor a minimum length follows from $N_U$ alone. Refinement resolves the same SOURCE ledger more finely; it does not create a new independent SOURCE budget in every cell.

**Outputs and ledger connection.** The following is a conservation interface for transporting already-defined additive ledger energies, not a newly established physical allocation law. Given source energies $E_n$ and nonnegative transfer coefficients $K_{jn}$ with $\sum_jK_{jn}=1$ for each source,

$$E_j=\sum_nK_{jn}E_n,\qquad u_j=E_j/V_j,\qquad \sum_j u_jV_j=\sum_nE_n.$$

Resources outside the phenotype remain in a separate reserve ledger, included in the total balance. No arbitrary spatial volume or density is assigned to that reserve ledger. Normalized weights require an additional energy scale and volume before they can represent an energy density. Aggregates without defined per-origin energies remain aggregates. This interface is not claimed to be integrated into an executable model of the entire universe.

**Falsification conditions.** Increasing the total budget merely by increasing grid count, omitting reserves while claiming a complete balance, or assigning metre-scale sizes without a physical length input violates this distinction. Changes to $L,H,C$ or the zeta cutoff require recalculating the address count.

**Conclusion.** The value $1,015,000$ is the capacity of the declared finite SOURCE address domain. Receiver resolution is set by $\ell_{ref}$ and $m$. Spatial mapping and physical calibration are additional receiver contracts; address count alone fixes neither the global state count nor a minimum spatial cell.

'''
ko2=r'''
### 139.3.1 물리 단위 복원과 해상도 선택

38.B절의 구분에 따라, 이 절의 $1024$개 프로파일 표본과 $16^3,32^3,64^3,128^3$ 수신 격자는 $N_U$와 다른 수량이다. 기존 계산은 무차원 수신 문제의 보존·수렴을 검사한다. 물리 단위 복원에는 별도 기준 길이와 밀도가 필요하다. 질량 밀도 섭동 $\delta\rho=\rho_{ref}\widehat{\delta\rho}$에 대해

$$\Phi=4\pi G\rho_{ref}\ell_{ref}^2\widehat\Phi,\qquad \Delta_{\xi}\widehat\Phi=\widehat{\delta\rho},$$
$$\mathbf g=-4\pi G\rho_{ref}\ell_{ref}\nabla_{\xi}\widehat\Phi.$$

이는 표준 Poisson 식의 단위 복원이며, $\rho_{ref}$나 $\ell_{ref}$를 SOURCE 주소 수에서 새로 유도한 결과가 아니다. 에너지 밀도를 질량 밀도로 바꾸려면 해당 항에 적용되는 $\rho=u/c^2$ 계약을 별도로 명시해야 한다.

불균일 셀에서도 보존되는 평균은 $\bar u_J=(\sum_{j\in J}V_ju_j)/(\sum_{j\in J}V_j)$이다. 같은 물리 영역에서 격자를 세분화할 때 총 에너지는 일정하다. 반면 같은 에너지를 유지하면서 실제 영역 길이를 $a$배로 늘리면 부피는 $a^3$배, 평균 밀도는 $a^{-3}$배다. 이것은 단순한 단위 표기 변경과 다르다.

앞 절의 Poisson 역연산자 모드별 충분조건에서 상대오차 한계 $\delta$를 요구하면 $h_{phys}|k|\le\sqrt{12\delta/(1+\delta)}$를 택할 수 있다. 따라서 $\delta=0.01$일 때 해당 모드 파장당 적어도 $18.228458$개 셀이라는 보수적 기준을 얻는다. 이는 모드별 이산화 경계이며 관측 피팅 오차의 보증이 아니다. 미해상 고주파와 aliasing은 별도 검사한다.

이번 개정에서 기존 finite_scale_bridge_v0_1을 다시 실행하여 내부 검사 179/179와 별도 modal/Parseval 검증 통과를 확인했다. 추가 scale_contract.py는 주소 직렬화, 단위 복원과 보존 인터페이스를 검사한다. 추가 검사는 명시된 구현 규약의 검사이며, 실제 우주 크기 측정이나 전 3.0 실행 검증을 뜻하지 않는다.

'''
en2=r'''
### 139.3.1 Physical units and resolution selection

Under Section 38.B, the $1024$ profile samples and the $16^3,32^3,64^3,128^3$ receiver grids are distinct from $N_U$. The existing computation tests conservation and convergence of dimensionless receiver problems. Physical units require a separate reference length and density. For a mass-density perturbation $\delta\rho=\rho_{ref}\widehat{\delta\rho}$,

$$\Phi=4\pi G\rho_{ref}\ell_{ref}^2\widehat\Phi,\qquad \Delta_{\xi}\widehat\Phi=\widehat{\delta\rho},$$
$$\mathbf g=-4\pi G\rho_{ref}\ell_{ref}\nabla_{\xi}\widehat\Phi.$$

These are unit-restoration identities for the standard Poisson equation, not a new derivation of $\rho_{ref}$ or $\ell_{ref}$ from address count. Converting energy density to mass density requires an explicit applicable $\rho=u/c^2$ contract for that term.

For unequal cells the conservative average is $\bar u_J=(\sum_{j\in J}V_ju_j)/(\sum_{j\in J}V_j)$. Refining a fixed physical domain preserves total energy. Enlarging the actual domain length by $a$ at fixed energy instead multiplies volume by $a^3$ and mean density by $a^{-3}$. This differs from changing the units used to describe the same physical domain.

The preceding per-mode inverse-Poisson bound gives the sufficient condition $h_{phys}|k|\le\sqrt{12\delta/(1+\delta)}$ for relative error tolerance $\delta$. For $\delta=0.01$, the conservative requirement is at least $18.228458$ cells per wavelength of that mode. This is a mode-wise discretization bound, not a guarantee of observational fitting accuracy. Unresolved high frequencies and aliasing require separate checks.

For this revision, finite_scale_bridge_v0_1 was rerun: 179/179 internal checks and the independent modal/Parseval verification passed. The added scale_contract.py checks serialization, unit restoration, and the conservation interface. These additional checks test explicit implementation conventions, not a measured cosmic size or an execution validation of all MCC 3.0.

'''
b=root/'book_v0_28_r2'
for lang,a,c in [('KO',ko,ko2),('EN',en,en2)]:
 p=b/f'MCC_3_0_Full_Book_{lang}_v0.28-r1.md'; s=p.read_text()
 lines=s.splitlines(); lines[2]=('## 개정판 v0.28-r2: 유한 주소와 물리 해상도 보완' if lang=='KO' else '## Revision v0.28-r2: finite addresses and physical resolution')
 lines.insert(6,('**v0.28-r2 준비본.** 38.B 및 139.3.1절을 추가했다. 이 개정본은 아직 별도 DOI로 출판하지 않았다. 아래 v0.28-r1 DOI는 이전 출판본을 가리킨다.\n' if lang=='KO' else '**Prepared revision v0.28-r2.** Sections 38.B and 139.3.1 are added. This revision has not been published under a separate DOI; the v0.28-r1 DOI below identifies the preceding publication.\n'))
 s='\n'.join(lines)+'\n'; marker='# 39장' if lang=='KO' else '# Chapter 39'
 i=s.index(marker); s=s[:i]+a+s[i:]; i=s.index('### 139.4.'); s=s[:i]+c+s[i:]
 (b/f'MCC_3_0_Full_Book_{lang}_v0.28-r2.md').write_text(s)
 p.unlink(); (b/f'MCC_3_0_Full_Book_{lang}_v0.28-r1.pdf').unlink(missing_ok=True)
(b/'review/render.sh').write_text((b/'review/render.sh').read_text().replace('v0.28-r1','v0.28-r2'))
