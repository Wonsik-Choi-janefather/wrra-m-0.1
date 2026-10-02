from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(root/'verify.py')],check=True)
subprocess.run([sys.executable,str(root/'write_papers.py')],check=True)
