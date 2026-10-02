# WRRA M 0 10 Physical energy and pressure

0.9-r1 address effects now feed a positive SI energy operator. Pressure is the
volume derivative of the same energy. The frozen calibration reproduces all
nine inherited state-volume cases, q=-0.52855, v=207.5109051266 km/s and
conditional deflection=0.5355865106 arcsec. The 32 verification groups pass.

검증 입력 → WRRA 고유 변환 → 산출값 → 반증조건 순서와 전체 계산은 한영 원고에
기록한다. 산술 5%·26.8%·68.2%와 기존 에너지 4.93%·26.5%·68.57%는 구분하여
유지한다. 기준 SI 계수를 한 번 보정한 후 모든 주소·상태·부피 시험에서 고정한다.

```bash
python -m pip install -r calculations/wrra_m_0_10/requirements.txt
python calculations/wrra_m_0_10/run_release.py
```

The address response lambda and volume exponents are disclosed constitutive
inputs. A product address-carrier state is adopted. Pending SOURCE and returned
provenance use the same energy response. Admission conversion work is recorded
as signed exchange with the work-owning environment, not a fourth cosmic density.
The environment's microscopic law and physical measurement records are later
development tasks. Lensing remains conditional on Phi=Psi in the finite patch.

- [한국어 원고](source_ko.md)
- [English paper](source_en.md)
- [32 numerical check groups](results/verification.json)
- [Executed results and input ledger](results/results.json)
- [Energy samples](results/address_energy_samples.csv)
- [Frame conversion-work ledger](results/frame_energy_transport.csv)
- [Bilingual document checks](results/document_checks.json)
- [Clean-copy reproduction](results/reproduction_checks.json)
- [한국어 PDF](../../paper/WRRA_M_0_10_KO.pdf) · [DOCX](../../paper/WRRA_M_0_10_KO.docx)
- [English PDF](../../paper/WRRA_M_0_10_EN.pdf) · [DOCX](../../paper/WRRA_M_0_10_EN.docx)

Optional document publishing uses python-docx, pypdf, pandoc and a Korean font
named NanumGothic. build_reports.py creates native-equation Word editions from
the generated sources; PDF export uses a compatible office renderer. Numerical
reproduction does not require these publishing tools.

Wonsik Choi · ORCID 0009-0001-4263-9772 · janefather@gmail.com

The reviewed 0.9 baseline DOI is 10.5281/zenodo.23091892. It is a baseline
reference, not a DOI assigned to this 0.10 release.
