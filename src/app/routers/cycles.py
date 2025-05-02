from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from src.db import get_session
from src.models import Cycle, Category, Envelope

router = APIRouter(prefix="/cycles", tags=["cycles"])


class CycleCreate(Cycle, table=False):
    # Optional start_date (defaults to today), required pay_amount in cents
    start_date: Optional[date] = date.today()


@router.post("/", response_model=Cycle, status_code=status.HTTP_201_CREATED)
def create_cycle(
    payload: CycleCreate,
    session: Session = Depends(get_session),
):
    # 1. Record the cycle
    cycle = Cycle(start_date=payload.start_date, pay_amount=payload.pay_amount)
    session.add(cycle)
    session.commit()
    session.refresh(cycle)

    # 2. Seed envelopes for every category
    categories = session.exec(select(Category)).all()
    if not categories:
        raise HTTPException(400, "No categories defined; create some first.")

    half = lambda mb: mb // 2
    for cat in categories:
        env = Envelope(
            cycle_id=cycle.id,
            category_id=cat.id,
            initial_amount=half(cat.monthly_budget),
            current_amount=half(cat.monthly_budget),
        )
        session.add(env)

    session.commit()
    return cycle
