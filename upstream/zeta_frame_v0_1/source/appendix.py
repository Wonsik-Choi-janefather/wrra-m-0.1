"""Korean computational appendix derived from results.json."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
R=json.loads((ROOT/'results.json').read_text(encoding='utf8'))
TITLE='WRRA M 제타 영점 프레임 필터와 잔존 계산'
SUBTITLE='두 단계 차원필터 상위 구조 가설의 계산 부록 0.1'
B=[]
def p(text): B.append({'kind':'p','text':text})
def h(text): B.append({'kind':'h','text':text})
def eq(label,tex): B.append({'kind':'eq','label':label,'tex':tex})
def table(caption,headers,rows,widths): B.append({'kind':'table','caption':caption,'headers':headers,'rows':rows,'widths':widths})
def page(): B.append({'kind':'break'})
def pct(x,d=6):return f'{100*x:.{d}f}'

h('1 초기 변동을 주소별 프레임 계산으로 확장')
p('우리는 WRRA-M 상위 구조 가설 1.0의 초기 필터 변동을 제타 영점의 위상 합으로 구현했다. 소수와 합성수 주소에 제타 분모 가중치를 배정하고, 초기 8프레임에서 진입하지 않은 양만 다음 프레임으로 넘겼다. 정상화 뒤에는 접힘을 가진 진입 상태를 0차원 복귀 필터의 차단 부분공간에 남긴다.')
p('이 계산은 일정한 통과율 β를 주소와 프레임에 따른 aₙ(k)로 확장한다. 통과 임계값을 5%에 보정한 기준 사례에서 표현형 5%, 비표현형 Actual 26.8%, 복귀 68.2%가 하나의 분모를 공유한다. 임계값을 고정하고 초기 구간을 4·8·16프레임으로 바꾸면 표현형 잔존은 각각 3.7048%·5%·5.6825%가 된다.')
table('표 1 기준 사례의 입력과 보정', ['항목','계산값 또는 규칙'],[
 ['주소 범위','n = 2 … 1,000,000   n = 1은 제외'],
 ['위상 구성','첫 4개 양의 제타 영점   계수 1/√4   위상 오프셋 0'],
 ['초기 구간','K = 8프레임   무차원 위상 이동 ξ = 0.1'],
 ['가중 지수 α',f'{R["calibration"]["alpha"]:.15f}   26.8%에 보정'],
 ['통과 임계값 h',f'{R["calibration"]["sigmoid_threshold_h"]:.15f}   5%에 보정'],
 ['상태 분기','짝수 합성수 → 비표현형 Actual   진입한 홀수 합성수 → 표현형'],
], [1.65,5.2])
table('표 2 같은 분모의 정상화 이후 장부', ['출력','가중 비율'],[
 ['표현형 φ','5.000000%'],['비표현형 Actual D','26.800000%'],
 ['Actual 합계 φ + D','31.800000%'],['상류 복귀 R','68.200000%'],
], [4.55,2.3])
p('진입 필터와 0차원 복귀 필터가 두 차원필터다. 표현형과 비표현형의 구분은 잔존 상태의 판독이며 별도 차원필터를 추가하지 않는다. 여기서 유사소수는 불완전 판독에서 소수처럼 보이는 합성수 상태를 뜻한다. 통상적인 Fermat 유사소수 집합을 사용한 계산은 아니다.')

page();h('2 제타 영점과 두 단계 필터의 계산 규칙')
p('영점 ρⱼ = 1/2 + iγⱼ를 mpmath에서 40자리와 60자리 정밀도로 구했다. 사용한 첫 4개는 아래와 같다. 민감도 검사에는 첫 8개를 사용했다. Euler–Maclaurin 전개로 ζ(1/2 + iγⱼ)를 별도로 평가해 수치 입력을 교차 검증했다. [1–3]')
table('표 3 기준 위상에 사용한 영점 높이', ['j','γⱼ'],
      [[r['index'],f"{r['gamma_used_double']:.15f}"] for r in R['zeta_zero_validation'][:4]], [1.,5.85])
p('주소의 초기 기대 가중치는 wₙ이다. 홀수 합성수 집합을 Cₒ, 짝수 합성수 집합을 Cₑ로 표시한다. 단위 주소는 초기 SOURCE 잔량 sₙ(0) = wₙ에서 출발한다.')
eq('1',r'w_n=\frac{n^{-\alpha}}{\sum_{m=2}^{N}m^{-\alpha}}')
p('우리는 n⁻ˢ의 로그 위상 γⱼ log n을 이용해 다음 변동 함수를 선택했다. 동일 계수의 코사인 합과 sigmoid 통과 규칙은 이번 계산의 구체적인 필터 가정이다.')
eq('2',r'\delta_n(k)=\frac{1}{\sqrt{J}}\sum_{j=1}^{J}\cos\left[\gamma_j(\log n+\xi k)\right]')
eq('3',r'a_n(k)=\frac{1}{1+\exp[h-\delta_n(k)]}\quad (0\leq k<K,\ n\in C_o)')
p('한 프레임에서 새로 진입한 양은 bₙ(k)다. 이미 진입한 양을 다음 시도에 다시 넣지 않는다. 정상화 프레임 k = K 이후에는 신규 합성수 진입을 닫는다.')
eq('4',r'b_n(k)=s_n(k)a_n(k),\qquad s_n(k+1)=s_n(k)[1-a_n(k)]')
eq('5',r'T_n(K)=1-\prod_{k=0}^{K-1}[1-a_n(k)]')
p('짝수 합성수는 1.0의 소수 2 분기와 같이 첫 프레임에 전부 진입한다. 소수 주소와 끝까지 진입하지 않은 홀수 합성수 가중치는 정상화 때 복귀 장부로 옮긴다. 이 계산은 개별 우주의 무작위 경로를 뽑는 Monte Carlo가 아니라 기대 가중치를 운반하는 결정적 계산이다.')

page();h('3 프레임별 생성과 정상화 이후 장부')
p('표현형은 첫 프레임의 1.5018%에서 8번째 시도 종료 때 5%로 증가한다. 새 진입량은 위상에 따라 변하며, 잔량을 소모하므로 누적 진입량은 항상 해당 주소의 초기 가중치 이하에 머문다.')
B.append({'kind':'fig','name':'frames','width':6.6,'caption':'그림 1 초기 8프레임의 누적 잔존과 신규 진입. 점선 k = 8은 정상화 시점이다. 이후 신규 진입이 닫히고, 접힘 차단 규칙 아래 누적 표현형이 유지된다.'})
table('표 4 프레임 종료 시 표현형 및 상류 장부   단위 %',
 ['프레임 k','신규 표현형','누적 표현형','SOURCE 잔량','복귀'],
 [[f['frame'],pct(f['new_phenotype'],4),pct(f['phenotype'],4),pct(f['SOURCE_reservoir'],4),pct(f['returned'],4)] for f in R['frames'][:9]]+
 [['9 … 1032','0.0000','5.0000','0.0000','68.2000']],
 [.8,1.4,1.4,1.65,1.6])
p('비표현형 Actual은 첫 프레임에서 26.8%다. 각 행에서 표현형, 비표현형 Actual, SOURCE 잔량, 복귀의 합은 100%다. SOURCE 잔량은 초기 구간의 미진입 저장량이고, 정상화 때 복귀량으로 옮겨진다.')
p(f'잔량 소모를 생략하고 모든 시도의 wₙaₙ(k)를 단순 합산하면 {pct(R["naive_attempt_sum_without_reservoir_depletion"],4)}%가 나온다. 순차 운반식과 곱 형태의 Tₙ(K)는 같은 5%를 반환한다. 따라서 프레임 수와 통과율을 함께 쓰는 경우에는 잔량 갱신이 필수다.')

page();h('4 작은 소수부터 합산한 잔존 기여')
p('합성수 주소를 최소 소인수별로 분할하면 소수 조합의 기여를 중복 없이 셀 수 있다. 소수 2 가족은 비표현형 Actual 26.8%를 제공한다. 홀수 가족에는 주소별 Tₙ(K)를 곱한 잔존 가중치를 사용한다.')
cum=R['terminal']['nonphenotypic_Actual']
familyrows=[['2','26.800000',pct(cum)]]
for row in R['smallest_prime_family_residue'][:5]:
 cum+=row['residual_weight_fraction']
 familyrows.append([str(row['smallest_prime_factor']),pct(row['residual_weight_fraction']),pct(cum)])
familyrows.append(['17 이상',pct(R['terminal']['Actual']-cum),'31.800000'])
table('표 5 최소 소인수별 잔존과 Actual 누적   단위 %',
 ['최소 소인수','이 가족의 기여','누적 Actual'],familyrows,[1.55,2.65,2.65])
p('이 기준 사례에서 3·5·7·11 가족의 표현형 기여 합은 4.936374%이며, 전체 5%의 약 98.7275%다. 먼저 소수 2 가족을 넣고 작은 소수 가족을 차례로 합산하면 Actual 장부가 31.8%로 접근한다. 이 기여는 최소 소인수 가족의 합이며 개별 소수의 입자 질량을 뜻하지 않는다.')
table('표 6 주소별 8프레임 누적 통과와 잔존',
 ['주소 n','소인수 표현','Tₙ(8)   %','전체 중 잔존   %'],
 [[str(row['address']),factor,pct(row['cumulative_admission'],4),pct(row['residual_weight_fraction'],6)]
  for row,factor in zip(R['address_samples'][:8],['3²','3 × 5','3 × 7','5²','3³','3 × 11','5 × 7','7²'])],
 [1.,1.5,2.15,2.2])
p(f'동일한 평균 β를 입력하는 방식과 달리, 이제 주소별 누적 통과가 구별된다. 예를 들어 9와 15의 Tₙ(8)는 85.6813%와 87.3632%다. 홀수 소수 거듭제곱의 표현형 기여는 {pct(R["prime_power_residue_fraction"],6)}%, 서로 다른 소인수를 포함한 홀수 합성수의 기여는 {pct(R["non_prime_power_residue_fraction"],6)}%다.')

page();h('5 보정값을 고정한 초기 조건의 응답')
p('기준 임계값 h = 1.447673170352440을 그대로 유지하고 한 조건씩 바꿨다. 표 7의 수치는 새로운 목표 보정을 하지 않은 계산 출력이다. 4프레임에서는 충분한 시도가 쌓이기 전에 정상화되고, 16프레임에서는 더 많은 잔량이 진입한다.')
labels=['정상화 K = 4','정상화 K = 16','위상 이동 ξ = 0.05','위상 이동 ξ = 0.20','영점 J = 1','영점 J = 2','영점 J = 8','위상 이동 없음 ξ = 0','변동 함수 δ = 0','임계값 h − 0.1','임계값 h + 0.1']
table('표 7 조건 변화에 따른 표현형 출력', ['조건','표현형   %','복귀   %'],
 [['기준 K = 8   J = 4   ξ = 0.1','5.000000','68.200000']]+
 [[label,pct(row['phenotype']),pct(row['return'])] for label,row in zip(labels,R['frozen_threshold_sensitivity'])],
 [3.55,1.65,1.65])
p('제타 영점의 선택은 주소별 통과 패턴도 바꾼다. 이를 확인하기 위해 정지 위상과 등간격 주파수 대조군에서는 h를 각각 다시 5%에 보정했다. 전체 장부가 같더라도 주소별 출력은 아래처럼 다르다. 이후 입자 상수 연결은 이 주소별 출력을 사용해 필터 구성을 구별할 수 있다.')
table('표 8 같은 5%에 보정한 구성별 주소 응답', ['위상 구성','보정 h','주소 9의 T₉(8)   %'],[
 ['기준 제타 4영점',f'{R["calibration"]["sigmoid_threshold_h"]:.6f}','85.681301'],
 ['정지 제타 위상','1.327223','80.386717'],
 ['14·21·28·35 대조군','1.525841','88.580085'],
], [3.05,1.5,2.3])
p('분모의 유한 절단도 확인했다. α와 h를 고정한 N = 10,000·100,000·1,000,000 계산의 표현형은 4.989116%·4.998724%·5%다. 가중 평균 통과율 β_eff = 0.8654570124는 이번 프레임 출력의 평균이며 별도 상수 입력으로 넣지 않았다.')

page();h('6 복귀 차단의 보존 조건과 검증')
p('정상화된 복귀 연산자를 B, 접힘 잔존 부분공간을 𝒦 = ker B라 하자. 진입한 합성수는 𝒦에 놓이며 이번 계산의 정상화 이후 내부 갱신은 항등 연산이다. 일반적인 내부 갱신 U로 확장할 때는 다음 보존 조건이 필요하다.')
eq('6',r'\operatorname{supp}\rho_{\mathrm{res}}\subseteq\mathcal{K},\qquad U\mathcal{K}\subseteq\mathcal{K}')
p('이 조건에서는 프레임이 늘어나도 잔존이 복귀 통로에 새로 나타나지 않는다. 각 복귀 사건에서 잔존 확률의 ε만큼이 새는 대조 모형에서는 L번 사건 뒤 생존이 (1 − ε)ᴸ로 줄어든다. 아래는 100만 번 사건을 적용한 출력이다.')
table('표 9 정상화 이후 복귀 누수의 영향   L = 1,000,000',
 ['사건당 누수 확률 ε','잔존 생존   %','전체 Actual   %'],
 [[f"{row['epsilon_probability']:.0e}",pct(row['residue_survival_fraction'],4),pct(row['Actual'],4)]
  for row in R['return_leakage_stress'] if row['return_event_count']==1_000_000],
 [2.75,2.,2.1])
eq('7',r'(1-\epsilon)^L\geq 1-\eta\quad\Longrightarrow\quad\epsilon\leq 1-(1-\eta)^{1/L}')
p('100만 번의 복귀 사건 뒤에도 초기 잔존의 99% 이상을 유지하려면 사건당 누수 확률은 약 1.0050 × 10⁻⁸ 이하여야 한다. 사건 수는 무차원이다. 물리적 보존 수명은 프레임과 실제 시간의 대응을 정한 뒤 계산할 수 있다.')
h('수치 검증과 다음 물리 판독')
p('독립 Euler–Maclaurin 평가의 영점 잔차는 10⁻¹¹ 이하이고, 40자리와 60자리 재계산의 영점 높이 차는 10⁻³⁶ 이하다. 주소별 진입과 미진입의 합, 모든 프레임의 공통 장부, 최소 소인수 가족의 잔존 합을 확인했다. 코드의 14개 검증 항목이 모두 통과했다.')
p('다음 연결 대상은 같은 주소 상태에 작용하는 에너지·중력·전하 판독이다. 양성자와 중성자는 표현형과 중력 반응을 함께 읽어야 하므로 전하 0을 상류 복귀와 동일시하지 않는다. 프레임 주기와 허용 모드의 스펙트럼을 정하면 입자 상수 비교를 진행할 수 있다. 현재 ξ는 무차원 위상 이동량이며 플랑크 시간에 대응시키지 않았다.')
p('장부의 음수나 불완전성, 영점 재계산의 불일치, 요구 수명보다 큰 복귀 누수, 고정한 필터와 공통 물리 판독이 입자 또는 우주 에너지 구성과 충돌하는 경우를 계산 규칙의 기각·수정 조건으로 삼는다. 소수 가족의 가중 분할을 물리 에너지 비율로 연결하는 단계는 1.0에서 제안한 판독 문제를 이어받는다.')
h('참고 자료')
p('[1] NIST DLMF 25.10 Zeros. https://dlmf.nist.gov/25.10\n[2] NIST DLMF 25.11 iii Euler–Maclaurin Formula. https://dlmf.nist.gov/25.11.iii\n[3] mpmath Zeta functions. https://mpmath.readthedocs.io/en/latest/functions/zeta.html')

if __name__=='__main__':
 (ROOT/'appendix.json').write_text(json.dumps({'title':TITLE,'subtitle':SUBTITLE,'blocks':B},ensure_ascii=False,indent=2),encoding='utf8')
