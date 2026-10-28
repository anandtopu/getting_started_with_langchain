"""Remember customer preferences across separate conversation threads.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/11_memory/use_case/remembering_agent.py --offline
Expected: A second thread retrieves the stored preference using trusted customer context.
Cost: Four short model calls; offline no API fee.
Requires: agents
"""

from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langgraph.checkpoint.sqlite import SqliteSaver

from common.config import ROOT
from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.memory import Preferences, thread_config
from common.models import get_chat_model
from common.pretty import print_text
from common.returns import SupportContext


def main() -> None:
    settings = lesson_settings()
    folder = ROOT / settings.runtime_dir / "remembering-agent"
    folder.mkdir(parents=True, exist_ok=True)
    preferences = Preferences(Path(folder) / "preferences.db")
    if preferences.get("C001") is None:
        preferences.put("C001", "standard")

    @tool
    def read_preference(runtime: ToolRuntime[SupportContext]) -> dict:
        """Read only the authenticated customer's stored shipping preference."""
        return {"shipping": preferences.get(runtime.context.customer_id)}

    with SqliteSaver.from_conn_string(str(Path(folder) / "threads.db")) as saver:
        for thread in ["morning", "evening"]:
            # KEY IDEA: independent conversation history can share customer-scoped preferences.
            agent = create_agent(
                get_chat_model(
                    settings=settings,
                    responses=[
                        tool_request("read_preference", {}),
                        "Use the preference returned by the tool.",
                    ],
                ),
                [read_preference],
                context_schema=SupportContext,
                checkpointer=saver,
            )
            result = agent.invoke(
                {"messages": [{"role": "user", "content": "What shipping do I prefer?"}]},
                thread_config("C001", thread),
                context=SupportContext("C001", Path("unused")),
            )
            print_text(str([m.content for m in result["messages"] if m.type == "tool"]))


if __name__ == "__main__":
    run_cli(main)
