"""Reviewed scalar input contract; inherited numerical kernels stay frozen."""
import math
def validate_scalars(inp):
    for key in ('kappa','neutron_mean_life_s'):
        value=inp['inherited'][key]
        if isinstance(value,bool) or not math.isfinite(value) or value<=0:
            raise ValueError(key+' must be finite and positive')
    for name in ('proton','neutron'):
        value=inp['magnetic_moments_muN'][name]
        if isinstance(value,bool) or not math.isfinite(value):
            raise ValueError(name+' moment must be finite')
