"""Handbook Q&A with validated page references and an inspectable offline evaluation.

Run: uv run --extra rag python checkpoints/02_handbook_qa/solution.py --offline
Expected: an answer with handbook page citations; --evaluate writes a report.
Cost: one generation per question; offline/local has no API fee.
"""

import argparse
import json

from common.config import ROOT, get_settings
from common.errors import run_cli
from common.evaluation import save_report
from common.handbook import answer_handbook
from common.pretty import print_text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--question", default="What refund amount requires manager approval?")
    parser.add_argument("--evaluate", action="store_true")
    args = parser.parse_args()
    settings = get_settings()
    if args.offline:
        settings = settings.model_copy(update={"course_offline": True})
    if not args.evaluate:
        print_text(json.dumps(answer_handbook(args.question, settings), indent=2))
        return
    cases = [
        json.loads(line)
        for line in (ROOT / "checkpoints/02_handbook_qa/eval.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    rows = []
    for case in cases:
        answer = answer_handbook(case["question"], settings)
        hit = case["page"] in answer["retrieved_pages"] if case["page"] else None
        rows.append({"id": case["id"], "retrieval_hit": hit, "answer": answer})
    report = {
        "mode": "fixture" if settings.course_offline else "live",
        "rows": rows,
        "limits": "Retrieval/page validation only; inspect factual correctness separately.",
    }
    save_report(report, ROOT / settings.runtime_dir / "handbook_evaluation.json")
    print_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    run_cli(main)
