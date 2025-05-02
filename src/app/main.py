from fastapi import FastAPI
from src.db import create_db_and_tables

app = FastAPI(title="Budget Bot API")        # ① CREATE APP FIRST

@app.on_event("startup")                     # ② decorators can now see `app`
def on_startup():
    create_db_and_tables()

@app.get("/ping")
async def ping():
    return {"msg": "pong"}
