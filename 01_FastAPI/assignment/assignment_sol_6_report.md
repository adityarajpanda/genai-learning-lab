# Q6: FastAPI vs Flask - Performance Comparison

## Method

Two equivalent minimal apps were built (`benchmark/fastapi_app.py`, `benchmark/flask_app.py`),
each exposing the same three routes:

- `GET /ping` - trivial handler, returns a static JSON object.
- `POST /echo` - accepts a JSON body and validates it (Pydantic in FastAPI,
  manual type checks in Flask), then echoes it back.
- `GET /compute` - a small CPU-bound loop (`sum(i*i for i in range(2000))`)
  to see how each framework behaves once the handler itself does real work.

Both apps were run as single-process, single-worker servers on `127.0.0.1`
(FastAPI via `uvicorn`, Flask via its built-in `threaded=True` dev server) on
the same machine, one at a time, to avoid the two competing for CPU. `run_benchmark.py`
then fired `200` requests at each route using a `ThreadPoolExecutor`, at three
concurrency levels (`1`, `10`, `50`), and measured wall-clock throughput and
per-request latency (mean/median/p95). Raw numbers are in `benchmark/benchmark_results.json`.

**Important caveat:** this compares dev servers, not production deployments.
Flask is normally put behind `gunicorn`/`waitress` with multiple sync workers
in production, and FastAPI behind `uvicorn` with multiple workers (`--workers N`)
or `gunicorn -k uvicorn.workers.UvicornWorker`. Single-worker dev-server numbers
mainly isolate *framework/server overhead per request*, not real deployment throughput.

## Results (this machine, single run)

| Route | Concurrency | FastAPI req/s | Flask req/s | FastAPI median | Flask median |
|---|---|---|---|---|---|
| GET /ping | 1 | 89.7 | 75.3 | 5.55 ms | 15.02 ms |
| GET /ping | 10 | 519.7 | 352.0 | 17.92 ms | 27.24 ms |
| GET /ping | 50 | 496.5 | 345.6 | 63.49 ms | 114.33 ms |
| POST /echo (validated) | 1 | 92.0 | 67.7 | 6.58 ms | 15.30 ms |
| POST /echo (validated) | 10 | 321.7 | 326.1 | 23.00 ms | 30.05 ms |
| POST /echo (validated) | 50 | 400.2 | 334.1 | 90.49 ms | 118.94 ms |
| GET /compute (CPU-bound) | 1 | 78.0 | 65.8 | 7.60 ms | 15.59 ms |
| GET /compute (CPU-bound) | 10 | 413.4 | 306.1 | 22.19 ms | 32.08 ms |
| GET /compute (CPU-bound) | 50 | 367.3 | 331.9 | 97.88 ms | 151.28 ms |

## Analysis

- **FastAPI was faster in almost every cell**, roughly 15-45% higher throughput
  and 30-45% lower median latency at matching concurrency. This tracks with
  FastAPI/Starlette running on an ASGI event loop (`uvicorn`), which handles
  I/O-bound waiting (accepting the next connection, reading the request body)
  without blocking a whole OS thread the way Flask's WSGI thread-per-request
  model does.
- **The gap narrows on CPU-bound work** (`/compute`) and at higher concurrency.
  Once a handler is doing real computation instead of just I/O, Python's GIL
  means neither framework's concurrency model buys much - both are ultimately
  serialized on CPU. This shows up as `/compute` having the smallest relative
  FastAPI advantage of the three routes at concurrency 50.
- **Validation overhead**: Pydantic validation on `/echo` didn't make FastAPI
  slower than Flask's hand-rolled `isinstance` checks - if anything FastAPI
  stayed ahead, since Pydantic v2's Rust core is fast enough that it isn't the
  bottleneck compared to per-request framework/server overhead.
- **Latency grows with concurrency for both** (expected - single worker process,
  more requests queueing for the same event loop / thread pool), but Flask's
  p95 grows faster, consistent with thread-per-request overhead (thread
  creation/context switching) compounding under load more than async task
  scheduling does.

## Summary

| | FastAPI | Flask |
|---|---|---|
| Concurrency model | Async (ASGI, event loop) | Sync (WSGI, thread-per-request by default) |
| Built-in request validation | Pydantic models, automatic | Manual, or add an extension (marshmallow, pydantic-flask, etc.) |
| Built-in docs | OpenAPI/Swagger UI + ReDoc, automatic | None built-in (needs flask-swagger / flasgger) |
| Raw I/O-bound throughput (this test) | Higher | Lower |
| CPU-bound throughput (this test) | Slightly higher | Comparable |
| Ecosystem maturity | Newer, smaller but fast-growing | Older, very large ecosystem/extensions |
| Best fit | APIs, especially I/O-heavy (DB calls, external HTTP calls) needing high concurrency, and projects that want typed request/response validation + auto docs for free | Simpler apps, server-rendered pages, teams already invested in Flask's extension ecosystem, or where WSGI-only hosting is a constraint |

**Conclusion:** for building APIs specifically - the scenario in this
assignment - FastAPI's async model gives it a real, measurable throughput and
latency edge for I/O-bound endpoints (the common case for APIs that talk to a
database or another service), on top of validation and documentation that
Flask doesn't provide out of the box. Flask remains a fine choice for CPU-bound
work, simpler synchronous services, or when its broader ecosystem of mature
extensions outweighs the concurrency advantage.

## Reproducing

```
cd 01_FastAPI/assignment/benchmark
python run_benchmark.py
```
