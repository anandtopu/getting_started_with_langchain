"""Summarize configuration safely.

Task: Return provider, model and local fields from Settings; never serialize keys or all settings.
Run: uv run python modules/00_setup/solutions/03_stretch.py --offline
Expected: a runnable complete solution demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from common.config import Settings
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def profile(settings: Settings) -> dict:
    return {
        "provider": settings.llm_provider,
        "model": settings.chat_model,
        "local": settings.llm_provider == "ollama",
    }


def main() -> None:
    settings = lesson_settings()
    print_text(str(profile(settings)))


if __name__ == "__main__":
    run_cli(main)
