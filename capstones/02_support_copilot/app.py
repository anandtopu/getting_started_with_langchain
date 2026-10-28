"""Launch Streamlit with: uv run --extra apps streamlit run capstones/02_support_copilot/app.py.

Run finite check: uv run --extra apps python capstones/02_support_copilot/app.py --offline
Expected: startup guidance. Cost: none for CLI; browser chat may call the configured model.
Requires: apps
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.ui import render


def main() -> None:
    lesson_settings()
    print_text("Start the authenticated API, then run this file with streamlit run.")


if __name__ == "__main__":
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    if get_script_run_ctx(suppress_warning=True) is not None:
        render()
    else:
        run_cli(main)
