"""
Benchmark runner for question 6: compares FastAPI (Uvicorn/ASGI) against
Flask (Werkzeug dev server/WSGI) on three routes - a trivial GET, a
validated POST, and a small CPU-bound GET - across a few concurrency levels.

Usage:
    python run_benchmark.py

Writes a JSON results file (benchmark_results.json) alongside this script
and prints a summary table to stdout.
"""

import json
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

HERE = Path(__file__).parent
PYTHON = sys.executable

FASTAPI_PORT = 8010
FLASK_PORT = 8011

REQUESTS_PER_RUN = 200
CONCURRENCY_LEVELS = [1, 10, 50]

ROUTES = {
    "GET /ping (trivial)": {"method": "GET", "path": "/ping", "json": None},
    "POST /echo (validated)": {
        "method": "POST",
        "path": "/echo",
        "json": {"name": "widget", "value": 42, "tags": ["a", "b"]},
    },
    "GET /compute (CPU-bound)": {"method": "GET", "path": "/compute", "json": None},
}


def wait_for_server(base_url: str, timeout: float = 15.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            r = requests.get(f"{base_url}/ping", timeout=1)
            if r.status_code == 200:
                return
        except requests.RequestException:
            pass
        time.sleep(0.2)
    raise RuntimeError(f"Server at {base_url} did not become ready in time.")


def fire_request(base_url: str, route: dict) -> float:
    start = time.perf_counter()
    if route["method"] == "GET":
        requests.get(base_url + route["path"], timeout=10)
    else:
        requests.post(base_url + route["path"], json=route["json"], timeout=10)
    return time.perf_counter() - start


def run_load(base_url: str, route: dict, concurrency: int, total_requests: int) -> dict:
    latencies = []
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [pool.submit(fire_request, base_url, route) for _ in range(total_requests)]
        for f in futures:
            latencies.append(f.result())
    wall_time = time.perf_counter() - start

    latencies_ms = sorted(l * 1000 for l in latencies)
    return {
        "concurrency": concurrency,
        "total_requests": total_requests,
        "wall_time_s": round(wall_time, 3),
        "throughput_rps": round(total_requests / wall_time, 1),
        "latency_mean_ms": round(statistics.mean(latencies_ms), 2),
        "latency_median_ms": round(statistics.median(latencies_ms), 2),
        "latency_p95_ms": round(latencies_ms[int(len(latencies_ms) * 0.95) - 1], 2),
    }


def benchmark_app(name: str, base_url: str) -> dict:
    results = {}
    for route_name, route in ROUTES.items():
        results[route_name] = []
        for concurrency in CONCURRENCY_LEVELS:
            stats = run_load(base_url, route, concurrency, REQUESTS_PER_RUN)
            results[route_name].append(stats)
            print(
                f"  [{name}] {route_name:<26} concurrency={concurrency:<3} "
                f"-> {stats['throughput_rps']:>7.1f} req/s, "
                f"median={stats['latency_median_ms']:>6.2f}ms, "
                f"p95={stats['latency_p95_ms']:>6.2f}ms"
            )
    return results


def main():
    print("Starting FastAPI (uvicorn) server...")
    fastapi_proc = subprocess.Popen(
        [PYTHON, "-m", "uvicorn", "fastapi_app:app", "--host", "127.0.0.1", "--port", str(FASTAPI_PORT)],
        cwd=HERE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("Starting Flask (werkzeug) server...")
    flask_proc = subprocess.Popen(
        [PYTHON, "flask_app.py", str(FLASK_PORT)],
        cwd=HERE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        fastapi_url = f"http://127.0.0.1:{FASTAPI_PORT}"
        flask_url = f"http://127.0.0.1:{FLASK_PORT}"
        wait_for_server(fastapi_url)
        wait_for_server(flask_url)

        print("\nRunning FastAPI benchmark...")
        fastapi_results = benchmark_app("FastAPI", fastapi_url)

        print("\nRunning Flask benchmark...")
        flask_results = benchmark_app("Flask", flask_url)

        output = {"FastAPI": fastapi_results, "Flask": flask_results}
        out_path = HERE / "benchmark_results.json"
        with open(out_path, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\nResults written to {out_path}")

    finally:
        fastapi_proc.terminate()
        flask_proc.terminate()
        fastapi_proc.wait(timeout=5)
        flask_proc.wait(timeout=5)


if __name__ == "__main__":
    main()
