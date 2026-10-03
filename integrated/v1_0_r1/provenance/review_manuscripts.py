from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent / 'output/paper'
DOI = '10.5281/zenodo.23126800'
for lang in ('KO', 'EN'):
    p = ROOT / f'WRRA_M_Integrated_1_0_{lang}_2026_10_03.md'
    text = p.read_text()
    common = [
        (r'$$U(\tau)=e^{-iH\tau/\hbar},\qquad' + '\n' + r'E_j=\frac{\hbar}{\Delta\tau}(\theta_j+2\pi b_j),\qquad b_j\in\mathbb Z.\qquad(20)$$',
         r'$$U_{\rm rel}(\tau)=e^{-iH_{\rm rel}\tau/\hbar},\qquad' + '\n' + r'\varepsilon_j=\frac{\hbar}{\tau}(\theta_j+2\pi b_j),\qquad b_j\in\mathbb Z.\qquad(20)$$'),
        (r'\frac{\mathrm{gap}\,k\Delta\tau_{\rm frame}}{2\hbar}', r'\frac{\mathrm{gap}_J\,k\Delta\tau_{\rm frame}}{2\hbar}'),
    ]
    if lang == 'EN':
        changes = common + [
          ('Integrated manuscript 1.0 | 3 October 2026', 'Integrated manuscript 1.0 reviewed r1 | 3 October 2026'),
          ('Consolidation of upstream 0.10 downstream 0.12 and bridge 0.8 reviewed r1', 'Consolidation of upstream 0.10 downstream 0.12 and bridge 0.8 reviewed r1  \nDOI https://doi.org/' + DOI),
          ('Kc is the periodic Laplacian;', 'Kc is the positive semidefinite discrete negative Laplacian on the periodic carrier;'),
          ('In Eq. 20, θj is the principal phase of the eigenvalue of U†, matching the positive generator-phase convention.', 'The executed relative generator is Hrel = HB − EB,rest I. Its eigenvalues εj = Ej − EB,rest are expressed in joules in Eq. 20; τ = kΔτframe. Here θj is the principal phase of the corresponding eigenvalue of Urel†, matching the positive generator-phase convention.'),
          ('Evolution with the same H followed by another X readout gives', 'Evolution with the same relative H followed by another X readout gives Eq. 22, where gapJ = gapMeV × 1.602176634 × 10⁻¹³ J/MeV and ℏ is in J s. The cosine argument is dimensionless.'),
          ('[2] Choi W. WRRA M 0.10 through 0.12 Reviewed Series SI Energy and Pressure Sequential Calibration and Proper Time Mode Spectra. 0.12 r1. 2026. https://doi.org/10.5281/zenodo.23113101 Executable basis for WRRA M Downstream Integrated Model and Verification 1.0.', '[2] Choi W, Choi J. WRRA M Downstream Integrated Model and Verification 1.0. 2026. https://doi.org/10.5281/zenodo.23115883 Executable basis: Choi W. WRRA M 0.10 through 0.12 Reviewed Series SI Energy and Pressure Sequential Calibration and Proper Time Mode Spectra. 0.12 r1. 2026. https://doi.org/10.5281/zenodo.23113101'),
          ('This integrated manuscript has no newly assigned DOI; the listed DOIs identify prior public sources.', 'This author-reviewed r1 integrated edition is identified by DOI https://doi.org/' + DOI + '. Source publications retain their distinct DOIs. The review corrects unit and relative-energy notation and strengthens the distribution audit; it introduces no new fitted physical parameters.'),
          ('The integrated distribution retains bilingual manuscripts, a numerical-claim/source-path register, this replay evidence, generation code, baseline archives and SHA256SUMS.', 'The integrated distribution retains bilingual manuscripts, a numerical-claim/source-path register, a portable audit that reads the actual Word tables, fresh replay evidence, generation code, source archives and SHA256SUMS. Run python audit_release.py from the extracted package root to check the manuscript values and source hashes.'),
        ]
    else:
        changes = common + [
          ('통합 원고 1.0 | 2026년 10월 3일', '통합 원고 1.0 검토판 r1 | 2026년 10월 3일'),
          ('Kc는 주기 Laplacian이고', 'Kc는 주기 운반 격자의 −∇²에 대응하는 양의 준정부호 이산 연산자이고'),
          ('식 20의 θj는 U† 고유값의 주값 위상으로 정의하여 양의 생성자 위상과 부호를 맞춘다.', '실행한 상대 생성자는 Hrel = HB − EB,rest I이다. 식 20의 고유값 εj = Ej − EB,rest는 joule 단위이며 τ = kΔτframe이다. θj는 대응하는 Urel† 고유값의 주값 위상으로 정의하여 양의 생성자 위상과 부호를 맞춘다.'),
          ('같은 H로 관측 후 상태를 진화시킨 뒤 재측정하는 같은 결과 확률은 다음과 같다.', '같은 상대 H로 관측 후 상태를 진화시킨 뒤 재측정하는 같은 결과 확률은 식 22와 같다. 여기서 gapJ = gapMeV × 1.602176634 × 10⁻¹³ J/MeV이며 ℏ는 J s 단위이다. 따라서 cosine의 인수는 무차원이다.'),
          ('본 통합 원고의 고유 DOI는 아직 배정되지 않았으며 본문 DOI는 선행 공개 자료를 가리킨다.', '본 저자 검토판 r1 통합 원고의 DOI는 https://doi.org/' + DOI + '이다. 선행 공개 자료는 각 고유 DOI를 유지한다. 이번 검토는 단위·상대 에너지 표기를 바로잡고 배포 검증을 보강했으며 새로운 물리 맞춤 변수를 도입하지 않았다.'),
        ]
        # Preserve the Korean title wording while exposing the reviewed edition and its DOI.
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if '1.0 |' in line and i < 15:
                lines[i] = line.replace('1.0 |', '1.0 검토판 r1 |')
                lines.insert(i + 1, 'DOI https://doi.org/' + DOI + '  ')
                break
        text = '\n'.join(lines) + '\n'
        changes = [x for x in changes if x[0] != '통합 원고 1.0 | 2026년 10월 3일']
        ref = next(x for x in text.splitlines() if x.startswith('[2] '))
        changes.append((ref, '[2] Choi W, Choi J. WRRA M Downstream Integrated Model and Verification 1.0. 2026. https://doi.org/10.5281/zenodo.23115883 실행 기준: Choi W. WRRA M 0.10 through 0.12 Reviewed Series SI Energy and Pressure Sequential Calibration and Proper Time Mode Spectra. 0.12 r1. 2026. https://doi.org/10.5281/zenodo.23113101'))
        text = text.replace('# 참고문헌', '압축을 푼 패키지의 루트에서 python audit_release.py를 실행하면 실제 Word 표의 수치와 JSON 원자료·파일 해시를 대조할 수 있다.\n\n# 참고문헌')
    for old, new in changes:
        assert text.count(old) == 1, (lang, old, text.count(old))
        text = text.replace(old, new)
    assert text.count('$$') == 50
    p.write_text(text)
print(json.dumps({'reviewed': ['KO', 'EN'], 'doi': DOI}))
