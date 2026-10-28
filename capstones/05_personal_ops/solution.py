"""Manage local notes/tasks through two real MCP servers with explicit host approval.

Run: uv run --extra agents python capstones/05_personal_ops/solution.py --offline
Expected: approved synthetic actions persist; unapproved mode writes nothing.
Cost: up to five logical calls live; zero offline. Temporary data only. Requires: agents
"""

import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory

from common.errors import run_cli
from common.lesson import lesson_settings
from common.personal_ops import run_ops
from common.pretty import print_text

ACTIONS = [
    {
        "operation": "notes_create",
        "payload": {
            "item_id": "note-1",
            "title": "Brightwave planning",
            "body": "Review synthetic return policy.",
        },
    },
    {
        "operation": "tasks_create",
        "payload": {
            "item_id": "task-1",
            "title": "Check policy citations",
            "body": "Use the handbook.",
        },
    },
]


def run_case(case: dict, settings, directory: Path) -> dict:
    # KEY IDEA: approval is a host decision; no model argument can create its receipt.
    result = asyncio.run(
        run_ops(
            directory,
            settings,
            ACTIONS,
            approved=case["approved"],
            transport=case.get("transport", "memory"),
        )
    )
    passed = (
        len(result["notes"]) == case["expected_notes"]
        and len(result["tasks"]) == case["expected_tasks"]
    )
    return {"id": case["id"], "passed": passed, "result": result}


def main() -> None:
    settings = lesson_settings()
    with TemporaryDirectory() as directory:
        result = run_case(
            {"id": "approved-demo", "approved": True, "expected_notes": 1, "expected_tasks": 1},
            settings,
            Path(directory),
        )
        print_text(str(result))
        if not result["passed"]:
            raise ValueError("Ops acceptance failed.")


if __name__ == "__main__":
    run_cli(main)
