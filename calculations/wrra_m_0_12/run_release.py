from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(root.parent/'wrra_m_0_11/run_release.py')],check=True)
subprocess.run([sys.executable,str(root/'verify.py')],check=True)
subprocess.run([sys.executable,str(root/'write_papers.py')],check=True)
