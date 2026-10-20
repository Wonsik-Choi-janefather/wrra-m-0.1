from pathlib import Path
import numpy as np,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
P=Path(__file__).resolve().parent;z=np.load(P/'results/complete_projection.npz');h=np.load(P/'results/dynamic_preparation.npz')
font=FontProperties(fname='/usr/local/share/fonts/wrra/NotoSansCJKkr-Regular.otf')
plt.rcParams.update({'font.family':font.get_name(),'axes.unicode_minus':False,'font.size':9})
fig,ax=plt.subplots(2,2,figsize=(10,8),layout='constrained')
cum=np.cumsum(z['mode_variance'])/np.sum(z['mode_variance'])
ax[0,0].plot(np.arange(1,65),cum*100,lw=2);ax[0,0].axvline(7,ls='--',c='gray')
ax[0,0].set(xlabel='조화 번호 n',ylabel='누적 초기 분산 [%]',title='7개에서 64개로: 초기 분산 100% 전달')
ell=z['ell'];f=ell*(ell+1)/(2*np.pi)
ax[0,1].semilogy(ell,f*z['static_covariance'][:,0,0],label='정적 64모드')
ax[0,1].semilogy(ell,f*z['dynamic_covariance'][:,0,0],label='동역학 64모드')
ax[0,1].set(xlabel='다중극 ℓ',ylabel='Dℓ [μK²]',title='새 실제 전달값의 온도 스펙트럼');ax[0,1].legend()
N,C,M,H,W=h['history'][:5];beta=json.loads((P/'results/dynamics_results.json').read_text())['calibrated_convertible_radiation_fraction'];R=1-beta+C
t=h['time'];ax[1,0].plot(t,C/beta,label='복사 저장소 a⁴ρ / 초기값')
ax[1,0].plot(t,M/M[-1],label='물질 저장소 a³ρ / 최종값')
ax[1,0].set(xlabel='국소 고유시간 / 초기 허블시간',ylabel='정규화 저장소',title='전환 펄스와 이후 팽창');ax[1,0].legend()
err1=abs(R*np.exp(-N)+M+W-1);err2=abs(H*H-R*np.exp(-4*N)-M*np.exp(-3*N))/(R*np.exp(-4*N)+M*np.exp(-3*N))
ax[1,1].semilogy(t,np.maximum(err1,1e-17),label='에너지 + 압력 일')
ax[1,1].semilogy(t,np.maximum(err2,1e-17),label='프리드만 상대 오차')
ax[1,1].set(xlabel='국소 고유시간 / 초기 허블시간',ylabel='장부·제약 오차',title='독립 진화한 보존·중력 제약');ax[1,1].legend()
fig.savefig(P/'diagnostics_KO.png',dpi=170)
labels={'조화 번호 n':'Harmonic n','누적 초기 분산 [%]':'Cumulative initial variance [%]','7개에서 64개로: 초기 분산 100% 전달':'Modes 1-64 cover all finite-grid variance','다중극 ℓ':'Multipole ell','새 실제 전달값의 온도 스펙트럼':'Temperature from newly evolved transfers','정적 64모드':'Static 64 modes','동역학 64모드':'Dynamic 64 modes','국소 고유시간 / 초기 허블시간':'Local proper time / initial Hubble time','정규화 저장소':'Normalized reservoirs','전환 펄스와 이후 팽창':'Conversion pulse and subsequent expansion','복사 저장소 a⁴ρ / 초기값':'Comoving radiation a⁴ρ / initial','물질 저장소 a³ρ / 최종값':'Comoving matter a³ρ / final','에너지 + 압력 일':'Energy + pressure work','프리드만 상대 오차':'Friedmann relative error','장부·제약 오차':'Ledger / constraint error','독립 진화한 보존·중력 제약':'Independently evolved gravity constraint'}
for a in ax.flat:
 a.set_title(labels.get(a.get_title(),a.get_title()));a.set_xlabel(labels.get(a.get_xlabel(),a.get_xlabel()));a.set_ylabel(labels.get(a.get_ylabel(),a.get_ylabel()))
 if a.get_legend():
  for x in a.get_legend().get_texts():x.set_text(labels.get(x.get_text(),x.get_text()))
fig.savefig(P/'diagnostics_EN.png',dpi=170)
