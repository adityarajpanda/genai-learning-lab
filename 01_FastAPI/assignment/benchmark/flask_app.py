"""Minimal Flask app used as the other side of the FastAPI vs Flask benchmark.

Mirrors fastapi_app.py's three routes as closely as possible, with equivalent
manual request validation in place of Pydantic.
"""

import sys

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/ping")
def ping():
    return jsonify({"status": "ok"})


@app.post("/echo")
def echo():
    data = request.get_json(silent=True) or {}

    if "name" not in data or not isinstance(data["name"], str):
        return jsonify({"detail": "'name' must be a string"}), 422
    if "value" not in data or not isinstance(data["value"], int):
        return jsonify({"detail": "'value' must be an integer"}), 422
    tags = data.get("tags", [])
    if not isinstance(tags, list):
        return jsonify({"detail": "'tags' must be a list"}), 422

    return jsonify({"name": data["name"], "value": data["value"], "tags": tags})


@app.get("/compute")
def compute():
    total = sum(i * i for i in range(2000))
    return jsonify({"total": total})


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8011
    app.run(host="127.0.0.1", port=port, threaded=True)
