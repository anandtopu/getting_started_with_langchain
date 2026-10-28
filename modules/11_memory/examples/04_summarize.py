"""Summarize older history while retaining the current task.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/11_memory/examples/04_summarize.py --offline
Expected: A summary marker replaces older turns; the latest user request survives.
Cost: One summary call plus one answer call; offline no API fee.
Requires: agents
"""

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    summary = get_chat_model(
        settings=settings, responses=["Customer prefers standard shipping; now asks about returns."]
    )
    # KEY IDEA: summarization is another model call and can lose details; inspect the result.
    agent = create_agent(
        get_chat_model(settings=settings),
        tools=[],
        middleware=[
            SummarizationMiddleware(summary, trigger=("messages", 4), keep=("messages", 2))
        ],
    )
    messages = [
        {"role": "user", "content": "I prefer standard shipping."},
        {"role": "assistant", "content": "Recorded."},
        {"role": "user", "content": "I bought a tent."},
        {"role": "assistant", "content": "How can I help?"},
        {"role": "user", "content": "What is the return window?"},
    ]
    result = agent.invoke({"messages": messages})
    for message in result["messages"]:
        print_text(str((message.type, message.content)))


if __name__ == "__main__":
    run_cli(main)
