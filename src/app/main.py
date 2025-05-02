from fastapi import FastAPI

app = FastAPI(title="Budget Bot API")

@app.get("/ping")
async def ping():
    """
    Health-check endpoint.
    """
    return {"msg": "pong"}
