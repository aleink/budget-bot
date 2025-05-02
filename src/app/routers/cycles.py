from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from src.db import get_session
from src.models import Cycle, Envelope, Category

router = APIRouter(prefix="/cycles", tags=["cycles"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Cycle)
def create_cycle(
    cycle_in: Cycle,
    session: Session = Depends(get_session),
):
    cats = session.exec(select(Category)).all()
    if not cats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No categories defined; create some first."
        )

    session.add(cycle_in)
    session.commit()
    session.refresh(cycle_in)

    # create envelopes: split each category’s monthly_budget in half
    for cat in cats:
        half_cents = cat.monthly_budget // 2
        env = Envelope(
            cycle_id=cycle_in.id,
            category_id=cat.id,
            initial_amount=half_cents,
            current_amount=half_cents,
        )
        session.add(env)
    session.commit()

    # format pay_amount as dollars
    cycle_in.pay_amount = f"${cycle_in.pay_amount / 100:,.2f}"
    return cycle_in


@router.get("/", response_model=List[Cycle])
def list_cycles(session: Session = Depends(get_session)):
    cycles = session.exec(select(Cycle)).all()
    for c in cycles:
        c.pay_amount = f"${c.pay_amount / 100:,.2f}"
    return cycles


@router.delete("/{cycle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cycle(
    cycle_id: int,
    session: Session = Depends(get_session),
):
    cyc = session.get(Cycle, cycle_id)
    if not cyc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cycle not found."
        )
    # delete envelopes and transactions via cascade if configured, else explicitly:
    envs = session.exec(
        select(Envelope).where(Envelope.cycle_id == cycle_id)
    ).all()
    for env in envs:
        session.delete(env)
    session.delete(cyc)
    session.commit()
    return
