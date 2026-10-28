"""Run every lesson offline and assert the important contracts."""

import runpy

import pytest

from common.config import ROOT
from common.testing import execute_script

HERE = ROOT / "modules/04_lcel_runnables"


def load(name: str) -> dict:
    return runpy.run_path(str(HERE / "examples" / (name + ".py")))


@pytest.mark.parametrize("path", sorted((HERE / "examples").glob("*.py")), ids=lambda p: p.stem)
def test_example_runs(path):
    execute_script(path, ["--offline"])


@pytest.mark.parametrize(
    "path",
    sorted((HERE / "exercises").glob("*.py")) + sorted((HERE / "solutions").glob("*.py")),
    ids=lambda p: p.parent.name + "-" + p.stem,
)
def test_exercise_cli_runs(path):
    execute_script(path, ["--offline"])


def test_retry_actually_retries():
    from langchain_core.runnables import RunnableLambda

    function = load("06_resilience")["transient_request"]()
    with pytest.raises(TimeoutError):
        function("ticket")
    assert "attempt 2" in function("ticket")
    retry = RunnableLambda(load("06_resilience")["transient_request"]()).with_retry(
        retry_if_exception_type=(TimeoutError,), stop_after_attempt=2, wait_exponential_jitter=False
    )
    assert "attempt 2" in retry.invoke("ticket")


def test_routing_is_deterministic():
    router = load("05_routing")["router"]()
    assert router.invoke({"priority": "high"}) == "human review"
    assert router.invoke({"priority": "medium"}) == "standard queue"


@pytest.mark.asyncio
async def test_events_and_graph_are_real():
    pipeline = load("08_events_diagram")["pipeline"]()
    events = [event async for event in pipeline.astream_events(" bw-001 ", version="v2")]
    assert events[0]["event"] == "on_chain_start"
    assert events[-1]["event"] == "on_chain_end"
    assert events[-1]["data"]["output"] == "BW-001"
    assert "trim" in pipeline.get_graph().draw_mermaid()


def test_assign_requires_dictionary():
    from langchain_core.runnables import RunnablePassthrough

    with pytest.raises(ValueError, match="dict"):
        RunnablePassthrough.assign(length=lambda row: 1).invoke("text")
