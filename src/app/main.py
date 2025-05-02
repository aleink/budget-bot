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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(categories.router,   prefix="/categories",   tags=["categories"])
app.include_router(cycles.router,       prefix="/cycles",       tags=["cycles"])
app.include_router(budget.router,       prefix="/budget",       tags=["budget"])
app.include_router(alerts.router,       prefix="/alerts",       tags=["alerts"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
