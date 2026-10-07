#!/usr/bin/env python3
"""Single replay entry point for Minimal Computing Cosmology 3.0.

Stage 1 is a frozen provenance declaration. Stages 2–5 are recomputed in
dependency order, and Stage 6 then audits the regenerated ledgers.
"""
from pathlib import Path
import subprocess, sys

ROOT=Path(__file__).resolve().parent
scripts=[
 ROOT/"stage_2_finite_source_insertion"/"run_stage2.py",
 ROOT/"stage_3_particle_component_replay"/"run_stage3.py",
 ROOT/"stage_4_single_load_energy_master_ledger"/"run_stage4.py",
 ROOT/"stage_5_macro_universe_replay"/"run_stage5.py",
 ROOT/"stage_6_end_to_end_closure"/"run_stage6.py",
]
for script in scripts:
    print(f"\n=== {script.relative_to(ROOT)} ===")
    p=subprocess.run([sys.executable,str(script)],cwd=ROOT.parent)
    if p.returncode:
        raise SystemExit(f"FAILED: {script} (exit {p.returncode})")
print("\nMCC 3.0 end-to-end replay: PASS")
