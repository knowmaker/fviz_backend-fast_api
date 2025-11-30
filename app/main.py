# app/main.py
from fastapi import FastAPI

from app.api.v1 import lt

app = FastAPI(
    title="FViZ Backend",
    version="0.1.0",
)

app.include_router(lt.router, prefix="/lt", tags=["lt"])