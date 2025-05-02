from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, SQLModel
from datetime import datetime
from typing import Optional

from src.db import get_session
from src.models import Transaction, Envelope, Cycle

class TransactionCreate(SQLModel):
    category_id: int
    amount:      int  # in cents

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post(
    "/", response_model=Transaction, status_code=status.HTTP_201_CREATED
)
def create_transaction(
    tx: TransactionCreate,
    session: Session = Depends(get_session),
):
    cycle = session.exec(
        select(Cycle).order_by(Cycle.start_date.desc(), Cycle.id.desc())
    ).first()
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cycle found. Please create a cycle first."
        )

    env = session.exec(
        select(Envelope).where(
            Envelope.cycle_id == cycle.id,
            Envelope.category_id == tx.category_id
        )
    ).first()
    if not env:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Envelope not found for this category."
        )

    if tx.amount > env.current_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds."
        )

    env.current_amount -= tx.amount
    session.add(env)

    record = Transaction(
        cycle_id=cycle.id,
        category_id=tx.category_id,
        amount=tx.amount,
        timestamp=datetime.utcnow()
    )
    session.add(record)
    session.commit()
    session.refresh(record)

    # format amount as dollars
    record.amount = f"${record.amount / 100:,.2f}"
    return record


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    session: Session = Depends(get_session),
):
    tx = session.get(Transaction, transaction_id)
    if not tx:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found."
        )
    # refund envelope if exists
    env = session.exec(
        select(Envelope).where(
            Envelope.cycle_id == tx.cycle_id,
            Envelope.category_id == tx.category_id
        )
    ).first()
    if env:
        env.current_amount += tx.amount
        session.add(env)

    session.delete(tx)
    session.commit()
    return
