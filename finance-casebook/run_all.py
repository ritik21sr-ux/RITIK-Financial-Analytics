import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
for script in ('src/run.py','src/run_advanced.py','src/presentation.py'):
    subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True)
