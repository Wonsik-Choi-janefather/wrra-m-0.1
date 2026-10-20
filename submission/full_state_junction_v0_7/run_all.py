from pathlib import Path
import subprocess,sys,json
P=Path(__file__).resolve().parent
for name in ['event_tangent.py','state_adapter.py']:
    subprocess.run([sys.executable,str(P/name)],check=True)
sys.path.insert(0,str(P))
from event_tangent import run,EOS
r=run(EOS(n=1200,nquad=240),rtol=2e-12)
(P/'results/event_tangent_refined.json').write_text(json.dumps(r,indent=2)+'\n')
subprocess.run([sys.executable,str(P/'run_checks.py')],check=True)
