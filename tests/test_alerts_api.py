from datetime import date

from fastapi.testclient import TestClient
from sqlmodel import Session

from src.app.main import app
from src.db import engine, create_db_and_tables
from src.models import Category, Cycle, Envelope

client = TestClient(app)

def setup_module():
    create_db_and_tables()
    with Session(engine) as session:
        # 1) One category
        cat = Category(name="LowFunds", monthly_budget=10_00)  # $10.00
        session.add(cat)
        session.commit()
        session.refresh(cat)

        # 2) One cycle
        cycle = Cycle(start_date=date(2025,5,1), pay_amount=100_00)
        session.add(cycle)
        session.commit()
        session.refresh(cycle)

        # 3) Two envelopes: one above, one below 20%
        env_ok = Envelope(
            cycle_id=cycle.id,
            category_id=cat.id,
            initial_amount=10_00//2,    # $5
            current_amount=5_00          # 100% left
        )
        env_low = Envelope(
            cycle_id=cycle.id,
            category_id=cat.id,
            initial_amount=10_00//2,    # $5
            current_amount=0             # 0% left
        )
        session.add_all([env_ok, env_low])
        session.commit()

def test_alerts_endpoint():
    resp = client.get("/alerts/")
    assert resp.status_code == 200
    data = resp.json()
    assert "cycle_id" in data
    alerts = data["alerts"]
    # Only the envelope with 0 remaining should appear
    assert len(alerts) == 1
    assert alerts[0]["category"] == "LowFunds"
    assert alerts[0]["percent_left"] == 0.0
