import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'results'
j=json.loads((OUT/'address_results.json').read_text());d=j['dark_correction']
fig,axs=plt.subplots(1,2,figsize=(11,4.5))
bands=d['bands'];labels=[f"{x['address_min']:,}–{x['address_max']:,}" for x in bands]
axs[0].barh(labels,[100*x['fraction_of_increment'] for x in bands],color='#24759a')
axs[0].invert_yaxis();axs[0].set_xlabel('Share of dark-load correction [%]');axs[0].set_title('Correction attributed to actual addresses')
names=['Unweighted','Vacuum swap diagnostic','Weighted','Address-generated D-only']
scores=[1217.7512246828783,1121.9031209830046,591.5703352409629,585.9139188511556]
colors=['#bb6459','#be9567','#5683a0','#328570']
bars=axs[1].barh(names,scores,color=colors);axs[1].invert_yaxis()
for b,v in zip(bars,scores):axs[1].text(v+10,b.get_y()+b.get_height()/2,f'{v:.2f}',va='center',fontsize=9)
axs[1].set_xlim(0,1380);axs[1].set_xlabel('High-ell Plik-lite quadratic form');axs[1].set_title('Fixed inputs, no new optimizer')
for ax in axs:ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True)
fig.tight_layout();fig.savefig(OUT/'address_correction_and_CMB.png',dpi=180);plt.close(fig)
fig,axs=plt.subplots(3,1,figsize=(10,9),sharex=True)
for ax,(name,c,release) in zip(axs,[('TT',0,'3.01'),('TE',3,'3.02'),('EE',1,'3.02')]):
    data=np.loadtxt(ROOT/f'inputs/COM_PowerSpect_CMB-{name}-binned_R{release}.txt')
    ax.errorbar(data[:,0],data[:,1],yerr=[data[:,2],data[:,3]],fmt='.',color='#666',ms=2,alpha=.5,label='Planck PR3 public bins')
    for b,color in [('unweighted','#b26f3e'),('weighted','#356991')]:
        dl=np.load(OUT/f'{b}_standard_a2.5.npz')['Dl'];ax.plot(np.arange(len(dl)),dl[:,c],color=color,lw=1,label=b)
    a=np.loadtxt(OUT/'dark_weight_only_baseline_plus_SOURCE_Dl.csv',delimiter=',',skiprows=1)
    ax.plot(a[:,0],a[:,c+1],color='#2d8768',lw=1.2,label='address-generated D-only + linear SOURCE')
    ax.set_ylabel(name+r' $D_\ell$ [$\mu K^2$]');ax.grid(alpha=.2);ax.set_xlim(2,2508)
axs[0].legend(fontsize=8,ncol=2);axs[-1].set_xlabel(r'Multipole $\ell$')
fig.suptitle('Address-generated dark-weight candidate\nExisting conditional primordial extension; SOURCE-specific lensing remains open',fontsize=11)
fig.tight_layout();fig.savefig(OUT/'address_candidate_CMB.png',dpi=180);plt.close(fig)
