"""Separate retrieval hits, answer proxies and optional model-judge verdicts.

Run: uv run --extra rag python modules/09_advanced_rag/examples/07_evaluate.py --offline
Expected: A local metric report and a clearly labelled scripted judge verdict.
Cost: One answer and one judge call; offline judge is scripted and is not scored as quality.
Requires: rag
"""

from common.data import load_jsonl
from common.errors import run_cli
from common.evaluation import answer_metrics, judge_answer, retrieval_hit
from common.knowledge import chunk_documents, policy_documents
from common.lesson import lesson_settings
from common.pretty import print_text
from common.rag import answer_question, context_text
from common.retrieval import LexicalRetriever


def main() -> None:
    # KEY IDEA: Score retrieval and answers separately; scripted judges cannot assess meaning.
    settings = lesson_settings()
    case = load_jsonl("eval/rag.jsonl")[0]
    found = LexicalRetriever(chunk_documents(policy_documents())).search(case["question"])
    answer = answer_question(case["question"], found, settings)
    print_text(str({"retrieval_hit": retrieval_hit(case, found), **answer_metrics(case, answer)}))
    verdict = judge_answer(case["question"], answer, case["answer"], context_text(found), settings)
    print_text(
        (
            "FIXTURE judge: "
            if settings.course_offline
            else "LIVE model judge (needs human calibration): "
        )
        + verdict.model_dump_json()
    )


if __name__ == "__main__":
    run_cli(main)
