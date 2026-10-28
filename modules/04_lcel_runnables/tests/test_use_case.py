"""The realistic use case runs offline without changing committed data."""

from common.config import ROOT
from common.testing import execute_script


def test_use_case(tmp_path, monkeypatch):
    monkeypatch.setenv("RUNTIME_DIR", str(tmp_path))
    execute_script(ROOT / "modules/04_lcel_runnables/use_case/review_insights.py", ["--offline"])

    import json

    rows = [
        json.loads(line) for line in (tmp_path / "review_insights.jsonl").read_text().splitlines()
    ]
    assert len(rows) == 3
    assert set(rows[0]) == {"review_id", "sentiment", "theme", "reply"}


def test_review_pipeline_uses_fallback_on_transport_failure(monkeypatch):
    import runpy

    from langchain_core.runnables import RunnableLambda

    from common.config import Settings
    from common.models import get_chat_model

    module = runpy.run_path(str(ROOT / "modules/04_lcel_runnables/use_case/review_insights.py"))
    pipeline_builder = module["build_pipeline"]
    constructions = []

    def failed_primary(value):
        raise TimeoutError("Synthetic transport failure")

    def factory(**kwargs):
        constructions.append(kwargs)
        if len(constructions) % 2:
            return RunnableLambda(failed_primary)
        return get_chat_model(offline=True, responses=["fallback result"])

    monkeypatch.setitem(pipeline_builder.__globals__, "get_chat_model", factory)
    result = pipeline_builder(Settings(course_offline=True)).invoke({"text": "Tent review"})
    assert result == dict.fromkeys(["sentiment", "theme", "reply"], "fallback result")
