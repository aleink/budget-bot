from datetime import date, datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Category(SQLModel, table=True):
    """
    A spending category with a monthly budget.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    monthly_budget: int  # in cents

    # back‐refs
    envelopes: List["Envelope"] = Relationship(back_populates="category")
    transactions: List["Transaction"] = Relationship(back_populates="category")


class Cycle(SQLModel, table=True):
    """
    A two‐week cycle (paycheck) into which budgets/envelopes are split.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    pay_amount: int  # the full paycheck in cents
    start_date: date = Field(default_factory=date.today)

    # back‐refs
    envelopes: List["Envelope"] = Relationship(back_populates="cycle")
    transactions: List["Transaction"] = Relationship(back_populates="cycle")


class Envelope(SQLModel, table=True):
    """
    Tracks the per‐category allocation and remaining amount for a cycle.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    cycle_id: int = Field(foreign_key="cycle.id")
    category_id: int = Field(foreign_key="category.id")
    initial_amount: int  # cents allocated at cycle start
    current_amount: int  # cents remaining

    # relationships
    cycle: "Cycle" = Relationship(back_populates="envelopes")
    category: "Category" = Relationship(back_populates="envelopes")


class Transaction(SQLModel, table=True):
    """
    Records a single expense against a cycle/envelope.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    cycle_id: int = Field(foreign_key="cycle.id")
    category_id: int = Field(foreign_key="category.id")
    amount: int  # in cents (positive number for spend)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # back‐refs
    cycle: "Cycle" = Relationship(back_populates="transactions")
    category: "Category" = Relationship(back_populates="transactions")
