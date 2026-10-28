"""Reopen a SQLite workflow and replay an idempotent return.

Run: uv run --extra agents python modules/14_langgraph/examples/05_persistence.py --offline
Expected: One return and one outbox row after repeated requests.
Cost: No model calls. Offline fixtures incur no API fee.
Requires: agents
"""

import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from langgraph.checkpoint.sqlite import SqliteSaver

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
            "C008",
            runtime_orders(Path(folder) / "orders.db"),
            inspected_unused=True,
            proof_and_accessories=True,
        )
        request = {
            "order_id": "BW1008",
            "sku": "BW-021",
            "reason": "unused",
            "idempotency_key": "persistent-return",
        }
        config = thread_config("C008", "return")
        # KEY IDEA: durable state is separate from idempotency in the business database.
        for _ in range(2):
            with SqliteSaver.from_conn_string(str(Path(folder) / "graph.db")) as saver:
                graph = build_return_graph(saver)
                result = graph.invoke({"request": request}, config, context=context)
                print_text(result["status"])
        with closing(sqlite3.connect(context.database)) as db:
            print_text(str(db.execute("SELECT COUNT(*) FROM notification_outbox").fetchone()))


if __name__ == "__main__":
    run_cli(main)
