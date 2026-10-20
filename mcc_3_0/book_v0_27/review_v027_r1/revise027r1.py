from pathlib import Path
import re,json,hashlib,difflib,math
from fractions import Fraction
P=Path(__file__).resolve().parent.parent;R=P/'review_v027_r1';R.mkdir(exist_ok=True)
for L in ['KO','EN']:
 old=(P/f'MCC_3_0_Full_Book_{L}_v0.27.md').read_text()
 source=(P/f'source_summary_{L}.md').read_text();app=(P/f'appendixH_{L}.md').read_text()
 if L=='EN':
  heading=next(x for x in old.splitlines() if x.startswith('## Revision v0.27:'))
  replacement='## Revision v0.27-r1: SOURCE Traceability, Claim Tests and Terminology'
  note='''**v0.27-r1 editorial update · 21 October 2026.** Add a SOURCE construction table to Chapter 38 and Appendix H with the core falsification/OPEN register, module-boundary reading rules and Korean–English terminology. Clarify playback as execution of embodied relationships. Preserve all 138 chapters and earlier numerical results. This revision adds no scientific run, SPARC mass-bin diagnosis or Planck-scale error bound. Prior full book v0.27: https://zenodo.org/records/23511592.

'''
  ch39=next(x for x in old.splitlines() if x.startswith('# Chapter 39 '))
  archives='# Source archives and reproduction paths'
  playback='''**Execution and physical laws.** Playback means execution of relationships embodied in structure. It does not posit a previous completed calculation of the universe, an external computer or a prerecorded future. A Typed Ledger specifies types, owners and allowed updates; local causality and energy conservation additionally require the model's explicit event order, dynamics and supplier/recipient balance laws. Their implemented scope and remaining junctions are summarized in Appendix H.3.

'''
  anchor='**Minimal computation concerns the mode of execution more than the simplicity of the equations. A relationship already inscribed in structure need not be solved again during playback.**'
  toc='- 138. A live Galactic distribution function and the Gaia comparison'
  extra='- Appendix H. Claim tests, OPEN connections and bilingual glossary'
 else:
  heading=next(x for x in old.splitlines() if x.startswith('## 개정판 v0.27:'))
  replacement='## 개정판 v0.27-r1: SOURCE 구성·반증조건·용어의 추적성 보완'
  note='''**v0.27-r1 편집 보완 · 2026년 10월 21일.** 38장에 SOURCE 구성 요약표를 추가하고, 부록 H에 핵심 반증조건·OPEN 목록, 모듈 경계 읽기 규칙과 한영 용어표를 모았다. 재생은 구조에 구현된 관계의 실행임을 명확히 했다. 기존 138장과 수치 결과는 보존한다. 새 과학 계산·SPARC 질량별 잔차 진단·플랑크 영역 오차 한계를 추가한 판이 아니다. 이전 전체 책 v0.27: https://zenodo.org/records/23511592.

'''
  ch39=next(x for x in old.splitlines() if x.startswith('# 39장 '))
  archives='# 원본 자료와 재현 경로'
  playback='''**실행과 물리 법칙.** 재생은 구조에 구현된 관계의 실행이다. 우주를 미리 계산해 두었다거나 외부 컴퓨터 또는 사전 녹화된 미래를 가정하지 않는다. 타입 장부는 타입·소유권·허용 갱신을 명세하며, 국소 인과율과 에너지 보존에는 모형의 명시적 사건 순서·동역학·공급자/수신자 균형 법칙이 함께 필요하다. 실제 구현 범위와 남은 접합은 부록 H.3에 모았다.

'''
  anchor='**최소계산은 수식의 단순함보다 실행의 방식에 관한 생각이다. 이미 구조에 새겨진 관계는, 재생할 때 다시 풀 필요가 없다.**'
  toc='- 138. 살아 있는 은하 분포함수와 Gaia 비교'
  extra='- 부록 H. 반증조건·OPEN 연결과 한영 용어표'
 text=old.replace(heading,replacement,1)
 note_anchor='**v0.27 integration note.**' if L=='EN' else '**v0.27 통합 안내.**'
 text=text.replace(note_anchor,note+note_anchor,1)
 text=text.replace(ch39,'\\clearpage\n\n'+source+'\n\n'+ch39,1)
 text=text.replace(anchor,anchor+'\n\n'+playback.rstrip(),1)
 assert archives in text and toc in text
 text=text.replace(archives,'\\clearpage\n\n'+app+'\n\n\\clearpage\n\n'+archives,1).replace(toc,toc+'\n'+extra,1)
 (P/f'MCC_3_0_Full_Book_{L}_v0.27-r1.md').write_text(text)
 (R/f'changes_{L}.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),text.splitlines(True),fromfile='v0.27',tofile='v0.27-r1')))
 (R/f'Playback_{L}.md').write_text(playback)
 (R/f'Update_{L}.md').write_text(note)
 # Exact inverse of the six editorial insertions/title change must restore the whole baseline.
 restored=text.replace('\\clearpage\n\n'+app+'\n\n\\clearpage\n\n'+archives,archives,1).replace('\\clearpage\n\n'+source+'\n\n'+ch39,ch39,1).replace(anchor+'\n\n'+playback.rstrip(),anchor,1).replace(toc+'\n'+extra,toc,1).replace(note,'',1).replace(replacement,heading,1)
 assert restored==old,(L,'baseline changed')
 assert len(re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text))==48
 assert text.count('### 38.A')==1 and text.count('# Appendix H' if L=='EN' else '# 부록 H')==1
assert math.lcm(*[Fraction(x).denominator for x in ['0.05','0.268','0.682']])==500
assert 500*29*70==1015000 and 1015000-1==1014999
render=(P/'review_v027/render.sh').read_text().replace('v0.27.md','v0.27-r1.md').replace('v0.27.pdf','v0.27-r1.pdf')
(R/'render.sh').write_text(render)
(R/'EDITORIAL_AUDIT.json').write_text(json.dumps({'version':'Book v0.27-r1','baseline_inverse_verified':['KO','EN'],'all_prior_content_preserved':True,'figures_per_language':48,'lcm':500,'product':1015000,'active_addresses':1014999,'new_scientific_run':False,'changes':['Chapter 38 construction summary','Playback clarification','Appendix H claim tests and OPEN register','Bilingual glossary and scoped symbol rules']},indent=2)+'\n')
print('Both languages revised; exact inverse restores full v0.27 baseline')
