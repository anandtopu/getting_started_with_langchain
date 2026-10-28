"""Reopen a durable checkpoint in a fresh Python process.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/11_memory/examples/02_sqlite_checkpoint.py --offline
Expected: A child process sees persisted messages without making a model call.
Cost: One generation; subprocess reads local state only.
Requires: agents
"""

import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver

from common.errors import run_cli
from common.lesson import lesson_settings
from common.memory import thread_config
from common.models import get_chat_model
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    with TemporaryDirectory() as folder:
        path = Path(folder) / "threads.db"
        config = thread_config("C001", "demo")
        with SqliteSaver.from_conn_string(str(path)) as saver:
            agent = create_agent(get_chat_model(settings=settings), tools=[], checkpointer=saver)
            agent.invoke(
                {"messages": [{"role": "user", "content": "Remember standard shipping."}]}, config
            )
        # KEY IDEA: a closed/reopened connection, even in a new process, retains state.
        code = """
from langgraph.checkpoint.sqlite import SqliteSaver
import sys
with SqliteSaver.from_conn_string(sys.argv[1]) as saver:
    checkpoint = saver.get({'configurable': {'thread_id': 'C001:demo'}})
    print(len(checkpoint['channel_values']['messages']))
"""
        result = subprocess.run(
            [sys.executable, "-c", code, str(path)],
            capture_output=True,
            text=True,
            timeout=20,
            check=True,
        )
        print_text("Fresh process retained messages: " + result.stdout.strip())


if __name__ == "__main__":
    run_cli(main)
