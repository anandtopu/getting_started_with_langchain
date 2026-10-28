"""The real LangSmith evaluation runner, local by default and cloud only by explicit call."""

from uuid import uuid4

from langsmith import Client, evaluate
from langsmith.schemas import Example

from common.config import Settings
from common.support_evaluation import score_answer, support_answer


def run_experiment(cases: list[dict], settings: Settings, *, cloud: bool = False) -> list[dict]:
    if not cases:
        raise ValueError("Evaluation needs examples.")
    if cloud and (settings.course_offline or not settings.langsmith_api_key.get_secret_value()):
        raise ValueError("Cloud evaluation requires explicit live settings and a LangSmith key.")
    client = Client(
        api_key=settings.langsmith_api_key.get_secret_value() if cloud else "local-only",
        auto_batch_tracing=False,
    )
    dataset_id = uuid4()
    records = [
        {"inputs": {"question": case["question"], "customer": case["customer"]}, "outputs": case}
        for case in cases
    ]
    if cloud:
        dataset = client.create_dataset("brightwave-support-" + uuid4().hex[:8])
        client.create_examples(dataset_id=dataset.id, examples=records)
        data = dataset.id
    else:
        data = [Example(id=uuid4(), dataset_id=dataset_id, **record) for record in records]

    def target(inputs: dict) -> dict:
        return support_answer(inputs["question"], inputs["customer"], settings)

    def evaluator(run, example) -> dict:
        metrics = score_answer(example.outputs, run.outputs)
        return {
            "key": "all_contracts",
            "score": all(value for value in metrics.values() if value is not None),
        }

    try:
        results = evaluate(
            target,
            data=data,
            evaluators=[evaluator],
            client=client,
            max_concurrency=0,
            upload_results=cloud,
            disable_evaluator_tracing=not cloud,
            experiment_prefix="brightwave-contract",
        )
        return [
            {
                "id": str(row["example"].id),
                "scores": [item.score for item in row["evaluation_results"]["results"]],
            }
            for row in results
        ]
    finally:
        client.close()
