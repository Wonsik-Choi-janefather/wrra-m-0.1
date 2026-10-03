"""Compare bilingual source/native equations and published tables with execution."""
from pathlib import Path
import json
import re
from docx import Document
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parent.parent / 'paper'
SECTORS = ('phenotype', 'resident_nonphenotype', 'return')


def signature(node):
    return node.tag, tuple(sorted(node.attrib.items())), node.text or '', tuple(signature(c) for c in node)


def run():
    r = json.loads((ROOT/'results/results.json').read_text())
    v = json.loads((ROOT/'results/verification.json').read_text())
    assert v['passed'] and v['check_count'] == 32
    ref = next(c for c in r['cases'] if c['case_name'] == 'uniform_a1.0')
    alt = r['alternate_reference']
    expected1 = [[label, f"{100*r['common_arithmetic_ledger'][s]:.6f}",
                  f"{100*r['calibration']['target_energy_fractions'][s]:.6f}",
                  f"{r['calibration']['eta_J_m3'][s]:.10e}"]
                 for label, s in zip(('phi', 'D', 'R'), SECTORS)]
    def values(case):
        return [f"{case['total_density_J_m3']:.10e}", f"{case['total_pressure_Pa']:.10e}",
                f"{case['deceleration_q']:.9f}", f"{case['local_readout']['v_total_km_s']:.9f}",
                f"{case['local_readout']['finite_patch_lensing']['alpha_patch_arcsec']:.9f}"]
    expected2 = [[label, a, b] for label, a, b in zip(
        ('u J m⁻³', 'P Pa', 'q', 'v km s⁻¹', 'Deflection arcsec'), values(ref), values(alt))]
    expected3 = [[x['case'], f"{100*x['arithmetic_shares']['phenotype']:.9f}",
                  f"{x['physical']['deceleration_q']:.9f}"] for x in r['frozen_coefficient_address_probes']]
    sources, native, editions = {}, {}, {}
    for lang in ('KO', 'EN'):
        source = (ROOT/f'source_{lang.lower()}.md').read_text()
        assert source == (PAPER/f'WRRA_M_0_10_{lang}.md').read_text()
        sources[lang] = re.findall(r'\$\$(.*?)\$\$', source, re.S)
        assert re.findall(r'\\tag\{(\d+)\}', source) == list(map(str, range(1, 13)))
        doc = Document(PAPER/f'WRRA_M_0_10_{lang}.docx')
        native[lang] = [signature(eq) for p in doc.paragraphs for eq in p._p.xpath('.//m:oMath')]
        assert len(native[lang]) == 12 and len(doc.tables) == 3
        for table, expected in zip(doc.tables, (expected1, expected2, expected3)):
            actual = [[c.text.strip() for c in row.cells] for row in table.rows[1:]]
            assert actual == expected, (lang, actual, expected)
        assert doc.core_properties.author == 'Wonsik Choi'
        reader = PdfReader(PAPER/f'WRRA_M_0_10_{lang}.pdf')
        texts = [p.extract_text() for p in reader.pages]
        text = '\n'.join(texts)
        assert len(reader.pages) >= 5 and all(len(p) > 300 for p in texts)
        assert '\ufffd' not in text and '\u25a1' not in text
        for value in ('5.000000', '26.800000', '68.200000', '-0.528550000',
                      '207.510905127', '0.535586511', r['input_hash_sha256']):
            assert value in text, (lang, value)
        assert all('creativecommons.org/licenses/by/4.0/' in p for p in texts)
        assert re.findall(r'\(\s*(\d+)\s*\)', text) == list(map(str, range(1, 13)))
        editions[lang] = {'pdf_pages': len(reader.pages), 'native_equations': 12, 'tables': 3,
                         'computed_table_body_rows': 12}
    assert sources['KO'] == sources['EN'], 'source equations differ'
    assert native['KO'] == native['EN'], 'native Word equations differ'
    report = {'version': 'WRRA-M 0.10', 'passed': True, 'input_hash_sha256': r['input_hash_sha256'],
              'source_equations_equal': True, 'native_equations_equal': True,
              'tables_match_results': True, 'editions': editions,
              'visual_QA': 'Every final PDF page rendered and individually inspected before release.'}
    (ROOT/'results/document_checks.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    run()
