# WRRA 64모드와 팽창 전환 동역학 v0.3

최원식 · 최정인, 독립연구자. 2026-10-20.

한글 REPORT_KO.md / WRRA_64Mode_Conversion_v0_3_KO.pdf, 영문 REPORT_EN.md / WRRA_64Mode_Conversion_v0_3_EN.pdf.

## 실행과 재현

Python 3.12, requirements.txt의 의존성이 필요하다. 동봉 runtime은 Linux x86-64, libgfortran 5를 사용한다. 다른 환경은 소스에서 빌드한다.

1. `python run_all.py`: 64개 정확 파수와 모든 정수 다중극의 실제 전달 묶음을 계산한다. 16개 묶음을 순서대로 실행해 메모리를 제한한다. 캐시가 없으면 수 분이 걸린다.
2. `python dynamics.py`: 팽창 전환 배경 보정·접선 이력·에너지/압력 일·프리드만 검사를 수행한다.
3. `python check_basis.py`: CAMB의 실제 초기 콜백으로 D/A 기저의 엔트로피·곡률 부호를 확인한다.
4. `python analyze.py`: 묶음을 합쳐 D_64_full.npz, A_64_full.npz와 complete_projection.npz, extension_results.json을 만든다.
5. 정밀도 대조: `python run_transfers.py 2.5 D 50000 32 0` 및 `python run_transfers.py 3.0 D 50000 32 0`. review_extension.py는 두 파일 이름을 모두 허용하므로 수정할 필요가 없다. 동봉된 원 대조 파일 D_64_a2.5_s32_k50000.npz도 같은 규칙으로 생성된 값이다.
6. `python review_extension.py`, `python figures.py`로 별도 대조와 그림을 생성한다.

`run_all.py`는 한 번의 거대한 Bessel 표 대신 어긋난 인접 짝홀 격자를 사용한다. 각 묶음은 실제 CAMB 진화와 투영이다. 최종 조립 결과의 5,999개 정수 다중극을 보간으로 채우지 않는다. 압축 묶음에는 재현 가능한 전체 합병 배열을 보존하며, 부피가 중복되는 개별 묶음 NPZ는 제외했다. 재계산하려면 첫 단계를 실행한다.

## 소스 빌드

gfortran, make, C/C++ 빌드 도구가 있는 환경에서 `python source/build.py`를 실행한다. 제공된 CAMB 2.0.4 원본 압축을 새로 풀고 cmb_patch.py와 apply_pair_sampling.py를 순서대로 적용한다. 이미 source/build 디렉터리가 있으면 새 위치에서 시작한다. 실행본은 source/runtime/camb에 저장된다. 소스 압축·원 라이선스·패치·런타임을 함께 제공한다.

## 검사와 범위

새 검사 123개: 투영·모드·공분산 96, 동역학 15, 실제 초기 기저 4, 정밀도/비선형 밀도면/최고 모드 8. 선행 v0.2의 576개는 이 수에 다시 넣지 않는다.

64모드와 모든 정수 다중극을 계산했고, 선언한 128셀 모형의 미전달 초기 분산은 0이다. 이는 모든 우주 파수 또는 ell>6000까지 계산했다는 뜻이 아니다. 기존 비중·배경은 재보정하지 않았으며, 새 전환 가능 저장소 비중은 관측 CDM/복사 비율로 보정했다. 시작 축척·전환 펄스·유체율과 공간 조절 규칙은 새 조건부 입력이다.

동역학은 하나의 우주의 국소 패치를 쓰는 선도 구배 근사다. 국소 고유시간에서 에너지 교환·압력 일·프리드만 방정식과 접선 곡률을 실제 진화시켰다. 양자화된 공간 프로파일을 입력으로 사용하지만 유한 양자별 방출 시각까지 계산한 것은 아니다. 유한 구배의 전체 운동량·계량·자유비행 중성미자 접합, 보통물질 입자 생성, 상세 열역사·비선형 진화와 새 관측 적합은 OPEN이다.

## 출처

선행 공개 v0.2: https://zenodo.org/records/23488763. 패치 CAMB 계보 원전: MCC_Initial_Preparation_SOURCE_Lensing_CMB_v0_1.zip, 보존 파일 libfile_98855230bffc8191b58b0817368d3571. 사용 입력과 코드 해시는 SHA256SUMS.json 및 PROVENANCE.json에 기록했다.

새 연구 원고: 저자 최원식·최정인, CC BY 4.0. CAMB 및 그 파생 소스·런타임은 동봉 원 라이선스를 유지한다. v0.3 DOI: https://doi.org/10.5281/zenodo.23489547 (게시 후 등록).

## GitHub 배포 구성

GitHub에는 코드·원본 CAMB 압축과 패치·고정 입력·결과 JSON·최종 투영 배열 complete_projection.npz를 제공한다. 빌드 실행본과 중복·대용량 전달 캐시는 저장하지 않는다. 새 체크아웃에서는 의존성 설치 후 `python source/build.py`, `python run_all.py`를 먼저 실행하고 위 검증 순서를 따른다. 정밀도 대조 두 실행을 마친 뒤 review_extension.py를 실행한다. 로컬 재현 압축에는 실행본과 합병 전달 배열도 포함한다.
