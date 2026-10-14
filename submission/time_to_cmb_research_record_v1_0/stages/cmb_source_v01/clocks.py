"""Represent standard-completion CMB physical times in the existing shutter unit."""
import json
import camb
from calculate import ROOT,OUT,params
frozen=json.loads((ROOT/'inputs/source_frozen_inputs.json').read_text())
Gyr_s=365.25*86400*1e9
rows=[]
for b in ['weighted','unweighted']:
    r=camb.get_background(params(b,'standard',2.5));d=r.get_derived_params();z=d['zstar']
    t=r.physical_time(z)*Gyr_s;now=r.physical_time(0)*Gyr_s
    rows.append(dict(branch=b,zstar=z,recombination_physical_age_s=t,recombination_age_years=t/(Gyr_s/1e9),
        recombination_shutter_units=t/frozen['dt_s'],today_age_Gyr=d['age'],today_shutter_units=now/frozen['dt_s'],
        comoving_distance_to_last_scattering_Mpc=r.comoving_radial_distance(z),dt_s=frozen['dt_s'],
        status='Representation in inherited calibrated shutter units; background physical time computed by the declared FRW/CAMB completion, not a SOURCE-only derivation of the SI second.'))
(OUT/'CMB_physical_time_and_shutter_units.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows),flush=True)
