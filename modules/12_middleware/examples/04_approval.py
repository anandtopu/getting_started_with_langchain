"""Pause a high-value refund, then demonstrate separate approve and reject decisions.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/12_middleware/examples/04_approval.py --offline
Expected: Approval writes once; rejection writes nothing.
Cost: Up to four model calls in the scripted path; offline no API fee. Only disposable ledgers
change.
Requires: agents
"""

import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from langgraph.types import Command

from common.errors import run_cli
from common.fixtures import tool_request
from common.guardrails import guarded_agent
from common.lesson import lesson_settings
from common.memory import thread_config
from common.pretty import print_text
from common.returns import SupportContext, runtime_orders


def main() -> None:
    settings = lesson_settings()
    for decision in ["approve", "reject"]:
        with TemporaryDirectory() as folder:
            context = SupportContext(
                "C001",
                runtime_orders(Path(folder) / "orders.db"),
                inspected_unused=True,
                proof_and_accessories=True,
            )
            agent = guarded_agent(
                settings,
                [
                    tool_request(
                        "approve_refund",
                        {
                            "order_id": "BW1001",
                            "sku": "BW-014",
                            "reason": "unused",
                            "idempotency_key": "approval-demo",
                        },
                    ),
                    "Follow the reviewed tool result; no payment sent.",
                ],
            )
            config = thread_config("C001", decision)
            paused = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": "Request return of BW-014 on BW1001 with key approval-demo.",
                        }
                    ]
                },
                config,
                context=context,
            )
            print_text(str(paused.get("__interrupt__")))
            # KEY IDEA: this is a simulated human decision, never an agent-generated approval.
            if paused.get("__interrupt__"):
                agent.invoke(
                    Command(resume={"decisions": [{"type": decision}]}), config, context=context
                )
            with closing(sqlite3.connect(context.database)) as db:
                count = db.execute(
                    "SELECT COUNT(*) FROM returns WHERE idempotency_key='approval-demo'"
                ).fetchone()[0]
            print_text(f"{decision}: new records={count}")


if __name__ == "__main__":
    run_cli(main)
