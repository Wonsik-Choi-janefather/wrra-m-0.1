from pathlib import Path
import json,html
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

ROOT=Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont('Nanum',str(ROOT/'fonts/NanumGothic-Regular.ttf')))
pdfmetrics.registerFontFamily('Nanum',normal='Nanum',bold='Nanum',italic='Nanum',boldItalic='Nanum')
CONTENT=json.loads((ROOT/'manuscript.json').read_text())
INK=HexColor('#172b43'); BLUE=HexColor('#245879'); PALE=HexColor('#eef4f7')

def build(lang):
    ko=lang=='KO'; font='Nanum'
    styles={
     'body':ParagraphStyle('body',fontName=font,fontSize=10.1,leading=15.4,textColor=INK,spaceAfter=8,wordWrap='CJK' if ko else None),
     'title':ParagraphStyle('title',fontName=font,fontSize=21 if ko else 20,leading=27,textColor=INK,spaceAfter=13,wordWrap='CJK' if ko else None),
     'sub':ParagraphStyle('sub',fontName=font,fontSize=11.2,leading=17,textColor=BLUE,spaceAfter=12,wordWrap='CJK' if ko else None),
     'h':ParagraphStyle('h',fontName=font,fontSize=12,leading=18,textColor=BLUE,spaceBefore=9,spaceAfter=6,keepWithNext=True),
     'math':ParagraphStyle('math',fontName=font,fontSize=10,leading=17,textColor=BLUE,spaceAfter=10,spaceBefore=4),
     'cell':ParagraphStyle('cell',fontName=font,fontSize=9.1,leading=13,textColor=INK,wordWrap='CJK' if ko else None)}
    def para(text, style):
        if ko:
            for char in 'öΠΣαβγξσ':
                text=text.replace(char,'<font name="Helvetica">'+char+'</font>')
        return Paragraph(text,style)
    story=[]
    for page_index,page in enumerate(CONTENT[lang]):
        if page_index:story.append(PageBreak())
        story.append(para(page['title'],styles['title']))
        if 'subtitle' in page:story.append(para(page['subtitle'],styles['sub']))
        for kind,text in page['blocks']:
            if kind=='table':
                cells=[[para(html.escape(x),styles['cell']) for x in row] for row in text]
                cols=len(cells[0]); widths=([173,165,145] if cols==3 else [323,160])
                table=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
                table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('LINEBELOW',(0,0),(-1,0),.8,BLUE),('LINEBELOW',(0,1),(-1,-1),.25,HexColor('#d2dce3')),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),8),('VALIGN',(0,0),(-1,-1),'TOP')]))
                story.extend([table,Spacer(1,10)])
            else:
                style=styles['body' if kind=='p' else kind]
                story.append(para(text,style))
    out=ROOT/f'WRRA_Number_Dimension_Layers_v0_1_{lang}_2026-10-16.pdf'
    def decoration(c,doc):
        w,h=A4;c.setStrokeColor(BLUE);c.setLineWidth(.8);c.line(56,h-40,w-56,h-40)
        c.setFont('Nanum',8);c.setFillColor(BLUE)
        c.drawString(56,h-31,'WRRA | Number-Dimension Layers | v0.1')
        c.drawString(56,30,'Wonsik Choi | 2026-10-16 | CC BY 4.0')
        c.drawRightString(w-56,30,str(doc.page))
    doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=56,leftMargin=56,topMargin=58,bottomMargin=48,title=CONTENT[lang][0]['title'],author='Wonsik Choi',subject=CONTENT[lang][0]['subtitle'])
    doc.build(story,onFirstPage=decoration,onLaterPages=decoration)
    return out

if __name__=='__main__':
    for lang in ['KO','EN']: print(build(lang))
