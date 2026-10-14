from pathlib import Path
import csv,json,math
import numpy as np
ROOT=Path(__file__).resolve().parent
IN=ROOT/'inputs';OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
CFG=json.loads((IN/'frozen_tests.json').read_text())
CLOCK=json.loads((IN/'clock.json').read_text())
C=CLOCK['c_m_s'];HB=CLOCK['h_J_s']/(2*math.pi)
HB_EV=HB/CLOCK['e_J_per_eV']
DT=CLOCK['epsilon']*HB_EV/CLOCK['mode_energy_eV'];ELL=C*DT
def csvwrite(name,rows):
    with (OUT/name).open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
def save(name,data):
    def scalar(value):
        if isinstance(value,np.generic):return value.item()
        if isinstance(value,np.ndarray):return value.tolist()
        raise TypeError(type(value).__name__)
    (OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False,default=scalar,allow_nan=False)+'\n')
def checks_pass(checks):
    checks={k:bool(v) for k,v in checks.items()}
    assert all(checks.values()),checks
    return checks
