from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
P=Path(__file__).resolve().parent
z=np.load(P/'results/projection.npz')
font=FontProperties(fname='/usr/local/share/fonts/wrra/NotoSansCJKkr-Regular.otf')
plt.rcParams.update({'font.family':font.get_name(),'axes.unicode_minus':False,'font.size':10})
fig,ax=plt.subplots(2,2,figsize=(10,8),layout='constrained')
x=np.arange(128)
ax[0,0].plot(x,(z['fraction']-.5)*1e8,drawstyle='steps-mid',label='양자화 후')
ax[0,0].plot(x,z['twist']/3.5*1e8,label='연속 목표',alpha=.8)
ax[0,0].set(xlabel='주기적 셀',ylabel='기준 대비 전환 비율 × 10⁸',title='복사에서 물질로 전환된 공간 분포')
ax[0,0].legend()
ax[0,1].plot(x,z['residual']/1e-8,color='#b66d12')
ax[0,1].axhline(1,color='black',ls='--',lw=.8)
ax[0,1].set(xlabel='주기적 셀',ylabel='잔여 / q',title='버리지 않은 잔여는 한 양자 미만')
h=np.fft.rfft(z['entropy'])/128
power=2*abs(h)**2;power[0]=0;power[-1]/=2
ax[1,0].bar(np.arange(1,65),power[1:]/sum(power),color=['#266c91' if n<=7 else '#b66d12' for n in range(1,65)])
ax[1,0].set(xlabel='조화 번호 n',ylabel='초기 엔트로피 분산 비중',title='파란색: CMB 전달 / 주황색: 미전달')
l=z['ell'];f=l*(l+1)/(2*np.pi)
ax[1,1].semilogy(l,f*z['Cl_T'],label='T')
ax[1,1].semilogy(l,f*z['Cl_E'],label='E')
ax[1,1].set(xlabel='다중극 ℓ',ylabel='Dℓ [μK²]',title='새 준비의 일곱 모드 CMB 투영')
ax[1,1].legend()
fig.savefig(P/'diagnostics.png',dpi=180)
translations={'주기적 셀':'Periodic cell','기준 대비 전환 비율 × 10⁸':'Conversion fraction offset x 1e8','복사에서 물질로 전환된 공간 분포':'Spatial radiation-to-matter conversion','양자화 후':'Quantized','연속 목표':'Continuous target','잔여 / q':'Residue / q','버리지 않은 잔여는 한 양자 미만':'Retained residue below one quantum','조화 번호 n':'Harmonic n','초기 엔트로피 분산 비중':'Fraction of initial entropy variance','파란색: CMB 전달 / 주황색: 미전달':'Blue: projected / orange: unprojected','다중극 ℓ':'Multipole ell','새 준비의 일곱 모드 CMB 투영':'Seven-mode CMB projection'}
for aa in ax.flat:
 aa.set_title(translations.get(aa.get_title(),aa.get_title()))
 aa.set_xlabel(translations.get(aa.get_xlabel(),aa.get_xlabel()))
 aa.set_ylabel(translations.get(aa.get_ylabel(),aa.get_ylabel()))
 if aa.get_legend():
  for t in aa.get_legend().get_texts(): t.set_text(translations.get(t.get_text(),t.get_text()))
fig.savefig(P/'diagnostics_EN.png',dpi=180)
print(P/'diagnostics.png')
