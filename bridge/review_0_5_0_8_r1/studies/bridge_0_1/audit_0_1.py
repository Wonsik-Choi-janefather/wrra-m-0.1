from pathlib import Path
import json, hashlib, math
R=Path(__file__).resolve().parent
c=json.loads((R/'bridge_contract_0_1.json').read_text())
h=json.loads((R/'source/upstream_0_9_handoff.json').read_text())
p=json.loads((R/'source/downstream_0_11_parameters.json').read_text())
d=(R/'source/downstream_synthesis_EN.md').read_text()
u=(R/'source/upstream_synthesis_EN.md').read_text()
b=c['baseline']; checks=[]
def test(name, ok):
    checks.append({'name':name,'passed':bool(ok)})
test('address shares normalized',math.isclose(sum(b['address_fractions']),1,abs_tol=1e-12))
test('resident Actual is .318',math.isclose(sum(b['address_fractions'][:2]),.318,abs_tol=1e-12))
for label in ['inherited','alternate']:
    f=b[label+'_energy_fractions']
    test(label+' energy shares normalized',math.isclose(sum(f),1,abs_tol=1e-12))
    test(label+' q follows pressureless phi,D and constant-density R',math.isclose((1-3*f[2])/2,b['q_'+label],abs_tol=1e-12))
test('upstream seconds remain unassigned',h['physical_time_unit'] is None)
test('upstream preparation excludes D,R', 'D and R remain outside nucleon preparation' in h['trace_contract'])
test('upstream energy supply not derived from norm','not supplied by dimensionless phi norm' in h['energy_contract'])
a=p['baseline_0_10']['upstream_0_9']['upstream']
test('same address cutoff',a['address_cutoff_N']==b['N'])
test('same exponent',math.isclose(a['state']['alpha'],b['alpha'],abs_tol=1e-14))
test('same frame convention',a['update']['frame_unit']=='dimensionless_order' and a['update']['admission_frames_K']==b['frames'])
test('downstream preserves failed clock identification','2.102556972196466' in d and 'fails identification' in d)
test('downstream records outcome implementation gap','Physical measurement outcomes, post-observation states and physical records remain unimplemented' in d)
test('upstream records physical persistence gap','stable physical record additionally needs a medium' in u)
report={'stage':'0.1','scope':'source-contract consistency, no new coupled dynamics','checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'sources_sha256':{str(x.relative_to(R)):hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted((R/'source').glob('*'))},'open_issues':[x for x in c['issues'] if x['status'] in ['open','failed-identification-preserved']]}
(R/'audit_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'passed':report['passed'],'failed':report['failed']}))
if report['failed']: raise SystemExit(1)
