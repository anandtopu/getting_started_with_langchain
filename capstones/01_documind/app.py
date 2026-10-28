"""Streamlit PDF upload and chat, with a finite CLI readiness path.

Run UI: uv run --extra apps streamlit run capstones/01_documind/app.py --server.address 127.0.0.1
Run check: uv run --extra apps python capstones/01_documind/app.py --offline
Expected: UI instructions; the UI defaults to free scripted mode. Requires: apps
Cost: no CLI calls; live PDF embedding/generation requires explicit UI consent.
"""

from common.document_chat import render_document_chat
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    print_text("Run this file with Streamlit; choose the sample handbook or upload your PDF.")


if __name__ == "__main__":
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    if get_script_run_ctx(suppress_warning=True) is not None:
        render_document_chat()
    else:
        run_cli(main)
