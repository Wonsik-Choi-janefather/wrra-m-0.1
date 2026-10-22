from pathlib import Path
import fitz,json,re
P=Path(__file__).resolve().parent.parent;out={}
for lang in ['KO','EN']:
 path=P/f'MCC_3_0_Full_Book_{lang}_v0.28-r6.pdf';doc=fitz.open(path);meta=doc.metadata;meta.update(title=f'Minimal Computing Cosmology 3.0 v0.28-r6 ({lang})',author='Wonsik Choi; Jeongin Choi',subject='Complete book; notation and execution supplements; DOI 10.5281/zenodo.23551789',keywords='MCC 3.0; WRRA; v0.28-r6; release')
 doc.set_metadata(meta);doc.saveIncr();pages=[];outside=[]
 for i,page in enumerate(doc):
  t=page.get_text()
  if ('J.2' in t or 'J.4' in t or 'J.5' in t) and i>len(doc)-15:pages.append(i)
  for b in page.get_text('dict')['blocks']:
   for l in b.get('lines',[]):
    for s in l.get('spans',[]):
     x0,y0,x1,y1=s['bbox']
     if x0 < -1 or y0 < -1 or x1>page.rect.width+1 or y1>page.rect.height+1:outside.append({'page':i+1,'text':s['text'][:80],'bbox':s['bbox']})
 samples=sorted(set([0,len(doc)-1]+pages))
 for i in samples:doc[i].get_pixmap(matrix=fitz.Matrix(.9,.9)).save(P/'review'/f'{lang}_page_{i+1}.png')
 out[lang]=dict(pages=len(doc),bookmarks=len(doc.get_toc()),sample_pages=[i+1 for i in samples],outside_page_spans=outside,metadata=doc.metadata)
(P/'review/PDF_QA.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({k:{f:v[f] for f in ['pages','bookmarks','sample_pages','outside_page_spans']} for k,v in out.items()},ensure_ascii=False))
