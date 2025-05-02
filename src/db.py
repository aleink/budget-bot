"""
Database setup and session helper for Budget Bot.

• Creates/opens an SQLite file called `budget.db` in the repo root.
• Exposes `create_db_and_tables()` to run at startup.
• Exposes `get_session()` as a FastAPI dependency that yields a
  short-lived SQLModel Session.
"""

from pathlib import Path
from typing import Generator

from sqlmodel import SQLModel, Session, create_engine

# --------------------------------------------------------------------------- #
# Engine
# --------------------------------------------------------------------------- #

DB_PATH = Path(__file__).resolve().parent.parent / "budget.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# --------------------------------------------------------------------------- #
# DDL helper
# --------------------------------------------------------------------------- #


def create_db_and_tables() -> None:
    """
    Create all tables declared with SQLModel subclasses.

    Safe to call multiple times; it only creates missing tables.
    """
    SQLModel.metadata.create_all(engine)


# --------------------------------------------------------------------------- #
# FastAPI dependency
# --------------------------------------------------------------------------- #


def get_session() -> Generator[Session, None, None]:
    """
    Yield a SQLModel Session bound to the global engine.

    Usage inside a FastAPI endpoint:

        @router.get("/")
        def endpoint(session: Session = Depends(get_session)):
            ...
    """
    with Session(engine) as session:
        yield session


# --------------------------------------------------------------------------- #
# CLI convenience: `python -m src.db`
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    create_db_and_tables()
    print(f"✔ Database initialised at {DB_PATH}")
