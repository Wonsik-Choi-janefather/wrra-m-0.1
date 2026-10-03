# WRRA M 0 11 첫 다섯 입력의 순차 보정

Wonsik Choi · 2026-10-03 · Revision 0.11-r1 · ORCID 0009-0001-4263-9772 · janefather@gmail.com · WRRA Core 1.0 / MCC 2.3.2 · CC BY 4.0

## 초록

고정된 WRRA Core 1.0과 MCC 2.3.2 위에서, 우리 우주에 특화된 WRRA_M의 첫 다섯 물리 입력을 G→H0→f_phi→f_c→전자 정지에너지 순서로 보정한다. 각 부분 단계는 아직 주어지지 않은 뒤의 목표를 읽지 않으며, 단계별 산출값과 남은 계수를 공개한다. 0.10의 에너지·압력 계산과 아홉 물리 사례를 유지하고, 주소 지수와 유효 입장률의 재표현 및 추가 산술 입력을 명시한다. 전자 모드 23과 영 절편을 채택하면 질량 단위는 22,217.345682 eV다. 동일 보정값을 만족하는 서로 다른 응답 형태를 계산하여 재현 성과와 식별되지 않은 자유도를 함께 기록한다.

## 검증 입력

전체 0.10 입력은 해시로 고정한다. G와 전자 에너지는 NIST 2022 CODATA 값을 사용하며, H0=67.4는 Planck 2018의 기본 LambdaCDM 보정 기준이다. CODATA 표준 불확도는 G에서 1.5×10⁻¹⁵ SI, 전자 에너지에서 0.00016 eV다. 채택 H0의 ±0.5 km s⁻¹ Mpc⁻¹는 Planck 기본 LambdaCDM 추론의 68% 신뢰구간이다. 물리 구성비 4.93%·26.5%는 계승한 반올림 보정값이며 이번 판에서 공분산을 부여하지 않는다. 후보표의 첫 다섯 행과 MCC의 전자 모드 관계를 출처로 기록한다.

| Input | Adopted value | Unit / role |
| --- | --- | --- |
| G | 6.6743000e-11 | m³ kg⁻¹ s⁻² |
| H0 | 67.4 | km s⁻¹ Mpc⁻¹ |
| f_phi | 0.0493 | energy fraction |
| f_c | 0.265 | energy fraction |
| m_e c² | 510998.95069 | eV |


c=299792458 m/s는 고정 입력이다. h=6.62607015×10⁻³⁴ J s와 1 eV=1.602176634×10⁻¹⁹ J는 정확한 SI 기준이다. 파섹 환산과 기존 국소 질량·반경·응답 함수 및 Phi=Psi 렌즈 조건은 계승한다. 주소 컷오프, 제타 영점 네 개, K=8, 위상 간격 0.1, 응답 계수 lambda_s, 부피 지수와 전자 모드 정수는 구성 입력이다. 이것들은 다섯 수치에서 새로 도출되지 않는다.

## WRRA 고유 변환

한 번에 한 입력만 추가하는 부분 계산을 실행한다. G는 작용의 SI 정규화와 곡률 응답을 고정한다. 정확한 h와 c를 함께 쓰면 플랑크 길이·시간도 단위 기준으로 계산된다. 뒤의 H0·구성비·전자 에너지를 NaN으로 바꿔도 해당 앞 단계 출력이 같아야 한다.


$$
C_G=\frac{c^4}{16\pi G},\qquad B_G=\frac{8\pi G}{c^4},\qquad \ell_P=\sqrt{\frac{\hbar G}{c^3}},\quad t_P=\ell_P/c. \tag{1}
$$


H0를 초의 역수로 환산한 뒤 임계 에너지 밀도를 계산한다. c/H0와 1/H0는 허블 길이·시간 기준이며 실제 우주의 전체 크기나 나이로 확정하지 않는다.


$$
H_0=\frac{H_{0,\mathrm{km/s/Mpc}}\,10^3}{10^6\,\mathrm{pc}_{\mathrm m}},\qquad u_{\mathrm{crit}}=\frac{3H_0^2c^2}{8\pi G}. \tag{2}
$$


표현형 구성비가 주어지면 숨은 전체 부하를 계산한다. 이어 모이는 부하 f_c를 넣어 D와 배경 R을 분리한다. eta_load는 0.6의 균질 운반자 기준 부하 계수이며 0.10의 주소별 eta_s와 다른 기호다.


$$
f_h=1-f_\varphi,\quad f_b=1-f_\varphi-f_c,\quad u_h=f_hu_{\mathrm{crit}},\quad \eta_{\mathrm{load}}=u_h/2. \tag{3}
$$



$$
Q_h\equiv\zeta\kappa_h^2=\frac{16\pi G u_h}{c^4},\qquad L_*=Q_h^{-1/2},\qquad L_0=L_*\sqrt{W_0}. \tag{4}
$$


식별되는 것은 가중 뒤틀림 Q_h다. 강성 zeta와 뒤틀림 kappa_h는 따로 정해지지 않는다. L_star는 계산된 길이 계수이고, W0가 주어지지 않아 L0는 미정이다. 95.07%라는 구성비만으로 우주 길이를 정하지 않는다.

| Step | New input | Newly available outputs | Remaining anchors / choices |
| --- | --- | --- | --- |
| 1 | G | action coefficient; SI response | H0, f_phi, f_c, E_e |
| 2 | H0 | H0 in s⁻¹; critical density | f_phi, f_c, E_e |
| 3 | f_phi | hidden density; weighted twist | f_c, E_e |
| 4 | f_c | sector energies; a_T, P, q | E_e |
| 5 | E_e | mass unit; electron units | structural freedoms remain |


0.10의 주소 효과 e_s(n), 정규화 가중치 w_n과 양의 응답 g_s(n)를 그대로 사용한다. 각 eta_s는 기준 주소 상태와 균질 운반자에서 한 번 맞춘 뒤 주소·상태 대조에서는 고정한다. 운반자 연산자는 A_phi=I, A_D=Kc/2, A_R=Kb/2이며 기준 균질 기대값은 모두 1이다.


$$
\mu_s=\sum_nw_ne_s(n)g_s(n),\quad \eta_s=\frac{f_su_{\mathrm{crit}}}{\mu_s},\quad \widehat E(a)=V_0\sum_s\eta_s\mu_sa^{\nu_s}A_s. \tag{5}
$$


압력은 같은 에너지 함수의 부피 미분이다. 지수 nu_phi=nu_D=0, nu_R=3을 유지하므로 D와 표현형은 무압력이고 R은 P_R=−u_R다. 부하가 비표현형이라는 이유로 에너지나 중력을 지우지 않는다.


$$
V=V_0a^3,\qquad E_s=\operatorname{Tr}(\rho\widehat E_s),\qquad P_s=-\partial E_s/\partial V=-\nu_su_s/3. \tag{6}
$$



$$
a_T=cH_0\sqrt{f_c/8},\qquad P_0=-f_bu_{\mathrm{crit}},\qquad q_0=(1-3f_b)/2. \tag{7}
$$


MCC의 영 절편 질량 가지에서 전자 모드 n_e=23을 채택한다. 전자 입력은 이 가지의 공통 에너지 단위를 정한다. 보고하는 ±1·±2·±3·±23은 일반 모드 대조이며 다른 입자의 질량 동정이 아니다. 모드 부호는 같은 정지에너지를 주고, 전하는 기존 필터 장부에서 별도로 유지된다. 모드 수와 영 절편은 추가 구성 선택이다.


$$
E_n=\sqrt{E_{\mathrm{off}}^2+n^2\mu_E^2},\qquad E_{\mathrm{off}}=0,\qquad \mu_E=E_e/23,\quad E_e=m_ec^2. \tag{8}
$$


같은 총 에너지 연산자를 전자 에너지 단위로 재표현한다. 차원 없는 값에 E_e를 다시 곱하면 원래 J 장부가 복원된다. 전자의 에너지를 우주 전체 밀도에 별도로 더하지 않는다. 미시 모드의 실제 경계조건과 시계 및 일반 스펙트럼은 0.12에 남긴다.


$$
\widetilde E_e=\widehat E/E_e,\qquad \widehat E=E_e\widetilde E_e,\qquad m_e=E_e/c^2. \tag{9}
$$


## 주소 alpha와 beta의 재표현

여기서 alpha_addr는 주소 가중치의 멱 지수, beta_eff는 홀수 합성수의 유효 입장률이다. 전자기 미세구조상수 alpha_EM과 구분한다. 0.9의 독립 산술 목표 D=0.268과 phi=0.05를 공개한 추가 입력으로 유지하며, 물리 에너지 목표 0.265·0.0493으로 대체하지 않는다. 짝수 합성수 집합 C_even은 소수 2를 제외한다.


$$
w_n(\alpha_{\mathrm{addr}})=\frac{n^{-\alpha_{\mathrm{addr}}}}{\sum_{j=2}^{N}j^{-\alpha_{\mathrm{addr}}}},\qquad \sum_{n\in C_{\mathrm{even}}}w_n=0.268. \tag{10}
$$



$$
\sum_{n\in C_{\mathrm{odd}}}w_n b_n(h)=0.05,\qquad \beta_{\mathrm{eff}}=\frac{0.05}{\sum_{n\in C_{\mathrm{odd}}}w_n}. \tag{11}
$$


고정한 위상·필터에서 다시 풀면 alpha_addr=1.899687695055, h=1.447673170353, beta_eff=0.865457012414다. alpha_addr와 h는 두 산술 목표에 맞춘 두 계수이며 beta_eff는 그 뒤의 재표현으로 계산된다. 세 번째 독립 beta 입력은 필요하지 않다. 다섯 물리 입력만으로 산술 목표나 alpha_EM을 정했다는 주장은 하지 않는다.

## 산출값

| Quantity | Calculated value |
| --- | --- |
| ucrit J m⁻³ | 7.668947767822e-10 |
| u_hidden J m⁻³ | 7.290868642868e-10 |
| eta_load J m⁻³ | 3.645434321434e-10 |
| zeta kappa_h² m⁻² | 3.028112744666e-52 |
| Length coefficient m | 5.746639841098e+25 |
| a_T m s⁻² | 1.191812669106e-10 |
| P Pa | -5.258597484395e-10 |
| q0 | -5.285500000000e-01 |
| mu_E eV | 2.221734568217e+04 |


기준 q0는 -0.528550000이며 국소 회전 속도 207.510905127 km/s와 조건부 렌즈 편향 0.535586511 arcsec를 유지한다. 질량 단위는 22217.345682174 eV다. 이 결과는 공개 입력을 통한 현실 기준 재현과 내부 계산으로 판정한다. 새 독립 예측이 완료의 선행조건은 아니다.

남은 자유도는 계산 대조로 표시한다. zeta와 kappa_h를 다음처럼 바꾸어도 Q_h는 같다. 또한 lambda_R=0과 1에서 각각 기준 eta_R를 맞추면 같은 다섯 목표와 같은 기준 q를 얻지만, 보정 뒤 K를 4로 바꾼 결과는 서로 다르다. 따라서 기준의 곱 eta_s mu_s를 맞추는 것과 전체 응답 형태를 정하는 것은 구분된다.


$$
\zeta\mapsto r\zeta,\qquad \kappa_h\mapsto\kappa_h/\sqrt r,\qquad \zeta\kappa_h^2\mapsto Q_h. \tag{12}
$$


| lambda_R | Reference q | K=4 q after fitting |
| --- | --- | --- |
| 0.0 | -0.528550000 | -0.547819855 |
| 1.0 | -0.528550000 | -0.548643149 |


다섯 입력의 독립성은 출력 (C_G,ucrit,u_h,u_c,mu_E)의 로그 민감도 행렬로 점검한다. 고정한 구성 선택 아래 수치 계수 5가 확인된다. 이는 다섯 보정 앵커의 국소 식별이며 모든 모형 계수의 완전 식별을 뜻하지 않는다.


$$
\frac{\partial\log(C_G,u_{\mathrm{crit}},u_h,u_c,\mu_E)}{\partial\log(G,H_0,f_\varphi,f_c,E_e)}=\begin{pmatrix}-1&0&0&0&0\\-1&2&0&0&0\\-1&2&-f_\varphi/(1-f_\varphi)&0&0\\-1&2&0&1&0\\0&0&0&0&1\end{pmatrix}. \tag{13}
$$


각 물리 입력을 ±1% 바꾼 열 가지 실행은 구성 민감도 대조이며 관측 신뢰구간이 아니다. 입력을 바꾼 경우에는 해당 물리 목표에 명시적으로 재보정하고, 주소 대조에서는 SI 계수를 고정한다. 전자 입력은 질량 단위를 바꾸지만 거시 밀도·q·회전 속도를 바꾸지 않는다. G 변화는 임계 밀도를 역비례로 바꾸고, H0 변화는 제곱으로 바꾼다.

고정 기준의 균질 팽창 출력은 같은 무압력·배경 에너지 관계를 사용한다. 비가환 운반자의 고정 부피 내부 교환은 총합 0이며, 상태의 양성과 정규화가 유지된다. 주소 입장에 필요한 변환 일과 환경 소유 계정은 0.10의 보존 검사로 계승한다.

r1은 0.12에서 확인한 시계 판정을 계승한다. 고정 부피 상태 진화는 xi=E_star tau_phys/hbar 환산으로 SI 위상에 연결된다. 0.10의 느린 비균질 팽창 일정과 그 SI 위상은 다르므로, 이 순차 보정의 완료를 완전 공변 비균질 동역학의 완료로 확장하지 않는다. 균질 I/N 상태는 단위 갱신에서 정지하며 아래 팽창식의 입력·출력을 유지한다.


$$
\frac{H(a)^2}{H_0^2}=(f_\varphi+f_c)a^{-3}+f_b,\qquad \frac{du}{d\log a}+3(u+P)=0. \tag{14}
$$


## 반증조건과 재현

앞 단계가 뒤 목표를 읽거나, 입력 순서가 바뀌거나, 에너지·압력 미분 및 0.10의 현실 기준 재현에 실패하거나, 전자 에너지를 중복 합산하거나, 식별되지 않은 W0·zeta·alpha_EM을 확정량으로 쓰면 해당 연결을 수정한다. 이번 판의 28개 검사와 계승한 0.10의 32개 검사를 실행한다. 영점·모드 부호, 5점 압력 미분, 로그 민감도, 실제 자유도 대조, 보존과 잘못된 입력 거부를 포함한다.

```bash
python -m pip install -r calculations/wrra_m_0_11/requirements.txt
python calculations/wrra_m_0_11/run_release.py
```

공개 패키지의 parameters.json는 입력·단위·출처·구성 선택을 포함한다. 순차 보정, 물리 사례, 질량 모드와 입력 변화는 JSON 및 CSV로 제공한다. 결과를 모두 삭제한 새 복사본에서 같은 실행 결과와 한영 원고를 바이트 단위로 대조한다. Word와 PDF는 원고에서 만든 최종 공개 판이며 계산 결과와 수식·표를 대조하고 모든 페이지를 렌더링 검토한다.

Reviewed 0.10 to 0.12 series DOI 10.5281/zenodo.23113101 · https://doi.org/10.5281/zenodo.23113101

Input SHA256 67de28abf0741c406178a2fe4ce07962e69bce827c3196b78e887da3bd0dab13

## 판정과 후속 범위

0.11은 공개한 다섯 입력의 순차 보정과 남은 자유도 표시를 완료한다. 보정값의 기원, 유일한 우주 해, 무보정 상수 도출은 이 판의 완료 조건이 아니다. 후속 0.12에서 시계·경계조건·스펙트럼, 0.13에서 물리 양자화·관측 뒤 상태·기록, 0.14 이후에서 불확실성·응력·곡률·크기와 중성미자 연결을 계산한다. 모형과 보정을 고정한 뒤 미측정량을 산출하면 그 입력과 반증조건을 붙여 WRRA의 예측으로 기록한다.

## 참고 자료

Choi Wonsik. WRRA_M 0.10, frozen baseline commit 24707c512c3994f2b19a96d6f257ef7d1249dab3. https://github.com/Wonsik-Choi-janefather/wrra-m-0.1

Choi Wonsik. Minimal Computation Cosmology 2.3.2, chapter 23, frozen commit 21daec110c0cbecb228c445d587eac8302e7f767. https://github.com/Wonsik-Choi-janefather/minimal-computing-cosmology-2.3.2

Choi Wonsik. WRRA_M_Calibration_Candidates.xlsx, first-sheet reference; source hash in parameters.json.

Planck Collaboration. Planck 2018 results VI, A&A 641 A6 (2020). https://doi.org/10.1051/0004-6361/201833910

NIST. CODATA 2022 constants table. https://physics.nist.gov/cuu/pdf/wall_2022.pdf

Copyright 2026 Wonsik Choi. CC BY 4.0. https://creativecommons.org/licenses/by/4.0/
