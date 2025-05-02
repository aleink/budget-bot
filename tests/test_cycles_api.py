from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.app.main import app
from src.db import engine, create_db_and_tables
from src.models import Category, Envelope

client = TestClient(app)

def setup_module():
    create_db_and_tables()
    with Session(engine) as session:
        session.add_all([
            Category(name="Foo", monthly_budget=100_00),
            Category(name="Bar", monthly_budget=200_00),
        ])
        session.commit()

def test_deposit_creates_cycle_and_envelopes():
    resp = client.post("/cycles/", json={"pay_amount": 4_200_00})
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data

    cycle_id = data["id"]
    with Session(engine) as session:
        envs = session.exec(
            select(Envelope).where(Envelope.cycle_id == cycle_id)
        ).all()
        assert len(envs) == 2
        assert sorted(e.initial_amount for e in envs) == [50_00, 100_00]
