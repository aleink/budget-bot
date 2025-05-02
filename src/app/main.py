from fastapi import FastAPI
from src.db import create_db_and_tables
from src.app.routers import categories, cycles, budget, alerts  # add alerts

app = FastAPI(title="Budget Bot API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(categories.router)
app.include_router(cycles.router)
app.include_router(budget.router)
app.include_router(alerts.router)   # <<< new

@app.get("/ping")
async def ping():
    return {"msg": "pong"}
