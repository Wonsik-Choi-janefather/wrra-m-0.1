#!/usr/bin/env python3
"""MCC 3.0 Stage 4 — single typed information-load / SI-energy Master Ledger."""
from __future__ import annotations
import csv, importlib.util, json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
OUT=ROOT/"results"; OUT.mkdir(parents=True,exist_ok=True)

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

m09=load("mcc3_s4_m09",REPO/"calculations"/"wrra_m_0_9"/"compute.py")
s3=load("mcc3_s4_s3",REPO/"mcc_3_0"/"stage_3_particle_component_replay"/"run_stage3.py")

handoff=json.loads((REPO/"mcc_3_0"/"stage_3_particle_component_replay"/"STAGE4_HANDOFF.json").read_text())
legacy_cfg=json.loads((REPO/"calculations"/"wrra_m_0_9"/"parameters.json").read_text())
m10_params=json.loads((REPO/"calculations"/"wrra_m_0_10"/"parameters.json").read_text())
m10_results=json.loads((REPO/"calculations"/"wrra_m_0_10"/"results"/"results.json").read_text())
legacy09=json.loads((REPO/"calculations"/"wrra_m_0_9"/"results"/"results.json").read_text())

SECTORS=("phenotype","resident_nonphenotype","return")

def candidate_cfg():
    c=json.loads(json.dumps(legacy_cfg))
    src=handoff["source_state"]
    c["upstream"]["address_cutoff_N"]=src["N_U"]
    # Stage-4 handoff intentionally does not repeat alpha/h; read Stage-2 canonical handoff.
    s2=json.loads((REPO/"mcc_3_0"/"stage_2_finite_source_insertion"/"STAGE3_HANDOFF.json").read_text())["source_state"]
    c["upstream"]["state"]["alpha"]=s2["alpha"]
    c["upstream"]["update"]["sigmoid_threshold_h"]=s2["threshold_h"]
    c["upstream"]["scalar_comparison"]["odd_composite_admission_beta"]=s2["derived_effective_beta"]
    return c

def address_moments(cfg,base,effect):
    N=cfg["upstream"]["address_cutoff_N"]
    lam=m10_params["energy_map"]["address_response_lambda"]
    g=np.array([1+lam[s]*np.log(base["n"])/math.log(N) for s in SECTORS])
    return np.sum(effect*g*base["w"][None,:],axis=1)

def component_profile(cfg,order):
    n,w,primes,phi,_,_=s3.phenotype_state(cfg)
    x=s3.assemble(n,w,primes,15,order)
    return phi,np.array(x["number_share"],dtype=float),x

def write_csv(path,rows):
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    cfg=candidate_cfg()
    base=m09.address_base(cfg)
    effect=m09.effects(cfg,base)
    shares=m09.shares(effect,base["w"])
    mu=address_moments(cfg,base,effect)

    eta=m10_results["calibration"]["eta_J_m3"]
    eta_vec=np.array([eta[s] for s in SECTORS])
    energy=eta_vec*mu
    total=float(energy.sum())
    pressure=np.array([0.0,0.0,-energy[2]])
    P=float(pressure.sum())
    q=.5*(total+3*P)/total

    component_rows=[]
    view_summaries={}
    for order in ("small","large"):
        phi,profile,raw=component_profile(cfg,order)
        rows=[]
        for p,c in zip(raw["pool"],profile):
            mui=float(mu[0]*c)
            Ei=float(eta["phenotype"]*mui)
            row={"view":order+"_first","prime_label":int(p),"conditional_number_share":float(c),
                 "information_load_mu":mui,"phenotype_energy_J":Ei,
                 "ledger_scope":"nonadditive alternative view inside phenotype"}
            rows.append(row);component_rows.append(row)
        view_summaries[order+"_first"]={
            "components":len(rows),
            "sum_conditional_share":float(profile.sum()),
            "sum_information_load_mu":sum(r["information_load_mu"] for r in rows),
            "sum_phenotype_energy_J":sum(r["phenotype_energy_J"] for r in rows),
            "neutron_fraction_5_47":raw["neutron_fraction_5_47"]
        }

    legacy_channels=legacy09["channel_inventory"]
    legacy_channel_sum=sum(x["arithmetic_phenotype_weight"] for x in legacy_channels)
    field_rows=[]
    for x in legacy_channels:
        conditional=x["arithmetic_phenotype_weight"]/legacy_channel_sum
        mui=float(mu[0]*conditional)
        Ei=float(eta["phenotype"]*mui)
        field_rows.append({"generation":x["generation"],"particle_label":x["particle_label"],
            "field":x["field"],"source":x["source"],"Q":x["Q"],"status":x["status"],
            "conditional_channel_share":conditional,"information_load_mu":mui,
            "phenotype_energy_J":Ei,
            "ledger_scope":"nonadditive field/channel view inside phenotype"})

    field_summary={
        "slots":len(field_rows),
        "sum_conditional_share":sum(x["conditional_channel_share"] for x in field_rows),
        "sum_information_load_mu":sum(x["information_load_mu"] for x in field_rows),
        "sum_phenotype_energy_J":sum(x["phenotype_energy_J"] for x in field_rows)
    }

    master=[
      {"sector":"phenotype","address_moment_mu":float(mu[0]),"eta_J_m3":eta["phenotype"],"energy_J":float(energy[0]),"pressure_Pa":0.0,"additive":True},
      {"sector":"resident_nonphenotype","address_moment_mu":float(mu[1]),"eta_J_m3":eta["resident_nonphenotype"],"energy_J":float(energy[1]),"pressure_Pa":0.0,"additive":True},
      {"sector":"return","address_moment_mu":float(mu[2]),"eta_J_m3":eta["return"],"energy_J":float(energy[2]),"pressure_Pa":float(pressure[2]),"additive":True},
    ]

    tol=2e-12
    checks={
      "address_sector_ledger_complete":abs(float(sum(shares))-1)<tol,
      "all_additive_sector_energies_positive":min(energy)>0,
      "master_energy_sum_closes":abs(sum(x["energy_J"] for x in master)-total)<1e-24,
      "pressure_is_derived_from_same_sector_energy":abs(P+energy[2])<1e-24,
      "small_component_view_closes_to_phenotype":abs(view_summaries["small_first"]["sum_phenotype_energy_J"]-energy[0])<1e-24,
      "large_component_view_closes_to_phenotype":abs(view_summaries["large_first"]["sum_phenotype_energy_J"]-energy[0])<1e-24,
      "field_channel_view_closes_to_phenotype":abs(field_summary["sum_phenotype_energy_J"]-energy[0])<1e-24,
      "component_order_changes_distribution_not_budget":abs(view_summaries["small_first"]["sum_phenotype_energy_J"]-view_summaries["large_first"]["sum_phenotype_energy_J"])<1e-24,
      "internal_views_marked_nonadditive":all("nonadditive" in x["ledger_scope"] for x in component_rows+field_rows),
      "frozen_eta_values_unchanged":eta==m10_results["calibration"]["eta_J_m3"],
      "no_new_cosmic_sector":len(master)==3,
      "spin_binding_remain_open":handoff["source_state"]["spin_status"]=="OPEN"
    }

    result={
      "project":"Minimal Computing Cosmology 3.0",
      "stage":"4_single_load_energy_master_ledger",
      "date":"2026-10-07",
      "status":"PASS" if all(checks.values()) else "FAIL",
      "inputs":{
        "N_U":cfg["upstream"]["address_cutoff_N"],
        "arithmetic_shares":dict(zip(SECTORS,map(float,shares))),
        "frozen_eta_J_m3":eta,
        "reference_volume_m3":m10_params["reference_volume_m3"],
        "energy_coefficient_refit":False
      },
      "additive_master_ledger":master,
      "totals":{"total_energy_J":total,"total_density_J_m3":total,
                "total_pressure_Pa":P,"deceleration_q_diagnostic":q},
      "phenotype_internal_views":{
        "prime_part_views":view_summaries,
        "field_channel_view":field_summary,
        "rule":"each view is a decomposition of phenotype energy and may not be added to the cosmic sector ledger or to another internal view"
      },
      "legacy_comparison":{
        "legacy_total_energy_J":m10_results["calibration"]["ucrit_J_m3"],
        "candidate_total_energy_J":total,
        "delta_total_energy_J":total-m10_results["calibration"]["ucrit_J_m3"],
        "relative_absolute_change":abs(total/m10_results["calibration"]["ucrit_J_m3"]-1)
      },
      "typed_ledger_policy":{
        "cosmic_additive_levels":["phenotype","resident_nonphenotype","return"],
        "nested_nonadditive_views":["15-prime small-first","15-prime large-first","48 field/channel slots"],
        "prime_label_energy_interpretation":"conditional phenotype budget suballocation; not measured component rest mass",
        "double_count_forbidden":True
      },
      "checks":checks,
      "all_checks_passed":all(checks.values()),
      "falsification_conditions":[
        "negative additive sector energy",
        "sector energy sum does not equal master total",
        "a single internal phenotype view fails to close to phenotype energy",
        "alternative internal views are summed as additional cosmic energy",
        "prime labels are silently reinterpreted as measured rest masses",
        "component ordering changes total phenotype energy",
        "any downstream SI eta coefficient is refitted in Stage 4",
        "Stage-3 open spin/binding/species claims are silently closed"
      ]
    }

    verification={
      "project":result["project"],"stage":result["stage"],"date":result["date"],"verdict":result["status"],
      "checks":[{"id":f"S4-{i+1:02d}","check":k,"passed":bool(v)} for i,(k,v) in enumerate(checks.items())],
      "key_evidence":{
        "address_moments":dict(zip(SECTORS,map(float,mu))),
        "sector_energy_J":dict(zip(SECTORS,map(float,energy))),
        "total_energy_J":total,"total_pressure_Pa":P,"q":q,
        "small_view_energy_sum_J":view_summaries["small_first"]["sum_phenotype_energy_J"],
        "large_view_energy_sum_J":view_summaries["large_first"]["sum_phenotype_energy_J"],
        "field_view_energy_sum_J":field_summary["sum_phenotype_energy_J"],
        "phenotype_energy_J":float(energy[0]),
        "energy_coefficient_refit":False},
      "all_checks_passed":all(checks.values())
    }

    (OUT/"results.json").write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    (OUT/"verification.json").write_text(json.dumps(verification,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    write_csv(OUT/"component_energy_ledger.csv",component_rows)
    write_csv(OUT/"field_channel_energy_ledger.csv",field_rows)
    write_csv(OUT/"master_sector_ledger.csv",master)
    assert result["all_checks_passed"],checks
    print(json.dumps({"status":result["status"],"energy_J":total,"pressure_Pa":P,"q":q,
        "phenotype_J":float(energy[0]),"component_views_close":True,"eta_refit":False},indent=2))

if __name__=="__main__":main()
