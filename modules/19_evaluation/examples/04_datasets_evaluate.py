"""Run LangSmith evaluate locally, then demonstrate a calibrated-judge boundary.

Run: uv run --extra agents python modules/19_evaluation/examples/04_datasets_evaluate.py --offline
Expected: Two local evaluator rows and an explicitly scripted judge verdict.
Cost: Up to eleven logical live calls; SDK retries may add attempts. Cloud upload is separate.
Requires: agents
"""

from common.errors import run_cli
from common.evaluation import judge_answer
from common.experiments import run_experiment
from common.lesson import lesson_settings
from common.pretty import print_text
from common.support_evaluation import load_cases


def main() -> None:
    settings = lesson_settings()
    # KEY IDEA: upload_results=False uses the real runner without creating a cloud experiment.
    print_text(str(run_experiment(load_cases()[:2], settings)))
    verdict = judge_answer(
        "What is the return window?",
        {"answer": "30 days"},
        "Unused gear within 30 days",
        "Unused gear within 30 days",
        settings,
    )
    print_text(str(verdict.model_dump()))


if __name__ == "__main__":
    run_cli(main)
