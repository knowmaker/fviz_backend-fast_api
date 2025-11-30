# app/main.py
from fastapi import FastAPI

app = FastAPI(
    title="FViZ Backend",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "FViZ backend is running"}
