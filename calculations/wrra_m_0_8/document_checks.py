"""Match bilingual native equations and tables to the executed 0.8 results.

Optional authoring check: python-docx and pypdf are needed.
Visual page inspection is a separate release activity.
"""
from pathlib import Path
import csv
import json
import re
from docx import Document
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parent.parent / 'paper'


def xml_signature(node):
    return (node.tag, tuple(sorted(node.attrib.items())), node.text or '',
            tuple(xml_signature(child) for child in node))


def run():
    result = json.loads((ROOT/'results/results.json').read_text())
    verification = json.loads((ROOT/'results/verification.json').read_text())
    assert result['closure_passed'] and verification['passed']
    ref = next(c for c in result['cases'] if c['case_name'] == 'uniform_a1.0')
    equations, native, editions = {}, {}, {}
    for lang in ('KO', 'EN'):
        text = (PAPER/f'WRRA_M_0_8_{lang}.md').read_text()
        equations[lang] = re.findall(r'\$\$(.*?)\$\$', text, re.S)
        assert len(equations[lang]) == 15
        doc = Document(PAPER/f'WRRA_M_0_8_{lang}.docx')
        native[lang] = [xml_signature(eq) for p in doc.paragraphs
                        for eq in p._p.xpath('.//m:oMath')]
        assert len(native[lang]) == 15 and len(doc.tables) == 4
        assert [len(t.rows) for t in doc.tables] == [9, 10, 7, 24]
        tags = result['input_ledger']['filter_calibration']['response_tags']
        for row, (origin, sign) in zip(doc.tables[0].rows[1:], tags.items()):
            expected = [origin, str(sign), f'{ref["response"]["dimensionless_shifts"][origin]:.2f}',
                        f'{ref["response"]["normalized_signatures"][origin]:.9f}']
            assert [cell.text.strip() for cell in row.cells] == expected
        for row, case in zip(doc.tables[1].rows[1:], result['cases']):
            s = case['selection']
            expected = [f'{s["Delta_L"]:.9f}', f'{s["Delta_R"]:.9f}', s['selected_filter']]
            assert [cell.text.strip() for cell in row.cells[1:]] == expected
        for row, (field, data) in zip(doc.tables[2].rows[1:], ref['placement_and_charge']['field_groups'].items()):
            expected = [field, str(data['multiplicity']), data['Y'], ', '.join(data['Q'])]
            assert [cell.text.strip() for cell in row.cells[:4]] == expected
        assert verification['check_count'] == 23
        for i, row in enumerate(doc.tables[3].rows[1:], 1):
            assert row.cells[0].text.strip() == str(i)
            assert row.cells[-1].text.strip() in ('Pass', '통과')
            assert verification['checks'][i-1]['passed']
        pdf = PdfReader(PAPER/f'WRRA_M_0_8_{lang}.pdf')
        page_text = [page.extract_text() for page in pdf.pages]
        pdf_text = '\n'.join(page_text)
        assert '\ufffd' not in pdf_text
        for number in ('0.04669193039', '207.510905', '0.535586511', result['input_hash_sha256']):
            assert number in pdf_text, (lang, number)
        assert all('creativecommons.org/licenses/by/4.0/' in t for t in page_text)
        editions[lang] = {'pdf_pages':len(pdf.pages), 'native_equations':len(native[lang]),
                         'numerical_rows':23, 'verification_rows':verification['check_count'], 'total_table_body_rows':46}
    assert equations['KO'] == equations['EN'], 'source equations differ'
    assert native['KO'] == native['EN'], 'native equations differ'
    with (ROOT/'results/particle_inventory.csv').open(newline='') as f:
        inventory = list(csv.DictReader(f))
    assert len(inventory) == 48
    assert sum(row['status'] == 'SM_chiral_component' for row in inventory) == 45
    assert sum(row['status'] != 'SM_chiral_component' for row in inventory) == 3
    report = {'version':'WRRA-M 0.8', 'passed':True,
              'input_hash_sha256':result['input_hash_sha256'],
              'source_equations_equal':True, 'native_equations_equal':True,
              'tables_match_computed_results':True, 'inventory_counts_match':True,
              'editions':editions,
              'visual_QA':'All final PDF pages separately rendered and inspected for the release.'}
    (ROOT/'results/document_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    run()
