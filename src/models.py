"""
All SQLModel tables for Budget Bot.
Amounts are stored in **cents** (INTEGER) to avoid float rounding errors.
"""

from __future__ import annotations

from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


# --------------------------------------------------------------------------- #
# 1 · Category – monthly budget template                                     #
# --------------------------------------------------------------------------- #

class Category(SQLModel, table=True):
    """Budget category, e.g. 'Groceries' or 'Rent'."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, max_length=50)
    monthly_budget: int  # cents


# --------------------------------------------------------------------------- #
# 2 · Cycle – one row per salary deposit                                      #
# --------------------------------------------------------------------------- #

class Cycle(SQLModel, table=True):
    """Bi-weekly (or twice-monthly) pay period started by a salary deposit."""
    id: Optional[int] = Field(default=None, primary_key=True)
    start_date: date
    end_date: Optional[date] = Field(default=None)
    pay_amount: int  # cents


# --------------------------------------------------------------------------- #
# 3 · Envelope – half-month slice of a category budget                        #
# --------------------------------------------------------------------------- #

class Envelope(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # FK → Cycle
    cycle_id: int = Field(foreign_key="cycle.id")

    # FK → Category
    category_id: int = Field(foreign_key="category.id")

    initial_amount: int  # cents
    current_amount: int
