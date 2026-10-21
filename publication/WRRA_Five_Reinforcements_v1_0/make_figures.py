from pathlib import Path
import json,numpy as np,matplotlib,shutil
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;M=P/'modules';(P/'figures').mkdir(exist_ok=True)
a=json.loads((M/'finite_scale_bridge_v0_1/results.json').read_text());b=json.loads((M/'source_carrier_action_v0_1/results.json').read_text())
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(10,3.2),layout='constrained');rr=a['refinement'];nn=[r['n'] for r in rr]
ax[0].loglog(nn,[r['poisson_relative_L2'] for r in rr],'-o',label='3D potential');ax[0].loglog(nn,[r['center_force_relative_L2'] for r in rr],'-s',label='3D centered force');ax[0].set(xlabel='Samples per axis',ylabel='Relative L2 error',title='A. Separate finite 3D receiver witness');ax[0].legend(fontsize=8)
for branch,col in [('weighted','#225ea8'),('unweighted','#bd3e4a')]:
 rows=[r for r in b['coupled_results'] if r['branch']==branch and r['coupling']=='source_shaped'];ax[1].plot([r['n'] for r in rows],[r['endpoint_record_probability'] for r in rows],'-o',label=branch,color=col)
ax[1].axhline(.5,color='.4',ls=':',label='Uniform coupling');ax[1].set(xlabel='Profile samples',ylabel='Record probability at tau',title='B. Frozen-payload source-shaped coupling',ylim=(.30,.52));ax[1].legend(fontsize=8)
fig.savefig(P/'figures/scaling_action.png',dpi=190);plt.close(fig)
for src,dst in [(M/'local_twist_load_bridge_v0_3/three_dimensional_receiver.png','twist_receiver.png'),(M/'freedom_falsifiability_v0_1/joint_constraints.png','joint_constraints.png'),(M/'zeta_physical_readout_v0_1/physical_readout.png','zeta_readout.png')]:shutil.copyfile(src,P/'figures'/dst)
