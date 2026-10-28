"""Reuse a persisted task result after interrupt, then run an async entrypoint.

Run: uv run --extra agents python modules/14_langgraph/examples/10_functional_api.py --offline
Expected: The drafting task executes once across pause/resume; async workflow returns.
Cost: No model calls. Offline fixtures incur no API fee.
Requires: agents
"""

import asyncio

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.types import Command, interrupt

from common.errors import run_cli
from common.lesson import lesson_settings
from common.memory import thread_config
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    calls = []

    @task
    def draft(topic: str) -> str:
        calls.append(topic)
        return "Brightwave draft: " + topic

    @entrypoint(checkpointer=InMemorySaver())
    def workflow(topic: str) -> dict:
        text = draft(topic).result()
        approved = interrupt({"draft": text})
        if type(approved) is not bool:
            raise ValueError("Review must be boolean")
        return {"draft": text, "approved": approved}

    config = thread_config("C001", "functional")
    workflow.invoke("repairable gear", config)
    # KEY IDEA: entrypoint code restarts, but the completed task result is replayed.
    print_text(str(workflow.invoke(Command(resume=False), config)))
    print_text(f"Draft task executions: {len(calls)}")

    @task
    async def read_topic(topic: str) -> str:
        return "Synthetic research: " + topic

    @entrypoint()
    async def async_workflow(topic: str) -> str:
        return await read_topic(topic)

    print_text(asyncio.run(async_workflow.ainvoke("tent setup")))


if __name__ == "__main__":
    run_cli(main)
