# src/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import create_db_and_tables
from src.app.routers import (
    categories,
    cycles,
    budget,
    alerts,
    transactions,
)

app = FastAPI(title="Budget Bot API")

@app.get("/ping")
def ping():
    return {"ping": "pong"}

# Allow your UI to talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Mount each router exactly as defined in its file (they each have their own prefix)
app.include_router(categories)    # categories.py does `APIRouter(prefix="/categories")`
app.include_router(cycles)        # cycles.py      does `APIRouter(prefix="/cycles")`
app.include_router(budget)        # budget.py      does `APIRouter(prefix="/budget")`
app.include_router(alerts)        # alerts.py      does `APIRouter(prefix="/alerts")`
app.include_router(transactions)  # transactions.pydoes `APIRouter(prefix="/transactions")`
