for page in pages:
 for block in page['blocks']:
  if block['kind']=='p':
   en,ko=block['en'],block['ko']
   if en.startswith('The evidence chain'):
    en=en.replace('and fixed-parameter controls assess consequences of the constructed state.', 'and fixed-parameter controls assess consequences of the constructed state. Unmeasured physical readouts computed after fixing verified inputs are conditional WRRA predictions, with the declared preparation and physical mapping specifying their scope. Originality resides in the finite architecture, transformations and connections; independent numerical novelty is not required.')
    ko=ko.replace('고정 매개변수 대조로 구성된 상태의 결과를 평가한다.', '고정 매개변수 대조로 구성된 상태의 결과를 평가한다. 검증 입력을 확정한 뒤 계산한 미측정 물리량은 선언한 준비·물리 대응 범위에서 WRRA의 조건부 예측이다. 독창성은 유한 구조·변환·연결에서 판정하며 수치의 독립적 새로움을 요구하지 않는다.')
   if en.startswith('Source and Actual'):
    en=en.replace('with S+A=1.', 'with S+A=1. Here A is a scalar stock, distinct from the admission operator A in Section 2.')
    ko=ko.replace('S+A=1이다.', 'S+A=1이다. 이 절의 A는 스칼라 보유량이며 2절의 진입 연산자 A와 구별한다.')
   if en.startswith('Here M̄'):
    en=en.replace('the current in nuclear magnetons is multiplied by M̄/mp before the Sachs–Dirac–Pauli conversion.', 'write the dimensional magnetic readout as M_B(Q²)=μN 𝓜_B(Q²). The dimensionless Sachs magnetic factor in the conversion above is G_M=(M̄/mp)𝓜_B, with 𝓜_B the numerical nuclear-magneton readout.')
    ko=ko.replace('핵자 자석온의 자기 판독에 M̄/mp를 곱한 후 Sachs–Dirac–Pauli 변환을 적용한다.', '차원 있는 자기 판독을 M_B(Q²)=μN 𝓜_B(Q²)로 쓴다. 위 변환의 무차원 Sachs 자기 인자는 G_M=(M̄/mp)𝓜_B이며 𝓜_B는 핵자 자석온 판독의 수치 계수다.')
   if en.startswith('At Q²=0.1'):
    en=en.replace('GMp=','Mp=').replace('GMn=','Mn=')
    ko=ko.replace('GMp=','Mp=').replace('GMn=','Mn=')
   if en.startswith('The Physics preparation'):
    en=en.replace('uniform-load bridge.', 'uniform-load bridge [8,9].')
    ko=ko.replace('균일 부하 연결을 실행했다.', '균일 부하 연결을 실행했다[8,9].')
   if en.startswith('The second expression'):
    en=en.replace('q0=−0.523.', 'q0=−0.523 at V=V0. Away from V0, the evolving energy fractions must be used in q(V); this value is not volume-independent.')
    ko=ko.replace('q0=−0.523을 계산한다.', 'V=V0에서 q0=−0.523을 계산한다. V0 밖에서는 변화한 에너지 구성비로 q(V)를 계산하므로 이 값은 부피에 독립인 상수가 아니다.')
   block['en'],block['ko']=en,ko
  elif block['kind']=='table':
   for row in block['rows']:
    for i,val in enumerate(row):row[i]=val.replace('GMp / GMn (μN)','Mp / Mn (μN)')
references=pages[-1]['blocks']
insert_at=next(i for i,b in enumerate(references) if b.get('en','').startswith('Data availability.'))
references[insert_at:insert_at]=[
 {'kind':'p','en':'[8] Choi, W., Choi, J. Reproduction of the ordinary-matter 5% composition, terminology edition r9 (2026). Prepared manuscript and calculation sources: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/main/submission/matter_fraction_r9','ko':'[8] 최원식, 최정인. 보통 물질 5퍼센트 구성비의 재현, 용어 병기 r9 (2026). 준비 원고·계산 자료: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/main/submission/matter_fraction_r9'},
 {'kind':'p','en':'[9] Choi, W., Choi, J. Extension possibilities and connection conditions, r8 (2026). Prepared manuscript: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/main/submission/extensions_r8','ko':'[9] 최원식, 최정인. WRRA의 확장 가능성과 접속 조건, r8 (2026). 준비 원고: https://github.com/Wonsik-Choi-janefather/wrra-m-0.1/tree/main/submission/extensions_r8'}]
