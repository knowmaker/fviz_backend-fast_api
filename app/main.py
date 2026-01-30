# app/main.py
from fastapi import FastAPI

from app.api.v1 import lt, gk, users

app = FastAPI(
    title="FViZ Backend",
    version="0.1.0",
)

app.include_router(lt.router, prefix="/lt", tags=["lt"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(gk.router, prefix="/gk", tags=["gk"])