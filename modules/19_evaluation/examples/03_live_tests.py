"""Expose what a provider capability matrix has and has not verified.

Run: uv run --extra agents python modules/19_evaluation/examples/03_live_tests.py --offline
Expected: A parsed company and an honest four-provider matrix.
Cost: One structured call with selected live provider; no calls offline. Requires: agents
"""

from pydantic import BaseModel

from common.errors import run_cli
from common.fixtures import structured_fixture
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


class Greeting(BaseModel):
    company: str


def main() -> None:
    settings = lesson_settings()
    model = get_chat_model(
        settings=settings, responses=[structured_fixture(Greeting, {"company": "Brightwave"})]
    )
    result = model.with_structured_output(Greeting).invoke("Return company Brightwave.")
    # KEY IDEA: only this selected profile was invoked; adapter support is not live evidence.
    matrix = {
        name: "not tested in this run" for name in ("openai", "anthropic", "google_genai", "ollama")
    }
    matrix[settings.llm_provider] = (
        "scripted parser only" if settings.course_offline else "structured output invoked"
    )
    print_text(str({"result": result.model_dump(), "matrix": matrix}))


if __name__ == "__main__":
    run_cli(main)
