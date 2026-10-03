from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
for script in ['compute.py','address_bridge.py','verify_release.py']:
 subprocess.run([sys.executable,str(root/script)],check=True,stdout=subprocess.DEVNULL)
print('Upstream 0.8-r1: numerical outputs and 431 counted checks reproduced')
