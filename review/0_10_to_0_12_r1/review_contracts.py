"""Cross-version review contracts and independent finite-step bound control."""
from pathlib import Path
import hashlib,importlib.util,json,math
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
def read(v,name='results/results.json'):return json.loads((REPO/f'calculations/wrra_m_0_{v}'/name).read_text())
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def run():
 baseline=json.loads((ROOT/'baseline_record.json').read_text());checks=[]
 def check(name,passed,evidence):
  item={'id':len(checks)+1,'check':name,'passed':bool(passed),'evidence':evidence};checks.append(item)
  assert passed,item
 skip=set(baseline['excluded_new_clock_metadata'])
 def scrub(x):
  if isinstance(x,dict):return {k:scrub(v) for k,v in x.items() if k not in skip}
  if isinstance(x,list):return [scrub(v) for v in x]
  return x
 rs={v:read(v) for v in (10,11,12)};vs={v:read(v,'results/verification.json') for v in rs}
 check('all_three_frozen_input_hashes_preserved',all(rs[v]['input_hash_sha256']==baseline['components'][str(v)]['input_sha256'] for v in rs),{str(v):rs[v]['input_hash_sha256'] for v in rs})
 fingerprints={str(v):digest(scrub(rs[v])) for v in rs}
 check('complete_pre_review_results_unchanged_except_added_clock_metadata',all(fingerprints[str(v)]==baseline['components'][str(v)]['original_result_fingerprint'] for v in rs),fingerprints)
 check('96_distinct_component_groups_pass',all(vs[v]['passed'] and vs[v]['check_count']==n for v,n in ((10,32),(11,28),(12,36))),{'component_groups':32+28+36})
 ratio=rs[12]['legacy_clock_comparison']['old_frequency_over_SI_frequency'];history=rs[10]['expansion_state_history']
 check('slow_clock_verdict_carried_back_to_all_expansion_rows',all(x['physical_SI_phase_identification'] is False and math.isclose(x['old_frequency_over_SI_frequency'],ratio,rel_tol=1e-13) for x in history),{'rows':len(history),'frequency_ratio':ratio})
 path=rs[12]['accelerated_worldline'];events=path['events']
 check('57_events_include_initial_point_and_56_completed_updates',len(events)==57 and events[0]['proper_frame']==0 and events[-1]['proper_frame']==path['complete_frames']==56 and 0<=path['residual_tick_fraction']<1,{'events':len(events),'completed_updates':path['complete_frames'],'residual':path['residual_tick_fraction']})
 H=np.array([[2.,1.,.5],[1.,-1.,.2],[.5,.2,3.]])
 hn=np.linalg.norm(H,2);bounds=[]
 for step in (.1,.05,.025,.0125):
  error=float(np.linalg.norm(1j*(expm(-1j*step*H)-np.eye(3))/step-H,2));bound=step*hn**2/2
  bounds.append({'positive_step':step,'norm_error':error,'bound':float(bound)})
 check('finite_step_bound_holds_for_independent_signed_Hermitian_control',all(x['norm_error']<=x['bound']*(1+1e-12) for x in bounds),{'eigenvalues':np.linalg.eigvalsh(H).tolist(),'controls':bounds})
 source={v:{l:(REPO/f'calculations/wrra_m_0_{v}/source_{l}.md').read_text() for l in ('ko','en')} for v in rs}
 check('clock_scope_explicit_in_both_editions_of_all_components',all(any(term in source[v]['ko'] for term in ('구성 일정','구성 시계','팽창 일정')) and 'SI' in source[v]['ko'] and 'SI' in source[v]['en'] and 'schedule' in source[v]['en'] for v in rs),{'editions_checked':6})
 check('review_identity_and_DOI_present_in_six_sources',all('23113101' in s and '0009-0001-4263-9772' in s and 'janefather@gmail.com' in s and f'0.{v}-r1' in s for v,langs in source.items() for s in langs.values()),{'DOI':'10.5281/zenodo.23113101','editions':6})
 documents={v:read(v,'results/document_checks.json') for v in rs}
 check('bilingual_native_equations_and_computed_tables_match',all(d['passed'] and d['native_equations_equal'] and d['tables_match_results'] for d in documents.values()),{'native_equations_per_edition':12+14+18,'bilingual_equations':2*(12+14+18),'pdf_pages':{str(v):{l:e['pdf_pages'] for l,e in d['editions'].items()} for v,d in documents.items()}})
 report={'release':'0.12-r1','passed':True,'review_check_count':len(checks),'component_check_groups':96,'checks':checks}
 (ROOT/'review_checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'review_checks':len(checks),'component_checks':96}))
if __name__=='__main__':run()
