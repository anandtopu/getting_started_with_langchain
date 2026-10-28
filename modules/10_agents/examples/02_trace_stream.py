"""Compare graph updates with streamed message chunks.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/10_agents/examples/02_trace_stream.py --offline
Expected: Updates contain node changes; messages contain chunks and metadata.
Cost: Two short calls; offline no API fee. Streaming does not reduce token cost.
Requires: agents
"""

from langchain.agents import create_agent

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    for mode in ["updates", "messages"]:
        agent = create_agent(
            get_chat_model(
                settings=settings, responses=["Brightwave supports 30-day returns for unused gear."]
            ),
            tools=[],
            system_prompt="Supplied fact: unused gear has a 30-day return window.",
        )
        # KEY IDEA: graph updates and model chunks describe different layers of the same run.
        for event in agent.stream(
            {"messages": [{"role": "user", "content": "Summarize the supplied policy."}]},
            stream_mode=mode,
        ):
            print_text(f"{mode}: {event}")


if __name__ == "__main__":
    run_cli(main)
