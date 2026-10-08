from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
p=Path(__file__).resolve().parent.parent/'output/WRRA_Address_Particle_Interface_v0_2_EN.docx'
d=Document(p)
for para in list(d.paragraphs):
 br=para._p.xpath('.//w:br[@w:type="page"]')
 if br and not para.text.strip():para._p.getparent().remove(para._p)
d.save(p)
