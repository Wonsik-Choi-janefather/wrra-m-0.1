from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak
from reportlab.lib import colors
R=Path(__file__).resolve().parent
font=Path('/usr/local/share/fonts/wrra/NanumGothic.ttf')
if not font.exists():font=Path('/usr/share/fonts/truetype/nanum/NanumGothic.ttf')
pdfmetrics.registerFont(TTFont('Body',str(font)))
PAGES={
'KO':[
('상하류 연결 연구 0.1-0.4 | 검토 r1',[
'Wonsik Choi · Jeongin Choi | 2026-10-03 | CC BY 4.0',
'DOI: 10.5281/zenodo.23119802',
'이 자료집은 상류 0.10과 하류 0.12 사이의 연결을 단계별로 구현·검토한다. 기존 마감을 유지하며 연결 연구는 0.8에서 끝내고 1.0은 통합 확정판으로 둔다.',
'0.1: 상태·단위·정규화와 열 개 쟁점의 전달 규약. 0.2: 주소별 조건부 핵자 상태와 주변 상태의 곱 비교. 0.3: SI 에너지 교체와 유한 환경 교환. 0.4: 같은 에너지의 압력과 균일 팽창.',
'검토 후 사례별 검사: 0.1 15개, 0.2 95개, 0.3 134개, 0.4 600개. 단계 간 추가 검사 36개. 합계 880개는 구현·수학 검사이며 실험 수가 아니다.',
'수정: 비유한 값·음수·공급 부족 교환을 거부하고, 결합 블록 trace 검사를 추가했다. 0.2 근거 해시는 실제 포함한 의존 소스로 한정했다. 새 단계 출력이 다음 단계 입력으로 전달되도록 전체 실행기를 추가했다.',
'판정: 공개한 가정 아래 상태·에너지·균일 부하의 연결을 실행했다. 준비 장치, 실제 공급 기원, 물리 프레임 시계, 영속 기록 및 비균질 공변 동역학은 미해결이다.']),
('1 | 연결 규약과 상태 비교',[
'주소 비중 5%/26.8%/68.2%와 SI 에너지 비중 4.93%/26.5%/68.57%는 다른 측도이다. 응답 보정 없이 같다고 두지 않는다. 잔존 Actual 31.8%와 반환을 포함한 전체 장부 100%도 범위가 다르다.',
'0.2는 phi 조건부 주소 n=2..1,000,000에 대해 다음 고전-양자 블록을 실행했다. D와 반환은 기존 분기 장부에 보존하며 핵자 준비를 적용하지 않는다.',
'Sigma_phi = sum_n p(n|phi) |n><n| x rho_internal(n) x I_128/128',
'rho_internal(n) = (1-0.2 chi(n)) |g><g| + 0.2 chi(n) |e1><e1|',
'chi(n)는 소수 3의 지수 홀수 여부이다. 실제 내부 기저는 95차원이며 두 고정 모드로 블록을 표현한다. 128차원 운반자는 정상 혼합 상태이다. 일반 얽힘이나 주소 코히런스 보존을 구현한 것으로 해석하지 않는다.',
'주소에 무관한 내부 H와 전류에서는 결합 상태와 주변 상태의 곱이 같은 기대값을 준다. 주소 가중 관측량에는 차이가 생긴다. r(n)=1+0.25 log(n)/log(N)의 에너지 진단 차이는 기준 0.1447722277 MeV이다.',
'이 차이는 a*gap*(<r chi>-<r><chi>)와 일치한다. 우주 밀도에 추가할 물리 에너지 항이 아니다. 전류는 Q2=0,0.01,0.1 GeV2에서 같은 고정 전하 연산자로 비교했다.']),
('2 | SI 에너지 교체와 공급 경계',[
'1 MeV = 1.602176634e-13 J. 입자 수는 주소 확률에서 유도하지 않는다. 기준 V0=1 m3에서 기대 입자 수를 외부 보정으로 맞춘다.',
'Nbar = E_phi_ref / (E_rest_particle + E_exc_baseline_particle)',
'E_system = Nbar*E_rest_particle + Nbar*E_exc_case_particle + E_D + E_R',
'기존 E_phi를 이 분해로 교체한다. 기존 총 에너지에 rest+excitation을 다시 더하면 기준 E_phi만큼 중복된다. 순수 proton/neutron과 두 보정의 조건부 예시이며 실제 풍부도 예측이 아니다.',
'기존 보정의 proton 예시: Nbar=0.2425893464. 이는 기대 점유수이며 한 실행의 정수 입자 수가 아니다. 기준 phi 할당은 rest 3.6467913480e-11 J와 excitation 1.3399990150e-12 J로 분해된다.',
'deltaE = Nbar*(E_exc_case-E_exc_baseline). 시스템은 +deltaE, 환경은 -deltaE를 기록한다. 초기 환경은 0.2*E_phi_ref의 유한 진단 입력이다. 저진폭 조건부 준비는 시스템에 +8.9385339569e-15 J를 준다.',
'외부 환경의 교환은 경계 일이다. 포함 환경에서는 양쪽 증분이 총 장부에서 상쇄된다. 기존 하류 입장 conversion work와 같은 사건인지 확인하지 않고 합산하지 않는다.']),
('3 | 압력과 균일 기하 응답',[
'준비 뒤 입자 수·내부 상태를 고정하고 comoving phi/D 총 에너지를 일정하게 둔다. R은 일정 밀도이다. 포함 환경은 P_env=0을 별도로 가정한다.',
'V=V0*a^3; E(V)=M+L*V; P=-dE/dV=-L; u=M/V+L',
'H^2/H0^2=u/ucrit; q=(u+3P)/(2u); a*du/da+3*(u+P)=0',
'외부 환경 기준 a=1: 기존 q=-0.52855, 대체 q=-0.523, 두 경우 H/H0=1. a=.5,1,2에서는 변하는 비중으로 q(a)를 계산했다.',
'환경 포함 기준은 별도 부하이다. 기존 q=-0.5185075159, H/H0=1.0049179071; 대체 q=-0.5128712871, H/H0=1.0049875621. 이 값은 환경 입력을 더한 조건부 모형 결과이다.',
'96개 부피별 결과와 32개 균일 적분을 실행했다. tau=H0*t에서 17개 시점을 계산했고 해석해 대비 최대 scale-factor 오차는 3.297429e-11이다. 이 tau는 소스 프레임의 초를 결정하지 않는다.',
'검토 결론: 같은 E의 압력·연속식·균일 가속도는 일치한다. 실제 공급 압력, 준비 중 Q(t), 부피 의존 미시 상태와 비균질 동역학은 남는다. 로컬 회전·렌즈는 재계산하지 않았다.']),
('4 | 재현·마감 판정·근거',[
'패키지 루트에서 OPENBLAS_NUM_THREADS=1 python reproduce_all.py를 실행한다. Python 3, numpy, scipy, mpmath가 필요하다. 보고서 재작성에는 reportlab, pypdf와 NanumGothic 글꼴이 필요하다.',
'전체 실행은 0.2 -> 0.3 -> 0.4 입력을 순서대로 갱신하고 36개 연결 검사를 수행한다. 과거 단계의 원본 ZIP은 historical/에 보존한다. 최신 근거는 studies/와 review_checks.json이다.',
'이번 완료 판정은 공개한 최소 결합·회계·균일 모형의 실행 범위에 한한다. source branch 변화와 종별 입자 생성이 함께 이동하는 전체 전달은 미실행이다. 실제 환경 법칙, 기록 안정성, SI 소스 시계는 후속 검증이다.',
'다음 0.5: 프레임·고유시간·SI 위상. 0.6: 측정 후 진화·기록·반복. 0.7: 유한 비균질 결합. 0.8: 전체 재현·검토. 숫자 일치만으로 미구현 연결을 닫지 않는다.',
'상류 근거: 통합 1.0-r1, DOI 10.5281/zenodo.23119041. 하류 근거: 통합 1.0과 0.10-0.12 계열, DOI 10.5281/zenodo.23113101. 두 저자의 Physics 준비 원고를 각 계열이 인용한다.',
'저장소: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1. 입력·코드·결과 해시는 패키지 SHA256SUMS와 단계별 결과에 기록한다.'])],
'EN':[
('Upstream-downstream bridge 0.1-0.4 | Review r1',[
'Wonsik Choi and Jeongin Choi | 3 October 2026 | CC BY 4.0',
'DOI: 10.5281/zenodo.23119802',
'This collection reviews the finite bridge between upstream 0.10 and downstream 0.12. Both endpoints remain closed. Bridge research ends at 0.8; 1.0 consolidates its publication.',
'Stage 0.1 defines typed interfaces. Stage 0.2 executes a conditional address/internal state and compares product reduction. Stage 0.3 replaces the reference phenotype allocation with matched SI rest and excitation energies. Stage 0.4 derives pressure and homogeneous expansion from that energy.',
'Re-executed case checks: 15, 95, 134 and 600, plus 36 cross-stage checks: 880 total implementation/mathematical checks, not experiments.',
'Revision r1 rejects nonfinite and negative exchange inputs, adds block trace controls, scopes provenance to bundled dependencies and propagates newly generated results through the pipeline.',
'Completion means execution under disclosed assumptions. Preparation hardware, species abundance, source-frame seconds, durable physical records and nonuniform covariant dynamics remain open.']),
('1 | Typed interfaces and correlated state',[
'Address shares 0.05/0.268/0.682 differ from inherited SI energy shares 0.0493/0.265/0.6857. Response calibration is explicit. Resident Actual 0.318 differs in scope from the complete ledger 1.',
'For phi-conditioned addresses n=2..1,000,000, the exact block representation is:',
'Sigma_phi = sum_n p(n|phi) |n><n| x rho_internal(n) x I_128/128',
'rho_internal(n) = (1-0.2 chi(n)) |g><g| + 0.2 chi(n) |e1><e1|',
'chi selects odd prime-3 valuation. Two frozen modes occupy the real 95-dimensional nucleon basis; the stationary carrier is 128-dimensional. D and return keep their original branch ledgers without nucleon preparation. General entanglement and address coherence preservation are not claimed.',
'Address-independent internal energy and charge-current expectations equal those of the internal marginal product. Address-weighted probes retain a covariance term that the product loses.',
'For r(n)=1+0.25 log(n)/log(N), the baseline excitation-probe difference is 0.1447722277 MeV. It equals a*gap*(<r chi>-<r><chi>). This diagnostic is not an additional cosmic energy term. Fixed charge operators were tested at Q2=0,0.01,0.1 GeV2.']),
('2 | SI replacement and signed exchange',[
'The exact conversion is 1 MeV=1.602176634e-13 J. Particle count is not an address probability. An external reference matching sets an expected occupancy in V0=1 m3:',
'Nbar = E_phi_ref / (E_rest_particle + E_exc_baseline_particle)',
'E_system = Nbar*E_rest_particle + Nbar*E_exc_case_particle + E_D + E_R',
'This decomposition replaces E_phi. Adding it to the original total again duplicates E_phi. Pure-proton and pure-neutron illustrations under two calibrations do not predict actual composition.',
'The inherited proton example has Nbar=0.2425893464: an expected count, not an integer event count. Its rest and reference excitation totals are 3.6467913480e-11 J and 1.3399990150e-12 J.',
'deltaE=Nbar*(E_exc_case-E_exc_baseline). System and environment receive opposite entries. A reservoir initially equal to 0.2*E_phi_ref is a disclosed finite diagnostic input. The low-amplitude conditional preparation gives +8.9385339569e-15 J to the system.',
'An external reservoir supplies boundary work. An included reservoir cancels internal exchange in the full energy ledger. The inherited admission conversion work is a separate event account; it is not added without checking event identity.']),
('3 | Same-energy pressure and homogeneous response',[
'After preparation, comoving population and internal state are fixed. Phenotype and D total energies are constant; R has constant density. An included reservoir additionally assumes pressure zero.',
'V=V0*a^3; E(V)=M+L*V; P=-dE/dV=-L; u=M/V+L',
'H^2/H0^2=u/ucrit; q=(u+3P)/(2u); a*du/da+3*(u+P)=0',
'At a=1 with an external reservoir, inherited q=-0.52855 and alternate q=-0.523 both reproduce H/H0=1. At a=.5,1,2, q uses evolving energy shares.',
'Including the finite reservoir changes the reference load without refitting: inherited q=-0.5185075159, H/H0=1.0049179071; alternate q=-0.5128712871, H/H0=1.0049875621. These are conditional load results, not new observational calibrations.',
'The execution supplies 96 volume rows and 32 homogeneous integrations with 17 sample times in tau=H0*t. Maximum scale-factor error against the analytic dust/background solution is 3.297429e-11. This time coordinate does not assign physical seconds to source frames.',
'Same-energy pressure, continuity and homogeneous acceleration agree. Real reservoir pressure, Q(t) during preparation, microscopic volume coupling and nonuniform dynamics remain open. Local rotation and lensing were not recalculated.']),
('4 | Reproduction and closure ledger',[
'At package root run OPENBLAS_NUM_THREADS=1 python reproduce_all.py. Numerical dependencies are Python 3, numpy, scipy and mpmath. PDF rebuilding additionally needs reportlab and NanumGothic.',
'The runner regenerates 0.2 -> 0.3 -> 0.4 inputs sequentially and checks 36 cross-stage contracts. Original ZIPs remain in historical/. Current executable evidence is in studies/ and review_checks.json.',
'The implemented bridge covers a conditional phi state, external reference-matched expected populations, finite signed exchange and homogeneous post-preparation evolution. Simultaneous source-branch population transport and particle creation are not executed.',
'Remaining stages: 0.5 clocks and SI phase; 0.6 measurement, records and repeated outcomes; 0.7 finite nonuniform coupling; 0.8 complete replay and review. Scalar agreement does not close an unimplemented connection.',
'Upstream integrated source: DOI 10.5281/zenodo.23119041. Downstream integrated source and 0.10-0.12 lineage: DOI 10.5281/zenodo.23113101. The coauthored Physics preparation manuscripts are cited by those source collections.',
'Repository: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1. Source/result hashes and a complete SHA-256 manifest accompany the release.'])]}
style=ParagraphStyle('Body',fontName='Body',fontSize=10.5,leading=17,spaceAfter=12,wordWrap='CJK',textColor=colors.HexColor('#253244'))
title=ParagraphStyle('Heading',parent=style,fontSize=19,leading=26,spaceAfter=24,textColor=colors.HexColor('#113b61'))
def footer(canvas,doc):
 canvas.setFont('Body',8);canvas.setFillColor(colors.HexColor('#65758a'))
 canvas.drawString(44,31,'WRRA M | bridge 0.1-0.4 r1 | DOI 10.5281/zenodo.23119802')
 canvas.drawRightString(550,31,str(doc.page))
for lang,pages in PAGES.items():
 flow=[]
 for i,(heading,ps) in enumerate(pages):
  if i:flow.append(PageBreak())
  flow.append(Paragraph(escape(heading),title))
  for p in ps:flow.append(Paragraph(escape(p),style))
 doc=SimpleDocTemplate(str(R/f'WRRA_M_Bridge_0_1_0_4_Reviewed_r1_{lang}_2026_10_03.pdf'),pagesize=(595.28,841.89),leftMargin=44,rightMargin=44,topMargin=48,bottomMargin=55,title='WRRA M bridge 0.1-0.4 reviewed r1',author='Wonsik Choi and Jeongin Choi')
 doc.build(flow,onFirstPage=footer,onLaterPages=footer)
