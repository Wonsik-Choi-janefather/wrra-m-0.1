"""Bilingual equation and table agreement against executed 0.9 outputs."""
from pathlib import Path
import json
import re
from docx import Document
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent.parent/'paper'


def signature(node):
    return node.tag,tuple(sorted(node.attrib.items())),node.text or '',tuple(signature(c) for c in node)


def run():
    r=json.loads((ROOT/'results/results.json').read_text()); v=json.loads((ROOT/'results/verification.json').read_text())
    assert v['passed'] and v['check_count']==26
    sources={}; native={}; editions={}
    for lang in ('KO','EN'):
        source=(PAPER/f'WRRA_M_0_9_{lang}.md').read_text()
        sources[lang]=re.findall(r'\$\$(.*?)\$\$',source,re.S)
        assert len(sources[lang])==12
        doc=Document(PAPER/f'WRRA_M_0_9_{lang}.docx')
        native[lang]=[signature(eq) for p in doc.paragraphs for eq in p._p.xpath('.//m:oMath')]
        assert len(native[lang])==12 and len(doc.tables)==4
        assert [len(t.rows) for t in doc.tables]==[3,13,6,7]
        for row,value in zip(doc.tables[0].rows[1:],r['separate_exponent_comparisons']):
            expected=[f"{value['alpha']:.1f}",f"{100*value['full_odd_composite_share']:.6f}",
                      f"{100*value['even_composite_share']:.6f}",f"{100*value['prime_share']:.6f}"]
            assert [c.text.strip() for c in row.cells]==expected
        for row,value in zip(doc.tables[1].rows[1:],r['frame_transport']):
            expected=[str(value['frame'])]+[f'{100*value[k]:.6f}' for k in
                     ('phenotype','resident_nonphenotype','source_pending','return')]
            assert [c.text.strip() for c in row.cells]==expected
        vals=list(r['terminal_common_arithmetic_ledger'].values())+[r['upstream_resident_Actual'],r['complete_current_Actual']]
        for row,value in zip(doc.tables[2].rows[1:],vals):
            assert [c.text.strip() for c in row.cells[1:]]==['1',f'{100*value:.8f}']
        for row,field in zip(doc.tables[3].rows[1:],('Q_L','L_L','u_c','d_c','nu_c','e_c')):
            selected=[x for x in r['channel_inventory'] if x['field']==field]
            expected=[field,str(len(selected)),selected[0]['Y'],f"{100*sum(x['arithmetic_phenotype_weight'] for x in selected):.8f}"]
            assert [c.text.strip() for c in row.cells]==expected
        pdf=PdfReader(PAPER/f'WRRA_M_0_9_{lang}.pdf'); texts=[p.extract_text() for p in pdf.pages]; text='\n'.join(texts)
        assert '\ufffd' not in text
        for value in ('5.00000000','26.80000000','68.20000000','31.80000000','100.00000000',r['input_hash_sha256']):
            assert value in text,(lang,value)
        assert all('creativecommons.org/licenses/by/4.0/' in p for p in texts)
        assert all(len(p)>300 for p in texts),'near-empty bibliography page'
        editions[lang]={'pdf_pages':len(pdf.pages),'native_equations':12,'tables':4,'computed_table_body_rows':25}
    assert sources['KO']==sources['EN'],'source equations differ'
    assert native['KO']==native['EN'],'Word equations differ'
    report={'version':'WRRA-M 0.9','passed':True,'input_hash_sha256':r['input_hash_sha256'],
            'source_equations_equal':True,'native_equations_equal':True,'tables_match_results':True,
            'editions':editions,'visual_QA':'All final PDF pages rendered and inspected separately before release.'}
    (ROOT/'results/document_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':run()
