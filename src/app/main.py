from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import create_db_and_tables
from src.app.routers import (
    categories,
    cycles,
    budget,
    alerts,
    transactions  # <-- our new router
)

app = FastAPI(title="Budget Bot API")

# CORS so your GitHub Pages UI can talk to it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# existing routers
app.include_router(categories.router,   prefix="/categories", tags=["categories"])
app.include_router(cycles.router,       prefix="/cycles",     tags=["cycles"])
app.include_router(budget.router,       prefix="/budget",     tags=["budget"])
app.include_router(alerts.router,       prefix="/alerts",     tags=["alerts"])

# new transactions router
app.include_router(transactions.router)
