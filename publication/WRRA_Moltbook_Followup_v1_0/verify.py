"""Second verification: high-precision/modal, exhaustive and independent ledgers.

Not an independent human review; this is a separate numerical/logic route.
Mutation counts describe the listed isolated corruptions, not global coverage.
"""
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
import copy
import itertools
import json
import math
import mpmath as mp
import life
import neuro

P=Path(__file__).resolve().parent
checks={}
def check(name,value):
    checks[name]=bool(value)
    if not value:raise AssertionError(name)


def enumerate_paths(budget,feedback):
    """Enumerate every binary action path; does not call the DP implementation."""
    out=defaultdict(float)
    for actions in itertools.product((0,1),repeat=len(feedback)):
        remaining=budget;weight=1.0;r=0.0
        for action,failed in zip(actions,feedback):
            score=1.2+.9*remaining/budget-1.1*r
            p=math.exp(score)/(1+math.exp(score)) if remaining>0 else 0
            weight*=p if action else 1-p
            if action:
                if remaining==0:weight=0;break
                remaining-=1
            r=.8*r+.4*failed
        out[remaining]+=weight
    return out


def main():
    c=json.loads((P/'cosmos_results.json').read_text())
    mp.mp.dps=60
    differences=[]
    for row in c['rows']:
        n=row['n'];mode=row['mode']
        k=[2*mp.pi*m for m in mode];k2=sum(x*x for x in k)
        # Cosine eigenvalue identity instead of float64 sine-square formula.
        eigen=sum(2*n*n*(1-mp.cos(x/n)) for x in k)
        exact=1-mp.sqrt(eigen/k2)
        differences.append(abs(float(exact)-row['phase_speed_error']))
    check('60digit_directional_crosscheck',max(differences)<3e-15)
    check('nonzero_finite_direction_effect',c['rows'][0]['phase_speed_error']!=c['rows'][1]['phase_speed_error'])
    check('boost_claim_explicitly_open',c['boost_test'].startswith('OPEN'))
    baseline=json.loads((P/'inputs/baseline_rerun_summary.json').read_text())
    check('inherited_rerun_179',baseline['passed']==baseline['total']==179)
    l=json.loads((P/'life_results.json').read_text())
    for case in l['cases'][:2]:
        events=case['events']
        for key in ('substrate','energy_tokens'):
            # Global rational balance, independent of step-by-step audit.
            initial=Fraction(events[0]['before'][key])
            inflow=sum(Fraction(e['inflow'][key]) for e in events)
            used=sum(Fraction(e['consumed'][key]) for e in events)
            final=Fraction(events[-1]['after'][key])
            check(case['name']+'_'+key+'_global_balance',initial+inflow-used==final)
    check('finite_stock_capacity_independent',l['completed_cycles'][0]==min(8//2,12//3))
    check('external_supply_not_erased',l['cases'][1]['events'][-1]['after']=={'substrate':2,'energy_tokens':6})
    base=copy.deepcopy(l['cases'][1]['events'])
    check('valid_trace_accepted',life.audit(base)[0]=='READY')
    mutations=[]
    def mutate(name,fn,expected='FAIL'):
        changed=copy.deepcopy(base);fn(changed);result=life.audit(changed)
        mutations.append(dict(name=name,expected=expected,actual=result[0],reason=result[1]))
        check('mutation_'+name,result[0]==expected)
    mutate('duplicate_id',lambda x:x[2].update(id=x[1]['id']))
    mutate('broken_parent',lambda x:x[2].update(parent='absent'))
    mutate('missing_machinery',lambda x:x[1].update(machinery=False))
    mutate('missing_boundary',lambda x:x[1].update(boundary=False))
    mutate('missing_information',lambda x:x[1].update(information=False))
    mutate('fabricated_stock',lambda x:x[1]['after'].update(substrate=99))
    mutate('hidden_inflow',lambda x:x[1]['inflow'].update(substrate=0))
    mutate('negative_stock',lambda x:x[1]['before'].update(substrate=-1))
    mutate('nonfinite_stock',lambda x:x[1]['before'].update(substrate=float('nan')))
    mutate('wrong_resource_type',lambda x:x[1]['before'].update(substrate='7'))
    mutate('missing_resource_species',lambda x:x[1]['after'].pop('substrate'))
    mutate('omitted_cost',lambda x:x[1]['consumed'].update(energy_tokens=0))
    mutate('state_discontinuity',lambda x:(x[2]['before'].update(substrate=10),x[2]['after'].update(substrate=9)))
    mutate('missing_record_field',lambda x:x[1].pop('information'),'OPEN')
    mutate('unmeasured_resource',lambda x:x[1]['inflow'].update(substrate=None),'OPEN')
    mutate('unmeasured_machinery',lambda x:x[1].update(machinery=None),'OPEN')
    n=json.loads((P/'neuro_results.json').read_text())
    r=Fraction(2)*(1-Fraction(4,5)**5)
    check('original_residue_exact_replay',abs(float(r)-n['original_five_failure_residue'])<1e-15)
    check('published_probability_replay',abs(n['original_model'][0]['probability']-.650422)<.5e-6 and abs(n['original_model'][1]['probability']-.497724)<.5e-6)
    check('lower_mean_can_have_higher_variance',n['original_model'][0]['probability']>n['original_model'][1]['probability'] and n['original_model'][0]['bernoulli_variance']<n['original_model'][1]['bernoulli_variance'])
    for b in (1,3,6):
        f=[1,1,0,1,0,0,0,1]
        enum=enumerate_paths(b,f);dp=neuro.distribution(b,f)['final_distribution']
        check(f'exhaustive_256_paths_budget_{b}',max(abs(enum[k]-dp.get(str(k),0)) for k in range(b+1))<1e-14)
    for kind in ('full','residue_ablated'):
        for row in n[kind]:
            b=row['budget'];dist={int(k):v for k,v in row['final_distribution'].items()}
            mean=sum((b-k)*v for k,v in dist.items())
            var=sum((b-k)**2*v for k,v in dist.items())-mean**2
            check(f'{kind}_{b}_budget_bounds',0<=row['mean_actions']<=b and min(dist)>=0 and abs(sum(dist.values())-1)<2e-14)
            check(f'{kind}_{b}_second_moment',abs(var-row['variance_actions'])<1e-12)
    e=json.loads((P/'energy_results.json').read_text())
    # Direct average log multiplicity within each retained-state group.
    states=list(itertools.product((0,1),repeat=2))
    keys=[lambda a,b:(a&b,),lambda a,b:(a,a&b),lambda a,b:(a,b,a&b)]
    for i,key in enumerate(keys):
        groups=defaultdict(list)
        for a,b in states:groups[key(a,b)].append((a,b))
        lost=sum(len(v)/4*math.log2(len(v)) for v in groups.values())
        check(f'conditional_entropy_by_enumeration_{i}',abs(lost-e['rows'][i]['discarded_bits'])<1e-15)
    check('one_input_not_sufficient',(0&0)==(0&1) and (0,0)!=(0,1) and e['rows'][1]['discarded_bits']==.5)
    check('reversible_embedding_eight_states',e['reversible_states_checked']==8)
    check('no_device_heat_claim','measured complete-cycle work and heat' in e['missing_for_device_claim'])
    # Synthetic confounding witness: independent errors conditional on difficulty.
    easy=Fraction(1,10);hard=Fraction(7,10)
    marginal=(easy+hard)/2;joint=(easy**2+hard**2)/2
    cov=joint-marginal**2
    check('difficulty_can_create_shared_errors',cov==Fraction(9,100))
    verification=dict(passed=sum(checks.values()),total=len(checks),checks=checks,
      max_60digit_phase_error_difference=max(differences),mutations=mutations,
      synthetic_difficulty_control=dict(marginal_error=float(marginal),joint_error=float(joint),naive_independence_joint=float(marginal**2),conditional_error_covariance=0,pooled_error_covariance=float(cov)),
      scope='Separate numerical/logic verification by the same workflow, not a third-party review. 16 isolated data corruptions and missing-evidence controls; not exhaustive defect coverage. Shared-error example is constructed, not new AI test data.')
    (P/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    print(json.dumps({k:verification[k] for k in ('passed','total','max_60digit_phase_error_difference')},indent=2))

if __name__=='__main__':main()
