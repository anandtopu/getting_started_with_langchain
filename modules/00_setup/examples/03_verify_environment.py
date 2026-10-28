"""Check the environment without a billable model request.

Run: uv run python modules/00_setup/examples/03_verify_environment.py --offline
Expected: Package versions and OFFLINE CHECK PASSED.
Cost: No generation; live Ollama checks only its installed-model list.
"""

import runpy
import sys

from common.config import ROOT
from common.errors import run_cli
from common.lesson import lesson_settings


def main() -> None:
    settings = lesson_settings()
    old = sys.argv
    try:
        sys.argv = ["check_env.py", *(["--offline"] if settings.course_offline else [])]
        # KEY IDEA: checking credentials locally does not validate a hosted API key.
        runpy.run_path(str(ROOT / "scripts/check_env.py"), run_name="__main__")
    finally:
        sys.argv = old


if __name__ == "__main__":
    run_cli(main)
