"""Uvicorn factory: uv run --extra apps uvicorn common.web:configured_app --factory.

Run finite check: uv run --extra apps python modules/18_apps/use_case/api.py --offline
Expected: public health and authentication checks. Cost: none. Requires: apps
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.web import demo_app


def main() -> None:
    lesson_settings()
    with TemporaryDirectory() as directory, TestClient(demo_app(Path(directory))) as client:
        assert client.post("/threads").status_code == 401
        print_text(str(client.get("/health").json()))


if __name__ == "__main__":
    run_cli(main)
