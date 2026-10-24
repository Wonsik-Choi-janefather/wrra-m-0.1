"""Executable synthetic audit profile for How Life Runs v2.7.4, chapters 2/26.

Two independent resource ledgers are symbolic units, not ATP/mass equivalence.
No measured cellular trajectories, organism model, or biological efficacy claim.
"""
import copy
import math

REQUIRED=('id','parent','before','inflow','consumed','after','machinery','boundary','information','success')
COST={'substrate':2,'energy_tokens':3}


def audit(events):
    seen=set(); previous=None
    for event in events:
        if any(k not in event or (event[k] is None and k!='parent') for k in REQUIRED):
            return 'OPEN','missing_evidence'
        if event['id'] in seen or event['parent'] != previous:
            return 'FAIL','lineage_identity'
        if type(event['success']) is not bool or any(type(event[k]) is not bool for k in ('machinery','boundary','information')):
            return 'FAIL','invalid_boolean'
        for field in ('before','inflow','consumed','after'):
            if set(event[field])!=set(COST):return 'FAIL','resource_schema'
            for value in event[field].values():
                if value is None:return 'OPEN','unmeasured_resource'
                if type(value) not in (int,float) or not math.isfinite(value) or value<0:
                    return 'FAIL','invalid_resource'
        if previous is not None and event['before']!=events[len(seen)-1]['after']:
            return 'FAIL','state_discontinuity'
        for key in COST:
            if abs(event['before'][key]+event['inflow'][key]-event['consumed'][key]-event['after'][key])>1e-12:
                return 'FAIL','resource_balance'
            if event['consumed'][key] != (COST[key] if event['success'] else 0):
                return 'FAIL','execution_cost'
        ready=event['machinery'] and event['boundary'] and event['information']
        if event['success'] and not ready:return 'FAIL','missing_execution_layer'
        seen.add(event['id']);previous=event['id']
    if not events:return 'OPEN','no_events'
    last=events[-1]
    next_ready=all(last[k] for k in ('machinery','boundary','information')) and all(last['after'][k]>=v for k,v in COST.items())
    return ('READY' if next_ready else 'NOT_READY'),'current_observed_state'


def make_trace(inflow, cycles=6):
    stock={'substrate':8,'energy_tokens':12};events=[]
    for i in range(cycles):
        available={k:stock[k]+inflow[k] for k in COST}
        success=all(available[k]>=COST[k] for k in COST)
        consumed={k:COST[k] if success else 0 for k in COST}
        after={k:available[k]-consumed[k] for k in COST}
        events.append(dict(id=f'g{i+1}',parent=f'g{i}' if i else None,before=stock.copy(),
          inflow=inflow.copy(),consumed=consumed,after=after,machinery=True,boundary=True,information=True,success=success))
        stock=after
        if not success:break
    return events


def run():
    closed=make_trace({'substrate':0,'energy_tokens':0})
    supported=make_trace({'substrate':1,'energy_tokens':2})
    incomplete=copy.deepcopy(supported);incomplete[2]['inflow']['substrate']=None
    cases=[dict(name='finite_internal_stock',events=closed,decision=audit(closed)),
           dict(name='recorded_external_supply',events=supported,decision=audit(supported)),
           dict(name='unmeasured_external_supply',events=incomplete,decision=audit(incomplete))]
    assert audit(closed)[0]=='NOT_READY'
    assert audit(supported)[0]=='READY'
    assert audit(incomplete)[0]=='OPEN'
    return dict(cases=cases,completed_cycles=[sum(e['success'] for e in c['events']) for c in cases[:2]],
      scope='Synthetic ledger execution, not cell simulation. READY is current execution capacity, not indefinite self-maintenance. External nutrient/resource dependence is explicit, not a failure by itself. No population or division is simulated.')
