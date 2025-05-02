"""
Pytest configuration: make the repo importable, enable TESTING mode,
and reset the DB tables before each test module.
"""
import os
import sys
from pathlib import Path

# 1) Make the repo root importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

# 2) Signal to src/db.py that we're in TESTING (use in-memory DB)
os.environ["TESTING"] = "1"

import pytest
from sqlmodel import SQLModel
from src.db import engine

@pytest.fixture(autouse=True, scope="module")
def reset_db():
    """
    Drop and re-create all tables before each test module,
    ensuring no data leaks between test files.
    """
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
