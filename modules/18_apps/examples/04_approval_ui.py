"""Exercise the HTTP endpoints behind approve and reject buttons.

Run: uv run --extra apps python modules/18_apps/examples/04_approval_ui.py --offline
Expected: Both reviewed outcomes; a customer review and repeated resume are rejected.
Cost: No API calls; deterministic local checks. Requires: apps
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.release import api_contract


def main() -> None:
    lesson_settings()
    for decision in ("approve", "reject"):
        with TemporaryDirectory() as directory:
            # KEY IDEA: a reviewer role and current interrupt ID are checked on the server.
            result = api_contract(Path(directory), decision)
            print_text(str({"decision": decision, **result}))
            assert all(value for key, value in result.items() if key != "result")


if __name__ == "__main__":
    run_cli(main)
