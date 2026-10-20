"""Fail-closed release claim gate for the actual particle/color audit.

This consumes existing evidence; it neither changes the physics nor turns
software consistency into physical validation. The five claim contracts are
explicit policy inputs, not an inferred universal theory of scientific merit.
"""
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parent

def decide(audit,dependency,requested):
    passed=audit.get('all_passed') is True and dependency.get('passed')==dependency.get('total')==4
    evidence={
      'component_replay':(passed,'Frozen component outputs and conservation were replayed.'),
      'declared_color_consistency':(passed,'Supplied representation passes the declared singlet tests.'),
      'exact_three_factor_color_constraint':(passed and audit['extended_color']['exact_common_kernel_dimension']==1,'Exact rank-one color support entails address-color factorization.'),
      'arithmetic_derivation_of_color':(False,'The audited color function reads no arithmetic state; no executable arithmetic-to-color selection rule is supplied.'),
      'order_independent_component_decoder':(passed and audit['order_total_variation']<1e-12,'Measured order TV is '+str(audit['order_total_variation'])+'; order independence is not supported.'),
    }
    decisions={k:{'allowed':bool(evidence[k][0]) if k in evidence else False,'reason':evidence[k][1] if k in evidence else 'Unknown claim: no declared evidence contract.'} for k in requested}
    return {'accepted':all(x['allowed'] for x in decisions.values()),'claims':decisions}

def main():
    a=json.loads((ROOT/'audit_results.json').read_text());d=json.loads((ROOT/'dependency_results.json').read_text())
    if len(sys.argv)>1:
        requested=json.loads(Path(sys.argv[1]).read_text());result=decide(a,d,requested)
        print(json.dumps(result,indent=2));return 0 if result['accepted'] else 2
    cases={
      'supported_release':decide(a,d,['component_replay','declared_color_consistency','exact_three_factor_color_constraint']),
      'arithmetic_origin_claim':decide(a,d,['component_replay','declared_color_consistency','arithmetic_derivation_of_color']),
      'order_independence_claim':decide(a,d,['component_replay','order_independent_component_decoder']),
      'unknown_claim':decide(a,d,['confinement_derived']),
    }
    checks={'supported_release_accepted':cases['supported_release']['accepted'],
      'arithmetic_origin_claim_rejected_despite_original_audit_passing':a['all_passed'] and not cases['arithmetic_origin_claim']['accepted'],
      'order_independence_rejected_using_actual_replay':not cases['order_independence_claim']['accepted'],
      'unknown_claim_fails_closed':not cases['unknown_claim']['accepted']}
    result={'scope':'Claim eligibility under explicit release contracts, not publication merit or observational validity.','cases':cases,'checks':checks,'passed':sum(checks.values()),'total':len(checks)}
    (ROOT/'claim_gate_results.json').write_text(json.dumps(result,indent=2)+'\n');assert all(checks.values()),checks
    print(json.dumps(result,indent=2));return 0

if __name__=='__main__':sys.exit(main())
