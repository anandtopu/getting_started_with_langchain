"""Use the provider-neutral factory built on init_chat_model.

Run: uv run python modules/01_chat_models/examples/01_hello_model.py --offline
Expected: One AIMessage and the selected provider name.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message, print_text


def main() -> None:
    settings = lesson_settings()
    # KEY IDEA: get_chat_model delegates to init_chat_model in common/models.py.
    model = get_chat_model(settings=settings)
    print_text(f"Configured provider: {settings.llm_provider}")
    print_message(model.invoke("Greet a Brightwave customer in one sentence."))


if __name__ == "__main__":
    run_cli(main)
