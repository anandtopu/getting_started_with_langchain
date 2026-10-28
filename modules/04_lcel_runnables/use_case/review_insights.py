"""Run sentiment, theme and reply branches over reviews with a low-cost fallback.

Run: uv run python modules/04_lcel_runnables/use_case/review_insights.py --offline
Expected: Three review reports by default; use --all to process all 300 reviews.
Cost: Default nine calls, usually under $0.02; --all is 900 calls, budget $1; offline/local no
API fee.
"""

import argparse
import json

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel

from common.config import ROOT, Settings, get_settings
from common.data import load_csv
from common.errors import run_cli
from common.models import get_chat_model
from common.pretty import print_text
from common.resilience import TRANSIENT_ERRORS


def build_pipeline(settings: Settings) -> Runnable:
    primary_settings = settings.model_copy(update={"model_max_retries": 0})
    cheap_settings = primary_settings.model_copy(
        update={"llm_model": getattr(settings, f"{settings.llm_provider}_chat_model")}
    )
    branches = {}
    for task, fixture in {
        "sentiment": "positive",
        "theme": "comfort",
        "reply": "Thank you for sharing your feedback.",
    }.items():
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"For this Brightwave review, return only {task}. "
                    "Do not invent product facts or promise compensation.",
                ),
                ("human", "{text}"),
            ]
        )
        primary = get_chat_model(settings=primary_settings, responses=[fixture] * 300)
        fallback = get_chat_model(settings=cheap_settings, responses=[fixture] * 300)
        # Retry only transient failures; schema/programming errors should remain visible.
        branches[task] = (
            prompt
            | primary.with_fallbacks([fallback], exceptions_to_handle=TRANSIENT_ERRORS)
            | StrOutputParser()
        )
    return RunnableLambda(lambda row: {"text": row["text"]}) | RunnableParallel(**branches)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--all", action="store_true", help="Process all 300 rows (900 model calls)")
    args = parser.parse_args()
    settings = get_settings()
    if args.offline:
        settings = settings.model_copy(update={"course_offline": True})
    rows = load_csv("reviews.csv")
    selected = rows if args.all else rows[:3]
    results = build_pipeline(settings).batch(selected, config={"max_concurrency": 2})
    output = ROOT / settings.runtime_dir / "review_insights.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    reports = [
        {"review_id": row["review_id"], **result}
        for row, result in zip(selected, results, strict=True)
    ]
    output.write_text("".join(json.dumps(report) + "\n" for report in reports), encoding="utf-8")
    print_text(
        "OFFLINE FIXTURE: outputs do not classify the input."
        if settings.course_offline
        else "LIVE review analysis"
    )
    print_text(
        f"Fallback profile: {getattr(settings, f'{settings.llm_provider}_chat_model')}; "
        "cheaper only when your LLM_MODEL is a more expensive choice."
    )
    print_text(json.dumps(reports, indent=2))


if __name__ == "__main__":
    run_cli(main)
