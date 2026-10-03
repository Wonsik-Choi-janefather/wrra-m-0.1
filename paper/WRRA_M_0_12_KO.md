# WRRA_M 0.12 고유시간 갱신과 유한 경계의 모드 스펙트럼

Wonsik Choi · 2026-10-03 · WRRA Core 1.0 / MCC 2.3.2 · CC BY 4.0

## 초록

0.11의 다섯 보정 입력과 전자 모드 23을 고정하고, 셔터 갱신을 각 시간꼴 경로의 고유시간에 연결한다. 평탄·가속·유한 약한 중력·균질 팽창 경로의 시계와 유한 접힘·공간 연산자의 스펙트럼을 실행한다. 갱신 위상에서 에너지를 복원할 때 필요한 정수 가지를 공개하고, 자유 연속 분산과 경계로 이산화된 모드를 함께 계산한다. 기존 SI 에너지 장부의 고정 부피 갱신은 정확한 시간 환산으로 이어지지만, 0.10의 느린 팽창 구성 시계는 그 SI 위상 시계와 불일치한다. 이 실패를 보존하고 완료된 연결의 범위를 표시한다.

## 검증 입력

0.11의 전체 입력은 SHA256 67de28abf0741c406178a2fe4ce07962e69bce827c3196b78e887da3bd0dab13으로 동결한다. G=6.67430×10⁻¹¹ SI, H0=67.4 km/s/Mpc, 물리 에너지 구성비 0.0493·0.265·0.6857, 전자 정지에너지 510998.95069 eV를 유지한다. 주소 산술 구성비 0.05·0.268·0.682는 다른 장부다. c=299792458 m/s, h=6.62607015×10⁻³⁴ J s, 1 eV=1.602176634×10⁻¹⁹ J도 계승한다. 새로운 상수 보정은 없다.

새 구성 입력은 위상 간격 epsilon=0.05, 128개 유한 모드, 접힘 경계 위상 eta=0·0.5, 공간 경계 periodic·Dirichlet, 길이 L=20 ell_mu다. 가속 경로 beta(s)=0.2+0.5s는 지정 경로이며 중력 운동방정식에서 도출한 궤도가 아니다. 정적 중력 패치 R=200 kpc와 Phi=Psi 조건은 계승한다. 상류 가설 r1의 5·11·12쪽은 경로별 갱신과 위상-에너지 가지의 출처다. epsilon, 경계 및 길이는 측정한 최소시간이나 실제 입자 가둠 조건으로 확정하지 않는다.

## WRRA 고유 변환

전자 보정이 정한 mu_E=E_e/23에서 시간·길이 단위를 계산하고 epsilon으로 셔터의 고유시간 간격을 정한다. ell_mu는 단위 기준이다. 미시 공간 길이를 우주 크기나 0.11의 미정 L0에 대입하지 않는다. 플랑크 시간은 비교 기준이며 c delta_tau도 독립적인 최소 공간 길이의 증명이 아니다.


$$
\mu_E=E_e/23,\quad t_\mu=\hbar/\mu_E,\quad \ell_\mu=ct_\mu,\quad \Delta\tau_*=\epsilon t_\mu,\quad \epsilon=0.05. \tag{1}
$$


| Quantity | Calculated value | Unit |
| --- | --- | --- |
| mu_E | 22217.345682174 | eV |
| t_mu | 2.962603932832e-20 | s |
| delta_tau | 1.481301966416e-21 | s |
| L_cavity | 1.776332630208e-10 | m |


실행값 delta_tau=1.481301966416e-21 s, delta_tau/t_P=2.747605735737e+22다. 동일 입력에서 epsilon을 두 배로 바꾸어도 에너지 스펙트럼과 전자 보정은 바뀌지 않는다.

시간꼴 경로에는 누적 고유시간을 사용한다. 약한 정적 패치의 A=1+2Phi/c², B=1−2Phi/c²에서 beta_local은 정적 관측자가 잰 속도다. 좌표 속도를 그대로 대입하지 않는다. 평탄 공간에서는 A=B=1이다. 이는 서로 다른 경로에 하나의 전역 셔터 틱을 강제하지 않는다.


$$
\begin{aligned}c^2d\tau^2&=A c^2dt^2-B\,d\mathbf{x}^2,\\\beta_{\mathrm{local}}^2&=\frac{B}{A c^2}\left|\frac{d\mathbf{x}}{dt}\right|^2,\quad \frac{d\tau}{dt}=\sqrt{A(1-\beta_{\mathrm{local}}^2)}.\end{aligned} \tag{2}
$$



$$
\tau(t)=\int_0^t\frac{d\tau}{dt^{\prime}}dt^{\prime},\quad k=\lfloor\tau/\Delta\tau_*\rfloor,\quad r_\tau=\tau/\Delta\tau_*-k,\quad \tau(t_k)=k\Delta\tau_*. \tag{3}
$$


같은 좌표 간격 T=64 delta_tau에서 beta=0·0.6·0.8의 완전 갱신 수는 64·51·38이고 나머지 위상 구간을 따로 유지한다. 표의 overlap은 에너지 차 mu_E인 같은 가중치의 두 접힘 모드가 처음 상태와 겹치는 값이며 측정 결과의 확률이나 기록이 아니다. 빛꼴 경로는 고유시간 0이지만 정지 시계의 갱신 수를 지정하지 않는다. 광자 전파가 멈춘다는 판정도 하지 않는다.

| beta | tau / delta_tau | Complete ticks | Coherent overlap |
| --- | --- | --- | --- |
| 0.0 | 64.0 | 64 | 0.000852612 |
| 0.6 | 51.2 | 51 | 0.082205611 |
| 0.8 | 38.4 | 38 | 0.328925174 |



$$
t^{\prime}=\gamma_u(t-ux/c^2),\quad x^{\prime}=\gamma_u(x-ut),\quad c^2\Delta t^{\prime 2}-\Delta x^{\prime 2}=c^2\Delta t^2-\Delta x^2. \tag{4}
$$


가속 경로를 16·32·64·128 구간으로 나누고 u/c=0.3인 좌표계에서 각 구간의 고유시간을 대조한다. 경로 적분의 tau/T=0.877980386396에 대한 오차는 약 4배씩 감소한다. 누적 고유시간을 역으로 풀어 57개 갱신 사건을 실제 계산했다. 이 구간 수렴은 유한 경로의 수치 검사다.

정적 국소 시계의 퍼텐셜은 기존 g(r)를 유한 경계 R까지 적분한다. Phi(R)=0은 경계 시계의 정규화다. 무한 거리 기준을 도입하지 않는다. 퍼텐셜의 독립 수치 미분은 같은 중력 가속도를 반환한다.


$$
\Phi(r)=-\int_r^R g(s)\,ds,\quad R=200\,\mathrm{kpc},\quad \Phi(R)=0,\quad \frac{\nu_R}{\nu_r}=\sqrt{A(r)/A(R)}. \tag{5}
$$


| r / kpc | Phi / c² | Static d_tau / d_t |
| --- | --- | --- |
| 3 | -1.728306260831e-06 | 0.999998271692 |
| 8.2 | -1.248693279810e-06 | 0.999998751306 |
| 50 | -4.966030243693e-07 | 0.999999503397 |
| 200 | -0.000000000000e+00 | 1.000000000000 |


8.2 kpc에서 기존 회전 속도 207.510905127 km/s를 넣으면 이동 시계의 d_tau/d_t=0.999998511748이다. 균질 운반자 I/N은 임의의 Hamiltonian 아래 정지하므로, 기존 균질 에너지·압력·팽창을 유지하며 FRW의 시계 적분을 연결할 수 있다. 일정한 특이 속도 beta=0.6은 지정 경로이며 별도 운동을 가정한다. 초거대 갱신 수는 부동소수점 규모 추정이고 정확한 정수나 모든 사건의 시뮬레이션으로 제시하지 않는다.


$$
H(a)=H_0\sqrt{(f_\varphi+f_c)a^{-3}+f_b},\quad \Delta\tau=\int_{a_0}^{a_1}\frac{\sqrt{1-\beta_{\mathrm{pec}}^2}}{aH(a)}\,da. \tag{6}
$$


이제 유한 접힘 기저에서 자기수반 에너지 연산자를 구성한다. 모든 실제 행렬의 차원은 N=128로 유한하다. F는 정규화 Fourier 행렬이고 eta는 명시한 접힘 경계 위상이다. 허용 집합은 −64부터 63까지다. 공간 미분의 유한 스펙트럼 투영을 사용하며 전자 모드에서 격자 오차를 다시 보정하지 않는다.


$$
F_{jn}=N^{-1/2}e^{2\pi i jn/N},\quad H_{\mathrm{fold},\eta}=F\,\operatorname{diag}(\mu_E|n+\eta|)F^{\dagger},\quad H=H^{\dagger}. \tag{7}
$$


F는 주기 함수 phi(y)의 게이지 표현이다. 물리 접힘 함수 psi(y)=exp(2pi i eta y)phi(y)를 사용하면 경계 위상이 미분의 n+eta 이동으로 나타난다.


$$
\psi(y+1)=e^{2\pi i\eta}\psi(y),\quad \eta=0\ \mathrm{or}\ 1/2,\quad E_{23,0}=23\mu_E=E_e. \tag{8}
$$


eta=0은 0.11의 영 절편 질량 가지를 그대로 재현한다. eta=0.5에서 같은 모드 23의 에너지는 522107.623531087 eV로 바뀐다. 같은 보정의 경계 민감도이며 실제 전자의 경계가 바뀌었다는 주장이나 새 입자 동정이 아니다. eta=0에서 ±23의 같은 에너지는 전하 부호를 정하지 않는다. 전하는 기존 필터 장부에 남는다.

별도의 유한 공간 구간에서 전자 정지에너지를 가진 자유 양의 에너지 연산자를 구성한다. K는 주어진 경계의 양의 파수제곱 연산자다. 주기 경계는 영 운동량을 허용하고 Dirichlet 경계는 양 끝의 함수값 0을 제약한다. 이는 유한 구간의 명시적 경계이며 실제로 무한한 에너지 장벽을 만드는 모형이 아니다.


$$
K=F_B\operatorname{diag}(k_n^2)F_B^{\dagger},\quad H_{\mathrm{space}}=\sqrt{E_e^2I+(\hbar c)^2K},\quad L=20\ell_\mu. \tag{9}
$$



$$
k_n^{\mathrm{periodic}}=2\pi n/L,\quad k_n^{\mathrm{Dirichlet}}=\pi n/L,\quad \psi_n(x)\propto\sin(\pi nx/L),\quad n=1,\ldots,N. \tag{10}
$$


| Boundary / operator | Mode | Energy / eV | Kinetic / eV |
| --- | --- | --- | --- |
| fold periodic | 0 | 0.000000000 | — |
| fold periodic | 23 | 510998.950690000 | — |
| dirichlet | 1 | 511010.867747384 | 11.917057384 |
| dirichlet | 2 | 511046.617252180 | 47.666562180 |
| periodic | 0 | 510998.950690000 | 0.000000000 |
| periodic | 1 | 511046.617252180 | 47.666562180 |


공간 표는 전체 에너지와 정지에너지를 뺀 운동에너지를 구분한다. 특정 원자선이나 실제 공동의 측정값에 보정한 표가 아니다. L=20·40·80 ell_mu의 유한 길이 대조에서 운동량 간격은 반으로, 첫 운동에너지 간격은 약 4분의 1로 줄어든다. 이 대조는 실제 무한 공간의 실현을 가정하지 않는다.

가둠 경계를 부과하지 않은 국소 자유 분산은 유한한 실수 운동량 입력에 연속 응답한다. pc/mu_E=0.1·0.5 등 비정수 입력도 같은 셔터 갱신에서 실행된다. 시간 이산성만으로 모든 운동량·에너지가 이산화되는 것은 아니다. 전자 모드의 유한차분 대조는 N=128·256·512에서 오차 −5.2271%·−1.3225%·−0.3316%를 보이며 mu_E를 고정한다.


$$
E(p)=\sqrt{E_e^2+c^2p^2},\quad p\ \mathrm{real},\quad E^{\mathrm{FD}}_{23,N}=\mu_E\frac{N}{\pi}|\sin(23\pi/N)|. \tag{11}
$$


고유시간 한 번의 갱신은 같은 Hamiltonian의 단위 연산자다. U의 고유값을 독립적으로 계산해 위상 theta를 읽는다. 기본 epsilon에서 접힘 및 두 공간 스펙트럼 모두 위상 복원이 수치 정밀도 내에서 맞는다. 위상만 읽으면 에너지는 정수 가지 ell만큼 미정이므로 선택한 생성자와 가지를 공개해야 한다.


$$
U_* = e^{-iH\Delta\tau_*/\hbar},\quad U_*v_j=e^{-i\theta_j}v_j,\quad 0\leq\theta_j<2\pi. \tag{12}
$$



$$
E_j=\frac{\hbar}{\Delta\tau_*}(\theta_j+2\pi\ell_j),\quad \ell_j\in\mathbb{Z},\quad E_{\mathrm{band}}=2\pi\hbar/\Delta\tau_*. \tag{13}
$$



$$
e^{-i(H+mE_{\mathrm{band}}I)\Delta\tau_*/\hbar}=U_*,\quad m\in\mathbb{Z}. \tag{14}
$$


epsilon=0.25인 대조에서는 77개 접힘 모드가 정수 가지를 필요로 한다. 가지를 버리면 에너지 복원이 크게 실패한다. U를 생성자 고유기저에서 읽은 위상에 공개한 가지를 더하면 복원된다. 가지 정수는 U만에서 새로 발견한 값이 아니다.

## 산출값과 기존 시계의 대조

0.10 고정 부피 장부의 E_star=ucrit V0와 무차원 좌표 xi를 정확히 SI 고유시간으로 환산한다. 이때 같은 에너지 행렬을 사용한다. 미시 접힘과 공간 스펙트럼은 별도 탐침이며 그 전자 에너지를 거시 밀도에 중복 합산하지 않는다. V0=1 m³는 공개한 집합적 장부 부피이고 기본 입자의 고유시계를 도출하는 부피가 아니다.


$$
U_{0.10}(\xi)=e^{-i\xi\widehat E/E_*}=e^{-i\widehat E\tau/\hbar},\quad \xi=E_*\tau/\hbar,\quad \rho(\tau)=U\rho_0U^{\dagger}. \tag{15}
$$


실제 delta_tau 간격으로 k=0·1·2·4·8의 상태와 D·R 부하를 실행했다. 총 에너지는 3.200810499959×10⁻¹⁰ J로 보존되며 D 부하의 최대-최소 차는 0.038059728227이다. 정규화·양성도 수치 허용오차 내에서 유지된다. 이 고정 부피 내부 교환에 측정 장치나 물리 기록 생성은 아직 없다.


$$
\operatorname{Tr}\rho=1,\quad \operatorname{Tr}(\rho\widehat E)=\mathrm{constant},\quad |\langle\psi_0|U(\tau)|\psi_0\rangle|^2=\cos^2(\mu_E\tau/2\hbar). \tag{16}
$$


그러나 0.10의 팽창 상태 계산에 쓴 느린 omega_info=0.7H0는 E_star/hbar와 같지 않다. 두 주파수는 각각 1.528999668760×10⁻¹⁸ s⁻¹와 7.272096256981×10²⁴ s⁻¹다. 비율은 약 2.10×10⁻⁴³이다. 같은 에너지 생성자의 물리 SI 위상이라는 해석은 이 대조에서 반증된다. 느린 일정을 유지하려면 다른 유효 생성자나 상호작용의 별도 근거가 필요하며, 이번 판에서 임의로 대입해 해결했다고 하지 않는다.


$$
r_{\mathrm{clock}}=\frac{\hbar\omega_{\mathrm{info}}}{E_*}\ne1,\quad H_{\mathrm{eff}}=r_{\mathrm{clock}}\widehat E\ne\widehat E. \tag{17}
$$


| Computed comparison | Value | Unit / role |
| --- | --- | --- |
| Default U eigenphase error | 6.519258022308e-09 | eV |
| Aliased naive error | 8.664764816048e+05 | eV |
| Declared-branch error | 4.656612873077e-10 | eV |
| Old / SI frequency | 2.102556972196e-43 | ratio |


기존 느린 비균질 팽창 이력은 구성 일정의 기록으로 보존한다. 새 물리 위상은 고정 부피 장부에서 실행했고, 균질 FRW 시계는 I/N의 정지성 아래 연결했다. 비균질 운반자·중력·팽창의 완전 공변 동역학까지 닫혔다고 판정하지 않는다. 또한 작은 갱신 간격에서 같은 Hamiltonian의 연속 생성자에 접근함을 수치로 대조한다. 이는 연속 근사의 계산이며 실제 무한한 공간·시간 지지의 요구가 아니다.


$$
\frac{i\hbar(U(\delta\tau)-I)}{\delta\tau}\longrightarrow H,\quad \delta\tau\longrightarrow0. \tag{18}
$$


## 반증조건과 재현

고유시간이 Lorentz 좌표 변환에서 달라지거나, 정적 퍼텐셜 미분이 같은 g를 재현하지 못하거나, 경계별 에너지·갱신 위상이 어긋나거나, 정수 가지를 누락하거나, 고정 부피 에너지 보존이 깨지면 해당 연결을 수정한다. 느린 기존 시계를 SI 위상으로 무환산 식별하는 실패도 판정표에 포함한다. 새 검사 36개와 0.11·0.10에서 계승한 60개가 통과한다. 잘못된 전역/최소 시계 주장, 무한 경계 입력, 경계 밖 경로와 미실행 기록 입력을 거부한다.

```bash
python -m pip install -r calculations/wrra_m_0_12/requirements.txt
python calculations/wrra_m_0_12/run_release.py
```

parameters.json에 입력·출처·구성 선택을 공개한다. JSON과 8개 CSV는 경로 시계·갱신 사건·허용 모드·공간 분산·부하 교환을 제공한다. 결과를 모두 삭제한 새 복사본에서 결과와 한영 원고를 바이트 단위로 재현한다. Word의 18개 native 수식과 5개 계산 표를 한영 대조하고, 모든 PDF 페이지를 렌더링 검토한다. 검사 결과, 문서 대조와 새 복사본 재현 판정은 각각 JSON으로 제공한다.

Input SHA256 c80742fa4d0e0bdbb94e3390a2cc02da4a535168eaf66fb28f7318ec9b7b8b3d

## 판정과 후속 범위

0.12는 공개한 구성 선택 아래 경로별 고유시간 갱신, 유한 연산자·경계의 스펙트럼 및 고정 부피 SI 시간 환산을 완료한다. 기존 시계의 실패와 미완료 공변 연결은 함께 동결한다. delta_tau의 기원·측정 최소시간, 실제 가둠 경계와 길이 선택은 남는다. 0.13은 물리 0/1 결과·관측 뒤 상태·기록을 실행하고 0.14 이후는 반복 불확실성·응력·곡률·크기·중성미자·전파를 다룬다. 새 독립 예측이나 우주의 유일한 해는 이번 완료의 선행조건이 아니다.

## 참고 자료

Choi Wonsik. WRRA_M 0.11, frozen baseline commit 6e9e9c9162c650b71b78035abf02ec6c1f753d02. https://github.com/Wonsik-Choi-janefather/wrra-m-0.1

Choi Wonsik. WRRA_M Upper Two-Stage Filter Hypothesis 1.0-r1 (2026-10-02), pp. 5, 11–12; source contract in references/clock_contract.md.

Choi Wonsik. Minimal Computation Cosmology 2.3.2, chapter 23, frozen commit 21daec110c0cbecb228c445d587eac8302e7f767. https://github.com/Wonsik-Choi-janefather/minimal-computing-cosmology-2.3.2

Hughes Scott. MIT 8.033, Fall 2024 lecture notes, sections 18.2–18.3. https://ocw.mit.edu/courses/8-033-introduction-to-relativity-and-spacetime-physics-fall-2024/mit8_033_f24_lec_full.pdf

Copyright 2026 Wonsik Choi. CC BY 4.0. https://creativecommons.org/licenses/by/4.0/
