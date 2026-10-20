from pathlib import Path
import json,hashlib,difflib,shutil
HERE=Path(__file__).resolve().parent
P=HERE.parent; S=P.parent/'book_v0_26'
R=P/'review_v027';R.mkdir(exist_ok=True)
for lang in ['KO','EN']:
    old=(S/f'MCC_3_0_Full_Book_{lang}_v0.26.md').read_text()
    c137=(P/f'chapter137_{lang}.md').read_text();c138=(P/f'chapter138_{lang}.md').read_text()
    if lang=='EN':
        front='''# Minimal Computing Cosmology 3.0

## Revision v0.27: Particle/Color Interface and Live Galactic Dynamics

Wonsik Choi · Jeongin Choi | 21 October 2026

**v0.27 integration note.** Preserve the artistic opening and cumulative Chapters 1–136. Add Chapter 137 for the frozen component replay, exact singlet restriction and source-dependency audit through color manuscript v0.8.2; add Chapter 138 for the actual live WRRA–AGAMA v0.3 iteration and Gaia comparison. This book update reran the 36 replay/algebra checks and four dependency checks, and cross-checked released galactic records; it did not rerun the full AGAMA integration. Numerical closure and sample-level disagreement are both retained. Complete CAMB initial-state injection, mean-to-individual preparation and full selection-corrected Galactic validation remain open. WRRA retains its established name, Wonsik Reality–Renderer Architecture. The conflicting expansion in one source manuscript is disclosed in Section 137.1. Book series: https://doi.org/10.5281/zenodo.23202731. Previous book v0.26: https://doi.org/10.5281/zenodo.23492729. Code/data: GitHub; complete Korean/English PDFs: Zenodo.

'''
        cut='## Research Purpose and Design Principle:'
        marker='## Current synthesis — v0.26'
        synth='''## Current synthesis — v0.27

Verified inputs are the frozen finite address/admission/assembly rules, adopted charges and color representation, fixed Galactic response and trial stellar DFs, and declared public Gaia selections. WRRA-specific transformations are admission-weighted component assembly, dependency/information-retention audit, and a live residual-response/stellar-DF/Poisson iteration. Outputs are the reproduced conditional component statistics and exact singlet restriction (Chapter 137), two-resolution Galactic numerical closure and an actual Gaia comparison whose current count template disagrees with the data (Chapter 138). Falsification conditions are replay, conservation, dependency, kernel, convergence, invariant and properly population/selection-matched observational failures.

These extend the executable explanation and locate the remaining coupling and observational tasks. The 36+4 color checks were rerun for this book; the Galactic source records were checked without a new full AGAMA integration. No external review verdict, observational confirmation of the whole framework, new particle spectrum or completed cosmological state injection is inferred. Earlier achievements retain their declared contracts. The preceding v0.26 synthesis and earlier genealogy follow unchanged.

### Preserved synthesis through v0.26'''
        text=front+old[old.index(cut):]
        text=text.replace('Current Chapters 1–136.','Current Chapters 1–138.',1)
        toc='- 136. From residue seeds to finite emission, thermal history and observational calculation'
        text=text.replace(toc,toc+'\n- 137. Particle/component replay and the address–color interface\n- 138. A live Galactic distribution function and the Gaia comparison',1)
    else:
        front='''# 최소계산우주론 3.0

## 개정판 v0.27: 입자·색상 인터페이스와 살아 있는 은하 동역학

최원식 · 최정인 | 2026년 10월 21일

**v0.27 통합 안내.** 예술적 서두와 누적 1–136장을 보존한다. 137장은 색상 원고 v0.8.2까지의 동결 성분 재실행·정확한 싱글릿 제약·코드 의존성 감사를, 138장은 실제 WRRA–AGAMA v0.3 항성 반복과 Gaia 비교를 추가한다. 이번 갱신은 재현·대수 검사 36개와 의존성 검사 4개를 재실행하고 공개 은하 기록을 검산했으며, 전체 AGAMA 적분을 다시 수행하지 않았다. 수치 닫힘과 표본 비교의 불일치를 함께 보존한다. 전체 CAMB 초기상태 주입·평균–개별 우주 준비·선택 보정 은하 결합 검증은 열려 있다. WRRA의 기존 명칭 Wonsik Reality–Renderer Architecture를 유지하고 한 원전의 상충 표기는 137.1절에 밝힌다. 책 계열: https://doi.org/10.5281/zenodo.23202731. 이전 책 v0.26: https://doi.org/10.5281/zenodo.23492729. 코드·데이터는 GitHub, 한·영 전체 PDF는 Zenodo로 제공한다.

'''
        cut='## 연구 목적과 설계 원칙:'
        marker='## 현재 종합 — v0.26'
        if marker not in old:
            marker=next(x for x in old.splitlines() if x.startswith('## ') and 'v0.26' in x and ('종합' in x or '현재' in x))
        synth='''## 현재 종합 — v0.27

검증 입력은 동결 주소·허가·조립 규칙, 채택한 전하와 색상 표현, 고정 은하 응답과 시험 항성 DF, 선언한 공개 Gaia 선택이다. WRRA 고유 변환은 허가 가중 성분 조립, 의존성·정보 보존 감사 및 살아 있는 잔여 응답·항성 DF·포아송 반복이다. 산출은 137장의 조건부 성분 통계 재현과 정확한 싱글릿 제약, 138장의 두 해상도 은하 수치 닫힘과 현재 개수 틀이 자료와 맞지 않는 실제 Gaia 비교다. 반증조건은 재현·보존·의존성·공통 핵·수렴·불변량 및 인구집단·선택을 일치시킨 관측 검증의 실패다.

이는 실행 가능한 설명을 확장하고 남은 결합·관측 과제를 구체화한다. 색상 36+4 검사는 이번 책에서 재실행했고, 은하는 전체 AGAMA 재적분 없이 원전 기록을 검산했다. 외부 심사 판정·전체 체계의 관측 확증·새 입자 스펙트럼·우주론 전체 상태 주입 완료를 추론하지 않는다. 기존 성과는 선언한 계약을 유지한다. 아래에는 v0.26 종합과 이전 계보를 그대로 보존한다.

### v0.26까지의 종합 보존'''
        text=front+old[old.index(cut):]
        text=text.replace('1–136장','1–138장',1) if False else text
        # Only the current contents label changes; the integration note remains 1–136 preserved.
        text=text.replace('전권 1–136장','전권 1–138장',1).replace('현행 1–136장','현행 1–138장',1).replace('현재 1–136장','현재 1–138장',1)
        toc=next(x for x in text.splitlines() if x.startswith('- 136.'))
        text=text.replace(toc,toc+'\n- 137. 입자·성분 재실행과 주소–색상 인터페이스\n- 138. 살아 있는 은하 분포함수와 Gaia 비교',1)
    assert marker in text
    text=text.replace(marker,'\\clearpage\n\n'+c137+'\n\n\\clearpage\n\n'+c138+'\n\n'+synth,1)
    out=P/f'MCC_3_0_Full_Book_{lang}_v0.27.md';out.write_text(text)
    (R/f'changes_{lang}.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),text.splitlines(True),fromfile='v0.26',tofile='v0.27')))
    (R/f'Front_{lang}.md').write_text(front)
    (R/f'Synthesis_{lang}.md').write_text(synth.split('### ')[0])
    assert old[old.index('## Opening' if lang=='EN' else '## 서문'):old.index('\n---',old.index('## Opening' if lang=='EN' else '## 서문'))] in text if ('## Opening' if lang=='EN' else '## 서문') in old else True
status={'version':'Book v0.27','date':'2026-10-21','state':'built; publication pending','baseline_book':'10.5281/zenodo.23492729','baseline_repository_commit':'1070a2aab2d17bcd0b4978ba696f486868fdc055','color_source':'publication/WRRA_Color_Interface_Audit_v0_8_2','galaxy_source_commit':'3b49da87c27379e9637a53aa38e325f43808685d','new_chapters':[137,138],'color_checks_rerun':{'replay':36,'dependency':4},'full_AGAMA_rerun':False,'name':'Wonsik Reality–Renderer Architecture'}
(P/'PUBLICATION_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
(P/'README.md').write_text('# Minimal Computing Cosmology 3.0 — Book v0.27\n\nCurrent sources: MCC_3_0_Full_Book_KO_v0.27.md and MCC_3_0_Full_Book_EN_v0.27.md. Preserve v0.26 and earlier sources as genealogy.\n\nAdds Chapters 137–138: particle/color dependency and exact-singlet audit, and live AGAMA v0.3 numerical closure with the actual Gaia comparison. See PUBLICATION_STATUS.json for publication state. Code/data remain on GitHub; Zenodo book deposit carries only the two complete PDFs.\n\n36+4 color checks rerun; Galactic result records cross-checked, full AGAMA integration not rerun. No full observational-validation or external review verdict is claimed.\n')
# This script is retained in review_v027; do not overwrite itself.
print(status)
