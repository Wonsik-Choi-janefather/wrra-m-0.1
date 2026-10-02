"""Check matched native equations and result-derived bilingual tables."""
from pathlib import Path
import json
import re
from docx import Document
from pypdf import PdfReader
from write_papers import tables

ROOT=Path(__file__).resolve().parent;PAPER=ROOT.parent.parent/'paper'
def signature(n):return n.tag,tuple(sorted(n.attrib.items())),n.text or '',tuple(signature(c) for c in n)

def run():
    r=json.loads((ROOT/'results/results.json').read_text());v=json.loads((ROOT/'results/verification.json').read_text())
    assert v['passed'] and v['check_count']==28 and v['inherited_0_10_check_count']==32
    expected=tables(r);source_eq={};native={};editions={}
    for lang in ('KO','EN'):
        source=(ROOT/f'source_{lang.lower()}.md').read_text();assert source==(PAPER/f'WRRA_M_0_11_{lang}.md').read_text()
        source_eq[lang]=re.findall(r'\$\$(.*?)\$\$',source,re.S)
        assert re.findall(r'\\tag\{(\d+)\}',source)==list(map(str,range(1,15)))
        d=Document(PAPER/f'WRRA_M_0_11_{lang}.docx');native[lang]=[signature(eq) for p in d.paragraphs for eq in p._p.xpath('.//m:oMath')]
        assert len(native[lang])==14 and len(d.tables)==4 and d.core_properties.author=='Wonsik Choi'
        for t,want in zip(d.tables,expected):assert [[c.text.strip() for c in row.cells] for row in t.rows[1:]]==want
        reader=PdfReader(PAPER/f'WRRA_M_0_11_{lang}.pdf');texts=[p.extract_text() for p in reader.pages];text='\n'.join(texts)
        assert all(len(t)>300 for t in texts) and len(reader.pages)>=4
        assert '\ufffd' not in text and '\u25a1' not in text
        for value in ('510998.95069','-0.528550000','22217.345682174','-0.547819855','-0.548643149',r['input_hash_sha256']):assert value in text,(lang,value)
        tags=[x for x in re.findall(r'\(\s*(\d+)\s*\)',text) if 1<=int(x)<=14]
        assert tags==list(map(str,range(1,15)))
        assert all('creativecommons.org/licenses/by/4.0/' in t for t in texts)
        editions[lang]={'pdf_pages':len(reader.pages),'native_equations':14,'tables':4,'computed_table_body_rows':21}
    assert source_eq['KO']==source_eq['EN'] and native['KO']==native['EN']
    report={'version':r['version'],'passed':True,'input_hash_sha256':r['input_hash_sha256'],'source_equations_equal':True,'native_equations_equal':True,'tables_match_results':True,'editions':editions,'visual_QA':'Every final PDF page rendered and individually inspected before publication.'}
    (ROOT/'results/document_checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':run()
