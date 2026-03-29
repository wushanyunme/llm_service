
from fastapi import FastAPI
from datetime import datetime
from app.api.routes import router

app = FastAPI(title = "LLM Platform API", version = "1.0.0")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}