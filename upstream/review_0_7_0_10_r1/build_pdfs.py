"""Bilingual reviewed collection; render with ReportLab and inspect with Poppler."""
from pathlib import Path
import importlib.util,os
ROOT=Path(__file__).resolve().parent
os.environ.setdefault('WRRA_PDF_OUTPUT',str(ROOT/'paper'))
spec=importlib.util.spec_from_file_location('layout',ROOT.parent/'generator_v0_10/build_pdfs.py');layout=importlib.util.module_from_spec(spec);spec.loader.exec_module(layout)
# Reuse verified Korean typeface and table styles; explicit boundaries keep stages together.
from reportlab.platypus import PageBreak
original=layout.build
# The source parser recognizes each explicit page boundary as a heading.
for lang in ['EN','KO']:
 source=(ROOT/f'REPORT_{lang}.md').read_text().replace('[[PAGEBREAK]]','## [[PAGEBREAK]]')
 temp=ROOT/f'_render_{lang}.md';temp.write_text(source)
 # Adapt the existing helper without modifying the frozen historical publication helper.
 code=(ROOT.parent/'generator_v0_10/build_pdfs.py').read_text()
 code=code.replace("if line.startswith('# '):style='title';text=line[2:]", "if line=='## [[PAGEBREAK]]':story.append(PageBreak());i+=1;continue\n  if line.startswith('# '):style='title';text=line[2:]")
 code=code.replace('fontSize=9.5,leading=15','fontSize=9,leading=13').replace('fontSize=18,leading=27','fontSize=17,leading=24').replace('fontSize=8.5,leading=13','fontSize=8.5,leading=11').replace("(-1,-1),7)","(-1,-1),5)")
 code=code[:code.index("if __name__=='__main__':")]
 code=code.replace("'WRRA_M · 상류 '+version+' · 2026-10-03'", "'WRRA M · upstream review 0.7-0.10-r1 · 2026-10-03'")
 code=code.replace("'최원식 Wonsik Choi · 조건부 유한 실행 모형'", "'Wonsik Choi · finite conditional upstream model'")
 namespace={'__file__':str(ROOT.parent/'generator_v0_10/build_pdfs.py'),'__name__':'review_layout'};exec(compile(code,'review_layout','exec'),namespace)
 namespace['build'](temp,f'WRRA_M_Upstream_0_7_0_10_Reviewed_r1_{lang}_2026_10_03.pdf','0.7-0.10-r1')
 temp.unlink()
