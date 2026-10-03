from pathlib import Path
import subprocess,sys,json,shutil,math
R=Path(__file__).resolve().parent;S=R/'studies'
summ=[];checks=[]
def ck(n,b):checks.append({'name':n,'passed':bool(b)})
for k in range(1,5):
 d=S/f'bridge_0_{k}'
 if k>2:shutil.copy2(S/f'bridge_0_{k-1}/results.json',d/'source'/f'bridge_0_{k-1}_results.json')
 p=subprocess.run([sys.executable,str(d/('audit_0_1.py' if k==1 else f'compute_0_{k}.py'))],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr+p.stdout)
 r=json.loads((d/('audit_results.json' if k==1 else 'results.json')).read_text())
 summ.append({'stage':f'0.{k}','passed':r['passed'],'failed':r['failed']})
 if r['failed']:raise AssertionError(r)
a=json.loads((S/'bridge_0_2/results.json').read_text());b=json.loads((S/'bridge_0_3/results.json').read_text());c=json.loads((S/'bridge_0_4/results.json').read_text())
for row in a['rows']:
 for species in ['proton','neutron']:
  for cal in ['inherited','alternate']:
   e=next(x for x in b['rows'] if x['case']==row['case'] and x['species']==species and x['calibration']==cal)
   ck(cal+' '+species+' '+row['case']+' SI propagation',math.isclose(e['excitation_total_J'],e['expected_population_input']*row['conditional_excitation_MeV']*b['unit_conversion_MeV_to_J'],rel_tol=1e-12))
   load=next(x for x in c['rows'] if x['a']==1 and x['boundary']=='external' and x['case']==row['case'] and x['species']==species and x['calibration']==cal)
   ck(cal+' '+species+' '+row['case']+' gravity propagation',math.isclose(load['E_J'],e['system_energy_J'],rel_tol=1e-12))
for cal in ['inherited','alternate']:
 for species in ['proton','neutron']:
  group=[x['E_J'] for x in c['rows'] if x['a']==1 and x['boundary']=='included_pressureless' and x['species']==species and x['calibration']==cal]
  ck(cal+' '+species+' internal exchange no extra total load',max(group)-min(group)<1e-22)
report={'version':'bridge-0.1-0.4-r1','stages':summ,'stage_case_checks':sum(x['passed'] for x in summ),'cross_checks':checks,'cross_passed':sum(x['passed'] for x in checks),'cross_failed':sum(not x['passed'] for x in checks),'count_scope':'implementation and mathematical case checks; repeated source checks not experiments','closure':'upstream 0.10; downstream 0.12; bridge 0.8 then consolidated 1.0'}
(R/'review_checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'stage_checks':report['stage_case_checks'],'cross_passed':report['cross_passed'],'cross_failed':report['cross_failed']}))
if report['cross_failed']:raise SystemExit(1)
