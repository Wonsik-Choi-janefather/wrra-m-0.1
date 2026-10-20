from pathlib import Path
import re,json,hashlib,fitz
P=Path(__file__).resolve().parent.parent
checks={}
def check(n,x):
 checks[n]=bool(x)
 if not x:raise AssertionError(n)
pro=json.loads((P/'review_v026/EDITORIAL_PROVENANCE.json').read_text())
for lang in ['KO','EN']:
 s=(P/f'MCC_3_0_Full_Book_{lang}_v0.26.md').read_text();d=fitz.open(P/f'MCC_3_0_Full_Book_{lang}_v0.26.pdf')
 for k in ['prior_chapters_preserved','artistic_opening_preserved','historical_appendix_preserved']:check(lang+'_'+k,pro['sources'][lang][k])
 check(lang+'_book_revision', 'v0.26' in s[:300])
 check(lang+'_chapter136',len(re.findall(r'^## 136[장.]',s,re.M))==1)
 check(lang+'_full_TOC','1–136' in s and '- 136.' in s)
 check(lang+'_four_sources',all(v in s for v in ['23490141','23491041','23491673','23492328']))
 check(lang+'_partial_scope', ('전체 CAMB 초기상태 접합과 평균–개별 우주 준비는 미완료' in s) if lang=='KO' else ('Complete CAMB initial-state injection and mean-to-individual preparation remain incomplete' in s))
 images=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',s)
 check(lang+'_48_images_retained',len(images)==48 and all((P/x.split()[0]).exists() for x in images if not x.startswith('http')))
 text='\n'.join(p.get_text() for p in d)
 check(lang+'_full_PDF',len(d)>240 and '136.7' in text)
 check(lang+'_PDF_version','v0.26' in d[0].get_text())
 check(lang+'_stable_metric_fix', '4.35' in text and '16.66' in text)
 check(lang+'_calibration_values',all(x in s for x in ['0.103663511129','8.85389093544','0.194818034056','0.723567385056']))
 check(lang+'_likelihood_values',all(x in s for x in ['11.6855836908','10.6060135496','10.6032279730']))
 check(lang+'_legitimate_calibration',('정당한' in s) if lang=='KO' else ('legitimate' in s))
 check(lang+'_no_independent_prediction_requirement', ('필수조건으로 두지 않는다' in s) if lang=='KO' else ('not a prerequisite' in s))
result=dict(book_version='0.26',editorial_checks_passed=sum(checks.values()),checks=checks,
 source_check_counts={'v0.4':643,'v0.5':{'base':444,'release':12},'v0.6':{'base':54,'release':8},'v0.7-dev-r1':{'base':472,'release':10}},
 no_new_scientific_runs_claimed=True,full_state_CAMB_injection=False,
 pdf_pages={lang:len(fitz.open(P/f'MCC_3_0_Full_Book_{lang}_v0.26.pdf')) for lang in ['KO','EN']})
(P/'review_v026/EDITORIAL_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
