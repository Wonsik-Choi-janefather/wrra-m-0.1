# 최소계산 우주론 3.0
## 유한 SOURCE에서 입자·에너지·중력·우주 팽창까지의 통합 실행모형

Minimal Computing Cosmology 3.0  
Finite-Source Integrated Model: From a Generated Address Space to Components, Energy, Gravity and Cosmic Expansion

저자: 최원식 (Wonsik Choi), 최정인 (Jeongin Choi)  
날짜: 2026년 10월 7일  
상태: 6단계 계산 통합 PASS / 통합 과학모형 PASS-C  
ORCID: Wonsik Choi — 0009-0001-4263-9772

---

## 초록

최소계산 우주론(Minimal Computing Cosmology, MCC)은 우주가 무한한 상세정보를 미리 저장한 완성본이 아니라, 유한한 상태·관계·경계·잔여·자원 장부로 현재를 실행한다는 가설에서 출발한다. 버전 2.3.2는 SOURCE, 공통운반자, 차원필터, residue, phenotype, gravity/geometry를 하나의 소유권 구조로 정리했지만, 우리 우주에 특화된 수치모형 WRRA_M에서는 주소범위 N=1,000,000이 실용적 계산 cutoff로 남아 있었다. 따라서 “유한한 우주”라는 철학과 “유한한 SOURCE의 크기가 내부에서 생성되는가”라는 계산 사이에 한 칸의 공백이 존재했다.

본 연구는 이 공백을 WRRA_M의 기존 세 구조를 결합한 finite Klein–Zeta SOURCE 후보로 채운다. 채택된 산술 장부 0.05/0.268/0.682의 최소 정수 해상도에서 L=500, 기존 중성미자 harmonic ledger (0,5,29)에서 H=29, 유한 위상 경계 T=2πH 아래의 양의 비자명 Riemann-zeta 영점 수에서 C=70을 취한다. 선언된 후보 생성규칙

\[
N_U=LHC
\]

에 따라

\[
\boxed{N_U=500\times29\times70=1,015,000}
\]

을 얻는다. 이 값은 실험적으로 측정된 우주 상수가 아니라, 선언된 KZF 구성 아래에서 얻는 조건부 MCC/WRRA 예측이다.

새 SOURCE를 기존 WRRA_M 주소필터에 삽입하면 무보정 상태에서 장부가 5.000002539%/26.800001829%/68.199995632%로 유지된다. 기존과 동일한 두 산술 보정 자유도 α와 h만 다시 고정하면 5%/26.8%/68.2%가 수치정밀도 안에서 다시 닫힌다. 그 상태를 component/phenotype, 정보부하, SI 에너지, 압력, 중력, 은하회전, 조건부 렌즈, 우주팽창으로 연속 전달했다. SI 응답계수와 국소 중력 응답을 재보정하지 않은 현재 기준 결과는

\[
q_0=-0.5285585894,
\]

\[
a_T=1.1917875314\times10^{-10}\ {\rm m\,s^{-2}},
\]

\[
v_{\rm ref}=207.5102419\ {\rm km\,s^{-1}},
\]

\[
\theta_{\rm lens}=0.5355822400''
\]

이며, 균일 constitutive branch의 가속전환 scale factor는

\[
a_{\rm trans}=0.6119598068
\]

이다.

MCC 3.0은 검증 입력 → WRRA 고유 변환 → 산출값 → 반증조건의 고정 규칙으로 작성되었다. 1–5단계의 54개 계산·구현 검증과 6단계의 11개 cross-stage 검사가 모두 통과했다. 다만 T=2πH, L,H,C의 독립성, N_U=LHC의 유일성, Klein형 closure의 물리적 필연성, particle-species decoder의 유일성, full spin/flavor/confinement/binding closure는 OPEN이다. 따라서 6단계 계산 통합은 PASS, 과학모형 전체는 PASS-C로 판정한다.

---

# 서문 — 하나의 전시에서 하나의 시작점으로

MCC 3.0의 직접적인 개념적 출발점은 물리학 논문이나 새로운 관측값이 아니었다. 서울 리움미술관에서 KOO JEONG A: OUSSSMOS를 보던 중, “한 지점에서 꺾이는 것이 아니라 전체 형상에 걸쳐 분포된 꼬임”이라는 이미지가 떠올랐다. 그 직관은 이후 선행연구 《Finite but Boundaryless: A WRRA Hybrid Expansion and Accumulated Twist Cosmology with Hidden Gravitational State》로 정리되었다 [1].

그 선행연구에서 뫼비우스 띠는 우주의 문자 그대로의 위상으로 제시되지 않았다. 뫼비우스 띠는 경계를 가지며 차원도 다르다. 대신 핵심은 다음 질문이었다.

> 우주가 유한하더라도 끝에 벽이 없어야 한다면, 상태는 어떻게 닫히고, 이동은 어떻게 다시 자기 자신으로 돌아오며, 그 과정에서 누적된 꼬임은 어떤 물리적 residue를 남기는가?

그때의 연구는

\[
\text{global closure}
\rightarrow
\text{distributed connection}
\rightarrow
\text{holonomy}
\rightarrow
\text{transport residue}
\rightarrow
\text{twist stress}
\rightarrow
\text{gravity}
\]

라는 구조를 제시했다 [1]. 이 전시는 과학적 증거가 아니며, 구정아 작가의 작품이 우주론을 증명하는 것도 아니다. 전시는 질문을 만든 개념적 계기였고, 이후의 식·계산·반증조건은 독립적으로 검토되어야 한다.

MCC 3.0은 바로 그 질문을 한 단계 더 위로 밀어 올린 결과다. “유한하지만 경계 없는 우주”를 말하려면 단순히 우주의 공간형태만 유한하다고 선언해서는 부족하다. 그 우주를 실행하는 SOURCE 자체도 유한하게 생성되어야 한다. 2.3.2와 WRRA_M까지는 이 요구를 알고 있었지만, 실제 주소공간은 N=1,000,000이라는 외부 cutoff를 사용했다. 3.0의 목표는 이 마지막 외부 상한을 내부 생성규칙으로 바꾸고, 그 시작점에서 기존 입자·에너지·중력·팽창 계산까지 한 번에 내려가는 것이다.

---

# 1. WRRA와 최소계산 원리

## 1.1 우주는 완성된 파일인가, 실행되는 현재인가

최소계산 우주론의 기본 질문은 단순하다. 우주가 미래의 모든 사건과 입자상태를 미리 저장해야 하는가, 아니면 현재 상태와 법칙에서 필요한 다음 상태만 생성하면 되는가?

MCC는 두 번째 입장을 모델 가정으로 선택한다. 우주는 “미래가 모두 기록된 데이터베이스”가 아니라 “현재를 통해 다음 현재를 계산하는 실행계”로 본다. 이 관점은 MCC 2.3.2에서 SOURCE–RELATION–BOUNDARY–RESIDUE–UPDATE–LEDGER 구조와 WRRA로 정리되었다 [2].

WRRA는 이 논문에서 다음 실행문법으로 사용한다.

\[
\boxed{
\text{SOURCE}
\rightarrow
\text{RELATION/FILTER}
\rightarrow
\text{RESIDUE}
\rightarrow
\text{RESOURCE/LEDGER}
\rightarrow
\text{ACTION/PHENOTYPE}
}
\]

SOURCE는 실행 가능한 상태의 원천, RELATION은 연결과 변환, BOUNDARY는 허용영역, RESIDUE는 현재에 남아 다음 상태에 영향을 주는 이력, LEDGER는 보존·이동·소유 자원의 장부다.

## 1.2 비특수성

MCC는 “우리 우주가 유일하게 특별한 수학적 대상으로 선택되어야 한다”는 요구를 두지 않는다. 고정된 생성법칙이 허용하는 가능한 실행 중 하나가 우리 우주일 수 있다. 따라서 목표는 “우리 우주만을 위해 만들어진 무한한 초기정보”가 아니라, 유한한 규칙으로 우리 우주의 관측구조를 재현할 수 있는가를 묻는 것이다.

## 1.3 수학적 무한과 물리적 실행의 구분

수학에서 무한집합과 극한은 필수적인 도구다. MCC 3.0은 이를 부정하지 않는다. 다만 물리적으로 한 번에 실현되어야 하는 SOURCE에 무한한 주소공간을 요구하지 않는다.

\[
\text{mathematical infinity}
\neq
\text{physically instantiated infinite SOURCE}.
\]

---

# 2. 왜 무한 SOURCE가 필요 없는가

WRRA_M은 이미 유한 주소

\[
n=2,\ldots,10^6
\]

을 사용했다 [3]. 그러나 10^6은 실행의 편의적 cutoff였다. 3.0에서는 이를 외부설정이 아니라 내부에서 생성되는 finite SOURCE 후보로 바꾸는 것이 핵심이다.

MCC 3.0의 시작점은 다음 조건을 만족해야 한다.

1. 유한해야 한다.
2. 주소를 생성할 수 있어야 한다.
3. 경계에서 단순 종료하지 않는 closure를 가질 수 있어야 한다.
4. 기존 WRRA_M filter와 접속 가능해야 한다.
5. 기존 검증값을 숨은 보정 없이 유지해야 한다.
6. 실패 시 어느 규칙이 실패했는지 분리할 수 있어야 한다.

---

# 3. Finite Klein–Zeta Generator

첫 번째 좌표는 산술 장부다.

\[
(0.05,0.268,0.682)
=
\left(
\frac{25}{500},
\frac{134}{500},
\frac{341}{500}
\right).
\]

따라서 최소 공통 정수 ledger resolution은

\[
\boxed{L=500}.
\]

두 번째 좌표는 기존 중성미자 harmonic ledger다.

\[
(n_1,n_2,n_3)=(0,5,29)
\]

에서

\[
\boxed{H=29}.
\]

세 번째 좌표는 finite zeta-focus count다. 위상 경계를

\[
T_H=2\pi H
\]

로 선언하면

\[
T_H=182.212373908208.
\]

이 경계 안의 양의 비자명 zeta zero는 70개이고,

\[
\gamma_{70}=182.20707848436646,
\]

\[
\gamma_{71}=184.87446784838750
\]

이므로

\[
\boxed{C=70}.
\]

실행에서 무한 Dirichlet series 자체를 물리 SOURCE로 취하지 않기 위해 M=LH=14,500에서 잘린 Euler–Maclaurin surrogate를 사용한다.

\[
\zeta_M(s)=
\sum_{n=1}^{M-1}n^{-s}
+\frac{M^{1-s}}{s-1}
+\frac12M^{-s}
+\frac{s}{12}M^{-s-1}
-\frac{s(s+1)(s+2)}{720}M^{-s-3}.
\]

표준 첫 70개 영점 위치에서 최대 잔차는 약 5.29×10^-13이고 70번째에서 약 6.98×10^-14이다 [4].

단, 이 surrogate는 표준 zeta zero 위치의 유한 수치검산이다. 현재 구현은 finite surrogate 자체만으로 70개 zero를 독립적으로 처음부터 증명한 것이 아니다.

Klein형 closure는 schematic identification

\[
(-T,\theta)\sim(T,-\theta)
\]

으로 표현한다. 실제 4차원 시공간이 Klein bottle이라는 관측주장이 아니라, 유한 주소계의 끝을 terminal wall이 아닌 orientation-reversing return으로 구현하는 후보이다.

세 좌표의 product rule을 선언하면

\[
\boxed{N_U=LHC}
\]

이고

\[
\boxed{N_U=500\times29\times70=1,015,000}.
\]

---

# 4. 유한 정수 주소의 생성

세 좌표를

\[
0\le\ell<L,\qquad
0\le h<H,\qquad
1\le z\le C
\]

로 두고

\[
n=1+\ell+L[h+H(z-1)]
\]

로 직렬화하면

\[
1\le n\le1,015,000
\]

의 유한 정수 label이 생성된다.

label 1은 비활성 multiplicative/vacuum reference로 남기고 실제 주소필터는

\[
\boxed{n=2,\ldots,1,015,000}
\]

을 사용한다.

따라서 이 모형에서 정수는 무한 정수집합이 물리적으로 미리 놓여 있다는 가정이 아니라, 유한 product-state를 순서화한 실행주소다.

---

# 5. Prime/Composite Filter

주소 상태는

\[
w_n\propto n^{-\alpha}
\]

로 가중한다.

legacy 값은

\[
\alpha_0=1.8996876950554356.
\]

새 N_U에서 기존 α0,h0를 그대로 사용하면

\[
\phi=0.05000002538983289,
\]

\[
D=0.26800001828881304,
\]

\[
R=0.6819999563213559.
\]

N_U=1,015,000에서 주소 수는

- prime: 79,608
- even composite: 507,499
- odd composite: 427,892

이다.

odd composite에는 기존 WRRA_M의 8-frame zeta phase drive를 그대로 사용한다. candidate window에서 기존과 동일한 두 자유도만 다시 고정하면

\[
\boxed{\alpha_1=1.8996877935161325},
\]

\[
\boxed{h_1=1.4476744689338703}.
\]

β_eff는 세 번째 fit이 아니라 결과 readout이다.

\[
\boxed{\beta_{\rm eff}=0.8654567230719301}.
\]

최종 장부는

\[
\boxed{(\phi,D,R)=(0.05,0.268,0.682)}
\]

로 닫힌다.

---

# 6. Residue와 Component

주소 필터의 목적은 정수를 입자 이름으로 바로 바꾸는 것이 아니다.

\[
\text{address}\rightarrow\{\phi,D,R\}.
\]

MCC 3.0에서는 residue가 실패한 출력이 아니라 다음 상태에 영향을 줄 수 있는 실제 장부항이다.

Stage 3에서 finite SOURCE의 실제 phase-aware phenotype measure

\[
p_n\propto w_n e_\phi(n)
\]

를 Prime-Parts 조립에 전달했다. admitted odd-composite 주소는

\[
\boxed{427,892}
\]

개이고 phenotype 총가중치는 0.05다.

첫 15개 prime label을 사용하는 one-each cyclic assembly에서 기존의 조건부 neutron candidate labels {5,47}를 유지하면

- small-first: 0.12947198694
- large-first: 0.12715941170

이 된다.

두 order의 number distribution total-variation distance는

\[
0.20472100116
\]

이다. 따라서 산술분해는 실행되지만 순서만으로 유일한 물리 species decoder가 정해지지 않는다.

---

# 7. 입자와 표현형

기존 Prime-Parts/WRRA_M에는 16-channel 확장표가 있다. Standard-Model one-generation 15 Weyl components에 하나의 neutral extension을 둔다. 3세대에 대해 48 field/channel slots가 phenotype 내부 bookkeeping view로 사용된다.

Stage 3에서는 frozen charge table을 그대로 사용해 neutral motif를 다시 검증했다.

- proton-electron candidate motif: net charge 0
- neutron candidate motif: net charge 0
- electron-conjugate pair: net charge 0
- neutral channel: net charge 0

이는 charge compatibility test다. 이 motif가 실제 생성동역학의 유일한 해라는 뜻은 아니다.

세 quark의 완전 반대칭 color state는 norm 1을 유지하고, 8개 total color generator에 대해 numerical residual 0을 유지한다.

조건부 p/n/e decoder를 사용하면

small-first:

\[
f_n=0.12947198694,\qquad u/d=1.65641446069
\]

large-first:

\[
f_n=0.12715941170,\qquad u/d=1.66166981400.
\]

전하중성은 decoder 구조상 닫힌다. 그러나 baryon/lepton origin은 도출되지 않는다.

다음은 OPEN이다.

- full spin-flavor wavefunction
- confinement Hamiltonian
- binding-energy derivation
- unique hadron/species assignment
- sea/gluon completion

---

# 8. 정보부하와 에너지

Stage 4의 핵심은 component를 발견했다고 우주 에너지를 새로 더하지 않는 것이다.

cosmic additive ledger는 오직

\[
\boxed{\phi\oplus D\oplus R}
\]

이다.

주소응답은

\[
g_s(n)=1+\lambda_s\frac{\log n}{\log N_U},
\]

\[
(\lambda_\phi,\lambda_D,\lambda_R)=(0,0.25,0.1).
\]

address moment는

\[
\mu_s=\sum_n w_n e_s(n)g_s(n).
\]

finite SOURCE에서

\[
\boxed{
(\mu_\phi,\mu_D,\mu_R)
=
(0.0500000000000001,
0.278925610976744,
0.687742539854239)
}.
\]

SI 계수는 WRRA_M reference에서 한 번 보정된 값을 그대로 고정한다.

\[
\eta_\phi=7.561582499072265\times10^{-10},
\]

\[
\eta_D=7.285761328795971\times10^{-10},
\]

\[
\eta_R=7.646102818811323\times10^{-10}
\quad{\rm J\,m^{-3}}.
\]

기준부피 V0=1 m^3에서

\[
E_\phi=3.78079124953614\times10^{-11}{\rm J},
\]

\[
E_D=2.03218543006515\times10^{-10}{\rm J},
\]

\[
E_R=5.25855017259595\times10^{-10}{\rm J}.
\]

합은

\[
\boxed{
E_{\rm total}=7.668814727614716\times10^{-10}{\rm J}
}.
\]

Prime-Parts small-first, large-first, 48 field/channel slots는 모두 phenotype의 내부분해다. 한 view의 normalized component fraction을 c_j라 하면

\[
\mu_{\phi,j}=\mu_\phi c_j,
\]

\[
E_{\phi,j}=\eta_\phi\mu_{\phi,j}
\]

이고

\[
\sum_jE_{\phi,j}=E_\phi.
\]

따라서 internal view를 cosmic total에 다시 더하는 것은 금지된다.

---

# 9. 중력과 뒤틀림

구정아 전시에서 출발한 선행연구는 전체에 걸쳐 누적되는 꼬임을 twist stress의 개념적 owner로 제안했다 [1]. 이후 WRRA twist-stress 연구에서는 dark mass phenotype을 spatial stress의 중력적 표현으로 해석하고, 우주 규모 fraction과 은하 low-acceleration scale을 연결했다 [5].

MCC 3.0은 이 아이디어를 독립 force로 추가하지 않는다. 하나의 energy/load ledger에서 resident nonphenotype D가 국소 추가중력 response를 소유하도록 한다.

동결된 local clustering reference f_c=0.265에 대해

\[
a_{T,0}=cH_0\sqrt{\frac{f_c}{8}}
\]

를 기준으로 하고, candidate state에서는

\[
a_T
=
a_{T,0}
\sqrt{
\frac{\rho_D}
{u_{\rm crit}f_c}
}.
\]

현재 a=1에서

\[
\boxed{
a_T=
1.1917875313971119\times10^{-10}
\ {\rm m\,s^{-2}}
}.
\]

이 a_T 하나가 rotation과 lensing에 같이 들어간다.

---

# 10. 은하 회전과 렌즈

Stage 5에서는 동일한 finite-SOURCE D load를 Plummer reference source에 전달한다.

시험 source:

- mass: 6×10^10 M_sun
- scale radius: 3 kpc
- test radius: 8.2 kpc
- lens patch radius: 200 kpc
- impact: 10 kpc

현재 a=1에서 직접 baryonic rotation은

\[
161.4505105\ {\rm km\,s^{-1}}
\]

이다.

같은 a_T를 적용한 total reference rotation은

\[
\boxed{
207.5102419\ {\rm km\,s^{-1}}
}.
\]

동일한 중력 response를 조건부 finite-patch lens calculation에 넣으면

\[
\boxed{
0.5355822400''
}
\]

를 얻는다.

legacy N=1,000,000과의 차이는

\[
\Delta v=-6.63261\times10^{-4}\ {\rm km\,s^{-1}},
\]

\[
\Delta\theta=-4.27055\times10^{-6}''.
\]

이 값들은 새 astronomical measurement가 아니라 기존 동결 renderer가 새 finite SOURCE에서도 깨지지 않는지 보는 continuity output이다.

---

# 11. 우주 팽창

volume exponent는

\[
(n_\phi,n_D,n_R)=(0,0,3)
\]

으로 상속한다.

따라서

\[
\rho_\phi(a)=\frac{E_\phi}{a^3},
\]

\[
\rho_D(a)=\frac{E_D}{a^3},
\]

\[
\rho_R(a)=E_R.
\]

pressure는

\[
P_\phi=P_D=0,
\qquad
P_R=-\rho_R.
\]

total density에서

\[
\frac{H(a)}{H_0}
=
\sqrt{
\frac{\rho(a)}
{u_{\rm crit}}
}
\]

와

\[
q(a)
=
\frac12
\frac{\rho(a)+3P(a)}
{\rho(a)}
\]

를 계산한다.

| a | ρ J/m³ | H/H0 | q |
|---:|---:|---:|---:|
| 0.5 | 2.4540666613×10^-9 | 1.7888556123 | 0.1785814590 |
| 1.0 | 7.6688147276×10^-10 | 0.9999913260 | -0.5285585894 |
| 2.0 | 5.5598332420×10^-10 | 0.8514575347 | -0.9187161585 |

전환조건 q=0으로부터

\[
\boxed{
a_{\rm trans}=0.6119598067968817
}
\]

를 얻는다.

---

# 12. proper-time과 기록

WRRA_M 0.12는 event/order discreteness와 physical minimum time을 구분한다 [3]. MCC 3.0은 이 구분을 유지한다.

상속된 proper-time step은

\[
\Delta\tau
=
1.4813019664158691\times10^{-21}{\rm s}
\]

이다.

이 값은 Planck time이 아니며 우주의 절대 최소 시간이라고 주장하지 않는다.

finite carrier의 noncommuting update에서 내부 D/R load는 변하지만 전체 에너지는 수치정밀도 안에서 보존된다. KZF candidate의 최대 relative energy drift는

\[
\boxed{
9.99\times10^{-16}
}
\]

수준이다.

state trace도 1을 유지한다.

MCC는 현재 실행과 Record를 구분한다. 그러나 autonomous physical apparatus가 실제 irreversible record를 만드는 full measurement dynamics는 아직 3.0의 완료항목이 아니다.

---

# 13. End-to-End Master Ledger

MCC 3.0의 최종 실행사슬은

\[
\boxed{
\text{finite rule}
\rightarrow
\text{finite addresses}
\rightarrow
\text{prime/composite filter}
\rightarrow
\text{residue}
\rightarrow
\text{component/phenotype}
\rightarrow
\text{information load}
\rightarrow
\text{energy}
\rightarrow
\text{pressure/gravity}
\rightarrow
\text{rotation/lensing}
\rightarrow
\text{expansion}
}
\]

이다.

| 단계 | 소유 정보 | additive 여부 |
|---|---|---|
| finite SOURCE | L,H,C,N_U | 주소생성 |
| address filter | φ,D,R share | normalized partition |
| component views | prime/channel 내부구성 | nonadditive |
| SI ledger | Eφ,ED,ER | additive |
| pressure | same ER | derived |
| local gravity | same D density | derived |
| rotation/lensing | same a_T | derived |
| expansion | same sector densities | derived |

이 구조가 3.0의 핵심이다. 서로 다른 설명을 같은 우주에 적용한다고 해서 별도의 에너지나 중력을 다시 만들지 않는다.

---

# 14. 검증값 재현

legacy N=1,000,000 장부는

\[
(0.05,0.268,0.682)
\]

를 재현한다.

reference macro output은

\[
q_0=-0.52855,
\]

\[
v=207.5109051266\ {\rm km\,s^{-1}},
\]

\[
\theta=0.5355865106''
\]

였다.

MCC 3.0 finite SOURCE branch는

\[
q_0=-0.5285585894,
\]

\[
v=207.5102418659\ {\rm km\,s^{-1}},
\]

\[
\theta=0.5355822400''
\]

를 얻는다.

legacy 대비 현재값 상대변화는 대략

- q: 1.63×10^-5
- rotation: 3.20×10^-6
- lensing: 7.97×10^-6

이다.

repository에 공개된 검사는

- Stage 1: 5
- Stage 2: 7
- Stage 3: 16
- Stage 4: 12
- Stage 5: 14
- Stage 6 cross-stage: 11

로 총

\[
\boxed{65}
\]

개다.

모두 PASS다. 이는 65개의 독립 물리실험을 뜻하지 않고 계산, 구현, provenance, 장부 일치 검증의 합이다.

---

# 15. WRRA/MCC 예측값

## 15.1 finite SOURCE size

\[
\boxed{
N_U=1,015,000
}
\]

은 선언된 N_U=LHC 규칙을 고정한 뒤 산출한 미측정량이다. 따라서 현재 지위는 conditional MCC/WRRA prediction이다. 단, LHC의 유일성이 아직 OPEN이므로 fundamental constant로 확정하지 않는다.

## 15.2 acceleration-transition scale

현재 uniform constitutive branch에서

\[
\boxed{
a_{\rm trans}=0.6119598068
}
\]

이 나온다. 이는 frozen energy/pressure law의 derived output이다.

## 15.3 중성미자 absolute mass 후보의 상속

MCC 2.3.2에서 observation-guided harmonic ledger (0,5,29)를 고정한 후

\[
m_1=0,
\]

\[
m_2=8.62965\ {\rm meV},
\]

\[
m_3=50.05195\ {\rm meV},
\]

\[
\sum m_\nu=58.6816\ {\rm meV}
\]

를 frozen holdout prediction으로 기록했다 [2].

MCC 3.0은 이 값을 새로 도출한 것이 아니라 H=29를 finite SOURCE generator에 상속했다.

---

# 16. 열린 가정과 반증조건

다음은 OPEN이다.

1. T=2πH가 유일한 physical phase boundary인가?
2. L,H,C가 정말 독립 Cartesian coordinate인가?
3. N_U=LHC 외의 동일하게 단순한 closure가 있는가?
4. Klein형 orientation reversal이 실제 우주 topology와 관련있는가?
5. zeta-focus가 물리적 microscopic mechanism인가, 수학적 organizing rule인가?
6. Prime-Parts가 particle species를 유일하게 정하는가?
7. full spin/flavor/confinement/binding Hamiltonian을 WRRA 내부에서 닫을 수 있는가?
8. baryon/lepton asymmetry의 생성자가 무엇인가?
9. full covariant background + inhomogeneous perturbation theory가 가능한가?
10. autonomous measurement/record dynamics를 같은 ledger에서 닫을 수 있는가?

MCC 3.0은 다음 중 하나가 발생하면 수정되어야 한다.

- KZF가 frozen rule에서 N_U=1,015,000을 재현하지 못한다.
- finite SOURCE insertion 후 address effects가 음수 또는 불완전해진다.
- 동일한 두 arithmetic calibration으로 장부를 닫을 수 없다.
- 숨은 세 번째 fit이 필요해진다.
- component internal view가 추가 cosmic energy로 중복계상된다.
- same state에서 rotation과 lensing이 서로 다른 a_T 보정을 요구한다.
- proper-time update가 energy/trace를 보존하지 못한다.
- Stage 1–6 handoff가 서로 다른 값을 소유한다.
- 문서의 식과 실행코드가 다르다.
- OPEN으로 기록한 microscopic rule이 실제 계산을 위해 필수인데 일관된 closure를 제공할 수 없다.

필요한 계산이 정의되지 않으면 OPEN으로 남긴다. undefined를 PASS로 처리하지 않는다.

---

# 17. 결론

MCC 3.0의 목적은 새 숫자를 계속 추가하는 것이 아니었다. 지금까지 나뉘어 있던 두 연구를 하나로 닫는 것이었다.

첫 번째는 MCC 2.3.2와 WRRA_M이 만든

\[
\text{filter}
\rightarrow
\text{residue}
\rightarrow
\text{phenotype}
\rightarrow
\text{load}
\rightarrow
\text{gravity/expansion}
\]

의 하류 구조다.

두 번째는 유한하지만 경계 없는 우주라는 직관에서 발전한 KZF finite SOURCE다.

둘을 합치면

\[
\boxed{
\text{finite generator}
\rightarrow
\text{finite universe address space}
\rightarrow
\text{particle/component}
\rightarrow
\text{energy}
\rightarrow
\text{gravity}
\rightarrow
\text{galaxy}
\rightarrow
\text{cosmic expansion}
}
\]

이라는 하나의 실행사슬이 된다.

이제 MCC의 시작점은 “무한한 정수집합을 준다”가 아니다.

\[
\boxed{
\text{유한 생성규칙이 유한 주소를 만든다.}
}
\]

그 주소가 filter를 지나 residue와 phenotype을 만들고, 동일한 resource ledger가 물리적 에너지와 중력, 은하회전, 렌즈, 팽창으로 내려간다.

6단계 계산통합은 PASS다. 그러나 모형 전체는 PASS-C다. 그 이유는 실패가 아니라 정직하게 남겨둔 구조적 조건 때문이다. finite SOURCE의 곱법칙과 microscopic particle closure가 유일하게 도출되는 순간, 3.0의 조건부 시작점은 더 강한 법칙으로 승격될 수 있다.

구정아 작가의 전시에서 시작된 “전체에 분포된 꼬임”이라는 한 장면은 과학적 증거가 아니었다. 하지만 그 장면은 질문을 만들었다. “유한하지만 끝이 없는 구조가 물리적으로 가능하다면, 그 구조를 만드는 시작점도 유한해야 하지 않는가?” MCC 3.0은 그 질문에 대해 처음으로 실행 가능한 시작점 후보와 아래로 이어지는 전체 계산사슬을 함께 제시한다.

---

# 재현성

GitHub 기준 단일 entry point:

python -m pip install -r mcc_3_0/requirements.txt  
python mcc_3_0/reproduce_mcc_3_0.py

Stage 1은 provenance freeze이고 Stage 2–5를 순서대로 재실행한 뒤 Stage 6 cross-stage audit을 수행하도록 구성되어 있다.

현재 공개 repository audit에서는 Stage 1–5의 published results/verification/handoff를 다시 읽은 Stage 6 cross-check가 PASS했다. 별도의 clean machine에서의 complete replay는 독립 재현 단계로 남긴다.

---

# 참고문헌

1. Choi, W. (2026). Finite but Boundaryless: A WRRA Hybrid Expansion and Accumulated Twist Cosmology with Hidden Gravitational State, Version 1.0. GitHub repository: Wonsik-Choi-janefather/wrra-finite-boundaryless-twist-cosmology. 이 논문은 KOO JEONG A: OUSSSMOS, Leeum Museum of Art, Seoul을 과학적 증거가 아닌 개념적 영감의 출처로 명시한다.
2. Choi, W. (2026). Minimal Computing Cosmology 2.3.2: Integrated Model. Zenodo. DOI: 10.5281/zenodo.22733000.
3. Choi, W.; Choi, J. (2026). WRRA M Integrated Upstream–Downstream Model 1.0 r1. Zenodo. DOI: 10.5281/zenodo.23126800.
4. Choi, W.; Choi, J. (2026). WRRA_M Finite Klein–Zeta Generation Window v0.1. GitHub: Wonsik-Choi-janefather/wrra-m-0.1/upstream/finite_klein_zeta_window_v0_1.
5. Choi, W. (2026). Twist Stress Universe and the Mass Phenotype of Dark Matter. Zenodo. DOI: 10.5281/zenodo.22700557.
6. Choi, W. (2026). WRRA Spatial Twist Selection of Galactic Disk Planes and the Dark Mass Phenotype. Zenodo. DOI: 10.5281/zenodo.23003875.
7. Choi, W. (2026). WRRA Prime-Parts Rendering: Finite Assembly, Neutrality, Composition and Decay. Zenodo. DOI: 10.5281/zenodo.23128482.
8. NIST Digital Library of Mathematical Functions. Riemann Zeta Function: zeros and Euler–Maclaurin representations.
9. mpmath documentation. zetazero.

---

## 최종 판정

6단계 실행 통합: PASS

MCC 3.0 통합 과학모형: PASS-C

현재 finite SOURCE 후보:

\[
\boxed{N_U=1,015,000}
\]
