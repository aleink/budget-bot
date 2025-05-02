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

# Health check
@app.get("/ping")
def ping():
    return {"ping": "pong"}

# Allow UI (Pages or localhost) to call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Mount your routers
app.include_router(categories,   prefix="/categories",   tags=["categories"])
app.include_router(cycles,       prefix="/cycles",       tags=["cycles"])
app.include_router(budget,       prefix="/budget",       tags=["budget"])
app.include_router(alerts,       prefix="/alerts",       tags=["alerts"])
app.include_router(transactions, prefix="/transactions", tags=["transactions"])
