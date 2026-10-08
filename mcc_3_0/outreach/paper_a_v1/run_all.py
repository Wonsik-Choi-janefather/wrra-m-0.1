"""Run all three registered paper A audits and compare the fresh outputs."""
from pathlib import Path
import subprocess, sys, os, json, hashlib
if not __debug__:
    raise RuntimeError('Run without -O; inherited assertions are required.')
r=Path(__file__).resolve().parent
manifest=r/'SOURCE_SHA256.json'
if manifest.exists():
    for name,digest in json.loads(manifest.read_text()).items():
        if hashlib.sha256((r/name).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Source integrity failure: '+name)
env=dict(os.environ)
env['PYTHONPATH']=str(r/'vendor')+os.pathsep+env.get('PYTHONPATH','')
for p in ['audit_A.py','evidence/structural/dependencies/frozen_source_replay.py','evidence/structural/address_structure.py']:
    result=subprocess.run([sys.executable,str(r/p)],cwd=r,env=env,capture_output=True,text=True)
    (r/'evidence'/('run_'+Path(p).stem+'.log')).write_text(result.stdout+result.stderr)
    if result.returncode:
        raise RuntimeError(p+' failed; inspect corresponding evidence log')
a=json.loads((r/'evidence/audit_A_results.json').read_text())
s=json.loads((r/'evidence/structural/address_structure_results.json').read_text())
f=json.loads((r/'evidence/structural/dependencies/frozen_source_replay_results.json').read_text())
checks={
 'source_count':a['N']==1015000 and a['active_count']==1014999,
 'standard_count':a['C_nzeros']==70,
 'finite_contour_refinements':all(abs(x['winding']-70)<1e-9 for x in a['winding_checks']),
 'boundary_control':abs(a['lowered_boundary_winding']-69)<1e-9,
 'tail_mass_reference':abs(a['cutoff_comparison']['tail_mass_over_Znew']-7.883125509595178e-8)<1e-16,
 'structural_registered_checks':all(s['checks'].values()),
}
p0=list(f['unretuned_upstream_replay'][0]['address_shares'].values())
p1=list(f['unretuned_upstream_replay'][1]['address_shares'].values())
checks['frozen_share_bound']=max(abs(x-y) for x,y in zip(p0,p1))<=a['cutoff_comparison']['tail_mass_over_Znew']+1e-12
checks['frozen_values']=max(abs(x-y) for x,y in zip(p1,[.05000002538983289,.26800001828881304,.6819999563213559]))<5e-12
if not all(checks.values()): raise RuntimeError(str(checks))
(r/'evidence/REPLAY_STATUS.json').write_text(json.dumps({'status':'PASS','checks':checks,'scope':'Implementation and numerical replay, not interval certification or physical experiment.'},indent=2))
print(json.dumps(checks,indent=2))
