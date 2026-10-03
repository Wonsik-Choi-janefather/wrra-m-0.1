"""Bilingual-source Korean PDF publication helper (ReportLab + NanumGothic)."""
from pathlib import Path
import re,html,os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,KeepTogether,PageBreak
ROOT=Path(__file__).resolve().parent;UP=ROOT.parent
OUT=Path(os.environ.get('WRRA_PDF_OUTPUT','output/pdf')).resolve();OUT.mkdir(parents=True,exist_ok=True)
fontdir=Path(os.environ.get('WRRA_FONT_DIR','/usr/local/share/fonts/wrra'))
pdfmetrics.registerFont(TTFont('Nanum',str(fontdir/'NanumGothic.ttf')))
pdfmetrics.registerFont(TTFont('NanumBold',str(fontdir/'NanumGothicBold.ttf')))
pdfmetrics.registerFontFamily('Nanum',normal='Nanum',bold='NanumBold',italic='Nanum',boldItalic='NanumBold')
width=A4[0]-96
styles={
 'body':ParagraphStyle('Body',fontName='Nanum',fontSize=9.5,leading=15,wordWrap='CJK',spaceAfter=6),
 'title':ParagraphStyle('Title',fontName='NanumBold',fontSize=18,leading=27,wordWrap='CJK',spaceAfter=16),
 'h2':ParagraphStyle('Heading',fontName='NanumBold',fontSize=12,leading=19,wordWrap='CJK',spaceBefore=10,spaceAfter=6,keepWithNext=True),
 'cell':ParagraphStyle('Cell',fontName='Nanum',fontSize=8.5,leading=13,wordWrap='CJK'),
 'head':ParagraphStyle('TableHead',fontName='NanumBold',fontSize=8.5,leading=13,wordWrap='CJK',textColor=colors.HexColor('#19344d'))}

def clean(t):
 t=t.replace('—','-').replace('–','-').replace('‑','-')
 t=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:m.group(1)+' ('+m.group(2)+')',t)
 t=t.replace('`','').replace('**','')
 return html.escape(t)

def build(source,name,version):
 lines=source.read_text().splitlines();story=[];i=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r'[:\-\s]+',c) for c in cells):rows.append(cells)
    i+=1
   n=len(rows[0]);weights=[.22,.78] if n==2 else ([.2]+[(.8)/(n-1)]*(n-1))
   formatted=[[Paragraph(clean(c),styles['head' if j==0 else 'cell']) for c in row] for j,row in enumerate(rows)]
   tab=Table(formatted,colWidths=[width*w for w in weights],repeatRows=1,hAlign='LEFT')
   tab.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eaf1f6')),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#6b879c')),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d5dfe6')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
   story.extend([KeepTogether([tab,Spacer(1,9)])]);continue
  if line.startswith('# '):style='title';text=line[2:]
  elif line.startswith('## '):
   style='h2';text=line[3:]
   if (version=='0.10' and text in ['같은 분모에서의 산출','에너지·전류와 하류 전달의 형 구분']) or (version=='0.9' and text=='실제 계산 산출') or (version=='0.8-r1' and text.startswith('0.8-r1 마무리')):
    story.append(PageBreak())
  else:
   style='body';text=line
   while i+1<len(lines) and lines[i+1].strip() and not lines[i+1].strip().startswith(('#','|')):
    i+=1;text+=' '+lines[i].strip()
  story.append(Paragraph(clean(text),styles[style]));i+=1
 def page(c,doc):
  c.saveState();c.setFont('Nanum',8);c.setFillColor(colors.HexColor('#516273'))
  c.drawString(48,A4[1]-30,'WRRA_M · 상류 '+version+' · 2026-10-03')
  c.setStrokeColor(colors.HexColor('#d5dfe6'));c.line(48,A4[1]-37,A4[0]-48,A4[1]-37)
  c.drawString(48,28,'최원식 Wonsik Choi · 조건부 유한 실행 모형')
  c.drawRightString(A4[0]-48,28,str(doc.page));c.restoreState()
 doc=SimpleDocTemplate(str(OUT/name),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=53,bottomMargin=48,title='WRRA_M upstream '+version,author='Wonsik Choi')
 doc.build(story,onFirstPage=page,onLaterPages=page)
 print(OUT/name)
if __name__=='__main__':
 build(UP/'shutter_v0_8/manuscript_KO.md','WRRA_M_Upstream_0_8_r1_KO_2026_10_03.pdf','0.8-r1')
 build(UP/'residue_current_v0_9/README.md','WRRA_M_Upstream_0_9_KO_2026_10_03.pdf','0.9')
 build(ROOT/'README.md','WRRA_M_Upstream_0_10_KO_2026_10_03.pdf','0.10')
