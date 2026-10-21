from pathlib import Path
import json,csv,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;r=json.loads((P/'results.json').read_text())
with (P/'shared_gravity_curve.csv').open() as f:g=list(csv.DictReader(f))
with (P/'zeta_joint_constraint.csv').open() as f:z=list(csv.DictReader(f))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(10,3.2),layout='constrained')
ax[0].plot([float(a['rotation_km_s']) for a in g],[float(a['conditional_lens_arcsec']) for a in g],color='#225ea8')
v=r['gravity']['reference_rotation_km_s'];l=r['gravity']['reference_lens_arcsec']
ax[0].scatter([v],[l],color='#225ea8',label='Frozen reference');ax[0].scatter([v],[l*1.02],color='#bd3e4a',marker='x',s=45,label='Synthetic lens-only +2%')
ax[0].set(xlabel='Rotation speed (km/s)',ylabel='Conditional lens angle (arcsec)',title='A. One shared acceleration, two observables');ax[0].legend(fontsize=7)
for prep,label,col in [('uniform','Uniform','#225ea8'),('inherited_alpha','Inherited alpha','#bd3e4a')]:
 q=[a for a in z if a['preparation']==prep]
 ax[1].plot([float(a['band_fraction_of_selected']) for a in q],[float(a['conditional_energy_keV']) for a in q],color=col,label=label)
ax[1].set(xlabel='Band detections / all selected detections',ylabel='Selected conditional mean energy (keV)',title='B. Efficiency-independent zeta constraint');ax[1].legend(fontsize=8)
fig.savefig(P/'joint_constraints.png',dpi=180);plt.close(fig)
# Freeze rule: legitimate revisions remain possible, but declare changed inputs.
lock={'architecture':'Wonsik Reality-Renderer Architecture','scope':'Reference gravity and finite zeta diagnostics',
 'input_manifest_sha256':__import__('hashlib').sha256((P/'input_manifest.json').read_bytes()).hexdigest(),
 'new_observational_fit_count':0,'gravity_free_receiver_coordinates_in_reference':[],
 'gravity_if_a_eff_recalibrated':['a_eff'],
 'zeta_optional_instrument_coordinates':['common_efficiency','coherence_eta'],
 'required_shared_rule':'Do not independently refit rotation/lensing or each zeta observable while reporting one fixed model.',
 'revision_policy':'Known constants and observations may legitimately revise the model; record changed inputs, objective, fit dimension and resulting shared outputs as a new calibration branch.',
 'synthetic_data_notice':'Injections and recovery examples in this package are generated diagnostics, not measured data.'}
(P/'MODEL_LOCK.json').write_text(json.dumps(lock,indent=2))
