"""One-command common-ledger reproduction and verification."""
from pathlib import Path
import subprocess
import sys
subprocess.run([sys.executable,str(Path(__file__).with_name('verify.py'))],check=True)
