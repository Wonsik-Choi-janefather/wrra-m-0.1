"""Independent precision/domain/comparator review and regression of old outputs."""
import json,math
import numpy as np
from decimal import Decimal,getcontext
from common import ROOT,OUT,save,checks_pass
from supply import averaging_factor,threshold_count
from metrics import collect,compare
def main():
    checks={};getcontext().prec=75;errors=[]
    for r in [0,1,1/128,1e-3,1e-6,1e-12]:
        for N in [1,2,31,128,100000,10**15,10**24]:
            rr=Decimal(str(r));nn=Decimal(N)
            if N==1 or r==0:exact=Decimal(1)
            elif r==1:exact=1/nn
            elif N<=128:exact=(nn+2*sum(((nn-k)*(1-rr)**k for k in range(1,N)),Decimal(0)))/nn**2
            else:
                # (1-r)^N <= exp(-N*r); omitted only below exp(-250),
                # far below the 75-digit precision used for this comparison.
                tail=Decimal(0) if nn*rr>250 else (1-rr)**(N+1)
                exact=(nn+2*((nn-1)*(1-rr)-nn*(1-rr)**2+tail)/rr**2)/nn**2
            error=abs(Decimal(str(averaging_factor(N,r)))/exact-1);errors.append(float(error))
            checks[f'75digit_average_N{N}_r{r:g}']=error<Decimal('1e-12')
    for r in [0,1/128,1]:checks[f'already_below_target_r{r:g}']=all(threshold_count(r,q)==1 for q in [0,.25,1])
    for N,r in [(0,.1),(1,-.1),(1,1.1),(1.5,.1)]:
        try:averaging_factor(N,r);rejected=False
        except ValueError:rejected=True
        checks[f'invalid_domain_N{N}_r{r}']=rejected
    compare(collect(OUT),json.loads((ROOT/'review/v0_1_numerical_reference.json').read_text()))
    checks['v0_1_primary_observables_preserved']=True
    nodes=np.array([0.,math.sqrt(3),-math.sqrt(3)]);weights=np.array([2/3,1/6,1/6])
    X=.7*nodes[:,None]-.4*nodes[None,:]
    var=float(np.sum(weights[:,None]*weights[None,:]*X**2));fourth=float(np.sum(weights[:,None]*weights[None,:]*X**4))
    checks['finite_ternary_fourth_order_enumeration']=abs(fourth-3*var**2)<1e-14
    c=json.loads((OUT/'CMB_higher_results.json').read_text())
    checks['common_axis_Gaussian_moment_counterexample']=all(r['common_axis_Gaussian_moment_reference_excess_kurtosis']>1 for r in c['outputs']['bandlimited_sky_cumulants'])
    checks['angular_reference_distinguished']=all(r['isotropic_angular_Gaussian_reference_excess_kurtosis']==0 for r in c['outputs']['bandlimited_sky_cumulants'])
    p=json.loads((OUT/'photon_results.json').read_text())
    checks['GDD_units_corrected']='hbar_eV²' in p['outputs']['group_delay_dispersion_definition']
    s=json.loads((OUT/'supply_results.json').read_text())
    checks['large_noise_linear_gravity_not_promoted']=not s['outputs']['linear_gravity_small_noise_control_passed']
    checks['path_entropy_not_claimed_as_universal_lower_bound']=all('minimum_path_record_entropy_at_threshold_nats' not in r for r in s['outputs']['resource_ledger'])
    result=dict(version='0.2',date='2026-10-15',review_type='Internal numerical and interpretation review, not external peer review',maximum_75_digit_averaging_relative_error=max(errors),primary_observable_regression='Unchanged from preserved v0.1 values',fixes=['Distinguish isotropic angular Gaussian reference from common-axis initial harmonics','Calculate finite common-axis Gaussian-moment comparator','Correct GDD units','Separate archive integrity and numerical reproducibility','Fix threshold/domain edge cases','Clarify entropy/linear-gravity accounting'],checks=checks_pass(checks))
    save('review_results.json',result);print('Review:',len(checks),'checks passed',flush=True);return result
if __name__=='__main__':main()
