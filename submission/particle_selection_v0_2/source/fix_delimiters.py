"""Preserve explicit square brackets and Dirac bars in Word/PDF rendering.
Run after the existing document reconstruction scripts.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
import sys

path = Path(sys.argv[1])
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
ns = {'m': M}
with ZipFile(path) as z:
    parts = {n: z.read(n) for n in z.namelist()}
root = E.fromstring(parts['word/document.xml'])
count = 0
def run(text):
    r = E.Element('{%s}r' % M)
    pr = E.SubElement(r, '{%s}rPr' % M)
    E.SubElement(pr, '{%s}sty' % M).set('{%s}val' % M, 'p')
    E.SubElement(r, '{%s}t' % M).text = text
    return r
for d in list(root.findall('.//m:d', ns)):
    pr = d.find('m:dPr', ns)
    if pr is None: continue
    b, e = pr.find('m:begChr', ns), pr.find('m:endChr', ns)
    if b is None or e is None: continue
    begin, end = b.get('{%s}val' % M), e.get('{%s}val' % M)
    if (begin, end) not in [('[', ']'), ('|', '|')]: continue
    contents = d.findall('m:e', ns)
    assert len(contents) == 1
    parent, pos = d.getparent(), d.getparent().index(d)
    nodes = [run(begin), *list(contents[0]), run(end)]
    parent.remove(d)
    for offset, node in enumerate(nodes): parent.insert(pos + offset, node)
    count += 1
parts['word/document.xml'] = E.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with ZipFile(path, 'w', ZIP_DEFLATED) as z:
    for n, data in parts.items(): z.writestr(n, data)
print('Explicit delimiter groups:', count)
