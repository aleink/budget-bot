from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from src.db import get_session
from src.models import Cycle, Envelope, Category

router = APIRouter(prefix="/budget", tags=["budget"])


@router.get("/", description="Get status for the latest cycle")
def get_budget(session: Session = Depends(get_session)):
    # 1) Find the most recent cycle by date, then by id
    cycle = session.exec(
        select(Cycle)
        .order_by(Cycle.start_date.desc(), Cycle.id.desc())
    ).first()
    if not cycle:
        return {"detail": "No cycle found. Please /cycles first."}

    # 2) Load envelopes joined to categories
    stmt = (
        select(Envelope, Category)
        .where(Envelope.cycle_id == cycle.id)
        .join(Category, Envelope.category_id == Category.id)
    )
    results = session.exec(stmt).all()

    # 3) Build the status list
    out = []
    for env, cat in results:
        rem = env.current_amount
        init = env.initial_amount
        pct = round((rem / init) * 100, 1) if init > 0 else 0.0
        out.append({
            "category": cat.name,
            "remaining_cents": rem,
            "initial_cents": init,
            "percent_left": pct,
        })

    return {
        "cycle_id": cycle.id,
        "start_date": cycle.start_date,
        "budget": out,
    }
