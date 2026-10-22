from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
rows=(root/'SHA256SUMS.txt').read_text().splitlines()
for row in rows:
    digest,path=row.split('  ',1)
    actual=hashlib.sha256((root/path).read_bytes()).hexdigest()
    assert actual==digest,path
print(f'{len(rows)} file hashes verified')
