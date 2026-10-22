# Historical preparation script; release metadata is applied separately.
from pathlib import Path
import json,re,shutil,hashlib,subprocess
P=Path(__file__).resolve().parent.parent;old=P.parent/'publication_r5/book_v0_28_r5';audit={}
for lang in ['KO','EN']:
 src=old/f'MCC_3_0_Full_Book_{lang}_v0.28-r5.md';s=src.read_text();body=s[s.index('**v0.28-r4' if lang=='KO' else '**Prepared revision v0.28-r4'):]
 title='# 최소계산우주론 3.0\n\n## 개정판 v0.28-r6 준비본: 실행 보강·표기·판정 통합\n\n최원식 · 최정인 | 2026년 10월 22일\n\n' if lang=='KO' else '# Minimal Computing Cosmology 3.0\n\n## Prepared revision v0.28-r6: execution supplements, notation and decisions\n\nWonsik Choi · Jeongin Choi | 22 October 2026\n\n'
 notice='**현 판 안내.** 기존139장과 부록A–I를 보존하고 부록J에 이번1–3번 실행 보강과4번 표기 기준을 통합했다. 현재는 새 DOI가 없는 준비본이다. 이전 출판본 v0.28-r5: https://doi.org/10.5281/zenodo.23550759. 아래 판본 메모의 “현재/이번 판”은 각 기록 당시의 판을 뜻한다. PDF 북마크에서 장·절을 탐색할 수 있다. 상세 기호는 부록I·J, 실패 판정은 부록H·J를 따른다.\n\n**v0.28-r5 출판 이력.** SPARC 피팅과 수학 부록을 재검토하고38.B·139.3.1·122.1·H.7·부록I·139.5.3을 통합했다.\n\n' if lang=='KO' else '**Edition notice.** Preserve139 chapters and Appendices A–I; add the execution supplements from items1–3 and editorial conventions from item4 in Appendix J. This prepared edition has no new DOI. Preceding publication v0.28-r5: https://doi.org/10.5281/zenodo.23550759. “Current/this edition” in the historical notices below refers to the edition at the time of that notice. Use PDF bookmarks for navigation, Appendices I/J for notation and H/J for failure decisions.\n\n**v0.28-r5 publication history.** Reviewed SPARC fitting and mathematical notation; integrated38.B,139.3.1,122.1,H.7,Appendix I and139.5.3.\n\n'
 original_body=body;edits=[]
 if lang=='KO':
  for num in range(19,28):
   oldtext=f'- {num}. . ';newtext=f'- {num}. '
   if oldtext in body:body=body.replace(oldtext,newtext,1);edits.append((oldtext,newtext))
 oldtoc='- 부록 H. 반증조건·OPEN 연결과 한영 용어표' if lang=='KO' else '- Appendix H. Claim Tests, OPEN Connections and a Bilingual Glossary'
 if oldtoc not in body:
  oldtoc=next(l for l in body.splitlines() if l.startswith('- Appendix H'))
 newtoc=oldtoc+('\n- 부록 I. 수학 기호·텐서·핵심 연산자 대응표\n- 부록 J. 실행 보강과 표기·판정의 편집 기준' if lang=='KO' else '\n- Appendix I. Mathematical Notation, Tensors and Operators\n- Appendix J. Execution Supplements and Editorial Conventions')
 body=body.replace(oldtoc,newtoc,1);edits.append((oldtoc,newtoc))
 restored=body
 for a,b in reversed(edits):restored=restored.replace(b,a,1)
 assert restored==original_body
 (P/'review'/f'editorial_changes_{lang}.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2))
 addition=(P/'review'/f'add_{lang}.md').read_text();text=title+notice+body+addition
 dest=P/f'MCC_3_0_Full_Book_{lang}_v0.28-r6.md';dest.write_text(text)
 for f in [src,dest]:
  r=subprocess.run(['pandoc',str(f),'-f','markdown+autolink_bare_uris-implicit_figures','-t','json'],check=True,capture_output=True,text=True);(P/'review'/(f.stem+'.ast.json')).write_text(r.stdout)
 def collect(x,typ):
  if isinstance(x,dict):return ([x['c']] if x.get('t')==typ else [])+sum((collect(v,typ) for v in x.values()),[])
  if isinstance(x,list):return sum((collect(v,typ) for v in x),[])
  return []
 before=json.loads((P/'review'/(src.stem+'.ast.json')).read_text());after=json.loads((P/'review'/(dest.stem+'.ast.json')).read_text());bm=collect(before,'Math');am=collect(after,'Math');assert am[:len(bm)]==bm
 headers=collect(after,'Header');ids=[h[1][0] for h in headers];assert len(ids)==len(set(ids))
 images=collect(after,'Image');missing=[i[2][0] for i in images if not (P/i[2][0]).exists()];assert not missing,missing
 assert body in text and text.count(body)==1
 (P/'review'/f'heading_inventory_{lang}.json').write_text(json.dumps(headers,ensure_ascii=False,indent=2))
 (P/'review'/f'math_inventory_{lang}.json').write_text(json.dumps(am,ensure_ascii=False,indent=2))
 audit[lang]=dict(original_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),old_body_preserved_except_logged_toc_edits=True,logged_toc_edits=len(edits),inherited_math_nodes=len(bm),new_math_nodes=len(am)-len(bm),unique_heading_ids=len(ids),images=len(images),missing_images=missing)
(P/'review/EDITORIAL_AUDIT.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
