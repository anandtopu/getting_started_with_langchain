"""Render the real Streamlit entry point in its application test harness.

Run: uv run --extra apps python modules/18_apps/examples/03_streamlit_chat.py --offline
Expected: The credential prompt renders; no server or real model is contacted.
Cost: No API calls; deterministic local checks. Requires: apps
"""

from streamlit.testing.v1 import AppTest

from common.config import ROOT
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    # KEY IDEA: AppTest executes the same render function as streamlit run.
    app = AppTest.from_file(ROOT / "modules/18_apps/use_case/app.py")
    AppTest.run(app)
    assert not app.exception
    assert app.title[0].value == "Brightwave support"
    print_text(app.info[0].value)


if __name__ == "__main__":
    run_cli(main)
