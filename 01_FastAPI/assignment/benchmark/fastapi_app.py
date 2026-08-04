"""Minimal FastAPI app used as one side of the FastAPI vs Flask benchmark."""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class EchoPayload(BaseModel):
    name: str
    value: int
    tags: list[str] = []


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.post("/echo")
def echo(payload: EchoPayload):
    return payload


@app.get("/compute")
def compute():
    total = sum(i * i for i in range(2000))
    return {"total": total}
