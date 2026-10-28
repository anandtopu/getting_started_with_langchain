"""Set token, timeout, retry and sampling limits centrally.

Run: uv run python modules/01_chat_models/examples/05_parameters.py --offline
Expected: Configured limits and a short reply; unsupported sampling parameters are omitted.
Cost: One short hosted call, typically under $0.01; --offline is free.
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message, print_text


def main() -> None:
    settings = lesson_settings().model_copy(
        update={"model_max_tokens": 96, "model_timeout": 20, "model_max_retries": 1}
    )
    # KEY IDEA: Ollama uses num_predict; hosted adapters use max_tokens in our factory.
    print_text("Output cap 96 tokens; timeout 20 seconds; at most 1 transport retry.")
    print_message(
        get_chat_model(settings=settings, temperature=0).invoke(
            "Write one Brightwave greeting. Do not make product or policy claims."
        )
    )


if __name__ == "__main__":
    run_cli(main)
