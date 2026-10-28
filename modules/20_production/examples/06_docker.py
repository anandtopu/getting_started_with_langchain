"""Check the health endpoint and inspect the runnable container recipe.

Run: uv run --extra apps python modules/20_production/examples/06_docker.py --offline
Expected: Local health succeeds and the explicit container build command is printed.
Cost: No API calls; deterministic local checks. Requires: apps
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient

from common.config import ROOT
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.web import demo_app


def main() -> None:
    lesson_settings()
    recipe = ROOT / "modules/20_production/use_case/Dockerfile"
    assert "USER 10001" in recipe.read_text(encoding="utf-8")
    with TemporaryDirectory() as directory, TestClient(demo_app(Path(directory))) as client:
        # KEY IDEA: readiness here checks the local app, not a live model/provider account.
        print_text(str(client.get("/health").json()))
    print_text(
        "Build from repository root: docker build -f modules/20_production/use_case/Dockerfile "
        "-t brightwave-course:local ."
    )


if __name__ == "__main__":
    run_cli(main)
