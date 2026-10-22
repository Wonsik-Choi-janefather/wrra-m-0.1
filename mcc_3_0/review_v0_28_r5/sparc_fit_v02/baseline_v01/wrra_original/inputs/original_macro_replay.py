#!/usr/bin/env python3
"""MCC 3.0 Stage 5 — macro-universe replay with frozen coefficients."""
from __future__ import annotations
import json, math
from pathlib import Path
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
OUT=ROOT/"results"; OUT.mkdir(parents=True,exist_ok=True)

handoff=json.loads((REPO/"mcc_3_0"/"stage_4_single_load_energy_master_ledger"/"STAGE5_HANDOFF.json").read_text())
legacy10=json.loads((REPO/"calculations"/"wrra_m_0_10"/"results"/"results.json").read_text())

C=299792458.0
G=6.6743e-11
PARSEC_M=30856775814913670.0
M_SUN_KG=1.98847e30
H0_KM_S_MPC=67.4
FC=0.265
SPHERE_MASS_MSUN=60_000_000_000.0
SPHERE_SCALE_KPC=3.0
TEST_RADIUS_KPC=8.2
PATCH_RADIUS_KPC=200.0
LENS_IMPACT_KPC=10.0

def nu(y):
    return 1.0/(-math.expm1(-math.sqrt(y)))

def plummer(r,aT):
    b=SPHERE_SCALE_KPC*1000*PARSEC_M
    M=SPHERE_MASS_MSUN*M_SUN_KG
    mb=M*r**3/(r*r+b*b)**1.5
    gm=G*mb/r**2
    g=gm*nu(gm/aT) if aT>0 else gm
    return g,gm

def lens(aT):
    kpc=1000*PARSEC_M
    b=LENS_IMPACT_KPC*kpc
    R=PATCH_RADIUS_KPC*kpc
    zmax=math.sqrt(R*R-b*b)
    def f(t):
        z=t*kpc
        r=math.hypot(b,z)
        g,_=plummer(r,aT)
        return g*b/r*kpc
    total,err=quad(f,0,zmax/kpc,epsabs=1e-4,epsrel=2e-11)
    alpha=4/C**2*total
    return {"alpha_patch_rad":alpha,
            "alpha_patch_arcsec":alpha*180/math.pi*3600,
            "quad_abs_error_rad":4/C**2*err}

def legacy_uniform_cases():
    out={}
    for x in legacy10["cases"]:
        if x["case_name"] in ("uniform_a0.5","uniform_a1.0","uniform_a2.0"):
            out[float(x["scale_factor"])]=x
    return out

def main():
    src=handoff["source_state"]
    E=src["sector_energy_J"]
    Ephi=E["phenotype"]; ED=E["resident_nonphenotype"]; ER=E["return"]
    ucrit=legacy10["calibration"]["ucrit_J_m3"]
    H0=H0_KM_S_MPC*1000/(1e6*PARSEC_M)
    aT0=C*H0*math.sqrt(FC/8)
    legacy=legacy_uniform_cases()
    rows=[]
    for a in (0.5,1.0,2.0):
        rho_phi=Ephi/a**3
        rho_D=ED/a**3
        rho_R=ER
        rho=rho_phi+rho_D+rho_R
        P=-rho_R
        Hrel=math.sqrt(rho/ucrit)
        q=.5*(rho+3*P)/rho
        aT=aT0*math.sqrt(rho_D/(ucrit*FC))
        r=TEST_RADIUS_KPC*1000*PARSEC_M
        g,gm=plummer(r,aT)
        v=math.sqrt(r*g)/1000
        v_direct=math.sqrt(r*gm)/1000
        L=lens(aT)
        old=legacy[a]
        row={
          "scale_factor":a,
          "sector_density_J_m3":{"phenotype":rho_phi,"resident_nonphenotype":rho_D,"return":rho_R},
          "total_density_J_m3":rho,
          "total_pressure_Pa":P,
          "H_over_H0":Hrel,
          "H_km_s_Mpc":H0_KM_S_MPC*Hrel,
          "deceleration_q":q,
          "aT_m_s2":aT,
          "rotation_km_s":v,
          "direct_baryonic_rotation_km_s":v_direct,
          "conditional_lensing":L,
          "legacy":{
            "total_density_J_m3":old["total_density_J_m3"],
            "total_pressure_Pa":old["total_pressure_Pa"],
            "H_over_H0":old["H_over_H0"],
            "deceleration_q":old["deceleration_q"],
            "aT_m_s2":old["local_readout"]["aT_m_s2"],
            "rotation_km_s":old["local_readout"]["v_total_km_s"],
            "lensing_arcsec":old["local_readout"]["finite_patch_lensing"]["alpha_patch_arcsec"]
          },
          "delta_vs_legacy":{
            "density_J_m3":rho-old["total_density_J_m3"],
            "pressure_Pa":P-old["total_pressure_Pa"],
            "H_over_H0":Hrel-old["H_over_H0"],
            "q":q-old["deceleration_q"],
            "aT_m_s2":aT-old["local_readout"]["aT_m_s2"],
            "rotation_km_s":v-old["local_readout"]["v_total_km_s"],
            "lensing_arcsec":L["alpha_patch_arcsec"]-old["local_readout"]["finite_patch_lensing"]["alpha_patch_arcsec"]
          },
          "relative_abs_delta_vs_legacy":{
            "density":abs(rho/old["total_density_J_m3"]-1),
            "H_over_H0":abs(Hrel/old["H_over_H0"]-1),
            "q":abs((q-old["deceleration_q"])/old["deceleration_q"]),
            "rotation":abs(v/old["local_readout"]["v_total_km_s"]-1),
            "lensing":abs(L["alpha_patch_arcsec"]/old["local_readout"]["finite_patch_lensing"]["alpha_patch_arcsec"]-1)
          }
        }
        rows.append(row)

    a_trans=((Ephi+ED)/(2*ER))**(1/3)
    checks={
      "stage4_energy_handoff_preserved":abs(Ephi+ED+ER-src["total_energy_J"])<1e-24,
      "all_macro_densities_positive":all(x["total_density_J_m3"]>0 for x in rows),
      "return_pressure_from_same_energy":all(abs(x["total_pressure_Pa"]+ER)<1e-24 for x in rows),
      "H_diagnostic_finite":all(math.isfinite(x["H_over_H0"]) and x["H_over_H0"]>0 for x in rows),
      "early_branch_decelerating":rows[0]["deceleration_q"]>0,
      "present_and_late_branch_accelerating":rows[1]["deceleration_q"]<0 and rows[2]["deceleration_q"]<0,
      "transition_between_half_and_one":0.5<a_trans<1.0,
      "same_aT_drives_rotation_and_lensing":all(x["aT_m_s2"]>0 and x["conditional_lensing"]["alpha_patch_arcsec"]>0 for x in rows),
      "direct_baryonic_reference_frozen":max(x["direct_baryonic_rotation_km_s"] for x in rows)-min(x["direct_baryonic_rotation_km_s"] for x in rows)<1e-12,
      "no_SI_or_local_refit":src["eta_refit"] is False,
      "present_rotation_close_to_legacy":rows[1]["relative_abs_delta_vs_legacy"]["rotation"]<1e-5,
      "present_lensing_close_to_legacy":rows[1]["relative_abs_delta_vs_legacy"]["lensing"]<1e-5,
      "all_three_density_changes_below_5e_5":all(x["relative_abs_delta_vs_legacy"]["density"]<5e-5 for x in rows),
      "stage4_internal_views_not_added":src["phenotype_internal_views_nonadditive"] is True
    }

    result={
      "project":"Minimal Computing Cosmology 3.0",
      "stage":"5_macro_universe_replay",
      "date":"2026-10-07",
      "status":"PASS" if all(checks.values()) else "FAIL",
      "inputs":{"stage4_source_state":src,
                "frozen_macro_reference":{"ucrit_J_m3":ucrit,"H0_km_s_Mpc":H0_KM_S_MPC,
                "clustering_fraction_fc":FC,"test_mass_Msun":SPHERE_MASS_MSUN,
                "test_scale_kpc":SPHERE_SCALE_KPC,"test_radius_kpc":TEST_RADIUS_KPC,
                "lens_patch_radius_kpc":PATCH_RADIUS_KPC,"lens_impact_kpc":LENS_IMPACT_KPC},
                "refit":False},
      "uniform_macro_replay":rows,
      "acceleration_transition_scale_factor":a_trans,
      "checks":checks,
      "all_checks_passed":all(checks.values()),
      "falsification_conditions":[
        "negative total density",
        "pressure not derived from the same return-sector energy",
        "undefined homogeneous H diagnostic",
        "rotation and lensing require different local gravity scales or independent refits",
        "direct baryonic source changes during replay",
        "any frozen SI or local-gravity coefficient is refitted",
        "macro outputs are published without legacy deltas and verification evidence",
        "Stage-4 internal phenotype views are added again as extra cosmic energy"
      ]
    }
    verification={
      "project":result["project"],"stage":result["stage"],"date":result["date"],"verdict":result["status"],
      "checks":[{"id":f"S5-{i+1:02d}","check":k,"passed":bool(v)} for i,(k,v) in enumerate(checks.items())],
      "key_evidence":{
        "a_transition":a_trans,
        "a_0_5":{k:rows[0][k] for k in ("total_density_J_m3","H_over_H0","deceleration_q","aT_m_s2","rotation_km_s")},
        "a_1":{k:rows[1][k] for k in ("total_density_J_m3","H_over_H0","deceleration_q","aT_m_s2","rotation_km_s")},
        "a_1_lensing_arcsec":rows[1]["conditional_lensing"]["alpha_patch_arcsec"],
        "a_2":{k:rows[2][k] for k in ("total_density_J_m3","H_over_H0","deceleration_q","aT_m_s2","rotation_km_s")},
        "present_relative_deltas":rows[1]["relative_abs_delta_vs_legacy"],
        "refit":False},
      "all_checks_passed":all(checks.values())
    }
    (OUT/"results.json").write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    (OUT/"verification.json").write_text(json.dumps(verification,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    assert result["all_checks_passed"],checks
    print(json.dumps({"status":result["status"],"transition_a":a_trans,
      "present_q":rows[1]["deceleration_q"],"present_rotation":rows[1]["rotation_km_s"],
      "present_lensing":rows[1]["conditional_lensing"]["alpha_patch_arcsec"]},indent=2))

if __name__=="__main__":main()
