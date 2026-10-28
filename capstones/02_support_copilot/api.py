"""Flagship API factory, or a finite no-network health check.

Serve: uv run --extra apps uvicorn common.copilot:copilot_app --factory --host 127.0.0.1 --workers 1
Check: uv run --extra apps python capstones/02_support_copilot/api.py --offline
Expected: local health passes; serving requires distinct runtime tokens. Cost: none. Requires: apps
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient

from common.copilot import copilot_demo
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    with TemporaryDirectory() as directory, TestClient(copilot_demo(Path(directory))) as client:
        print_text(str(client.get("/health").json()))


if __name__ == "__main__":
    run_cli(main)
