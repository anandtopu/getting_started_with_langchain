"""Guarded Support: actual middleware pauses and transactional synthetic return writes.

Run: uv run --extra agents python checkpoints/03_guarded_support/solution.py --offline
Expected: eight labelled contract cases; report saved under .runtime/guarded_support.json.
Cost: offline no API fees; live up to five generations per case. No payment integration.
"""

import json
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from langgraph.types import Command

from common.config import ROOT, Settings
from common.errors import run_cli
from common.evaluation import save_report
from common.fixtures import tool_request
from common.guardrails import guarded_agent
from common.lesson import lesson_settings
from common.memory import thread_config
from common.pretty import print_text
from common.returns import SupportContext, runtime_orders


def run_case(case: dict, settings: Settings) -> dict:
    """Cases explicitly script model calls; this measures controls, not agent decision quality."""
    with TemporaryDirectory(prefix="brightwave-guarded-") as folder:
        context = SupportContext(
            case["customer"],
            runtime_orders(Path(folder) / "orders.db"),
            inspected_unused=case.get("warehouse_checked", True),
            proof_and_accessories=case.get("warehouse_checked", True),
        )
        calls = [
            tool_request(case["tool"], case["args"], f"call-{i}")
            for i in range(case.get("repeats", 1))
        ]
        agent = guarded_agent(settings, [*calls, "Review the tool outcome. No payment was sent."])
        config = thread_config(context.customer_id, "checkpoint")
        result = agent.invoke(
            {"messages": [{"role": "user", "content": case["question"]}]}, config, context=context
        )
        paused = bool(result.get("__interrupt__"))
        with closing(sqlite3.connect(context.database)) as db:
            before = db.execute(
                "SELECT COUNT(*) FROM returns WHERE idempotency_key=?",
                (case["args"]["idempotency_key"],),
            ).fetchone()[0]
        if paused and case.get("decision"):
            # This benchmark simulates a reviewer; real UI review requires authenticated humans.
            result = agent.invoke(
                Command(resume={"decisions": [{"type": case["decision"]}]}), config, context=context
            )
        with closing(sqlite3.connect(context.database)) as db:
            records = db.execute(
                "SELECT COUNT(*) FROM returns WHERE idempotency_key=?",
                (case["args"]["idempotency_key"],),
            ).fetchone()[0]
        return {
            "id": case["id"],
            "mode": "scripted-contract" if settings.course_offline else "live",
            "paused": paused,
            "records_before_review": before,
            "records": records,
            "tool_results": [m.content for m in result["messages"] if m.type == "tool"],
        }


def main() -> None:
    settings = lesson_settings()
    cases = [
        json.loads(line)
        for line in (Path(__file__).with_name("eval.jsonl"))
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    rows = [run_case(case, settings) for case in cases]
    report = {
        "mode": "scripted-contract" if settings.course_offline else "live",
        "limits": "Scripted trajectories and simulated review; not autonomous-agent quality.",
        "rows": rows,
    }
    save_report(report, ROOT / settings.runtime_dir / "guarded_support.json")
    print_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    run_cli(main)
