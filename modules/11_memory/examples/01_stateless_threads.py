"""Contrast stateless calls with isolated checkpoint threads.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/11_memory/examples/01_stateless_threads.py --offline
Expected: Same-thread history grows; another thread starts fresh.
Cost: Six short calls; offline no API fee.
Requires: agents
"""

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from common.errors import run_cli
from common.lesson import lesson_settings
from common.memory import thread_config
from common.models import get_chat_model
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    for saver in [None, InMemorySaver()]:
        agent = create_agent(get_chat_model(settings=settings), tools=[], checkpointer=saver)
        for thread, text in [
            ("first", "My preferred shipping is standard."),
            ("first", "What did I say?"),
            ("other", "What did I say?"),
        ]:
            # KEY IDEA: the host owns customer/thread scope; a thread ID is not authentication.
            result = agent.invoke(
                {"messages": [{"role": "user", "content": text}]}, thread_config("C001", thread)
            )
            print_text(
                f"saved={saver is not None}, thread={thread}, messages={len(result['messages'])}"
            )
    print_text("Offline replies are fixed; inspect retained messages, not recall quality.")


if __name__ == "__main__":
    run_cli(main)
