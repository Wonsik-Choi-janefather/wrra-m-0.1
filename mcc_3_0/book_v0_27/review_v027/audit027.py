from pathlib import Path
import re,json,hashlib,fitz
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent.parent;S=P.parent/'book_v0_26'; R=P/'review_v027'
checks={}; info={}
for L in ['KO','EN']:
 old=(S/f'MCC_3_0_Full_Book_{L}_v0.26.md').read_text();new=(P/f'MCC_3_0_Full_Book_{L}_v0.27.md').read_text()
 # Every old section after the introductory/contents area remains byte-identical.
 heading='## Chapter 1 One' if L=='EN' else '## **1장 '
 if heading not in old: heading=next(x for x in old.splitlines() if x.startswith('## ') and re.match(r'## 1[.장 ]',x))
 oldbody=old[old.index(heading):]
 current='## Current synthesis — v0.26' if L=='EN' else next(x for x in old.splitlines() if x.startswith('## ') and 'v0.26' in x and ('종합' in x or '현재' in x))
 main,tail=oldbody.split(current,1)
 checks[L+'_old_chapters_1_136_preserved']=main in new
 checks[L+'_old_synthesis_appendix_preserved']=tail in new
 checks[L+'_new_chapters_once']=all(new.count(f'## {n}. ' if L=='EN' else f'## {n}장 ')==1 for n in [137,138])
 imgs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',new)
 checks[L+'_images_resolve']=all((P/x).exists() for x in imgs if not x.startswith('http'))
 checks[L+'_name_preserved']='WRRA stands for Wonsik Reality' in new if L=='EN' else 'WRRA는 Wonsik Reality' in new
 checks[L+'_actual_limit_disclosed']='full AGAMA integration' in new if L=='EN' else '전체 AGAMA 적분' in new
 pdf=P/f'MCC_3_0_Full_Book_{L}_v0.27.pdf';d=fitz.open(pdf)
 selected=[0];newpages=[]
 for i,page in enumerate(d):
  t=page.get_text()
  if ('137.' in t or '138.' in t) and i>200:newpages.append(i)
 selected+=newpages
 checks[L+'_pdf_new_sections']=len(newpages)>=3
 checks[L+'_pdf_font_text']=all('\ufffd' not in d[i].get_text() for i in selected)
 info[L]={'pages':len(d),'bytes':pdf.stat().st_size,'md5':hashlib.md5(pdf.read_bytes()).hexdigest(),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'image_references':len(imgs),'review_pages':[i+1 for i in selected]}
 tiles=[]
 for i in selected:
  pix=d[i].get_pixmap(matrix=fitz.Matrix(.7,.7));im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
  tile=Image.new('RGB',(440,660),'#cccccc');im.thumbnail((430,630));tile.paste(im,(5,22));ImageDraw.Draw(tile).text((8,4),f'{L} page {i+1}',fill='black');tiles.append(tile)
 sheet=Image.new('RGB',(440*3,660*((len(tiles)+2)//3)),'white')
 for k,tile in enumerate(tiles):sheet.paste(tile,((k%3)*440,(k//3)*660))
 sheet.save(R/f'visual_{L}.jpg')
v=json.loads((R/'galaxy_validation.json').read_text());obs=json.loads((R/'galaxy_observations.json').read_text())
delta=abs(v['refined']['midplane_total_density_Msun_pc3']-v['base']['midplane_total_density_Msun_pc3'])/v['refined']['midplane_total_density_Msun_pc3']
checks['galaxy_midplane_percent']=abs(delta*100-.034372510372238096)<1e-10
checks['galaxy_count_validation_open']=obs['full_star_count_and_velocity_validation_passed'] is False
checks['galaxy_count_deviance']=abs(obs['direct_DR3']['geometry_only_folded_count_poisson_deviance']-1747.2021268516487)<1e-9
audit=json.loads((R/'rerun_audit_results.json').read_text());dep=json.loads((R/'rerun_dependency_results.json').read_text())
checks['color_rerun_36']=audit['passed']==audit['total']==36
checks['dependency_rerun_4']=dep['passed']==dep['total']==4
report={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'pdfs':info,'scope':'Editorial preservation, source-record verification and 36+4 actual color rerun; no full AGAMA integration rerun.'}
(R/'AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps(report,indent=2,ensure_ascii=False));assert all(checks.values())
