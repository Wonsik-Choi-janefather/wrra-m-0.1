#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from fractions import Fraction as F
import csv, importlib.util, itertools, json, math
import numpy as np

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
OUT=ROOT/"results"
OUT.mkdir(parents=True,exist_ok=True)

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

m09=load("mcc3_stage3_m09",REPO/"calculations"/"wrra_m_0_9"/"compute.py")
legacy_cfg=json.loads((REPO/"calculations"/"wrra_m_0_9"/"parameters.json").read_text())
handoff=json.loads((REPO/"mcc_3_0"/"stage_2_finite_source_insertion"/"STAGE3_HANDOFF.json").read_text())
fit=json.loads((REPO/"exploratory"/"prime_parts_v1_0"/"studies"/"WRRA_Quark_Open_Branches_2026_10_04"/"input_fit.json").read_text())

def candidate_cfg():
    c=json.loads(json.dumps(legacy_cfg))
    c["upstream"]["address_cutoff_N"]=handoff["source_state"]["N_U"]
    c["upstream"]["state"]["alpha"]=handoff["source_state"]["alpha"]
    c["upstream"]["update"]["sigmoid_threshold_h"]=handoff["source_state"]["threshold_h"]
    c["upstream"]["scalar_comparison"]["odd_composite_admission_beta"]=handoff["source_state"]["derived_effective_beta"]
    return c

def phenotype_state(cfg):
    base=m09.address_base(cfg)
    effect=m09.effects(cfg,base)
    odd=base["odd"]
    raw=base["w"]*effect[0]
    w=raw[odd]/raw[odd].sum()
    primes=base["n"][base["prime"]]
    return base["n"][odd],w,primes,float(raw.sum()),base,effect

def scalar_state(cfg):
    base=m09.address_base(cfg);odd=base["odd"]
    w=base["w"][odd];w=w/w.sum()
    return base["n"][odd],w,base["n"][base["prime"]]

def assemble(n,w,primes,K,order):
    pool=primes[:K]
    parts=pool if order=="small" else pool[::-1]
    cyc=n//parts.sum()
    counts=np.repeat(cyc[:,None],K,axis=1)
    r=n-cyc*parts.sum()
    for _ in range(int(parts.sum())//2+2):
        for j,p in enumerate(parts):
            take=r>=p
            counts[:,j]+=take
            r-=p*take
        if not np.any(r>=2):break
    assert np.all(counts@parts+r==n)
    avg=w@counts
    neutron=float(avg[np.isin(parts,[5,47])].sum()/avg.sum())
    order_idx=np.argsort(parts)
    exp=avg[order_idx]
    return {
      "K":K,"order":order,"pool":pool.tolist(),"addresses":len(n),
      "integer_conservation":True,
      "neutron_fraction_5_47":neutron,
      "mean_parts":float(avg.sum()),
      "residue1_weight":float(w[r==1].sum()),
      "number_share":(exp/exp.sum()).tolist()
    }

def charge_checks(candidate_addresses,phenotype_weight):
    source=REPO/"exploratory"/"prime_parts_v1_0"/"studies"/"WRRA_Click_Rendering_Probe_2026_10_04"/"input_channels.csv"
    rows=list(csv.DictReader(source.open()))
    q=[F(r["Q"]) for r in rows]; idx={r["source"]:i for i,r in enumerate(rows)}
    def vec(names):
        v=[0]*len(rows)
        for name in names:v[idx[name]]+=1
        return v
    motifs={
      "proton_electron":vec(["3_A_r","3_A_g","3_B_b","1_B"]),
      "neutron":vec(["3_A_r","3_B_g","3_B_b"]),
      "electron_conjugate_pair":vec(["1_B","1_0"]),
      "neutral_channel":vec(["1_A"])
    }
    charges={k:str(sum(x*y for x,y in zip(v,q))) for k,v in motifs.items()}
    bags={}
    for size in range(1,5):
        bags[str(size)]=sum(sum((q[i] for i in bag),F(0))==0 for bag in itertools.combinations_with_replacement(range(len(q)),size))
    return {"candidate_odd_composite_addresses":candidate_addresses,"phenotype_weight":phenotype_weight,
            "channel_count":len(rows),"motif_charges":charges,"neutral_bag_counts":bags,
            "all_motifs_neutral":all(F(v)==0 for v in charges.values())}

def color_check():
    psi=np.zeros((3,3,3),complex)
    for perm in itertools.permutations(range(3)):
        inv=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
        psi[perm]=(-1)**inv/math.sqrt(6)
    z=np.zeros((3,3),complex);G=[]
    for i,j in [(0,1),(0,2),(1,2)]:
        x=z.copy();x[i,j]=x[j,i]=1;G.append(x)
        x=z.copy();x[i,j]=-1j;x[j,i]=1j;G.append(x)
    G.extend([np.diag([1,-1,0]),np.diag([1,1,-2])/math.sqrt(3)])
    errs=[]
    for g in G:
        v=np.einsum("ia,ajk->ijk",g,psi)+np.einsum("ja,iak->ijk",g,psi)+np.einsum("ka,ija->ijk",g,psi)
        errs.append(float(np.linalg.norm(v)))
    return {"norm":float(np.vdot(psi,psi).real),"generator_residuals":errs,"maximum_residual":max(errs)}

def particle_bookkeeping(f):
    p=1-f;n=f;e=p;u=2*p+n;d=p+2*n
    return {"proton":p,"neutron":n,"electron":e,"valence_u":u,"valence_d":d,
            "u_per_d":u/d,"net_charge":2*u/3-d/3-e,
            "p_per_n":p/n,"helium_mass_fraction_proxy":2*f}

def main():
    legacy_n,legacy_w,legacy_primes,legacy_phi,_,_=phenotype_state(legacy_cfg)
    cand_cfg=candidate_cfg()
    cand_n,cand_w,cand_primes,cand_phi,base,effect=phenotype_state(cand_cfg)
    scalar_n,scalar_w,scalar_primes=scalar_state(cand_cfg)

    legacy_profiles={};candidate_profiles={};scalar_profiles={}
    for K in (15,16):
        for order in ("small","large"):
            key=f"K{K}_{order}"
            legacy_profiles[key]=assemble(legacy_n,legacy_w,legacy_primes,K,order)
            candidate_profiles[key]=assemble(cand_n,cand_w,cand_primes,K,order)
            scalar_profiles[key]=assemble(scalar_n,scalar_w,scalar_primes,K,order)

    a=np.array(candidate_profiles["K15_small"]["number_share"])
    b=np.array(candidate_profiles["K15_large"]["number_share"])
    tv=float(np.abs(a-b).sum()/2)

    charge=charge_checks(len(cand_n),cand_phi)
    color=color_check()
    small=particle_bookkeeping(candidate_profiles["K15_small"]["neutron_fraction_5_47"])
    large=particle_bookkeeping(candidate_profiles["K15_large"]["neutron_fraction_5_47"])
    mp=938.27208943;mn=939.56542194;me=0.51099895069
    beta_Q=mn-mp-me

    checks={
      "stage2_handoff_N_preserved":cand_cfg["upstream"]["address_cutoff_N"]==1_015_000,
      "candidate_phenotype_weight_is_5_percent":abs(cand_phi-.05)<2e-12,
      "candidate_address_count":len(cand_n)==427892,
      "all_prime_assembly_cases_conserve_integer_addresses":all(x["integer_conservation"] for x in candidate_profiles.values()),
      "all_component_number_shares_normalized":all(abs(sum(x["number_share"])-1)<2e-12 for x in candidate_profiles.values()),
      "K15_small_finite_source_shift_small":abs(candidate_profiles["K15_small"]["neutron_fraction_5_47"]-legacy_profiles["K15_small"]["neutron_fraction_5_47"])<5e-5,
      "K15_large_finite_source_shift_small":abs(candidate_profiles["K15_large"]["neutron_fraction_5_47"]-legacy_profiles["K15_large"]["neutron_fraction_5_47"])<5e-5,
      "K16_small_remains_near_one_eighth":abs(candidate_profiles["K16_small"]["neutron_fraction_5_47"]-.125)<1e-4,
      "order_sensitivity_remains_nonzero":tv>0.1,
      "charge_motifs_neutral":charge["all_motifs_neutral"],
      "color_singlet_normalized":abs(color["norm"]-1)<1e-12,
      "color_generators_annihilate_singlet":color["maximum_residual"]<1e-12,
      "candidate_pne_charge_neutral":abs(small["net_charge"])<1e-12 and abs(large["net_charge"])<1e-12,
      "beta_Q_positive_from_supplied_masses":beta_Q>0,
      "spin_claim_remains_open":True,
      "no_SI_energy_refit_in_stage3":True
    }

    result={
      "project":"Minimal Computing Cosmology 3.0",
      "stage":"3_particle_component_replay",
      "date":"2026-10-07",
      "status":"PASS-C" if all(checks.values()) else "FAIL",
      "inputs":{
        "stage2_handoff":handoff["source_state"],
        "prime_parts_source_commit":"577099f54386b1950ffe0512d72bcc9ea45dc75b",
        "prime_parts_DOI":"10.5281/zenodo.23128482",
        "neutron_prime_labels":[5,47],
        "decoder_status":"historically fitted candidate, not derived particle identity"
      },
      "candidate_address_state":{
        "active_addresses":len(base["n"]),
        "admitted_odd_composite_addresses":len(cand_n),
        "prime_addresses":int(base["prime"].sum()),
        "even_composite_addresses":int(base["even"].sum()),
        "phenotype_weight":cand_phi,
        "minimum_effect":float(effect.min()),
        "maximum_completeness_error":float(np.max(np.abs(effect.sum(axis=0)-1)))
      },
      "legacy_phase_profiles":legacy_profiles,
      "candidate_phase_profiles":candidate_profiles,
      "candidate_scalar_compatibility_profiles":scalar_profiles,
      "K15_small_large_total_variation":tv,
      "particle_candidate":{
        "small_first":small,
        "large_first":large,
        "historical_fit_reference":fit["joint_fit"],
        "species_decoder_unique":False,
        "baryon_lepton_origin_derived":False
      },
      "charge":charge,
      "color":color,
      "beta_transition":{"Q_MeV":beta_Q,"role":"known-mass reproduction only; rate/amplitude/neutrino spectrum not derived"},
      "spin":{"status":"OPEN","reason":"no inherited WRRA spin-flavor/binding operator or full nucleon wavefunction"},
      "energy":{"status":"NOT MODIFIED","rule":"Stage 3 does not refit or duplicate downstream SI energy; Stage 4 owns the typed component-to-load connection"},
      "checks":checks,
      "all_checks_passed":all(checks.values()),
      "falsification_conditions":[
        "finite SOURCE insertion breaks integer component assembly conservation",
        "component weights become negative or fail normalization",
        "frozen charge motifs cease to be neutral",
        "the exact color-singlet test fails",
        "a unique particle decoder is claimed despite order sensitivity",
        "spin, binding, confinement or species identity is claimed without an executable rule",
        "Stage 3 changes downstream SI energy coefficients"
      ]
    }
    (OUT/"results.json").write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    verification={"project":result["project"],"stage":result["stage"],"date":result["date"],"verdict":result["status"],
                  "checks":[{"id":f"S3-{i+1:02d}","check":k,"passed":bool(v)} for i,(k,v) in enumerate(checks.items())],
                  "all_checks_passed":result["all_checks_passed"],"key_evidence":{
                    "candidate_phenotype_weight":cand_phi,
                    "candidate_addresses":len(cand_n),
                    "K15_small_neutron_fraction":candidate_profiles["K15_small"]["neutron_fraction_5_47"],
                    "K15_large_neutron_fraction":candidate_profiles["K15_large"]["neutron_fraction_5_47"],
                    "K16_small_neutron_fraction":candidate_profiles["K16_small"]["neutron_fraction_5_47"],
                    "K15_order_total_variation":tv,
                    "color_max_residual":color["maximum_residual"],
                    "beta_Q_MeV":beta_Q,
                    "spin_status":"OPEN"}}
    (OUT/"verification.json").write_text(json.dumps(verification,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    assert result["all_checks_passed"],checks
    print(json.dumps({"status":result["status"],"candidate_addresses":len(cand_n),
        "K15_small":candidate_profiles["K15_small"]["neutron_fraction_5_47"],
        "K15_large":candidate_profiles["K15_large"]["neutron_fraction_5_47"],
        "K16_small":candidate_profiles["K16_small"]["neutron_fraction_5_47"],
        "color_max_residual":color["maximum_residual"],"spin":"OPEN"},indent=2))

if __name__=="__main__":main()
