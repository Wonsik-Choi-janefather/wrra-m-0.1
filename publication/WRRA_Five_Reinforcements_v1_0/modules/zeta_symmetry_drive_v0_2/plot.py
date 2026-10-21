from pathlib import Path
import json,csv,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
with (P/'phase_noise.csv').open() as f:r=list(csv.DictReader(f))
with (P/'driven_path.csv').open() as f:t=list(csv.DictReader(f))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(10,3.2),layout='constrained')
for prep,label,col in [('uniform','Uniform','#225ea8'),('inherited_alpha','Inherited alpha','#b63d50')]:
 q=[v for v in t if v['preparation']==prep];ax[0].plot([float(v['time_over_tau']) for v in q],[float(v['selected_port_probability']) for v in q],'-o',color=col,label=label)
 q=[v for v in r if v['preparation']==prep];ax[1].plot([float(v['phase_std_rad']) for v in q],[float(v['pass_probability']) for v in q],'-o',color=col,label=label)
ax[0].set(xlabel='Post-embedding drive time / tau',ylabel='Selected-port probability',title='A. Exact driven-law readout (sampled times)');ax[0].legend(fontsize=8)
ax[1].axhline(1/70,color='.4',ls=':',label='Fully dephased 1/70')
ax[1].set(xlabel='Independent branch phase error std (rad)',ylabel='Selected-port probability',title='B. More counts need not mean more coherence');ax[1].legend(fontsize=8)
fig.savefig(P/'drive_and_noise.png',dpi=180);plt.close(fig)
