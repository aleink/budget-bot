"""
Make the project root importable as a top-level module in tests.

By appending the repo’s root directory to sys.path, `import src...`
works whether you run tests locally on Windows or inside CI.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
