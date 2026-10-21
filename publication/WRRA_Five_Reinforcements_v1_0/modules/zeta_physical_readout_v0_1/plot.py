from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;r=json.loads((P/'results.json').read_text())
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(10,3.35),layout='constrained')
for prep,label,col in [('uniform','Uniform','#225ea8'),('inherited_alpha','Inherited alpha','#c44e52')]:
 s=np.loadtxt(P/(prep+'_spectrum.csv'),delimiter=',',skiprows=1)
 ax[0].plot(s[:,0],s[:,1],color=col,label=label+' selected')
 ax[0].plot(s[:,0],s[:,2],color=col,ls='--',alpha=.6,label=label+' all ports')
ax[0].axvline(.8*np.pi*r['constants']['energy_unit_keV'],color='.4',ls=':',lw=1)
ax[0].set(xlabel='Calibrated carrier energy (keV)',ylabel='Probability / equal-width bin',title='A. Energy readout; fixed inherited scale')
ax[0].legend(fontsize=7)
x=np.arange(2);ref=[r['combiner'][p]['uniform_pass_probability'] for p in ['uniform','inherited_alpha']];opt=[r['combiner'][p]['optimal_pass_probability'] for p in ['uniform','inherited_alpha']]
ax[1].bar(x-.17,ref,.34,label='Original equal combination',color='#225ea8');ax[1].bar(x+.17,opt,.34,label='Maximum-pass diagnostic',color='#dfb14c')
ax[1].set(xticks=x,xticklabels=['Uniform','Inherited alpha'],ylabel='Unfiltered selected-port probability',title='B. Specified objective changes the optimum',ylim=(0,.32));ax[1].legend(fontsize=8)
fig.savefig(P/'physical_readout.png',dpi=180);plt.close(fig)
