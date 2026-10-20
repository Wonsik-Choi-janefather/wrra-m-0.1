from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
expected=json.loads((p/'INPUT_SHA256.json').read_text())
for name,digest in expected.items():
    if hashlib.sha256((p/name).read_bytes()).hexdigest()!=digest:
        raise SystemExit('Frozen input hash mismatch: '+name)
print('Frozen input audit passed:',len(expected),'files')
