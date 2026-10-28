"""Check the guarded local support application end to end.

Run: uv run --extra apps python modules/18_apps/use_case/support_web.py --offline
Expected: authentication, streaming, review and replay checks pass.
Cost: none; this finite demonstration always uses explicit fixtures. Requires: apps
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.release import api_contract


def main() -> None:
    lesson_settings()
    with TemporaryDirectory() as directory:
        result = api_contract(Path(directory))
        assert all(value for key, value in result.items() if key != "result")
        print_text(str(result))


if __name__ == "__main__":
    run_cli(main)
