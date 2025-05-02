from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from src.db import get_session
from src.models import Cycle, Envelope, Category

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get(
    "/",
    description="List categories at or below 20% remaining for the latest cycle"
)
def get_alerts(session: Session = Depends(get_session)):
    # 1) Find the most recent cycle
    cycle = session.exec(
        select(Cycle).order_by(Cycle.start_date.desc())
    ).first()
    if not cycle:
        return {"detail": "No cycle found."}

    # 2) Join envelopes to categories for that cycle
    stmt = (
        select(Envelope, Category)
        .where(Envelope.cycle_id == cycle.id)
        .join(Category, Envelope.category_id == Category.id)
    )
    rows = session.exec(stmt).all()

    # 3) Filter those ≤ 20% remaining
    alerts = []
    for env, cat in rows:
        if env.initial_amount > 0 and env.current_amount / env.initial_amount <= 0.20:
            alerts.append({
                "category": cat.name,
                "remaining_cents": env.current_amount,
                "initial_cents": env.initial_amount,
                "percent_left": round(env.current_amount / env.initial_amount * 100, 1),
            })

    return {
        "cycle_id": cycle.id,
        "alerts": alerts,
    }
