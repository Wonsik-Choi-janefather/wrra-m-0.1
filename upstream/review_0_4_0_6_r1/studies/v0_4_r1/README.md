# Reviewed upstream 0.4-r1

Review date: 2026-10-03. Collection DOI: https://doi.org/10.5281/zenodo.23112253. Run `python code/compute.py` then `python verify_release.py`; see `verification.json` for the current check count. The original study and frozen kernels remain preserved in their historical GitHub paths.

# WRRA-M upstream 0.4 · 내부 공간 결합과 핵자의 공동 전류

**Wonsik Choi · 2026-10-02 · CC BY 4.0**

교정 상류 0.3-r1을 이어, 실제 가우스·야코비 공간 모드 사이의 결합을 구성하고
그 결합의 자기장 미분으로 자기 전류를 계산합니다. 같은 영자기장 고유상태에
약한 벡터·축벡터 전류도 적용합니다. 알려진 축벡터·자기모멘트를 공동 보정한
상태는 **q=0.293525, gV=1, gA=1.2753**, 양성자·중성자 자기모멘트를 반환합니다.

자기장 응답 **η=0.438092892645**는 추가 보정 정보입니다. 그 미분의 기대값이
이전 **c₁=0.439987792930 μN**에 연결됩니다. 실제 교환 전류는 비대각 연산자이며
c₁ 상수 대조군과 들뜬 상태·전이·내부 곡률이 다릅니다.

- [한국어 논문 PDF](paper/WRRA_M_Internal_Spatial_Coupling_Joint_Currents_v0_4_r1_KO_2026_10_03.pdf)
- [편집 가능한 Word](paper/WRRA_M_Internal_Spatial_Coupling_Joint_Currents_v0_4_r1_KO_2026_10_03.docx)
- [GitHub 원고](manuscript_KO.md)
- [전체 재현 ZIP](paper/WRRA_M_Internal_Spatial_Coupling_Joint_Currents_v0_4_Reproducibility_2026_10_02.zip)
- [입력](code/inputs.json) · [계산 결과](code/results.json) · [검증 결과](verification.json)
- [기준 출처와 구성 선택](source/provenance.json) · [SHA256 장부](SHA256SUMS)

## 입력 → 변환 → 출력 → 반증조건

관측 핵자 질량은 유효 응답 에너지와 질량 기준, 축벡터는 C와 혼합 상태,
두 자기모멘트는 c₀·η를 정합니다. 부모 0.2의 κ와 수명 기준은 고정합니다.
유한 소수 계열, 주소 45·75, 가우스 모드, 보존 공간 투영, Δ 및 선형 자기장
법칙은 공개한 구성 입력입니다.

WRRA 변환은 공간 E 표현 정렬 → 순열 불변 결합의 투영 → 소수 계열 결합의
대각화 → 같은 상태에서 자기장 미분 전류와 약한 전류의 판독입니다.
추가 산출은 고정 보정 입력 사례와 조건부 들뜬·전이 응답입니다.
공동 보정 반환 실패, 순열·전하·스핀 위반, 에너지 미분 불일치,
입력 전달 실패, Actual 에너지·전하·양성·노름 위반은 실패조건입니다.

## 실행과 검증

```bash
python -m pip install -r requirements.txt
python code/compute.py
python verify_release.py
```

**86개 구현 검사 + 26개 별도 검증 = 112개 통과**.
5차·6차 Gauss–Hermite 공간 적분, 공간 폭 변경, 유한 자기장의 특성방정식,
자기장 미분, 바뀐 보정 입력, 잘못된 입력 거부, 새 디렉터리의 결과 바이트
재현을 포함합니다. 재현 기준 환경은 Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0입니다.
다른 플랫폼에서는 마지막 자릿수 차이가 가능하므로 먼저 수치 검사 결과를 확인합니다.

## 해석 범위

공간 조화진동자와 투영은 유효 구성입니다. 투영 전 결합은 고차 모드 성분을
만들며 그 노름 제곱 7/3을 결과에 명시했습니다. 전체 QCD나 끈 압축화의
결합상태 해로 제시하지 않습니다. η는 영자기장 C만으로 정해지지 않습니다.
Δ=(mp+mn)/6은 상속한 기준 척도로, 계산 들뜬 상태를 관측 핵자 공명과 식별하지 않습니다.
명시적 b² 항을 넣지 않은 모델의 내부 곡률을 측정 Compton 편극률과 동일시하지 않습니다.
수명 878.3 s의 기준 반환은 기존 κ 보정의 전달입니다.

이전 공개 기록: [상류 교정 r1](../review_r1/README.md),
[DOI 10.5281/zenodo.23092499](https://doi.org/10.5281/zenodo.23092499).
현재 0.4는 그 자료집 다음 연구이며 새로운 DOI를 부여하지 않았습니다.

## 원고 재생성

```bash
python -m pip install -r source/requirements.txt
python source/build_doc.py
```

Pandoc와 NanumGothic·Latin Modern Math 폰트가 필요합니다. 수식은 native Word
OMML 개체입니다. Word→PDF는 LibreOffice 또는 Word에서 내보내고 페이지를 검수합니다.
원고의 숫자·표는 결과 JSON에서 생성됩니다.
