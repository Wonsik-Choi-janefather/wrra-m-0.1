from pathlib import Path
import re,json,hashlib,shutil
P=Path(__file__).resolve().parent.parent
BASE=P/'review/baseline';BASE.mkdir(exist_ok=True)
UP=Path('/workspace/scratch/32eba3ce3073/wrra/mcc_3_0/book_v0_28')
URL='https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/e5a833afd65c282b06fa1318467362de90156338/mcc_3_0/chapter_132_134_recovery_2026_10_22'
DOI='https://doi.org/10.5281/zenodo.23549809'
notes={
'KO':{
'front':f'''**v0.28-r1 실행 근거 보완 · 2026년 10월 22일.** 132–134장의 원전 ZIP 다섯 개를 v0.24 완전 패키지에서 복구하고, 원전 주 계산 다섯 개의 실제 재실행 결과를 본문과 부록 H.6에 반영했다. 과거 출력이 보존된 네 프로그램의 JSON 일치, 원전 내부 파일 25개의 해시 일치와 격리 훼손 시험의 실패 탐지를 확인했다. 선언한 구조·변환을 통한 알려진 값의 재현은 WRRA의 구현·설명 성과다. 기존 139장과 수치·예술적 서두를 보존하며 전체 3.0 실행 검증이나 실제 xi의 전 차수 양성 증명을 뜻하지 않는다. 이번 판 DOI: {DOI}. 이전 판: https://doi.org/10.5281/zenodo.23524780.\n\n''',
132:'''#### 132.6 원전 복구와 정확 계산 재실행 (2026-10-22)

**검증 입력.** v0.24 완전 패키지에서 회수한 소수 관계·양성 v0.4 및 성장 강화 v0.8의 원본 ZIP과 그 안의 정확 유리수 코드다. 실제 xi 계수를 새로 수치 적분한 입력은 아니다.

**WRRA 고유 변환.** 선언한 모멘트에서 로그미분 관계 계수를 구성해 Hankel 행렬식으로 읽고, 별도 소유의 성장 제약 커널에서는 이차형식의 음의 증거 구간을 구성한다.

**산출값.** `exact_check.py`는 행렬식 3/25와 −223/70000을 재현했다. `certify_double_exponential_counterkernel.py`의 증거 구간은 약 [−8.750604288241009×10⁻⁹, −8.750061502880118×10⁻⁹]로, 상한이 −1/200000000보다 작다. 두 원전 프로그램은 종료코드 0이며 성장 커널의 JSON 출력은 2026-10-17 기록과 일치했다. 정확 유리수 구간이 인증 대상이고 소수 표시는 읽기용이다.

**반증조건.** 계수·행렬식·구간 산술의 실패 또는 보존된 원전·출력과의 불일치다. 별도 커널을 실제 theta의 반례로 바꾸어 해석할 수 없다.

**결론.** 본 장이 구별한 양성 조건과 증명 간극의 유한 대조를 실제 원전으로 재현했다. 실제 xi의 전 차수 양성과 RH는 계속 열려 있다. 원전과 명령·로그는 부록 H.6에서 연결한다.
''',
133:'''#### 133.4 원천 투영과 보정 이득의 재실행 (2026-10-22)

**검증 입력.** 공통 영점 영상 v0.11과 홀수 합성수 영상 v0.10 원전의 유한 주소 및 명시된 진단용 beta 값이다. 진단값은 실제 제타 영점 측정치가 아니다.

**WRRA 고유 변환.** 소수의 곱 생성으로 홀수 주소를 구성하고 합성수 성분을 투영한다. 이어 공통 보정 중심에 따른 성분 이득을 계산해 중심의 최적성과 모든 성분의 노름 보존을 구별한다.

**산출값.** `analyze_odd_hologram.py`에서 N=1000의 정확 투영 및 Euler 주소 일치 검사가 통과했다. `projector_contract.py`에서 중앙 성분의 최악 이득은 1, 대칭적인 선 밖 진단 성분의 중앙 최악 이득은 2, 두 바깥 중심에서는 각각 4다. 켤레 이득 곱 1과 산술평균 5/4도 정확히 재현했다. 두 프로그램의 종료코드는 0이고 JSON 출력은 과거 기록과 일치했다.

**반증조건.** 주소 중복·누락, 투영 항등식 또는 보정 이득 계산의 실패다.

**결론.** 원천→선택→공통 보정이라는 구조 연결의 유한 계산을 재현했다. 실제 xi에서 전 성분의 노름 보존을 도출하는 의무와 물리적 영상 측정은 별도로 남는다.
''',
134:'''#### 134.5 대비·비용의 원전 실행 확인 (2026-10-22)

**검증 입력.** 모든 자연수 선명도 v0.1의 선언된 상보 채널과 N=16, 128, 1000이다.

**WRRA 고유 변환.** 같은 주소의 두 상보 진폭을 모드별 에너지·기준 위상 대비로 읽고, 유리수 바깥 구간으로 유한 합의 비용과 대비를 계산한다.

**산출값.** `clarity_analysis.py`는 종료코드 0이며 과거 JSON 출력과 인증서를 재현했다. N=1000에서 중앙 모드 비용은 14.97094172110069, 대비는 1이다. 양 끝점 비용은 1001.6439345666815, 대비는 0.014946370865388635다. 이 값은 앞 표의 표시 정밀도와 일치한다.

**반증조건.** 상보 진폭 규칙·주소별 합·구간 경계 또는 기록된 산출값의 불일치다. 원시 강도 영상과 모드별 에너지 합을 혼동하면 적용 조건을 벗어난다.

**결론.** 선언한 WRRA 판독 안에서 최대 대비와 최소 모드 비용의 정합성을 재현했다. 현실의 광학 화질을 새로 측정하거나 전체 제타의 영점을 증명한 결과로 확대하지 않는다.
''',
'appendix':f'''## H.6 v0.28-r1: 132–134장 원전과 실행 근거의 복구

**검증 입력.** 원본 `MCC_3_0_Book_v0.24_Projector_Focus_Complete_Package.zip`(76,970,934바이트)에서 R1–R5 원전 다섯 개를 바이트 그대로 복구했다. 원본 SHA-256은 `09e8f19d163931792b501e36ba6f070d2745916065a592925bfd829cf3072b93`이다. 공개 v0.25 게시 커밋에는 본문은 있었지만 두 원전 폴더가 빠져 있었고, 후속 본문에는 보존 문구가 남았다. 파일 선택이 누락된 구체적인 당시 이유는 확인되지 않았다.

**WRRA 고유 변환.** 132장의 관계계수·이차형식, 133장의 주소 투영·공통 보정, 134장의 상보 모드 대비·비용을 원전 코드로 각각 재생한다. 다섯 계산의 입력·변환·판정을 하나의 원전 계보와 실행 기록으로 연결한다.

**산출값.** 주 계산 5/5가 종료코드 0, 과거 stdout이 있는 4/4가 JSON 일치, 원전 내부 파일 25개의 해시가 일치했다. 새 임시 폴더에서도 원전 프로그램을 실행하고 산출·인증서를 대조했다. 이 개수는 유한 프로그램과 파일 검사 수이며 독립 실험 수가 아니다. 실제 실행 파일은 132.6, 133.4, 134.5절에 명시했다.

**반증조건.** 별도 재현 실행기 `reproduce.py`는 원전 ZIP·보존 출력의 SHA-256, 원전 내부 manifest, 프로세스 종료코드, JSON 출력 및 인증서를 검사한다. 격리한 복사본 ZIP에 바이트를 덧붙이자 `ARCHIVE_OR_RECORD_HASH_MISMATCH`와 종료코드 1로 거부했다. 중첩 과거 연구 전체와 본문의 모든 해석적 논증을 다시 검증한 것은 아니다.

**결론.** 누락 원전은 공개 복구됐으며 해당 유한 계산은 재현됐다. 기존 전체 감사의 ‘132–134장 원전 미확보’ 항목은 해소된다. 다른 모듈의 연결 실패나 미실행 항목까지 해소됐다고 판정하지 않는다. 전체 3.0 실행 검증의 완료 여부와 이 복구의 성과는 별도로 기록한다.

[고정 커밋의 원전·실행기·실제 로그]({URL}). 해당 폴더에서 `python reproduce.py`로 재현한다. `PROVENANCE.json`, `SHA256SUMS.json`, `REPLAY_RESULT.json`, `NEGATIVE_TEST.json` 및 `runs_2026_10_22/`가 근거다. 2026-10-17 기록은 `verification/`에 구분 보존한다. 역사적 R1–R5의 상대 링크도 book_v0_25–book_v0_28에 복구됐다.
'''
},
'EN':{
'front':f'''**v0.28-r1 execution evidence update · 22 October 2026.** Five original ZIPs cited in Chapters 132–134 were recovered from the v0.24 complete package. Their five top-level finite programs were replayed and the results are incorporated in those chapters and Appendix H.6. Four available historical JSON outputs match; 25 original internal file hashes match; an isolated corruption is rejected. Reproduction through declared WRRA structures and transformations is an implementation and explanatory achievement. All 139 chapters, earlier values and artistic opening are retained. This does not establish whole-MCC execution or actual all-order xi positivity. This edition: {DOI}. Previous edition: https://doi.org/10.5281/zenodo.23524780.\n\n''',
132:'''#### 132.6 Recovered originals and exact replay (2026-10-22)

**Verified inputs.** Original Prime Relations/Positivity v0.4 and Growth Barrier v0.8 ZIPs recovered from the v0.24 complete package, with their exact rational programs. These inputs are not a fresh numerical integration of actual xi coefficients.

**WRRA transformation.** Declared moments produce logarithmic-derivative relation coefficients and Hankel determinants. A separately owned growth-constrained kernel produces a negative quadratic-form enclosure.

**Outputs.** `exact_check.py` reproduces determinants 3/25 and −223/70000. `certify_double_exponential_counterkernel.py` yields an interval approximately [−8.750604288241009×10⁻⁹, −8.750061502880118×10⁻⁹], strictly below −1/200000000. Both programs exit 0; the growth-kernel JSON matches the 2026-10-17 replay. Exact rational intervals carry the certificate; decimals are displays.

**Falsification conditions.** Failed coefficient, determinant or interval arithmetic, or disagreement with preserved sources/results. The separate kernel cannot be reinterpreted as a counterexample for actual theta.

**Conclusion.** The finite diagnostics separating positivity properties and the remaining proof gap are reproduced from their original code. Actual all-order xi positivity and RH remain open. Appendix H.6 links the sources, commands and logs.
''',
133:'''#### 133.4 Replay of source projection and compensated gains (2026-10-22)

**Verified inputs.** Common-Zero Image v0.11 and Odd-Composite Image v0.10 originals, finite addresses and declared diagnostic beta values. The diagnostic values are not measured zeta zeros.

**WRRA transformation.** Prime products construct odd addresses and project composite components. Common-center compensation then distinguishes minimax centering from componentwise norm preservation.

**Outputs.** `analyze_odd_hologram.py` passes exact projection and Euler-address agreement at N=1000. `projector_contract.py` reproduces worst gain 1 for a centered component, central worst gain 2 for the symmetric off-line diagnostic and gain 4 at each outer center. The conjugate gain product is 1 and arithmetic mean 5/4. Both programs exit 0 and their JSON outputs match the historical records.

**Falsification conditions.** Duplicate or missing addresses, failed projection identity or incorrect compensated gains.

**Conclusion.** The finite source→selection→common-compensation connection is reproduced. Deriving componentwise norm preservation from actual xi and measuring physical image quality remain distinct tasks.
''',
134:'''#### 134.5 Original execution of visibility and cost (2026-10-22)

**Verified inputs.** All-Natural Clarity v0.1, its declared complementary channels and N=16, 128, 1000.

**WRRA transformation.** Same-address complementary amplitudes are read as mode energy and reference-phase visibility. Outward rational intervals evaluate finite costs and visibility.

**Outputs.** `clarity_analysis.py` exits 0 and reproduces the historical JSON and certificate. At N=1000, central pair energy is 14.97094172110069 and visibility is 1. Endpoint energy is 1001.6439345666815 and visibility is 0.014946370865388635, agreeing with the displayed precision in the preceding table.

**Falsification conditions.** Failure of the complementary-amplitude contract, address sums, interval enclosure or recorded outputs. Equating raw coherent pixel intensity with a mode-energy sum violates the readout conditions.

**Conclusion.** Maximum visibility and minimum mode cost are reproduced within the declared WRRA readout. This does not constitute a new optical-quality measurement or a proof about all zeta zeros.
''',
'appendix':f'''## H.6 v0.28-r1: recovery of Chapters 132–134 sources and execution evidence

**Verified inputs.** Five R1–R5 ZIPs were recovered byte-for-byte from `MCC_3_0_Book_v0.24_Projector_Focus_Complete_Package.zip` (76,970,934 bytes), SHA-256 `09e8f19d163931792b501e36ba6f070d2745916065a592925bfd829cf3072b93`. The public v0.25 publication commit contained the book text but omitted two source directories, while later editions retained the preservation statements. The precise historical reason for that selection omission is unknown.

**WRRA transformation.** Replay Chapter 132 relation coefficients/quadratic forms, Chapter 133 address projection/common compensation and Chapter 134 complementary-mode visibility/cost. Connect their inputs, transformations and decisions to one preserved source genealogy and execution record.

**Outputs.** All 5/5 top-level programs exit 0; all 4/4 available historical stdout JSONs match; 25 original internal file hashes match. A clean temporary-directory replay compares actual outputs and certificates. These are finite program/file checks, not independent experiments. Sections 132.6, 133.4 and 134.5 name the executed programs.

**Falsification conditions.** The separate `reproduce.py` runner checks source ZIP/result SHA-256 values, original internal manifests, process status, JSON outputs and certificates. Appending bytes to a ZIP in an isolated copy triggers `ARCHIVE_OR_RECORD_HASH_MISMATCH` and exit code 1. Not all nested historical programs or analytic arguments were reverified.

**Conclusion.** The original sources are publicly recovered and the cited finite computations are reproduced. The earlier full-audit limitation “Chapters 132–134 source packages unavailable” is resolved. Other module-interface failures and unexecuted items are not thereby resolved. Whole-MCC execution status remains distinct from this recovery result.

[Version-pinned originals, replay runner and actual logs]({URL}). Run `python reproduce.py` in that directory. Evidence is in `PROVENANCE.json`, `SHA256SUMS.json`, `REPLAY_RESULT.json`, `NEGATIVE_TEST.json` and `runs_2026_10_22/`; historical 2026-10-17 records remain separate under `verification/`. Historical R1–R5 relative paths were also restored for book_v0_25–book_v0_28.
'''
}}
audit={}
for L,n in notes.items():
 name=f'MCC_3_0_Full_Book_{L}_v0.28.md'
 if not (BASE/name).exists():shutil.copy2(UP/name,BASE/name)
 old=(BASE/name).read_text();text=old;changes=[]
 def replace(a,b):
  global text
  assert text.count(a)==1,(L,a[:60],text.count(a));text=text.replace(a,b,1);changes.append([a,b])
 title=old.splitlines()[2];replace(title,title.replace('v0.28:','v0.28-r1:')+(' — 132–134장 원전 재현' if L=='KO' else ' — Recovered Sources and Replay for Chapters 132–134'))
 date='최원식 · 최정인 | 2026년 10월 21일' if L=='KO' else 'Wonsik Choi · Jeongin Choi | 21 October 2026'
 replace(date,date.replace('21','22')+'\n\n'+n['front'].strip())
 for chapter in [132,133,134]:
  nextheading=next(x for x in text.splitlines() if re.match(r'^## '+str(chapter+1)+r'(?:장 |[. ]+)',x))
  replace(nextheading,n[chapter]+'\n\n'+nextheading)
 # Append evidence supplement without moving inherited text.
 text+='\n\n\\clearpage\n\n'+n['appendix'];changes.append(['','\n\n\\clearpage\n\n'+n['appendix']])
 reverse=text
 for a,b in reversed(changes):
  assert reverse.count(b)==1;reverse=reverse.replace(b,a,1)
 assert reverse==old
 # Point recovered evidence links at the immutable public source, retaining historical statements.
 out=P/f'MCC_3_0_Full_Book_{L}_v0.28-r1.md';out.write_text(text)
 (P/'review'/f'additions_{L}.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
 audit[L]={'baseline_sha256':hashlib.sha256(old.encode()).hexdigest(),'new_sha256':hashlib.sha256(text.encode()).hexdigest(),'exact_inverse_restores_v028':True,'original_image_refs':len(re.findall(r'!\[.*?\]\(.*?\)',old)),'new_image_refs':len(re.findall(r'!\[.*?\]\(.*?\)',text))}
(P/'review/INTEGRATION_AUDIT.json').write_text(json.dumps(audit,indent=2))
print(json.dumps(audit,indent=2))
