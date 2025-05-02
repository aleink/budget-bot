from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, SQLModel, Field
from typing import Optional

from src.db import get_session
from src.models import Transaction, Envelope, Cycle

# Pydantic model for request body
class TransactionCreate(SQLModel):
    category_id: int
    amount:      int  # in cents

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post(
    "/",
    response_model=Transaction,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    tx: TransactionCreate,
    session: Session = Depends(get_session),
):
    # 1) Find latest cycle
    cycle = session.exec(
        select(Cycle).order_by(Cycle.start_date.desc(), Cycle.id.desc())
    ).first()
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cycle found. Please create a cycle first."
        )

    # 2) Fetch the envelope for this category in that cycle
    env = session.exec(
        select(Envelope).where(
            Envelope.cycle_id == cycle.id,
            Envelope.category_id == tx.category_id
        )
    ).first()
    if not env:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Envelope not found for given category in current cycle."
        )

    # 3) Check funds
    if tx.amount > env.current_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds in envelope."
        )

    # 4) Deduct
    env.current_amount -= tx.amount
    session.add(env)

    # 5) Create Transaction record
    record = Transaction(
        cycle_id=cycle.id,
        category_id=tx.category_id,
        amount=tx.amount
    )
    session.add(record)

    # 6) Commit & return
    session.commit()
    session.refresh(record)
    return record
