"""Record a reviewed synthetic return and queue one local notification.

Run: uv run --extra agents python modules/14_langgraph/use_case/return_workflow.py --offline
Expected: Pause with no write, then an approved record and one queued notice.
Cost: No model or delivery service calls. Requires: agents
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from common.errors import run_cli
from common.graphs import build_return_graph
from common.lesson import lesson_settings
from common.memory import thread_config
from common.pretty import print_text
from common.returns import SupportContext, runtime_orders


def main() -> None:
    lesson_settings()
    with TemporaryDirectory() as folder:
        context = SupportContext(
            "C001",
            runtime_orders(Path(folder) / "orders.db"),
            inspected_unused=True,
            proof_and_accessories=True,
        )
        config = thread_config("C001", "return")
        with SqliteSaver.from_conn_string(str(Path(folder) / "graph.db")) as saver:
            graph = build_return_graph(saver)
            state = graph.invoke(
                {
                    "request": {
                        "order_id": "BW1001",
                        "sku": "BW-014",
                        "reason": "unused",
                        "idempotency_key": "workflow-demo",
                    }
                },
                config,
                context=context,
            )
            print_text(str(state["__interrupt__"]))
            # KEY IDEA: this is a simulated reviewer, never a model-generated approval.
            result = graph.invoke(Command(resume="approve"), config, context=context)
            print_text(str(result))
            print_text("Notification queued locally, not sent. Temporary demo data is discarded.")


if __name__ == "__main__":
    run_cli(main)
