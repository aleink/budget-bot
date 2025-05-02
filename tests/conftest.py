"""
Make the project root importable in tests and ensure a fresh DB file.
"""
import sys, os
from pathlib import Path

# 1) Add the repo root to PYTHONPATH
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

# 2) Remove any lingering budget.db so each test run starts clean
DB = ROOT / "budget.db"
if DB.exists():
    os.remove(DB)
