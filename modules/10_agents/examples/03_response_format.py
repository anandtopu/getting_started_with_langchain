"""Compare agent tool-based and provider-native structured final answers.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/10_agents/examples/03_response_format.py --offline
Expected: Both paths return a validated SupportAnswer in structured_response.
Cost: Two generations; unsupported live native schemas fail visibly rather than falling back.
Requires: agents
"""

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy, ToolStrategy
from pydantic import BaseModel

from common.errors import run_cli
from common.fixtures import structured_fixture
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


class SupportAnswer(BaseModel):
    answer: str
    needs_review: bool


def main() -> None:
    settings = lesson_settings()
    values = {"answer": "Unused gear has a 30-day return window.", "needs_review": False}
    for strategy, response in [
        (ToolStrategy(SupportAnswer), structured_fixture(SupportAnswer, values)),
        (ProviderStrategy(SupportAnswer), SupportAnswer(**values).model_dump_json()),
    ]:
        model = get_chat_model(settings=settings, temperature=0, responses=[response])
        # KEY IDEA: structured_response is parsed data; message text is still a separate trace.
        agent = create_agent(
            model,
            tools=[],
            response_format=strategy,
            system_prompt="Answer from this fact: unused gear has a 30-day return window.",
        )
        result = agent.invoke(
            {"messages": [{"role": "user", "content": "What is the return window?"}]},
            {"recursion_limit": 8},
        )
        print_text(str(result["structured_response"]))
    print_text("Offline JSON tests parsing only. Live models must support the selected strategy.")


if __name__ == "__main__":
    run_cli(main)
