from pathlib import Path
import json,hashlib
import pymupdf as fitz
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent.parent;R=P/'review_v027_r1';info={}
for L in ['KO','EN']:
 f=P/f'MCC_3_0_Full_Book_{L}_v0.27-r1.pdf';d=fitz.open(f);idx={0}
 for i,page in enumerate(d):
  if any(t in page.get_text() for t in ['38.A','H.1','H.2','H.3','H.4','Execution and physical laws','실행과 물리 법칙']):idx.update([i,min(i+1,len(d)-1)])
 idx=sorted(idx);tiles=[]
 for i in idx:
  pix=d[i].get_pixmap(matrix=fitz.Matrix(.7,.7));im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((430,620));tile=Image.new('RGB',(440,650),'#ddd');tile.paste(im,(5,22));ImageDraw.Draw(tile).text((5,3),f'{L} {i+1}',fill='black');tiles.append(tile)
 for start in range(0,len(tiles),6):
  chunk=tiles[start:start+6];sheet=Image.new('RGB',(1320,650*((len(chunk)+2)//3)),'white')
  for k,t in enumerate(chunk):sheet.paste(t,((k%3)*440,(k//3)*650))
  sheet.save(R/f'visual_{L}_{start//6}.jpg')
 text='\n'.join(p.get_text() for p in d).replace('\u2011','-')
 assert all(x in text for x in ['v0.27-r1','38.A','H.4'])
 info[L]={'pages':len(d),'bytes':f.stat().st_size,'md5':hashlib.md5(f.read_bytes()).hexdigest(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'review_pages':[i+1 for i in idx]}
(R/'PDF_VERIFICATION.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info))
