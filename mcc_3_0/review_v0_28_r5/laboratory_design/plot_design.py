from design import ROOT,profile
import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
f=profile(); L=np.linspace(0,40,1001); v=abs(np.exp(2j*np.pi*L[:,None]*f[None,:]/1064e-9).mean(axis=1))
cfg=json.loads((ROOT/'design.json').read_text());pts=[p for p in cfg['points'] if abs(p['wavelength_m']-1064e-9)<1e-15]
fig,ax=plt.subplots(figsize=(8,3.6));ax.plot(L,v,label='Frozen WRRA branch, 1064 nm',color='#174c70',lw=2)
ax.fill_between(L,np.maximum(v-.01,0),np.minimum(v+.01,1),alpha=.2,color='#174c70',label='Selected ±0.01 design band (not data)')
ax.scatter([p['L_m'] for p in pts],[p['visibility'] for p in pts],s=35,color='#bc4c24',zorder=5)
ax.axhline(1,ls='--',color='grey',lw=1,label='Balanced common-coupling control')
ax.set(xlabel='Effective differential exposure L (m; not automatically path length)',ylabel='Normalized visibility V/V0',ylim=(0,1.08),xlim=(0,40));ax.legend(fontsize=8,loc='lower left');ax.grid(alpha=.15);fig.tight_layout()
fig.savefig(ROOT/'book_v0_28_r3/figures/lab_visibility_design.png',dpi=200)
