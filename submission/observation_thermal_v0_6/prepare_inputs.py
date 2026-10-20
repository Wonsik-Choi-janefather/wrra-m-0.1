"""Extract frozen released data and fetch the hash-pinned reference implementation.
The upstream CosmoMC source is not redistributed in this package.
"""
from pathlib import Path
import json,hashlib,zipfile,urllib.request
P=Path(__file__).resolve().parent
def main():
    meta=json.loads((P/'PROVENANCE.json').read_text());folder=P/'inputs'
    archive=folder/'sptplanck_lenslike.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==meta['files'][archive.name]
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for n in z.namelist():
            if n.startswith('/') or '..' in Path(n).parts:raise ValueError('Unsafe data path')
        z.extractall(folder/'sptplanck')
    reference=folder/'CMBlikes_reference.py'
    expected=meta['files'][reference.name]
    if not reference.exists() or hashlib.sha256(reference.read_bytes()).hexdigest()!=expected:
        u=meta['sources']['likelihood_reference_pinned']
        data=urllib.request.urlopen(u,timeout=40).read()
        if hashlib.sha256(data).hexdigest()!=expected:raise ValueError('Reference source hash mismatch')
        reference.write_bytes(data)
    print('Frozen inputs and reference source verified')
if __name__=='__main__':main()
