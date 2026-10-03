# Reviewed 0.12 r1

2026-10-03 · [Reviewed series DOI](https://doi.org/10.5281/zenodo.23113101) · [Corrections](../../REVISION_0_10_TO_0_12_R1.md)

The parameter hash and calculated outputs are preserved. The old slow nonuniform expansion schedule is distinct from the SI Hamiltonian phase; its clock mismatch remains open. Both English and Korean papers are corrected.

# WRRA_M 0.12 · 고유시간 갱신과 유한 경계의 모드 스펙트럼

Wonsik Choi · 2026-10-03 · WRRA Core 1.0 / MCC 2.3.2 · CC BY 4.0

0.11의 입력과 전자 모드 23을 고정하고 경로별 고유시간, 유한 연산자의 허용 모드, 경계별 에너지와 갱신 위상을 실행한다. 새 구성 선택은 epsilon=0.05, 유한 N=128, 접힘 경계 위상 0·0.5, periodic·Dirichlet 공간 경계와 L=20 hbar c/mu_E다. **delta_tau=1.4813019664158691e-21 s는 선택한 갱신 간격이며 측정한 최소시간이 아니다.**

## 판정 순서

| 단계 | 실행과 판정 |
| --- | --- |
| 검증 입력 | 해시로 고정한 0.11 전체 입력, 정확한 SI 단위, 공개한 시계·경계 구성 입력 |
| WRRA 고유 변환 | 경로 고유시간 → 셔터 사건; 유한 모드·경계 → Hamiltonian → U의 고유위상; 기존 SI 장부 → 정확한 고유시간 환산 |
| 산출값 | 평탄·가속·유한 중력·균질 FRW 시계, 접힘·공간 스펙트럼, 자유 연속 분산, 정수 위상 가지, 고정 부피 상태·부하 교환 |
| 반증조건 | Lorentz 불일치, 경계별 위상·에너지 불일치, 정수 가지 누락, 에너지 보존 실패, 기존 느린 시계를 SI 위상으로 무환산 동일시 |

**기존 시계의 실패도 공개한다.** 0.10의 omega_info=0.7H0와 SI 장부의 E_star/hbar는 비율 2.102556972196466e-43으로 불일치한다. 느린 비균질 팽창 이력은 구성 일정의 기록으로 보존한다. 이번 물리 SI 위상은 같은 에너지 연산자의 **고정 부피** 갱신에서 실행하고, 균질 FRW는 정지 상태 I/N 아래 연결한다. 완전한 비균질 공변 동역학은 미완료다.

## Reproduce

```bash
python -m pip install -r calculations/wrra_m_0_12/requirements.txt
python calculations/wrra_m_0_12/run_release.py
```

Run from the repository/package root. The command executes 36 new checks, 28 inherited 0.11 checks and 32 inherited 0.10 checks, regenerating captured numerical results and matched manuscript sources. It uses deterministic finite matrices and quadrature, without random draws. `OPENBLAS_NUM_THREADS=1` is recommended for byte comparison on the recorded runtime.

- [한국어 PDF](../../paper/WRRA_M_0_12_KO.pdf) · [Word](../../paper/WRRA_M_0_12_KO.docx)
- [English PDF](../../paper/WRRA_M_0_12_EN.pdf) · [Word](../../paper/WRRA_M_0_12_EN.docx)
- [Reproducibility ZIP](../../paper/WRRA_M_0_12_Reproducibility.zip)
- [Inputs](parameters.json) · [Computed results](results/results.json) · [Verification](results/verification.json)
- [Document comparison](results/document_checks.json) · [Clean-copy replay](results/reproduction_checks.json)
- [Source contract](references/clock_contract.md) · [Completion record](../../REVISION_0_12.md)

## Result scope

The finite fold operator reproduces E_23=510998.95069 eV using the frozen mu_E. Boundary eta=0.5 changes that mode without a hidden mass refit. Finite spatial periodic and Dirichlet spectra differ at the ground state. Continuous free dispersion accepts finite noninteger momentum inputs under the same discrete update, without asserting actual infinite space.

The eigenspectrum of U recovers energy only modulo 2 pi hbar/delta_tau. A longer-step alias control fails on the naive branch; the disclosed generator-owned integer branches restore energy. Those branches are not identified from U alone. Timelike clocks use proper time, null paths have no rest-clock tick assignment, and no frozen-photon claim follows. Huge FRW tick estimates are not exact giant integer counts.

Remaining inputs/connections: empirical origin of epsilon, actual microscopic confinement/length/boundary selection, fully covariant interacting dynamics, physical binary outcomes and records in 0.13. A new independent prediction is not required for this stage's completion.

`build_reports.py`, `document_checks.py` and `package_release.py` are publication-maintenance scripts using Pandoc, python-docx, pypdf and a PDF renderer. Published Word/PDF files are checked final artifacts; ordinary numerical replay does not rebuild them.
