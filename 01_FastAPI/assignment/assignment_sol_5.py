"""
FastAPI application with two endpoints backed by the EURI API
(https://api.euron.one):

  POST /generate/text   - text completion using a GPT-5 mini style chat model
  POST /generate/image  - image generation

Rate limiting
-------------
Each endpoint is limited to RATE_LIMIT_MAX_CALLS calls per RATE_LIMIT_WINDOW_SECONDS
per client IP, using an in-memory sliding window. This needs no extra
dependencies, but only works within a single process - if you run uvicorn
with multiple workers, each worker has its own independent counter. For a
multi-worker/multi-instance deployment, back the limiter with Redis instead
(e.g. the `slowapi` + `redis` libraries).

Configuring the API key
------------------------
1. Sign up at https://euron.one and generate an API key.
2. Add it to the `.env` file at the project root:
       EURI_API_KEY=your-api-key-here
   (`.env.example` at the project root already lists this variable.)
3. Optionally override the default models via `.env`:
       EURI_TEXT_MODEL=gpt-5-mini
       EURI_IMAGE_MODEL=gpt-4.1-nano
   python-dotenv (already used across this project) loads `.env` automatically.
"""

import os
import time
from collections import defaultdict, deque
from typing import Deque, Dict

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

load_dotenv()

EURI_API_KEY = os.getenv("EURI_API_KEY")
EURI_TEXT_MODEL = os.getenv("EURI_TEXT_MODEL", "gpt-5-mini")
EURI_IMAGE_MODEL = os.getenv("EURI_IMAGE_MODEL", "gpt-4.1-nano")

EURI_CHAT_URL = "https://api.euron.one/api/v1/euri/chat/completions"
EURI_IMAGE_URL = "https://api.euron.one/api/v1/euri/images/generations"

RATE_LIMIT_MAX_CALLS = 5
RATE_LIMIT_WINDOW_SECONDS = 60

app = FastAPI(
    title="EURI Generation API",
    description="Text and image generation via the EURI API, with per-client rate limiting.",
    version="1.0.0",
)

# client_ip -> deque of call timestamps (per-endpoint buckets)
_call_history: Dict[str, Dict[str, Deque[float]]] = defaultdict(
    lambda: {"text": deque(), "image": deque()}
)


def enforce_rate_limit(request: Request, bucket: str) -> None:
    """Raise 429 if this client has exceeded the allowed calls for `bucket`."""
    client_ip = request.client.host if request.client else "unknown"
    now = time.monotonic()
    history = _call_history[client_ip][bucket]

    while history and now - history[0] > RATE_LIMIT_WINDOW_SECONDS:
        history.popleft()

    if len(history) >= RATE_LIMIT_MAX_CALLS:
        retry_after = RATE_LIMIT_WINDOW_SECONDS - (now - history[0])
        raise HTTPException(
            status_code=429,
            detail=(
                f"Rate limit exceeded: max {RATE_LIMIT_MAX_CALLS} requests per "
                f"{RATE_LIMIT_WINDOW_SECONDS}s. Retry in {retry_after:.1f}s."
            ),
        )

    history.append(now)


def require_api_key() -> str:
    if not EURI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="EURI_API_KEY environment variable is not configured.",
        )
    return EURI_API_KEY


# ── Request/response models ──────────────────────────────────────────
class TextGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    max_tokens: int = Field(default=1000, gt=0, le=4000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    size: str = Field(default="1024x1024")
    n: int = Field(default=1, gt=0, le=4)


# ── Endpoints ─────────────────────────────────────────────────────────
@app.post(
    "/generate/text",
    summary="Generate text with the EURI GPT-5 mini model",
    responses={429: {"description": "Rate limit exceeded"}},
)
def generate_text(body: TextGenerationRequest, request: Request):
    enforce_rate_limit(request, "text")
    api_key = require_api_key()

    payload = {
        "messages": [{"role": "user", "content": body.prompt}],
        "model": EURI_TEXT_MODEL,
        "max_tokens": body.max_tokens,
        "temperature": body.temperature,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    try:
        response = requests.post(EURI_CHAT_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"EURI API request failed: {exc}")

    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return {"model": EURI_TEXT_MODEL, "text": content, "usage": data.get("usage")}


@app.post(
    "/generate/image",
    summary="Generate an image with the EURI image generation endpoint",
    responses={429: {"description": "Rate limit exceeded"}},
)
def generate_image(body: ImageGenerationRequest, request: Request):
    enforce_rate_limit(request, "image")
    api_key = require_api_key()

    payload = {
        "model": EURI_IMAGE_MODEL,
        "prompt": body.prompt,
        "n": body.n,
        "size": body.size,
        "response_format": "url",
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(EURI_IMAGE_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"EURI API request failed: {exc}")

    data = response.json()
    return {"model": EURI_IMAGE_MODEL, "images": data.get("data", [])}
