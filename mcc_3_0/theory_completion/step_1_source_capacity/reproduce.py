"""Replay the reviewed research package and compare its registered outputs."""
from pathlib import Path
import json,math,subprocess,sys

ROOT=Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError('Run without -O.')
paths=['results.json','capacity_transport_results.json']
registered={name:json.loads((ROOT/name).read_text()) for name in paths}
for script in ('audit.py','capacity_transport.py'):
    process=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,capture_output=True,text=True)
    if process.returncode:
        print(process.stdout);print(process.stderr,file=sys.stderr)
        raise SystemExit(process.returncode)
    print(script+': PASS')
current={name:json.loads((ROOT/name).read_text()) for name in paths}
assert current['results.json']==registered['results.json']
actual=current['capacity_transport_results.json']
old=registered['capacity_transport_results.json']
assert actual['status']=='PASS' and all(actual['checks'].values())
assert actual['source_provenance']==old['source_provenance']
assert actual['frozen_input_hash']==old['frozen_input_hash']
assert len(actual['branches'])==len(old['branches'])
for new_branch,old_branch in zip(actual['branches'],old['branches']):
    assert new_branch['N']==old_branch['N'] and new_branch['counts']==old_branch['counts']
    for new_row,old_row in zip(new_branch['macro']['rows'],old_branch['macro']['rows']):
        for name in ('density_J_m3','pressure_Pa','q','H_over_H0','aT_m_s2','rotation_km_s','lensing_arcsec'):
            assert math.isclose(new_row[name],old_row[name],rel_tol=1e-9,abs_tol=1e-20),(name,new_row[name],old_row[name])
print('Registered arithmetic and macro outputs reproduced; all '+str(len(actual['checks']))+' checks passed.')
