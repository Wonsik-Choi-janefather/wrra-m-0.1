from pathlib import Path
from docx import Document
R=Path(__file__).resolve().parent.parent
pairs=[('with fixed normalized address weights.','with normalized address weights that are independent of v in each candidate state. Identifiability is quantified over all such normalized address distributions, not just one fixed distribution.'),('The energy–pressure obstruction is the main design constraint for a next implementation.','The answer to the opening question is therefore twofold: sector totals suffice for energy only when the energy function is sectorwise constant, and they suffice for pressure only when its volume derivative is sectorwise constant. Equality at one reference point supplies the first property there without supplying the second. This energy–pressure obstruction is the main design constraint for a next implementation.')]
p=R/'output/WRRA_Address_Particle_Interface_v0_2_EN.docx';d=Document(p)
for para in d.paragraphs:
 for a,b in pairs:
  if a in para.text:
   para.text=para.text.replace(a,b)
d.save(p)
f=R/'source/build.py';s=f.read_text()
for a,b in pairs:s=s.replace(a,b)
f.write_text(s)
