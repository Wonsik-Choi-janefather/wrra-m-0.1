"""One-command result table and release verification."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
subprocess.run([sys.executable, str(ROOT/'verify.py')], check=True)
