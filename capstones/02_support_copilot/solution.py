"""Evaluate the actual flagship HTTP chat path, including SQL and policy-RAG tool traces.

Run: uv run --extra apps python capstones/02_support_copilot/solution.py --offline
Expected: 6/6 complete contracts; the offline quality gate passes.
Cost: up to 30 logical model calls live; HTTP identities are synthetic. Requires: apps
"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient
from langchain_core.messages import messages_from_dict

from common.copilot import copilot_demo
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.release import CUSTOMER, OTHER, headers
from common.support_evaluation import load_cases, score_answer


def run_case(case: dict, settings, directory: Path) -> dict:
    app = copilot_demo(directory)
    app.state.service.settings = settings
    token = CUSTOMER if case["customer"] == "C001" else OTHER
    if case["customer"] not in {"C001", "C002"}:
        raise ValueError("Unknown fixture identity.")
    with TestClient(app) as client:
        thread = client.post("/threads", headers=headers(token)).json()["thread_id"]
        response = client.post(
            f"/threads/{thread}/messages", headers=headers(token), json={"text": case["question"]}
        )
        events = []
        for frame in response.text.strip().split("\n\n"):
            event, data = frame.split("\n", 1)
            events.append((event[7:], json.loads(data[6:])))
        history = client.get(f"/threads/{thread}", headers=headers(token)).json()["messages"]
    messages = messages_from_dict(history)
    answer = {
        "answer": "".join(data["text"] for event, data in events if event == "text"),
        "trajectory": [
            {"name": call["name"], "args": call["args"]}
            for message in messages
            if message.type == "ai"
            for call in message.tool_calls
        ],
        "evidence": [json.loads(message.content) for message in messages if message.type == "tool"],
    }
    metrics = score_answer(case, answer)
    metrics["http_completed"] = response.status_code == 200 and any(
        event == "done" for event, data in events
    )
    return {
        "id": case["id"],
        "answer": answer,
        "metrics": metrics,
        "passed": all(value for value in metrics.values() if value is not None),
    }


def main() -> None:
    settings = lesson_settings()
    cases = load_cases(Path(__file__).with_name("eval.jsonl"))
    with TemporaryDirectory() as directory:
        results = [run_case(case, settings, Path(directory) / case["id"]) for case in cases]
    # KEY IDEA: evaluate the same HTTP path used by the UI, not a separate mock answer function.
    print_text(
        str(
            {
                "passed": sum(row["passed"] for row in results),
                "total": len(results),
                "release_allowed": all(row["passed"] for row in results),
                "cases": results,
            }
        )
    )


if __name__ == "__main__":
    run_cli(main)
